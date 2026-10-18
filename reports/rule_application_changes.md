# Applying the E and U rules to the 30 dev drafts (2026-10-18)

AI-drafted labels; not human-verified. Rules: see PREREGISTRATION.md (DRAFT, 'Event and upstream rules').

## Step 1 (owner-requested, before the rules)
- #29: removed the June 3, 2022 remedy event ('DTNA captured and repaired the 4 vehicles'). Events 4 -> 3.
- #3: added the Sept 22, 2015 INVESTIGATION_START ('Airstream opens an investigation on the issue.'). Events 6 -> 7.
- #12: added the November 2016 INVESTIGATION_START ('Investigations were initiated to identify potentially affected vehicles.'). Events 3 -> 4.
- Net after step 1: 98 -> 99 events.

## Step 2: E rule applied to all 30 drafts: 99 -> 150 events
- A label is the pair (date, type). Kept unchanged: 97. **Added: 53. Removed: 2. Changed E labels in total: 55.** Re-typed (same date, different type): 0.
- Quotes also changed for most events (they are now single sentences, or start at the entry's date); that is not counted as a label change.
- 55 events carry an inherited date (the entry sentence is stored with them). Filing counts: events per filing now range 0-18; the schema cap on events was raised from 12 to 24 (tt/agent/schemas.py) because #1 has 13 and #24 has 18.

### Removed (2)
- #7 'november 2, 2015' OTHER: "a production issue that occurred during one day of production (November 2, 2015)." — removed because the sentence also carries an earlier-dated event; one event per dated sentence.
- #22 'june 14 and 15, 2020' OTHER: "on June 14 and 15, 2020, conducted additional photometry tests on sample lamps." — removed because the sentence also carries an earlier-dated event; one event per dated sentence.

### Added (53)
- #1 '12/2/2014' FILER_AWARENESS: "The District Service Manager contacted Peterbilt Customer Service."
- #1 '12/2/2014' OTHER: "12/2/2014 - A Peterbilt dealership technician completed steering wheel nut recall (14V-731) on a recalled vehi"
- #1 '12/2/2014' OTHER: "12/2/2014 - A Peterbilt dealership technician completed steering wheel nut recall (14V-731) on a recalled vehi"
- #1 '12/2/2014' OTHER: "12/2/2014 - A Peterbilt dealership technician completed steering wheel nut recall (14V-731) on a recalled vehi"
- #1 '12/3/2014' OTHER: "The Peterbilt plant initiated containment procedures, established a clean point and produced a list of affecte"
- #1 '12/5/2014' OTHER: "12/5/2014 - Engineering found that the horn contact plate on the steering wheel assembly had a tab on the horn"
- #1 '12/5/2014' SUPPLIER_NOTICE: "VIP confirmed that the steering wheels were built incorrectly because an assembler had selected the wrong horn"
- #1 '12/9/2014' OTHER: "12/9/2014 Engineering tested a Pride & Class Model 389 Show Truck parked at Denton that had the ESC option."
- #3 'july 27, 2015' OTHER: "No conclusive determination of the cause could be arrived at due to dealer work that had be done on the vehicl"
- #3 'july 27, 2015' OTHER: "No conclusive determination of the cause could be arrived at due to dealer work that had be done on the vehicl"
- #3 'october 5, 2015' OTHER: "October 5, 2015 - Airstream conducts a safety review of both incidents."
- #3 'september 22, 2015' OTHER: "Airstream examines online and inventory vehicles and determines that this is an isolated issue."
- #6 'nov-2015' OTHER: "Investigation identified universal cap bolts not to proper torque on trucks exhibiting vibration."
- #8 'november 13, 2016' FILER_AWARENESS: "a GM employee submitted a Speak Up For Safety report that same day."
- #9 'mid-august 2017' OTHER: "Subsequently the potentially affected vehicles as well as the production period of potentially affected vehicl"
- #12 'mid-2017' OTHER: "In mid-2017, the review identified that the adjustment device in the assembly plant was set incorrectly regard"
- #12 'mid-2017' OTHER: "In mid-2017, the review identified that the adjustment device in the assembly plant was set incorrectly regard"
- #12 'mid-2017' OTHER: "In mid-2017, the review identified that the adjustment device in the assembly plant was set incorrectly regard"
- #12 'november 2016' OTHER: "Test data from start of production through November 2016 was reviewed."
- #13 '7/17/2018' OTHER: "Production had not installed these reflectors since moving production to new plant."
- #14 'august 30, 2018' OTHER: "CCRG requested an assessment of center seat structural integrity with one or both J- bracket reinforcements mi"
- #14 'september - october 2018' OTHER: "September - October 2018: Directional CAE analysis was conducted on a rigidized body sheet metal structure wit"
- #14 'september - october 2018' OTHER: "September - October 2018: Directional CAE analysis was conducted on a rigidized body sheet metal structure wit"
- #17 'february 2019' OTHER: "February 2019 A review of manufacturing processes identified the lathe used to machine the transmission main s"
- #17 'february 2019' OTHER: "February 2019 A review of manufacturing processes identified the lathe used to machine the transmission main s"
- #17 'january 2019' INVESTIGATION_START: "Honda and the transmission main shaft supplier launched a joint investigation."
- #17 'january 2019' OTHER: "Failed parts analysis confirmed the groove for a gear circlip on the transmission main shaft was out-of-spec."
- #17 'march 2019' FILER_AWARENESS: "March 2019 The first claim from the U.S. market was received, which claimed the motorcycle unexpectedly moved "
- #17 'march 2019' OTHER: "Additional investigation was performed at the transmission main shaft supplier as the motorcycle involved in t"
- #19 'august 2019' INVESTIGATION_START: "Electrical Engineering began testing to determine the root cause."
- #19 'august 2019' OTHER: "When the cause was determined, Engineering worked with a supplier to develop a solid state relay and a sample "
- #19 'jan 2, 2018' OTHER: "A recall was issued, 18V-019."
- #19 'nov to dec 2017' OTHER: "Root cause was identified as damage caused to the starter lock-out relay by a high transient voltage during st"
- #19 'nov to dec 2017' OTHER: "Root cause was identified as damage caused to the starter lock-out relay by a high transient voltage during st"
- #20 '4/20/19' INVESTIGATION_START: "A preliminary investigation is initiated."
- #20 '5/14/19' OTHER: "Research is begun to determine the markets these kits have been shipped to and an Engineering review of each m"
- #21 'july 8, 2020' OTHER: "On July 8, 2020, GM’s investigator was able to duplicate the condition on a 2020 Corvette."
- #21 'june 19, 2020' FILER_AWARENESS: "On June 19, 2020, an auditor at GM’s Bowling Green assembly plant tested the trunk lid release button located "
- #21 'june 19, 2020' OTHER: "The button would not unlatch the trunk lid while the vehicle was in this mode."
- #22 'march 30 and 31, 2020' OTHER: "March 30 and 31, 2020 – Photometry testing was conducted in connection with a change in suppliers for the PCB "
- #24 'august 2019' OTHER: "Testing indicated parts were within specification."
- #24 'august 2019' OTHER: "Testing indicated parts were within specification."
- #24 'august 2019' OTHER: "Testing indicated parts were within specification."
- #24 'january 2020' OTHER: "January 2020, DTNA provided a status update to NHTSA ODI on testing to understand detectability and severity."
- #24 'may 2019' OTHER: "Upon repairing the vehicle, the dealer was able to isolate the failure to the right single modulator valve."
- #24 'may 2019-july 2019' OTHER: "May 2019-July 2019, DTNA performed a preliminary population and warranty seek."
- #24 'may 2019-july 2019' OTHER: "May 2019-July 2019, DTNA performed a preliminary population and warranty seek."
- #24 'november 2019' OTHER: "November 2019, DTNA shared an update of the ongoing investigation with NHTSA ODI, including the low claim rate"
- #24 'october 2019' OTHER: "October 2019, DTNA and supplier began reviewing vehicle routes and chemical wash processes, with ongoing corro"
- #24 'october 2019' OTHER: "October 2019, DTNA and supplier began reviewing vehicle routes and chemical wash processes, with ongoing corro"
- #29 'may 5, 2022' INVESTIGATION_START: "DTNA promptly began an investigation into that vehicle and other vehicles like it, which were produced in only"
- #30 'december 2021' OTHER: "Proterra investigated and determined the root cause of this failure was the same as the root cause of two 2020"
- #30 'february 21, 2022' OTHER: "On February 21, 2022, the Committee reviewed the investigation findings, including the supplier’s production r"

### Sentences in dated chronologies that are NOT events, with the reason (37)
- #1: "During vehicle operation the truck gave no indication or warning of a damaged sensor." — descriptive (no action)
- #1: "Corrective Action - VIP Engineering implemented process changes to ensure that the assembl" — corrective action under no date of its own (would wrongly inherit 12/9/2014)
- #4: "June 30, 2015." — pointer chronology (date is of the attached document)
- #9: "To date Daimler AG is not aware of any customer complaints concerning this matter." — status/absence
- #14: "This seat track assembly design contains two J-channel reinforcement brackets, one left- h" — descriptive (design description, no action)
- #14: "Ford is not aware of any reports of accident or injury related to this condition." — status/absence
- #15: "04/02/2018" — fragment: the first date of the range '04/02/2018 - 04/23/18'
- #17: "As of May 28, 2019, Honda has received two warranty claims and no reports of injuries or c" — status/absence
- #20: "To date, there have been no identified crashes or injuries associated with this defect." — status/absence
- #21: "GM is not aware of any field incidents related to this condition." — status/absence
- #22: "There have been no known complaints, accidents or injuries related to this noncompliance." — status/absence
- #26: "6/02/21 Started process with outside company to gather all customers information." — remedy logistics (gathering customer information for mailings)
- #26: "Once we have this information we will send to Dometic contact "STERICYCLE" for processing." — remedy logistics
- #26: "7/20/21 All custome and dealer contacts sent to "STERICYLE" to start the recall process at" — remedy logistics
- #26: "7/23/21 Followed up with Dometic contact on letter" — remedy logistics (follow-up on the letter)
- #26: "7/27/21 as of this date we have not heard of any units with "leaks" or issues from custome" — status/absence
- #26: "7/27/21 Stericycle sent email they apologize for not responding and they will start the pr" — remedy logistics
- #26: "7/30/21 Stericycle send email via DocuSign to approve documents to start mailings" — remedy logistics
- #26: "8/13/21 I sent email asking for a update" — remedy logistics (status email)
- #26: "8/16/21 no updated provide from Stericycle" — remedy logistics
- #26: "8/16/21 no "leaks" or issues reported from customers or dealers only asking process" — status statement (no leaks reported)
- #26: "8/16/21 Stericycle emailed that Customer(end user)Letters mailed out" — remedy logistics
- #26: "8/13/21 and Dealer notifications mailed out 8/16." — remedy logistics
- #26: "11/04/21 Emailed Stericycle on update to ensure all customer and dealer letters where deli" — remedy logistics
- #26: "They reported that all dealers letters were delivered and 9 of the consumers have failed." — remedy logistics
- #26: "11/09/21 Emailed Stericycle to ask what is their process on getting the 9 failed letters t" — remedy logistics
- #26: "11/09/21 Received email back from Stericycle they will attempt to locate valid address." — remedy logistics
- #26: "11/22/21 Requested update from Stericycle for the 9 failed addresses from customers." — remedy logistics
- #26: "12/2/21 Email confirmation from Stericycle that all 9 failed customers where mailed out 2n" — remedy logistics
- #26: "12/17/21 No change in 9 undeliverable customer mailings." — status/absence
- #28: "As of August 13, 2021, FCA US is aware of 55 customer assistance records, 806 warranty cla" — status/absence
- #28: "As of August 13, 2021, FCA US is aware of zero accidents and zero injuries potentially rel" — status/absence
- #29: "At that time, DTNA believed the issue to be an isolated occurrence on only one vehicle wit" — belief statement, not an event
- #29: "As of today, DTNA is not aware of any incidents due to this defect." — status/absence
- #29: "June 3, 2022, DTNA captured and repaired the 4 vehicles at DTNA’s own expense." — remedy (repair of the 4 vehicles); removed on owner instruction
- #30: "The vehicle in the December 2021 report was not one of the 169 vehicles included in the 20" — descriptive (which vehicle), no action
- #30: "As of February 21, Proterra knows of no crashes, injuries, or fatalities associated with t" — status/absence

## Step 2: U rule applied to all 30 drafts
- **U labels changed: 0.** U was already consistent: NAMED in the 6 filings where S2 is SUPPORTED or names are listed (#1, #7, #8, #15, #16, #26); no supplier-chain company is named in cause/chronology in any other filing (checked by scanning capitalised names in all 24 non-NAMED filings: only filers, parent groups, regulators and committees appear).
- Counts: NAMED 6, UNNAMED 8, NONE_MENTIONED 10, NOT_REPORTED 6. #15 stays NAMED (Shield is named in the cause); the blind pass's UNNAMED came from reading U as about sub-tier suppliers, which the new rule does not do.

## Checks after applying
- Event date rule: 150 of 150 events pass (own date inside the quote, or date inside the entry sentence that precedes the quote). Quote check: 296 of 296 quotes located verbatim. Tests: 35 pass.
- Judgment calls are mine and unreviewed: which undated sentences count as events (an action or occurrence is an event; descriptions, beliefs, status and no-incident statements, remedy logistics are not) and the type given to each.