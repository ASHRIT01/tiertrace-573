# PRD corrections (found 2026-10-18; supersede the PRD wording)

1. **The recalls flat file has 29 fields, not 24** (layout: RCL.txt, last updated May 2025; fields 25-27 added March 2020,
   28-29 and longer text fields May 2025). Fields 25-27 are MFR_COMP_NAME, MFR_COMP_DESC, MFR_COMP_PTNO: the manufacturer-supplied
   *component* name, description and part number (non-empty for 6,169 of 11,692 campaigns from 2015). So part numbers are partly
   available in the flat file; the earlier statement "no part-number field" is outdated.
2. **Supplier NAMES appear only in the PDFs.** None of the 29 fields names the component manufacturer; that name exists only in the
   Part 573 PDF's Component Manufacturer block and narrative.
3. **A campaign can have several 573 versions** (163 of 300 sampled campaigns). A later version's submission date can be years after
   the campaign year (e.g. 15V370, latest version dated 2023-04-13). Default evaluation uses the LATEST version (DRAFT, not frozen).
4. **The "Tier of Supplier" field only exists in recent filings** (observed: 0% before 2025; 24% in 2025, 44% in 2026 in our sample).
   A 2015 and a 2018 filing read in full have only Name, Address, Country in the block. Tier for older years can only come from the
   narrative or human labels.
5. **"NR" and blank are different in the source.** Older forms print NR; the newer form (2025+) lets filers leave fields blank.
6. **Text layer:** 300/300 sampled PDFs (2015-2026) have a text layer; no OCR needed in the sample.
