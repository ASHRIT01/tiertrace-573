# Adjudication sheet (nothing is marked)

A = reports/dev_labels_draft.json at commit 7a97553; B = reports/blind_labels_ai.json. Both sets were produced by AI. For each item mark exactly one box. The PDF section is the text the labels were drawn from.
Part 1: the 14 items where A and B differ. Part 2: 10 items drawn at random (seed 0) from the 37 where they agreed, so you can see how the sheet looks when both passes are the same.
Filings covered: #3, #8, #12, #15, #29.

## Part 1: differences

### Item 1: claim E on draft #3 (RCLRPT-15V658-6735.PDF)
What differs (mechanical): event only in set B

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | (none) | September 22, 2015 |
| type | (none) | INVESTIGATION_START |
| quote | (none) | September 22, 2015 - Airstream notified of a vehicle inverter smoking at a servicing dealership due to loose cabling connections on the positive side of the electrical system. Airstream opens an investigation on the issue. |

PDF section `chronology`:

```
- July 25, 2015 - Airstream notified of a fire in an Interstate motor home vehicle by a servicing dealer. - July 27, 2015 - Airstream opens investigation into the incident. No conclusive determination of the cause could be arrived at due to dealer work that had be done on the vehicle earlier. It was determined that it was not a production line issue. - August 19, 2015 - Production line changed routing of ground wire location due to engineering update. - September 22, 2015 - Airstream notified of a vehicle inverter smoking at a servicing dealership due to loose cabling connections on the positive side of the electrical system. Airstream opens an investigation on the issue. Airstream examines online and inventory vehicles and determines that this is an isolated issue. - October 5, 2015 - Airstream conducts a safety review of both incidents. Considering both incidents together, Airstream decides to conduct a safety recall on the entire vehicle population to insure no vehicles have any issues in the future. - October 9, 2015 - Airstream submits a 573 to the NHTSA portal. -
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 2: claim S2 on draft #8 (RCLRPT-16V870-6167.PDF)
What differs (mechanical): quote span/presence

| field | A (draft) | B (blind) |
|---|---|---|
| status | SUPPORTED | SUPPORTED |
| quote | ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module | ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module, performed an incorrect off seam inboard weld on the inflator manifold. |

PDF section `cause`:

```
ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module, performed an incorrect off seam inboard weld on the inflator manifold. The off seam weld caused the inflator to rupture at the manifold.
```

PDF section `chronology`:

```
On November 13, 2016, RSIAB module supplier Takata reported to GM that, during lot acceptance testing (“LAT”) of an assembled airbag module at 85C, the inflator ruptured. a GM employee submitted a Speak Up For Safety report that same day. GM opened an investigation on November 14, 2016 and immediately initiated actions to trace inflators from the same lot as the failed inflator to potentially impacted plants and vehicles. On November 16, 2016, testing of the failed inflator by ARC, the supplier of the inflator to Takata, identified that the failed inflator had ruptured at its manifold as the result of an incorrect off seam inboard weld but that weld inspection, hydro burst testing and deployment testing indicated that other inflators from the same lot performed normally. On November 18, 2016, GM’s Safety Field Action Decision Authority (SFADA) decided to conduct a safety recall on the entire suspect lot.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 3: claim E on draft #8 (RCLRPT-16V870-6167.PDF)
What differs (mechanical): quote span

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | November 16, 2016 | November 16, 2016 |
| type | OTHER | OTHER |
| quote | On November 16, 2016, testing of the failed inflator by ARC, the supplier of the inflator to Takata, identified that the failed inflator had ruptured at its manifold as the result of an incorrect off seam inboard weld but that weld inspection, hydro burst testing | On November 16, 2016, testing of the failed inflator by ARC, the supplier of the inflator to Takata, identified that the failed inflator had ruptured at its manifold as the result of an incorrect off seam inboard weld |

PDF section `chronology`:

```
On November 13, 2016, RSIAB module supplier Takata reported to GM that, during lot acceptance testing (“LAT”) of an assembled airbag module at 85C, the inflator ruptured. a GM employee submitted a Speak Up For Safety report that same day. GM opened an investigation on November 14, 2016 and immediately initiated actions to trace inflators from the same lot as the failed inflator to potentially impacted plants and vehicles. On November 16, 2016, testing of the failed inflator by ARC, the supplier of the inflator to Takata, identified that the failed inflator had ruptured at its manifold as the result of an incorrect off seam inboard weld but that weld inspection, hydro burst testing and deployment testing indicated that other inflators from the same lot performed normally. On November 18, 2016, GM’s Safety Field Action Decision Authority (SFADA) decided to conduct a safety recall on the entire suspect lot.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 4: claim C on draft #8 (RCLRPT-16V870-6167.PDF)
What differs (mechanical): quote span/presence

| field | A (draft) | B (blind) |
|---|---|---|
| status | SUPPORTED | SUPPORTED |
| quote | performed an incorrect off seam inboard weld on the inflator manifold | performed an incorrect off seam inboard weld on the inflator manifold. The off seam weld caused the inflator to rupture at the manifold. |

PDF section `cause`:

```
ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module, performed an incorrect off seam inboard weld on the inflator manifold. The off seam weld caused the inflator to rupture at the manifold.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 5: claim U on draft #8 (RCLRPT-16V870-6167.PDF)
What differs (mechanical): names: ['Takata', 'ARC Automotive'] vs ['Takata']

| field | A (draft) | B (blind) |
|---|---|---|
| kind | NAMED | NAMED |
| names | Takata, ARC Automotive | Takata |
| quote | ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module | ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module |

PDF section `cause`:

```
ARC Automotive, the supplier of the inflator incorporated by Takata into the RSIAB module, performed an incorrect off seam inboard weld on the inflator manifold. The off seam weld caused the inflator to rupture at the manifold.
```

PDF section `chronology`:

```
On November 13, 2016, RSIAB module supplier Takata reported to GM that, during lot acceptance testing (“LAT”) of an assembled airbag module at 85C, the inflator ruptured. a GM employee submitted a Speak Up For Safety report that same day. GM opened an investigation on November 14, 2016 and immediately initiated actions to trace inflators from the same lot as the failed inflator to potentially impacted plants and vehicles. On November 16, 2016, testing of the failed inflator by ARC, the supplier of the inflator to Takata, identified that the failed inflator had ruptured at its manifold as the result of an incorrect off seam inboard weld but that weld inspection, hydro burst testing and deployment testing indicated that other inflators from the same lot performed normally. On November 18, 2016, GM’s Safety Field Action Decision Authority (SFADA) decided to conduct a safety recall on the entire suspect lot.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 6: claim E on draft #12 (RCLRPT-17V819-6798.PDF)
What differs (mechanical): event only in set B

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | (none) | November 2016 |
| type | (none) | INVESTIGATION_START |
| quote | (none) | In November 2016, incorrect light distribution values were detected in certain vehicles within the assembly plant. Investigations were initiated to identify potentially affected vehicles. |

PDF section `chronology`:

```
In November 2016, incorrect light distribution values were detected in certain vehicles within the assembly plant. Investigations were initiated to identify potentially affected vehicles. Test data from start of production through November 2016 was reviewed. In mid-2017, the review identified that the adjustment device in the assembly plant was set incorrectly regarding the light distribution. Further investigations showed that in the test and initialization specifications for GLC-class headlamps the values from C-class vehicles were initialized from start of production onwards. Further tests were conducted to identify potential effects of incorrectly adjusted headlamps. Glare of oncoming traffic was ruled out. In December 2017, DAG determined that a potential non-compliance regarding the requirements of FMVSS 108 and cannot be ruled out.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 7: claim S2 on draft #15 (RCLRPT-18V293-6049.PDF)
What differs (mechanical): quote span/presence

| field | A (draft) | B (blind) |
|---|---|---|
| status | SUPPORTED | SUPPORTED |
| quote | The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability | The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability and the presence of hydrogen embrittlement in the D-ring bolt. |

PDF section `cause`:

```
The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability and the presence of hydrogen embrittlement in the D-ring bolt.
```

PDF section `chronology`:

```
• 03/22/2018 – Navistar receives reports of broken seat belt D-ring bolts during the assembly process at the Springfield Assembly Plant. • 03/23/2018 – Navistar quarantines vehicles at the Springfield assembly plant. • 03/24/2018 – Navistar initiates metallurgical testing of suspect bolts. • 03/25/2018 – Navistar completes metallurgical testing and initiates investigation to understand the scope of the issue in manufacturing and supplier parts. • 03/26/2016 – Navistar contains the issue at the Springfield assembly plant and repairs quarantined vehicles. • 03/27/2018 – Navistar quarantines vehicles at the Escobedo assembly plant. • 03/28/2018 – Navistar quarantines suspect seat belt bolts at the Parts Distribution Centers. • 04/02/2018 – Navistar certifies seat belt bolts at the Parts distribution Centers. • 04/02/2018 - 04/23/18 – Navistar initiates investigation to understand the scope of the issue with the supplier and their sub suppliers and the impact on International products. • 04/05/2018 – Navistar contains the issue at the Escobedo assembly plant and repairs quarantined vehicles. • 04/24/2018 – Navistar finalizes the suspect population. • 04/26/2018 – Navistar declares a Safety Recall.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 8: claim C on draft #15 (RCLRPT-18V293-6049.PDF)
What differs (mechanical): quote span/presence

| field | A (draft) | B (blind) |
|---|---|---|
| status | SUPPORTED | SUPPORTED |
| quote | did not fully evaluate supplier quality capability and the presence of hydrogen embrittlement in the D-ring bolt | The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability and the presence of hydrogen embrittlement in the D-ring bolt. |

PDF section `cause`:

```
The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability and the presence of hydrogen embrittlement in the D-ring bolt.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 9: claim U on draft #15 (RCLRPT-18V293-6049.PDF)
What differs (mechanical): kind: NAMED vs UNNAMED

| field | A (draft) | B (blind) |
|---|---|---|
| kind | NAMED | UNNAMED |
| names | Shield | (none) |
| quote | The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability | 04/02/2018 - 04/23/18 – Navistar initiates investigation to understand the scope of the issue with the supplier and their sub suppliers and the impact on International products. |

PDF section `cause`:

```
The Shield supplier pre-sourcing evaluation did not fully evaluate supplier quality capability and the presence of hydrogen embrittlement in the D-ring bolt.
```

PDF section `chronology`:

```
• 03/22/2018 – Navistar receives reports of broken seat belt D-ring bolts during the assembly process at the Springfield Assembly Plant. • 03/23/2018 – Navistar quarantines vehicles at the Springfield assembly plant. • 03/24/2018 – Navistar initiates metallurgical testing of suspect bolts. • 03/25/2018 – Navistar completes metallurgical testing and initiates investigation to understand the scope of the issue in manufacturing and supplier parts. • 03/26/2016 – Navistar contains the issue at the Springfield assembly plant and repairs quarantined vehicles. • 03/27/2018 – Navistar quarantines vehicles at the Escobedo assembly plant. • 03/28/2018 – Navistar quarantines suspect seat belt bolts at the Parts Distribution Centers. • 04/02/2018 – Navistar certifies seat belt bolts at the Parts distribution Centers. • 04/02/2018 - 04/23/18 – Navistar initiates investigation to understand the scope of the issue with the supplier and their sub suppliers and the impact on International products. • 04/05/2018 – Navistar contains the issue at the Escobedo assembly plant and repairs quarantined vehicles. • 04/24/2018 – Navistar finalizes the suspect population. • 04/26/2018 – Navistar declares a Safety Recall.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 10: claim E on draft #29 (RCLRPT-22V374-1195.PDF)
What differs (mechanical): date_text: 'May 5, 2022' vs 'On or about May 5, 2022'

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | May 5, 2022 | On or about May 5, 2022 |
| type | FILER_AWARENESS | FILER_AWARENESS |
| quote | On or about May 5, 2022, DTNA received a notification from its Engineering group that, while testing a specific DTNA owned vehicle that had not been sold to commerce, there was a situation that resulted in an unintended brake application. | On or about May 5, 2022, DTNA received a notification from its Engineering group that, while testing a specific DTNA owned vehicle that had not been sold to commerce, there was a situation that resulted in an unintended brake application. |

PDF section `chronology`:

```
On or about May 5, 2022, DTNA received a notification from its Engineering group that, while testing a specific DTNA owned vehicle that had not been sold to commerce, there was a situation that resulted in an unintended brake application. At that time, DTNA believed the issue to be an isolated occurrence on only one vehicle with unknown cause and unknown population. DTNA promptly began an investigation into that vehicle and other vehicles like it, which were produced in only a very limited production run. On or about May 16, DTNA determined that the occurrence could occur on a population of 4 vehicles, as listed on the prior 573 report. On or about May 18, 2022, after DTNA verified the limited population of vehicles potentially subject to the defect to the extent necessary to declare a recall and file that 573 report, out of abundance of caution, DTNA decided to conduct a voluntary safety recall campaign for this very specific group of vehicles to remove the double check valve from the backup pneumatic circuit. As of today, DTNA is not aware of any incidents due to this defect. June 3, 2022, DTNA captured and repaired the 4 vehicles at DTNA’s own expense.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 11: claim E on draft #29 (RCLRPT-22V374-1195.PDF)
What differs (mechanical): date_text: 'May 16' vs 'On or about May 16'

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | May 16 | On or about May 16 |
| type | OTHER | OTHER |
| quote | On or about May 16, DTNA determined that the occurrence could occur on a population of 4 vehicles, as listed on the prior 573 report. | On or about May 16, DTNA determined that the occurrence could occur on a population of 4 vehicles, as listed on the prior 573 report. |

PDF section `chronology`:

```
On or about May 5, 2022, DTNA received a notification from its Engineering group that, while testing a specific DTNA owned vehicle that had not been sold to commerce, there was a situation that resulted in an unintended brake application. At that time, DTNA believed the issue to be an isolated occurrence on only one vehicle with unknown cause and unknown population. DTNA promptly began an investigation into that vehicle and other vehicles like it, which were produced in only a very limited production run. On or about May 16, DTNA determined that the occurrence could occur on a population of 4 vehicles, as listed on the prior 573 report. On or about May 18, 2022, after DTNA verified the limited population of vehicles potentially subject to the defect to the extent necessary to declare a recall and file that 573 report, out of abundance of caution, DTNA decided to conduct a voluntary safety recall campaign for this very specific group of vehicles to remove the double check valve from the backup pneumatic circuit. As of today, DTNA is not aware of any incidents due to this defect. June 3, 2022, DTNA captured and repaired the 4 vehicles at DTNA’s own expense.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 12: claim E on draft #29 (RCLRPT-22V374-1195.PDF)
What differs (mechanical): quote span; date_text: 'May 18, 2022' vs 'On or about May 18, 2022'

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | May 18, 2022 | On or about May 18, 2022 |
| type | DECISION | DECISION |
| quote | On or about May 18, 2022, after DTNA verified the limited population of vehicles potentially subject to the defect to the extent necessary to declare a recall and file that 573 report, out of abundance of caution | On or about May 18, 2022, after DTNA verified the limited population of vehicles potentially subject to the defect to the extent necessary to declare a recall and file that 573 report, out of abundance of caution, DTNA decided to conduct a voluntary safety recall campaign |

PDF section `chronology`:

```
On or about May 5, 2022, DTNA received a notification from its Engineering group that, while testing a specific DTNA owned vehicle that had not been sold to commerce, there was a situation that resulted in an unintended brake application. At that time, DTNA believed the issue to be an isolated occurrence on only one vehicle with unknown cause and unknown population. DTNA promptly began an investigation into that vehicle and other vehicles like it, which were produced in only a very limited production run. On or about May 16, DTNA determined that the occurrence could occur on a population of 4 vehicles, as listed on the prior 573 report. On or about May 18, 2022, after DTNA verified the limited population of vehicles potentially subject to the defect to the extent necessary to declare a recall and file that 573 report, out of abundance of caution, DTNA decided to conduct a voluntary safety recall campaign for this very specific group of vehicles to remove the double check valve from the backup pneumatic circuit. As of today, DTNA is not aware of any incidents due to this defect. June 3, 2022, DTNA captured and repaired the 4 vehicles at DTNA’s own expense.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 13: claim E on draft #29 (RCLRPT-22V374-1195.PDF)
What differs (mechanical): event only in set A

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | June 3, 2022 | (none) |
| type | OTHER | (none) |
| quote | June 3, 2022, DTNA captured and repaired the 4 vehicles at DTNA’s own expense. | (none) |
| value | (none) | (none: no such item in this set) |

PDF section `chronology`:

```
On or about May 5, 2022, DTNA received a notification from its Engineering group that, while testing a specific DTNA owned vehicle that had not been sold to commerce, there was a situation that resulted in an unintended brake application. At that time, DTNA believed the issue to be an isolated occurrence on only one vehicle with unknown cause and unknown population. DTNA promptly began an investigation into that vehicle and other vehicles like it, which were produced in only a very limited production run. On or about May 16, DTNA determined that the occurrence could occur on a population of 4 vehicles, as listed on the prior 573 report. On or about May 18, 2022, after DTNA verified the limited population of vehicles potentially subject to the defect to the extent necessary to declare a recall and file that 573 report, out of abundance of caution, DTNA decided to conduct a voluntary safety recall campaign for this very specific group of vehicles to remove the double check valve from the backup pneumatic circuit. As of today, DTNA is not aware of any incidents due to this defect. June 3, 2022, DTNA captured and repaired the 4 vehicles at DTNA’s own expense.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 14: claim C on draft #29 (RCLRPT-22V374-1195.PDF)
What differs (mechanical): quote span/presence

| field | A (draft) | B (blind) |
|---|---|---|
| status | NOT_REPORTED | NOT_REPORTED |
| quote | NR | (none) |

PDF section `cause`:

```
NR
```

[ ] A right   [ ] B right   [ ] neither: ________________

## Part 2: agreed items (random sample)

### Item 15: claim S1 on draft #3 (RCLRPT-15V658-6735.PDF)
What differs (mechanical): nothing; both passes gave the same value

| field | A (draft) | B (blind) |
|---|---|---|
| status | NOT_REPORTED | NOT_REPORTED |
| quote | Name : NR | Name : NR |

PDF section `block`:

```
Name : NR
Address : NR
     
NR
Country :  NR

```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 16: claim C on draft #12 (RCLRPT-17V819-6798.PDF)
What differs (mechanical): nothing; both passes gave the same value

| field | A (draft) | B (blind) |
|---|---|---|
| status | SUPPORTED | SUPPORTED |
| quote | C-class parameters were used for headlamp adjustment on GLC-class vehicles | C-class parameters were used for headlamp adjustment on GLC-class vehicles. |

PDF section `cause`:

```
C-class parameters were used for headlamp adjustment on GLC-class vehicles.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 17: claim S1 on draft #12 (RCLRPT-17V819-6798.PDF)
What differs (mechanical): nothing; both passes gave the same value

| field | A (draft) | B (blind) |
|---|---|---|
| status | NOT_REPORTED | NOT_REPORTED |
| quote | Name : NR | Name : NR |

PDF section `block`:

```
Name : NR
Address : NR
 NR
Country : NR


```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 18: claim S1 on draft #15 (RCLRPT-18V293-6049.PDF)
What differs (mechanical): nothing; both passes gave the same value

| field | A (draft) | B (blind) |
|---|---|---|
| status | SUPPORTED | SUPPORTED |
| quote | Name : Shield | Name : Shield |

PDF section `block`:

```
Name : Shield
Address : 3802 Gallatin Way
 Elkhart  46514
Country : United States 

```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 19: claim E on draft #15 (RCLRPT-18V293-6049.PDF)
What differs (mechanical): nothing; both passes gave the same value

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | 03/22/2018 | 03/22/2018 |
| type | FILER_AWARENESS | FILER_AWARENESS |
| quote | 03/22/2018 – Navistar receives reports of broken seat belt D-ring bolts during the assembly process at the Springfield Assembly Plant. | 03/22/2018 – Navistar receives reports of broken seat belt D-ring bolts during the assembly process at the Springfield Assembly Plant. |

PDF section `chronology`:

```
• 03/22/2018 – Navistar receives reports of broken seat belt D-ring bolts during the assembly process at the Springfield Assembly Plant. • 03/23/2018 – Navistar quarantines vehicles at the Springfield assembly plant. • 03/24/2018 – Navistar initiates metallurgical testing of suspect bolts. • 03/25/2018 – Navistar completes metallurgical testing and initiates investigation to understand the scope of the issue in manufacturing and supplier parts. • 03/26/2016 – Navistar contains the issue at the Springfield assembly plant and repairs quarantined vehicles. • 03/27/2018 – Navistar quarantines vehicles at the Escobedo assembly plant. • 03/28/2018 – Navistar quarantines suspect seat belt bolts at the Parts Distribution Centers. • 04/02/2018 – Navistar certifies seat belt bolts at the Parts distribution Centers. • 04/02/2018 - 04/23/18 – Navistar initiates investigation to understand the scope of the issue with the supplier and their sub suppliers and the impact on International products. • 04/05/2018 – Navistar contains the issue at the Escobedo assembly plant and repairs quarantined vehicles. • 04/24/2018 – Navistar finalizes the suspect population. • 04/26/2018 – Navistar declares a Safety Recall.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 20: claim E on draft #12 (RCLRPT-17V819-6798.PDF)
What differs (mechanical): nothing; both passes gave the same value

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | mid-2017 | mid-2017 |
| type | OTHER | OTHER |
| quote | In mid-2017, the review identified that the adjustment device in the assembly plant was set incorrectly regarding the light distribution. | In mid-2017, the review identified that the adjustment device in the assembly plant was set incorrectly regarding the light distribution. |

PDF section `chronology`:

```
In November 2016, incorrect light distribution values were detected in certain vehicles within the assembly plant. Investigations were initiated to identify potentially affected vehicles. Test data from start of production through November 2016 was reviewed. In mid-2017, the review identified that the adjustment device in the assembly plant was set incorrectly regarding the light distribution. Further investigations showed that in the test and initialization specifications for GLC-class headlamps the values from C-class vehicles were initialized from start of production onwards. Further tests were conducted to identify potential effects of incorrectly adjusted headlamps. Glare of oncoming traffic was ruled out. In December 2017, DAG determined that a potential non-compliance regarding the requirements of FMVSS 108 and cannot be ruled out.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 21: claim S1 on draft #29 (RCLRPT-22V374-1195.PDF)
What differs (mechanical): nothing; both passes gave the same value

| field | A (draft) | B (blind) |
|---|---|---|
| status | SUPPORTED | SUPPORTED |
| quote | Name : Bendix Corp Heavy Vehicle Systems Group | Name : Bendix Corp Heavy Vehicle Systems Group |

PDF section `block`:

```
Name : Bendix Corp Heavy Vehicle Systems Group
Address : 100 Jessica ln
 Del Rio Texas 78840-8527
Country : United States 

```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 22: claim E on draft #15 (RCLRPT-18V293-6049.PDF)
What differs (mechanical): nothing; both passes gave the same value

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | 04/02/2018 - 04/23/18 | 04/02/2018 - 04/23/18 |
| type | INVESTIGATION_START | INVESTIGATION_START |
| quote | 04/02/2018 - 04/23/18 – Navistar initiates investigation to understand the scope of the issue with the supplier and their sub suppliers and the impact on International products. | 04/02/2018 - 04/23/18 – Navistar initiates investigation to understand the scope of the issue with the supplier and their sub suppliers and the impact on International products. |

PDF section `chronology`:

```
• 03/22/2018 – Navistar receives reports of broken seat belt D-ring bolts during the assembly process at the Springfield Assembly Plant. • 03/23/2018 – Navistar quarantines vehicles at the Springfield assembly plant. • 03/24/2018 – Navistar initiates metallurgical testing of suspect bolts. • 03/25/2018 – Navistar completes metallurgical testing and initiates investigation to understand the scope of the issue in manufacturing and supplier parts. • 03/26/2016 – Navistar contains the issue at the Springfield assembly plant and repairs quarantined vehicles. • 03/27/2018 – Navistar quarantines vehicles at the Escobedo assembly plant. • 03/28/2018 – Navistar quarantines suspect seat belt bolts at the Parts Distribution Centers. • 04/02/2018 – Navistar certifies seat belt bolts at the Parts distribution Centers. • 04/02/2018 - 04/23/18 – Navistar initiates investigation to understand the scope of the issue with the supplier and their sub suppliers and the impact on International products. • 04/05/2018 – Navistar contains the issue at the Escobedo assembly plant and repairs quarantined vehicles. • 04/24/2018 – Navistar finalizes the suspect population. • 04/26/2018 – Navistar declares a Safety Recall.
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 23: claim E on draft #3 (RCLRPT-15V658-6735.PDF)
What differs (mechanical): nothing; both passes gave the same value

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | October 9, 2015 | October 9, 2015 |
| type | NHTSA_FILING | NHTSA_FILING |
| quote | October 9, 2015 - Airstream submits a 573 to the NHTSA portal. | October 9, 2015 - Airstream submits a 573 to the NHTSA portal. |

PDF section `chronology`:

```
- July 25, 2015 - Airstream notified of a fire in an Interstate motor home vehicle by a servicing dealer. - July 27, 2015 - Airstream opens investigation into the incident. No conclusive determination of the cause could be arrived at due to dealer work that had be done on the vehicle earlier. It was determined that it was not a production line issue. - August 19, 2015 - Production line changed routing of ground wire location due to engineering update. - September 22, 2015 - Airstream notified of a vehicle inverter smoking at a servicing dealership due to loose cabling connections on the positive side of the electrical system. Airstream opens an investigation on the issue. Airstream examines online and inventory vehicles and determines that this is an isolated issue. - October 5, 2015 - Airstream conducts a safety review of both incidents. Considering both incidents together, Airstream decides to conduct a safety recall on the entire vehicle population to insure no vehicles have any issues in the future. - October 9, 2015 - Airstream submits a 573 to the NHTSA portal. -
```

[ ] A right   [ ] B right   [ ] neither: ________________

### Item 24: claim E on draft #3 (RCLRPT-15V658-6735.PDF)
What differs (mechanical): nothing; both passes gave the same value

| field | A (draft) | B (blind) |
|---|---|---|
| date_text | September 22, 2015 | September 22, 2015 |
| type | FILER_AWARENESS | FILER_AWARENESS |
| quote | September 22, 2015 - Airstream notified of a vehicle inverter smoking at a servicing dealership due to loose cabling connections on the positive side of the electrical system. | September 22, 2015 - Airstream notified of a vehicle inverter smoking at a servicing dealership due to loose cabling connections on the positive side of the electrical system. |

PDF section `chronology`:

```
- July 25, 2015 - Airstream notified of a fire in an Interstate motor home vehicle by a servicing dealer. - July 27, 2015 - Airstream opens investigation into the incident. No conclusive determination of the cause could be arrived at due to dealer work that had be done on the vehicle earlier. It was determined that it was not a production line issue. - August 19, 2015 - Production line changed routing of ground wire location due to engineering update. - September 22, 2015 - Airstream notified of a vehicle inverter smoking at a servicing dealership due to loose cabling connections on the positive side of the electrical system. Airstream opens an investigation on the issue. Airstream examines online and inventory vehicles and determines that this is an isolated issue. - October 5, 2015 - Airstream conducts a safety review of both incidents. Considering both incidents together, Airstream decides to conduct a safety recall on the entire vehicle population to insure no vehicles have any issues in the future. - October 9, 2015 - Airstream submits a 573 to the NHTSA portal. -
```

[ ] A right   [ ] B right   [ ] neither: ________________
