import json, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def sections(fn):
    raw = open(os.path.join(T, fn), encoding="utf-8").read()
    fileline = re.search(r"^FILE: (.+)$", raw, re.M).group(1).strip()
    blk = raw.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    cause = raw.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    chron = raw.split("=== CHRONOLOGY ===")[1]
    return fileline, {"block": norm(blk), "cause": norm(cause), "chronology": norm(chron)}


def ev(date, typ, quote, entry=None):
    e = {"date_text": date, "type": typ, "quote": quote}
    if entry is not None:
        e["inherited_date"] = True
        e["entry_quote"] = entry
        e["date_inferred"] = False
    else:
        e["inherited_date"] = False
        e["date_inferred"] = (date == "")
    return e


def lab(fn, s1, s2, cause, up, events):
    return dict(fn=fn, s1=s1, s2=s2, cause=cause, up=up, events=events)


L = []

# 1
q198a = "On February 17, 2023, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into some 2018-2021 MY Dodge Charger and Chrysler 300 vehicles that may have been built with a suspect SABIC inflator that may rupture."
q198b = "From February 17, 2023, through February 20, 2024, FCA US TSRC conducted an analysis of SABIC inflator ruptures and determined that the affected vehicles may have had moisture introduced into the inflator during supplier manufacturing"
L.append(lab("RCLRPT-24V198-2281.txt",
    ("SUPPORTED", "Name : JOYSON SAFETY SYSTEMS"),
    ("INSUFFICIENT", None, q198b, "chronology"),
    ("NOT_REPORTED", "NR"),
    ("UNNAMED", [], q198b, "chronology"),
    [ev("February 17, 2023", "INVESTIGATION_START", q198a),
     ev("February 17, 2023, through February 20, 2024", "INVESTIGATION_START", q198b),
     ev("March 7, 2024", "DECISION", "On March 7, 2024, FCA US determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected vehicles.")]))

# 2
q217g = "Porsche continued investigating this issue together with the battery cell/module manufacturer, using in particular data analytics and hardware analyses."
L.append(lab("RCLRPT-24V217-5008.txt",
    ("SUPPORTED", "Name : LG ENERGY SOLUTION WROCŁAW sp. z o.o."),
    ("INSUFFICIENT", None, q217g, "chronology"),
    ("SUPPORTED", "The root cause analysis suggests that production issues in high-voltage battery modules can increase the risk of internal short circuits."),
    ("UNNAMED", [], q217g, "chronology"),
    [ev("2021", "FILER_AWARENESS", "In 2021 Porsche became aware of a report of a single vehicle battery fire that occurred shortly after charging."),
     ev("", "INVESTIGATION_START", "Porsche investigated this incident and began obtaining comparable undamaged batteries from the field for analysis."),
     ev("2023", "FILER_AWARENESS", "In 2023, Porsche became aware of further instances of battery fires in Taycan vehicles after charging."),
     ev("6 December 2023", "DECISION", "Therefore, although the root cause analysis was still ongoing, on 6 December 2023 Porsche determined that a safety-related defect exists in the identified vehicles (manufacturer recall identification code APB5)."),
     ev("", "INVESTIGATION_START", q217g),
     ev("13 March 2024", "DECISION", "With this additional investigation and analyses, on 13 March 2024 Porsche determined that a safety-related defect exists in additional vehicles identified via data analytics and hardware analyses."),
     ev("13 March 2024", "DECISION", "As there are different batches of potentially affected Porsche Taycan vehicles which require different remedies, Porsche decided to conduct two different recalls on 13 March 2024 (manufacturer recall identification code ARA4 and ARA5)")]))

# 3
L.append(lab("RCLRPT-24V274-3413.txt",
    ("SUPPORTED", "Name : TOKAI RIKA CO., LTD."),
    ("INSUFFICIENT", None, "Name : TOKAI RIKA CO., LTD.", "block"),
    ("NOT_REPORTED", "NR"),
    ("NOT_REPORTED", [], "Please see attached Part 573 Defect Information Report for full chronology.", "chronology"),
    []))

# 4
q276c = "On April 3, 2024, Tesla received notice of a second customer claim of the condition present on an affected vehicle."
L.append(lab("RCLRPT-24V276-7026.txt",
    ("SUPPORTED", "Name : KSR International Inc."),
    ("INSUFFICIENT", None, "Name : KSR International Inc.", "block"),
    ("SUPPORTED", "An unapproved change introduced lubricant (soap) to aid in the component assembly of the pad onto the accelerator pedal."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("March 31, 2024", "FILER_AWARENESS", "On March 31, 2024, Tesla received notice of a customer claim of the condition present on an affected vehicle."),
     ev("April 2, 2024", "INVESTIGATION_START", "On April 2, 2024, Tesla Engineering reviewed the vehicle’s data logs, which confirmed that both brake and accelerator pedals were pressed and the vehicle behaved as intended, meaning the brake pedal cut drive torque and brought the vehicle to a stop."),
     ev("April 3, 2024", "FILER_AWARENESS", q276c),
     ev("April 3, 2024", "INVESTIGATION_START", "In parallel, as part of its ongoing assessment of the condition, Tesla Engineering performed tests to characterize and recreate the condition.", q276c),
     ev("April 8, 2024", "OTHER", "On April 8, 2024, Tesla Engineering received and reviewed images associated with the first customer claim, which confirmed the presence of the condition."),
     ev("the week of April 8, 2024", "INVESTIGATION_START", "Through the week of April 8, 2024, Tesla Engineering continued additional tests relating to the scope and behavior of the condition."),
     ev("April 12, 2024", "DECISION", "On April 12, 2024, having completed its assessment of the condition, Tesla made a determination to voluntarily recall the affected vehicles.")]))

# 5
q294 = "Contamination may have been present on the glass surface during primer application at the roof supplier facility."
L.append(lab("RCLRPT-24V294-3024.txt",
    ("SUPPORTED", "Name : BOS AUTOMOTIVE PRODUCTS HUNGARY LP"),
    ("INSUFFICIENT", None, q294, "cause"),
    ("SUPPORTED", q294),
    ("NOT_REPORTED", [], "Chronology is provided as an attachment.", "chronology"),
    []))

# 6
L.append(lab("RCLRPT-24V318-2050.txt",
    ("NOT_REPORTED", "Name : NR"),
    ("NOT_REPORTED", None, "", None),
    ("SUPPORTED", "Improperly routed wiring under the driver or passenger seat during Winnebago upfit assembly process can be caught in the seat mechanism when adjusting the seat."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("March 12, 2024", "FILER_AWARENESS", "On or about March 12, 2024, Winnebago was notified of a NHTSA VOQ related to Airbag deployment."),
     ev("", "INVESTIGATION_START", "Winnebago wasn't able to confirm the VOQ complaint, however an investigation was initiated."),
     ev("", "FILER_AWARENESS", "During the course of the investigation, Winnebago identified 66 claims from 06/07/2018 – 01/11/2024 related to Supplemental Restraint Systems (SRS) alerts."),
     ev("", "OTHER", "Winnebago reviewed the claims and identified potential for under seat wiring to become damaged."),
     ev("", "DECISION", "A meeting of Winnebago’s Product Safety Committee was held and it was decided to issue a voluntary recall.")]))

# 7
L.append(lab("RCLRPT-24V352-8650.txt",
    ("SUPPORTED", "Name : Freedman Seating Company"),
    ("INSUFFICIENT", None, "Name : Freedman Seating Company", "block"),
    ("SUPPORTED", "Incorrect welding process and use of welding fixtures."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("May 13th, 2024", "SUPPLIER_NOTICE", "On May 13th, 2024 we were notified of recall 24E-026, in response we are submitting our own recall for the units produced potentially containing the affected equipment.")]))

# 8
q360 = "Freedman Seating Company initiated NHTSA recall # 24E026 May 2024"
L.append(lab("RCLRPT-24V360-5197.txt",
    ("SUPPORTED", "Name : Freedman Seating Company"),
    ("SUPPORTED", "Freedman Seating Company", q360, "chronology"),
    ("SUPPORTED", "Incorrect welding process and use of welding fixtures."),
    ("NAMED", ["Freedman Seating Company"], q360, "chronology"),
    [ev("May 2024", "OTHER", q360)]))

# 9
L.append(lab("RCLRPT-24V364-1692.txt",
    ("SUPPORTED", "Name : Continental Teves AG& Co. oHG"),
    ("INSUFFICIENT", None, "Name : Continental Teves AG& Co. oHG", "block"),
    ("NOT_REPORTED", "NR"),
    ("NOT_REPORTED", [], "See File \"Recall N901 Chronology\".", "chronology"),
    []))

# 10
L.append(lab("RCLRPT-24V369-1153.txt",
    ("SUPPORTED", "Name : Ashimori Korea., LTD"),
    ("INSUFFICIENT", None, "Name : Ashimori Korea., LTD", "block"),
    ("SUPPORTED", "Certain airbags were equipped with an inert airbag ignitor and not a production level airbag ignitor."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("April 19, 2024", "FILER_AWARENESS", "On April 19, 2024, a VinFast vehicle was brought to a dealer in Vietnam due to the airbag warning light remaining active."),
     ev("", "OTHER", "The dealer traced the concern to the front passenger side airbag."),
     ev("", "OTHER", "Further investigation determined the front passenger side airbag was equipped with an inert airbag ignitor."),
     ev("", "INVESTIGATION_START", "A formal investigation was immediately undertaken."),
     ev("May 22, 2024", "DECISION", "On May 22, 2024, following the conclusion of its investigation, VinFast determined the existence of an unreasonable risk to safety that could exist under a unique crash scenario and authorized a voluntarily safety recall.")]))

# 11
q438s = "Terex consulted with the level controller supplier to determine if all units in the time frame may have been affected."
q438z = "The affected unit list was finalized on 6/5/2024 and the decision to recall was made on 6/10/2024."
L.append(lab("RCLRPT-24V438-1492.txt",
    ("SUPPORTED", "Name : Hartfiel Automation"),
    ("INSUFFICIENT", None, q438s, "chronology"),
    ("SUPPORTED", "The software for the tilt controller on the affected machines may lose the ability to maintain level while squeezing the enable trigger if power to the controller is lost."),
    ("UNNAMED", [], q438s, "chronology"),
    [ev("10/30/2023", "FILER_AWARENESS", "On 10/30/2023, Terex received a report from the field of a platform that dumped."),
     ev("", "OTHER", "The investigation found that a cover was damaged due to contact with another object and severed the power wires to the leveling controller and the secondary system that limits platform tilting to 15 degrees."),
     ev("11/3/2023", "OTHER", "On 11/3/2023, testing of the system shows that if power is disconnected from the leveling controller while squeezing the unit control enable trigger, the platform may dump."),
     ev("11/14/2023", "OTHER", "On 11/14/2023, a software update is implemented for production that prevents the platform from dumping if power to the leveling controller is disconnected."),
     ev("11/16/2023", "FILER_AWARENESS", "On 11/16/2023, Terex received a report from a dealer of a platform that dumped during a function test, the investigation discovered the power wire to the leveling controller was disconnected."),
     ev("", "INVESTIGATION_START", q438s),
     ev("6/5/2024", "OTHER", q438z),
     ev("6/10/2024", "DECISION", q438z)]))

# 12
q446a = "In the course of 2022 MBAG received two individual and presumably unrelated field cases from outside the US."
L.append(lab("RCLRPT-24V446-1426.txt",
    ("SUPPORTED", "Name : MBAG"),
    ("SUPPORTED", "MBAG", q446a, "chronology"),
    ("SUPPORTED", "Due to a deviation in the vehicle production process, the bolted connection of a wiring harness to the pre-fuse box might not be tightened to the specified torque."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("2022", "FILER_AWARENESS", q446a),
     ev("February 2024", "FILER_AWARENESS", "In February 2024, Mercedes-Benz AG identified an additional case outside the US, which showed similarities with the above-mentioned deviation."),
     ev("", "OTHER", "A subsequent detailed examination of this case identified that the vehicle in question had been subject to corrective measures targeting this specific tightening connection during its assembly process."),
     ev("April 2024", "OTHER", "In April 2024, a comprehensive evaluation enabled the association of this corrective action with the two previously unattributable field incidents that also exhibited a torque deviation at the same tightening connection."),
     ev("", "OTHER", "The analyses showed that the vehicles had undergone rework on the screw connection of the pre- fuse box during production."),
     ev("May 2024", "OTHER", "Based on this determination, out of an abundance of caution, in May 2024, MBAG determined the potentially affected vehicles by reviewing the rework data from production."),
     ev("June 7, 2024", "DECISION", "On June 7, 2024, MBAG determined that a potential safety risk in the identified vehicle population cannot be ruled out and decided to conduct a recall.")]))

# 13
q448h = "But since HSM, the seats supplier, had conducted the same test with success, further investigation was required."
L.append(lab("RCLRPT-24V448-4950.txt",
    ("SUPPORTED", "Name : HSM Transportation Solutions"),
    ("SUPPORTED", "HSM", q448h, "chronology"),
    ("NOT_REPORTED", "NR"),
    ("NAMED", ["HSM"], q448h, "chronology"),
    [ev("October 2023", "OTHER", "During development of a floor reinforcement, testing was conducted in October 2023, to validate that tracked seats could withstand the strength required by Federal Motor Vehicle Safety Standards, Standard #210, “Seat belt assembly anchorages.”"),
     ev("", "OTHER", "The 2-place seats equipped with lap and shoulder seat belts failed the test."),
     ev("", "OTHER", "The leg, and more precisely, the way it is attached to the track, was identified as the source of the failure."),
     ev("", "INVESTIGATION_START", q448h),
     ev("", "INVESTIGATION_START", "The following months, further tests were conducted, both by HSM and Micro Bird, obtaining either non- conclusive or contradictory results."),
     ev("June 12, 2024", "DECISION", "In the end, it was determined that the original hardware may or may not be sufficient to ensure that 2-place seats equipped with lap and shoulder seat belts meet the requirements of Standards #210, and it was decided, on June 12, 2024, to recall the vehicles designed with those seats.")]))

# 14
L.append(lab("RCLRPT-24V476-9574.txt",
    ("NOT_REPORTED", "Name : NR"),
    ("NOT_REPORTED", None, "", None),
    ("SUPPORTED", "Identified wires (including the 6 gauge Travel Mode wire) were inadvertently specified for connection to the unprotected side of the mini-breaker block, eliminating the over-current protection provided by the mini-breaker for the subject circuits."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("5/3/24", "FILER_AWARENESS", "On 5/3/24, through standard Brinkley RV Safety/Quality escalation procedures, the Customer Care Center identified a Claim with multiple component failures."),
     ev("5/3/24", "INVESTIGATION_START", "An investigation was opened on 5/3/24."),
     ev("", "OTHER", "Initial investigations indicated potential concerns with over-current protection and refrigerator wiring size, although predicted failures were not replicated through extensive testing efforts."),
     ev("5/31/24", "OTHER", "Interim findings were reviewed with the Brinkley Safety Committee on 5/31/24."),
     ev("", "INVESTIGATION_START", "The Safety Committee directed the testing team to continue testing all reasonably replicated scenarios."),
     ev("6/19/24", "OTHER", "The testing team published a final report dated 6/19/24 indicating that despite lack of consistent failures in testing, the potential for safety-related failures still exists in the subject population,"),
     ev("6/25/24", "DECISION", "A formal recall is being initiated on 6/25/24.")]))

# 15
q477c = "Polestar has identified that during the backing event, the graphical memory allocation process within the infotainment head unit (IHU) may cause a limited visualization in the rear camera view."
L.append(lab("RCLRPT-24V477-8229.txt",
    ("SUPPORTED", "Name : Polestar AB"),
    ("SUPPORTED", "Polestar", q477c, "cause"),
    ("SUPPORTED", q477c),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("March 9, 2021", "FILER_AWARENESS", "On March 9, 2021, Polestar received the first customer complaint."),
     ev("May 14, 2024", "FILER_AWARENESS", "On May 14, 2024, Polestar received questions from NTHSA."),
     ev("May 15, 2024", "INVESTIGATION_START", "On May 15, 2024, Polestar performed a deep dive in customer inputs in US."),
     ev("June 20,2024", "DECISION", "On June 20,2024, Polestar decided the condition as critical concern."),
     ev("June 25, 2024", "DECISION", "On June 25, 2024, Polestar decided to conduct a voluntary safety recall."),
     ev("July 1, 2024", "OTHER", "On July 1, 2024, the updated software is available in VIDA."),
     ev("", "DECISION", "Please note that Polestar reviewed the field reports/complaints and determined that the rear camera system performance did not meet the requirements of FMVSS 111, specifically for the following:")]))

# 16
e480 = "April 2024: NHTSA inquiry regarding the rearview camera in 2023 model year Volkswagen Golf 8 vehicles."
L.append(lab("RCLRPT-24V480-8563.txt",
    ("SUPPORTED", "Name : LG Electronics (Poland)"),
    ("INSUFFICIENT", None, "Name : LG Electronics (Poland)", "block"),
    ("SUPPORTED", "Various software errors may lead to a delay or blackscreen of the rearview image or the system may not start up at all."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("August 2023", "FILER_AWARENESS", "August 2023: NHTSA inquiry regarding the rearview camera in 2022 model year Volkswagen Golf vehicles."),
     ev("September 2023", "INVESTIGATION_START", "September 2023: Analysis within VWGoA and VWAG."),
     ev("October 2023", "OTHER", "October 2023: Presentation of the analysis results of the rearview camera in 2022 model year Volkswagen Golf vehicles at the NHTSA quarterly meeting."),
     ev("CW49/2023", "FILER_AWARENESS", "CW49/2023: Priority Customer Complaint submitted for 2024 model year Volkswagen Atlas regarding various rearview image complaints."),
     ev("CW50/2023", "OTHER", "CW50/2023: Software 1969 for MB3 Optional Infotainment (OI) was developed for various robustness improvements to the system generally."),
     ev("CW05/24", "OTHER", "CW05/24: Publication of the TPI for SW1969 OI."),
     ev("April 2024", "FILER_AWARENESS", e480),
     ev("April 2024", "INVESTIGATION_START", "Analysis of rearview camera system of 2023 model year Volkswagen Golf 8 vehicles started.", e480),
     ev("June 2024", "OTHER", "June 2024: Analysis found no systematic issue in the rearview camera components."),
     ev("June 19, 2024", "DECISION", "June 19, 2024: The topic was discussed in the Volkswagen Product Safety Committee, and the Committee decided a non-compliance recall for the optional infotainment system")]))

# 17
L.append(lab("RCLRPT-24V485-4954.txt",
    ("SUPPORTED", "Name : BEITONG IMPORT & EXPORT CO LTD"),
    ("INSUFFICIENT", None, "Name : BEITONG IMPORT & EXPORT CO LTD", "block"),
    ("NOT_REPORTED", "NR"),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("February 2024", "FILER_AWARENESS", "In February 2024, during inspection of the rear emergency door, in three (3) occasions, the handle broke."),
     ev("", "OTHER", "The exact circumstances of this breakage could not be determined, but examination of the broken handles showed porosity in the metal."),
     ev("", "INVESTIGATION_START", "An investigation of the issue was launched."),
     ev("", "INVESTIGATION_START", "Many resistance tests were conducted on different lots of handles, including on handles installed on older vehicles."),
     ev("", "OTHER", "These tests determined that all tested handles resisted to a force of at least 178 N,"),
     ev("", "INVESTIGATION_START", "Micro bird having not received claims regarding broken rear emergency door exterior handles, some dealers were polled to evaluate the prevalence of broken handles in the field."),
     ev("", "OTHER", "It was identified that these handles had been purchased by owners, sometimes because they had broken."),
     ev("June 20, 2024", "DECISION", "In regards of these information, and because we cannot determine whether this situation was limited in time, on June 20, 2024, it was decided to recall all the vehicles equipped with the identified rear emergency door exterior handle.")]))

# 18
q486a = "On May 9, 2024, an issue pertaining to windshield adhesion on certain F-150 vehicles was brought to Ford’s Critical Concerns Review Group (CCRG) for review."
L.append(lab("RCLRPT-24V486-3579.txt",
    ("SUPPORTED", "Name : Ford Motor Company"),
    ("SUPPORTED", "Ford", q486a, "chronology"),
    ("SUPPORTED", "Improperly functioning windshield positioning equipment at the vehicle assembly plant caused variance in the location of the windshield during the urethane bead application."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("May 9, 2024", "INVESTIGATION_START", q486a),
     ev("May 2, 2024", "FILER_AWARENESS", "On May 2, 2024, personnel at Ford’s Kansas City Assembly Plant (KCAP) identified visible urethane sealer on the interior passenger side A-pillar that was off location relative to the windshield and flange."),
     ev("", "OTHER", "Upon further investigation, Ford discovered that variations in the manufacturing fixture process, used to position the windshield before applying the urethane, could lead to the possibility of insufficient adhesion between the windshield and the vehicle's structure."),
     ev("", "INVESTIGATION_START", "To verify the potential for improper windshield adhesion along the A-pillar, Ford conducted vehicle windshield glass cut-out inspections at Ford’s Kansas City Assembly Plant across the suspect vehicle build timeframe."),
     ev("", "INVESTIGATION_START", "Windshield air leakage testing and water leak audits were also performed on units within the suspect population."),
     ev("", "INVESTIGATION_START", "Photos from an overhead camera Artificial Intelligence (AI) pilot program were utilized to further identify windshields that were improperly positioned during the urethane application."),
     ev("", "DECISION", "Ford determined that suspect vehicles with this potential condition may not conform to Federal Motor Vehicle Safety Standard (FMVSS) No. 212 Windshield mounting."),
     ev("June 21, 2024", "DECISION", "On June 21, 2024, Ford’s Field Review Committee reviewed the concern and approved a field action.")]))

# 19
L.append(lab("RCLRPT-24V515-2399.txt",
    ("SUPPORTED", "Name : Autocar LLC"),
    ("SUPPORTED", "Autocar", "An Autocar manufacturing error.", "cause"),
    ("SUPPORTED", "An Autocar manufacturing error."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("March 14, 2024", "FILER_AWARENESS", "March 14, 2024, Autocar personnel identified a single unit missing the retaining rings from the cab tilt pins."),
     ev("March 19-21", "OTHER", "March 19-21, all in-house units were quarantined and inspected, and a clean point established for production."),
     ev("March 21-June 21, 2024", "INVESTIGATION_START", "March 21-June 21, 2024, Autocar personnel inspected multiple units in the field and deployed additional inspection and installation practices."),
     ev("June 27, 2024", "DECISION", "June 27, 2024, all relevant information was presented to Autocar's management team and out of an abundance of caution, Autocar decided to perform a voluntary Safety Recall.")]))

# 20
L.append(lab("RCLRPT-24V526-6201.txt",
    ("SUPPORTED", "Name : Terex South Dakota, Inc"),
    ("INSUFFICIENT", None, "Name : Terex South Dakota, Inc", "block"),
    ("SUPPORTED", "The retaining balls on the original basket retaining pins may not be able to withstand the force applied to them when installed in the replacement basket bracket, which may cause the pins to disengage."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("March 19, 2024", "FILER_AWARENESS", "On March 19, 2024 there was a report of an operator falling to the ground from an unknown height when the basket tilted."),
     ev("", "INVESTIGATION_START", "The investigation into the root cause began at that time."),
     ev("June 3, 2024", "OTHER", "On June 3, 2024 it was determined that both of the original basket retaining pins would need to fully disengage from the replacement basket bracket for the basket to tilt."),
     ev("", "OTHER", "It was determined that the retaining balls on the original basket retaining pins may not be able to withstand the force applied to them when installed in the replacement basket bracket."),
     ev("June 10, 2024", "OTHER", "On June 10, 2024 the replacement parts system was changed so that basket bracket 626478 no longer replaces the original bracket."),
     ev("July 8, 2024", "OTHER", "On July 8, 2024 the list of replacement basket brackets sold was determined."),
     ev("July 10, 2024", "DECISION", "On July 10, 2024 the decision to recall was made.")]))

# 21
q556a = "07/08/2024 – Meritor communicates to Navistar findings that certain Meritor steer axle assemblies built with USK International’s tie rod ball studs were manufactured with less than the required hardness."
e556 = "8/23/2024 – Axle supplier who was performing inspections and repairs to suspect units notifies Navistar that they cannot locate 40 vehicles."
L.append(lab("RCLRPT-24V556-5723.txt",
    ("SUPPORTED", "Name : Cummins Drivetrain and Braking Systems"),
    ("SUPPORTED", "Meritor", q556a, "chronology"),
    ("SUPPORTED", "USK International introduced experimental ball studs from an unapproved heat treat process into production assemblies"),
    ("NAMED", ["Meritor", "USK International"], q556a, "chronology"),
    [ev("07/08/2024", "SUPPLIER_NOTICE", q556a),
     ev("7/08/2024 thru 7/17/2024", "OTHER", "7/08/2024 thru 7/17/2024: Navistar initiates ship hold of steer axles and vehicles at the assembly plants, finding 400 suspect date code tie rod assemblies out of 3,019 possible vehicles, and established the clean point at Escobedo and San Antonio assembly plants."),
     ev("07/17/2024", "OTHER", "07/17/2024 – Navistar finalizes the suspect population."),
     ev("07/18/2024", "DECISION", "07/18/2024 – Navistar declares a Safety Recall."),
     ev("09/03/2024", "OTHER", "09/03/2024- Revised recall schedule due to holiday."),
     ev("09/12/2024", "NHTSA_FILING", "09/12/2024- Revised defect report with new population."),
     ev("8/23/2024", "SUPPLIER_NOTICE", e556),
     ev("8/23/2024", "INVESTIGATION_START", "Navistar Supplier Quality reviews the records of the 40 units and determines that they were not placed on hold.", e556),
     ev("8/28/2024", "OTHER", "8/28/2024 – Navistar confirmed additional suspect population."),
     ev("9/5/2024", "DECISION", "9/5/2024 – Navistar approved to extend the population for 24511.")]))

# 22
L.append(lab("RCLRPT-24V587-7214.txt",
    ("SUPPORTED", "Name : Yazaki Corporation"),
    ("INSUFFICIENT", None, "Name : Yazaki Corporation", "block"),
    ("NOT_REPORTED", "NR"),
    ("NOT_REPORTED", [], "Please see the attached Part 573 Defect Information Report.", "chronology"),
    []))

# 23
L.append(lab("RCLRPT-24V588-9241.txt",
    ("SUPPORTED", "Name : Benteler Automobiletechnik GmbH"),
    ("INSUFFICIENT", None, "Name : Benteler Automobiletechnik GmbH", "block"),
    ("NOT_REPORTED", "NR"),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("March 2023", "FILER_AWARENESS", "In March 2023, subsequent to the implementation of 22V-614, warranty claims were being processed, and it was noticed that some warranty claim records did not include certain details which would indicate that an appropriate EGR replacement part had been used as the remedy part"),
     ev("Between April and September", "INVESTIGATION_START", "Between April and September, as additional warranty claims were processed, field monitoring and analyses were performed in an attempt to identify vehicles that may have received an inappropriate EGR replacement part."),
     ev("", "OTHER", "However, the results were inconclusive."),
     ev("October", "OTHER", "In October, it was found that at the start of the 2022 campaign, an inspection of the replacement parts inventory may not have been performed."),
     ev("Between November 2023 and June 2024", "INVESTIGATION_START", "Between November 2023 and June 2024, further reviews were conducted in an attempt to identify potentially affected vehicles with possible suspect replacement parts."),
     ev("late July", "OTHER", "In late July, the analysis concluded that a small number of vehicles may have received a suspect replacement part during a 22V-614 dealer service visit."),
     ev("August 1, 2024", "DECISION", "On August 1, 2024, in an abundance of caution, BMW decided to conduct a voluntary safety recall.")]))

# 24
q607a = "6/18/2024 REV RV received information regarding a 2024 Model Year Admiral motor home, serial number 655NR4440572 that the front overhead cabinet under the HappiJac drop down bed started to detach from the mounting surface."
e607b = "6/24 Unit arrived for inspection."
e607c = "6/26 REV RV service communicated with engineering to advise of the situation."
e607d = "7/08 Manufacturing and Engineering returned from shutdown."
q607s = "Manufacturing Operations were shut down the weeks of June 24 & July 4th (holiday week)."
L.append(lab("RCLRPT-24V607-1671.txt",
    ("SUPPORTED", "Name : REV Recreation Group (RRG)"),
    ("SUPPORTED", "REV RV", q607a, "chronology"),
    ("SUPPORTED", "The cabinets may have been installed with fewer fasteners (screws and staples) than was specified causing a lack of support."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("6/18/2024", "FILER_AWARENESS", q607a),
     ev("6/19", "OTHER", "6/19 The unit overhead was secured, and the unit was driven to REV RV in Decatur Indiana for evaluation."),
     ev("6/20", "OTHER", "6/20 The manufacturing plant was notified of the issue with the front overhead cabinet coming loose."),
     ev("6/24", "OTHER", e607b),
     ev("6/24", "OTHER", "A ship hold was placed on similar units until testing was performed.", e607b),
     ev("June 24", "OTHER", q607s),
     ev("July 4th", "OTHER", q607s),
     ev("6/26", "OTHER", e607c),
     ev("6/26", "INVESTIGATION_START", "Investigation began to review field data.", e607c),
     ev("7/02", "INVESTIGATION_START", "7/02 Manufacturing leaders inspected the unit and reviewed the prints."),
     ev("7/08", "OTHER", e607d),
     ev("7/08", "OTHER", "Units on stop ship were inspected.", e607d),
     ev("7/08", "INVESTIGATION_START", "Claim data analyzed.", e607d),
     ev("7/11", "INVESTIGATION_START", "7/11 Stress testing was performed on an overhead cabinet from manufacturing."),
     ev("7/12", "OTHER", "7/12 Plant inspection and repairs were performed."),
     ev("7/18", "OTHER", "7/18 Data reviewed with the Operations, Engineering and Quality."),
     ev("7/22", "OTHER", "7/22 Summary forwarded to safety committee.."),
     ev("7/25", "OTHER", "7/25 Safety committee met to discuss engineering investigation results and sent recommendation to declare a voluntary safety recall to REV Senior Leadership Team for consideration and review."),
     ev("08/09", "DECISION", "08/09 DIR Approval to proceed with Part 573 Safety Recall Report.")]))

# 25
L.append(lab("RCLRPT-24V631-8870.txt",
    ("NOT_REPORTED", "Name : NR"),
    ("NOT_REPORTED", None, "", None),
    ("INSUFFICIENT", "S5.5.3(b): Emergency Exit Identification: Concise operating instructions describing the motions necessary to unlatch and open the emergency exit shall be located within 15 centimeters of the release mechanism on the inside surface of the bus."),
    ("NONE_MENTIONED", [], "", "chronology"),
    [ev("5/20/24", "OTHER", "On a lab test performed on 5/20/24 it was determined and reported by NHTSA that the subject Titan SRW School Bus model year 2020 did not comply with the FMVSS 217 regulation regarding proper bus emergency exit window labeling instructions."),
     ev("6/11/24", "FILER_AWARENESS", "Reporting took place from NHTSA to Endera Motors on 6/11/24."),
     ev("7/19/24", "DECISION", "Investigation of the reported failure was conducted by Endera Motors internally and confirmed via email on 7/19/24 that this issue would be recalled in order to properly be addressed."),
     ev("8/22/24", "NHTSA_FILING", "On 8/22/24 the recall was submitted via the NHTSA portal.")]))

# ---------- build + verify ----------
out, errs = [], []
VT = {"FILER_AWARENESS", "SUPPLIER_NOTICE", "INVESTIGATION_START", "DECISION", "NHTSA_FILING", "OTHER"}


def chk(fn, secs, q, sec, what):
    if q == "":
        return
    if len(q) > 300:
        errs.append(f"{fn} {what}: quote too long ({len(q)})")
    if norm(q) not in secs[sec]:
        errs.append(f"{fn} {what}: quote not found in {sec}: {q[:80]}")


for l in L:
    fn = l["fn"]
    fileline, secs = sections(fn)
    s1st, s1q = l["s1"]
    s1 = {"id": "S1", "status": s1st, "quote": s1q, "section": "block"}
    chk(fn, secs, s1q, "block", "S1")
    s2st, s2name, s2q, s2sec = l["s2"]
    s2 = {"id": "S2", "status": s2st}
    if s2name:
        s2["name"] = s2name
    s2["quote"] = s2q
    s2["section"] = s2sec if s2sec else ""
    if s2q:
        chk(fn, secs, s2q, s2sec, "S2")
    cst, cq = l["cause"]
    cause = {"status": cst, "quote": cq, "section": "cause"}
    chk(fn, secs, cq, "cause", "cause")
    uk, un, uq, usec = l["up"]
    up = {"kind": uk, "names": un, "quote": uq, "section": usec}
    if uq:
        chk(fn, secs, uq, usec, "upstream")
    for n in un:
        if n not in secs["cause"] + " " + secs["chronology"]:
            errs.append(f"{fn} upstream name not in narrative: {n}")
    for i, e in enumerate(l["events"]):
        chk(fn, secs, e["quote"], "chronology", f"event{i}")
        if e["type"] not in VT:
            errs.append(f"{fn} event{i} bad type")
        if e["date_text"] and not e.get("inherited_date") and e["date_text"] not in norm(e["quote"]):
            errs.append(f"{fn} event{i} date_text not in quote")
        if e.get("inherited_date"):
            chk(fn, secs, e["entry_quote"], "chronology", f"event{i} entry")
            if e["date_text"] not in e["entry_quote"]:
                errs.append(f"{fn} event{i} date not in entry_quote")
        e["quote"] = norm(e["quote"])
    out.append({"file": fileline, "claims": [s1, s2], "cause": cause, "upstream": up, "events": l["events"]})

if errs:
    print("\n".join(errs))
    sys.exit(1)
with open(os.path.join(D, "passB.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("ok", len(out), sum(len(o["events"]) for o in out))
