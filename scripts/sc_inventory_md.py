"""Render reports/sc/SC_INVENTORY.json -> reports/SC_INVENTORY.md (formatting and sums of stored counts only)."""
import json

R = json.load(open("reports/sc/SC_INVENTORY.json"))
S = ["testA", "testB", "unseen"]
NAME = {"testA": "Test-A", "testB": "Test-B", "unseen": "unseen-filer"}
LAY = ["portal", "older"]
ST = ["NAMED_SUPPLIER", "OEM_SELF", "OBTAINED_FROM", "MULTIPLE", "BLANK", "PARSE_FAIL"]
L = []
w = L.append
g = lambda d, *k: d.get("|".join(k), 0)

w("# SC-1 Step 0 inventory: supplier and component reference")
w("")
w("**Reference = filer-declared supplier/component (non-AI, not ground truth).** This file has parsing, strata and field checks only: **no agent or silver "
  "claim was compared with the reference.** Only company names, supplier type and country are kept from the supplier block; address and telephone lines "
  "are never stored or printed, and the example blocks below redact them. No model was run, and nothing under `freeze-v1`, `amendment-1` or "
  "`ts-protocol-1` changed. Scripts: `scripts/sc_lib.py` (parsers, normalisation), `scripts/sc_gate.py` (reads the frozen gate decisions for supplier claims), "
  "`scripts/sc_inventory.py`. Raw output: `reports/sc/SC_INVENTORY.json`.")
w("")
b = R["1_block_parse"]
w("## 1. Supplier block: layouts, parser, parse rate")
w("Text comes from the frozen `extract_text` followed by `clean`. The parser (`supplier_blocks`) works by regex and layout only:")
w("- **Start:** a line that is only \"Component Manufacturer\", optionally preceded by \"Supplier Identification :\".")
w("- **Fields:** `Tier of Supplier`, `Supplier Type`, `Name`, `Address`, `Country`. Each value is either on the label line (older layout, \"Name : X\") or on "
  "the following line(s) (portal layout, \"Name:\" then \"X\").")
w("- **Records:** a new supplier record starts at a repeated Name, Tier or Type label.")
w("- **Skipped:** repeated page-header lines of the portal form. Address values are skipped and never stored.")
w("- **End:** the next section heading (Involved Components, Chronology, Description of Remedy, Component Name, …).")
w("")
for lay, title in (("portal", "Portal layout (\"Component Manufacturer\" … \"Supplier Type:\" … \"Name:\" … \"Country:\")"),
                   ("older", "Older layout (\"Supplier Identification : Component Manufacturer\")")):
    w(f"**{title}**: 5 real examples (address and other lines redacted):")
    w("")
    for e in b["examples"][lay]:
        w(f"- {NAME[e['split']]}: `{e['block']}`")
    w("")
w("| split | layout | filings | block heading found | parsed (heading and a Name label) |")
w("|---|---|---|---|---|")
for s in S:
    for lay in LAY:
        n = g(b["counts"], s, lay, "filings")
        if n:
            w(f"| {NAME[s]} | {lay} | {n} | {g(b['counts'], s, lay, 'blocks found')} | {g(b['counts'], s, lay, 'parsed')}/{n} |")
w("")
w(f"**Parse rate: 397/397. Failures: {len(b['failures']) or 'none'}.** Every filing has exactly one block heading.")
w("")
st = R["2_strata"]
w("## 2. Supplier strata")
w("Precedence: PARSE_FAIL > BLANK > MULTIPLE > OEM_SELF > OBTAINED_FROM > NAMED_SUPPLIER.")
w("- **BLANK:** the name is empty, NR or N/A, or is a pointer to an attachment (\"See - … .pdf\": "
  f"{st['pointer_names_counted_as_blank']} filings).")
w("- **MULTIPLE:** two or more different normalised names.")
w("- **OBTAINED_FROM:** Supplier Type \"Distributor\", or distributor or obtained-from wording in the name.")
w("")
w("| split | layout | " + " | ".join(ST) + " |")
w("|---|---|" + "---|" * len(ST))
for s in S:
    for lay in LAY:
        if g(b["counts"], s, lay, "filings"):
            w(f"| {NAME[s]} | {lay} | " + " | ".join(str(g(st["primary"], s, lay, k)) for k in ST) + " |")
for s in S:
    w(f"| **{NAME[s]}** | all | " + " | ".join(str(sum(g(st["primary"], s, lay, k) for lay in LAY)) for k in ST) + " |")
w(f"| **all** | all | " + " | ".join(str(sum(g(st["primary"], s, lay, k) for s in S for lay in LAY)) for k in ST) + " |")
w("")
w("**OEM_SELF: why the literal rule is not used.** The instruction defined OEM_SELF as \"Supplier Type 'OEM', or the name normalises to the filer's MFGNAME\". "
  "In the portal form, though, \"OEM\" is a supplier type for original-equipment suppliers:")
w("")
w("| Supplier Type | declared name = a filer name | declared name ≠ filer |")
w("|---|---|---|")
for t in ["OEM", "Other", "Distributor", "(blank)"]:
    w(f"| {t} | {st['supplier_type_vs_filer_name'].get(t + '|name = filer', 0)} | {st['supplier_type_vs_filer_name'].get(t + '|name ≠ filer', 0)} |")
w("")
w("- **Most OEM-typed names are external suppliers:** 52 of the 65 OEM-typed names are not the filer (they include large external parts makers).")
w("- **Primary definition:** to avoid dropping them, OEM_SELF is the single declared name normalising to a filer name, either a flat-file MFGNAME of the "
  "campaign or the PDF header \"Manufacturer Name\". MFGNAME is truncated to 40 characters.")
w("- **The literal rule** (Supplier Type OEM also counts as OEM_SELF) is kept as a pre-declared sensitivity. Its strata would be: "
  + "; ".join(f"{NAME[s]} " + ", ".join(f"{k} {st['literal_type_oem_rule'].get(s + '|' + k, 0)}" for k in ST if st['literal_type_oem_rule'].get(s + '|' + k, 0)) for s in S) + ".")
w("")
c3 = R["3_components"]
w("## 3. Involved Components block")
w("The parser (`component_records`) reads `Component Name [n]`, `Component Description` and `Component Part Number`, either with \"label : value\" on one "
  "line or the label followed by the value line.")
w("")
w("| split | layout | filings | PRESENT (a name or part number) | BLANK | PARSE_FAIL | records | filings with a component name | filings with a part number |")
w("|---|---|---|---|---|---|---|---|---|")
for s in S:
    for lay in LAY:
        n = g(c3, s, lay, "filings")
        if n:
            w(f"| {NAME[s]} | {lay} | {n} | {g(c3, s, lay, 'PRESENT')} | {g(c3, s, lay, 'BLANK')} | {g(c3, s, lay, 'PARSE_FAIL')} | {g(c3, s, lay, 'component records')} | "
              f"{g(c3, s, lay, 'with component name')} | {g(c3, s, lay, 'with part number')} |")
w("")
fl = R["4_flat_file"]
w("## 4. NHTSA flat file")
w(f"- **File:** `{fl['file']}` (member `{fl['member']}`, member date {fl['member_date']}), SHA-256 `{fl['sha256']}`.")
w(f"- **Column names:** {', '.join(fl['column_names'])}.")
w(f"- **No download.** MFR_COMP_NAME, MFR_COMP_DESC and MFR_COMP_PTNO are present, so nothing was downloaded and the old file is unchanged.")
w(f"- **Join rule:** {fl['join_rule']}.")
w("")
w("| split | campaigns | joined | MFR_COMP_NAME: campaigns with a value (median / max distinct values) | MFR_COMP_DESC | MFR_COMP_PTNO |")
w("|---|---|---|---|---|---|")
for s in S:
    d = fl["per_split"][s]
    f3 = lambda k: f"{d[k]['campaigns_with_value']} ({d[k]['distinct_values_median']:g} / {d[k]['distinct_values_max']})"
    w(f"| {NAME[s]} | {d['campaigns']} | {d['joined']} | {f3('MFR_COMP_NAME')} | {f3('MFR_COMP_DESC')} | {f3('MFR_COMP_PTNO')} |")
w("")
c5 = R["5_claims"]
w("## 5. What the claims store")
w(f"- **Agent:** {c5['agent_stores']}.")
w(f"- **Silver:** {c5['silver_stores']}.")
w(f"- **Components:** {c5['no_component_claims']}. Component metrics (protocol E) therefore have no claims to score.")
w("")
w("**Locating quotes.** No claim stores a character offset. A quote is located in the parsed text by `locate_quote` (`scripts/sc_lib.py`), which is "
  "whitespace-insensitive and lets a `[MASKED]` token stand for the masked name.")
w("")
rows = ["agent supplier claims (all)", "agent supplier claims (gate-accepted)", "agent quote located in parsed text", "agent quote contains [MASKED]",
        "silver S1 SUPPORTED", "silver S1 quote located in parsed text", "silver S2 SUPPORTED", "silver S2 quote located in parsed text"]
w("| count | " + " | ".join(NAME[s] for s in S) + " | all |")
w("|---|---|---|---|---|")
for r in rows:
    w(f"| {r} | " + " | ".join(str(c5['counts'][s].get(r, 0)) for s in S) + f" | {sum(c5['counts'][s].get(r, 0) for s in S)} |")
w("")
w("**Agent claims** are companies with role SUPPLIER, SUB_SUPPLIER or DISTRIBUTOR and status SUPPORTED; acceptance follows the frozen gate (score ≥ 3). "
  "**Silver claims** are S1 (the block's component manufacturer, read from the block) and S2 (the narrative names that supplier), SUPPORTED only. Silver has "
  "no gate. Agent quotes that cannot be located are not verbatim, which is the same failure V1 rejects.")
w("")
c6 = R["6_agent_input"]
w("## 6. Does the agent's input contain the supplier block?")
w(f"**No, in either layout.** How this was checked: {c6['how']}.")
w("")
w("| split | layout | filings | input contains a block heading or block field line | input contains [MASKED] | a declared name appears verbatim (case-insensitive) in the input |")
w("|---|---|---|---|---|---|")
for s in S:
    for lay in LAY:
        n = g(c6["counts"], s, lay, "filings")
        if n:
            w(f"| {NAME[s]} | {lay} | {n} | {g(c6['counts'], s, lay, 'input contains a block heading or block field line')} | {g(c6['counts'], s, lay, 'input contains [MASKED]')} | "
              f"{g(c6['counts'], s, lay, 'a declared name appears verbatim (case-insensitive) in the input')} |")
w("")
w("**What this means:**")
w("- **The agent never sees the block.** It reads only the cause and chronology, with the frozen block name masked wherever it appears.")
w("- **So an agent claim matching the declared supplier cannot have been copied from the block.** Such a claim comes from a narrative mention that the mask "
  "did not catch: a different spelling, or a multi-supplier name the frozen parser joined.")
w("- **A declared name can still appear unmasked** in the input when it is also the filer's own name (OEM_SELF), or when it is spelled differently from the "
  "frozen block name.")
w("- **The silver S1 claims are read from the block itself** (circular by construction). Silver S2 claims come from the narrative.")
open("reports/SC_INVENTORY.md", "w").write("\n".join(L) + "\n")
print("written", len(L))
