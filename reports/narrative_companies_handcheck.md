# Hand-check: companies named only in the narrative (judged 2026-10-18 by Claude, reading cause + chronology)

Scope: the 35 rule-A hits minus the 8 that are checksheet filings (not touched) = **27 judged**, plus **15 random filings with no rule-A hit**
(seed 0, checksheet and debugged filings excluded). A "narrative-only company" = a named company that is neither the filer nor the
block-named supplier. Role classes: SUPPLY-CHAIN (sub-tier, distributor or other supplier), AFFILIATE (filer's parent, sibling or brand),
CUSTOMER/OTHER (customer, operator, other OEM). Internal committees ("Ford's Critical Concern Review Group") are NOT companies.
These are one reader's judgments, not double-labelled: UNVERIFIED.

## Rule-A hits (27 judged): 20 false positives, 7 true
False positives (internal committee of the filer matched by the suffix "Group"): 15V606-9433, 15V122-1202, 15V865-1479, 15V038-0174,
15V436-2235, 16V735-5959, 16V874-2516, 16V345-0099, 17V652-8824, 20V791-8463, 20V573-7499, 20V178-9403, 20V782-9943, 21V534-4350,
22V917-6757, 23V184-8706, 25V823-0908, 25V403-5235, 26V117-4642, 26V343-5687.
True hits: 16V310-7330 Freedman Seating Company (**SUPPLY-CHAIN**: the seat supplier that notified the filer; block names S&S International);
18V670-8826 Volvo Group (AFFILIATE); 18E065-2341 Polaris Industries (AFFILIATE); 23V317-4406 REV Group (AFFILIATE);
24V545-9256 REV Group (AFFILIATE); 25V265-7002 Jayco Inc. (AFFILIATE); 23V767-5890 DCLI and National Chassis Inc. (CUSTOMER/OTHER).
Rule-A precision for any real company: 7/27 (26%); for a supply-chain company: 1/27 (4%).

## 15 random non-A filings: 5 contain a real narrative-only company that rule A missed (no corporate suffix)
20E075-7667 REV Orlando (CUSTOMER/OTHER); 17V685-6777 Gillig, PACE Transit, airports (CUSTOMER/OTHER); 21V354-9125 MBAG (AFFILIATE);
15V310-0723 Kenworth, Peterbilt (AFFILIATE brands of the filer PACCAR); 22V272-4269 Thomas Built Bus (AFFILIATE).
None of the 15 names a SUPPLY-CHAIN company beyond the block supplier. No company beyond filer/block: 25V653-1400, 22V315-8779,
26V392-6562, 20V402-5139, 24V715-7859, 25V813-3170, 19V724-3364, 23V601-9768, 17V338-2104, 22V892-9108.
Unnamed upstream suppliers ARE referenced in some: 20E075 ("the Steel Supplier"), 22V892 ("Meritor's supplier", a furnace supplier),
21V354 ("the MBUX system supplier"), 20V402 (axle supplier unnamed).

## Totals over the 42 judged
- Narrative-only company of any kind: 12 filings (8 AFFILIATE, 3 CUSTOMER/OTHER, **1 SUPPLY-CHAIN**).
- Named sub-tier / distributor / other supplier beyond the block: **1 of 42 (2%)**; 95% Wilson interval about 0.4% to 12%.
- Rough extrapolation to the 300 (very wide interval, the 15 is small): about a quarter to a third of filings name some company beyond
  filer and block supplier, mostly affiliates and customers, not upstream suppliers.
- Implication (for the go/no-go): named sub-tier suppliers are rare in the narrative. Upstream involvement is mostly an UNNAMED reference
  ("their supplier"), so INSUFFICIENT / NOT_REPORTED is the right status for most tier questions. Rule A should not be reused as a
  detector (74% false positives, mostly committees).
