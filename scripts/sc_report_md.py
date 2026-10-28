"""Render reports/sc/phase_8_supplier_check.json (+ SC_INVENTORY.json, phase_8_posthoc.json) -> reports/phase_8_supplier_check.md. Formatting only."""
import json

R = json.load(open("reports/sc/phase_8_supplier_check.json"))
I = json.load(open("reports/sc/SC_INVENTORY.json"))
PH = json.load(open("reports/sc/phase_8_posthoc.json"))
S = ["testA", "testB", "unseen"]
G = ["testA", "testB", "unseen", "layout_portal", "layout_older", "rcltypecd_V", "rcltypecd_E", "pooled"]
NAME = {"testA": "Test-A", "testB": "Test-B", "unseen": "unseen-filer", "layout_portal": "portal layout", "layout_older": "older layout",
        "rcltypecd_V": "vehicle (V)", "rcltypecd_E": "equipment (E)", "pooled": "**pooled**"}
ST = ["NAMED_SUPPLIER", "OEM_SELF", "OBTAINED_FROM", "MULTIPLE", "BLANK", "PARSE_FAIL"]
L = []
w = L.append


def p(x):
    return "n/a" if x is None or x != x else f"{x:.3f}"


def sh(v, ci=True):
    if v["n"] == 0:
        return "0/0"
    s = f"{v['k']}/{v['n']} = {p(v['share'])}"
    if ci:
        s += f" W[{p(v['wilson95'][0])}, {p(v['wilson95'][1])}] B[{p(v['cluster_boot95'][0])}, {p(v['cluster_boot95'][1])}]"
    return s + (" *unstable*" if v["unstable"] else "")


E = R["levels"]["exact"]
w("# Phase 8 (SC-1): agent and silver supplier claims checked against the filer's own declaration")
w("")
w("**Reference = filer-declared supplier (non-AI, not ground truth).** The declared supplier is what the filer wrote under 49 CFR 573.6(c)(2)(iv). It may be "
  "a tier-1 assembler, the entity the part was obtained from, or the filer itself. **A match measures fidelity to the filer's declaration, not who really made "
  "the part, and a non-match is not an error by the filer.**")
w("")
w(f"The computation follows the protocol fixed before any comparison (`reports/SC_PROTOCOL.md`, tag `sc-protocol-1`), with one amendment (SC-A1). No model was "
  f"run, and nothing under `freeze-v1`, `amendment-1` or `ts-protocol-1` changed. Tests: `{R['tests']}` (`tests/test_sc_check.py`, run by the script before "
  "anything is written). Raw aggregates: `reports/sc/phase_8_supplier_check.json`. Aggregates only; no per-filer rows and no supplier names in any result table.")
w("")
w("W = Wilson 95% CI; B = filer-cluster bootstrap 95% CI (2,000 resamples, seed 0); *unstable* = n < 20.")
w("")
w("## Summary")
pa = E["pooled"]
w("**1. The reference and the population.**")
w("- **Parsing:** the supplier block parses in 397/397 filings, in both layouts.")
w(f"- **Population:** {pa['n_filings']} filings declare one or more external suppliers (NAMED_SUPPLIER or MULTIPLE).")
w("- **Other strata:** 47 OEM_SELF, 4 OBTAINED_FROM and 85 BLANK filings are reported as counts only.")
w("")
w("**2. The agent never saw the supplier block.** Its frozen input is the cause and chronology, with the block name masked (Step 0). So its matches are "
  "recoveries from the narrative, not copies of the block.")
w(f"- **All supplier claims:** exact match on {sh(pa['agent_all']['recall'], False)} filings (recall) and {sh(pa['agent_all']['precision'], False)} claims "
  "(precision).")
w(f"- **Gate-accepted claims:** recall {sh(pa['agent_accepted']['recall'], False)}, precision {sh(pa['agent_accepted']['precision'], False)}.")
w("- **Evidence location:** all agent evidence lies outside the block.")
w("- **Why precision understates:** a correct sub-supplier named only in the narrative, and not in the block, counts as a non-match. Which companies the "
  "non-matching claims name was not tabulated.")
w("")
w("**3. The silver labels against the declaration (the first non-AI check of the silver supplier labels).**")
w(f"- **S1 (read from the block):** matches in {sh(pa['silver_S1']['precision'], False)} claims. This is circular by construction.")
w(f"- **S2 (narrative claims):** match the declared supplier in {sh(pa['silver_S2']['precision'], False)} claims, and cover "
  f"{sh(pa['silver_S2']['recall'], False)} population filings.")
w("")
w("**4. Components: not run.** Neither the frozen agent schema nor the silver labels contain component claims. Only the reference's availability is reported.")
w("")
# ---- inventory summary + strata
w("## Inventory summary (`reports/SC_INVENTORY.md`, commit c27b962)")
w("- **Supplier block:** one per filing in all 397. Parse rate 397/397, with 0 failures, in both layouts: portal (186) and older (211).")
w("- **Agent input:** no block heading or field line appears in the agent's frozen input in any filing. The block name is masked wherever it appears.")
w("- **Involved Components:** a name or part number is present in 390 of 397 filings, and flat-file MFR_COMP_NAME in 392 of 397. No new flat file was "
  f"downloaded; the MFR_COMP fields are present (SHA-256 `{I['4_flat_file']['sha256'][:16]}…`, member date {I['4_flat_file']['member_date']}).")
w("- **Supplier claims:**")
w("  - Agent run-1: 226 in total, of which 92 are gate-accepted.")
w("  - Silver: 312 S1 and 158 S2, SUPPORTED.")
w("  - No claim stores a character offset, so quotes are located in the parsed text.")
w("")
w("**Strata (supplier block)**")
w("")
w("| split | " + " | ".join(ST) + " |")
w("|---|" + "---|" * len(ST))
prim = I["2_strata"]["primary"]
for s in S:
    w(f"| {NAME[s]} | " + " | ".join(str(sum(v for k, v in prim.items() if k.startswith(s + "|") and k.endswith("|" + t))) for t in ST) + " |")
w("| **all** | " + " | ".join(str(sum(v for k, v in prim.items() if k.endswith("|" + t))) for t in ST) + " |")
w("")
w("OEM_SELF is defined as a declared name normalising to the filer's name (protocol C). The instruction's literal rule, which also counts Supplier Type \"OEM\", "
  "is a sensitivity below.")
w("")
# ---- C(a)(b)
w("## C(a)–(b): agent supplier claims, exact match (primary)")
w("**Recall** is the share of population filings whose declared supplier set is matched by at least one agent claim. **Precision** is the share of agent "
  "supplier claims in population filings that match a declared name.")
w("")
w("| group | filings | recall: all claims | recall: gate-accepted | precision: all claims | precision: gate-accepted |")
w("|---|---|---|---|---|---|")
for g in G:
    m = E[g]
    w(f"| {NAME[g]} | {m['n_filings']} | {sh(m['agent_all']['recall'])} | {sh(m['agent_accepted']['recall'])} | {sh(m['agent_all']['precision'])} | {sh(m['agent_accepted']['precision'])} |")
w("")
w("Precision understates: a correct sub-supplier named only in the chronology counts as a non-match.")
w("")
# ---- C(c)
w("## C(c): silver supplier labels, exact match")
w("| group | filings | recall: S1 + S2 | recall: S2 only (narrative) | precision: S1 (from the block) | precision: S2 (narrative) |")
w("|---|---|---|---|---|---|")
for g in G:
    m = E[g]
    w(f"| {NAME[g]} | {m['n_filings']} | {sh(m['silver_S1_S2']['recall'])} | {sh(m['silver_S2']['recall'])} | {sh(m['silver_S1']['precision'])} | {sh(m['silver_S2']['precision'])} |")
w("")
w("**Circularity of S1.** S1 is Pass A's reading of the block, so its precision is circular. Its non-matches are filings where Pass A's block name differs "
  "from this parser's, such as a joined multi-supplier name or a truncated name. **The informative silver figure is S2**: claims that the narrative names the "
  "declared supplier.")
w("")
# ---- D in/out of block
w("## D: in-block vs out-of-block evidence (exact match)")
w("Each claim's quote is located in the parsed text: in-block, out-of-block, or not located (the quote is not verbatim).")
w("- **Recall by location:** a filing counts if a matching claim with that kind of evidence exists.")
w("- **Precision by location:** claims are partitioned by where their evidence lies.")
w("")
w("| group | set | claims: in-block / out-of-block / not located | recall: in-block evidence | recall: out-of-block evidence | precision: in-block | precision: out-of-block | precision: not located |")
w("|---|---|---|---|---|---|---|---|")
for g in ["testA", "testB", "unseen", "pooled"]:
    for side, lab in (("agent_all", "agent, all"), ("agent_accepted", "agent, accepted"), ("silver_S1", "silver S1"), ("silver_S2", "silver S2")):
        m = E[g][side]; c = m["claims_by_location"]; pl = m["precision_by_location"]
        w(f"| {NAME[g]} | {lab} | {c.get('in_block', 0)} / {c.get('out_of_block', 0)} / {c.get('not_located', 0)} | {sh(m['recall_in_block'], False)} | "
          f"{sh(m['recall_out_of_block'], False)} | {sh(pl['in_block'], False)} | {sh(pl['out_of_block'], False)} | {sh(pl['not_located'], False)} |")
w("")
s1 = PH["silver_S1_located_outside_block"]
w("- **Agent:** has no in-block evidence, as expected; its input contains no block.")
w(f"- **Silver S1:** {s1['n']} S1 quotes are located out of block. **POST HOC diagnostic:** in all {s1['n']} the quote's text (\"Name : X\") also matches "
  f"the page header's \"Manufacturer Name : X\", which comes first; and all {s1['with_an_occurrence_inside_block']} also occur inside the block. Their "
  "out-of-block status is an artefact of the first-match rule, not narrative evidence. Only the **S2** out-of-block matches are informative silver evidence.")
w("")
# ---- C(d)
w("## C(d): agent vs silver, per population filing (exact match)")
w("| group | comparison | agent ✓ / silver ✓ | agent ✓ / silver ✗ | agent ✗ / silver ✓ | agent ✗ / silver ✗ |")
w("|---|---|---|---|---|---|")
for g in ["testA", "testB", "unseen", "pooled"]:
    for k, t in E[g]["d_agent_vs_silver"].items():
        w(f"| {NAME[g]} | {k.replace('_', ' ')} | {t.get('agent match / silver match', 0)} | {t.get('agent match / silver no match', 0)} | "
          f"{t.get('agent no match / silver match', 0)} | {t.get('agent no match / silver no match', 0)} |")
w("")
w("**Reading.** The off-diagonal cells are the disagreements.")
w("- **Agent ✓ / silver ✗ never occurs:** every filing the agent recovers is also covered by silver.")
w("- **Agent ✗ / silver S2 ✓ is large.** Part of it is the evaluation masking: wherever the narrative spells the supplier exactly as the frozen block name, "
  "the agent's input showed `[MASKED]` instead, while the silver S2 labeller saw the name. How much of the cell this explains was not quantified, so the cell "
  "is not read as agent failure.")
w("")
# ---- sensitivities
w("## Pre-declared sensitivity analyses")
w("| level / population | group | filings | agent recall (all) | agent precision (all) | agent recall (accepted) | agent precision (accepted) | silver recall (S1 + S2) | silver S2 recall | silver S2 precision |")
w("|---|---|---|---|---|---|---|---|---|---|")
for lev, lab in (("containment", "token containment"), ("fuzzy_tsr90", "fuzzy token_set_ratio ≥ 90")):
    for g in ["testA", "testB", "unseen", "pooled"]:
        m = R["levels"][lev][g]
        w(f"| {lab} | {NAME[g]} | {m['n_filings']} | {sh(m['agent_all']['recall'], False)} | {sh(m['agent_all']['precision'], False)} | {sh(m['agent_accepted']['recall'], False)} | "
          f"{sh(m['agent_accepted']['precision'], False)} | {sh(m['silver_S1_S2']['recall'], False)} | {sh(m['silver_S2']['recall'], False)} | {sh(m['silver_S2']['precision'], False)} |")
for g in ["testA", "testB", "unseen", "pooled"]:
    m = R["literal_oem_sensitivity"][g]
    w(f"| exact, literal OEM rule (Supplier Type OEM = OEM_SELF) | {NAME[g]} | {m['n_filings']} | {sh(m['agent_all']['recall'], False)} | {sh(m['agent_all']['precision'], False)} | "
      f"{sh(m['agent_accepted']['recall'], False)} | {sh(m['agent_accepted']['precision'], False)} | {sh(m['silver_S1_S2']['recall'], False)} | {sh(m['silver_S2']['recall'], False)} | {sh(m['silver_S2']['precision'], False)} |")
w("")
w("The pooled rows of the containment and fuzzy levels, with CIs:")
w("")
for lev in ("containment", "fuzzy_tsr90"):
    m = R["levels"][lev]["pooled"]
    w(f"- **{lev}:** agent recall (all) {sh(m['agent_all']['recall'])}; agent precision (all) {sh(m['agent_all']['precision'])}; agent precision (accepted) "
      f"{sh(m['agent_accepted']['precision'])}; silver S2 precision {sh(m['silver_S2']['precision'])}.")
w("")
# ---- other strata
w("## Claims in the other strata (counts only, not errors)")
w("| stratum | filings | agent claims (all) | agent claims (accepted) | silver S1 + S2 claims |")
w("|---|---|---|---|---|")
oc = R["other_strata_claim_counts"]["pooled"]
for t in ST:
    if oc.get(f"{t}|filings"):
        w(f"| {t} | {oc.get(t + '|filings', 0)} | {oc.get(t + '|agent claims (all)', 0)} | {oc.get(t + '|agent claims (accepted)', 0)} | {oc.get(t + '|silver S1+S2 claims', 0)} |")
w("")
# ---- components
w("## Components (protocol E)")
w("**Not run: there are no component claims to check.** The frozen agent schema (`tt/agent/schemas.py`) has no component field, and the silver labels have "
  "no component claims.")
w("")
w("The reference exists and is reported for completeness:")
w("- **Involved Components:** a name or part number in 390 of 397 filings, with component names in 389 and part numbers in 355.")
w("- **Flat file:** MFR_COMP_NAME in 392 of 397, MFR_COMP_DESC in 380, MFR_COMP_PTNO in 374.")
w("")
w("The matching rule and the fuzzy threshold (token_set_ratio ≥ 90) are fixed in the protocol for any later component extractor.")
w("")
# ---- post hoc
sf = PH["declared_name_is_short_form_of_filer"]
w("## POST HOC diagnostics (added after seeing results; no protocol change)")
w(f"- **Short forms of the filer's own name.** In {sf['filings']} of {PH['population_filings']} population filings, the declared name is a short form of the "
  "filer's own name (\"X\" for \"X Industries, Inc.\": token containment with a filer name). The pre-declared exact OEM_SELF rule leaves them in "
  "NAMED_SUPPLIER.")
w(f"  - Agent matches inside them: {sf['agent_all_matching_claims_in_them']} of {sf['agent_all_matching_claims_total']} matching claims, and "
  f"{sf['agent_filings_recalled_in_them']} of {sf['agent_filings_recalled_total']} recalled filings.")
w("  - So the agent's matches are not mainly the filer naming itself.")
w(f"- **Silver S1 outside the block:** {s1['n']} S1 quotes are located out of block by the first-match rule; all {s1['with_an_occurrence_inside_block']} also "
  "occur inside the block (section D).")
w("")
w("## Amendments")
w("**SC-A1 (2026-10-29)** (`reports/SC_AMENDMENTS.md`). The 26 Pass-C-decided silver S2 claims store their name in `name`, not in `label`. The script stopped "
  "on them before any comparison, and the name is now read from `name`. **23 of these 26 claims fall in the population;** the silver S2 results that include "
  "them are labelled POST HOC per the protocol rule.")
w("")
w("## Limitations")
w("- **Declared ≠ actual maker.** The reference is what the filer declared: an assembler, a distributor or the filer itself. A match is fidelity to that "
  "declaration, not identification of the true manufacturer. A non-match is not a filer error.")
w("- **Masking and circularity.**")
w("  - The agent saw neither the block nor the masked block name, so its recall is bounded by narrative mentions that the mask missed. Agent vs silver "
  "comparisons are affected by this, by an amount not quantified here.")
w("  - Silver S1 is read from the block (circular). Only out-of-block S2 evidence is independent of the reference.")
w("- **Small accepted n.** Gate-accepted agent claims in the population number 70 pooled, and 17–32 per split, so the intervals are wide; cells with n < 20 "
  "are marked unstable.")
w("- **Parse failures.** None in the 397 filings, but the parser was written on these filings' layouts, and two pointer names (\"See … .pdf\") are counted as "
  "BLANK.")
w(f"- **Normalisation.** No alias list was used. Short forms and parent-subsidiary names (\"Bosch\" vs \"Robert Bosch LLC\") match only at the containment level. "
  f"{sf['filings']} population filings declare a short form of the filer's own name (POST HOC).")
w("- **Quote location.** It takes the first occurrence of the quote; for 14 silver S1 quotes that is the page header (section D). Agent quotes that are not "
  "verbatim cannot be located.")
w(f"- **Flat-file vintage.** The flat file is from {I['4_flat_file']['member_date']} (RCL.txt layout last updated May 2025). It was used here for MFGNAME (the "
  "OEM_SELF test) and for component availability only.")
w("- **Prior-art context.** The owner reports that the DOT OIG (2018) found the component-manufacturer information missing in 16.2% (±8.5%) of 2012–2016 "
  "initial reports. That figure is owner-supplied and was not verified here (protocol G). In these 397 filings, the block names no supplier in 85 (BLANK).")
open("reports/phase_8_supplier_check.md", "w").write("\n".join(L) + "\n")
print("written", len(L))
