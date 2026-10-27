"""Renders reports/phase_6_failure_analysis.md from reports/phase_6_failure_analysis_<split>.json (no new scoring)."""
import json
from collections import defaultdict

S = [("testA", "Test-A (primary)"), ("testB", "Test-B"), ("unseen", "unseen-filer")]
R = {k: json.load(open(f"reports/phase_6_failure_analysis_{k}.json")) for k, _ in S}
ci = lambda c: f"{c[0]:.3f} [{c[1]:.3f}, {c[2]:.3f}]"
CL = [("i", "(i) date matches a gold event, type differs"), ("ii", "(ii) type matches a gold event, date differs"), ("iii", "(iii) neither matches"),
      ("iii_undated_same_type", "(iii-u) neither matches, but an undated gold event of that type exists"), ("v", "(v) own date unparseable"), ("iv", "(iv) duplicate of an earlier accepted claim")]
L = ["# Phase 6 failure analysis: **POST HOC, EXPLORATORY, silver labels, not human-verified, not a result**", "",
     "Nothing here was preregistered. It uses the existing run outputs and the frozen scorer machinery (amendment-1 wrapper, primary settings) only; no model run, no rerun, no change to prompt, verifiers, thresholds, scorer or labels. Events only. 'Accepted' = no verifier fired and run 2 agrees (the H1 accepted set); 'wrong' = the frozen scorer's `event_class` is not `right` (so the same claims as H1/H5; the strict view below reproduces the committed H1 delta, CI and counts exactly on all three splits). Silver labels are AI-made and not independent of the pipeline; no label-error figure is claimed. Scripts: `scripts/phase6_failure_analysis.py`, `scripts/phase6_failure_analysis_md.py`.", "",
     "## (a) Accepted event claims scored wrong, classified by code",
     "Classes are assigned in this order: (iv) an earlier accepted claim in the same filing has the same type and the same normalised quote (dates and digits removed); otherwise (i) the claim's date overlaps a scored gold event of that filing but the type differs; (ii) a scored gold event of that type exists but none has a matching date; (iii) neither; (v) the claim's own date text cannot be parsed (frozen class `wrong:date_unparsed`, not in the requested list but needed so the classes add up). Class (iii-u) is the part of (iii) where the filing has an unscored (undated) gold event of the same type. Mutually exclusive.", "",
     "| class | " + " | ".join(n for _, n in S) + " |", "|---|" + "---|" * len(S)]
L.append("| accepted event claims / of which scored wrong | " + " | ".join(f"{R[k]['accepted']} / {R[k]['accepted_wrong']} ({R[k]['accepted_wrong'] / R[k]['accepted']:.1%})" for k, _ in S) + " |")
for c, name in CL:
    L.append(f"| {name} | " + " | ".join(f"{R[k]['classes'].get(c, 0)} ({R[k]['classes'].get(c, 0) / R[k]['accepted_wrong']:.1%})" for k, _ in S) + " |")
L.append("| date matches a gold event (i) vs date does not match (ii + iii + iii-u + v) | " + " | ".join(
    f"{R[k]['classes'].get('i', 0)} vs {sum(R[k]['classes'].get(c, 0) for c in ('ii', 'iii', 'iii_undated_same_type', 'v'))}" for k, _ in S) + " |")
L += ["", "Duplicates (iv): underlying class of the repeated claims: " + "; ".join(f"{n}: {R[k]['duplicate_underlying'] or 'none'}" for k, n in S) + ".", "",
      "### By manufacturer (filer): the 5 filers with the most accepted-wrong claims in each split, plus other"]
for k, n in S:
    r = R[k]; rows = r["top5_filers_by_accepted_wrong"] + ["other"]
    L += ["", f"**{n}**", "", "| filer | accepted wrong | (i) | (ii) | (iii) | (iii-u) | (v) | (iv) |", "|---|---|---|---|---|---|---|---|"]
    for f in rows:
        d = r["classes_by_filer"].get(f, {})
        L.append(f"| {f} | {sum(d.values())} | " + " | ".join(str(d.get(c, 0)) for c, _ in CL[:3] + CL[3:5] + CL[5:]) + " |")
L += ["", "## (b) Date-only view (event type ignored): NOT PREREGISTERED",
      "A claim counts as right if its date overlaps ANY scored gold event of the filing, whatever the type. Same claims, same accepted set, same filer-cluster bootstrap (2000 resamples, seed 0). Strict = the committed definition (date and type).", "",
      "| split | view | B2 error (all claims) | agent accepted error | delta = B2 - accepted | coverage |", "|---|---|---|---|---|---|"]
for k, n in S:
    for v, vn in (("strict_view", "strict (date + type)"), ("date_only_view", "date only")):
        x = R[k][v]
        L.append(f"| {n} | {vn} | {ci(x['error_all'])} | {ci(x['error_accepted'])} | {ci(x['delta_all_minus_accepted'])} | {x['coverage']:.3f} ({x['accepted']}/{x['claims']}) |")
# (c) repetition
L += ["", "## (c) Repetition: near-duplicate chronology entries vs agent accepted error",
      "Per filing, the chronology is split into sentences with the labelling sentence splitter; sentences of at least 4 words are normalised (dates, digits and punctuation removed, lower case); the repeat share = entries whose normalised text already occurred earlier in the same filing / all such entries. Pooled over the three splits (the split of each filing is not shown); manufacturers with at least 15 accepted event claims, sorted by accepted claims. Accepted error = accepted-wrong / accepted; B2 error = wrong / all event claims of that manufacturer's filings.", ""]
agg = defaultdict(lambda: defaultdict(int)); rows = []
seen_in = defaultdict(lambda: defaultdict(set))          # filer -> normalised sentence -> {(split, file)}
for k, _ in S:
    for r in R[k]["repetition_rows"]:
        for t in set(r["norm"]):
            seen_in[r["filer"]][t].add((k, r["file"]))
for k, _ in S:
    for r in R[k]["repetition_rows"]:
        agg[r["filer"]]["cross_entries"] += len(r["norm"])
        agg[r["filer"]]["cross_dup"] += sum(1 for t in r["norm"] if len(seen_in[r["filer"]][t] - {(k, r["file"])}) > 0)
for k, _ in S:
    for r in R[k]["repetition_rows"]:
        a = agg[r["filer"]]
        for key in ("entries", "dup_entries", "claims", "wrong", "accepted", "accepted_wrong"): a[key] += r[key]
        a["filings"] += 1
L += ["| manufacturer | filings | chronology entries | repeat share within a filing | repeat share across other filings of the same manufacturer (extra column) | accepted claims | accepted error | B2 error |", "|---|---|---|---|---|---|---|---|"]
for f, a in sorted(agg.items(), key=lambda kv: -kv[1]["accepted"]):
    if a["accepted"] >= 15:
        L.append(f"| {f} | {a['filings']} | {a['entries']} | {a['dup_entries'] / a['entries']:.3f} | {a['cross_dup'] / a['cross_entries']:.3f} | {a['accepted']} | {a['accepted_wrong'] / a['accepted']:.3f} | {a['wrong'] / a['claims']:.3f} |")


def ranks(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0] * len(xs); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and xs[o[j + 1]] == xs[o[i]]: j += 1
        for t in range(i, j + 1): r[o[t]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b); n = len(a); ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb)); den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5
    return num / den if den else float("nan")


L += ["", "Filing-level association (Spearman rank correlation between a filing's repeat share and its accepted error; filings with at least 3 accepted claims; descriptive, no p-value):", "",
      "| split | filings | filings with any repeated entry | Spearman rho | mean accepted error: repeat share > 0.2 / <= 0.2 |", "|---|---|---|---|---|"]
for k, n in S:
    rr = [r for r in R[k]["repetition_rows"] if r["accepted"] >= 3 and r["entries"] > 0]
    sh = [r["dup_entries"] / r["entries"] for r in rr]; ae = [r["accepted_wrong"] / r["accepted"] for r in rr]
    hi = [e for s, e in zip(sh, ae) if s > 0.2]; lo = [e for s, e in zip(sh, ae) if s <= 0.2]
    L.append(f"| {n} | {len(rr)} | {sum(1 for s in sh if s > 0)} | {spearman(sh, ae):.2f} | {(sum(hi) / len(hi)) if hi else float('nan'):.3f} (n={len(hi)}) / {(sum(lo) / len(lo)) if lo else float('nan'):.3f} (n={len(lo)}) |")
b = R["testB"]; nb = b["accepted_wrong"]; ib = b["classes"].get("i", 0); do = b["date_only_view"]
L += ["", "## (d) Conclusion (two sentences)", "",
      f"Mostly type disagreement: in Test-B {ib} of the {nb} accepted-wrong event claims ({ib / nb:.0%}) have a date that matches a gold event of the same filing but a different type, only {nb - ib} ({(nb - ib) / nb:.0%}) have a date that matches no gold event or cannot be parsed, and ignoring type the Test-B delta is {do['delta_all_minus_accepted'][0]:.3f} [{do['delta_all_minus_accepted'][1]:.3f}, {do['delta_all_minus_accepted'][2]:.3f}] with accepted error {do['error_accepted'][0]:.3f}, so wrong or invented dates do not drive the Test-B shortfall. The data cannot say whether those type disagreements are the agent mistyping events or silver labelling conventions (both are AI judgements, none human-verified), and the date-only view is lenient (a date can coincide with an unrelated gold event), so it understates date errors somewhat.", "",
      "Notes: (1) The pattern is the same on Test-A (85% type-only) and unseen-filer (75%); Test-B's smaller delta comes with a higher strict accepted error, not with more date errors. (2) Within a filing, near-duplicate entries are almost absent (repeat share about 0 for Ford, Jayco and most manufacturers; only 2 accepted-wrong claims are duplicates, both in unseen-filer), and the filing-level correlation between repeat share and accepted error is about 0. (3) **Correction to `reports/phase_6_secondary_splits.md` section 3**, which described Ford and Jayco as having 'repeated' chronologies: that is supported only across filings of the same manufacturer for Ford (about 33% of its entries recur in another Ford filing, e.g. the shared software-recall text of 26V369/370/374; FCA also shows about 26% with a low accepted error of 0.197, and Jayco about 11%), not within filings, and the data do not show that repetition causes the errors. (4) The class counts, date-only view and repetition shares are descriptive; nothing here was tuned, rerun or changed."]
# ---- (e) type-ambiguity ceiling (scripts/phase6_type_ceiling.py) --------------------------------------------------------------
from tt.labels.agree import wilson
T = {k: json.load(open(f"reports/phase_6_type_ceiling_{k}.json")) for k, _ in S}
GR = ["Ford", "Jayco", "PACCAR", "FCA", "other"]
def rate(k, n):
    if not n: return "n/a (0)"
    lo, hi = wilson(k, n); return f"{k / n:.3f} [{lo:.3f}, {hi:.3f}] ({k}/{n})"
def tot(k):
    t = defaultdict(int)
    for v in T[k]["groups"].values():
        for a, b in v.items(): t[a] += b
    return t
L += ["", "## (e) Type-ambiguity ceiling: labeller vs labeller, next to the agent (POST HOC, EXPLORATORY)",
      "Existing label files only (`data/labels/<split>_passA.json`, `_passB.json`, final silver); no model call. Same matching rule as the frozen scorer: an event is date-matched if its date span coarsely overlaps a non-fuzzy event of the other side in the same filing, and its type agrees if any overlapping event has the same type (lenient for both sides). Dates of both passes are parsed with the same guarded parser and the filing's chronology-year context; undated, inferred or unparseable events take no part. Labellers: every Pass A event that is date-matched to Pass B (A->B; B->A shown too). Agent: every accepted run-1 event claim (the H1 accepted set) that is date-matched to the final scoring labels, so agent agreement = 1 - share of class (i) among date-matched accepted claims (duplicates included). Wilson 95% intervals; manufacturers by the filer name in the header.", ""]
for k, n in S:
    L += [f"**{n}**", "", "| manufacturer | Pass A vs Pass B type agreement (A->B) | (B->A) | agent vs final label, date-matched accepted claims |", "|---|---|---|---|"]
    for g in GR + ["all"]:
        v = tot(k) if g == "all" else T[k]["groups"].get(g, {})
        L.append(f"| {'**all**' if g == 'all' else g} | {rate(v.get('AB_agree', 0), v.get('AB_n', 0))} | {rate(v.get('BA_agree', 0), v.get('BA_n', 0))} | {rate(v.get('agent_agree', 0), v.get('agent_n', 0))} |")
    L.append("")
# confusion pairs
from collections import Counter as _C
pab, pag = _C(), _C()
for k, _ in S: pab.update(T[k]["pairs_AB"]); pag.update(T[k]["pairs_agent"])
L += ["Most frequent type disagreements (unordered pairs; a disagreeing event is paired with the most frequent type among the events it overlaps), pooled over the three splits, with the per-split counts:", ""]
for title, P_, key in (("(a) Pass A vs Pass B", pab, "pairs_AB"), ("(b) agent (accepted claims) vs final label", pag, "pairs_agent")):
    totd = sum(P_.values())
    L += [f"{title}: {totd} disagreements", "", "| type pair | count | share of disagreements | Test-A | Test-B | unseen |", "|---|---|---|---|---|---|"]
    for pair, c in P_.most_common(6):
        L.append(f"| {pair} | {c} | {c / totd:.1%} | " + " | ".join(str(T[k][key].get(pair, 0)) for k, _ in S) + " |")
    L.append("")
top_ab = [p for p, _ in pab.most_common(6)]; top_ag = [p for p, _ in pag.most_common(6)]
shared = [p for p in top_ag if p in top_ab]
words = []
for k, n in S:
    t = tot(k); a_lo, a_hi = wilson(t["AB_agree"], t["AB_n"]); g_lo, g_hi = wilson(t["agent_agree"], t["agent_n"])
    rel = "below" if g_hi < a_lo else ("above" if g_lo > a_hi else "similar to (the intervals overlap)")
    words.append(f"{n}: agent {t['agent_agree'] / t['agent_n']:.1%} vs labellers {t['AB_agree'] / t['AB_n']:.1%}, i.e. {rel}")
L += ["**Plain reading.** The agent's type agreement with the final labels, on date-matched accepted claims, compared with Pass A's type agreement with Pass B on date-matched events: " + "; ".join(words) + ". "
      f"{len(shared)} of the agent's 6 most frequent confusions are also among the labellers' 6 most frequent ({', '.join(shared) if shared else 'none'}), so the two disagree over largely the same type boundaries. "
      "On Test-A the agent's type disagreement is at about the level two AI labellers already have with each other on the same dates; on Test-B and unseen-filer it is larger. The labeller rate indicates how ambiguous these type boundaries are, but it is not a hard ceiling (an extractor could agree with the adjudicated labels more often than two raw passes agree with each other). "
      f"Two differences stand out. FILER_AWARENESS / INVESTIGATION_START is a much larger share of the agent's confusions ({pag['FILER_AWARENESS / INVESTIGATION_START'] / sum(pag.values()):.0%}) than of the labellers' ({pab.get('FILER_AWARENESS / INVESTIGATION_START', 0) / sum(pab.values()):.0%}), which matches the logged rule gap for sentences that report both awareness and the start of an investigation. "
      f"And on Test-B the gap is concentrated where the labellers did not find the types ambiguous: for Jayco the two passes agree {T['testB']['groups']['Jayco']['AB_agree']}/{T['testB']['groups']['Jayco']['AB_n']} but the agent only {T['testB']['groups']['Jayco']['agent_agree']}/{T['testB']['groups']['Jayco']['agent_n']}; for Ford the passes agree {T['testB']['groups']['Ford']['AB_agree']}/{T['testB']['groups']['Ford']['AB_n']} and the agent {T['testB']['groups']['Ford']['agent_agree']}/{T['testB']['groups']['Ford']['agent_n']} (small numbers, wide intervals). That part of the Test-B shortfall is therefore not explained by label ambiguity as measured here; it points more to the agent's typing (or to how the adjudicated labels typed these filers), though the data cannot separate those two.", "",
      "**Caveats.** The labels are not independent: Pass C sided with Pass B in 72-78% of its items (Test-A 73.5%, Test-B 72.2%, unseen 77.6%), the final labels are Pass A plus Pass C's corrections, and Pass B and Pass C are both Opus; the agent's event-type definitions were copied from the labelling rules (a disclosed bias in the agent's favour). The labeller rate compares two raw passes before adjudication, the agent rate compares with the adjudicated labels, so the two are not measured against the same reference. Matching is lenient on both sides (any overlapping event of the same type counts). Nothing here is a label-error figure; none of it is human-verified."]
open("reports/phase_6_failure_analysis.md", "w").write("\n".join(L) + "\n")
