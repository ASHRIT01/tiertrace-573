# Hand-check sheet

4 filings per year plus random top-up to 50 (seed 0), latest version, excluding 13 filings opened during development.
Compare PARSED against the PDF. Mark each field OK / WRONG. Do not ask for parser changes tuned to these files.

## 1. RCLRPT-15V370-6865.PDF  (2015, V)
File: `data/audit_raw/RCLRPT-15V370-6865.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Honda (American Honda Motor Co.)' | `'Manufacturer Name : Honda (American Honda Motor Co.)\nSubmission Date : APR 13, 2'` |
| filing date | 2023-04-13 | `'Submission Date : APR 13, 2023\nNHTSA Rec'` |
| supplier name | 'T.K. Holdings, Inc.' | `'Name : T.K. Holdings, Inc.\nAddress : 888 16th Street NW\n Suite 800 Washington  20006\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'NR' | `'Description of the Cause : NR\nIdentification of Any Warning \nthat can Occur : \nNR\nInvolved Components :\nComponent Name  1 : NR\nComponent Description : NR\nComponent Part Number : NR\n\nSupplier Identification :\nComponent Manufacturer   \nName : T.K. Holdings, Inc.\nAddress : 888 16th Street NW\n Suite 800'` |
| chronology (start) | 'May 18, 2015 Takata submitted equipment defect notifications (15E-042, 15E-043) to NHTSA that identified a safety-related defect in the subject passenger frontal airbag inflators. Takata and NHTSA als' | `'Chronology :\nMay 18, 2015 \nTakata submitted equipment defect notifications (15E-042, 15E-043) to NHTSA that identified a safety-related \ndefect in the subject passenger frontal airbag inflators. Takata and NHTSA also executed a Consent Order in \nEA15-001. Copies of Takata’s notifications and the Con'` |

## 2. RCLRPT-15V547-8443.PDF  (2015, V)
File: `data/audit_raw/RCLRPT-15V547-8443.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Spartan Motors USA' | `'Manufacturer Name :  Spartan Motors USA\nSubmission Date : SEP 25,2015\nNHTSA Reca'` |
| filing date | 2015-09-25 | `'Submission Date : SEP 25,2015\nNHTSA Reca'` |
| supplier name | 'Retrac' | `'Name : Retrac\nAddress : 1200 East Birch Street\n     \nBrandon SOUTH DAKOTA 57005\nCountry :  United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The actuator for the mirror had a nylon thread stud and a nylon nut.' | `'Description of the Cause :  The actuator for the mirror had a nylon thread stud and a nylon nut. \nIdentification of Any Warning that can Occur : Mirrors lenses may fall out of the mirror housing without \nwarning.  \n\nPage \n2\n\nSupplier Identification :\nComponent Manufacturer   \nName : Retrac\nAddress :'` |
| chronology (start) | 'In August 2013, Office of Defect Investigations requested information on a service bulletin that was previously submitted by Spartan. In September 2013, Spartan submitted the requested information. On' | `'Chronology :\nIn August 2013, Office of Defect Investigations requested information on a service bulletin that was previously \nsubmitted by Spartan. In September 2013, Spartan submitted the requested information. On July 8, 2015, \nSpartan agreed to submit a defect information report for the issue add'` |

## 3. RCLRPT-15V619-6612.PDF  (2015, V)
File: `data/audit_raw/RCLRPT-15V619-6612.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'C & B Quality Trailer Works, Inc.' | `'Manufacturer Name :  C & B Quality Trailer Works, Inc.\nSubmission Date : SEP 30,'` |
| filing date | 2015-09-30 | `'Submission Date : SEP 30,2015\nNHTSA Reca'` |
| supplier name | 'Henderson Wheel & Supply' | `'Name : Henderson Wheel & Supply\nAddress : 1825 300 W\n     \nSalt Lake City UTAH 84115\nCountry :  United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Improper welds/weld penetration to steel of torsion arm and torsion bar/beam. See MFG of axle for more info.' | `'Description of the Cause :  Improper welds/weld penetration to steel of torsion arm and torsion bar/beam. See \nMFG of axle for more info.\nIdentification of Any Warning that can Occur : Visual inspection of torsion arm welds, crooked looking tire, \ntilted beyond straight.\n\nPage \n2\n\nSupplier Identific'` |
| chronology (start) | 'Henderson Wheel & Supply did all tests and decision making on applying for recall.' | `'Chronology :\nHenderson Wheel & Supply did all tests and decision making on applying for recall.\nDescription of Remedy :\nDescription of Remedy Program : Henderson Wheel & Supply will supply new axle(s) dependent on which \nneed replaced, to the customer, typically to the trailer dealer where the \ntrai'` |

## 4. RCLRPT-15V682-1265.PDF  (2015, V)
File: `data/audit_raw/RCLRPT-15V682-1265.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Volvo Trucks North America' | `'Manufacturer Name :  Volvo Trucks North America\nSubmission Date : OCT 15,2015\nNH'` |
| filing date | 2015-10-15 | `'Submission Date : OCT 15,2015\nNHTSA Reca'` |
| supplier name | 'Eaton Corporation' | `'Name : Eaton Corporation\nAddress : 1000 Eaton Blvd\n     \nCleveland OHIO\nCountry :  United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'According to Eaton, "A spacer assembly that lacks necessary clearance for the transmission\'s main shaft key causes the recall condition by forcing the main shaft key out of Page 2 position. When the m' | `'Description of the Cause :  According to Eaton, "A spacer assembly that lacks necessary clearance for the \ntransmission\'s main shaft key causes the recall condition by forcing the main shaft \nkey out of \n\nPage \n2\n\nposition. When the main shaft key is out of position and the shift lever moves from \nr'` |
| chronology (start) | '9/17/15 Eaton informs Volvo of a potential problem with transmissions they supply 9/18/15 Eaton provides additional information to Volvo. Volvo opens an investigation 10/15/15 Volvo submits preliminar' | `'Chronology :\n9/17/15 Eaton informs Volvo of a potential problem with transmissions they supply \n9/18/15 Eaton provides additional information to Volvo. Volvo opens an investigation \n10/15/15 Volvo submits preliminary defect report to NHTSA \n \nDescription of Remedy :\nDescription of Remedy Program : V'` |

## 5. RCLRPT-15V872-7027.PDF  (2015, V)
File: `data/audit_raw/RCLRPT-15V872-7027.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Allied Recreation Group, Inc.' | `'Manufacturer Name :  Allied Recreation Group, Inc.\nSubmission Date : JAN 05, 201'` |
| filing date | 2016-01-05 | `'Submission Date : JAN 05, 2016\nNHTSA Rec'` |
| supplier name | 'Lippert Components, Inc.' | `'Name : Lippert Components, Inc.\nAddress : PO Box 2888 \n     \nElkhart INDIANA 46515\nCountry :  United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The bolt may fracture from stress on the bolt caused by misuse of the steps, overloading, collision, or other outside influences.' | `'Description of the Cause :  The bolt may fracture from stress on the bolt caused by misuse of the steps, \noverloading, collision, or other outside influences.\nIdentification of Any Warning that can Occur : According to the Part 573 Report filed by Lippert, 15E078, steps \nthat do not fully retract un'` |
| chronology (start) | 'On Wednesday, December 16, 2015, REV Recreation Group ("REV") received a notification letter from Lippert Components, Inc., ("Lippert") advising of their determination that certain double and triple e' | `'Chronology :\n     On Wednesday, December 16, 2015, REV Recreation Group ("REV") received a notification letter from \nLippert Components, Inc., ("Lippert") advising of their determination that certain double and triple entry step \nassemblies may contain a safety-related defect, and describing Lippert'` |

## 6. RCLRPT-16V100-8801.pdf  (2016, V)
File: `data/audit_raw/RCLRPT-16V100-8801.pdf`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Blue Bird Body Company' | `'Manufacturer Name :  Blue Bird Body Company\nSubmission Date : FEB 18, 2016\nNHTSA'` |
| filing date | 2016-02-18 | `'Submission Date : FEB 18, 2016\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n     \nNR\nCountry :  NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'A 3/0 starter cable was possibly incorrectly attached to one of the Power Distribution Unit (PDU) studs on the chassis. Page 2' | `'Description of the Cause :  A 3/0 starter cable was possibly incorrectly attached to one of the Power \nDistribution Unit (PDU) studs on the chassis.  \n\nPage \n2\n\nIdentification of Any Warning that can Occur : Possible engine shutdown.\nSupplier Identification :\nComponent Manufacturer   \nName : NR\nAddr'` |
| chronology (start) | 'June, 2015, one of our dealers reported a thermal event that occurred on a 2008 Vision (BBCV) unit with a CAT C707 engine. November 30, 2015, initial inspection results of the subject bus were made av' | `'Chronology :\nJune, 2015, one of our dealers reported a thermal event that occurred on a 2008 Vision (BBCV) unit with a CAT \nC707 engine.   \nNovember 30, 2015, initial inspection results of the subject bus were made available.   \nFurther evaluations were conducted in an effort to determine root cause'` |

## 7. RCLRPT-16V268-2446.PDF  (2016, V)
File: `data/audit_raw/RCLRPT-16V268-2446.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Volvo Car USA LLC' | `'Manufacturer Name :  Volvo Car USA LLC\nSubmission Date : MAY 03, 2016\nNHTSA Reca'` |
| filing date | 2016-05-03 | `'Submission Date : MAY 03, 2016\nNHTSA Rec'` |
| supplier name | 'Volvo Car Corporation' | `'Name : Volvo Car Corporation\nAddress : SE-405 31\n     \nGothenburg FOREIGN STATES\nCountry :  Sweden\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The switch is not sufficiently recessed to prevent actuation from a 20 mm radius sphere for certain panoramic roof operation cycles. (Testing requirement according to FMVSS No. 118.) Page 2' | `'Description of the Cause :  The switch is not sufficiently recessed to prevent actuation from a 20 mm radius \nsphere for certain panoramic roof operation cycles. (Testing requirement according \nto FMVSS No. 118.) \n\nPage \n2\n\nIdentification of Any Warning that can Occur : The customers will not be awa'` |
| chronology (start) | 'A test conducted on April 13, 2016 demonstrated that the power-operated roof panel system in a pre- production vehicle of the new S90 model would auto-close when pressing the switch in the overhead co' | `'Chronology :\nA test conducted on April 13, 2016 demonstrated that the power-operated roof panel system in a pre-\nproduction vehicle of the new S90 model would auto-close when pressing the switch in the overhead console \nand the roof panel is open. Due to the functionality, the switch can be actuated'` |

## 8. RCLRPT-16V343-7282.PDF  (2016, V)
File: `data/audit_raw/RCLRPT-16V343-7282.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Ford Motor Company' | `'Manufacturer Name : Ford Motor Company\nSubmission Date : MAY 23, 2016\nNHTSA Reca'` |
| filing date | 2016-05-23 | `'Submission Date : MAY 23, 2016\nNHTSA Rec'` |
| supplier name | 'Magna International Incorporated' | `'Name : Magna International Incorporated\nAddress : 400 Courtney Park Drive East\n Mississauga FOREIGN STATES L5T 2S5\nCountry : Canada\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'NR' | `'Description of the Cause : NR\nIdentification of Any Warning \nthat can Occur : \nNR\nSupplier Identification :\nComponent Manufacturer   \nName : Magna International Incorporated\nAddress : 400 Courtney Park Drive East\n Mississauga FOREIGN STATES L5T 2S5\nCountry : Canada\nChronology :\nOn May 10, 2016, Ford'` |
| chronology (start) | 'On May 10, 2016, Ford’s Critical Concern Review Group (CCRG) was informed that certain vehicles were built with the second row center child seat tether anchor concealed by the seat back trim cover. Th' | `'Chronology :\nOn May 10, 2016, Ford’s Critical Concern Review Group (CCRG) was informed that certain vehicles were built \nwith the second row center child seat tether anchor concealed by the seat back trim cover.  The CCRG reviewed \nand elevated the concern.   \n \nOn May 16, 2016, Ford’s Field Review '` |

## 9. RCLRPT-16V521-0781.PDF  (2016, V)
File: `data/audit_raw/RCLRPT-16V521-0781.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'General Motors LLC' | `'Manufacturer Name : General Motors LLC\nSubmission Date : JUL 07, 2016\nNHTSA Reca'` |
| filing date | 2016-07-07 | `'Submission Date : JUL 07, 2016\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n NR\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The MSD was not properly latched into a locked position.' | `'Description of the Cause : The MSD was not properly latched into a locked position.\nIdentification of Any Warning \nthat can Occur : \nNR\n\nSupplier Identification :\nComponent Manufacturer   \nName : NR\nAddress : NR\n NR\nCountry : NR\nChronology :\nOn June 2, 2016, a GM brand quality manager submitted a sp'` |
| chronology (start) | 'On June 2, 2016, a GM brand quality manager submitted a speak up for safety report relating to a 2016 Malibu Hybrid that lost power and stalled during a scheduled ride. On June 6, 2016, GM began inves' | `'Chronology :\nOn June 2, 2016, a GM brand quality manager submitted a speak up for safety report relating to a 2016 Malibu \nHybrid that lost power and stalled during a scheduled ride.  On June 6, 2016, GM began investigating this issue. \nFrom an analysis of the vehicle that stalled, GM determined tha'` |

## 10. RCLRPT-17V581-5957.PDF  (2017, V)
File: `data/audit_raw/RCLRPT-17V581-5957.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Rosenbauer Motors' | `'Manufacturer Name : Rosenbauer Motors\nSubmission Date : SEP 20, 2017\nNHTSA Recal'` |
| filing date | 2017-09-20 | `'Submission Date : SEP 20, 2017\nNHTSA Rec'` |
| supplier name | 'Cummins, Inc.' | `'Name : Cummins, Inc.\n\nAddress : 301 Washington Street\n Columbus INDIANA 47202\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The drive gear mat have benn improperly assembled onto the drive shaft.' | `'Description of the Cause : The drive gear mat have benn improperly assembled onto the drive shaft.\nIdentification of Any Warning \nthat can Occur : \nNR\nSupplier Identification :\nComponent Manufacturer   \nName : Cummins, Inc.\n\nAddress : 301 Washington Street\n Columbus INDIANA 47202\nCountry : United St'` |
| chronology (start) | 'NR' | `'Chronology :\nNR\nDescription of Remedy :\nDescription of Remedy Program : Cummins will replace the component free of charge\nHow Remedy Component Differs \nfrom Recalled Component :\nFurl pumps are assigned serial numbers at the time of assembly.  Remedy \nfuel pumps have different numbers than the recall'` |

## 11. RCLRPT-17V595-7604.PDF  (2017, V)
File: `data/audit_raw/RCLRPT-17V595-7604.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Daimler Vans USA, LLC' | `'Manufacturer Name : Daimler Vans USA, LLC\nSubmission Date : SEP 22, 2017\nNHTSA R'` |
| filing date | 2017-09-22 | `'Submission Date : SEP 22, 2017\nNHTSA Rec'` |
| supplier name | 'Robert Bosch Automotive Steering Kft.' | `'Name : Robert Bosch Automotive Steering Kft.\nAddress : 3300 Kistályai út 2.\n Eger FOREIGN STATES\nCountry : Hungary\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Due to a process deviation at the supplier, certain power steering control units might not meet the requirements regarding the welding of contact pins. Due to a technical weakness in the optically gui' | `'Description of the Cause : Due to a process deviation at the supplier, certain power steering control units \nmight not meet the requirements regarding the welding of contact pins.  Due to \na technical weakness in the optically guided laser welding machine during part \nmanufacturing on supplier site '` |
| chronology (start) | 'In March 2017, DAG received a report regarding a defective steering rack from a passenger car (C-Class) vehicle within the US-market, and immediately requested the return of the part for analysis. In ' | `'Chronology :\nIn March 2017, DAG received a report regarding a defective steering rack from a passenger car (C-Class) \nvehicle within the US-market, and immediately requested the return of the part for analysis. In April 2017, the \nsteering rack was delivered to the supplier, who initiated root-cause'` |

## 12. RCLRPT-17V814-7599.PDF  (2017, V)
File: `data/audit_raw/RCLRPT-17V814-7599.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Ford Motor Company' | `'Manufacturer Name : Ford Motor Company\nSubmission Date : DEC 18, 2017\nNHTSA Reca'` |
| filing date | 2017-12-18 | `'Submission Date : DEC 18, 2017\nNHTSA Rec'` |
| supplier name | 'Visteon' | `'Name : Visteon\nAddress : 1 Village Center Drive\n Township of Van Buren MICHIGAN 48111\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The instrument cluster software checks the status of the internal power supply (IPS) at 10ms after start-up, although it can take as long as 12ms for the IPS to reach stable voltage. If the power supp' | `'Description of the Cause : The instrument cluster software checks the status of the internal power supply \n(IPS) at 10ms after start-up, although it can take as long as 12ms for the IPS to \nreach stable voltage.  If the power supply stability is achieved after the 10ms \ncheck, the software may judge'` |
| chronology (start) | 'November 2017: During a vehicle review at the Flat Rock Assembly Plant , a 2018 model year Mustang did not illuminate the PRNDL display or activate the key-in-the-ignition warning chime when the key w' | `'Chronology :\nNovember 2017: \nDuring a vehicle review at the Flat Rock Assembly Plant , a 2018 model year Mustang did not illuminate the \nPRNDL display or activate the key-in-the-ignition warning chime when the key was turned off and the \ntransmission was not in park.  On Noveber 22, 2017, this issue'` |

## 13. RCLRPT-17V845-8639.PDF  (2017, V)
File: `data/audit_raw/RCLRPT-17V845-8639.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Volvo Bus Corporation' | `'Manufacturer Name : Volvo Bus Corporation\nSubmission Date : DEC 28, 2017\nNHTSA R'` |
| filing date | 2017-12-28 | `'Submission Date : DEC 28, 2017\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n NR\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Manufacturing error, nut attaching cable to stud was not torqued correctly.' | `'Description of the Cause : Manufacturing error, nut attaching cable to stud was not torqued correctly. \nIdentification of Any Warning \nthat can Occur : \nPotential that warning may be provided to driver by interruption of power to \nitems such as dash lighting. \nSupplier Identification :\n\nComponent Ma'` |
| chronology (start) | '2017-12-03 Report received of overheating of the fuse box. 2017-12-19 Info received at VBC in Sweden. Investigation opened 2017-12-20 Delivery stop in production. 2017-12-22 Safety related defect deci' | `'Chronology :\n2017-12-03 Report received of overheating of the fuse box.  \n2017-12-19 Info received at VBC in Sweden. Investigation opened \n2017-12-20 Delivery stop in production. \n2017-12-22 Safety related defect decision \n2017-12-28 573 Report submitted to NHTSA \nDescription of Remedy :\nDescription'` |

## 14. RCLRPT-18V003-7205.PDF  (2018, V)
File: `data/audit_raw/RCLRPT-18V003-7205.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Forest River, Inc.' | `'Manufacturer Name : Forest River, Inc.\nSubmission Date : SEP 27, 2018\nNHTSA Reca'` |
| filing date | 2018-09-27 | `'Submission Date : SEP 27, 2018\nNHTSA Rec'` |
| supplier name | 'DAIMLER TRUCKS NORTH AMERICA, LLC' | `'Name : DAIMLER TRUCKS NORTH AMERICA, LLC\nAddress : P.O. BOX 4090\n PORTLAND OREGON 97208-4090\nCountry : United States \n\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'N/A' | `'Description of the Cause : N/A\nIdentification of Any Warning \nthat can Occur : \nN/A\nSupplier Identification :\nComponent Manufacturer   \nName : DAIMLER TRUCKS NORTH AMERICA, LLC\nAddress : P.O. BOX 4090\n PORTLAND OREGON 97208-4090\nCountry : United States \n\nChronology :\nOn December 22, 2017, Forest Riv'` |
| chronology (start) | 'On December 22, 2017, Forest River’s Office of Corporate Compliance (“OCC”) received a recall notice from Daimler Trucks North America (“DTNA”) containing the VINs affected under DTNA’s Recall Number ' | `'Chronology :\nOn December 22, 2017, Forest River’s Office of Corporate Compliance (“OCC”) received a recall notice from \nDaimler Trucks North America (“DTNA”) containing the VINs affected under DTNA’s Recall Number 17V759 \nand 17V760.  OCC began an investigation to identify the affected vehicles.  On'` |

## 15. RCLRPT-18V361-6855.PDF  (2018, V)
File: `data/audit_raw/RCLRPT-18V361-6855.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Forest River, Inc.' | `'Manufacturer Name : Forest River, Inc.\nSubmission Date : NOV 15, 2018\nNHTSA Reca'` |
| filing date | 2018-11-15 | `'Submission Date : NOV 15, 2018\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n NR\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'An installation error by the manufacturing personnel. Training is planned on the subject to ensure that the Federal Placards and Tire/Rim combinations match.' | `'Description of the Cause : An installation error by the manufacturing personnel.  Training is planned on \nthe subject to ensure that the Federal Placards and Tire/Rim combinations \nmatch.   \nIdentification of Any Warning \nthat can Occur : \nNone\n\nSupplier Identification :\nComponent Manufacturer   \nNa'` |
| chronology (start) | 'On May 25, 2018, Forest River – Office of Corporate Compliance (OCC) was made aware of a potential issue concerning the tire size by the manufacturing facility. Forest River began an investigation whe' | `'Chronology :\nOn May 25, 2018, Forest River – Office of Corporate Compliance (OCC) was made aware of a potential issue \nconcerning the tire size by the manufacturing facility.  Forest River began an investigation whether the \nincorrect tires had been installed. Upon review of the weight data sheets, '` |

## 16. RCLRPT-18V405-6087.PDF  (2018, V)
File: `data/audit_raw/RCLRPT-18V405-6087.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Mercedes-Benz USA, LLC.' | `'Manufacturer Name : Mercedes-Benz USA, LLC.\nSubmission Date : AUG 15, 2018\nNHTSA'` |
| filing date | 2018-08-15 | `'Submission Date : AUG 15, 2018\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n NR\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Due to a documentation issue, the top tether anchorage on the inboard side of the rear seat backrest might be missing.' | `'Description of the Cause : Due to a documentation issue, the top tether anchorage on the inboard side of \nthe rear seat backrest might be missing.\nIdentification of Any Warning \nthat can Occur : \nThe customer will be made aware of the missing anchorage point during child \nseat installation at the ce'` |
| chronology (start) | 'In September 2017 Daimler AG started initial investigations based on feedback from the Australian Vehicle Preparation Center regarding a vehicle with a missing top tether anchorage point on the center' | `'Chronology :\nIn September 2017 Daimler AG started initial investigations based on feedback from the Australian Vehicle \nPreparation Center regarding a vehicle with a missing top tether anchorage point on the center position of the \nrear seat bench. \nIn late 2017 analysis showed that certain vehicles'` |

## 17. RCLRPT-18V908-5711.PDF  (2018, V)
File: `data/audit_raw/RCLRPT-18V908-5711.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Mercedes-Benz USA, LLC.' | `'Manufacturer Name : Mercedes-Benz USA, LLC.\nSubmission Date : APR 19, 2019\nNHTSA'` |
| filing date | 2019-04-19 | `'Submission Date : APR 19, 2019\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n NR\nCountry : NR\n\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Due to a deviation in the assembly process in the production plant, the steering boot may not have been installed according to current production specifications.' | `'Description of the Cause : Due to a deviation in the assembly process in the production plant, the steering \nboot may not have been installed according to current production \nspecifications. \nIdentification of Any Warning \nthat can Occur : \nThe driver may be made aware of the issue by the absence of'` |
| chronology (start) | 'In April 2018, DAG identified two vehicles that showed no deactivation of Active Steering Assist after the driver took his hands permanently off the steering wheel during internal testing. Based on th' | `'Chronology :\nIn April 2018, DAG identified two vehicles that showed no deactivation of Active Steering Assist after the driver \ntook his hands permanently off the steering wheel during internal testing. Based on these incidents, DAG \nlaunched initial investigations for analysis.  \nThese investigatio'` |

## 18. RCLRPT-19E071-8708.PDF  (2019, E)
File: `data/audit_raw/RCLRPT-19E071-8708.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Honda (American Honda Motor Co.)' | `'Manufacturer Name : Honda (American Honda Motor Co.)\nSubmission Date : OCT 17, 2'` |
| filing date | 2019-10-17 | `'Submission Date : OCT 17, 2019\nNHTSA Rec'` |
| supplier name | 'Chaiyoot Factory (1988) Co., Ltd.' | `'Name : Chaiyoot Factory (1988) Co., Ltd.  \nAddress : 45/9 Moo.9 Theparak Rd.,\n Bangpla Bangphli District Samutprakan FOREIGN STATES 10540\nCountry : Thailand\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'NR' | `'Description of the Cause : NR\nIdentification of Any Warning \nthat can Occur : \nNR\n\nSupplier Identification :\nComponent Manufacturer   \nName : Chaiyoot Factory (1988) Co., Ltd.  \nAddress : 45/9 Moo.9 Theparak Rd.,\n Bangpla Bangphli District Samutprakan FOREIGN STATES 10540\nCountry : Thailand\nChronolo'` |
| chronology (start) | 'May to June 2019 Honda received the first report of a broken rear carrier from the Japanese market and launched an investigation. July 2019 Three additional reports of a broken rear carrier were recei' | `'Chronology :\nMay to June 2019 \nHonda received the first report of a broken rear carrier from the Japanese market and launched an \ninvestigation. \n \nJuly 2019 \nThree additional reports of a broken rear carrier were received from the Japanese market. \n  \nAugust 2019 \nPreliminary analysis suspected imp'` |

## 19. RCLRPT-19V069-1382.PDF  (2019, V)
File: `data/audit_raw/RCLRPT-19V069-1382.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Forest River, Inc.' | `'Manufacturer Name : Forest River, Inc.\nSubmission Date : FEB 01, 2019\nNHTSA Reca'` |
| filing date | 2019-02-01 | `'Submission Date : FEB 01, 2019\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n NR\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The process for wiring the break-away switch wire was not consistently followed during production.' | `'Description of the Cause : The process for wiring the break-away switch wire was not consistently \nfollowed during production.\nIdentification of Any Warning \nthat can Occur : \nNone\nSupplier Identification :\nComponent Manufacturer   \nName : NR\nAddress : NR\n NR\nCountry : NR\nChronology :\nDuring the wee'` |
| chronology (start) | 'During the week of January 21st, 2018 after the Corporate Manufacturing Standard was released testing had begun within the manufacturing plants. During the new inspection process which was updated dur' | `'Chronology :\nDuring the week of January 21st, 2018 after the Corporate Manufacturing Standard was released testing had \nbegun within the manufacturing plants. During the new inspection process which was updated during the \nCorporate Standards that had been updated on January 11th, 2019. \nOn January '` |

## 20. RCLRPT-19V146-9045.PDF  (2019, V)
File: `data/audit_raw/RCLRPT-19V146-9045.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'A-1 AUTO ELECTRIC' | `'Manufacturer Name : A-1 AUTO ELECTRIC\nSubmission Date : FEB 28, 2019\nNHTSA Recal'` |
| filing date | 2019-02-28 | `'Submission Date : FEB 28, 2019\nNHTSA Rec'` |
| supplier name | 'Luxfer Canada Ltd' | `'Name : Luxfer Canada Ltd\nAddress : 4410-46 AVE South East\n\n Calgary FOREIGN STATES T2B 3N7\nCountry : Canada\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Design may allow valve to be over-tightened and exceeding the torque and pressure on snap ring.' | `'Description of the Cause : Design may allow valve to be over-tightened and exceeding the torque and \npressure on snap ring.\nIdentification of Any Warning \nthat can Occur : \nOver-tighten using the valve handle\nSupplier Identification :\nComponent Manufacturer   \nName : Luxfer Canada Ltd\nAddress : 4410'` |
| chronology (start) | 'A-1 Alternative Fuel Systems is a company that performs CNG conversions on new vehicles. In 2015 we acquired from a Freightliner dealership a CNG conversion job on fifteen 2015 AutoCar refuse trucks. ' | `'Chronology :\nA-1 Alternative Fuel Systems is a company that performs CNG conversions on new vehicles. In 2015 we \nacquired from a Freightliner dealership a CNG conversion job on fifteen 2015 AutoCar refuse trucks. These \nvehicles were being sold to the City of Los Angeles. Based on the specification'` |

## 21. RCLRPT-19V671-3143.PDF  (2019, V)
File: `data/audit_raw/RCLRPT-19V671-3143.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Heartland Recreational Vehicles, LLC' | `'Manufacturer Name : Heartland Recreational Vehicles, LLC\nSubmission Date : SEP 2'` |
| filing date | 2019-09-20 | `'Submission Date : SEP 20, 2019\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n NR\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Wood backers were not installed in the end walls to which provided the support for the 2 1/2" wood wrapped stiles.' | `'Description of the Cause : Wood backers were not installed in the end walls to which provided the \nsupport for the 2 1/2" wood wrapped stiles. \nIdentification of Any Warning \nthat can Occur : \nThe bunk support stiles not may be secured tight to the walls. \n\nSupplier Identification :\nComponent Manufa'` |
| chronology (start) | 'On 9/19/2019 a dealer called in relaying a problem they noticed with the bunk bed supports. Engineering pulled the prints for this wall and noticed the backers for the bunk supports were not on the pr' | `'Chronology :\nOn 9/19/2019 a dealer called in relaying a problem they noticed with the bunk bed supports. Engineering \npulled the prints for this wall and noticed the backers for the bunk supports were not on the prints for the end \nwall construction.\nDescription of Remedy :\nDescription of Remedy Pro'` |

## 22. RCLRPT-20V012-2152.PDF  (2020, V)
File: `data/audit_raw/RCLRPT-20V012-2152.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Toyota Motor Engineering & Manufacturing' | `'Manufacturer Name : Toyota Motor Engineering & Manufacturing\nSubmission Date : A'` |
| filing date | 2020-04-09 | `'Submission Date : APR 09, 2020\nNHTSA Rec'` |
| supplier name | 'Denso Corporation' | `'Name : Denso Corporation\nAddress : 1-1, Showa-cho\n Kariya-city, Aichi FOREIGN STATES 448-8661\nCountry : Japan\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'NR' | `'Description of the Cause : NR\nIdentification of Any Warning \nthat can Occur : \nNR\nInvolved Components :\nComponent Name  1 : NR\nComponent Description : NR\nComponent Part Number : NR\nSupplier Identification :\nComponent Manufacturer   \nName : Denso Corporation\nAddress : 1-1, Showa-cho\n Kariya-city, Aic'` |
| chronology (start) | 'Please see the attached Amended Part 573 Defect Information Report for the full chronology' | `'Chronology :\nPlease see the attached Amended Part 573 Defect Information Report for the full chronology\n\nDescription of Remedy :\nDescription of Remedy Program : All known owners of the affected Toyota and Lexus vehicles will be \nnotified by first class mail to return their vehicles to a Toyota or Le'` |

## 23. RCLRPT-20V222-8216.PDF  (2020, V)
File: `data/audit_raw/RCLRPT-20V222-8216.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Driverge Vehicle Innovations' | `'Manufacturer Name : Driverge Vehicle Innovations\nSubmission Date : APR 27, 2020\n'` |
| filing date | 2020-04-27 | `'Submission Date : APR 27, 2020\nNHTSA Rec'` |
| supplier name | 'Freedman Seating Company' | `'Name : Freedman Seating Company\nAddress : 4545 W. Augusta Blvd\n Chicago Illinois 60465\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Seat belt retractors may not be compliant to FMVSS 209. Further details not available from equipment manufacturer at the time of this filing.' | `'Description of the Cause : Seat belt retractors may not be compliant to FMVSS 209. Further details not \navailable from equipment manufacturer at the time of this filing.\nIdentification of Any Warning \nthat can Occur : \nSeat belt fail criteria: upon retracting webbing, (1) no webbing can be \nextracte'` |
| chronology (start) | 'Driverge Vehicle Innovations received notification of Recall #20E-004 on 4/13/20 from Freedman Seating Company and began identifying parts and vehicles potentially affected by the recall. Driverge imm' | `'Chronology :\nDriverge Vehicle Innovations received notification of Recall #20E-004 on 4/13/20 from Freedman Seating \nCompany and began identifying parts and vehicles potentially affected by the recall. Driverge immediately \nstopped shipment of all vehicles and the installation of seats with the iden'` |

## 24. RCLRPT-20V259-9360.PDF  (2020, V)
File: `data/audit_raw/RCLRPT-20V259-9360.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Blue Bird Body Company' | `'Manufacturer Name : Blue Bird Body Company\nSubmission Date : MAY 18, 2020\nNHTSA '` |
| filing date | 2020-05-18 | `'Submission Date : MAY 18, 2020\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n NR\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Blue Bird determined that it was discovered that the installation diagram adjustment procedure may not be sufficient for all T3FE bus configurations at GVW when subjected to the 20% grade requirement.' | `'Description of the Cause : Blue Bird determined that it was discovered that the installation diagram \nadjustment procedure may not be sufficient for all T3FE bus configurations at \n\nGVW when subjected to the 20% grade requirement. The adjustment \nprocedure was reviewed and updated to ensure that all'` |
| chronology (start) | 'Chronology on a separate document.' | `'Chronology :\n\nChronology on a separate document.\nDescription of Remedy :\nDescription of Remedy Program : Blue Bird will notify the affected dealers and owners and provide \ninspection instructions for the Orscheln Foot Pedal Park Brake Assembly \n(Part Numbers 10064449 & 10064450). In the event that t'` |

## 25. RCLRPT-20V381-1401.PDF  (2020, V)
File: `data/audit_raw/RCLRPT-20V381-1401.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Porsche Cars North America, Inc.' | `'Manufacturer Name : Porsche Cars North America, Inc.\nSubmission Date : JUL 01, 2'` |
| filing date | 2020-07-01 | `'Submission Date : JUL 01, 2020\nNHTSA Rec'` |
| supplier name | 'MAGNA POWERTRAIN GmbH&Co.KG' | `'Name : MAGNA POWERTRAIN GmbH&Co.KG\nAddress : Industriestrasse 35\n Lannach FOREIGN STATES 8502\nCountry : Austria\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | "Due to an insufficiently robust process at the supplier's production line, one of two threaded joints of the bracket for the front axle differential were only tightened with the initial torque, but no" | `"Description of the Cause : Due to an insufficiently robust process at the supplier's production line, one of \ntwo threaded joints of the bracket for the front axle differential were only \ntightened with the initial torque, but not to the final specified torque.\nIdentification of Any Warning \nthat ca"` |
| chronology (start) | '- In March 2020 three customer complaints were received, concerning loud knocking noises and vibrations that occurred while driving. The issue was attributed to front axle differentials not tightened ' | `'Chronology :\n- In March 2020 three customer complaints were received, concerning loud knocking noises and vibrations \nthat occurred while driving. The issue was attributed to front axle differentials not tightened to specification. \nAll three cases happened in the EU and no further incidents have be'` |

## 26. RCLRPT-20V668-5029.PDF  (2020, V)
File: `data/audit_raw/RCLRPT-20V668-5029.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'General Motors LLC' | `'Manufacturer Name : General Motors LLC\nSubmission Date : OCT 29, 2020\nNHTSA Reca'` |
| filing date | 2020-10-29 | `'Submission Date : OCT 29, 2020\nNHTSA Rec'` |
| supplier name | 'BorgWarner' | `'Name : BorgWarner\nAddress : 600 Highway 32 East\n Water Valley MISSISSIPPI 38965\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'An error in the supplier’s assembly line software logic may have allowed start- stop accumulators to be released from the supplier’s automated bolt torque station without two required bolts.' | `'Description of the Cause : An error in the supplier’s assembly line software logic may have allowed start-\nstop accumulators to be released from the supplier’s automated bolt torque \nstation without two required bolts.\nIdentification of Any Warning \nthat can Occur : \nNR\nInvolved Components :\nCompone'` |
| chronology (start) | 'On July 13, 2020, GM discovered two missing bolts on two start-stop transmission accumulators supplied by Borg Warner at GM’s San Luis Potosi (“SLP”) Assembly plant. GM immediately notified Borg Warne' | `'Chronology :\nOn July 13, 2020, GM discovered two missing bolts on two start-stop transmission accumulators supplied by \nBorg Warner at GM’s San Luis Potosi (“SLP”) Assembly plant.  GM immediately notified Borg Warner and \nstarted containment efforts at SLP by inspecting 21,620 accumulators.  Borg Wa'` |

## 27. RCLRPT-21V232-3340.PDF  (2021, V)
File: `data/audit_raw/RCLRPT-21V232-3340.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Mercedes-Benz USA, LLC' | `'Manufacturer Name : Mercedes-Benz USA, LLC\nSubmission Date : MAY 21, 2021\nNHTSA '` |
| filing date | 2021-05-21 | `'Submission Date : MAY 21, 2021\nNHTSA Rec'` |
| supplier name | 'Mercedes-Benz AG' | `'Name : Mercedes-Benz AG\nAddress : NR\n Foreign States\nCountry : Germany\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Due to a process deviation in the assembly plant, the front wheel arch covers might not have been installed according to current production specifications.' | `'Description of the Cause : Due to a process deviation in the assembly plant, the front wheel arch covers \nmight not have been installed according to current production specifications.\nIdentification of Any Warning \nthat can Occur : \nBefore the issue occurs, the customer may notice a gap between whee'` |
| chronology (start) | 'In July 2020, MBAG launched initial investigations based on an isolated field report describing an instance in which a wheel arch cover had allegedly detached from the vehicle while driving. Further c' | `'Chronology :\nIn July 2020, MBAG launched initial investigations based on an isolated field report describing an instance in \nwhich a wheel arch cover had allegedly detached from the vehicle while driving. \nFurther cases from the field describing similar incidents were reported in August 2020. In par'` |

## 28. RCLRPT-21V289-7210.PDF  (2021, V)
File: `data/audit_raw/RCLRPT-21V289-7210.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'REV Ambulance Group Orlando, Inc.' | `'Manufacturer Name : REV Ambulance Group Orlando, Inc.\nSubmission Date : APR 23, '` |
| filing date | 2021-04-23 | `'Submission Date : APR 23, 2021\nNHTSA Rec'` |
| supplier name | 'Weldon Division of Akron Brass' | `'Name : Weldon Division of Akron Brass\nAddress : 3656 Paragon Drive\n Columbus Ohio 43228\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'NR' | `'Description of the Cause : NR\nIdentification of Any Warning \nthat can Occur : \nNR\nInvolved Components :\n\nComponent Name  1 : V-MUX Vista Interface\nComponent Description : Vista Screen\nComponent Part Number : NR\nSupplier Identification :\nComponent Manufacturer   \nName : Weldon Division of Akron Brass'` |
| chronology (start) | 'REV Ambulance Group Orlando, Inc. (REVO) warranty department received notification from Weldon regarding Equipment recall 20E-078 in early December (12/01/2020). REVO conducted an inventory inspection' | `'Chronology :\nREV Ambulance Group Orlando, Inc. (REVO) warranty department received notification from Weldon \nregarding Equipment recall 20E-078 in early December (12/01/2020). REVO conducted an inventory \ninspection on December 2, 2021, to see if any of the recall population parts were still at REVO'` |

## 29. RCLRPT-21V332-7058.PDF  (2021, V)
File: `data/audit_raw/RCLRPT-21V332-7058.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'E-One Incorporated' | `'Manufacturer Name : E-One Incorporated\nSubmission Date : AUG 26, 2021\nNHTSA Reca'` |
| filing date | 2021-08-26 | `'Submission Date : AUG 26, 2021\nNHTSA Rec'` |
| supplier name | 'Cummins Inc.' | `'Name : Cummins Inc.\nAddress : P.O. Box 3005\n Columbus Indiana 47202-3005\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The rail end sealing bores in the fuel rail may have undersized pilot bores for the sealing washer, thus preventing the washer from properly seating, potentially resulting in inadequate load for the j' | `'Description of the Cause : The rail end sealing bores in the fuel rail may have undersized pilot bores for \nthe sealing washer, thus preventing the washer from properly seating, \npotentially resulting in inadequate load for the joint to remain properly sealed \nin service.\nIdentification of Any Warni'` |
| chronology (start) | 'On April 30, 2021, E-ONE, Inc. received communication from Cummins about recall 21E-032 for their L9 and ISX12 engines. On May 4, 2021, it was agreed that E-ONE, Inc. should file a Part 573.' | `'Chronology :\nOn April 30, 2021, E-ONE, Inc. received communication from Cummins about recall 21E-032 for their L9 and \nISX12 engines.  \n \nOn May 4, 2021, it was agreed that E-ONE, Inc. should file a Part 573.\n\nDescription of Remedy :\nDescription of Remedy Program : A recall-specific reimbursement pl'` |

## 30. RCLRPT-21V892-4129.PDF  (2021, V)
File: `data/audit_raw/RCLRPT-21V892-4129.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Volkswagen Group of America, Inc.' | `'Manufacturer Name : Volkswagen Group of America, Inc.\nSubmission Date : NOV 17, '` |
| filing date | 2021-11-17 | `'Submission Date : NOV 17, 2021\nNHTSA Rec'` |
| supplier name | 'Air International Thermal Systems' | `'Name : Air International Thermal Systems \n \n \n \nAddress : 750 Standard Parkway \n \n \n Auburn Hills \n \n \n \n Michigan 48326 \n \n \n \nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Incorrect manufactured parts at a sub-supplier for the air conditioning system in a certain time frame' | `'Description of the Cause : Incorrect manufactured parts at a sub-supplier for the air conditioning system \nin a certain time frame  \n \n \n \nIdentification of Any Warning \nthat can Occur : \nThe airbag warning light may illuminate if a malfunction is detected.  \n \nInvolved Components :\nComponent Name  '` |
| chronology (start) | 'July 27, 2021: VW Chattanooga receives information about a case in which the airbags deployed without an accident/impact to the vehicle. Analysis started. July 2021 - September, 2021: Root cause analy' | `'Chronology :\nJuly 27, 2021: VW Chattanooga receives information about a case in which the airbags deployed without an \naccident/impact to the vehicle. Analysis started.  \nJuly 2021 - September, 2021: Root cause analysis and determination of potentially affected vehicles with \n\nsupplier initiated. On'` |

## 31. RCLRPT-22V144-8961.PDF  (2022, V)
File: `data/audit_raw/RCLRPT-22V144-8961.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Keystone RV Company' | `'Manufacturer Name : Keystone RV Company\nSubmission Date : MAR 22, 2022\nNHTSA Rec'` |
| filing date | 2022-03-22 | `'Submission Date : MAR 22, 2022\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\n\nAddress : NR\n NR\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The solar panel wiring and battery wiring were not installed properly on the solar controller.' | `'Description of the Cause : The solar panel wiring and battery wiring were not installed properly on the \nsolar controller.\nIdentification of Any Warning \nthat can Occur : \nIt will exhibit either no voltage or more than 14.2 VDC coming out of the \ncontroller.\nInvolved Components :\nComponent Name  1 :'` |
| chronology (start) | '2/22/2022 – Report was made that during a routine audit it was found that solar wiring was wired incorrectly. Investigation opened into claims for solar wiring. 3/3/2022 – Keystone Safety Committee re' | `'Chronology :\n2/22/2022 – Report was made that during a routine audit it was found that solar wiring was wired incorrectly. \nInvestigation opened into claims for solar wiring.   \n3/3/2022 – Keystone Safety Committee reviewed the information on 22 separate claims for wiring that was \nreversed. First c'` |

## 32. RCLRPT-22V355-9384.PDF  (2022, V)
File: `data/audit_raw/RCLRPT-22V355-9384.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Navistar, Inc.' | `'Manufacturer Name : Navistar, Inc.\nSubmission Date : MAY 19, 2022\nNHTSA Recall N'` |
| filing date | 2022-05-19 | `'Submission Date : MAY 19, 2022\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n NR\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The new hydraulic brake line assembly drawing did not contain the torque requirement for the pressure sensor fitting.' | `'Description of the Cause : The new hydraulic brake line assembly drawing did not contain the torque \nrequirement for the pressure sensor fitting.\nIdentification of Any Warning \nthat can Occur : \n• \nProgression of a soft brake pedal condition \n• \nVisible signs of brake fluid leak at the pressure sens'` |
| chronology (start) | '• 04/07/2022 – Navistar assembly plant experienced a CV vehicle with a soft brake pedal. Investigation found that the leak was at the brake pressure sensor • 04/07/2022 – Navistar assembly plant inspe' | `'Chronology :\n• \n04/07/2022 – Navistar assembly plant experienced a CV vehicle with a soft brake pedal.  Investigation \nfound that the leak was at the brake pressure sensor \n• \n04/07/2022 – Navistar assembly plant inspects all brake line assemblies for this configuration that are \nnot yet installed a'` |

## 33. RCLRPT-22V445-7572.PDF  (2022, V)
File: `data/audit_raw/RCLRPT-22V445-7572.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Toyota Motor Engineering & Manufacturing' | `'Manufacturer Name : Toyota Motor Engineering & Manufacturing\nSubmission Date : J'` |
| filing date | 2022-06-23 | `'Submission Date : JUN 23, 2022\nNHTSA Rec'` |
| supplier name | 'Hino Motors Manufacturing USA' | `'Name : Hino Motors Manufacturing USA \nAddress : 45501 Twelve Mile Rd.\n Novi Michigan 48377\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'NR' | `'Description of the Cause : NR\nIdentification of Any Warning \nthat can Occur : \nNR\n\nInvolved Components :\nComponent Name  1 : Bracket Assembly, Caliper Support w/ Bearing, RH\nComponent Description : Axle Shaft Subassembly excluding Shaft\nComponent Part Number : 47870-0C020\nComponent Name  2 : Bracket'` |
| chronology (start) | 'Please see the attached Part 573 Defect Information Report for the full chronology.' | `'Chronology :\nPlease see the attached Part 573 Defect Information Report for the full chronology.\nDescription of Remedy :\nDescription of Remedy Program : All known owners of the subject vehicles will be notified to return their \nvehicles to a Toyota dealer.  For all involved vehicles, the dealers wil'` |

## 34. RCLRPT-22V701-3469.PDF  (2022, V)
File: `data/audit_raw/RCLRPT-22V701-3469.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Volkswagen Group of America, Inc.' | `'Manufacturer Name : Volkswagen Group of America, Inc.\nSubmission Date : SEP 19, '` |
| filing date | 2022-09-19 | `'Submission Date : SEP 19, 2022\nNHTSA Rec'` |
| supplier name | 'Sisecam Automotive Romania' | `'Name : Sisecam Automotive Romania\nAddress : Aleea INDUSTRIILOR 1BIS\n Buzău  \n \n \n Foreign States 120068\nCountry : Romania\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Deviations in the coolant process during the production of the rear window at our supplier company may have resulted in an inhomogeneous stress distribution in the rear window glass. This makes the wi' | `'Description of the Cause : Deviations in the coolant process during the production of the rear window at \nour supplier company may have resulted in an inhomogeneous stress \ndistribution in the rear window glass. This makes the window more susceptible \nto breakages caused by external influences such '` |
| chronology (start) | 'May 27, 2022: On 2 newly produced Audi Q3 vehicles, a broken rear window was discovered at the Audi factory in Hungary. Investigation into cause and gathering of additional information commenced. May ' | `'Chronology :\nMay 27, 2022: On 2 newly produced Audi Q3 vehicles, a broken rear window was discovered at the Audi \nfactory in Hungary. Investigation into cause and gathering of additional information commenced. \nMay - mid-July 2022: Detailed analysis of potential influencing factors together with sup'` |

## 35. RCLRPT-23V176-2072.PDF  (2023, V)
File: `data/audit_raw/RCLRPT-23V176-2072.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Porsche Cars North America, Inc.' | `'Manufacturer Name : Porsche Cars North America, Inc.\nSubmission Date : MAR 30, 2'` |
| filing date | 2023-03-30 | `'Submission Date : MAR 30, 2023\nNHTSA Rec'` |
| supplier name | 'Dr. Ing. h. c. F. Porsche AG' | `'Name : Dr. Ing. h. c. F. Porsche AG\nAddress : NR\n Foreign States\nCountry : Germany\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Due to an incorrect market-specific coding of instrument clusters for Puerto Rico and Canada, the "initial seat belt warning" function is not displayed as legally required on the subject vehicles.' | `'Description of the Cause : Due to an incorrect market-specific coding of instrument clusters for Puerto \nRico and Canada, the "initial seat belt warning" function is not displayed as \nlegally required on the subject vehicles.\nIdentification of Any Warning \nthat can Occur : \nThe seat belt warning ico'` |
| chronology (start) | 'February 21, 2023: Porsche AG learned that some instrument clusters did not perform as expected during an internal check of the market-specific coding. Testing revealed that the "initial seat belt war' | `'Chronology :\nFebruary 21, 2023: Porsche AG learned that some instrument clusters did not perform as expected during an \ninternal check of the market-specific coding. \nTesting revealed that the "initial seat belt warning" function was not displayed correctly. \nAs a result, the suspect software had to'` |

## 36. RCLRPT-23V464-5088.PDF  (2023, V)
File: `data/audit_raw/RCLRPT-23V464-5088.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Mercedes-Benz USA, LLC' | `'Manufacturer Name : Mercedes-Benz USA, LLC\nSubmission Date : JUL 18, 2023\nNHTSA '` |
| filing date | 2023-07-18 | `'Submission Date : JUL 18, 2023\nNHTSA Rec'` |
| supplier name | 'Mercedes-Benz AG' | `'Name : Mercedes-Benz AG\nAddress : NR\n Foreign States\nCountry : Germany\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Due to a deviation in the rework process, the bolts that secure the rear seat belt buckles might not meet torque specifications.' | `'Description of the Cause : Due to a deviation in the rework process, the bolts that secure the rear seat belt \nbuckles might not meet torque specifications. \nIdentification of Any Warning \nthat can Occur : \nThe driver will not receive a warning due to the nature of the failure \nmechanism.\nInvolved C'` |
| chronology (start) | 'At the end of April 2023, MBAG launched initial investigations based on a finding during internal analyses for quality assurance at the production plant. This finding indicated a loose rear seat belt ' | `'Chronology :\nAt the end of April 2023, MBAG launched initial investigations based on a finding during internal analyses for \nquality assurance at the production plant. This finding indicated a loose rear seat belt buckle bolt connection. \nImmediately, analyses were started to determine the root caus'` |

## 37. RCLRPT-23V478-2832.PDF  (2023, V)
File: `data/audit_raw/RCLRPT-23V478-2832.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Toyota Motor Engineering & Manufacturing' | `'Manufacturer Name : Toyota Motor Engineering & Manufacturing\nSubmission Date : F'` |
| filing date | 2024-02-23 | `'Submission Date : FEB 23, 2024\nNHTSA Rec'` |
| supplier name | 'Denso Corporation' | `'Name : Denso Corporation\nAddress : 1-1, Showa-cho, Kariya-city\n Aichi-pref. Foreign States 448-8661\nCountry : Japan\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'NR' | `'Description of the Cause : NR\nIdentification of Any Warning \nthat can Occur : \nNR\nInvolved Components :\n\nComponent Name  1 : Converter Assy, Hybrid Vehicle\nComponent Description : DC-DC Converter\nComponent Part Number : G9270-42060\nSupplier Identification :\nComponent Manufacturer   \nName : Denso Cor'` |
| chronology (start) | 'Please see the attached Part 573 Defect Information Report for the full chronology.' | `'Chronology :\nPlease see the attached Part 573 Defect Information Report for the full chronology.\nDescription of Remedy :\nDescription of Remedy Program : All known owners of the subject vehicles will be notified to return their \nvehicles to a Toyota and Lexus dealer.  The dealers will replace the DC-'` |

## 38. RCLRPT-23V728-8027.PDF  (2023, V)
File: `data/audit_raw/RCLRPT-23V728-8027.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Winnebago Industries, Inc.' | `'Manufacturer Name : Winnebago Industries, Inc.\nSubmission Date : JAN 24, 2024\nNH'` |
| filing date | 2024-01-24 | `'Submission Date : JAN 24, 2024\nNHTSA Rec'` |
| supplier name | None | `'Name : NR\nAddress : NR\n NR\nCountry : NR\n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'During installation of the structure used to secure the sliding seat, two fasteners were not installed.' | `'Description of the Cause : During installation of the structure used to secure the sliding seat, two \nfasteners were not installed.\nIdentification of Any Warning \nthat can Occur : \nThere are no warnings which occur.\nInvolved Components :\n\nComponent Name  1 : Bracket Asm-Seatbelt\nComponent Descriptio'` |
| chronology (start) | 'On or about October 18, 2023 during normal quality inspections, two fasteners were identified missing from the structure used to secure the sliding seat in the extended position. An investigation was ' | `'Chronology :\nOn or about October 18, 2023 during normal quality inspections, two fasteners were identified missing from \nthe structure used to secure the sliding seat in the extended position.  An investigation was opened.  The \nProduct Safety Committee met to review the findings of the investigatio'` |

## 39. RCLRPT-24V043-9157.PDF  (2024, V)
File: `data/audit_raw/RCLRPT-24V043-9157.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'PACCAR Incorporated' | `'Manufacturer Name : PACCAR Incorporated\nSubmission Date : MAY 10, 2024\nNHTSA Rec'` |
| filing date | 2024-05-10 | `'Submission Date : MAY 10, 2024\nNHTSA Rec'` |
| supplier name | 'Hendrickson' | `'\nName : Hendrickson\nAddress : 2021 Parkside Drive\n Schaumburg Illinois 60173\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Hendrickson identified excessive wear on the tooling used to install the journal rings and inadequate quality measurements performed after such installations.' | `'Description of the Cause : Hendrickson identified excessive wear on the tooling used to install the journal \nrings and inadequate quality measurements performed after such installations. \nIdentification of Any Warning \nthat can Occur : \nPotential signs of oil lubricant leaking from the wheel end hub'` |
| chronology (start) | 'Dec 15, 2023: Hendrickson sent NHTSA filing to PACCAR Safety and Compliance. Dec 25, 2023: Safety and Compliance gathering location of affected population. Jan 8, 2023: S&C finished gathering informat' | `'Chronology :\nDec 15, 2023: Hendrickson sent NHTSA filing to PACCAR Safety and Compliance.  \n \nDec 25, 2023: Safety and Compliance gathering location of affected population. \n \nJan 8, 2023: S&C finished gathering information of chassis list provided by Hendrickson. \n \nJan 9, 2023: S&C reached out to '` |

## 40. RCLRPT-24V238-4544.PDF  (2024, V)
File: `data/audit_raw/RCLRPT-24V238-4544.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Chrysler (FCA US, LLC) (Stellantis)' | `'Manufacturer Name : Chrysler (FCA US, LLC) (Stellantis)\nSubmission Date : MAR 28'` |
| filing date | 2024-03-28 | `'Submission Date : MAR 28, 2024\nNHTSA Rec'` |
| supplier name | '3M' | `'Name : 3M\nAddress : 3M Center\n 223-3S-33 St Paul Minnesota 55144-1000\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'NR' | `'Description of the Cause : NR\nIdentification of Any Warning \nthat can Occur : \nNone\nInvolved Components :\n\nComponent Name  1 : Scotch Masking Tape 2800\nComponent Description : Masking Tape\nComponent Part Number : 3M ID 7100194288\nSupplier Identification :\nComponent Manufacturer   \nName : 3M\nAddress '` |
| chronology (start) | '• On January 13, 2024, the FCA US LLC ("FCA US") Technical Safety and Regulatory Compliance ("TSRC") organization was notified of a potential issue related to some Chrysler Pacifica/Voyager vehicles b' | `'Chronology :\n• On January 13, 2024, the FCA US LLC ("FCA US") Technical Safety and Regulatory Compliance ("TSRC") \norganization was notified of a potential issue related to some Chrysler Pacifica/Voyager vehicles built with \nwindshields that may have low adhesion characteristics to the vehicle body.'` |

## 41. RCLRPT-24V266-5647.PDF  (2024, V)
File: `data/audit_raw/RCLRPT-24V266-5647.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Ford Motor Company' | `'Manufacturer Name : Ford Motor Company\nSubmission Date : APR 12, 2024\nNHTSA Reca'` |
| filing date | 2024-04-12 | `'Submission Date : APR 12, 2024\nNHTSA Rec'` |
| supplier name | 'Ford Motor Company' | `'Name : Ford Motor Company\nAddress : 1 American Road\n Dearborn Michigan 48126\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Some Maverick XLT vehicles equipped with the FX4 package and 4k trailer tow package were incorrectly produced with a mini size spare tire instead of a full size spare tire due to a codification error.' | `'Description of the Cause : Some Maverick XLT vehicles equipped with the FX4 package and 4k trailer tow \npackage were incorrectly produced with a mini size spare tire instead of a full \nsize spare tire due to a \ncodification error. The TREAD label was not replaced during the rework \nprocess to instal'` |
| chronology (start) | 'On March 12, 2024, an issue pertaining to 2024MY Ford Maverick vehicles with potentially incorrect spare tire information on the TREAD label was brought to Ford’s Critical Concern Review Group (CCRG) ' | `'Chronology :\nOn March 12, 2024, an issue pertaining to 2024MY Ford Maverick vehicles with potentially incorrect spare tire \ninformation on the TREAD label was brought to Ford’s Critical Concern Review Group (CCRG) for review. \nThe CCRG investigation determined that certain information contained on t'` |

## 42. RCLRPT-24V683-8541.PDF  (2024, V)
File: `data/audit_raw/RCLRPT-24V683-8541.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Ford Motor Company' | `'Manufacturer Name : Ford Motor Company\nSubmission Date : SEP 13, 2024\nNHTSA Reca'` |
| filing date | 2024-09-13 | `'Submission Date : SEP 13, 2024\nNHTSA Rec'` |
| supplier name | 'Ford Motor Company' | `'Name : Ford Motor Company\nAddress : 1 American Road\n Dearborn Michigan 48126\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'Certain 2024 MY Bronco Sport vehicles were inadvertently produced with 2023 MY PCM software. This incorrect PCM software prevents Ford’s Diagnosis and Repair System (FDRS) tool from installing the 24V' | `'Description of the Cause : Certain 2024 MY Bronco Sport vehicles were inadvertently produced with \n2023 MY PCM software. This incorrect PCM software prevents Ford’s Diagnosis \nand Repair System (FDRS) tool from installing the 24V-267 remedy software.  \nIdentification of Any Warning \nthat can Occur :'` |
| chronology (start) | 'On June 18, 2024, an issue pertaining to 2024 MY Bronco Sport vehicles produced with 2023 MY PCM software was brought to Ford’s Critical Concern Group (CCRG) for review. From June – August, 2024, Ford' | `'Chronology :\nOn June 18, 2024, an issue pertaining to 2024 MY Bronco Sport vehicles produced with 2023 MY PCM software \n\nwas brought to Ford’s Critical Concern Group (CCRG) for review. \n \nFrom June – August, 2024, Ford queried the PCM software version on vehicles produced in 2024 MY to identify \nthe'` |

## 43. RCLRPT-25V095-1385.PDF  (2025, V)
File: `data/audit_raw/RCLRPT-25V095-1385.PDF`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Ford Motor Company' | `'Manufacturer Name : Ford Motor Company\nSubmission Date : FEB 24, 2025\nNHTSA Reca'` |
| filing date | 2025-02-24 | `'Submission Date : FEB 24, 2025\nNHTSA Rec'` |
| supplier name | 'Ford Motor Company' | `'Name : Ford Motor Company\nAddress : 1 American Road\n Dearborn Michigan 48126\nCountry : United States \n'` |
| tier | None | `'(heading not found in text)'` |
| cause | 'The dealer instructions to complete the recall instruct the technician to upload the latest software using the service tool, which downloads the latest software from Ford for installation on the vehic' | `'Description of the Cause : The dealer instructions to complete the recall instruct the technician to upload \nthe latest software using the service tool, which downloads the latest software \nfrom Ford for installation on the vehicle.  For these vehicles, the software tool \ndid not upload the correct '` |
| chronology (start) | 'On November 26, 2024, an issue pertaining to incomplete software recall remedies was brought to Ford’s Critical Concern Group for review. This issue was initially identified in a Quality Office forum,' | `'Chronology :\nOn November 26, 2024, an issue pertaining to incomplete software recall remedies was brought to Ford’s \nCritical Concern Group for review.  This issue was initially identified in a Quality Office forum, where an audit \nwas requested for software part numbers applied to a vehicles remedi'` |

## 44. RCLRPT-25V581-3944.pdf  (2025, V)
File: `data/audit_raw/RCLRPT-25V581-3944.pdf`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Altec Industries, Inc.' | `'Manufacturer Name:\nAltec Industries, Inc.\nAddress:\n210 Inverness Center Drive\nBi'` |
| filing date | 2025-09-25 | `'Submission Date: Sep 25, 2025\nNHTSA Reca'` |
| supplier name | None | `'Tier of Supplier:\nSupplier Type:\nName:\nAddress:\nCountry:\n'` |
| tier | None | `'Tier of Supplier:\nSupplier Type:\nName:\nAddress:\nCountry:\nInv'` |
| cause | '' | `'Description of the cause:\nIdentification of any warning that can occur:\nA periodic inspection and circuit load test could identify the potential for a circuit overload. There are no\nother warnings that the circuit is overloaded prior to blowing the fuse.\nComponent Manufacturer\nTier of Supplier:\nSupp'` |
| chronology (start) | 'On July 17, 2024, an inline quality inspection discovered that the 2024 and newer Freightliner Business Class M2 chassis would lose engine power when multiple accessories were switched on. Altec opene' | `'Chronology\nOn July 17, 2024, an inline quality inspection discovered that the 2024 and newer Freightliner Business\nClass M2 chassis would lose engine power when multiple accessories were switched on. Altec opened a\n\nroot-cause investigation across multiple manufacturing divisions to determine why th'` |

## 45. RCLRPT-25V755-3652.pdf  (2025, V)
File: `data/audit_raw/RCLRPT-25V755-3652.pdf`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'McNeilus Truck & Manufacturing, Inc.' | `'Manufacturer Name:\nMcNeilus Truck &\nManufacturing, Inc.\nAddress:\n524 County Road'` |
| filing date | 2025-11-17 | `'Submission Date: Nov 17, 2025\nNHTSA Reca'` |
| supplier name | 'MTM Equipos' | `'Tier of Supplier:\nSupplier Type:\nName:\nMTM Equipos\nAddress:\nForeign States\nCountry:\nMexico\n'` |
| tier | None | `'Tier of Supplier:\nSupplier Type:\nName:\nMTM Equipos\nAddress:\n'` |
| cause | 'Required lamps were omitted during manufacture of the refuse body.' | `'Description of the cause:\nRequired lamps were omitted during manufacture of the refuse body.\nIdentification of any warning that can occur:\nNone.\nComponent Manufacturer\nTier of Supplier:\nSupplier Type:\nName:\nMTM Equipos\nAddress:\nForeign States\nCountry:\nMexico\nInvolved Components\nComponent Name 1:\nref'` |
| chronology (start) | 'In September 2025, in the course of considering whether another model of McNeilus refuse vehicles complied with the requirements of FMVSS 108, McNeilus initiated a review of the lighting on its Metro ' | `'Chronology\nIn September 2025, in the course of considering whether another model of McNeilus refuse vehicles\ncomplied with the requirements of FMVSS 108, McNeilus initiated a review of the lighting on its Metro\nPak model vehicle. McNeilus identified certain Metro Pak vehicles that were produced with'` |

## 46. RCLRPT-25V757-9752.pdf  (2025, V)
File: `data/audit_raw/RCLRPT-25V757-9752.pdf`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Volvo Trucks North America' | `'Manufacturer Name:\nVolvo Trucks North America\nAddress:\n7900 National Service Roa'` |
| filing date | 2025-11-10 | `'Submission Date: Nov 10, 2025\nNHTSA Reca'` |
| supplier name | 'Grote' | `'Tier of Supplier:\nTier 1\nSupplier Type:\nOther\nName:\nGrote\nAddress:\n2600 Lanier Drive\nMadison IN, 47250\nCountry:\nUnited States\n'` |
| tier | 'Tier 1' | `'Tier of Supplier:\nTier 1\nSupplier Type:\nOther\nName:\nGrote\nAd'` |
| cause | 'U.S. Department of Transportation National Highway Traffic Safety Administration Manufacturer Name: Volvo Trucks North America Submission Date: Nov 10, 2025 NHTSA Recall No.: 25V757 Manufacturer Recal' | `'Description of the cause:\nU.S. Department\nof Transportation\nNational Highway\nTraffic Safety\nAdministration\n\nManufacturer Name: Volvo Trucks North America\nSubmission Date: Nov 10, 2025\nNHTSA Recall No.: 25V757\nManufacturer Recall No.: RVXX2509\n\nDuring the production of the marker lights the molding o'` |
| chronology (start) | 'August 12, 2025, Safety Office opens a product safety related issue investigation. August 25, 2025, Product Safety Evaluation Committee review #1 requests additional information. October 20, 2025, Pro' | `'Chronology\nAugust 12, 2025, Safety Office opens a product safety related issue investigation.\nAugust 25, 2025, Product Safety Evaluation Committee review #1 requests additional information.\nOctober 20, 2025, Product Safety Evaluation Committee review #2 recommends escalation to\nProduct\xa0Safety Commit'` |

## 47. RCLRPT-26V002-0368.pdf  (2026, V)
File: `data/audit_raw/RCLRPT-26V002-0368.pdf`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Blue Bird Body Company' | `'Manufacturer Name:\nBlue Bird Body Company\nAddress:\nP.O. Box 937\n402 Blue Bird Bo'` |
| filing date | 2026-01-05 | `'Submission Date: Jan 05, 2026\nNHTSA Reca'` |
| supplier name | 'Blue Bird' | `'Tier of Supplier:\nSupplier Type:\nName:\nBlue Bird\nAddress:\nCountry:\n'` |
| tier | None | `'Tier of Supplier:\nSupplier Type:\nName:\nBlue Bird\nAddress:\nCo'` |
| cause | 'Still under investigation' | `'Description of the cause:\nStill under investigation\nIdentification of any warning that can occur:\nPotential intermittent operation of electrical systems\nComponent Manufacturer\nTier of Supplier:\nSupplier Type:\nName:\nBlue Bird\nAddress:\nCountry:\nInvolved Components\nComponent Name 1:\nComponent Descripti'` |
| chronology (start) | 'November 2025: Report of an electric school bus being involved in an accident. Customer mentioned the vehicle lost propulsion when in motion and collided with a tree. November 2025: Blue Bird Customer' | `'Chronology\nNovember 2025: Report of an electric school bus being involved in an accident. Customer mentioned\nthe vehicle lost propulsion when in motion and collided with a tree.\nNovember 2025: Blue Bird Customer Service team investigated and identified a power cable was\nunsecured at the 12V battery '` |

## 48. RCLRPT-26V061-2359.pdf  (2026, V)
File: `data/audit_raw/RCLRPT-26V061-2359.pdf`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Ford Motor Company' | `'Manufacturer Name:\nFord Motor Company\nAddress:\n20000 Rotunda Drive\nMezzanine\nDea'` |
| filing date | 2026-02-03 | `'Submission Date: Feb 03, 2026\nNHTSA Reca'` |
| supplier name | 'Ford Motor Company' | `'Tier of Supplier:\nSupplier Type:\nOEM\nName:\nFord Motor Company\nAddress:\n1 American Road\nDearborn MI, 48126\nCountry:\nUnited States\n'` |
| tier | None | `'Tier of Supplier:\nSupplier Type:\nOEM\nName:\nFord Motor Compan'` |
| cause | 'The vehicle was modified in preparation for the vehicle’s body lift. During the modification, a substitute bolt was used to secure the engine crossmember to the vehicle body. The substitute bolt may h' | `'Description of the cause:\nThe vehicle was modified in preparation for the vehicle’s body lift. During the modification, a substitute\nbolt was used to secure the engine crossmember to the vehicle body. The substitute bolt may have\nbeen installed without a washer.\nIdentification of any warning that ca'` |
| chronology (start) | 'On July 17, 2025, an issue pertaining to the fasteners used to secure the engine crossmember to the vehicle body on 2023-2024 model year Transit vehicles equipped with the Transit Trail equipment pack' | `'Chronology\nOn July 17, 2025, an issue pertaining to the fasteners used to secure the engine crossmember to the\nvehicle body on 2023-2024 model year Transit vehicles equipped with the Transit Trail equipment\npackage was introduced to Ford’s Critical Concern Review Group (CCRG) for review. During a Fo'` |

## 49. RCLRPT-26V241-8011.pdf  (2026, V)
File: `data/audit_raw/RCLRPT-26V241-8011.pdf`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Winnebago Industries, Inc.' | `'Manufacturer Name:\nWinnebago Industries, Inc.\nAddress:\nPO BOX 152\n605 W. Crystal'` |
| filing date | 2026-04-15 | `'Submission Date: Apr 15, 2026\nNHTSA Reca'` |
| supplier name | 'Winnebago Industries' | `'Tier of Supplier:\nSupplier Type:\nName:\nWinnebago Industries\nAddress:\n605 West Crystal Lake Road\nForest City IA, 50436\nCountry:\nUnited States\n'` |
| tier | None | `'Tier of Supplier:\nSupplier Type:\nName:\nWinnebago Industries\n'` |
| cause | 'During production, the required side marker reflex reflectors were inadvertently omitted from the affected vehicles.' | `'Description of the cause:\nDuring production, the required side marker reflex reflectors were inadvertently omitted from the\naffected vehicles.\nIdentification of any warning that can occur:\nNone. The absence of the reflectors is not accompanied by any warning indicator or symptom\nnoticeable to the dr'` |
| chronology (start) | 'On April 8, 2026, during an engineering review, it was identified that side marker reflex reflectors had been omitted from certain vehicles. On April 9,2026, the Product Safety Committee reviewed this' | `'Chronology\n\nOn April 8, 2026, during an engineering review, it was identified that side marker reflex reflectors had\nbeen omitted from certain vehicles.\nOn April 9,2026, the Product Safety Committee reviewed this issue and approved the need for a Recall.\nRelated NHTSA Recall Number:\nDescription of R'` |

## 50. RCLRPT-26V365-8440.pdf  (2026, V)
File: `data/audit_raw/RCLRPT-26V365-8440.pdf`

| field | PARSED | SOURCE (verbatim window) |
|---|---|---|
| filer | 'Honda (American Honda Motor Co.)' | `'Manufacturer Name:\nHonda (American Honda\nMotor Co.)\nAddress:\n1919 Torrance Blvd.'` |
| filing date | 2026-06-04 | `'Submission Date: Jun 04, 2026\nNHTSA Reca'` |
| supplier name | 'F&P Georgia' | `'Tier of Supplier:\nTier 1\nSupplier Type:\nOEM\nName:\nF&P Georgia\nAddress:\n88 Enterprise Drive SE\nRome GA, 30161\nCountry:\nUnited States\n'` |
| tier | 'Tier 1' | `'Tier of Supplier:\nTier 1\nSupplier Type:\nOEM\nName:\nF&P Georgi'` |
| cause | 'Rear subframes manufactured with improper coating specifications may result in insufficient paint adhesion and premature paint peeling near the arm bracket weld area. In regions where de-icing salt is' | `'Description of the cause:\nRear subframes manufactured with improper coating specifications may result in insufficient paint\nadhesion and premature paint peeling near the arm bracket weld area. In regions where de-icing salt is\nheavily used, the exposed area may corrode prematurely. As the corrosion '` |
| chronology (start) | 'December 2021 Honda identified a difference in paint quality between the supplier’s and Honda test conditions for the rear subframe and initiated further analysis. November 2022 – February 2023 Honda ' | `'Chronology\nDecember 2021\nHonda identified a difference in paint quality between the supplier’s and Honda test conditions for the\nrear subframe and initiated further analysis.\n\xa0\nNovember 2022 – February 2023\nHonda began to monitor and survey vehicles in the US and Canadian markets. \xa0\n\xa0\nJuly – Septemb'` |
