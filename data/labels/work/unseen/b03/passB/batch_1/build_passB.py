import json, os, re
D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")

def E(date, typ, quote, inh=None, inf=False):
    e = {"date_text": date, "type": typ, "quote": quote, "inherited_date": bool(inh)}
    if inh:
        e["entry_quote"] = inh
    e["date_inferred"] = inf
    return e

def I(typ, quote):
    return E("", typ, quote, None, True)

def S1(q):
    if q is None:
        return {"id": "S1", "status": "NOT_REPORTED", "quote": "", "section": "block"}
    st = "NOT_REPORTED" if q.strip().endswith(("NR", "N/A")) else "SUPPORTED"
    return {"id": "S1", "status": st, "quote": q, "section": "block"}

def S2(st, q="", sec="chronology", name=None):
    d = {"id": "S2", "status": st}
    if name:
        d["name"] = name
    d["quote"] = q
    d["section"] = sec
    return d

def C(st, q, sec="cause"):
    return {"status": st, "quote": q, "section": sec}

def U(kind, q="", sec="chronology", names=None):
    return {"kind": kind, "names": names or [], "quote": q, "section": sec}

L = []
def add(fname, s1, s2, c, u, ev):
    L.append({"txt": fname, "claims": [s1, s2], "cause": c, "upstream": u, "events": ev})

# 1
q1 = "In early October 2023, Weldon was notified that eternal wiring in a vehicle using the node had melted."
add("RCLRPT-24V347-4177.txt", S1("Name : Weldon Division of Akron Brass"),
    S2("SUPPORTED", q1, name="Weldon"), C("NOT_REPORTED", "NR"), U("NAMED", q1, names=["Weldon"]), [
    E("early October 2023", "OTHER", q1),
    E("mid-October", "INVESTIGATION_START", "the part was returned to Weldon for analysis in mid-October where it was found that when an external short circuit occurred, the electrical output did not shut down as specified."),
    I("INVESTIGATION_START", "Weldon conducted testing and analysis of the version of the node used in the vehicle as well as prior versions of the node and it was found that for the version of the node installed on the vehicle, the electrical current sensing calibration was outside the specified limits."),
    I("OTHER", "Weldon found that the calibration was previously updated in production but was not considered to pose a broader concern at the time."),
    E("October 24, 2023", "DECISION", "On October 24, 2023, Weldon decided to conduct a safety recall to address the issue."),
])
# 2
q2 = "Root cause is not confirmed; however, supplier deviation in the manufacturing of the safety plug’s Female-Female terminal is suspected."
add("RCLRPT-24V358-2557.txt", S1("Name : KET"), S2("INSUFFICIENT", q2, "cause"),
    C("INSUFFICIENT", q2), U("UNNAMED", q2, "cause"), [])
# 3
add("RCLRPT-24V379-7287.txt", S1("Name : NR"), S2("NOT_REPORTED", "", ""),
    C("SUPPORTED", "The headlamp turn indicator functions intermittently due to an issue detected on the turn indicator circuit."),
    U("NOT_REPORTED", "See Karma Automotive Supplemental Report to 24-0023809-31063-10 uploaded June 5, 2024."), [])
# 4
q4 = "4/29/2024 - Suburban notified Host Industries Inc. Compliance by email of their equipment recall 24E-028 that they filed with NHTSA regarding certain slide in range models that contain Red LED backlight knobs that we purchased affected by their equipment recall 24E-028."
add("RCLRPT-24V389-8924.txt", S1("Name : Suburban Manufacturing"), S2("SUPPORTED", q4, name="Suburban"),
    C("SUPPORTED", "The PCBs did not have the correct amount of conformal coating to properly seal the circuit board from contamination."),
    U("NAMED", q4, names=["Suburban"]), [
    E("4/29/2024", "SUPPLIER_NOTICE", q4),
    E("5/23/24", "FILER_AWARENESS", "5/23/24 - NHTSA had informed us of recall."),
    E("5/29/24", "INVESTIGATION_START", "5/29/24 - The warranty department and management had discussed the incident and had started an investigation on which customers were affected."),
    E("5/31/24", "NHTSA_FILING", "5/31/24 Host had started and submitted form 573 to NHTSA"),
])
# 5
add("RCLRPT-24V429-7759.txt", S1("Name : NR"), S2("NOT_REPORTED", "", ""), C("NOT_REPORTED", "NR"),
    U("NOT_REPORTED", "SEE ATTACHED CHRONOLOGY 05-1584 - 6.10.24"), [])
# 6
e6 = "January 11, 2024 to June 2024: Investigation into potential causes of loss of high-voltage distribution."
e6b = "June 14, 2024: Confirmation that the misalignment of the CAN connector increases the risk of water infiltration into the CAN connector and represents a defect with respect to the Motor Vehicle Safety Regulations."
add("RCLRPT-24V460-2667.txt", S1("Name : NR"), S2("NOT_REPORTED", "", ""), C("NOT_REPORTED", "NR"),
    U("NONE_MENTIONED", ""), [
    E("January 11, 2024", "FILER_AWARENESS", "January 11, 2024: Reported loss of high-voltage distribution on a LionC in the state of Maine."),
    E("January 11, 2024", "INVESTIGATION_START", e6),
    E("January 11, 2024", "INVESTIGATION_START", "Inspection of vehicles in the state of Maine.", e6),
    E("June 14, 2024", "DECISION", e6b),
    E("June 14, 2024", "DECISION", "Recall proposal approved by Lion Electric's safety committee.", e6b),
])
# 7
q7 = "On May 2, Webasto provided preliminary results from their analysis, which indicated approximately 82% of failed HVCH examined were delaminations."
add("RCLRPT-24V495-3479.txt", S1("Name : Webasto Thermo & Comfort SE"), S2("SUPPORTED", q7, name="Webasto"),
    C("SUPPORTED", "HVCH manufactured by Supplier prior to February 2023 have an unreasonable risk of delamination failure."),
    U("NAMED", q7, names=["Webasto"]), [
    E("January 10, 2024", "OTHER", "Since just before filing of Lucid’s recall report for 24V-011 on January 10, 2024, Lucid has monitored HVCH failures via vehicle telemetry."),
    E("April 17", "INVESTIGATION_START", "On or about April 17, Lucid shipped 98 failed HVCH to Supplier for additional analysis to determine the failure mode, delamination or otherwise, and whether any HVCH outside the 24V-011 population had experienced delamination failures."),
    E("May 2", "SUPPLIER_NOTICE", q7),
    I("INVESTIGATION_START", "Lucid’s Product Safety Working Group (PSWG) examined the failures detected via telemetry, Lucid internal analysis and analysis of data from Supplier, and vehicle production and service records."),
    E("June 20", "DECISION", "Based on recommendation of the PSWG on June 20, Lucid’s Product Safety Executive Council (PSEC) determined that, in addition to the 24V-011 population, an unreasonable risk to safety exists for all vehicles with HVCH manufactured from July 2022 to Feb. 2023"),
])
# 8
e8 = "March 2024 to June 2024: Volvo Bus initiated a field survey in Mexico on vehicles outside the recall 24V083 population to further corroborate its scope."
e8b = "2024-06-25 Case was presented on Volvo Product Safety Evaluation Committee (PSEC) to evaluate if there is a potential safety-related issue."
e8c = "2024-07-04 Case was presented to Volvo Product Safety Committee (PSC)."
add("RCLRPT-24V524-5942.txt", S1("Name : NR"), S2("NOT_REPORTED", "", ""),
    C("SUPPORTED", "During the vehicle manufacturing, castellated nuts securing the link rod to the steering arm and/or the pitman arm may not have been properly torqued by Volvo."),
    U("NONE_MENTIONED", ""), [
    E("March 2024", "INVESTIGATION_START", e8),
    E("March 2024", "FILER_AWARENESS", "During this field survey, improperly torqued castle nuts were identified on certain vehicles, but no missing cotter pins were identified.", e8),
    E("June 2024", "INVESTIGATION_START", "June 2024: Field survey results were analyzed by Volvo Bus Product Safety Office."),
    E("2024-06-25", "OTHER", e8b),
    E("2024-06-25", "OTHER", "Decision made to raise the potential safety issue to Volvo Product Safety Committee (PSC) for review and determination.", e8b),
    E("2024-07-04", "OTHER", e8c),
    E("2024-07-04", "DECISION", "It was concluded that there was a safety-related issue and that a recall is needed.", e8c),
    E("2024-07-04", "DECISION", "Given that an improperly torqued castle nut secured by a cotter pin poses a different safety risk compared to an improperly torqued caste nut without a cotter pin, Volvo Bus opted to initiate a new recall instead of expending the recall scope of 24V083.", e8c),
    E("2024-07-09", "NHTSA_FILING", "2024-07-09 Defect Information Report submitted to authorities."),
])
# 9
add("RCLRPT-24V620-8075.txt", S1("Name : NR"), S2("NOT_REPORTED", "", ""),
    C("SUPPORTED", "Apparently, in the process, the air tank size was decreased and the minimum required capacity was overlooked making it noncompliant."),
    U("NONE_MENTIONED", ""), [
    E("January 2016", "OTHER", "In January 2016, after 3rd party testing and receiving a 'pass', one of the air tanks was relocated."),
    I("OTHER", "In the process, the air tank size was decreased and the minimum required capacity was overlooked."),
    E("2019", "OTHER", "In 2019, when federal requirements for stability control (FMVSS 136) went into effect, Kalmar decided to limit the maximum speed of the vehicle to less than 33mph, thus exempting it from federal requirements for ABS and Stability Control."),
    I("FILER_AWARENESS", "In some recent design changes, air volume was recalculated to determine required capacity and it was determined that existing trucks were insufficient, not meeting the regulatory requirement."),
    E("August 7, 2024", "DECISION", "Thus, leading to the decision on August 7, 2024 to issue a non-compliance recall."),
])
# 10
add("RCLRPT-24V647-3002.txt", S1("Name: RECARO Automotive North America, Inc."),
    S2("INSUFFICIENT", "Name: RECARO Automotive North America, Inc.", "block"),
    C("SUPPORTED", "Recline limitation stopping device does not in all cases stop the seat inclination at the correct angle."),
    U("NONE_MENTIONED", ""), [
    E("May 17, 2023", "NHTSA_FILING", "May 17, 2023: Nova Bus submits a vehicle recall report to NHTSA (23V350)"),
    E("May 09, 2024", "FILER_AWARENESS", "May 09, 2024: Nova Bus was informed by a customer regarding a potential ineffective remedy to prevent seat belt pinching."),
    E("May 13, 2024", "INVESTIGATION_START", "May 13, 2024: Nova Bus started an internal Investigation."),
    E("May 17, 2024", "OTHER", "May 17, 2024: The issue was raised to the safety forum as a potential risk for evaluation."),
    E("June 18, 2024", "INVESTIGATION_START", "June 18, 2024: Survey to confirm seat models potentially affected was completed."),
    E("August 22, 2024", "OTHER", "August 22, 2024: Product Safety Evaluation Committee evaluates and raises to Product Safety Committee."),
    E("August 27, 2024", "DECISION", "August 27, 2024: Product Safety Committee determination of product defect."),
    E("September 3, 2024", "NHTSA_FILING", "September 3, 2024: Nova Bus files 573 with NHTSA that a voluntary recall will be released to address the safety-related defect."),
])
# 11
add("RCLRPT-24V670-1290.txt", S1("Name : Trail King Ind."),
    S2("SUPPORTED", "In March 2019, Trail King began production of a new HDG Paver Special gooseneck design that was specially developed to transport paving equipment.", name="Trail King"),
    C("SUPPORTED", "Insufficient reinforcement in the radius of the lower cylinder mount."),
    U("NONE_MENTIONED", ""), [
    E("March 2019", "OTHER", "In March 2019, Trail King began production of a new HDG Paver Special gooseneck design that was specially developed to transport paving equipment."),
    E("September 3, 2020", "FILER_AWARENESS", "On September 3, 2020, Trail King was notified by a customer of a failure in the lower cylinder mount."),
    I("INVESTIGATION_START", "During the review, it was determined that the welds showed signs of fatigue cracking and which appeared to be due to dynamic loading by not having the transport doors in place during specific points during transport to achieve clearance of road obstacles."),
    E("October 2020", "OTHER", "However, reinforcements to the lower cylinder mount were added to new production in October 2020 to reinforce this area."),
    E("February 10, 2021", "FILER_AWARENESS", "On February 10, 2021, Trail King was informed of another failure to the lower cylinder mount on a unit built prior to October 2020 that did not have reinforcements added."),
    I("INVESTIGATION_START", "Trail King reviewed the unit and again indicated the failure was due to dynamic loading by not having the transport doors in place during specific points during transport to achieve clearance of road obstacles."),
    E("August 21, 2024", "FILER_AWARENESS", "On August 21, 2024, Trail King was notified of a failure of the lower cylinder mount area of the gooseneck where the vehicle operator alleged an injury."),
    I("INVESTIGATION_START", "Trail King initiated an investigation into the issue."),
    I("OTHER", "The investigation indicated this unit appeared to have experienced fatigue-related cracks due to the presence of repair welds in the gooseneck."),
    E("September 4, 2024", "DECISION", "Trail King decided to conduct a safety recall to address this issue on September 4, 2024."),
])
# 12
add("RCLRPT-24V701-1046.txt", S1("Name : NR"), S2("NOT_REPORTED", "", ""),
    C("SUPPORTED", "Error during the manual assembly step of the component."), U("NONE_MENTIONED", ""), [
    E("August 28th", "FILER_AWARENESS", "On August 28th during production assembly phase, one working shift reported the bracket 4T0803662 assembled in the wrong vehicle side (left side instead of right side)."),
    I("INVESTIGATION_START", "Lamborghini immediately launched an internal investigation to determine the root cause."),
    I("OTHER", "Results from the investigation revealed a risk that additional number of vehicles may have been produced not according to product specification."),
    E("September 12th", "DECISION", "A compliance assessment was requested and following the results, on September 12th, Lamborghini Product Safety Committee determined that a non-compliance related to motor vehicle safety exists and decided to conduct a voluntary non-compliance recall."),
])
# 13
e13a = "9/25/2024: Motiv received a customer report alleging a loss of power on a Motiv Motiv EPIC4 E-450 vehicle."
e13b = "9/27/2024: Motiv field technicians conducted an inspection of the affected vehicle."
e13c = "9/27 – 10/10/2024: Motiv conducted additional analysis and testing to identify a failure or malfunction that may have led to a reported loss of propulsion."
add("RCLRPT-24V781-6389.txt", S1("Name : NR"), S2("NOT_REPORTED", "", ""),
    C("SUPPORTED", "Cable assembly failure caused by a partially collapsed grid on the connector’s socket that in turn resulted in a loss of connection."),
    U("NONE_MENTIONED", ""), [
    E("9/25/2024", "FILER_AWARENESS", e13a),
    E("9/25/2024", "FILER_AWARENESS", "The customer reported a loss of propulsion while driving.", e13a),
    E("9/25/2024", "INVESTIGATION_START", "Motiv immediately grounded the vehicle and began an investigation of the incident.", e13a),
    E("9/27/2024", "INVESTIGATION_START", e13b),
    E("9/27/2024", "OTHER", "That inspection determined the vehicle had experienced a temporary loss of 12-volt control power to the High Voltage (HV) batteries.", e13b),
    E("9/27", "INVESTIGATION_START", e13c),
    E("9/27", "OTHER", "The investigation determined that a cable assembly failure caused by a partially collapsed grid on the connector’s socket that in turn resulted in a temporary loss of connection – interrupting 12-volt control power to the HV batteries.", e13c),
    E("10/10/2024", "DECISION", "10/10/2024 Based on its investigation and analysis, Motiv concluded that a potential safety risk could not be ruled out and decided to conduct a recall."),
])
# 14
add("RCLRPT-24V844-7354.txt", S1("Name : Pektron SEV"), S2("INSUFFICIENT", "Name : Pektron SEV", "block"),
    C("SUPPORTED", "Instrument Cluster (IC) resistor is degraded over time because of in-rush current."),
    U("NONE_MENTIONED", ""), [
    E("September 23, 2024", "FILER_AWARENESS", "On September 23, 2024 the Nikola Campaign Committee identified 6 reported cases in customer service portal of instrument cluster screens going black for 3 to 5 seconds or permanently in the field from 6/17/24 to 9/16/24 and launched an investigation into root cause and corrective action."),
    E("October 18, 2024", "OTHER", "On October 18, 2024 Nikola Campaign Committee met to discuss field action and referred issue to Vehicle Defects Managers as a potential FMVSS non-compliance."),
    E("October 21, 2024", "OTHER", "On October 21, 2024 Nikola Vehicle Defects Managers met and referred issue to Vehicle Defects Technical Team for consideration of a recall."),
    E("October 23, 2024", "OTHER", "On October 23, 2024 Nikola Vehicle Defects Technical Team recommend recall to Vehicle Defects Committee."),
    E("October 31, 2024", "DECISION", "On October 31, 2024 Nikola Vehicle Defects Committee voted to issue a voluntary recall to replace all affected instrument clusters."),
])
# 15
q15 = "BRV Safety Committee met on 11/18/24 and determined that if the Lippert investigation indicated the need for a voluntary recall, that BRV would issue a parallel recall for the affected population."
add("RCLRPT-24V885-4062.txt", S1("Name : Lippert Components"), S2("SUPPORTED", q15, name="Lippert"),
    C("SUPPORTED", "The fasteners used to assemble the Helux Pin Box may not have been properly torqued."),
    U("NAMED", q15, names=["Lippert"]), [
    E("11/14/24", "SUPPLIER_NOTICE", "On 11/14/24, Brinkley RV (BRV) was notified by the chassis/pin box supplier of an open investigation regarding pin box torque."),
    I("OTHER", "Material was put on hold and inspected/corrected as necessary."),
    E("11/18/24", "OTHER", q15),
    E("11/21/24", "SUPPLIER_NOTICE", "On 11/21/24, Lippert formally notified BRV that a voluntary recall is being issued."),
    E("11/22/24", "DECISION", "The corresponding BRV recall is being initiated on 11/22/24."),
])
# 16
q16 = "We found that other RV manufacturers were using a rubber hose in that area also but after investigating with the manufacturer of the hose that the hose was not rated for the heat in the cooktop"
add("RCLRPT-24V931-9261.txt", S1("Name : NR"), S2("INSUFFICIENT", q16), C("NOT_REPORTED", "NR"),
    U("UNNAMED", q16), [
    E("August 12th 2024", "FILER_AWARENESS", "On August 12th 2024, i was notified by our production team that they felt the rubber LP line inside the cooktop was not adequate for the application we were using on the cooktop which could cause a failure in the hose and cause a fire."),
    I("INVESTIGATION_START", q16),
])
# 17
add("RCLRPT-24V933-4637.txt", S1("Name : Ashimori Korea., LTD"), S2("INSUFFICIENT", "Name : Ashimori Korea., LTD", "block"),
    C("NOT_REPORTED", "NR"), U("NONE_MENTIONED", ""), [
    E("June 14, 2024", "OTHER", "On June 14, 2024, NHTSA conducted a dynamic side impact compliance test on a 2024 VinFast VF 8 with VIN: RLLV1AEBXRH006590."),
    I("OTHER", "During the test, NHTSA observed that the deploying Center Air Bag contacted the test dummy’s arm."),
    E("July 10th, 2024", "FILER_AWARENESS", "NHTSA then sent an inquiry to VinFast on July 10th, 2024, seeking an explanation of this anomaly."),
    E("December 16th, 2024", "DECISION", "VinFast conducted an investigation which concluded on December 16th, 2024, resulting in the filing decision on the same date."),
])
# 18
q18 = "2024-12-05 Polestar was notified by its supplier that they had found a potentially critical issue with the far- side airbag (FSAB)."
add("RCLRPT-24V939-5483.txt", S1("Name : Joyson Safety Systems Sachsen GmbH"), S2("INSUFFICIENT", q18),
    C("SUPPORTED", "Missed crimping process for airbag during subassembly from supplier due to human error, that was not identified due to wrong software control parameters in assembly process."),
    U("UNNAMED", q18), [
    E("2024-12-13", "OTHER", "Condition considered as a critical concern by Critical Concern Management Team 2024-12-13"),
    E("2024-12-18", "DECISION", "Field Service Action decision confirmed by Polestar 2024-12-18"),
    E("2024-12-05", "SUPPLIER_NOTICE", q18),
    E("2024-12-05", "INVESTIGATION_START", "The investigation was escalated through the Critical Concern Action Process (CCAP).", q18),
    E("2024-12-11", "INVESTIGATION_START", "On 2024-12-11, the issue was concluded as potentially critical and the Critical Concern Management Team (CCMT) initiated a technical investigation to conclude customer symptom, risk assessment, testing, root cause etc."),
    E("2024-12-13", "DECISION", "On 2024-12-13 the technical investigation was complete, the CCMT team took the decision to start the preparation of a recall as it was judged as an increased risk towards motor vehicle safety."),
])
# 19
q19 = "2024-12-04 Polestar was notified by its supplier that they had found 6 (in the US) vehicles with diagnostic trouble codes set indicating that the high to low voltage converter module (HLCM) is not working properly."
add("RCLRPT-24V940-8922.txt", S1("Name : Lear Corporation Holding"), S2("INSUFFICIENT", q19),
    C("SUPPORTED", "Voltage fluctuations on the 12V system damaging one of the HLCM phases during Software Upgrade."),
    U("UNNAMED", q19), [
    E("2024-12-16", "OTHER", "Condition considered as a critical concern by Critical Concern Management Team 2024-12-16"),
    E("2024-12-18", "DECISION", "Field Service Action decision confirmed by Polestar 2024-12-18"),
    E("2024-12-04", "SUPPLIER_NOTICE", q19),
    E("2024-12-04", "INVESTIGATION_START", "The investigation was escalated through the Critical Concern Action Process (CCAP).", q19),
    E("2024-12-04", "OTHER", "We connected customer symptoms reported from the market with the diagnostic trouble codes identified by our supplier.", q19),
    E("2024-12-11", "INVESTIGATION_START", "On 2024-12-11, the issue was concluded as potentially critical and the Critical Concern Management Team (CCMT) initiated a technical investigation to conclude customer symptom, risk assessment, root cause etc."),
    E("2024-12-16", "DECISION", "On 2024-12-16 the technical investigation was complete, the CCMT team took the decision to start the preparation of a recall as it was judged as an increased risk towards motor vehicle safety."),
])
# 20
add("RCLRPT-24V964-8436.txt", S1(None), S2("NOT_REPORTED", "", ""),
    C("SUPPORTED", "Orange EV did not properly conduct a visibility assessment after offering frame extenders as an option."),
    U("NOT_REPORTED", "Please see the attached Part 573 Defect Information Report for the full chronology."), [])
# 21
q21 = "The current analysis seems to indicate that variability in the battery cell supplier’s production process may result in the cell’s cathode inducing micro-defects and/or local stresses in the cell’s separator layer."
add("RCLRPT-25E007-3917.txt", S1("Name : NR"), S2("INSUFFICIENT", q21, "cause"),
    C("INSUFFICIENT", "VWGoA recall - The root cause is still under investigation."),
    U("UNNAMED", q21, "cause"), [])
# 22
q22 = "Jan 30 Internal testing at Firefly Integrations found possible awning program issue."
add("RCLRPT-25E009-8553.txt", S1("Name : Firefly Integrations"), S2("SUPPORTED", q22, name="Firefly Integrations"),
    C("SUPPORTED", "It has been identified that there was a programming issue which would allow a user to deploy their awning when they should be locked out."),
    U("NONE_MENTIONED", ""), [
    E("Jan 30", "FILER_AWARENESS", q22),
    E("Jan 31", "OTHER", "Jan 31 Issue was confirmed, and programming update began."),
    E("Jan 31", "OTHER", "Jan 31 Firefly Integrations communicated with Thor engineering about the confirmed issues."),
    E("Feb 3", "OTHER", "Feb 3 Firefly Integrations notified Thor Motor Coach compliance of the issue."),
])
# 23
add("RCLRPT-25E024-9877.txt", S1("Name : NR"), S2("NOT_REPORTED", "", ""), C("NOT_REPORTED", "NR"),
    U("NOT_REPORTED", "See Miscellaneous Document"), [])
# 24
q24 = "As a result of the supplier’s modification to its machining process, the overall detent depth for the diaphragm was reduced and the chamfer was removed, allowing for a potential pinch point on the diaphragm."
e24 = "3/12/25: A new customer complaint was received, and a Quality Audit Request was initiated."
add("RCLRPT-25E036-8756.txt", S1("Name: Accauto Co., LTD"), S2("INSUFFICIENT", q24, "cause"),
    C("SUPPORTED", q24), U("UNNAMED", q24, "cause"), [
    E("2/10/25", "FILER_AWARENESS", "2/10/25: Following receipt of a report of a leaking pressure regulator from a customer, 20 units were pulled from Holley inventory and tested at 80 PSI dead head with no failures."),
    E("3/12/25", "FILER_AWARENESS", e24),
    E("3/12/25", "INVESTIGATION_START", "Additional samples were pulled for evaluation.", e24),
    E("3/13/25", "INVESTIGATION_START", "3/13/25 – 5/8/25: Holley conducted a product investigation to evaluate the issue, including a comparison of the subject products to similar products sourced from a different supplier which showed visually different diaphragms, testing and teardowns of sample products"),
    E("5/9/25", "DECISION", "5/9/25: Based upon the results of the investigation, Holley decided to initiate a safety recall to address this condition."),
])
# 25
q25 = "The Zoox Safety Committee met on May 19 and 21, 2025 and after final analysis and review of all the facts, made a determination to voluntarily and proactively submit this Part 573 notification for the remedied software."
add("RCLRPT-25E037-4912.txt", S1(None), S2("NOT_REPORTED", "", ""),
    C("SUPPORTED", "At speeds less than 0.5 m/s the Zoox vehicle may not detect the presence of a prone VRU at certain locations immediately adjacent to the vehicle."),
    U("NONE_MENTIONED", ""), [
    E("May 8, 2025", "FILER_AWARENESS", "On May 8, 2025, in San Francisco, CA, an unoccupied stopped Zoox robotaxi operating in autonomy was struck by an e-scooterist."),
    I("OTHER", "The e-scooterist fell to the ground directly next to the vehicle."),
    I("OTHER", "The robotaxi then started to move, but did not make contact with the fallen e-scooterist."),
    I("OTHER", "Minor injuries related to the initial collision were reported."),
    I("OTHER", "Zoox paused all driverless vehicle operations across all geofences to conduct an internal review."),
    E("May 8, 2025", "INVESTIGATION_START", "Between May 8, 2025 and May 15, 2025, Zoox confirmed the root cause, implemented a software update, and conducted simulation and testing with both robotaxis and drivered, retrofitted test vehicles."),
    E("May 9, 2025", "OTHER", "On May 9, 2025, Zoox reported the incident to NHTSA in accordance with the Standing General Order (SGO Report 30610-10711) and offered a heads-up call to NHTSA."),
    E("May 13, 2025", "OTHER", "Zoox met several times with NHTSA to discuss the SGO submission and answered additional questions between May 13, 2025 and May 21, 2025."),
    E("May 15, 2025", "OTHER", "Between May 15, 2025 and May 20, 2025, Zoox verified the software update through the safety clearance process."),
    I("OTHER", "Following confirmation of the deployment of the updated software, operations resumed in all geofences."),
    E("May 19", "OTHER", q25),
    E("21, 2025", "DECISION", q25),
])

# ---- build + verify ----
norm = lambda s: re.sub(r"\s+", " ", s).strip()
def sections(path):
    raw = open(path, encoding="utf-8").read()
    fl = re.search(r"^FILE:\s*(\S+)", raw, re.M).group(1)
    blk = raw.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    cau = raw.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    chr_ = raw.split("=== CHRONOLOGY ===")[1]
    return fl, {"block": norm(blk), "cause": norm(cau), "chronology": norm(chr_)}

out, errs = [], []
for o in L:
    fl, sec = sections(os.path.join(T, o["txt"]))
    def chk(q, s, tag):
        if not q:
            return
        if len(q) > 300: errs.append((fl, tag, "len", len(q)))
        if norm(q) not in sec.get(s, ""): errs.append((fl, tag, "notfound", q[:80]))
    for c in o["claims"]: chk(c["quote"], c["section"], c["id"])
    chk(o["cause"]["quote"], o["cause"]["section"], "C")
    chk(o["upstream"]["quote"], o["upstream"]["section"], "U")
    for i, e in enumerate(o["events"]):
        chk(e["quote"], "chronology", f"ev{i}")
        if e.get("entry_quote"):
            chk(e["entry_quote"], "chronology", f"ev{i}entry")
            if e["date_text"] not in e["entry_quote"]: errs.append((fl, i, "date not in entry"))
        elif e["date_text"] and e["date_text"] not in e["quote"]:
            errs.append((fl, i, "date not in quote"))
    out.append({"file": fl, "claims": o["claims"], "cause": o["cause"], "upstream": o["upstream"], "events": o["events"]})

print("ERRORS:", errs)
with open(os.path.join(D, "passB.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
