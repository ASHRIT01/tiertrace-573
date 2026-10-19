"""Phase 2 diagnosis of dev-bench output against the SILVER labels (AI-made, not human-verified). Dev only.
Usage: python -m tt.eval.diagnose runs/dev_bench_4b_silver.jsonl out.json"""
import difflib
import json
import os
import pickle
import random
import re
import sys
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path

from tt.agent.schemas import Extraction
from tt.eval.devscore import HEADLINE, SUPPLIER_ROLES, _doc, _same, gold_supplier, score
from tt.kind import kind, load_groups
from tt.labels.agree import wilson
from tt.labels.dates import coarse_overlap, parse_span
from tt.labels.protocol import prepare_gold
from tt.norm.aliases import AliasTable
from tt.parse.pdf import extract_text
from tt.parse.sections import norm, split_sections
from tt.verify.dates import parse_date
from tt.verify.verifier import EARLIEST, locate, verify

# split paths: default = dev; Phase 6 sets TT_PDF / TT_GOLD / TT_CACHE (code is identical, only the data differ)
PDF = Path(os.environ.get("TT_PDF", "data/dev_raw"))
GOLD = Path(os.environ.get("TT_GOLD", "data/labels/dev_silver_v1.json"))
CACHE = Path(os.environ.get("TT_CACHE", "runs/diag_cache.pkl"))


def load_world():
    """-> gold list (scoring view), docs {file: Doc}, raw sections {file: {name: text with line breaks}}."""
    if CACHE.exists():
        return pickle.load(open(CACHE, "rb"))
    gold = prepare_gold(json.load(open(GOLD)), PDF)
    from tt.labeldraft import load
    docs, raw, blocks = {}, {}, {}
    for l in gold:
        docs[l["file"]] = _doc(l, PDF)
        raw[l["file"]] = split_sections(extract_text(PDF / l["file"])[0], collapse=False)
        blocks[l["file"]] = load(PDF / l["file"])["block"].name
    CACHE.parent.mkdir(exist_ok=True)
    pickle.dump((gold, docs, raw, blocks), open(CACHE, "wb"))
    return gold, docs, raw, blocks


def load_preds(path):
    return {json.loads(l)["file"]: json.loads(l) for l in open(path)}


# ---- quote normalisation (principled, case-sensitive) -------------------------------------------------------------------
_Q = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", "−": "-", "‐": "-", "‑": "-"})


def qnorm(s: str, dehyph: bool) -> str:
    s = unicodedata.normalize("NFKC", s).translate(_Q)
    s = re.sub(r"(?<=\w)-[ \t]*\n[ \t]*(?=\w)", "" if dehyph else "-", s)
    return re.sub(r"\s+", " ", s).strip()


def qfound(quote: str, text: str) -> bool:
    q = qnorm(quote, True)
    return bool(q) and (q in qnorm(text, True) or q in qnorm(text, False) or qnorm(quote, False) in qnorm(text, False))


def classify_fail(quote: str, section: str, raw: dict) -> str:
    q = qnorm(quote, True)
    if any(qfound(quote, t) for k, t in raw.items() if k != section):
        return "wrong_section"
    frags = [f.strip() for f in re.split(r"\.\.\.|…", quote) if len(f.strip()) > 8]
    if len(frags) > 1 and all(any(qfound(f, t) for t in raw.values()) for f in frags):
        return "truncation(ellipsis)"
    body = qnorm(raw.get(section, ""), True)
    sm = difflib.SequenceMatcher(None, q, body, autojunk=False)
    cov = sum(b.size for b in sm.get_matching_blocks()) / max(1, len(q))
    if cov >= 0.6:
        return "paraphrase"
    return "other"


# ---- claims -> right / wrong / unlabelled vs silver -----------------------------------------------------------------------
def gold_names(l):
    names = []
    for c in l["claims"]:
        if c["id"] == "S1" and c["status"] == "SUPPORTED":
            names.append(c["label"].split(": ", 1)[1] if ": " in c.get("label", "") else c.get("name", ""))
        if c["id"] == "S2" and c["status"] == "SUPPORTED":
            names.append(gold_supplier(l)[0])
    names += l["upstream"].get("names", [])
    return [n for n in names if n]


def event_spans(l):
    out = []
    for e in l["events"]:
        sp = e.get("span")
        if sp and not e.get("date_inferred"):
            from tt.labels.dates import Span
            out.append((Span(date.fromisoformat(sp["start"]), date.fromisoformat(sp["end"]), sp["granularity"]), e["type"]))
    return out


def pred_span(e, filing, years):
    sp = parse_span(e.date_text or "", years=years or None, filing=filing)
    return None if sp is None or sp.inferred else sp


def company_class(c, l, doc, groups):
    gn = gold_names(l)
    if any(_same(c.name, g) for g in gn):
        return "right"
    isf = kind(c.name, doc.filer, groups)[0] != "external"
    if isf or not locate(c.name, doc.full_text):
        return "wrong"
    return "unlabelled"


def event_class(e, l, doc, years):
    sp = pred_span(e, doc.filing_date, years)
    if sp is None:
        return "wrong:date_unparsed"
    ov = [t for gs, t in event_spans(l) if gs.granularity != "fuzzy" and coarse_overlap(gs, sp)]
    if not ov:
        return "wrong:extra"
    return "right" if e.type in ov else "wrong:type"


def years_of(ex):
    ys = set()
    for e in ex.events:
        s = parse_span(e.date_text or "")
        if s and not s.inferred and not s.year_from_context and s.granularity != "range":
            ys.add(s.start.year)
    return ys


# ---- per-claim verifier flags (mirror tt/verify/verifier.py; consistency-checked against verify()) -------------------------
def flags(ex, doc, aliases, v1=None, block_name=None, new=False):
    """-> {'company': [set of codes per company], 'event': [...], 'filing': [codes]}"""
    f = {"company": [set() for _ in ex.companies], "event": [set() for _ in ex.events], "filing": []}
    filer = norm(doc.filer)
    if new:
        from tt.verify.extra import date_errors, masked_doc
        md = masked_doc(doc, block_name)
        ok1 = lambda ev: locate(ev.quote, md.sections.get(ev.section, "")) is not None
    else:
        ok1 = v1 or (lambda ev: locate(ev.quote, doc.sections.get(ev.section, "")) is not None)
    for i, c in enumerate(ex.companies):
        if not ok1(c.evidence): f["company"][i].add("V1")
        full = doc.full_text
        if not (locate(c.name, full) or aliases.resolve(c.name)): f["company"][i].add("V2a")
        if c.role != "FILER" and norm(c.name) == filer and not (new and norm(c.name) == norm(block_name or "\0")): f["company"][i].add("V2b")
    dated = []
    for i, e in enumerate(ex.events):
        if not ok1(e.evidence): f["event"][i].add("V1")
        d = parse_date(e.date_text, anchor=doc.filing_date)
        bad = bool(date_errors(type("X", (), {"events": [e]})(), doc)) if new else (d is None or d < EARLIEST or d > doc.filing_date)
        if bad: f["event"][i].add("V3")
        elif d is not None and d >= EARLIEST: dated.append((d, e.type))
    if ex.locus_evidence and not ok1(ex.locus_evidence): f["filing"].append("V1-locus")
    if ex.locus_status == "SUPPORTED" and ex.locus_evidence is None: f["filing"].append("V1-locus-missing")
    order = ["SUPPLIER_NOTICE", "FILER_AWARENESS", "DECISION", "NHTSA_FILING"]
    ranks = [(d, order.index(t)) for d, t in dated if t in order]
    if any(r1 < r2 and d1 > d2 for d1, r1 in ranks for d2, r2 in ranks): f["filing"].append("V3-order")
    if doc.cause_is_nr and ex.cause_reported: f["filing"].append("V4")
    known = {norm(c.name) for c in ex.companies} | {filer}
    f["filing"] += ["V5"] * sum(norm(p) not in known for p in ex.supply_path)
    return f


def analyse(preds_path, out_path, new=False):
    gold, docs, raw, blocks = load_world()
    P = load_preds(preds_path)
    groups, aliases = load_groups(), AliasTable()
    R = {"n": len(gold)}
    exs = {l["file"]: Extraction.model_validate(P[l["file"]]["extraction"]) for l in gold if P[l["file"]].get("extraction")}
    sc = score(gold, list(P.values()), PDF)
    R["score"] = {k: v for k, v in sc.items()}
    k, n = sc["s2_recovered"], sc["s2_gold_supported"]
    R["s2_recovery"] = {"k": k, "n": n, "wilson95": wilson(k, n)}
    # consistency: my per-claim flags reproduce verify()
    mism, tot = 0, Counter()
    claim_rows = []   # (kind, class, flags set)
    quote_total = quote_old = quote_new = 0
    resid, resid_examples = Counter(), []
    v2_match = Counter()
    event_rows = []
    for l in gold:
        f = l["file"]; ex = exs.get(f)
        if ex is None: continue
        doc = docs[f]; years = years_of(ex)
        fl = flags(ex, doc, aliases, block_name=blocks[f], new=new)
        n_old = sum(1 for e in verify(ex, doc, aliases) if e.startswith(("V1", "V2", "V3")))
        n_mine = sum(len(s) for s in fl["company"]) + sum(len(s) for s in fl["event"]) + sum(1 for x in fl["filing"] if x in ("V1-locus", "V1-locus-missing", "V3-order"))
        mism += (n_old != n_mine) and not new
        for c, s in zip(ex.companies, fl["company"]):
            cls = company_class(c, l, doc, groups)
            claim_rows.append(("company", cls, s))
            if "V2b" in s and cls == "right": v2_match["rejected_but_matches_silver"] += 1
            if "V2b" in s: v2_match["V2b_total"] += 1
        for e, s in zip(ex.events, fl["event"]):
            claim_rows.append(("event", event_class(e, l, doc, years), s))
        for ev in [c.evidence for c in ex.companies] + [e.evidence for e in ex.events] + ([ex.locus_evidence] if ex.locus_evidence else []):
            quote_total += 1
            old = locate(ev.quote, doc.sections.get(ev.section, "")) is not None
            q_ok = qfound(ev.quote, raw[f].get(ev.section, ""))
            quote_old += old; quote_new += q_ok
            if not q_ok:
                cl = classify_fail(ev.quote, ev.section, raw[f]); resid[cl] += 1
                if len(resid_examples) < 400: resid_examples.append((cl, f, ev.section, ev.quote[:160]))
        # events vs silver
        gs = [(s, t) for s, t in event_spans(l) if s.granularity != "fuzzy" and t in HEADLINE]
        used, rows = set(), []
        ps = [(pred_span(e, doc.filing_date, years), e) for e in ex.events]
        for g, gt in gs:
            hit = next((j for j, (p, e) in enumerate(ps) if j not in used and p and e.type == gt and coarse_overlap(g, p)), None)
            if hit is not None: used.add(hit); rows.append("matched"); continue
            hit = next((j for j, (p, e) in enumerate(ps) if j not in used and p and coarse_overlap(g, p)), None)
            if hit is not None: used.add(hit); rows.append("type_mismatch"); continue
            rows.append("missing")
        for j, (p, e) in enumerate(ps):
            if j in used: continue
            rows.append("date_format" if p is None else "extra")
        event_rows += rows
    R["verify_consistency_mismatched_filings"] = mism
    R["quote_check"] = {"total": quote_total, "old_pass": quote_old, "new_pass": quote_new, "residual": dict(resid)}
    R["quote_residual_examples"] = random.Random(0).sample(resid_examples, min(20, len(resid_examples)))
    R["event_miss_classes"] = dict(Counter(event_rows))
    # verifier precision/recall at catching wrong claims (company+event claims)
    tab = {}
    for code in ("V1", "V2a", "V2b", "V3", "ANY"):
        fl_ = [(c, s) for c, s in ((cls, s) for _, cls, s in claim_rows) if (code in s if code != "ANY" else bool(s))]
        wrong = sum(1 for cls, _ in fl_ if cls.startswith("wrong")); right = sum(1 for cls, _ in fl_ if cls == "right"); unl = sum(1 for cls, _ in fl_ if cls == "unlabelled")
        allwrong = sum(1 for _, cls, _ in claim_rows if cls.startswith("wrong"))
        tab[code] = {"failed": len(fl_), "true_reject(wrong)": wrong, "false_reject(right)": right, "unlabelled": unl,
                     "precision": wrong / (wrong + right) if wrong + right else None, "recall": wrong / allwrong if allwrong else None}
    R["verifier_audit"] = tab
    R["claim_classes"] = dict(Counter((k, c) for k, c, _ in claim_rows).most_common())
    R["claim_classes"] = {f"{a}:{b}": v for (a, b), v in Counter((k, c) for k, c, _ in claim_rows).items()}
    R["v2"] = dict(v2_match)
    R["filings_failing"] = {"V4": sum("V4" in flags(exs[l["file"]], docs[l["file"]], aliases)["filing"] for l in gold if l["file"] in exs)}
    # silver S1 supported where supplier is filer/affiliate
    s1f = 0; s1n = 0
    for l in gold:
        for c in l["claims"]:
            if c["id"] == "S1" and c["status"] == "SUPPORTED":
                s1n += 1; nm = c["label"].split(": ", 1)[1]
                s1f += kind(nm, docs[l["file"]].filer, groups)[0] != "external"
    R["silver_S1_supported"] = {"n": s1n, "filer_or_affiliate": s1f}
    # slow filings
    R["over_120s"] = [{"file": r["file"], "seconds": round(r["seconds"], 1), "prompt_tokens": r.get("prompt_eval_count"), "output_tokens": r.get("eval_count")}
                      for r in P.values() if r["seconds"] > 120]
    json.dump(R, open(out_path, "w"), indent=1, default=str)
    return R


def side_by_side(preds_path, k=20):
    gold, docs, raw, blocks = load_world(); P = load_preds(preds_path)
    out = []
    for l in random.Random(0).sample(gold, k):
        ex = Extraction.model_validate(P[l["file"]]["extraction"])
        out.append(f"### {l['file']}\nsilver:")
        out += [f"  - {e.get('date_text')} | {e['type']} | {e['quote'][:80]}" for e in l["events"]]
        out.append("model:")
        out += [f"  - {e.date_text} | {e.type} | {e.evidence.quote[:80]}" for e in ex.events]
    return "\n".join(out)


if __name__ == "__main__":
    R = analyse(sys.argv[1], sys.argv[2], new=len(sys.argv) > 3 and sys.argv[3] == "new")
    print(json.dumps({k: v for k, v in R.items() if k not in ("score", "quote_residual_examples")}, indent=1, default=str))


def event_split(gold, docs, preds_ext):
    """Event metrics over ALL scored silver events (headline + OTHER) and all predicted events.
    Pairing prefers the same type, then any type, one-to-one on span overlap. -> date_only, date_type, type_acc_given_date."""
    tp_d = tp_t = n_pred = n_gold = 0
    for l in gold:
        ex = preds_ext.get(l["file"])
        if ex is None: continue
        doc = docs[l["file"]]; years = years_of(ex)
        gs = [(s, t) for s, t in event_spans(l) if s.granularity != "fuzzy"]
        ps = [(pred_span(e, doc.filing_date, years), e.type) for e in ex.events]
        ps = [(p, t) for p, t in ps if p is not None and p.granularity != "fuzzy"]
        n_gold += len(gs); n_pred += len(ps); used = set()
        for g, gt in gs:
            j = next((j for j, (p, t) in enumerate(ps) if j not in used and t == gt and coarse_overlap(g, p)), None)
            if j is None:
                j = next((j for j, (p, t) in enumerate(ps) if j not in used and coarse_overlap(g, p)), None)
            if j is not None:
                used.add(j); tp_d += 1; tp_t += ps[j][1] == gt
    f1 = lambda tp: (2 * tp / (n_pred + n_gold)) if n_pred + n_gold else float("nan")
    return {"gold_events": n_gold, "pred_events": n_pred, "date_matched": tp_d, "date_type_matched": tp_t,
            "date_only_F1": f1(tp_d), "date_type_F1": f1(tp_t), "type_acc_given_date": tp_t / tp_d if tp_d else float("nan")}
