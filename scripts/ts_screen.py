"""TS-1 timeliness screen: compute (protocol tag ts-protocol-1, reports/TS_PROTOCOL.md). Pure Python, deterministic. No model run.
Silver reference (AI-generated, not human-verified). A descriptive screening signal, not a legal finding.
  python scripts/ts_screen.py  -> reports/ts/phase_7_timeliness.json (aggregates only)
Runs tests/test_ts_screen.py first and writes nothing if any test fails. Needs runs/ts/<split>_agent_events.json (scripts/ts_gate.py)."""
import io
import json
import re
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ts_inventory import LISTINGS, SPLITS, TYPE_HDR, campaign_of, sub_dates  # noqa: E402
from ts_lib import anchor, anon_labels, flag, kappa_pabak, load_holidays, quantile, resolve, wd_between, wilson  # noqa: E402
import tt.eval.amend1 as AM  # noqa: E402  (amendment TS-A1: the amendment-1 crash-only parse_span guard, applied at import)
import tt.labels.events as EV  # noqa: E402
from tt.data.flat import FIELDS  # noqa: E402
from tt.eval.riskcov import cluster_bootstrap  # noqa: E402
from tt.labels.events import chronology_years  # noqa: E402
from tt.parse.pdf import extract_text  # noqa: E402
from tt.parse.sections import split_sections  # noqa: E402

ST = ["FLAGGED", "NOT_FLAGGED", "INDETERMINATE", "NO_DECISION_DATE"]
HOL = load_holidays()
NOTE = "silver reference (AI-generated, not human-verified); descriptive screening signal, not a legal finding"


# ------------------------------------------------------------------------------------------------ data
def guard_needed(chron: str) -> bool:
    """True if the unguarded frozen parse_span would crash inside chronology_years for this chronology (amendment TS-A1)."""
    EV.parse_span = AM._ORIG_PARSE
    try:
        chronology_years(chron)
        return False
    except (AttributeError, ValueError):
        return True
    finally:
        EV.parse_span = AM.safe_parse_span


def load_filings():
    listing = defaultdict(list)
    for p in LISTINGS:
        for l in open(p):
            r = json.loads(l); listing[r["campaign"]].append(r)
    camps = {}
    for s in SPLITS:
        for x in json.load(open(f"config/{s}_selection.json"))["filings"]:
            camps[campaign_of(x["file"])] = (s, x)
    flat = {}
    with zipfile.ZipFile("data/flat/FLAT_RCL_POST_2010.zip") as z, z.open(z.namelist()[0]) as raw:
        for line in io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""):
            f = line.rstrip("\r\n").split("\t")
            if len(f) == 29 and re.fullmatch(r"\d{2}[VECT]\d{6}", f[1].strip()) and f[1][:6] in camps and f[1][:6] not in flat:
                flat[f[1][:6]] = dict(zip(FIELDS, f))
    silver = {s: {x["file"]: x for x in json.load(open(f"data/labels/{s}_silver.json"))} for s in SPLITS}
    agent = {s: json.load(open(f"runs/ts/{s}_agent_events.json")) for s in SPLITS}
    out = []
    for c, (s, x) in camps.items():
        fn = x["file"]
        t, _ = extract_text(f"{SPLITS[s]}/{fn}")
        ds = sub_dates(t)
        rc = flat[c]["RCDATE"]
        hd = sorted(set(TYPE_HDR.findall(t)))
        h = hd[0].upper() if len(hd) == 1 else None
        titles = {"DEFECT" if "defect notice" in r["summary"].lower() else "NONCOMPLIANCE" for r in listing[c]
                  if "defect notice" in r["summary"].lower() or "noncompliance notice" in r["summary"].lower()}
        ti = titles.pop() if len(titles) == 1 else None
        if h:
            typ, tsrc = h, "header"
        elif ti:
            typ, tsrc = ti, "title"
        else:
            typ, tsrc = ("NONCOMPLIANCE" if flat[c]["FMVSS"].strip() else "DEFECT"), "fmvss_proxy"
        ver = [r for r in listing[c] if r["fileName"] == fn][0]
        sev = [{"date_text": e.get("date_text") or "", "type": e["type"], "quote": e.get("quote") or ""}
               for e in silver[s][fn]["events"] if not e.get("contested")]
        av = agent[s][fn]
        aev = [e for e in av["events"] if e["accepted"]]
        out.append({"split": s, "campaign": c, "cluster": re.sub(r"\s+", " ", x["filer"].lower()).strip(),
                    "sub": ds[0] if ds else None, "rcdate": date(int(rc[:4]), int(rc[4:6]), int(rc[6:])) if re.fullmatch(r"\d{8}", rc) else None,
                    "years": chronology_years(chron := split_sections(t, collapse=False).get("chronology", "")), "guard_needed": guard_needed(chron),
                    "type": typ, "type_src": tsrc, "original": bool(ver["is_original"]),
                    "influenced_by": flat[c]["INFLUENCED_BY"] or "(empty)", "rcltypecd": flat[c]["RCLTYPECD"],
                    "silver": sev, "agent": aev, "agent_has_decision_claim": any(e["type"] == "DECISION" for e in aev)})
    return sorted(out, key=lambda r: (r["split"], r["campaign"]))


# ------------------------------------------------------------------------------------------------ screen one filing
def screen(events, f, fd, mode="latest_decision", count="wd"):
    """-> dict(status, gap_min, gap_max, gap_mid, lo, hi, precision, ambiguous) for one side of one filing."""
    if fd is None:
        return {"status": "NO_FILING_DATE"}
    iv, _ = anchor(events, fd, f["campaign"], f["years"], mode=mode)
    if iv is None:
        return {"status": "NO_DECISION_DATE"}
    hol = HOL if count == "wd" else set()
    wk = count != "calendar"
    gmin, gmax = wd_between(iv.hi, fd, hol, wk), wd_between(iv.lo, fd, hol, wk)
    return {"status": flag(gmin, gmax), "gap_min": gmin, "gap_max": gmax, "gap_mid": (gmin + gmax) / 2, "lo": iv.lo, "hi": iv.hi,
            "precision": iv.precision, "ambiguous": iv.ambiguous}


VARIANTS = {"primary": {}, "calendar_days": {"count": "calendar"}, "holidays_not_excluded": {"count": "wd_noholiday"},
            "earliest_decision": {"mode": "earliest_decision"}, "latest_any_event": {"mode": "latest_any"},
            "lexicon_event": {"mode": "latest_lexicon"}, "rcdate_as_filing_date": {"fd": "rcdate"}}


def run_variant(F, name):
    v = VARIANTS[name]
    for f in F:
        fd = f["rcdate"] if v.get("fd") == "rcdate" else f["sub"]
        kw = {"mode": v.get("mode", "latest_decision"), "count": v.get("count", "wd")}
        f.setdefault("ref", {})[name] = screen(f["silver"], f, fd, **kw)
        f.setdefault("agt", {})[name] = screen(f["agent"], f, fd, **kw)


# ------------------------------------------------------------------------------------------------ statistics helpers
def share_ci(F, pred):
    k, n = sum(1 for f in F if pred(f)), len(F)
    wl, wh = wilson(k, n)
    _, bl, bh = cluster_bootstrap([(f, None, f["cluster"]) for f in F], lambda it: sum(1 for x in it if pred(x[0])) / len(it) if it else float("nan"))
    return {"k": k, "n": n, "share": k / n if n else float("nan"), "wilson95": [wl, wh], "cluster_boot95": [bl, bh]}


def boot(F, stat):
    p, lo, hi = cluster_bootstrap([(f, None, f["cluster"]) for f in F], lambda it: stat([x[0] for x in it]))
    return {"value": p, "cluster_boot95": [lo, hi]}


def dist(xs):
    return {"n": len(xs), "median": quantile(xs, .5), "p25": quantile(xs, .25), "p75": quantile(xs, .75), "p90": quantile(xs, .9),
            "min": min(xs) if xs else None, "max": max(xs) if xs else None}


def table_a(F, side="ref", v="primary"):
    S = [f[side][v] for f in F]
    dec = [x for x in S if x["status"] in ("FLAGGED", "NOT_FLAGGED", "INDETERMINATE")]
    return {"N": len(F), "n_no_filing_date": sum(x["status"] == "NO_FILING_DATE" for x in S), "n_with_decision_date": len(dec),
            "gap_mid": dist([x["gap_mid"] for x in dec]), "gap_min": dist([x["gap_min"] for x in dec]), "gap_max": dist([x["gap_max"] for x in dec]),
            "status": {st: share_ci(F, lambda f, st=st: f[side][v]["status"] == st) for st in ST},
            "anchor_ambiguous": sum(x.get("ambiguous", False) for x in dec), "anchor_precision": dict(Counter(x["precision"] for x in dec))}


def table_b(F, v="primary"):
    N = len(F)
    unk = lambda f: f["agt"][v]["status"] in ("NO_DECISION_DATE", "INDETERMINATE")
    cc = [f for f in F if f["agt"][v]["status"] != "NO_DECISION_DATE"]
    return {"N": N,
            "coverage": share_ci(F, lambda f: f["agt"][v]["status"] != "NO_DECISION_DATE"),
            "abstained_no_accepted_decision_claim": sum(1 for f in F if not f["agent_has_decision_claim"]),
            "no_decision_date_total": sum(1 for f in F if f["agt"][v]["status"] == "NO_DECISION_DATE"),
            "status_counts": dict(Counter(f["agt"][v]["status"] for f in F)),
            "complete_case_flagged": share_ci(cc, lambda f: f["agt"][v]["status"] == "FLAGGED") if cc else None,
            "complete_case_indeterminate": share_ci(cc, lambda f: f["agt"][v]["status"] == "INDETERMINATE") if cc else None,
            "manski_lower": boot(F, lambda G: sum(f["agt"][v]["status"] == "FLAGGED" for f in G) / len(G) if G else float("nan")),
            "manski_upper": boot(F, lambda G: sum(f["agt"][v]["status"] == "FLAGGED" or unk(f) for f in G) / len(G) if G else float("nan")),
            "reference_flagged_share": sum(f["ref"][v]["status"] == "FLAGGED" for f in F) / N if N else float("nan")}


def table_c(F, v="primary"):
    B = [f for f in F if f["ref"][v]["status"] != "NO_DECISION_DATE" and f["agt"][v]["status"] != "NO_DECISION_DATE"]
    cats = ["FLAGGED", "NOT_FLAGGED", "INDETERMINATE"]
    tab = {r: {a: sum(1 for f in B if f["ref"][v]["status"] == r and f["agt"][v]["status"] == a) for a in cats} for r in cats}

    def same_iv(G):
        return sum((f["ref"][v]["lo"], f["ref"][v]["hi"]) == (f["agt"][v]["lo"], f["agt"][v]["hi"]) for f in G) / len(G) if G else float("nan")

    def same_day(G):
        return sum(f["ref"][v]["lo"] == f["ref"][v]["hi"] == f["agt"][v]["lo"] == f["agt"][v]["hi"] for f in G) / len(G) if G else float("nan")

    def prec(G):
        tp = sum(f["agt"][v]["status"] == "FLAGGED" and f["ref"][v]["status"] == "FLAGGED" for f in G)
        pp = sum(f["agt"][v]["status"] == "FLAGGED" for f in G)
        return tp / pp if pp else float("nan")

    def rec(G):
        tp = sum(f["agt"][v]["status"] == "FLAGGED" and f["ref"][v]["status"] == "FLAGGED" for f in G)
        rp = sum(f["ref"][v]["status"] == "FLAGGED" for f in G)
        return tp / rp if rp else float("nan")

    pairs = lambda G: [(f["ref"][v]["status"], f["agt"][v]["status"]) for f in G]
    d = [abs(f["agt"][v]["gap_mid"] - f["ref"][v]["gap_mid"]) for f in B]
    n_ref_flag = sum(f["ref"][v]["status"] == "FLAGGED" for f in B)
    return {"n_both": len(B), "identical_interval": boot(B, same_iv), "same_day_both_day_precision": boot(B, same_day),
            "abs_diff_gap_mid_wd": {**dist(d), "share_0": sum(x == 0 for x in d) / len(d) if d else None,
                                     "share_le_5": sum(x <= 5 for x in d) / len(d) if d else None},
            "flag_table_rows_reference_cols_agent": tab,
            "precision_agent_flagged": boot(B, prec), "recall_agent_flagged": boot(B, rec),
            "kappa": boot(B, lambda G: kappa_pabak(pairs(G))[0]), "pabak": boot(B, lambda G: kappa_pabak(pairs(G))[1]),
            "n_reference_flagged": n_ref_flag, "unstable": n_ref_flag < 10}


def audit(F, side):
    """(e): share of filings with an order inconsistency, an event after filing, a DECISION > 10 years before filing (dated events only)."""
    chain = {"FILER_AWARENESS": 0, "INVESTIGATION_START": 1, "DECISION": 2}
    res = {"order_inconsistency": [], "event_after_filing": [], "decision_over_10y_before": []}
    for f in F:
        fd = f["sub"]
        evs = []
        for e in f[side]:
            iv = resolve(e["date_text"], fd, f["years"])
            if iv is not None:
                evs.append((e["type"], iv))
        ch = [(chain[t], iv) for t, iv in evs if t in chain]
        bad = any(a[0] < b[0] and a[1].lo > b[1].hi for a in ch for b in ch) or any(t == "DECISION" and iv.lo > fd for t, iv in evs)
        try:
            ten = fd.replace(year=fd.year - 10)
        except ValueError:
            ten = fd.replace(year=fd.year - 10, day=28)
        res["order_inconsistency"].append(bad)
        res["event_after_filing"].append(any(iv.lo > fd for _, iv in evs))
        res["decision_over_10y_before"].append(any(t == "DECISION" and iv.hi < ten for t, iv in evs))
    n = len(F)
    return {k: {"k": sum(x), "n": n, "share": sum(x) / n if n else float("nan"), "wilson95": list(wilson(sum(x), n))} for k, x in res.items()}


def last_event_is_decision(f, side):
    fd = f["sub"]
    ivs = []
    for e in f[side]:
        iv = resolve(e["date_text"], fd, f["years"])
        if iv is not None and iv.lo <= fd:
            ivs.append((iv.hi, iv.lo, e["type"]))
    if not ivs:
        return None
    top = max((h, l) for h, l, _ in ivs)
    return any((h, l) == top and t == "DECISION" for h, l, t in ivs)


def rc_vs_sub(F):
    d = [(f["rcdate"] - f["sub"]).days for f in F if f["rcdate"] and f["sub"]]
    return {"n": len(d), "equal_share": sum(x == 0 for x in d) / len(d) if d else None, "below_0": sum(x < 0 for x in d),
            "equal_0": sum(x == 0 for x in d), "above_0": sum(x > 0 for x in d),
            "min": min(d) if d else None, "p10": quantile(d, .1), "median": quantile(d, .5), "p90": quantile(d, .9), "max": max(d) if d else None}


# ------------------------------------------------------------------------------------------------ main
def main():
    t = subprocess.run([sys.executable, "-m", "pytest", "tests/test_ts_screen.py", "-q"], capture_output=True, text=True)
    print(t.stdout.strip().splitlines()[-1])
    if t.returncode != 0:
        print(t.stdout); sys.exit("unit tests failed: no result written")
    F_all = load_filings()
    for name in VARIANTS:
        run_variant(F_all, name)
    defect = [f for f in F_all if f["type"] == "DEFECT"]
    nonc = [f for f in F_all if f["type"] == "NONCOMPLIANCE"]
    groups = {"testA": lambda f: f["split"] == "testA", "testB": lambda f: f["split"] == "testB", "unseen": lambda f: f["split"] == "unseen",
              "pooled": lambda f: True}
    R = {"note": NOTE, "protocol": "ts-protocol-1", "tests": t.stdout.strip().splitlines()[-1],
         "population": {"all_filings": len(F_all), "defect": len(defect), "noncompliance": len(nonc),
                        "type_source": {f"{s}|{ty}|{src}": n for (s, ty, src), n in sorted(Counter((f["split"], f["type"], f["type_src"]) for f in F_all).items())},
                        "filing_date_source": dict(Counter(f"{f['split']}|{'submission_date' if f['sub'] else 'NO_FILING_DATE'}" for f in F_all))},
         "a_reference": {}, "a_noncompliance_reference": {}, "b_agent": {}, "c_agreement": {}, "d_sensitivity": {}, "e_audit": {}, "f_descriptive": {}}
    for g, sel in groups.items():
        G = [f for f in defect if sel(f)]
        H = [f for f in nonc if sel(f)]
        R["a_reference"][g] = table_a(G)
        R["a_noncompliance_reference"][g] = table_a(H) if H else None
        R["b_agent"][g] = table_b(G)
        R["c_agreement"][g] = table_c(G)
        R["e_audit"][g] = {"silver": audit(G, "silver"), "agent": audit(G, "agent")}
        sens = {}
        for name in VARIANTS:
            if name == "primary":
                continue
            sens[name] = {side: {"changed_vs_primary": sum(f[side][name]["status"] != f[side]["primary"]["status"] for f in G),
                                 "N": len(G), "changed_share": sum(f[side][name]["status"] != f[side]["primary"]["status"] for f in G) / len(G) if G else None,
                                 "status_counts": dict(Counter(f[side][name]["status"] for f in G))} for side in ("ref", "agt")}
        for lab, pred in [("original_version_only", lambda f: f["original"]), ("amended_version_only", lambda f: not f["original"]),
                          ("type_from_document_only (proxy-typed dropped)", lambda f: f["type_src"] != "fmvss_proxy")]:
            S = [f for f in G if pred(f)]
            sens[lab] = {"N": len(S), "ref_status_counts": dict(Counter(f["ref"]["primary"]["status"] for f in S)),
                         "agt_status_counts": dict(Counter(f["agt"]["primary"]["status"] for f in S)),
                         "ref_flagged_share": share_ci(S, lambda f: f["ref"]["primary"]["status"] == "FLAGGED") if S else None}
        R["d_sensitivity"][g] = sens
        led = {side: [last_event_is_decision(f, side) for f in G] for side in ("silver", "agent")}
        R["f_descriptive"][g] = {
            "last_dated_event_is_decision": {side: {"k": sum(1 for x in led[side] if x), "n_with_dated_event": sum(1 for x in led[side] if x is not None), "N": len(G)}
                                             for side in led},
            "rcdate_minus_submission_calendar_days": {"all": rc_vs_sub(G), "original": rc_vs_sub([f for f in G if f["original"]]),
                                                      "amended": rc_vs_sub([f for f in G if not f["original"]])}}
    P = defect
    R["f_descriptive"]["strata_pooled"] = {
        k: {val: {"N": len(S), **{st: share_ci(S, lambda f, st=st: f["ref"]["primary"]["status"] == st) for st in ST}}
            for val in sorted({f[k] for f in P}) for S in [[f for f in P if f[k] == val]]}
        for k in ("influenced_by", "rcltypecd")}
    cnt = Counter(f["cluster"] for f in P)
    lab = anon_labels(dict(cnt))
    R["f_descriptive"]["manufacturers_n_ge_10_pooled"] = {
        lab[c]: {"N": n, **{st: sum(f["ref"]["primary"]["status"] == st for f in P if f["cluster"] == c) for st in ST}}
        for c, n in sorted(cnt.items(), key=lambda x: lab[x[0]]) if n >= 10}
    R["f_descriptive"]["manufacturers_total_and_with_n_ge_10"] = {"defect_filers": len(cnt), "with_n_ge_10": sum(n >= 10 for n in cnt.values())}
    G = [f for f in F_all if f["guard_needed"]]
    R["amendment_TS_A1"] = {"filings_needing_guard": len(G), "by_split": dict(Counter(f["split"] for f in G)), "defect_filings": sum(f["type"] == "DEFECT" for f in G),
                            "anchors_using_year_from_context": sum(1 for f in G for side in ("silver", "agent")
                                                                   if (iv := anchor(f[side], f["sub"], f["campaign"], f["years"])[0]) is not None and iv.year_from_context),
                            "context_years_sizes": [len(f["years"]) for f in G]}
    Path("reports/ts").mkdir(parents=True, exist_ok=True)
    json.dump(R, open("reports/ts/phase_7_timeliness.json", "w"), indent=1, default=str)
    print("written reports/ts/phase_7_timeliness.json")


if __name__ == "__main__":
    main()
