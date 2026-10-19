import json, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def sections(path):
    txt = open(path, encoding="utf-8").read()
    fname = re.search(r"^FILE:\s*(\S+)", txt, re.M).group(1)
    b = txt.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    c = txt.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    ch = txt.split("=== CHRONOLOGY ===")[1]
    return fname, {"block": norm(b), "cause": norm(c), "chronology": norm(ch)}

def E(date, typ, quote, entry=None):
    return {"date_text": date, "type": typ, "quote": quote, "entry": entry}

def C(status, quote="", section="", name=None):
    return {"status": status, "quote": quote, "section": section, "name": name}

def U(kind, quote="", section="", names=None):
    return {"kind": kind, "names": names or [], "quote": quote, "section": section}

L = {}

# ---------- 26E009
q_s = "An inquiry to the supplier Samsung SDI Co. Ltd. revealed that affected cells have also been delivered to Webasto Roof & Components SE."
e1 = "March 2025 As part of its market observation obligations, the Webasto organization noticed that there had been recalls by automotive manufacturers who use the same cells in the HV batteries installed in their vehicles as those used in Webasto’s CV Standard 12V & 24V batteries."
e4 = "From March 2025 to December 2025 Multiple alignment meetings with Samsung SDI Co., Ltd. to determine potential risks."
L["RCLRPT-26E009-2878.txt"] = dict(
    S1=C("SUPPORTED", "Name: Samsung SDI Co., Ltd.", "block"),
    S2=C("SUPPORTED", q_s, "chronology", "Samsung SDI Co., Ltd."),
    cause=C("INSUFFICIENT", "Samsung SDI Co., Ltd. recall (Reference no.: Part 573 Safety Recall Report 25E-007) states that the root cause is still under investigation.", "cause"),
    up=U("NAMED", q_s, "chronology", ["Samsung SDI Co., Ltd."]),
    ev=[
        E("March 2025", "FILER_AWARENESS", e1),
        E("March 2025", "SUPPLIER_NOTICE", q_s, e1),
        E("March 2025", "OTHER", "March 2025 First meeting with Samsung SDI Co., Ltd. to analyze the suspect cells and develop corrective measures."),
        E("March 2025 to December 2025", "OTHER", e4),
        E("March 2025 to December 2025", "INVESTIGATION_START", "Internal analyses were conducted.", e4),
        E("January 2026", "OTHER", "January 2026 Market analysis revealed that packs in the US market could also be affected."),
        E("Feb 27, 2026", "DECISION", "Feb 27, 2026 A final meeting to assess product safety relevance and U.S. market exposure was performed and concluded with the decision to notify NHTSA."),
    ])

# ---------- 26E010
q1 = "January 13, 2026: Seojin sends Vision Wheel an 8D report identifying an internal inventory of approximately 4,000 pieces manufactured for Vision Wheel’s Discount Tire program, and notes manufacturing irregularities."
q3 = "January 13, 2026, through February 27, 2026: Vision Wheel conducts a further investigation regarding wheels manufactured before January 13, 2026."
L["RCLRPT-26E010-2338.txt"] = dict(
    S1=C("SUPPORTED", "Name: Seojin Vietnam Co., Ltd.", "block"),
    S2=C("SUPPORTED", q1, "chronology", "Seojin"),
    cause=C("SUPPORTED", "The defect was caused by a manufacturing process deviation at Seojin in which wheels were subjected to excessive paint-oven temperatures during the curing process.", "cause"),
    up=U("NAMED", q1, "chronology", ["Seojin"]),
    ev=[
        E("January 13, 2026", "SUPPLIER_NOTICE", q1),
        E("January 13, 2026", "OTHER", "The report also states that a corrective action had been implemented as of the date of the report by reducing paint-oven temperatures to specification for the Vision Wheel program.", q1),
        E("January 13, 2026", "OTHER", "Subsequent validation testing shows post-paint hardness readings averaging approximately 90-95 HB and no impact-test cracking in these post-correction wheels.", q1),
        E("January 13, 2026, through February 27, 2026", "INVESTIGATION_START", q3),
        E("February 10, 2026", "OTHER", "On February 10, 2026, sales of the affected wheels were halted."),
        E("January 13, 2026, through February 27, 2026", "OTHER", "Vision Wheel also returns 14,003 affected wheels identified as defective to Seojin for destruction or controlled rework.", q3),
        E("March 5, 2026", "DECISION", "March 5, 2026: After reviewing the full set of supplier data, internal testing, and the results of the February validation and sorting activity, Vision Wheel’s executive team, in consultation with outside counsel and its regulatory team, determined that a safety-related defect exists"),
    ])

# ---------- 26E011
L["RCLRPT-26E011-5568.txt"] = dict(
    S1=C("NOT_REPORTED"), S2=C("NOT_REPORTED"),
    cause=C("SUPPORTED", "The cause is a defect in the controller software logic.", "cause"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("February 10, 2026", "FILER_AWARENESS", "February 10, 2026: A vehicle collision occurred in a customer's bus yard and was reported to Cummins Service Engineering."),
        E("February 11, 2026", "OTHER", "February 11, 2026: The Accelera by Cummins Product Safety Leader was notified of the incident."),
        E("February 13, 2026", "INVESTIGATION_START", "February 13, 2026: A review of datalogger data retrieved from the vehicle involved in the incident was reviewed with the software architect."),
        E("February 20, 2026", "OTHER", "February 20, 2026: The Accelera by Cummins engineering team was able to replicate the software behavior on a test vehicle."),
        E("February 20, 2026", "INVESTIGATION_START", "February 20, 2026: A Product Safety Hazard Analysis was initiated to evaluate this software behavior."),
        E("February 27, 2026", "OTHER", "February 27, 2026: The Product Safety Hazard Analysis was completed."),
        E("March 9, 2026", "DECISION", "March 9, 2026: The software behavior issue was reviewed by the Cummins Product Safety Defect Board and was determined to constitute a safety defect."),
    ])

# ---------- 26E013
a = "3/6/2026 – Investigation opened."
b = "3/11/2026 –PAC reviewed the information and concluded that the data reviewed indicated a unanimous vote for a voluntary recall."
L["RCLRPT-26E013-6412.txt"] = dict(
    S1=C("NOT_REPORTED"), S2=C("NOT_REPORTED"),
    cause=C("SUPPORTED", "The incorrect seal was installed.", "cause"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("3/6/2026", "FILER_AWARENESS", "3/6/2026 – Report was made of axles built with incorrect seals."),
        E("3/6/2026", "INVESTIGATION_START", a),
        E("3/6/2026", "OTHER", "Axles bill of materials reviewed and orders put on hold with affected seals.", a),
        E("3/11/2026", "DECISION", b),
        E("3/11/2026", "INVESTIGATION_START", "Investigation called for determining affected component range.", b),
        E("3/18/2026", "OTHER", "3/18/2026 – Investigation concluded and scope completed."),
    ])

# ---------- 26E020
s1 = "September 15 2025 - following a report of two failures of installed screens in vehicles in the field, a Weldon technician inspected the units and found installation issues (e.g. cracking around the mounting screws of the unit) which were believed to have caused the issue."
m5 = "March 5 2026 - Weldon scheduled a service call to same customer to check that screens were operating properly which the customer confirmed."
enc = "Weldon contacted the supplier of the device (Enovation Controls- ENC) for technical support and began to investigate further, including development of a test fixture."
L["RCLRPT-26E020-6137.txt"] = dict(
    S1=C("SUPPORTED", "Name: Enovation Controls", "block"),
    S2=C("SUPPORTED", enc, "chronology", "Enovation Controls"),
    cause=C("INSUFFICIENT", "Root cause is being researched.", "cause"),
    up=U("NAMED", enc, "chronology", ["Enovation Controls"]),
    ev=[
        E("September 15 2025", "FILER_AWARENESS", s1),
        E("September 15 2025", "OTHER", "The screens were returned to Weldon for futher assessment but no faults were found.", s1),
        E("March 5 2026", "OTHER", m5),
        E("March 13 2026", "FILER_AWARENESS", "Shortly thereafter, on March 13 2026, the same customer reported a screen failure on same vehicle where the installation issues were previously resolved."),
        E("March 5 2026", "OTHER", "A new screen out of the box indicated the same issue as the unit installed in the vehicle.", m5),
        E("March 5 2026", "INVESTIGATION_START", enc, m5),
        E("March 5 2026", "OTHER", "Testing data and additional failed units were provided to the supplier.", m5),
        E("March 17, 2026", "SUPPLIER_NOTICE", "By March 17, 2026, the supplier was able to recreate the failure."),
        E("March 5 2026", "OTHER", "It was also determined by that end of line testing at Enovation controls would not reliably indicate the presence of the issue.", m5),
        E("April 3 2026", "SUPPLIER_NOTICE", "April 3 2026 - the supplier advised Weldon that even though the root cause analysis is ongoing, given the potential safety implications it is recommended that Weldon report a safety defect."),
        E("April 8 2026", "DECISION", "April 8 2026 - upon further review of information and given the supplier's statement Weldon determined that a safety related defect exists and will conduct a recall to address units in the field."),
    ])

# ---------- 26E022
d17 = "02/17/26 Q’Straint detected a defect during random inspection of QRT-3 Retractor."
d413 = "04/13/26 Completed Testing."
L["RCLRPT-26E022-4329.txt"] = dict(
    S1=C("SUPPORTED", "Name: Red Wood Enterprise CO, LTD", "block"),
    S2=C("INSUFFICIENT", "Notified OEM supplier.", "chronology"),
    cause=C("SUPPORTED", "Sticking of the auto release function due to interference between internal components.", "cause"),
    up=U("UNNAMED", "Notified OEM supplier.", "chronology"),
    ev=[
        E("02/17/26", "FILER_AWARENESS", d17),
        E("02/17/26", "OTHER", "Discontinued production and shipments.", d17),
        E("02/17/26", "OTHER", "Notified OEM supplier.", d17),
        E("02/24/26", "INVESTIGATION_START", "02/24/26 OEM supplier Initiated evaluation to determine root cause, review of production records, product builds, and shipments."),
        E("03/11/26", "SUPPLIER_NOTICE", "03/11/26 OEM supplier confirmed defect and initiated testing to validate root cause."),
        E("03/17/26", "OTHER", "03/17/26 Dispatched company representative to visit manufacturing supplier"),
        E("04/10/26", "OTHER", "04/10/26 Identified root cause and finalized assembly and shipment records of suspected product."),
        E("04/13/26", "OTHER", d413),
        E("04/13/26", "DECISION", "Decided a Safety-Related Defect.", d413),
    ])

# ---------- 26E025
gs = "Chemical analysis of the tested samples completed by GM’s supplier confirmed that the visible sediment is a precipitate from two additives in the brake fluid, and is not external contamination."
aug = "On August 7, 2025, NHTSA notified GM that certain samples of AC Delco GMW DOT 3 brake and clutch fluid produced in 2022 failed FMVSS 116 compliance testing conducted by a third-party test lab in June 2024."
resp = "GM responded to NHTSA’s August 7, 2025 information requests on September 3, 2025 and November 3, 2025 (together, the “Responses”), and GM incorporates the Responses by reference."
L["RCLRPT-26E025-2942.txt"] = dict(
    S1=C("SUPPORTED", "Name: Dupont Specialty Products", "block"),
    S2=C("INSUFFICIENT", gs, "chronology"),
    cause=C("INSUFFICIENT", "The cause of the observed precipitates in the tested sample is unknown.", "cause"),
    up=U("UNNAMED", gs, "chronology"),
    ev=[
        E("August 7, 2025", "FILER_AWARENESS", aug),
        E("June 2024", "OTHER", aug),
        E("", "INVESTIGATION_START", "GM opened a product investigation on the same day."),
        E("September 3, 2025", "OTHER", resp),
        E("November 3, 2025", "OTHER", resp),
        E("March 10, 2026", "OTHER", "On March 10, 2026, NHTSA conducted supplemental compliance testing on the remaining unopened sample from the subject brake fluid lot."),
        E("March 24, 2026", "FILER_AWARENESS", "On March 24, 2026, NHTSA supplied GM with the final test reports from this supplemental testing, which indicated that the subject brake fluid failed S5.1.7 due to the presence of visible sediment."),
        E("", "SUPPLIER_NOTICE", gs),
        E("April 16, 2026", "DECISION", "On April 16, 2026, GM’s Safety Field Action Decision Authority (SFADA) decided to conduct a noncompliance recall on the 2022 production lot of the brake-fluid sample that failed NHTSA’s supplemental compliance testing."),
    ])

# ---------- 26E026
L["RCLRPT-26E026-6527.txt"] = dict(
    S1=C("NOT_REPORTED"), S2=C("NOT_REPORTED"),
    cause=C("NOT_REPORTED"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("4/20/2026", "FILER_AWARENESS", "On 4/20/2026 an unoccupied Waymo AV encountered an untraversable flooded section of a roadway that has a 40 mph speed limit."),
        E("", "OTHER", "The Waymo AV detected potentially untraversable flood water and proceeded at reduced speed."),
        E("4/20/2026", "OTHER", "On 4/20/2026, following the event described above, Waymo implemented additional operational restrictions at times and in locations where there is an elevated risk of encountering a flooded, higher-speed roadway."),
        E("4/24/2026", "DECISION", "On 4/24/2026 Waymo’s Safety Board reviewed information about this issue and decided to conduct a recall."),
    ])

# ---------- 26E032
L["RCLRPT-26E032-5214.txt"] = dict(
    S1=C("NOT_REPORTED"), S2=C("NOT_REPORTED"),
    cause=C("SUPPORTED", "The bolt heads may have been over-torqued.", "cause"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("April 15, 2026", "INVESTIGATION_START", "April 15, 2026: Opened internal review of any similar reports."),
        E("Apr 23, 2026", "OTHER", "Apr 23, 2026: Containment cutoff implemented in production."),
        E("May 7, 2026", "OTHER", "May 7, 2026: TSB released to replace all bolts on affected units"),
        E("May 15, 2026", "FILER_AWARENESS", "May 15, 2026: Keystone notifies Lippert of their decision to release as a recall."),
        E("May 18, 2026", "DECISION", "May 18, 2026: Lippert escalates to recall."),
    ])

# ---------- 26E033
m10 = "March 10, 2026: Potential issue initially identified through theoretical FEA stress analysis."
L["RCLRPT-26E033-7019.txt"] = dict(
    S1=C("SUPPORTED", "Name: Cummins Clean Fuel Technologies", "block"),
    S2=C("INSUFFICIENT", "Name: Cummins Clean Fuel Technologies", "block"),
    cause=C("SUPPORTED", "A design change introduced a localized stress concentration that was not identified during the initial analysis.", "cause"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("March 10, 2026", "FILER_AWARENESS", m10),
        E("March 10, 2026", "OTHER", "A stop-ship / stop-build was implemented for production units to prevent further release as the issue was investigated.", m10),
        E("March 19, 2026", "OTHER", "March 19, 2026: New bracket (ME04-3717) was introduced into design and production"),
        E("March - June 2026", "INVESTIGATION_START", "March - June 2026: Cross-functional team conducted an extended review, including root cause analysis, to confirm the FEA stress analysis and to evaluate potential safety implications."),
        E("June 2, 2026", "DECISION", "June 2, 2026: Determination to conduct a safety recall out of an abundance of caution."),
    ])

# ---------- 26E046
L["RCLRPT-26E046-1566.txt"] = dict(
    S1=C("SUPPORTED", "Name: Horizon Global, Inc.", "block"),
    S2=C("INSUFFICIENT", "Name: Horizon Global, Inc.", "block"),
    cause=C("SUPPORTED", "A software vulnerability within the ITRM allows for a potential race condition to occur between the ITRM and the CAN Standby Control bit (STBCC) during initial power-up.", "cause"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("May 20, 2026", "FILER_AWARENESS", "On May 20, 2026, Ford's Recall Service Program (RSP) team introduced a concern to Ford's Critical Concern Review Group (CCRG) after an RSP Analyst identified a vehicle that had Field Service Action (FSA) 26C10 marked as complete"),
        E("", "OTHER", "Subsequent investigation determined that although the vehicle had successfully received the FSA 26C10 software update, the commercially available Ford ITRM accessory kit contains ITRM modules with obsoleted pre-FSA 26C10 software."),
        E("May 20, 2026", "OTHER", "On May 20, 2026, Ford initiated containment actions to prevent further distribution of affected inventory for all Ford ITRM accessory kits containing the software level recalled under 26C10."),
        E("May 20, 2026, and June 25, 2026", "INVESTIGATION_START", "Between May 20, 2026, and June 25, 2026, Ford's cross-functional team investigated the affected population."),
        E("June 25, 2026", "OTHER", "On June 25, 2026, Ford's Critical Concern Review Group (CCRG) completed its investigation, which considered Ford’s 26C10 recall and Federal Motor Vehicle Safety Standard (FMVSS) No. 108, Section 6.2.1."),
        E("", "OTHER", "Based on this review, and because the ITRM accessory kits contain the same software previously recalled under 26C10, CCRG recommended an equipment recall for the ITRM accessory kits sold containing the software level identified under 26C10."),
        E("July 7, 2026", "DECISION", "On July 7, 2026, Ford’s Field Review Committee reviewed the concern and approved a field action."),
    ])

# ---------- 26E056
wq = "Webasto identified that automotive OEMs using Samsung SDI cells had initiated recalls; inquiry to Samsung SDI confirmed affected cells were delivered to Webasto."
L["RCLRPT-26E056-7471.txt"] = dict(
    S1=C("SUPPORTED", "Name: Webasto Thermo & Comfort NA, INC", "block"),
    S2=C("SUPPORTED", wq, "chronology", "Webasto"),
    cause=C("NOT_REPORTED"),
    up=U("NAMED", wq, "chronology", ["Webasto", "Samsung SDI"]),
    ev=[
        E("March 2025", "OTHER", "March 2025 " + wq),
        E("Mar-Dec 2025", "OTHER", "Mar-Dec 2025 Webasto and Samsung SDI conducted multiple alignment meetings and internal analyses; no field defects observed in Webasto batteries."),
        E("January 2026", "OTHER", "January 2026 Webasto determined that packs in the U.S. market may be affected."),
        E("Feb 27, 2026", "OTHER", "Feb 27, 2026 Webasto concluded decision to notify NHTSA following final product-safety assessment meeting."),
        E("March 5, 2026", "OTHER", "March 5, 2026 Webasto filed Part 573 Safety Recall Report (NHTSA Recall No. 26E009)."),
        E("Mar 13-20, 2026", "SUPPLIER_NOTICE", "Mar 13-20, 2026 Webasto began notifying purchasers, including Odyne, by email and certified mail."),
        E("May 6, 2026", "FILER_AWARENESS", "May 6, 2026 NHTSA contacted Odyne requesting submission of a Part 573 defect information report."),
        E("May 11, 2026", "OTHER", "May 11, 2026 Odyne responded to NHTSA, requesting clarification of filing obligations applicable to a downstream purchaser."),
        E("May 14, 2026", "OTHER", "May 14, 2026 NHTSA confirmed Odyne's independent filing obligation under 49 CFR § 573.3(f)."),
        E("May 22, 2026", "INVESTIGATION_START", "May 22, 2026 Odyne initiated internal audit and engaged legal counsel; began preparing this report."),
        E("May 27, 2026", "OTHER", "May 27, 2026 Odyne completed internal audit and confirmed total affected vehicle population and owner information."),
    ])

# ---------- 26E059
rv = "From June 26 through early August 2026, Avride conducted a thorough review of the incidents and behaviors detailed in NHTSA’s June 26 IR, and submitted a response and supporting information to NHTSA on August 7, 2026."
L["RCLRPT-26E059-0404.txt"] = dict(
    S1=C("NOT_REPORTED"), S2=C("NOT_REPORTED"),
    cause=C("SUPPORTED", "The condition stems from scenario-dependent constraints in which the ADS may execute inaccurate lateral maneuvers with high confidence, potentially failing to prevent a collision.", "cause"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("May 6, 2026", "FILER_AWARENESS", "On May 6, 2026, NHTSA opened a Preliminary Evaluation (PE26003) into Avride’s automated driving system (ADS), citing 21 incidents reported between December 2025 and April 2026 by Avride under Standing General Order 2021-01."),
        E("June 26, 2026", "FILER_AWARENESS", "On June 26, 2026, NHTSA issued Information Request (IR) PE26003-01, seeking further information on the 21 incidents and any others related to a set of “subject behaviors,”"),
        E("June 26 through early August 2026", "INVESTIGATION_START", rv),
        E("August 7, 2026", "OTHER", rv),
        E("August 13, 2026", "OTHER", "On August 13, 2026, upon completion of their review, the Avride Safety Team identified the lateral- maneuver condition, along with a set of previously-completed software updates that it was determined addressed the condition."),
        E("", "OTHER", "The Avride Safety Team then formally escalated the matter to Avride’s Safety Board for their consideration."),
        E("August 13, 2026", "DECISION", "On August 13, 2026, Avride’s Safety Board determined that, based on the Avride Safety Team’s review of the lateral-maneuver condition and the risks posed by the condition prior to its mitigation, that the circumstances that existed prior to the software updates warranted submitting this report"),
    ])

# ---------- 26E066
ev66 = "6/1/2026 – 9/4/2026 Following a redesign of the fuel hose that was implemented into production in April 2026, Cummins conducted an evaluation of the previous fuel hose designs that were used as remedy parts in Recall No. 23E055, 24E038, and 25E004 to assess in-service performance of those designs."
L["RCLRPT-26E066-0581.txt"] = dict(
    S1=C("SUPPORTED", "Name: HydraPower Dynamics Limited", "block"),
    S2=C("INSUFFICIENT", "Name: HydraPower Dynamics Limited", "block"),
    cause=C("SUPPORTED", "The subject hoses may have insufficient crimping of the connector, possibly resulting in insufficient hose retention.", "cause"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("6/1/2026 – 9/4/2026", "INVESTIGATION_START", ev66),
        E("April 2026", "OTHER", ev66),
        E("9/22/2026", "DECISION", "9/22/2026 – Based upon the results of this evaluation, Cummins decided to replace the fuel hoses on the subject population with the redesigned parts (which were used in current production beginning in April 2026)."),
    ])

# ---------- 26V119
sup = "Ford and the supplier conducted testing on the welders used to produce the subject driveshafts on December 22, 2025."
L["RCLRPT-26V119-2340.txt"] = dict(
    S1=C("SUPPORTED", "Name: Dana Incorporated", "block"),
    S2=C("INSUFFICIENT", sup, "chronology"),
    cause=C("SUPPORTED", "Due to degradation, the spindle at the friction weld station did not reach sufficient speed to provide acceptable weld energy.", "cause"),
    up=U("UNNAMED", sup, "chronology"),
    ev=[
        E("December 22, 2025", "FILER_AWARENESS", "On December 22, 2025, the Kentucky Truck Plant (KTP) Plant Vehicle Team reported that three 2025 model year Super Duty vehicles experienced separation of the aluminum driveshaft during End-of-Line testing."),
        E("", "OTHER", "KTP issued a stop ship for this concern on the same day."),
        E("December 22, 2025", "INVESTIGATION_START", sup),
        E("", "OTHER", "Testing confirmed that the issue was isolated to driveshafts produced on only one of the two welders, due to degradation of that welder’s spindle."),
        E("January 8, 2026", "INVESTIGATION_START", "On January 8, 2026, this issue was brought to Ford’s Critical Concern Review Group (CCRG) for review."),
        E("", "INVESTIGATION_START", "During the CCRG’s investigation, Ford and the supplier reviewed supplier production history and analyzed weld quality data to determine the population of driveshafts that may not have sufficient weld penetration to prevent a separation."),
        E("", "OTHER", "Ford utilized this information to determine suspect vehicle production."),
        E("February 24, 2026", "DECISION", "On February 24, 2026, Ford’s Field Review Committee reviewed the concern and approved a field action."),
    ])

# ---------- 26V126
mf = "SoC 0% issue was fixed with VCU and ICUC update, released as Recall to US from MFTBC on 2024.Feb.6 (C10126) for 173 units."
L["RCLRPT-26V126-1137.txt"] = dict(
    S1=C("SUPPORTED", "Name: Mitsubishi Fuso Truck & Bus Corporation", "block"),
    S2=C("SUPPORTED", mf, "chronology", "MFTBC"),
    cause=C("SUPPORTED", "The cause is an Electrical Control Unit transmitting error frames to the Vehicle Control Unit resulting in an error where the SoC is incorrectly displayed.", "cause"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("December 6th 2023", "FILER_AWARENESS", "On December 6th 2023 State of charge was observed to be faultily displayed as 0%."),
        E("2024.Feb.6", "OTHER", mf),
        E("", "FILER_AWARENESS", "However it was found further improvements are required for SoC 0% while standing issue remained."),
        E("", "DECISION", "With Software update development completed, MFTBC is ready to release recall to US units to complete SoC 0% defect in all 244 vehicles imported to the US."),
    ])

# ---------- 26V127
im = "On January 7, 2026, International Motors identified a broken roller on the wheel alignment fixture in their assembly plant as the cause of the tire damage."
L["RCLRPT-26V127-9048.txt"] = dict(
    S1=C("SUPPORTED", "Name: International Motors, LLC", "block"),
    S2=C("SUPPORTED", im, "chronology", "International Motors"),
    cause=C("SUPPORTED", "International Motors, the manufacturer of these vehicles, determined that a broken roller in a wheel alignment fixture caused the fixture to gouge the sidewalls of right rear tires during the vehicle manufacturing process.", "cause"),
    up=U("NAMED", im, "chronology", ["International Motors"]),
    ev=[
        E("December 18, 2025", "FILER_AWARENESS", "On December 18, 2025, a GM brand quality manager submitted a report to GM’s Speak Up For Safety (SUFS) program following a report from a fleet customer that they had received some vehicles with a gouge in the sidewall of the right rear tire."),
        E("January 7, 2026", "SUPPLIER_NOTICE", im),
        E("January 12, 2026", "SUPPLIER_NOTICE", "On January 12, 2026, International Motors provided a list of potentially affected VINs."),
        E("January 13, 2026", "INVESTIGATION_START", "GM opened a product investigation on January 13, 2026."),
        E("February 10, 2026", "OTHER", "An analysis of field data completed on February 10, 2026, identified 37 complaints potentially related to this condition."),
        E("February 26, 2026", "DECISION", "On February 26, 2026, GM’s Safety and Field Decision Authority decided to conduct a safety recall."),
    ])

# ---------- 26V133
L["RCLRPT-26V133-7407.txt"] = dict(
    S1=C("NOT_REPORTED"), S2=C("NOT_REPORTED"),
    cause=C("SUPPORTED", "Insufficient adhesion or pressure bonding may cause one or more solar panels to delaminate and separate from the roof.", "cause"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("February 15, 2026", "FILER_AWARENESS", "On February 15, 2026, Pebble Mobility Inc. (“Pebble”) received a customer report alleging that a solar panel had detached from the roof."),
        E("February 16, 2026", "INVESTIGATION_START", "On February 16, 2026, Pebble initiated an engineering study to investigate the condition and understand the scope of potentially affected vehicles."),
        E("February 24, 2026", "OTHER", "On February 24, 2026, the Pebble Safety Committee convened to assess the issue and review the root cause analysis performed by the Pebble Engineering team."),
        E("February 27, 2026", "DECISION", "On February 27, 2026, Pebble made the determination to voluntarily recall the affected vehicles."),
    ])

# ---------- 26V136
vs = "A process deviation at supplier that may result in intermittent contact in Audio."
L["RCLRPT-26V136-5856.txt"] = dict(
    S1=C("SUPPORTED", "Name: Lear Automotive Morocco SARL (X87), Keni", "block"),
    S2=C("INSUFFICIENT", vs, "cause"),
    cause=C("SUPPORTED", vs, "cause"),
    up=U("UNNAMED", vs, "cause"),
    ev=[
        E("16 October", "FILER_AWARENESS", "16 October a first report was received at Volvo Cars, Normal investigation and monitoring market situation."),
        E("12 of January", "INVESTIGATION_START", "After receiving some more reports an investigation started by Quality 12 of January."),
        E("18th of February", "OTHER", "18th of February the investigation was escalated to the Critical Concern Action Process (CCAP)."),
        E("March 4th, 2026", "DECISION", "On March 4th, 2026, after the completion of the investigation CCMT decided to start preparation for a recall to repair concerned cars wiring harness."),
    ])

# ---------- 26V147
L["RCLRPT-26V147-8112.txt"] = dict(
    S1=C("NOT_REPORTED"), S2=C("NOT_REPORTED"),
    cause=C("NOT_REPORTED"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("March 2, 2026", "FILER_AWARENESS", "On March 2, 2026 during a demonstration on the use of the wheelchair tie-downs with a new employee, an engineer couldn’t lock the tie-down in the anchor."),
        E("", "OTHER", "A visual inspection revealed that the anchor screw cap wasn’t pushed completely down, preventing the apparatus from locking."),
        E("", "OTHER", "After pushing it down manually, the system worked as intended."),
        E("", "INVESTIGATION_START", "An internal review of the procedures and inspection of the vehicles on site revealed that in a small percentage of vehicles, the caps were not pushed down sufficiently."),
        E("", "OTHER", "New tools and procedures were developed to ensure that the installation was consistent throughout, and extensive testing confirmed the successful corrections were implemented."),
    ])

# ---------- 26V150
al = "Upon review, Engineering determined that the Altec label was incorrect."
L["RCLRPT-26V150-4696.txt"] = dict(
    S1=C("SUPPORTED", "Name: Altec Industries Inc.", "block"),
    S2=C("SUPPORTED", al, "chronology", "Altec"),
    cause=C("NOT_REPORTED"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("December, 2025", "FILER_AWARENESS", "In December, 2025, an owner identified a discrepancy between the Altec final stage certification label and the tire ratings of the tires installed on the vehicle."),
        E("", "OTHER", al),
        E("", "INVESTIGATION_START", "Altec opened a root cause investigation, initiating containment procedures and identifying all potentially affected units and began containment of affected units."),
        E("December 12, 2025", "INVESTIGATION_START", "On December 12, 2025, 2025, a potential field action investigation was opened to determine whether additional completed units with an incorrect certification label had been delivered to owners and to find the number of field-affected units."),
        E("March 6, 2026", "DECISION", "On March 6, 2026, after reviewing the potential issue and the affected unit investigation, Altec determined that a field action was necessary to inspect and replace the potentially incorrect certification labels."),
    ])

# ---------- 26V153
oe = "Orange EV (OEV) produces electric terminal trucks that are primarily used at private shipping yards and terminals but may also operate on public roads in some capacity."
fin = "This assessment occurred through early March 2026, and on March 6, 2026, OEV concluded that the training seat did not meet FMVSS requirements for Designated Seating Positions under FMVSS 207 and 210."
L["RCLRPT-26V153-3088.txt"] = dict(
    S1=C("SUPPORTED", "Name: Orange EV", "block"),
    S2=C("SUPPORTED", oe, "chronology", "Orange EV"),
    cause=C("NOT_REPORTED"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("November 2022", "OTHER", "In November 2022, OEV began offering a foldable training seat as an option that customers could select at the time of order."),
        E("October 2025", "OTHER", "In October 2025, a customer requested the installation of a foldable training seat in their trucks."),
        E("early December 2025", "INVESTIGATION_START", "To support this request and given the passage of time, beginning in early December 2025, OEV undertook a comprehensive review of the training seat and its compliance with any applicable FMVSS requirements."),
        E("early March 2026", "OTHER", fin),
        E("March 6, 2026", "DECISION", fin),
    ])

# ---------- 26V170
nv = "In November 2025, a missing harness was discovered while troubleshooting for a different issue on a unit during production testing at Altec."
L["RCLRPT-26V170-5531.txt"] = dict(
    S1=C("SUPPORTED", "Name: ALTEC", "block"),
    S2=C("SUPPORTED", nv, "chronology", "Altec"),
    cause=C("NOT_REPORTED"),
    up=U("NONE_MENTIONED"),
    ev=[
        E("November 2025", "FILER_AWARENESS", nv),
        E("", "INVESTIGATION_START", "Upon identifying the issue, Altec immediately initiated an investigation to determine the underlying cause."),
        E("", "OTHER", "The investigation revealed the required harness was not installed on units built on a specific production line."),
        E("", "OTHER", "As a result, containment actions were promptly implemented, and the potentially affected units were inspected."),
        E("", "OTHER", "Further investigation indicated that additional units assembled on a particular production line could have been completed without the necessary harness."),
        E("", "OTHER", "It was also found that some units might have passed production testing without the lighting issue being detected and without the missing harness being noticed."),
        E("February 25, 2026", "INVESTIGATION_START", "On February 25, 2026, Altec opened a potential field action investigation to determine the scope of the issue, identify production dates, and affected units."),
        E("March 13, 2026", "DECISION", "On March 13, 2026, Altec determined that a potential defect affecting units in the field could exist and owner notification was necessary."),
    ])

# ---------- 26V172
mb = "Due to a deviation in the production process at the supplier, the incorrect seat belt variant might have been installed in the center rear seating position."
L["RCLRPT-26V172-3940.txt"] = dict(
    S1=C("SUPPORTED", "Name: Lear Corporation GmbH", "block"),
    S2=C("INSUFFICIENT", mb, "cause"),
    cause=C("SUPPORTED", mb, "cause"),
    up=U("UNNAMED", mb, "cause"),
    ev=[
        E("September 2025", "INVESTIGATION_START", "In September 2025, MBAG launched initial investigations regarding the potential installation of different belt variants based on seatbelt part anomalies discovered during an internal audit."),
        E("", "OTHER", "In the following months, out of an abundance of caution, MBAG implemented a plant action to rework all potentially affected vehicles, which were still accessible to MBAG."),
        E("November 2025", "FILER_AWARENESS", "In November 2025, MBAG became aware that vehicles in the field could also be affected."),
        E("", "INVESTIGATION_START", "Further analyses were initiated to determine the root cause of the possible deviation."),
        E("end of January 2026", "OTHER", "These analyses lasted until the end of January 2026."),
        E("February 2026", "INVESTIGATION_START", "In February 2026, MBAG launched investigations into potential consequences of different variants of the seat belts and to determine the potentially affected population in the field."),
        E("March 13, 2025", "DECISION", "On March 13, 2025, MBAG determined that a non-compliance cannot be ruled out and decided to conduct a recall."),
    ])

# ---------- 26V175
hs = "Hino worked with the supplier to investigate the issue and identify the root cause and potential scope."
L["RCLRPT-26V175-7571.txt"] = dict(
    S1=C("SUPPORTED", "Name: Saturn Printing", "block"),
    S2=C("INSUFFICIENT", hs, "chronology"),
    cause=C("SUPPORTED", "Due to process issues at the supplier, inside pages from an owner’s manual for a different model were printed with the cover for the subject model.", "cause"),
    up=U("UNNAMED", hs, "chronology"),
    ev=[
        E("January 14, 2026", "FILER_AWARENESS", "On January 14, 2026, Hino discovered during a Model Year 2027 production audit that some owner’s manuals for the identified Model Year 2026 vehicles contained pages from an owner’s manual associated with a different vehicle model."),
        E("", "INVESTIGATION_START", hs),
        E("", "INVESTIGATION_START", "Hino also began to assess potential customer impacts that could result from the issue."),
        E("February 2026", "SUPPLIER_NOTICE", "In February 2026, the supplier reported to Hino that a printer malfunction occurred while printing a specific order and, when printing resumed, the incorrect inside pages were mistakenly selected and printed for the remainder of the order."),
        E("", "INVESTIGATION_START", "Hino reviewed production records to identify the population of vehicles for which the incorrect owner’s manual may have been provided."),
        E("", "OTHER", "Hino also identified several differences between the correct and incorrect manual pages that could result in safety concerns in the event owners rely on the information in performing certain maintenance."),
        E("", "INVESTIGATION_START", "A technical review was performed to evaluate the impact those differences could have on vehicle safety."),
        E("March 2026", "OTHER", "In March 2026, Hino concluded that the front U-Bolt tightening torque specification in the incorrect pages was higher than the correct specification, which could result in bolt breakage if followed."),
        E("March 17, 2026", "DECISION", "On March 17, 2026, based on the investigation results, Hino determined to conduct a voluntary safety recall campaign for the subject vehicles."),
    ])

# ---------- build + verify
errors = []
out = []
files = sorted(f for f in os.listdir(T) if f.endswith(".txt") and not f.startswith("._"))
assert set(files) == set(L), (set(files) ^ set(L))
for f in files:
    fname, sec = sections(os.path.join(T, f))
    lab = L[f]
    def chk(q, s, what):
        if not q:
            return
        if len(q) > 300:
            errors.append(f"{f} {what}: quote too long {len(q)}")
        if norm(q) not in sec.get(s, ""):
            errors.append(f"{f} {what}: quote not found in {s}: {q[:80]}")
    claims = []
    for cid in ("S1", "S2"):
        c = lab[cid]
        chk(c["quote"], c["section"], cid)
        o = {"id": cid, "status": c["status"]}
        if cid == "S2" and c["status"] == "SUPPORTED":
            o["name"] = c["name"]
        o["quote"] = c["quote"]; o["section"] = c["section"]
        claims.append(o)
    c = lab["cause"]; chk(c["quote"], c["section"], "cause")
    cause = {"status": c["status"], "quote": c["quote"], "section": c["section"]}
    u = lab["up"]; chk(u["quote"], u["section"], "upstream")
    up = {"kind": u["kind"], "names": u["names"], "quote": u["quote"], "section": u["section"]}
    evs = []
    last_pos = -1
    for i, e in enumerate(lab["ev"]):
        chk(e["quote"], "chronology", f"event{i}")
        pos = sec["chronology"].find(norm(e["quote"]))
        if pos < last_pos:
            errors.append(f"{f} event{i}: out of order")
        last_pos = max(last_pos, pos)
        o = {"date_text": e["date_text"], "type": e["type"], "quote": e["quote"]}
        if e["entry"]:
            chk(e["entry"], "chronology", f"event{i}-entry")
            if e["date_text"] not in e["entry"]:
                errors.append(f"{f} event{i}: date not in entry_quote")
            o["inherited_date"] = True; o["entry_quote"] = e["entry"]; o["date_inferred"] = False
        elif e["date_text"]:
            if e["date_text"] not in norm(e["quote"]):
                errors.append(f"{f} event{i}: date_text not in quote")
            o["inherited_date"] = False; o["date_inferred"] = False
        else:
            o["inherited_date"] = False; o["date_inferred"] = True
        evs.append(o)
    out.append({"file": fname, "claims": claims, "cause": cause, "upstream": up, "events": evs})

if errors:
    print("\n".join(errors)); sys.exit(1)
with open(os.path.join(D, "passB.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("ok", len(out), sum(len(o["events"]) for o in out))
