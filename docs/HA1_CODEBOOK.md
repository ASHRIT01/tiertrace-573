# HA-1 codebook

Quotation blocks are copied from the frozen `docs/LABELING_RULES.md` unless another source is named. Examples come only from DEV filings and show their AI-made label, which no human has verified.

**How to mark (`reports/HA_PROTOCOL.md`, section C).** Judge each claim from the filing's own text; if the PDF and the shown text differ, the PDF decides.
- **`DATE_OK`:** yes if the claimed date is the date the filing gives this event; format does not matter. No if it belongs to something else, is coarser or finer, drops a qualifier the rules keep, or the sentence is undated prose.
- **`TYPE_OK`:** no if the type is wrong or the sentence is not an event. Use unsure when the rules do not settle the answer.

## Event types

> `FILER_AWARENESS`: a report or notice of the problem reaches the filer, the first one or a later one (customer or dealer report, field report, warranty claim, internal audit finding, notice from NHTSA, the filer "discovered"/"was notified"/"became aware").

> `SUPPLIER_NOTICE`: a supplier, sub-supplier or component maker tells the filer about the problem, a finding, a stop-sale or its own recall ("Supplier X informed us", "received a recall notice from X", "the supplier confirmed ...").

> `INVESTIGATION_START`: an investigation, analysis or testing is opened, started or conducted to find the cause or scope.

> `DECISION`: the decision that a safety defect or noncompliance exists, or the decision to recall.

> `NHTSA_FILING`: the filer submits or amends a Part 573 report, or informs NHTSA that it will recall.

> `OTHER`: any other action or occurrence (containment, stop shipment, meetings, test results, production changes, a supplier's own filing).

**Not events** (a claim on one of these gets `TYPE_OK` = no):

> status statements: "As of <date> there are N claims", "To date there have been no injuries", "X is not aware of ...", "no reports of ...";

> remedy logistics: owner or dealer mailings, notification letters, mailing vendors, repair of the affected vehicles;

> pointers: "See attached chronology", "Please refer to recall 20V-668";

> descriptions with no action ("This design contains two brackets"), beliefs and assumptions ("X believed ...", "We assumed ...");

## FILER_AWARENESS vs INVESTIGATION_START vs OTHER

The frozen rules give no ordered test, so this order only applies their definitions:
1. **Did a report, notice or finding of the problem reach the filer?** `FILER_AWARENESS` ("reaches the filer ... internal audit finding ... 'discovered'"). If a supplier or component maker told the filer, it is `SUPPLIER_NOTICE`.
2. **Was work opened, started or conducted to find the cause or scope?** `INVESTIGATION_START` ("opened, started or conducted").
3. **Is it another action or a result?** `OTHER` ("containment, stop shipment, meetings, test results").

The rules' own mixed example is labelled `INVESTIGATION_START`: "12/3/2014 - Peterbilt Customer Service notified Engineering, and Engineering initiated an investigation." The rules state no general tie-break. If a sentence still fits two types, mark unsure and add a note.

## Worked examples (DEV only)

| Type | Filing | Quote | Date |
|---|---|---|---|
| FILER_AWARENESS | 22V114 | In December 2021, Proterra received a customer report of a steering gearbox failure. | December 2021 |
| FILER_AWARENESS | 18V482 | 7/17/2018 Non-compliance was discovered by engineering during a routine audit. | 7/17/2018 |
| SUPPLIER_NOTICE | 19V850 | On July 26, 2019, BMW was informed by the headlamp control unit supplier of a potential for loss of functionality to the headlamp. | July 26, 2019 |
| SUPPLIER_NOTICE | 15V182 | December 2014, DTNA receives customer segregate, hold, and stop sale from Kidde. | December 2014 |
| INVESTIGATION_START | 15V658 | July 27, 2015 - Airstream opens investigation into the incident. | July 27, 2015 |
| INVESTIGATION_START | 18V293 | 03/24/2018 – Navistar initiates metallurgical testing of suspect bolts. | 03/24/2018 |
| DECISION | 16V928 | December 13, 2016 Product Safety Committee determines that a safety related defect exists and that a recall is required. | December 13, 2016 |
| DECISION | 21V665 | On August 19, 2021, FCA US determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected vehicles. | August 19, 2021 |
| NHTSA_FILING | 15V658 | October 9, 2015 - Airstream submits a 573 to the NHTSA portal. | October 9, 2015 |
| NHTSA_FILING | 16V135 | March 2, 2016 Nova Bus informs NHTSA that a voluntary safety recall will be released to address the safety- related defect | March 2, 2016 |
| OTHER | 18V426 | April 27, 2018 Mazda stopped the shipment and delivery of vehicles with the affected curtain air bags installed. | April 27, 2018 |
| OTHER | 19V811 | 10-14-19 Safety Committee meet - 3 fire on the same floor plan and origin is in the same area (near furnace). | 10-14-19 |

## Date rules

> **Own date:** if the sentence contains a date of its own, the event takes it. `date_text` is the date exactly as written, without a leading "On", "In", "On or about", "approximately" or "around" (keep words like "mid", "early", "late", "end of").

> **Two or more distinct dates in one sentence:** one event per distinct date (for example "notified on Sept 26 that they shipped defective axles in July" gives a Sept 26 event and a July event). A date that only bounds a data window ("vehicles produced between ...", "mfd. 3/24/14-5/22/15", "units built after ...") is not an event date; ignore it.

> **Inherited date (only inside a dated entry or bullet):** a dated entry starts at a sentence that *begins* with a date (no "On"/"In" in front: "12/3/2014 - ...", "May 2019, DTNA received ...", "Sept 2017 - ...") or at a bullet item, and runs until the next such entry, the next bullet, or a blank line. An undated sentence inside that entry is an event with the entry's date

> **Undated sentence in prose:** a sentence with no date of its own that is not inside a dated entry (for example it follows a sentence starting "On June 19, 2020, ...") is still listed, but with `date_inferred: true` and `date_text: ""`. It is not scored.

> A date without a year ("May 16", "11/29") is kept as written.

From the frozen `PREREGISTRATION.md`, rule c (partial and approximate dates):

> 'mid-2017', 'mid-August 2017', 'early/late/end of/beginning of X' are fuzzy. A year-less date takes its year from context only if unambiguous: the one year of all fully dated expressions in the chronology, or, with none, the filing year provided the result is not after the filing date

**DEV date examples:**
- **Partial:** 21V993, "11/29 - Engineering noted a discrepancy of tire sizes during an audit of our fed tags." has the date `11/29`.
- **Fuzzy:** 21V806, "In early October 2021, ..." has the date `early October 2021`.
- **Inherited:** 15V036, "The District Service Manager contacted Peterbilt Customer Service." takes the entry date `12/2/2014`.
