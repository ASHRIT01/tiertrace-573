import json, re, os, sys
D = os.path.dirname(os.path.abspath(__file__))

def E(d, t, q): return {"date_text": d, "type": t, "quote": q, "inherited_date": False, "date_inferred": False}
def I(d, t, q, eq): return {"date_text": d, "type": t, "quote": q, "inherited_date": True, "entry_quote": eq, "date_inferred": False}
def N(t, q): return {"date_text": "", "type": t, "quote": q, "inherited_date": False, "date_inferred": True}
def S1(name): return {"id": "S1", "status": "SUPPORTED", "quote": "Name: " + name, "section": "block"}
S1NR = {"id": "S1", "status": "NOT_REPORTED", "quote": "", "section": ""}
def S2s(name, q, sec="chronology"): return {"id": "S2", "status": "SUPPORTED", "name": name, "quote": q, "section": sec}
def S2i(q, sec): return {"id": "S2", "status": "INSUFFICIENT", "quote": q, "section": sec}
S2NR = {"id": "S2", "status": "NOT_REPORTED", "quote": "", "section": ""}
def C(st, q): return {"status": st, "quote": q, "section": "cause" if q else ""}
CNR = {"status": "NOT_REPORTED", "quote": "", "section": ""}
def UN(names, q, sec="chronology"): return {"kind": "NAMED", "names": names, "quote": q, "section": sec}
def UU(q, sec="chronology"): return {"kind": "UNNAMED", "names": [], "quote": q, "section": sec}
UNONE = {"kind": "NONE_MENTIONED", "names": [], "quote": "", "section": ""}

L = []

# 26V518
q1 = "6/16/26: Engineering notified Compliance that Production found out on June 15, 2026, that they need to wire the auto level controller differently now that production is no longer using BMPro."
e622 = "6/22/26: The incident was reviewed by the Warranty Incident Review Committee (WIRC)."
e85 = "8/5/26: Corrective and Preventive Action Committee (CPAC) met and determined that since the wire was omitted for the stop lamp lockout for the Auto Level System, there is a potential safety risk because the retail owner could use the phone app to activate the jacks during travel."
L.append({"file": "RCLRPT-26V518-5347.pdf",
 "claims": [S1("DAVE CARTER & ASSOCIATES, INC"), S2i("Name: DAVE CARTER & ASSOCIATES, INC", "block")],
 "cause": C("SUPPORTED", "Production did not install and connect the wire necessary for the Auto Level Jack lockout to function."),
 "upstream": UN(["BMPro"], q1),
 "events": [
  E("6/16/26", "FILER_AWARENESS", q1),
  E("June 15, 2026", "FILER_AWARENESS", q1),
  E("6/22/26", "OTHER", e622),
  I("6/22/26", "OTHER", "The members of WIRC decided to elevate it to the Corrective and Preventive Action Committee (CPAC).", e622),
  E("7/1/26", "INVESTIGATION_START", "7/1/26: During the Corrective and Preventive Action Committee (CPAC) meeting, Engineering informed the committee that root cause analysis would begin."),
  E("7/15/26", "OTHER", "7/15/26: Corrective and Preventive Action Committee (CPAC) met and decided that additional testing needs to be conducted."),
  E("8/5/26", "OTHER", e85),
  I("8/5/26", "OTHER", "CPAC decided to submit the incident to the Safety Steering Committee (SSC) for review and a vote.", e85),
  E("8/6/26", "DECISION", "8/6/26: An email vote was conducted by the Safety Steering Committee (SSC) and voted in favor of proceeding with a safety recall due to the possibility that the jacks could be activated during transit by the phone app."),
 ]})

# 26V520
bbM = "May 2026: Blue Bird began an in-depth review of the installation of the 12V power wire on the C and D-Zones."
bbA = "April 2026: Blue Bird received field complaints where bus units experienced thermal stress of the C- Zone body harness."
L.append({"file": "RCLRPT-26V520-6158.pdf",
 "claims": [S1("Blue Bird"), S2s("Blue Bird", bbA)],
 "cause": C("SUPPORTED", "Rubbing between the unfused 12V power wire and edges of body components could result in the C or D-Zone harness overheating, ultimately resulting in a short to ground."),
 "upstream": UNONE,
 "events": [
  E("April 2026", "FILER_AWARENESS", bbA),
  E("May 2026", "INVESTIGATION_START", bbM),
  I("May 2026", "OTHER", "Blue Bird’s investigation revealed that the power wire was rubbing on bus component edges over time, resulting in abrasion.", bbM),
  E("July 2026", "OTHER", "July 2026: Blue Bird further ruled out the risk of a thermal event, as the C and D-Zone harnesses are contained within and around non-combustible materials."),
  E("August 5, 2026", "DECISION", "August 5, 2026: Blue Bird’s Safety Committee determined that this issue affects safety critical components, deeming it a safety recall."),
  E("August 10, 2026", "NHTSA_FILING", "August 10, 2026: Blue Bird submitted a defect report."),
 ]})

# 26V521
hJ = "July 30, 2026 Marion Body Works was notified that two trucks that we built had components affected by this recall installed on them."
hq = "May 8, 2026 Hale Products Inc tested to determine that the same screen issues apply to Hale products that utilize different firmware which could have impacted or prevented the issue."
L.append({"file": "RCLRPT-26V521-9708.pdf",
 "claims": [S1("Hale Products"), S2s("Hale Products", hq)],
 "cause": C("INSUFFICIENT", "Root cause is being researched."),
 "upstream": UN(["Hale Products", "Weldon", "Akron Brass Company", "Enovation Controls"], "April 26, 2026 Weldon, an Akron Brass Company brand filed a part 573 recall resulting in NHTSA 26E020 regarding the same Enovation Controls touch screen user interface as noticed here."),
 "events": [
  E("April 26, 2026", "OTHER", "April 26, 2026 Weldon, an Akron Brass Company brand filed a part 573 recall resulting in NHTSA 26E020 regarding the same Enovation Controls touch screen user interface as noticed here."),
  E("May 8, 2026", "INVESTIGATION_START", hq),
  E("May 10, 2026", "OTHER", "May 10, 2026 Based on test results and Weldon recall Hale started a draft part 573 notice NHTSA portal."),
  E("May13, 2026", "OTHER", "May13, 2026 Hale researched the systems shipped that used the effected display and the qty affected and submitted the part 573 recall."),
  E("July 30, 2026", "FILER_AWARENESS", hJ),
  I("July 30, 2026", "NHTSA_FILING", "We identified which units those were and began the process of submitting the recall so we can notify our customers of the defect on their trucks.", hJ),
 ]})

# 26V527
L.append({"file": "RCLRPT-26V527-2982.pdf",
 "claims": [S1("SuperAlloy Industrial Co. Ltd"), S2i("Name: SuperAlloy Industrial Co. Ltd", "block")],
 "cause": CNR, "upstream": UNONE,
 "events": [
  N("FILER_AWARENESS", "During the course of repairs under prior safety recalls D025, D027 & N759, a concern was raised that the replacement front suspension knuckle had been difficult to fit onto a small number of vehicles."),
  N("OTHER", "On inspection of the engineering release data, it was revealed that the as-published repair procedure did not specify the correct replacement part for Range Rover SV vehicles."),
  E("04 August 2026", "OTHER", "On 04 August 2026, the issue was referred to JLR’s Product Safety and Compliance Committee (PSCC) for review,"),
  E("06 August 2026", "DECISION", "On 06 August 2026, the PSCC Decision Forum reviewed the matter and requested a safety recall be launched to remedy the incorrectly repaired vehicles."),
 ]})

# 26V528
L.append({"file": "RCLRPT-26V528-8235.pdf",
 "claims": [S1("Nascote Industries, Inc."), S2i("Name: Nascote Industries, Inc.", "block")],
 "cause": CNR, "upstream": UNONE,
 "events": [
  E("October 28, 2021", "NHTSA_FILING", "On October 28, 2021, FCA US LLC (\"FCA US\") filed NHTSA Recall ID 21V842 (\"Y73\") for 2021 MY Dodge Durango for rear spoilers that may detach from the vehicle."),
  E("February 23, 2023", "NHTSA_FILING", "On February 23, 2023, FCA US filed NHTSA Recall ID 23V115 (\"20A\") for 2021-2023 MY Dodge Durango for rear spoilers that may detach from the vehicle."),
  E("March 19, 2026", "INVESTIGATION_START", "On March 19, 2026, the FCA US Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation due to field data indicating potential rear spoiler detachments after Y73 or 20A recall remedies were completed."),
  E("March 19, 2026", "INVESTIGATION_START", "From March 19, 2026, through June 02, 2026, FCA US TSRC reviewed field data and met with Engineering to understand the part design and change history."),
  E("August 06, 2026", "DECISION", "On August 06, 2026, FCA US determined, through the Vehicle Regulations Committee, that a safety defect exists in certain vehicles."),
 ]})

# 26V529
L.append({"file": "RCLRPT-26V529-9405.pdf",
 "claims": [S1("Aptiv"), S2i("Name: Aptiv", "block")],
 "cause": CNR, "upstream": UNONE,
 "events": [
  E("June 18, 2026", "INVESTIGATION_START", "On June 18, 2026, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into some 2026 MY Jeep Grand Cherokee and Grand Cherokee L vehicles with a software issue which may disable windshield wiper functionality."),
  E("June 2026", "INVESTIGATION_START", "From June 2026 through July 2026, FCA US TSRC met with FCA US engineering and manufacturing to review the issue, understand the failure mode, and to determine the suspect population."),
  E("August 06, 2026", "DECISION", "On August 06, 2026, FCA US determined, through the Vehicle Regulations Committee, that a safety defect exists in certain vehicles."),
 ]})

# 26V531
L.append({"file": "RCLRPT-26V531-6260.pdf",
 "claims": [S1("Harman Becker Automotive Systems Inc."), S2i("Name: Harman Becker Automotive Systems Inc.", "block")],
 "cause": CNR, "upstream": UNONE,
 "events": [
  E("May 7, 2026", "INVESTIGATION_START", "On May 7, 2026, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into a potential issue related to a loss of rearview image display"),
  E("May and June 2026", "INVESTIGATION_START", "During May and June 2026, FCA US TSRC and FCA US Engineering reviewed warranty data, field records, vehicle production records and customer assistance records to understand potential customer consequence."),
  E("July 15, 2026", "OTHER", "On July 15, 2026, FCA US TSRC organization recognized an issue existed on certain vehicles related to the rearview image not being displayed, potentially resulting in a noncompliance with FMVSS No.111."),
  E("August 06, 2026", "DECISION", "On August 06, 2026, FCA US determined, through the Vehicle Regulations Committee, that a noncompliance to FMVSS No. 111 exists in certain vehicles."),
 ]})

# 26V535
L.append({"file": "RCLRPT-26V535-7741.pdf",
 "claims": [S1("The Heil Co."), S2s("The Heil Co.", "Between February and March 2026, The Heil Co. removed and inspected CNG cylinders from fourteen (14) customer vehicles equipped with the same ladder configuration.")],
 "cause": C("SUPPORTED", "An incorrect length bolt may be installed during initial build or during ladder service."),
 "upstream": UU("Measurements of the observed blemishes were evaluated against the cylinder manufacturer's damage assessment criteria and were determined to be within repairable limits."),
 "events": [
  E("November 2025", "FILER_AWARENESS", "In November 2025 Heil learned that a ladder mounting bracket may have been assembled with a bolt longer than specified in one leg of the ladder support structure on a customer unit."),
  N("INVESTIGATION_START", "however, The Heil Co. initiated an investigation to evaluate the potential for cylinder-to-bolt contact."),
  E("February and March 2026", "INVESTIGATION_START", "Between February and March 2026, The Heil Co. removed and inspected CNG cylinders from fourteen (14) customer vehicles equipped with the same ladder configuration."),
  N("OTHER", "Inspection identified surface blemishes on seven (7) cylinders in an area corresponding to the location of the ladder mounting bolt."),
  N("OTHER", "Measurements of the observed blemishes were evaluated against the cylinder manufacturer's damage assessment criteria and were determined to be within repairable limits."),
  N("INVESTIGATION_START", "The Heil Co. continued its investigation to determine the mechanism by which the observed blemishes could occur."),
  N("OTHER", "The investigation determined that installation of an incorrect bolt at one particular location during vehicle assembly or during subsequent service and inspection activities could reduce the intended clearance between the ladder structure and the cylinder."),
  E("July and early August 2026", "INVESTIGATION_START", "The investigation continued through July and early August 2026."),
  N("OTHER", "Based on the investigation findings, The Heil Co. concluded that an incorrect bolt could potentially be installed in the affected location and could reduce the designed clearance to the adjacent CNG cylinder,"),
  E("August 4, 2026", "OTHER", "To eliminate the possibility of incorrect bolt installation at this location, The Heil Co. implemented a design change on August 4, 2026, removing the ladder support leg containing the subject bolt ."),
  E("August 11, 2026", "DECISION", "On August 11, 2026, The Heil Co. determined that the condition described above constituted a safety- related defect and decided to conduct a voluntary safety recall."),
 ]})

# 26V541
a1 = "On June 25, 2026, during a Bendix programming audit conducted by the chassis team, Altec identified completed vehicles that had not received the required Bendix programming following installation."
L.append({"file": "RCLRPT-26V541-1703.pdf",
 "claims": [S1("Altec Ind. Inc."), S2s("Altec", a1)],
 "cause": CNR, "upstream": UN(["Bendix"], a1),
 "events": [
  E("June 25, 2026", "FILER_AWARENESS", a1),
  N("INVESTIGATION_START", "Altec initiated an investigation to determine whether other complete vehicles were affected."),
  E("August 10, 2026", "OTHER", "On August 10, 2026, the investigation identified 55 complete vehicles within the affected population."),
  E("August 10, 2026", "INVESTIGATION_START", "On August 10, 2026, a potential field action investigation was opened to review the scope of the issue."),
  E("August 14, 2026", "DECISION", "On August 14, 2026, after reviewing the potential field action investigation results, Altec approved the field action."),
 ]})

# 26V552
j729 = "7/29/26: Engineering provided Compliance with a scope of 8 units and reported a data entry error for the axle rating."
j83 = "8/3/26: The incident was reviewed by the Warranty Incident Review Committee (WIRC)."
L.append({"file": "RCLRPT-26V552-4130.pdf",
 "claims": [S1NR, S2NR],
 "cause": C("SUPPORTED", "Engineering data entry error resulting in an incorrect gross axle weight rating on the certification label."),
 "upstream": UNONE,
 "events": [
  E("7/28/26", "FILER_AWARENESS", "7/28/26 Production discovered the axle rating on the Certification labels was 8,000 pounds but the axles are actually rated at 7,000 pounds."),
  E("7/29/26", "OTHER", j729),
  I("7/29/26", "OTHER", "An incident was generated for review by WIRC.", j729),
  E("8/3/26", "OTHER", j83),
  I("8/3/26", "OTHER", "The members of WIRC decided to elevate it to the Corrective and Preventive Action Committee (CPAC) due to a non- compliance to 49 CRF Part 567.4 Certification.", j83),
  E("8/5/26", "OTHER", "8/5/26: The Corrective and Preventive Action Committee (CPAC) met to review the incident and decided to elevate the matter to the Safety Steering Committee (SSC)."),
  E("8/27/26", "DECISION", "8/27/26: Safety Steering Committee (SSC) met and voted in favor of proceeding with a noncompliance recall for failing to comply with requirement of the 49 CFR Part 567, “Certification.”"),
 ]})

# 26V553
mt = "The additional claims were reported on June 23, 2026, and July 16, 2026."
L.append({"file": "RCLRPT-26V553-8526.pdf",
 "claims": [S1NR, S2NR],
 "cause": C("SUPPORTED", "Variations in the welding process may have resulted in insufficient weld integrity between the winch post and base plate."),
 "upstream": UNONE,
 "events": [
  E("May 20, 2026", "FILER_AWARENESS", "On May 20, 2026, Magic Tilt Trailers received notice from NHTSA of a VOQ concerning a winch post issue on a 2025 trailer."),
  E("July 16, 2026", "FILER_AWARENESS", "On July 16, 2026, further investigation identified two additional warranty claims, bringing the total number of reports to three."),
  E("June 23, 2026", "FILER_AWARENESS", mt),
  E("July 16, 2026", "FILER_AWARENESS", mt),
  N("OTHER", "Review identified a possible safety issue involving the weld between the winch post and the base plate on certain aluminum PWC trailers manufactured between January 1, 2025, and December 31, 2025."),
  N("INVESTIGATION_START", "Magic Tilt immediately reviewed the applicable records and identified the trailers that could potentially be affected."),
  E("August 2026", "DECISION", "In August 2026, Magic Tilt initiated a safety recall."),
 ]})

# 26V554
j78 = "7/8/26: Jayco Motorized group informed Compliance via email of a situation where the label was incorrect."
j713 = "7/13/26: The incident was reviewed by the Warranty Incident Review Committee (WIRC)."
L.append({"file": "RCLRPT-26V554-9708.pdf",
 "claims": [S1NR, S2NR],
 "cause": C("SUPPORTED", "Engineering data entry error with the incorrect tire width."),
 "upstream": UNONE,
 "events": [
  E("7/8/26", "FILER_AWARENESS", j78),
  I("7/8/26", "INVESTIGATION_START", "Compliance reached out to the Jayco chassis group to determine scope.", j78),
  E("7/13/26", "OTHER", j713),
  I("7/13/26", "OTHER", "The members of WIRC decided to elevate it to the Corrective and Preventive Action Committee (CPAC) due to a potential safety issue.", j713),
  E("7/15/26", "OTHER", "7/15/26: The Corrective and Preventive Action Committee (CPAC) met to discuss this incident and decided more information needed to be collected."),
  E("8/5/26", "OTHER", "8/5/26: The Corrective and Preventive Action Committee (CPAC) met to discuss this incident and elevated it to the Safety Steering Committee due to understanding the scope and the issue."),
  E("8/27/26", "DECISION", "8/27/26: The Safety Steering Committee (SSC) voted in favor of proceeding with a noncompliance recall for failing to comply with requirement of the 49 CFR Part 120 section 5.3 \"Wheels and rims-other than passenger cars\""),
 ]})

# 26V558
L.append({"file": "RCLRPT-26V558-7885.pdf",
 "claims": [S1("Relyans Max Inc"), S2i("Name: Relyans Max Inc", "block")],
 "cause": CNR, "upstream": UNONE,
 "events": [
  E("August 7, 2026", "FILER_AWARENESS", "On August 7, 2026, Tesla personnel flagged a vehicle for a handling and noise concern at its Fremont Assembly Factory."),
  N("FILER_AWARENESS", "Upon inspection at end-of-line, Tesla’s production quality team discovered a missing fastener at the lateral link to sub-frame attachment."),
  E("August 7, 2026", "INVESTIGATION_START", "On August 7, 2026, Tesla initiated a vehicle containment hold and began investigating the issue."),
  E("August 7, 2026", "OTHER", "On August 7, 2026, after reviewing production records, Tesla's production quality team identified the incorrect torque recovery was completed for the vehicle in question."),
  E("July 26, 2026", "OTHER", "On July 26, 2026, a Programmable Logic Controller (PLC) control, which assured position control for a recovery torque completion tool, was inadvertently deactivated, eliminating process control for assuring the correct fastener was torqued."),
  E("August 10, 2026", "INVESTIGATION_START", "From August 10, 2026 – August 21, 2026, Tesla reviewed production torque records and video footage as well as vehicle test and repair records to further assess vehicle production between July 26, 2026, and August 7, 2026."),
  E("August 24, 2026", "OTHER", "On August 24, 2026, Tesla completed their investigation of all production records and affected vehicle population."),
  E("August 25, 2026", "DECISION", "On August 25, 2026, Tesla made a determination to voluntarily recall the affected vehicles."),
 ]})

# 26V561
L.append({"file": "RCLRPT-26V561-7630.pdf",
 "claims": [S1("CTS CORPORATION"), S2i("Name: CTS CORPORATION", "block")],
 "cause": CNR, "upstream": UNONE,
 "events": [
  E("March 25, 2026", "INVESTIGATION_START", "On March 25, 2026, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into some 2025-2026MY Chrysler Pacifica, Pacifica PHEV and Voyager vehicles that may have a loss of the brake pedal position sensor function."),
  E("March 2026", "INVESTIGATION_START", "From March 2026 through May 2026, FCA US TSRC met with FCA US Engineering to understand potential root cause, customer consequence and vehicle scope."),
  E("June 2026", "INVESTIGATION_START", "From June 2026 through August 2026, FCA US TSRC conducted analysis of additional field records and customer assistance records to verify affected components and vehicle scope."),
  E("August 5, 2026", "OTHER", "On August 5, 2026, FCA US TSRC organization recognized that a vehicle build issue existed on certain vehicles related to the brake pedal position sensor, potentially resulting in a noncompliance with FMVSS No. 126."),
  E("August 26, 2026", "DECISION", "On August 26, 2026, FCA US determined, through the Vehicle Regulations Committee, that a noncompliance to a Federal Motor Vehicle Safety Standard potentially exists in certain vehicles."),
 ]})

# 26V563
L.append({"file": "RCLRPT-26V563-6702.pdf",
 "claims": [S1NR, S2NR],
 "cause": C("SUPPORTED", "Production error"),
 "upstream": UNONE,
 "events": [
  E("August 20, 2026", "FILER_AWARENESS", "On August 20, 2026, Forest River's Corporate PDI was performing an inspection of a unit and found the concern."),
  E("August 24, 2026", "INVESTIGATION_START", "On August 24, 2026, Forest River's Corporate Standards Manager went to the plant to look into the concern and inspect units on hand."),
  E("August 26, 2026", "FILER_AWARENESS", "On August 26, 2026, Forest River's Office of Corporate Compliance was made aware of the concern and began research."),
  E("August 31, 2026", "DECISION", "On August 31, 2026, Forest Rivers Corporate Recall Committee voted to Recall"),
 ]})

# 26V568
h28 = "28-APR-2026: Hiab received a report of a second field failure."
h28b = "28-APR-2026 through 5-May-2026: The investigation observed broken deck pins in the field failures."
L.append({"file": "RCLRPT-26V568-9693.pdf",
 "claims": [S1("Hiab USA Inc."), S2s("Hiab", h28)],
 "cause": C("SUPPORTED", "Improperly bled hydraulic systems could lead to cylinders operating asymmetrically, increasing the risk of cracking in the deck pin."),
 "upstream": UN(["Hiab USA"], "Based on the investigation, Hiab USA decided to conduct a safety recall for the subject liftgates."),
 "events": [
  E("20-APR-2026", "INVESTIGATION_START", "20-APR-2026: Report of a field failure that Hiab reviewed and began investigating the potential cause."),
  E("28-APR-2026", "OTHER", h28),
  I("28-APR-2026", "INVESTIGATION_START", "The issue was escalated for further investigation.", h28),
  E("28-APR-2026", "OTHER", h28b),
  I("28-APR-2026", "INVESTIGATION_START", "Hiab reviewed warranty claims involving deck pins and inspected additional units in the field.", h28b),
  I("28-APR-2026", "OTHER", "Based on the investigation's review, Hiab found evidence of liftgates with hydraulic cylinders that appeared to operate asymmetrically, as well as evidence of hydraulic systems that had not been properly bled, which likely contributed to deck pin failures.", h28b),
  E("5-May-2026", "OTHER", "5-May-2026: The issue was elevated to Hiab’s liftgate leadership."),
  N("DECISION", "Based on the investigation, Hiab USA decided to conduct a safety recall for the subject liftgates."),
 ]})

# 26V577
L.append({"file": "RCLRPT-26V577-7489.pdf",
 "claims": [S1("Ford Motor Company"), S2s("Ford", "On March 5, 2026, Ford’s Critical Concern Review Group (CCRG) opened an investigation into loose or missing rear Panhard rod fasteners on 2026 MY Ford F-150 Raptor vehicles.")],
 "cause": C("SUPPORTED", "The error-proofing device at the relevant torque station was in bypass mode for a period during production, resulting in incomplete or non-conforming torque data for some vehicles."),
 "upstream": UNONE,
 "events": [
  E("February 23, 2026", "FILER_AWARENESS", "On February 23, 2026, Dearborn Truck Plant (DTP) was alerted to a warranty claim on a model year (MY) 2026 Ford F-150 Raptor regarding a “customer rattle.”"),
  N("OTHER", "Upon further inspection, the dealer confirmed that the rear Panhard rod was loose."),
  N("OTHER", "Further Investigation by DTP concluded that the error- proofing data for the relevant torque station was in bypass mode from December 27, 2025, until January 23, 2026."),
  N("OTHER", "A review of the torque data confirmed the vehicles that either did not meet the torque requirement or had missing/incomplete rundown data."),
  E("March 5, 2026", "INVESTIGATION_START", "On March 5, 2026, Ford’s Critical Concern Review Group (CCRG) opened an investigation into loose or missing rear Panhard rod fasteners on 2026 MY Ford F-150 Raptor vehicles."),
  N("INVESTIGATION_START", "As part of its ongoing investigation, CCRG evaluated the geometry of the suspension system and detectability of a loose Panhard rod."),
  E("August 2026", "OTHER", "CCRG continued its evaluation and in August 2026 ultimately determined that the loose condition may not be detectable from inside the cabin."),
  N("OTHER", "CCRG also considered the likely usage of these vehicles by owners, many of whom are driving or racing enthusiasts."),
  E("August 2026", "OTHER", "In August 2026, Ford's Global Data Insight and Analytics (GDIA) team completed a statistical analysis of the potentially affected population, which indicated a low likelihood of future field failures."),
  E("September 1, 2026", "DECISION", "On September 1, 2026, Ford’s Field Review Committee reviewed the concern and approved a field service action."),
 ]})

# 26V581
sup = "The passenger airbag supplier informed Ford that the active vent activation unit on the passenger airbag module failed to deploy correctly during a routine lot acceptance (LAT) audit test."
L.append({"file": "RCLRPT-26V581-3933.pdf",
 "claims": [S1("Joyson Safety Systems"), S2i(sup, "chronology")],
 "cause": C("SUPPORTED", "Certain passenger airbags assembled by the supplier were manufactured with incorrect active vent activation units."),
 "upstream": UU(sup),
 "events": [
  E("August 7, 2026", "FILER_AWARENESS", "On August 7, 2026, an issue pertaining to the 2026 Ford Explorer passenger airbag active vent was brought to Ford’s Critical Concern Review Group (CCRG) for review."),
  N("SUPPLIER_NOTICE", sup),
  E("August 7, 2026", "INVESTIGATION_START", "Beginning August 7, 2026, Ford conducted evaluation of the suspect active vent activation units."),
  E("September 1, 2026", "DECISION", "On September 1, 2026, Ford’s Field Review Committee reviewed the concern and approved a field action."),
 ]})

# 26V598
t1 = "June 2026 – July 2026 In late June 2026, during a standard quality audit, a tier 1 supplier conducted tensile strength tests and found a production batch of front steering knuckles that had material strength below specification."
t2 = "August 2026 – September 2026 In August to September 2026, Toyota investigated the impact of the below-specification material on the steering knuckle’s performance."
tsup = "The supplier contacted Toyota regarding the issue since the batch had already been shipped to the tier 2 supplier."
L.append({"file": "RCLRPT-26V598-8506.pdf",
 "claims": [S1("Bharat Forge Aluminum USA, INC"), S2i(tsup, "chronology")],
 "cause": CNR,
 "upstream": UU(tsup),
 "events": [
  E("late June 2026", "OTHER", "In late June 2026, during a standard quality audit, a tier 1 supplier conducted tensile strength tests and found a production batch of front steering knuckles that had material strength below specification."),
  I("June 2026 – July 2026", "SUPPLIER_NOTICE", tsup, t1),
  I("June 2026 – July 2026", "OTHER", "Toyota initiated containment activities and determined that some parts flowed out to the Toyota manufacturing plants.", t1),
  I("June 2026 – July 2026", "OTHER", "Toyota was able to identify some of the affected parts based on their batch ID, however a small number of parts were not contained.", t1),
  I("June 2026 – July 2026", "INVESTIGATION_START", "Additionally, Toyota began an investigation of the tier 1 supplier's manufacturing process and documentation.", t1),
  I("June 2026 – July 2026", "OTHER", "As a result of the investigation, Toyota confirmed that only one batch did not go through the aging furnace step.", t1),
  E("August to September 2026", "INVESTIGATION_START", "In August to September 2026, Toyota investigated the impact of the below-specification material on the steering knuckle’s performance."),
  I("August 2026 – September 2026", "INVESTIGATION_START", "Toyota conducted CAE on models of the part with the below- specification material.", t2),
  I("August 2026 – September 2026", "OTHER", "The test results concluded that a fracture could occur at the strut attachment point and/or the tie rod attachment point after a sudden large impact force such as from hitting a pot hole or a curb.", t2),
  I("August 2026 – September 2026", "OTHER", "Toyota further assessed the impact to vehicle performance should the steering knuckle fracture at these locations while driving and determined that the vehicle steering control function may be reduced or lost.", t2),
  E("September 11, 2026", "DECISION", "September 11, 2026 Based on the results of the above investigation, Toyota decided to conduct a voluntary safety recall campaign."),
 ]})

# 26V607
jsup = "On 18 August 2026, the Powertrain Control Module (PCM) supplier informed JLR that a review of production records had identified a small number of modules which had been identified as having anomalous production parameters."
L.append({"file": "RCLRPT-26V607-0797.pdf",
 "claims": [S1("Robert Bosch Elektronik GmbH"), S2i(jsup, "chronology")],
 "cause": CNR, "upstream": UU(jsup),
 "events": [
  E("18 August 2026", "SUPPLIER_NOTICE", jsup),
  N("INVESTIGATION_START", "Work was started to trace the affected parts to vehicles."),
  E("24 August 2026", "OTHER", "On 24 August 2026, a pre stop shipment meeting was held where it was confirmed that a number of at- risk PCMs had been assembled into new vehicles, and a Quarantine notice was issued together with an Update Prior to Sale instruction."),
  N("OTHER", "It was reported that 4 additional vehicles had been manufactured in this condition, but records showed that they were in the hands of customers."),
  N("INVESTIGATION_START", "The Product Safety and Compliance Committee (PSCC) requested that an investigation be launched to review the potential effect on vehicle operation to ascertain whether this issue would pose any elevated risk to the customers."),
  E("11 September 2026", "OTHER", "On 11 September 2026, the issue was further reviewed at PSCC where the range of possible effects on vehicle operation was reviewed and confirmed to include potential engine stall without warning."),
  N("OTHER", "The matter was referred to the PSCC Decision Forum."),
  E("16 September 2026", "DECISION", "On 16 September 2026, the PSCC Decision Forum agreed that the issue constitutes a safety defect and requested that a safety recall be launched to remedy the affected vehicles."),
 ]})

# 26V617
r = "On July 13, 2026, and July 30, 2026, Altec received reports from vehicle owners regarding improper operation of the boom stow auto-neutral functionality."
L.append({"file": "RCLRPT-26V617-0141.pdf",
 "claims": [S1("Altec Industies Inc."), S2s("Altec", r)],
 "cause": CNR, "upstream": UNONE,
 "events": [
  E("July 13, 2026", "FILER_AWARENESS", r),
  E("July 30, 2026", "FILER_AWARENESS", r),
  N("INVESTIGATION_START", "Altec opened an 8D investigation to determine the root cause and identify potentially affected units."),
  E("August 10, 2026", "INVESTIGATION_START", "On August 10, 2026, Altec initiated a potential field action investigation after the 8D indicated that additional units in the field may have the same condition."),
  N("OTHER", "The investigation evaluated the reported condition, identified units that could be affected, and reviewed production records to determine other owners with units equipped with the same functionality."),
  E("September 25, 2026", "DECISION", "On September 25, 2026, after reviewing the investigation results, Altec determined that a field campaign was necessary to address affected units in the field."),
 ]})

# 26V638
msup = "MBAG forwarded the components to the supplier for detailed technical analysis and testing."
L.append({"file": "RCLRPT-26V638-9238.pdf",
 "claims": [S1("Continental Automotive Technologies GmbH"), S2i(msup, "chronology")],
 "cause": C("SUPPORTED", "Affected brake hoses might not meet durability specifications as a result of accumulated material fatigue due to increased thermal and mechanical stresses sustained over the vehicle’s lifetime."),
 "upstream": UU(msup),
 "events": [
  E("February 24, 2025", "NHTSA_FILING", "This recall expands upon the vehicle population subject to Recall No. 25V116, filed on February 24, 2025."),
  N("OTHER", "Based on the field information and technical evidence then available, MBAG had identified two factors associated with the condition: climatic exposure and a particular vehicle production period."),
  N("OTHER", "MBAG therefore defined the original recall population using those factors."),
  N("OTHER", "Following the decision to conduct a recall, MBAG continued monitoring field performance of the front brake hoses, including vehicles both within and outside the original recall population."),
  E("March and August 2025", "FILER_AWARENESS", "Between March and August 2025, MBAG received additional field reports from markets outside the United States involving vehicles produced outside the original recall production range"),
  N("OTHER", "These reports presented information that was not reflected in the data available when the original recall population was determined and prompted MBAG to reassess whether the condition might extend beyond the originally identified production period and climatic regions."),
  E("September and October 2025", "INVESTIGATION_START", "During September and October 2025, MBAG reviewed the additional reports and available vehicle and production information to determine the appropriate means of obtaining and analyzing representative field parts."),
  E("November 2025", "INVESTIGATION_START", "In November 2025, MBAG began coordinating a dedicated Field Engineering Activity to obtain additional brake hoses from vehicles exhibiting the reported condition."),
  E("November 2025", "OTHER", "From November 2025 through February 2026, MBAG identified candidate vehicles and markets, developed the collection protocol, and coordinated the retrieval and shipment of the requested components."),
  E("March 2026", "INVESTIGATION_START", "The Field Engineering Activity was formally launched in March 2026."),
  E("June 2026", "OTHER", "By June 2026, the requested brake hose components had been collected and returned to MBAG."),
  N("INVESTIGATION_START", msup),
  E("July 2026", "OTHER", "In July 2026, MBAG reviewed and discussed the results of the supplier’s laboratory and durability testing for the retrieved field parts."),
  N("OTHER", "Based on the additional field reports, the analysis of the retrieved components, and the resulting laboratory and durability testing, MBAG reassessed the affected vehicle population with respect to production range and climatic restrictions."),
  N("OTHER", "As a result, MBAG identified an expanded vehicle scope covering vehicles produced up to the implementation of a modified brake hose design in series production."),
  N("OTHER", "MBAG subsequently identified the potentially affected vehicles in the field."),
  E("September 25, 2026", "DECISION", "On September 25, 2026, MBAG determined that a potential safety risk cannot be ruled out for the expanded vehicle population and decided to expand the recall."),
 ]})

# 26V644
nf = "Sep-2026; New Flyer began investigating the affected program and checking other similar programs to see if an ignition condition was required for hazard lamp tell-tale indicators to illuminate."
L.append({"file": "RCLRPT-26V644-1013.pdf",
 "claims": [S1("New Flyer"), S2s("New Flyer", nf)],
 "cause": C("SUPPORTED", "A program error."),
 "upstream": UNONE,
 "events": [
  E("Late Aug-2026", "FILER_AWARENESS", "Late Aug-2026, a USA based customer noticed the hazard lamp indicators did not operate with the MRS (Master Run Switch) in the off position, which varied from their previous buses."),
  E("Sep-2026", "INVESTIGATION_START", nf),
  E("16-Sep-2026", "OTHER", "16-Sep-2026 the issue was briefly discussed during the Vehicle Safety Committee Meeting while the engineering analysis continued."),
  E("24-Sep-2026", "OTHER", "24-Sep-2026 documentation indicated an error in programming on certain buses."),
  E("28-Sep-2026", "DECISION", "28-Sep-2026 the Vehicle Safety Committee was provided with the information, and concurred a noncompliance recall was warranted"),
 ]})

# 26V651
L.append({"file": "RCLRPT-26V651-6989.pdf",
 "claims": [S1("KOSTAL OF AMERICA, INC"), S2i("Name: KOSTAL OF AMERICA, INC", "block")],
 "cause": CNR, "upstream": UNONE,
 "events": [
  E("April 10, 2026", "DECISION", "On April 10, 2026, the FCA US LLC (\"FCA US\") determined, through the Vehicle Regulations Committee, that a safety defect exists in certain vehicles resulting in recall NHTSA ID 26V- 227/FCA US ID 36D (\"36D\")."),
  E("July 20, 2026", "INVESTIGATION_START", "On July 20, 2026, the FCA US Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into some 2026MY Ram 2500 vehicles potentially built with a suspect SCCM outside the scope of 36D due to continuous monitoring."),
  E("July 2026", "INVESTIGATION_START", "From July 2026, through September 2026, FCA US TSRC conducted an analysis of field records and customer assistance records to understand potential customer consequences."),
  E("September 2, 2026", "OTHER", "On September 2, 2026, the FCA US TSRC organization recognized a vehicle build issue existed on certain vehicles related to a condition potentially resulting in a noncompliance with FMVSS No. 126."),
  E("September 29, 2026", "DECISION", "On September 29, 2026, FCA US determined, through the Vehicle Regulations Committee, that a noncompliance to FMVSS No. 126 exists in certain vehicles."),
 ]})

# 26V671
vs = "Based on this, Volvo together with the supplier, initiated internal investigations to assess the reported information, evaluation of the existing attachment design and consideration of measures to improve its robustness."
vd = "On 30 September 2026, the concern was classified as critical, and on 07 October 2026 Volvo Cars decided to prepare a recall after determining that the condition could increase the risk to motor vehicle safety."
L.append({"file": "RCLRPT-26V671-6336.pdf",
 "claims": [S1("Magna Seating Baoji"), S2i(vs, "chronology")],
 "cause": C("SUPPORTED", "Volvo Cars investigations have identified that the head restraint cushion may under certain circumstances, such as very high speed in combination with multiple direction impacts, detach due to insufficient fastening."),
 "upstream": UU(vs),
 "events": [
  E("September 2025", "FILER_AWARENESS", "Volvo Cars received in September 2025 information concerning a potential issue with the head restraint cushion attachment."),
  N("INVESTIGATION_START", vs),
  N("INVESTIGATION_START", "The matter was subsequently escalated through the Critical Concern Action Process (CCAP), where a technical investigation and risk assessment were conducted."),
  E("30 September 2026", "OTHER", vd),
  E("07 October 2026", "DECISION", vd),
 ]})

# ---------- verification ----------
def norm(s): return re.sub(r"\s+", " ", s).strip()
def sections(path):
    t = open(path, encoding="utf-8").read()
    b = t.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    c = t.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    h = t.split("=== CHRONOLOGY ===")[1]
    fl = t.splitlines()[0].replace("FILE: ", "").strip()
    return fl, {"block": norm(b), "cause": norm(c), "chronology": norm(h)}

errs = []
byfile = {}
for fn in sorted(os.listdir(os.path.join(D, "texts"))):
    if fn.startswith("._") or not fn.endswith(".txt"): continue
    fl, s = sections(os.path.join(D, "texts", fn)); byfile[fl] = s
assert len(L) == 25 and set(x["file"] for x in L) == set(byfile), (len(L), set(byfile) ^ set(x["file"] for x in L))
def chk(f, q, sec, what):
    if not q: return
    if len(q) > 300: errs.append((f, what, "too long", len(q)))
    if norm(q) not in byfile[f][sec]: errs.append((f, what, "not found in " + sec, q))
for x in L:
    f = x["file"]
    for c in x["claims"]: chk(f, c["quote"], c["section"], c["id"])
    chk(f, x["cause"]["quote"], x["cause"]["section"], "cause")
    chk(f, x["upstream"]["quote"], x["upstream"]["section"], "upstream")
    for i, e in enumerate(x["events"]):
        chk(f, e["quote"], "chronology", "ev%d" % i)
        if e["inherited_date"]:
            chk(f, e["entry_quote"], "chronology", "ev%d-entry" % i)
            if e["date_text"] not in e["entry_quote"]: errs.append((f, i, "date not in entry_quote"))
        elif not e["date_inferred"]:
            if e["date_text"] not in e["quote"]: errs.append((f, i, "date not in quote"))
for e in errs: print(e)
print("errors:", len(errs), "events:", sum(len(x["events"]) for x in L))
if not errs:
    with open(os.path.join(D, "passB.json"), "w", encoding="utf-8") as fh:
        json.dump(L, fh, ensure_ascii=False, indent=1)
    print("written")
