"""Render reports/ts/phase_7_timeliness.json -> reports/phase_7_timeliness.md. Formatting only (shares and sums of stored counts)."""
import json

R = json.load(open("reports/ts/phase_7_timeliness.json"))
G = ["testA", "testB", "unseen", "pooled"]
NAME = {"testA": "Test-A", "testB": "Test-B", "unseen": "unseen-filer", "pooled": "pooled"}
ST = ["FLAGGED", "NOT_FLAGGED", "INDETERMINATE", "NO_DECISION_DATE"]
L = []
w = L.append


def p(x, d=3):
    return "n/a" if x is None or x != x else f"{x:.{d}f}"


def ci(v):
    return f"[{p(v[0])}, {p(v[1])}]"


def sh(v):
    return f"{v['k']}/{v['n']} = {p(v['share'])} W{ci(v['wilson95'])} B{ci(v['cluster_boot95'])}"


def num(x):
    return "n/a" if x is None or x != x else (f"{x:.0f}" if float(x).is_integer() else f"{x:.1f}")


pooled = R["a_reference"]["pooled"]
sens = R["d_sensitivity"]["pooled"]
rc = R["f_descriptive"]["pooled"]["rcdate_minus_submission_calendar_days"]
w("# Phase 7 (TS-1): 5-working-day timeliness screen of Part 573 filings")
w("")
w("**Silver reference (AI-generated, not human-verified).** This is a **descriptive screening signal, not a legal finding** about any filing or filer. It was "
  "computed under the protocol fixed before any gap was computed (`reports/TS_PROTOCOL.md`, tag `ts-protocol-1`), with one implementation amendment (TS-A1, "
  "below), which affects no anchor. No model was run and nothing under `freeze-v1` or `amendment-1` changed. Aggregates only; manufacturers are anonymised. "
  f"Tests: `{R['tests']}` (`tests/test_ts_screen.py`, run by the script before anything is written). Raw aggregates: `reports/ts/phase_7_timeliness.json`.")
w("")
w("## Summary")
amb = sens["amended_version_only"]; org = sens["original_version_only"]
w("**1. Population and primary result.**")
w(f"- **Population:** {R['population']['defect']} defect filings (out of 397; {R['population']['noncompliance']} noncompliance filings are reported separately).")
w(f"- **Primary screen:** the silver reference gives a decision date for {pooled['n_with_decision_date']} of {pooled['N']}. "
  f"FLAGGED {sh(pooled['status']['FLAGGED'])}, NOT_FLAGGED {pooled['status']['NOT_FLAGGED']['k']}, INDETERMINATE {pooled['status']['INDETERMINATE']['k']}, "
  f"NO_DECISION_DATE {pooled['status']['NO_DECISION_DATE']['k']}. W = Wilson 95%, B = filer-cluster bootstrap 95%.")
w("")
w("**2. The primary FLAGGED share is mostly a filing-date artefact. Read it with the pre-declared version and RCDATE results.**")
w(f"- **Most processed PDFs are amended versions.** For {amb['N']} of {pooled['N']} defect filings the processed PDF is a later, amended version.")
w(f"- **Their Submission Date is not the initial filing date.** It equals RCDATE (NHTSA's received date for the Part 573 report) in only {rc['amended']['equal_0']} of "
  f"{rc['amended']['n']}. RCDATE is earlier by a median of {num(-rc['amended']['median'])} calendar days, so that Submission Date is most likely the amendment's "
  "date.")
w("- **FLAGGED by version:**")
w(f"  - amended versions: {amb['ref_status_counts'].get('FLAGGED', 0)} of {amb['N']};")
w(f"  - original (only-version) filings, where Submission Date and RCDATE agree in {rc['original']['equal_0']} of {rc['original']['n']}: "
  f"{org['ref_status_counts'].get('FLAGGED', 0)} of {org['N']} ({sh(org['ref_flagged_share'])}).")
w(f"- **With RCDATE as the filing date** (a pre-declared sensitivity), the pooled reference has {sens['rcdate_as_filing_date']['ref']['status_counts'].get('FLAGGED', 0)} "
  f"FLAGGED of {pooled['N']}.")
w("- **Not promoted.** Neither variant is promoted to the primary result (that would be post hoc). They are pre-declared and shown so the primary share is not "
  "misread.")
w("")
w("**3. Coverage and agreement.**")
w(f"- **Decision dates:** {pooled['status']['NO_DECISION_DATE']['k']} of {pooled['N']} defect filings ({p(pooled['status']['NO_DECISION_DATE']['share'])}) have "
  "no usable DECISION date in the silver reference.")
w(f"- **Agent coverage:** the agent has an accepted, dated DECISION claim for {R['b_agent']['pooled']['coverage']['k']} of {pooled['N']}.")
w(f"- **Agreement where both have a date:** the agent and the reference agree closely (Cohen's κ {p(R['c_agreement']['pooled']['kappa']['value'])}). Both mostly "
  "read the same sentence.")
w("")
# ---------------------------------------------------------------- (a)
w("## (a) Reference (silver), defect filings")
w("Gaps are counted in working days (Mon–Fri, excluding observed federal holidays), from strictly after the decision date up to and including the filing date "
  "(the Submission Date). gap_min uses the latest possible decision day, gap_max the earliest, and gap_mid is their mean. Quantiles use linear interpolation "
  "and cover filings with a decision date only.")
w("")
w("| split | N | with decision date | gap_mid median [IQR] p90 | gap_min median [IQR] p90 | gap_max median [IQR] p90 | AMBIGUOUS anchors | anchor precision |")
w("|---|---|---|---|---|---|---|---|")
for g in G:
    a = R["a_reference"][g]
    q = lambda d: f"{num(d['median'])} [{num(d['p25'])}–{num(d['p75'])}] {num(d['p90'])}"
    w(f"| {NAME[g]} | {a['N']} | {a['n_with_decision_date']} | {q(a['gap_mid'])} | {q(a['gap_min'])} | {q(a['gap_max'])} | {a['anchor_ambiguous']} | "
      + ", ".join(f"{k} {v}" for k, v in sorted(a['anchor_precision'].items())) + " |")
w("")
w("| split | FLAGGED | NOT_FLAGGED | INDETERMINATE | NO_DECISION_DATE |")
w("|---|---|---|---|---|")
for g in G:
    a = R["a_reference"][g]["status"]
    w(f"| {NAME[g]} | " + " | ".join(sh(a[s]) for s in ST) + " |")
w("")
w("Share = k/N. W = Wilson 95%; B = filer-cluster bootstrap 95% (2,000 resamples, seed 0).")
w("")
w("**Noncompliance filings (descriptive only; § 573.6(c)(6) asks for a chronology for defects only):**")
w("")
w("| split | N | with decision date | FLAGGED | NOT_FLAGGED | INDETERMINATE | NO_DECISION_DATE |")
w("|---|---|---|---|---|---|---|")
for g in G:
    a = R["a_noncompliance_reference"][g]
    if a:
        w(f"| {NAME[g]} | {a['N']} | {a['n_with_decision_date']} | " + " | ".join(f"{a['status'][s]['k']} ({p(a['status'][s]['share'])})" for s in ST) + " |")
w("")
# ---------------------------------------------------------------- (b)
w("## (b) Agent (run-1 claims accepted by the frozen gate), defect filings")
w("**Unknown** = no accepted DECISION claim (abstention), no qualifying date, or INDETERMINATE.")
w("- **Manski lower bound:** every unknown counted as not flagged.")
w("- **Manski upper bound:** every unknown counted as flagged.")
w("")
w("| split | N | coverage (agent decision date) | abstained (no accepted DECISION claim) | NO_DECISION_DATE total | FLAGGED / NOT / INDET | complete-case FLAGGED share | Manski lower [B] | Manski upper [B] | reference FLAGGED share |")
w("|---|---|---|---|---|---|---|---|---|---|")
for g in G:
    b = R["b_agent"][g]; sc = b["status_counts"]
    cc = b["complete_case_flagged"]
    w(f"| {NAME[g]} | {b['N']} | {sh(b['coverage'])} | {b['abstained_no_accepted_decision_claim']} | {b['no_decision_date_total']} | "
      f"{sc.get('FLAGGED', 0)} / {sc.get('NOT_FLAGGED', 0)} / {sc.get('INDETERMINATE', 0)} | {sh(cc)} | {p(b['manski_lower']['value'])} {ci(b['manski_lower']['cluster_boot95'])} | "
      f"{p(b['manski_upper']['value'])} {ci(b['manski_upper']['cluster_boot95'])} | {p(b['reference_flagged_share'])} |")
w("")
w("**Bounds without INDETERMINATE as unknown** (INDETERMINATE counted as not flagged; the lower bound is unchanged): upper bound "
  + "; ".join(f"{NAME[g]} {p(R['b_agent'][g]['manski_upper']['value'] - R['b_agent'][g]['status_counts'].get('INDETERMINATE', 0) / R['b_agent'][g]['N'])}" for g in G) + ".")
w("")
# ---------------------------------------------------------------- (c)
w("## (c) Agreement where both the reference and the agent have a decision date")
w("| split | n both | identical interval [B] | same day, both day precision [B] | abs. diff of gap_mid (working days): median / p90 / max; share 0; share ≤ 5 | precision of agent FLAGGED [B] | recall [B] | Cohen's κ [B] | PABAK [B] | reference FLAGGED among n |")
w("|---|---|---|---|---|---|---|---|---|---|")
for g in G:
    c = R["c_agreement"][g]; d = c["abs_diff_gap_mid_wd"]
    b2 = lambda v: f"{p(v['value'])} {ci(v['cluster_boot95'])}"
    w(f"| {NAME[g]} | {c['n_both']} | {b2(c['identical_interval'])} | {b2(c['same_day_both_day_precision'])} | {num(d['median'])} / {num(d['p90'])} / {num(d['max'])}; "
      f"{p(d['share_0'])}; {p(d['share_le_5'])} | {b2(c['precision_agent_flagged'])} | {b2(c['recall_agent_flagged'])} | {b2(c['kappa'])} | {b2(c['pabak'])} | "
      f"{c['n_reference_flagged']}{' (fewer than 10: unstable)' if c['unstable'] else ''} |")
w("")
w("3×3 flag tables (rows = reference, columns = agent; raw counts):")
w("")
for g in G:
    t = R["c_agreement"][g]["flag_table_rows_reference_cols_agent"]
    w(f"**{NAME[g]}**")
    w("")
    w("| reference \\ agent | FLAGGED | NOT_FLAGGED | INDETERMINATE |")
    w("|---|---|---|---|")
    for r in ["FLAGGED", "NOT_FLAGGED", "INDETERMINATE"]:
        w(f"| {r} | {t[r]['FLAGGED']} | {t[r]['NOT_FLAGGED']} | {t[r]['INDETERMINATE']} |")
    w("")
w("High agreement here mostly means that the agent's accepted DECISION claim and the silver DECISION event quote the same chronology sentence. It says nothing "
  "about whether either date is the legally relevant one.")
w("")
# ---------------------------------------------------------------- (d)
w("## (d) Pre-declared sensitivity runs (defect filings)")
w("Status changes are measured against the primary over all N, in four categories (NO_DECISION_DATE included).")
w("")
w("| variant | split | reference: changed / N (share) | reference FLAGGED / NOT / INDET / NO_DATE | agent: changed / N (share) | agent FLAGGED / NOT / INDET / NO_DATE |")
w("|---|---|---|---|---|---|")
VN = {"calendar_days": "1 calendar days", "holidays_not_excluded": "2 holidays not excluded", "earliest_decision": "3 earliest DECISION",
      "latest_any_event": "4 latest event of any type", "lexicon_event": "5 lexicon event", "rcdate_as_filing_date": "6 RCDATE as filing date"}
cnt = lambda d: " / ".join(str(d.get(s, 0)) for s in ST)
for v, lab in VN.items():
    for g in G:
        x = R["d_sensitivity"][g][v]
        w(f"| {lab} | {NAME[g]} | {x['ref']['changed_vs_primary']}/{x['ref']['N']} ({p(x['ref']['changed_share'])}) | {cnt(x['ref']['status_counts'])} | "
          f"{x['agt']['changed_vs_primary']}/{x['agt']['N']} ({p(x['agt']['changed_share'])}) | {cnt(x['agt']['status_counts'])} |")
w("")
w("Subsets (status changes do not apply; primary rule within the subset):")
w("")
w("| subset | split | N | reference FLAGGED / NOT / INDET / NO_DATE | reference FLAGGED share | agent FLAGGED / NOT / INDET / NO_DATE |")
w("|---|---|---|---|---|---|")
SN = {"original_version_only": "7a original (only-version) filings", "amended_version_only": "7b amended-version filings",
      "type_from_document_only (proxy-typed dropped)": "8 type from document text only (FMVSS-proxy-typed dropped)"}
for v, lab in SN.items():
    for g in G:
        x = R["d_sensitivity"][g][v]
        w(f"| {lab} | {NAME[g]} | {x['N']} | {cnt(x['ref_status_counts'])} | {sh(x['ref_flagged_share']) if x['ref_flagged_share'] else 'n/a (N = 0)'} | {cnt(x['agt_status_counts'])} |")
w("")
w("Every pre-declared variant ran. Variant 7 cannot use the original version's own Submission Date, because those PDFs were not downloaded; it reports the two "
  "strata instead, as the protocol fixed. Variant 8 is empty for Test-B, where every filing is typed by the FMVSS proxy.")
w("")
# ---------------------------------------------------------------- (e)
w("## (e) Consistency audit (no ground truth), defect filings")
w("| split | set | order inconsistency (FILER_AWARENESS ≤ INVESTIGATION_START ≤ DECISION ≤ filing) | any dated event after the filing date | DECISION more than 10 years before filing |")
w("|---|---|---|---|---|")
for g in G:
    for side in ("silver", "agent"):
        e = R["e_audit"][g][side]
        w(f"| {NAME[g]} | {'silver' if side == 'silver' else 'agent accepted'} | " + " | ".join(f"{e[k]['k']}/{e[k]['n']} ({p(e[k]['share'])}) W{ci(e[k]['wilson95'])}"
                                                                                    for k in ("order_inconsistency", "event_after_filing", "decision_over_10y_before")) + " |")
w("")
w("An order inconsistency means an event of an earlier type in the chain lies entirely after an event of a later type, or a DECISION lies after the filing "
  "date. Investigations can legitimately continue after awareness or decision entries, so this is a consistency flag, not an error count.")
w("")
# ---------------------------------------------------------------- (f)
w("## (f) Descriptive")
w("**How informative the screen is:** the share of defect filings whose latest dated event (on or before the filing date) is DECISION-typed.")
w("")
w("| split | silver: k / filings with a dated event (N) | agent accepted: k / filings with a dated event (N) |")
w("|---|---|---|")
for g in G:
    x = R["f_descriptive"][g]["last_dated_event_is_decision"]
    w(f"| {NAME[g]} | {x['silver']['k']}/{x['silver']['n_with_dated_event']} ({x['silver']['N']}) | {x['agent']['k']}/{x['agent']['n_with_dated_event']} ({x['agent']['N']}) |")
w("")
w("**Submission Date vs RCDATE** (RCDATE − Submission Date, calendar days; defect filings):")
w("")
w("| split | stratum | n | equal | RCDATE earlier | RCDATE later | min | p10 | median | p90 | max |")
w("|---|---|---|---|---|---|---|---|---|---|---|")
for g in G:
    for k in ("all", "original", "amended"):
        x = R["f_descriptive"][g]["rcdate_minus_submission_calendar_days"][k]
        w(f"| {NAME[g]} | {k} | {x['n']} | {x['equal_0']} ({p(x['equal_share'])}) | {x['below_0']} | {x['above_0']} | {num(x['min'])} | {num(x['p10'])} | {num(x['median'])} | {num(x['p90'])} | {num(x['max'])} |")
w("")
w("**Strata (reference, primary rule, pooled defect filings):**")
w("")
w("| field | value | N | FLAGGED | NOT_FLAGGED | INDETERMINATE | NO_DECISION_DATE |")
w("|---|---|---|---|---|---|---|")
for k in ("influenced_by", "rcltypecd"):
    for val, x in R["f_descriptive"]["strata_pooled"][k].items():
        w(f"| {k.upper()} | {val} | {x['N']} | " + " | ".join(f"{x[s]['k']} ({p(x[s]['share'])}) W{ci(x[s]['wilson95'])}" for s in ST) + " |")
w("")
m = R["f_descriptive"]["manufacturers_total_and_with_n_ge_10"]
w(f"**Manufacturers with at least 10 pooled defect filings** ({m['with_n_ge_10']} of {m['defect_filers']} filers; anonymised; reference, primary rule):")
w("")
w("| manufacturer | N | FLAGGED | NOT_FLAGGED | INDETERMINATE | NO_DECISION_DATE |")
w("|---|---|---|---|---|---|")
for lab, x in R["f_descriptive"]["manufacturers_n_ge_10_pooled"].items():
    w(f"| {lab} | {x['N']} | " + " | ".join(str(x[s]) for s in ST) + " |")
w("")
# ---------------------------------------------------------------- amendments, limitations, prior art
a1 = R["amendment_TS_A1"]
w("## Amendments")
w(f"**TS-A1 (2026-10-28)** (`reports/TS_AMENDMENTS.md`):")
w("- **What it is:** the amendment-1 crash-only guard on the frozen date parser inside `chronology_years`, which crashed on an invalid calendar date.")
w(f"- **Scope:** {a1['filings_needing_guard']} filings ({', '.join(f'{k} {v}' for k, v in a1['by_split'].items())}).")
w(f"- **Effect:** it changes only the year context of those filings. **Anchors using a year from context in them: {a1['anchors_using_year_from_context']}**, so "
  "no anchor, gap or flag depends on the amendment. The POST HOC label therefore covers nothing in the tables above.")
w("")
w("## Limitations")
w("- **Silver labels.** Every decision date is an AI-made silver label or an AI agent's claim; no human checked any of them. Pass C sided with Pass B in "
  "72–78% of items, and both are the same model family.")
w("- **Self-reported dates.** The screen measures the interval between the decision date the filer wrote in its chronology and the filing date. The legally "
  "relevant trigger can be when a defect *should have* been determined, which may be earlier than any chronology date. So the gap is at best a lower bound on "
  "the legally relevant interval, and it depends on how each filer words its chronology.")
w("- **Filing-date artefact.** The processed PDF is the latest version. For amended versions, the Submission Date is generally later than RCDATE (section f), "
  "so the primary gap is longer than the initial-report gap for most of those filings. The original version's own date was not available (not downloaded).")
w("- **Working-days assumption.** Part 573 does not define \"working days\". We assume Mon–Fri excluding observed federal holidays. The holiday table "
  "follows 5 U.S.C. 6103 and **omits one-off executive-order closures** and Inauguration Day. The holidays-not-excluded variant changes few statuses; the "
  "calendar-days variant changes many.")
w("- **DECISION vs OTHER typing.** The DECISION/OTHER boundary is one of the most frequent type confusions, both between the labellers and between the agent "
  "and the labels (`reports/phase_6_failure_analysis.md` section e).")
w("  - Some DECISION-typed events are a supplier's own decision, or a sentence that only inherits an entry-header date.")
w("  - The lexicon and any-event variants show how much the anchor choice matters.")
w("- **Defect vs noncompliance typing.** The 2025+ form has no type field, so 186 of 397 filings are typed by a flat-file FMVSS proxy. On the pre-2025 form, the "
  "proxy's DEFECT calls are 153/154 correct, but it misses 13 of 166 defects.")
w("- **Small n.** Per-split counts are small, the cluster bootstrap intervals are wide, and only 3 manufacturers reach 10 defect filings.")
w("- **Scope.** These are three samples drawn for the extraction study (2023 to mid-2026), not a census.")
w("")
w("## Prior art")
w("- **Closest regulatory analogue:** NHTSA's case-by-case timeliness and audit queries. One example is TQ14-001, whose consent order (May 2014) is on nhtsa.gov; "
  "another is AQ23-002, whose information requests are on static.nhtsa.gov. We found no aggregate across manufacturers published by NHTSA.")
w("- **Closest method analogue:** Zhyrko, Han & Verberne (2026), \"Time as Structure: Temporal Dependency Graphs for Verifiable Deadline Computation over "
  "Legal Documents\", arXiv 2608.15270 (a preprint). Its design extracts dated facts with a model, then computes with a calendar engine.")
w("- **Closest data analogue:** Astvansh, Ball & Josefy (2022), *MSOM* 24(3):1457–1473. It hand-codes recall timing (awareness to recall) for 2,120 recalls by "
  "27 automakers, 2009–2018.")
w("- **Search scope:** four general web searches on 2026-10-28, read at snippet or summary level only. No bibliographic database was searched systematically, "
  "and no paper was read in full.")
w("- **The only claim made:** within this scope, we found no prior work that computes this gap across multi-manufacturer Part 573 filings. The method is not "
  "claimed to be new.")
open("reports/phase_7_timeliness.md", "w").write("\n".join(L) + "\n")
print("written", len(L), "lines")
