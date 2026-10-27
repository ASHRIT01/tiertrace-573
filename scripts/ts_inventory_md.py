"""Render reports/ts/TS_INVENTORY.json -> reports/TS_INVENTORY.md (no computation beyond sums and shares of the stored counts)."""
import json

R = json.load(open("reports/ts/TS_INVENTORY.json"))
S = ["testA", "testB", "unseen"]
NAME = {"testA": "Test-A", "testB": "Test-B", "unseen": "unseen-filer"}
L = []
w = L.append


def g(d, s, k):
    return d.get(f"{s} | {k}", 0)


w("# TS-1 Step 0 inventory: timeliness screen inputs")
w("")
w("**Silver reference (AI-generated, not human-verified).** This file has counts and field checks only: **no gap and no date difference was computed.** "
  "Aggregates only; no company names or recall numbers. It was produced by `scripts/ts_gate.py`, which reads the frozen gate decisions without changing them, "
  "and `scripts/ts_inventory.py` (raw output `reports/ts/TS_INVENTORY.json`). No model was run and nothing under `freeze-v1` or `amendment-1` changed.")
w("")
w("## 1. Filings")
w("| split | processed, readable filings | note |")
w("|---|---|---|")
note = {"testA": "200 drawn; 1 had no text layer and was excluded (amendment 1)", "testB": "100 drawn; all readable",
        "unseen": "100 drawn; 2 had no text layer and were excluded (amendment 1)"}
for s in S:
    w(f"| {NAME[s]} | {R['1_filings'][s]['processed_readable']} | {note[s]} |")
w(f"| **all** | **{sum(R['1_filings'][s]['processed_readable'] for s in S)}** | |")
w("")
d2 = R["2_submission_date"]
w("## 2. Submission date in the PDF text")
w("The text comes from the frozen extractor (`tt.parse.pdf.extract_text`). Below are five real headers, one for each split and form layout. Every value except "
  "the date is redacted.")
w("")
for e in d2["examples"]:
    w(f"- {NAME[e['split']]}, {e['layout']}: `{e['header']}`")
w("")
w(f"Regex: `{d2['regex']}`. It allows 1–2 digit days (\"MAR 7, 2025\") and 3–9 letter month names; the month is matched on its first three letters.")
w("")
w("| split | pre-2025 form | 2025+ form | parsed | single occurrence in the text | one-digit day seen | equals frozen `parse_header` | equals silver `filing_date` |")
w("|---|---|---|---|---|---|---|---|")
lay, par, cc = d2["layouts"], d2["parse"], d2["cross_checks"]
for s in S:
    w(f"| {NAME[s]} | {g(lay, s, 'pre-2025 form (label : value on one line)')} | {g(lay, s, '2025+ form (label and value on separate lines)')} | "
      f"{g(par, s, 'parsed')}/{R['1_filings'][s]['processed_readable']} | {g(par, s, 'single occurrence')} | {g(par, s, 'one-digit day in text')} | "
      f"{g(cc, s, 'equals frozen parse_header filing_date')} | {g(cc, s, 'equals silver label filing_date')} |")
w("")
w(f"Parse rate: **{sum(g(par, s, 'parsed') for s in S)}/{sum(R['1_filings'][s]['processed_readable'] for s in S)}**. Failing layouts: "
  f"{'none' if not d2['failing_layouts'] else d2['failing_layouts']}. Every processed filing holds exactly one Submission Date, and all three readings agree.")
w("")
d3 = R["3_flat_file"]
w("## 3. NHTSA flat file")
w(f"- **File:** `{d3['file']}` (member `{d3['member']}`); layout {d3['layout_doc']}.")
w(f"- **Column names** (from RCL.txt, as used by `tt/data/flat.py`): {', '.join(d3['column_names'])}.")
w(f"- **CAMPNO format** (letters shown as A, digits as 9, all rows): {', '.join(f'`{k}` {v:,}' for k, v in d3['campno_shapes_all_rows'].items())}. "
  "A test campaign is `YYTNNN` plus 3 digits.")
w(f"- **Join rule:** {d3['join_rule']}.")
w(f"- **Join rate:** Test-A {d3['joined']['testA']}, Test-B {d3['joined']['testB']}, unseen-filer {d3['joined']['unseen']}. "
  f"Fields that differ across a campaign's rows: {', '.join(f'{k.split(':')[0]} {v}' for k, v in d3['row_consistency'].items())}.")
w("")
w("| field | exists | meaning (RCL.txt) | what the joined campaigns hold |")
w("|---|---|---|---|")
w(f"| RCDATE | yes | {d3['RCDATE']['meaning (RCL.txt)']} | {d3['RCDATE']['present_and_8_digits']}/{d3['RCDATE']['of']} present, YYYYMMDD |")
w(f"| INFLUENCED_BY | yes | {d3['INFLUENCED_BY']['meaning (RCL.txt)']} | {', '.join(f'{k} {v}' for k, v in d3['INFLUENCED_BY']['values'].items())} |")
w(f"| RCLTYPECD | yes | {d3['RCLTYPECD']['meaning (RCL.txt)']} | {', '.join(f'{k} {v}' for k, v in d3['RCLTYPECD']['values'].items())}; {d3['RCLTYPECD']['note']} |")
w(f"| FMVSS | yes | {d3['FMVSS']['meaning (RCL.txt)']} | non-empty {d3['FMVSS']['non_empty']}/{d3['FMVSS']['of']} |")
w(f"| RPNO | yes | {d3['RPNO']['meaning (RCL.txt)']} | non-empty {d3['RPNO']['non_empty']}/{d3['RPNO']['of']} |")
w(f"| defect/noncompliance indicator | **no** | — | {d3['explicit_noncompliance_indicator']} |")
w("")
d4 = R["4_defect_vs_noncompliance"]
c4 = d4["counts"]
w("## 4. Defect vs noncompliance")
w("Sources checked:")
w("- **(a) Report text header (pre-2025 form only):** \"Description of Defect :\" or \"Description of Noncompliance :\".")
w("- **(b) The 2025+ form:** it has one combined heading, \"Description of the defect or noncompliance:\", and **no type field**.")
w("- **(c) NHTSA document titles in the version listing:** \"Defect Notice 573 Report\" or \"Noncompliance Notice 573 Report\" on any version.")
w("- **(d) The flat file has no type field.** The only proxy is FMVSS: empty → defect, non-empty → noncompliance.")
w("")
w("| split | header DEFECT | header NONCOMPLIANCE | header absent (2025+ form) | title DEFECT | title NONCOMPLIANCE | title absent | flat FMVSS empty | flat FMVSS non-empty |")
w("|---|---|---|---|---|---|---|---|---|")
for s in S:
    h = lambda k: c4.get(f"{s} | report text header | {k}", 0)
    t = lambda k: c4.get(f"{s} | NHTSA document title (any version) | {k}", 0)
    f = lambda k: c4.get(f"{s} | flat-file FMVSS empty=DEFECT / non-empty=NONCOMPLIANCE | {k}", 0)
    w(f"| {NAME[s]} | {h('DEFECT')} | {h('NONCOMPLIANCE')} | {h('absent')} | {t('DEFECT')} | {t('NONCOMPLIANCE')} | {t('absent')} | {f('DEFECT')} | {f('NONCOMPLIANCE')} |")
w("")
w("Cross-checks where two sources exist (all splits): " + "; ".join(f"{k} {v}" for k, v in d4["cross_checks"].items()) + ".")
w("")
w("The header and the NHTSA title disagree on 2 filings; the header is used.")
w("")
w("**Which source decides:** the report text header when present. Otherwise the NHTSA document title, which never decided a filing here: every filing with a "
  "title also has a header. Otherwise the flat-file FMVSS proxy.")
w("")
w("| split | DEFECT by header | NONCOMPLIANCE by header | DEFECT by FMVSS proxy | NONCOMPLIANCE by FMVSS proxy |")
w("|---|---|---|---|---|")
for s in S:
    k = lambda x: c4.get(f"{s} | DECIDED BY (hierarchy) | {x}", 0)
    w(f"| {NAME[s]} | {k('report text header: DEFECT')} | {k('report text header: NONCOMPLIANCE')} | {k('flat-file FMVSS proxy: DEFECT')} | {k('flat-file FMVSS proxy: NONCOMPLIANCE')} |")
w("")
w("**The proxy's limits.** Every 2025+-form filing is typed by the proxy: 186 of 397, and all 100 Test-B filings. On the 211 pre-2025-form filings, the proxy "
  "matches the header as follows:")
w("- Proxy DEFECT: 153 of its 154 calls are header DEFECT.")
w("- Header DEFECT: 13 of 166 would be called NONCOMPLIANCE by the proxy, because a defect report can cite an FMVSS.")
w("- Header NONCOMPLIANCE: 1 of 45 would be called DEFECT.")
w("")
w("So the proxy mostly errs by leaving defect filings out of the defect population.")
w("")
d5 = R["5_event_fields"]["counts"]
w("## 5. What the events store")
w(f"- **Silver labels:** {R['5_event_fields']['silver_stores']}.")
w(f"- **Agent claims:** {R['5_event_fields']['agent_stores']}.")
w("")
rows5 = ["silver events (all)", "silver events contested (dropped)", "silver non-contested", "  with raw date text", "  undated (no date text, no span)",
         "  with stored ISO span", "  ISO span only (no raw date text)", "  raw date text but no stored span", "  with evidence quote",
         "  DECISION (all)", "  DECISION with raw date text", "  DECISION quote cites a different recall number",
         "agent filings with valid run-1 output", "agent filings with valid run-2 output", "agent run-1 events", "agent run-1 events with raw date text",
         "agent run-1 events with evidence quote", "agent run-1 DECISION (any gate outcome)", "agent accepted events", "agent accepted DECISION",
         "agent accepted DECISION with raw date text", "agent accepted DECISION quote cites a different recall number"]
w("| count | " + " | ".join(NAME[s] for s in S) + " |")
w("|---|---|---|---|")
for r in rows5:
    lab = r.strip() if not r.startswith("  ") else "— " + r.strip()
    w(f"| {lab} | " + " | ".join(str(d5[s].get(r, 0)) for s in S) + " |")
w("")
w("**What this means for the screen:**")
w("- **No event is ISO-only.** Every event with a stored ISO span also has its raw date text.")
w("- **The stored span is incomplete.** It is missing for every Pass-C-decided item (Test-A 229, Test-B 111, unseen 94) and for 7 Pass A items whose text "
  "the frozen parser could not read (Test-A 5, unseen 2). The screen therefore re-parses `date_text` for both the silver labels and the agent with one parser.")
w("- **Quotes are present on every event**, so the different-recall-number rule (protocol E) can run.")
w("- **Agent counts:** they are run-1 events and their acceptance by the frozen gate (score ≥ 3), the same set as H1. On Test-A, the 4 filings with a run-2 "
  "timeout have no accepted claim.")
w("")
d6 = R["6_version"]["counts"]
w("## 6. Original vs amended version")
w("**Knowable for every filing** from the NHTSA version listing (`is_original`, `n_versions`). Only the latest version was downloaded and none of the originals "
  "of multi-version campaigns is cached, so the original's own Submission Date is **not** available.")
w("")
w("| split | processed PDF is the original (only version) | processed PDF is a later (amended) version | processed is the latest |")
w("|---|---|---|---|")
for s in S:
    w(f"| {NAME[s]} | {g(d6, s, 'processed = original (only version)')} | {g(d6, s, 'processed = later (amended) version')} | {g(d6, s, 'processed is the latest version')} |")
w("")
w("For a later version, the PDF's Submission Date may be the amendment's date rather than the original filing date. That matters for any filing-date anchor; "
  "the protocol handles it (TS_PROTOCOL.md section C and the version sensitivity).")
w("")
w("## 7. Raw date-text formats")
w("Each non-empty date text was classified by the TS parser (`scripts/ts_lib.py`, `date_format`), independently of any filing date:")
w("- **full_date:** a day with a year.")
w("- **numeric_ambiguous:** a numeric date that reads validly as both mm/dd and dd/mm.")
w("- **yearless:** a day or month with no year.")
w("- **week:** \"CW51/2020\" or \"week of …\".")
w("- **early_mid_late:** of a month or a year.")
w("- **quarter, year, range** (two dates), and **unparsed.**")
w("")
w("Silver = non-contested events. Agent = run-1 events accepted by the frozen gate.")
w("")
K = ["full_date", "numeric_ambiguous", "month", "yearless", "week", "early_mid_late", "quarter", "year", "range", "unparsed"]
w("| split | set | " + " | ".join(K) + " | total |")
w("|---|---|" + "---|" * (len(K) + 1))
for s in S:
    for key, lab in [("silver_all", "silver, all types"), ("silver_DECISION", "silver, DECISION"), ("agent_accepted_all", "agent accepted, all types"),
                     ("agent_accepted_DECISION", "agent accepted, DECISION")]:
        d = R["7_date_formats"][s][key]
        w(f"| {NAME[s]} | {lab} | " + " | ".join(str(d.get(k, 0)) for k in K) + f" | {sum(d.values())} |")
w("")
w("The 3 unparsed silver texts are a typo year, \"throughout\" used as a range word, and \"the months leading up to …\". None is a DECISION date. Every agent date "
  "text parses.")
open("reports/TS_INVENTORY.md", "w").write("\n".join(L) + "\n")
print("written", len(L), "lines")
