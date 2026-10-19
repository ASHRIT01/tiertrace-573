import json, os, re

D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def sections(path):
    txt = open(path, encoding="utf-8").read()
    fl = re.search(r"^FILE: (.+)$", txt, re.M).group(1).strip()
    b = txt.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    c = txt.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    ch = txt.split("=== CHRONOLOGY ===")[1]
    return fl, {"block": norm(b), "cause": norm(c), "chronology": norm(ch)}

def S1(q):
    return {"id": "S1", "status": "SUPPORTED", "quote": q, "section": "block"}
def S1NR(q=""):
    return {"id": "S1", "status": "NOT_REPORTED", "quote": q, "section": "block"}
def S2(status, q="", sec="chronology", name=None):
    d = {"id": "S2", "status": status}
    if name: d["name"] = name
    d["quote"] = q; d["section"] = sec if q else ""
    return d
def C(status, q=""):
    return {"status": status, "quote": q, "section": "cause"}
def U(kind, q="", sec="chronology", names=None):
    d = {"kind": kind}
    if kind == "NAMED": d["names"] = names
    d["quote"] = q; d["section"] = sec if q else ""
    return d
def E(dt, ty, q):
    return {"date_text": dt, "type": ty, "quote": q, "inherited_date": False, "date_inferred": False}
def I(dt, ty, q, eq):
    return {"date_text": dt, "type": ty, "quote": q, "inherited_date": True, "entry_quote": eq, "date_inferred": False}
def N(ty, q):
    return {"date_text": "", "type": ty, "quote": q, "inherited_date": False, "date_inferred": True}

L = {}

# 25V690 Tesla
L["RCLRPT-25V690-8658.txt"] = dict(
 claims=[S1("Name: Sistemas Mecatrónicos InTiCa S.A.P.I."),
         S2("INSUFFICIENT", "Name: Sistemas Mecatrónicos InTiCa S.A.P.I.", "block")],
 cause=C("NOT_REPORTED"), upstream=U("NONE_MENTIONED"),
 events=[
  E("August 8, 2025", "INVESTIGATION_START", "On August 8, 2025, Tesla’s Field Reliability team began investigating incidents identified through service records in which Tesla vehicles were unable to enter drive from a park condition and high coil resistance was found on the pack contactors resulting in contactor replacements."),
  E("August 8, 2025, through September 26, 2025", "INVESTIGATION_START", "From August 8, 2025, through September 26, 2025, Tesla recovered pack contactors from the field and completed a detailed failure analysis."),
  E("September 29, 2025, through October 2, 2025", "INVESTIGATION_START", "From September 29, 2025, through October 2, 2025, Tesla reviewed the failure analysis results, repair, and production records."),
  E("October 3, 2025", "DECISION", "On October 3, 2025, having completed the investigation and identified the scope of affected vehicles, Tesla made a determination to voluntarily recall the affected vehicles."),
 ])

# 25V702 International
e1 = "08/15/2025 A bus chassis that would not shift into reverse is identified at the Tulsa Bus Plant."
e2 = "08/18/2025 After identifying additional bus chassis that would not shift into reverse, International notifies Curtiss-Wright of the issue."
L["RCLRPT-25V702-0345.txt"] = dict(
 claims=[S1("Name: Curtiss-Wright"),
         S2("SUPPORTED", "After identifying additional bus chassis that would not shift into reverse, International notifies Curtiss-Wright of the issue.", name="Curtiss-Wright")],
 cause=C("NOT_REPORTED"),
 upstream=U("NAMED", "After identifying additional bus chassis that would not shift into reverse, International notifies Curtiss-Wright of the issue.", names=["Curtiss-Wright"]),
 events=[
  E("08/15/2025", "FILER_AWARENESS", e1),
  I("08/15/2025", "INVESTIGATION_START", "International begins a limited inspection of other bus chassis to determine if the same issue is present.", e1),
  E("08/18/2025", "OTHER", e2),
  I("08/18/2025", "OTHER", "Curtiss-Wright requests the suspect shift actuators be returned to them for further investigation.", e2),
  E("08/19/2025-09/17/2025", "INVESTIGATION_START", "08/19/2025-09/17/2025 Curtiss-Wright completes its inspection of 10 suspect shift actuators returned by International, finding there was unexpected variation in the neutral set point of the actuator that could contribute to a vehicle not being able to shift into reverse."),
  E("09/18/2025", "OTHER", "09/18/2025 International initiates a delivery stop at the Tulsa Bus Plant, establishing the clean point."),
  E("09/18/2025-10/02/2025", "SUPPLIER_NOTICE", "09/18/2025-10/02/2025 Curtiss-Wright continues its investigation into the issue and determines that the actuator’s input shaft was updated from powdered metal to cut steel which allowed a backlash to occur during the calibration process."),
  E("10/09/2025", "OTHER", "10/09/2025 – International finalizes the suspect population."),
  E("10/09/2025", "DECISION", "10/09/2025 – International declares a safety recall."),
 ])

# 25V706 Alexis
ej = "July 1 – August 8, 2025 – Supplier started corrective action request to determine root cause, started cycle testing on door frames, and contained internal inventory."
L["RCLRPT-25V706-1572.txt"] = dict(
 claims=[S1("Name: TriMark Corporation"),
         S2("SUPPORTED", "May 1, 2025 – Spartan Fire Chassis (Spartan) received claim of a cab door latch logic issue.", name="Spartan Fire Chassis")],
 cause=C("SUPPORTED", "The cause of the potential failure was a progressive die made the incorrect length of lever arm."),
 upstream=U("NAMED", "May 1, 2025 – Spartan Fire Chassis (Spartan) received claim of a cab door latch logic issue.", names=["Spartan Fire Chassis"]),
 events=[
  E("May 1, 2025", "OTHER", "May 1, 2025 – Spartan Fire Chassis (Spartan) received claim of a cab door latch logic issue."),
  E("May 5, 2025", "OTHER", "May 5, 2025 – Spartan notified supplier of issue."),
  E("May 19, 2025", "INVESTIGATION_START", "May 19, 2025 – Spartan received parts from field and started internal investigation with Engineering and Supplier."),
  E("June 19, 2025", "OTHER", "June 19, 2025 – Spartan shipped returned parts back to Supplier."),
  E("June 24, 2025", "OTHER", "June 24, 2025 – Supplier received parts from Spartan."),
  E("July 1 – August 8, 2025", "INVESTIGATION_START", ej),
  I("July 1 – August 8, 2025", "OTHER", "Spartan opened PSR, issued SCAR with Supplier, reviewed chassis cab production inventory and identified potential population.", ej),
  E("August 13, 2025", "OTHER", "August 13, 2025 – Supplier was onsite at Spartan Fire Chassis production to review application of the product, confirmation of the test results, and product inspection procedures."),
  E("August 20, 2025", "OTHER", "August 20, 2025 – Spartan conducted risk assessment and stop ship issued."),
  E("August 21, 2025", "OTHER", "August 21, 2025 – Spartan escalated the issue to REV Group Management."),
  E("August 29, 2025", "DECISION", "August 29, 2025 – REV’s senior leadership approved a voluntary recall for this issue"),
  E("September 5, 2025", "OTHER", "September 5, 2025 - Spartan determined final population."),
  E("October 14, 2025", "SUPPLIER_NOTICE", "October 14, 2025 - Alexis Fire Equipment was notified by Spartan about the recall and provided with the recall population"),
 ])

# 25V737 Mazda
m1 = "September 17, 2025: Mazda received a field report that a 2025 Mazda CX-50 experienced wheel and component detachment."
m2 = "September 18 through October 6, 2025: This vehicle has been confirmed as a subject unit for in-plant repair."
m3 = "October 7 through 22, 2025: Mazda assessed the potential risk associated with this issue, including its impact on vehicle operation and customer safety."
L["RCLRPT-25V737-6790.txt"] = dict(
 claims=[S1NR(), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "Improper torque application to bolts securing suspension components may result in bolt loosening or detachment, potentially causing separation of the affected components."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("September 17, 2025", "FILER_AWARENESS", m1),
  I("September 17, 2025", "OTHER", "After the dealer inspected the vehicle, the bolt that secures the lower control arm ball joint to the steering knuckle was found to be missing on the passenger-side.", m1),
  I("September 17, 2025", "INVESTIGATION_START", "Mazda initiated an investigation.", m1),
  E("September 18 through October 6, 2025", "OTHER", m2),
  I("September 18 through October 6, 2025", "OTHER", "A review of the in-plant repair records shows that no tightening torque value was recorded for the bolt securing the lower control arm ball joint to the steering knuckle.", m2),
  I("September 18 through October 6, 2025", "OTHER", "Further investigation confirmed that for some units, repair records were missing or torque entries were not recorded for the bolts removed and reinstalled during the repair process.", m2),
  I("September 18 through October 6, 2025", "OTHER", "The investigation concluded that operators did not follow in- plant repair procedures.", m2),
  E("September 19 through October 10, 2025", "OTHER", "September 19 through October 10, 2025: In-plant processes were corrected to ensure that proper repair procedures are followed, and that related documentation is recorded and retained."),
  E("October 7 through 22, 2025", "INVESTIGATION_START", m3),
  I("October 7 through 22, 2025", "OTHER", "To better understand the overall extent of the concern, the scope of the affected range was also identified.", m3),
  E("October 23, 2025", "DECISION", "October 23, 2025: Mazda held a Quality Audit Committee meeting to review all available information to date and approved a field action for affected MY 2025 CX-50 vehicles."),
  E("November 26, 2025", "NHTSA_FILING", "November 26, 2025: This first amendment is being filed to revise the description of the safety risk."),
 ])

# 25V744 Toyota
t1 = "April 2024 - December 2024 Toyota conducted a review of the Japan spec PVM system software programming as a part of a different activity and began bench testing to investigate possibility of (1) rearview image freezing and (2) rearview image not displaying, due to field reports in Japan."
t2 = "December 2024 - October 2025 Toyota conducted vehicle testing to confirm if (1) the interruptions, or (2) the abnormal camera optical alignment data could occur on a vehicle during actual customer usage, and what the phenomenon was if the conditions occurred."
L["RCLRPT-25V744-2593.txt"] = dict(
 claims=[S1("Name: DENSO International America, Inc."),
         S2("INSUFFICIENT", "Name: DENSO International America, Inc.", "block")],
 cause=C("NOT_REPORTED"), upstream=U("NONE_MENTIONED"),
 events=[
  E("April 2024 - December 2024", "INVESTIGATION_START", t1),
  I("April 2024 - December 2024", "OTHER", "During bench testing, Toyota found (1) if interruptions occurred during the image drawing process, the rearview image could freeze, and (2) if the camera optical alignment data became abnormal during the data writing process due to the Parking Assist ECU power down", t1),
  I("April 2024 - December 2024", "FILER_AWARENESS", "Additionally, it was discovered during the software programming review that, the possible errors could affect to the global spec PVM systems, including those sold in the U.S.", t1),
  E("December 2024 - October 2025", "INVESTIGATION_START", t2),
  I("December 2024 - October 2025", "OTHER", "For (1), the testing and analysis found that, if the vehicle is shifted into reverse within 0.7 to 2.6 seconds after ignition on, a vehicle speed is detected during the first image frame process, and the first image frame process occurs within 1.1 to 1.4 seconds after shifting into reverse", t2),
  I("December 2024 - October 2025", "OTHER", "For (2), the testing and analysis found that two 23 millisecond camera optical alignment data writing processes occur randomly during the first 12.5 seconds after ignition on and if the Parking Assist ECU powers off during either of these two data writing processes", t2),
  E("October 24, 2025", "DECISION", "On October 24, 2025, Toyota determined that it is possible that the involved vehicles could experience the conditions above and may not meet the requirements of FMVSS No. 111 S5.5.5, S5.5.6, S6.2.5 and/or S6.2.6."),
  I("December 2024 - October 2025", "DECISION", "As a result, Toyota decided to conduct a recall.", t2),
 ])

# 25V749 Heil
h1 = "August 31, 2024: Agility’s engineering team was advised of a report from a customer that the manual cylinder valve on a CNG fuel system experienced a leak."
h2 = "September 12 – November 13, 2024: Valves were sent to Agility engineering and a root cause investigation was initiated, which included the following activities: review of high magnification photos and analysis from engineering teams; regular meetings with the supplier, OMB- Saleri S.P.A. (“OMB”);"
h3 = "A review of service records revealed two additional failure reports (failure dates 6/19/2024 and 8/19/2024)."
L["RCLRPT-25V749-9037.txt"] = dict(
 claims=[S1("Name: OMB-Saleri S.P.A."),
         S2("SUPPORTED", h2, name="OMB-Saleri S.P.A.")],
 cause=C("INSUFFICIENT", "The root cause of the stress corrosion cracking is still under investigation."),
 upstream=U("NAMED", h2, names=["Agility Fuel Systems", "OMB-Saleri S.P.A."]),
 events=[
  E("August 31, 2024", "OTHER", h1),
  E("6/19/2024", "OTHER", h3),
  E("8/19/2024", "OTHER", h3),
  I("August 31, 2024", "OTHER", "Arrangements were made to obtain the valves for analysis.", h1),
  E("September 12 – November 13, 2024", "INVESTIGATION_START", h2),
  I("September 12 – November 13, 2024", "OTHER", "During this period, three additional valve failures were reported.", h2),
  I("September 12 – November 13, 2024", "OTHER", "Based upon the results of the investigation to date, Agility’s engineering team recommended that the matter be escalated to Agility’s Safety Committee for consideration.", h2),
  E("November 13, 2024", "DECISION", "November 13, 2024: Agility’s Safety Committee decided to initiate a safety recall to address this condition."),
 ])

# 25V754 McNeilus
L["RCLRPT-25V754-7812.txt"] = dict(
 claims=[S1NR(), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "During manufacturing of the refuse body, the intermediate amber reflex reflectors were not installed."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("September 2025", "FILER_AWARENESS", "In September 2025, in the course of considering a separate and unrelated issue, it came to McNeilus' attention that a Volterra model vehicle was not equipped with amber reflex reflectors at the middle of the refuse body."),
  N("INVESTIGATION_START", "McNeilus initiated an analysis of the issue including whether the individual vehicle was representative of broader vehicle production and whether the reflectors are required equipment under"),
 ])

# 25V770 Micro Bird
mb = "On Friday, October 24, 2025, Micro Bird received a notification letter of a recall (NHTSA #25E063) from its provider (Q’Straint) that certain wheelchair securement kits shipped between May 7, 2025, and September 10, 2025, may contain a defective retractor."
L["RCLRPT-25V770-7340.txt"] = dict(
 claims=[S1("Name: Q'STRAINT"), S2("SUPPORTED", mb, name="Q’Straint")],
 cause=C("NOT_REPORTED"),
 upstream=U("NAMED", mb, names=["Q’Straint"]),
 events=[
  E("Friday, October 24, 2025", "SUPPLIER_NOTICE", mb),
  N("INVESTIGATION_START", "Internal reviews of our recent orders and stock quickly determined that Micro Bird had been provided with potentially defective parts."),
  E("Monday, October 27, 2025", "DECISION", "On Monday, October 27, 2025, a meeting was called to advise strategic Micro Bird personnel that a recall notification was received from its provider and that a recall campaign would be launched."),
 ])

# 25V778 Yamaha
L["RCLRPT-25V778-6749.txt"] = dict(
 claims=[S1NR(), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "Due to insufficient consideration of the mounting structure of the retainer plate that secures the camshaft, the retainer bolt tightening force may be insufficient."),
 upstream=U("NOT_REPORTED"), events=[])

# 25V801 Mack
L["RCLRPT-25V801-2150.txt"] = dict(
 claims=[S1("Name: Nova Industries/Mayco International, LLC"),
         S2("INSUFFICIENT", "Name: Nova Industries/Mayco International, LLC", "block")],
 cause=C("SUPPORTED", "Component design inadequate for application"),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("August 06, 2025", "FILER_AWARENESS", "August 06, 2025: Repeat customer complaints drive creation of Quality Review case."),
  E("September 04, 2025", "INVESTIGATION_START", "September 04, 2025: Review determines need for corrective action and Safety Office opens product safety investigation."),
  E("November 03, 2025", "OTHER", "November 03, 2025: Product Safety Evaluation Committee review, recommends escalation to Product Safety Committee"),
  E("November 13, 2025", "DECISION", "November 13, 2025: Product Safety Committee determines that a product safety defect exists and decides to initiate a recall."),
 ])

# 25V807 Nissan
nq = "Nissan quarantined the vehicle and initiated an investigation together with the supplier."
L["RCLRPT-25V807-4146.txt"] = dict(
 claims=[S1("Name: VITRO"), S2("INSUFFICIENT", nq)],
 cause=C("NOT_REPORTED"), upstream=U("UNNAMED", nq),
 events=[
  E("August 25, 2025", "FILER_AWARENESS", "On August 25, 2025, during a routine yard audit at the Nissan Aguas II plant, a technician identified air bubbles trapped between the two sheets of glass and the Polyvinyl Butyral (PVB) film of the front windshield assembly on a Model Year 2025 Nissan Sentra vehicle."),
  N("INVESTIGATION_START", nq),
  E("August 2025 through September 2025", "INVESTIGATION_START", "August 2025 through September 2025 – Nissan and the supplier conducted duplication testing and discovered the bubble type delamination was potentially caused by foreign particles trapped between the glass sheets and the PVB film."),
  E("October 2025", "OTHER", "October 2025 – Investigation of the supplier’s assembly process determined that the root cause of the delamination was potentially caused by misaligned locator pins within the front windshield glass molds."),
  N("DECISION", "Nissan assessed the subject windshield and determined that the condition may not comply with certain FMVSS requirements."),
  E("November 13, 2025", "DECISION", "November 13, 2025 - Nissan decided to conduct a voluntary recall campaign to remedy the potentially affected vehicles in the U.S. market."),
 ])

# 25V818 Volvo
vq = "In October 2025, the supplier informed Volvo Cars’ Torslanda factory about a potential issue involving improperly torqued bolts in seat assemblies."
L["RCLRPT-25V818-2172.txt"] = dict(
 claims=[S1("Name: Adient"), S2("INSUFFICIENT", vq)],
 cause=C("SUPPORTED", "The root cause is due to maintenance or interruptions in the supplier manufacturing line, resulting in the abort timer starting before the tightening sequence was ready."),
 upstream=U("UNNAMED", vq),
 events=[
  E("2025-11-19", "OTHER", "A. Considered as a critical concern by CCMT* 2025-11-19"),
  E("2025-11-26", "DECISION", "B. Field Service Action decision confirmed by Volvo Car Corporation 2025-11-26"),
  E("October 2025", "SUPPLIER_NOTICE", vq),
  N("SUPPLIER_NOTICE", "Based on production records, the supplier identified a number of seats at risk."),
  N("INVESTIGATION_START", "The factory cross-checked these findings against vehicle production records and confirmed the affected vehicles."),
  N("OTHER", "During the initial investigation the symptom was also verified in a vehicle."),
  E("November 12, 2025", "INVESTIGATION_START", "On November 12, 2025, the concern was escalated to the Critical Concern Management Team (CCMT), which ordered a formal investigation including to conduct a risk assessment."),
  E("November 19, 2025", "DECISION", "This assessment was completed on November 19, 2025, and concluded that the issue posed an increased risk to motor vehicle safety."),
 ])

# 25V832 Virnig
L["RCLRPT-25V832-9661.txt"] = dict(
 claims=[S1("Name: Virnig Manufacturing"), S2("INSUFFICIENT", "Name: Virnig Manufacturing", "block")],
 cause=C("SUPPORTED", "Improper assembly procedures."),
 upstream=U("NONE_MENTIONED"),
 events=[
  N("FILER_AWARENESS", "Customer reached out to our Warranty/Service department with an issue regarding the trailer bearings (heard and felt vibrations)."),
  N("OTHER", "Plant Manager was informed of the issue."),
  N("OTHER", "Plant Manager then informed the Director of Operations, who then informed top management (company VPs and president)."),
  N("OTHER", "Meeting was held with Product Engineering Manager, Manufacturing Engineering Manager, VP of Operations and Engineering, Plant Manager, and Production Specialist."),
  N("OTHER", "It was brought to light that the problem might be from over torquing the spindle nut."),
  N("OTHER", "Determined there could have been discrepancies in the torquing value as well as the procedure."),
  N("INVESTIGATION_START", "Additional information was gathered from the customer who initially had reached out with the issue."),
  N("OTHER", "There was a phone call with the members listed above, as well as someone from Sales and another from the Service/Warranty department."),
  N("OTHER", "Made the decision to halt shipping additional units until root cause of the issue was determined and any remaining units at the plant could be checked."),
  N("OTHER", "After all evidence had been gathered, it was determined that the cause was improper torquing of the spindle nut."),
 ])

# 25V834 Zero
z2 = "October 7–9, 2025: Zero engineering staff met onsite with Dana in Italy to evaluate potential causes."
L["RCLRPT-25V834-3517.txt"] = dict(
 claims=[S1("Name: DANA TM4 Italia S.r.l."), S2("SUPPORTED", z2, name="Dana")],
 cause=C("SUPPORTED", "Non coated fasteners were introduced under a supplier deviation due to material shortage."),
 upstream=U("NAMED", z2, names=["Dana"]),
 events=[
  E("Late September 2025", "FILER_AWARENESS", "Late September 2025: Zero proactively reviewed all 'quits while running' cases and identified a pattern of controller failures consistent with overvoltage events."),
  E("October 7–9, 2025", "INVESTIGATION_START", z2),
  I("October 7–9, 2025", "OTHER", "Loose high power fasteners, caused by the use of non phosphate coated fasteners were identified as a likely contributor.", z2),
  E("October 21, 2025", "OTHER", "October 21, 2025: Zero convened a Product Integrity Team Zero (PITZ) review and determined that escalation was warranted."),
  E("October 23, 2025", "OTHER", "October 23, 2025: Zero notified Dana of its preliminary root cause assessment, shared supporting test results, and requested supplier validation."),
  E("October 28, 2025", "OTHER", "October 28, 2025: Zero initiated direct engagement with Dana’s Global Warranty leadership to expedite alignment and advance remedy planning."),
 ])

# 25V836 VW
wq = "In June 2025, the supplier conducted a CT analysis of the cell modules from 3 of the 4 thermal events referenced above and was unable to find a root cause within the battery cell module."
L["RCLRPT-25V836-1434.txt"] = dict(
 claims=[S1("Name: SK Battery America Inc."), S2("INSUFFICIENT", wq)],
 cause=C("SUPPORTED", "A quality deviation at the supplier was identified within a certain production period."),
 upstream=U("UNNAMED", wq),
 events=[
  E("January 18, 2024", "FILER_AWARENESS", "On January 18, 2024, Volkswagen was informed of a thermal event in Illinois, involving a vehicle that was charging at a Level 3 DC charger."),
  E("January 30, 2024", "INVESTIGATION_START", "An on-site investigation into the vehicle and the charging apparatus was carried out by Volkswagen on January 30, 2024, and the area of origin was determined to be within the HV battery."),
  N("OTHER", "The battery was shipped to Chattanooga for further analysis."),
  E("July 2, 2024", "FILER_AWARENESS", "On July 2, 2024, Volkswagen was notified about a thermal event in California, involving a parked vehicle that was not charging."),
  N("OTHER", "Volkswagen attempted to inspect the vehicle, but the inspection was delayed until permission was granted to have access to the vehicle."),
  E("December 2024", "INVESTIGATION_START", "The vehicle was inspected by Volkswagen in December 2024, and the area of origin was determined to be within the HV battery."),
  N("INVESTIGATION_START", "Various components of the battery assembly were sent to Chattanooga for analysis, which revealed no shortcomings, and the HV battery cell modules were sent to the supplier for analysis."),
  E("October 6, 2024", "FILER_AWARENESS", "On October 6, 2024, Volkswagen was notified about a thermal event in California, involving a parked vehicle that was not charging."),
  E("December 6, 2024", "FILER_AWARENESS", "On December 6, 2024, Volkswagen was notified about a thermal event in Utah, involving a vehicle while driving."),
  E("February 5, 2025", "INVESTIGATION_START", "The vehicle was inspected by Volkswagen on February 5, 2025, and the area of origin was determined to be within the HV battery."),
  E("June 2025", "INVESTIGATION_START", wq),
  E("June-July 2025", "INVESTIGATION_START", "In June-July 2025, after the supplier’s inconclusive CT Results, VW and the supplier investigated other potential causes/influences within the vehicle but outside of the HV battery."),
  N("OTHER", "This investigation found no evidence of other potential causes, so the investigation refocused on the HV battery."),
  E("August 15, 2025", "FILER_AWARENESS", "On August 15, 2025, Volkswagen was informed of a thermal event in Colorado involving a vehicle charging at a Level 3 DC charger."),
  E("September 23, 2025", "INVESTIGATION_START", "The vehicle was inspected by Volkswagen on September 23, 2025, and the area of origin was determined to be the HV battery."),
  E("late September 2025", "INVESTIGATION_START", "After regular back and forth discussions between Volkswagen and the supplier to try to identify the cause of these events, in late September 2025, the supplier performed Tear-Down Analysis of the other damaged cell modules which revealed the “shifted” electrode condition."),
  N("OTHER", "The supplier then compared this to the previous CT Images and was able to recognize the shifted cathode in the CT images."),
  E("October 2025", "OTHER", "In October 2025, Volkswagen voluntarily brought the topic of these thermal incidents to ODI during its quarterly meeting and discussed that it was working with its supplier to finalize root cause, risk assessment, affected population, and countermeasures."),
  E("November 2025", "SUPPLIER_NOTICE", "In November 2025, the supplier identified the specific modules with the shifted electrode condition, and based on that, the vehicle population was identified."),
  E("November 26, 2025", "DECISION", "On November 26, 2025, this topic was presented to the Volkswagen Product Safety Committee and a recall for vehicles built with affected HV battery cell modules was decided."),
  E("December 09, 2025", "SUPPLIER_NOTICE", "On December 09, 2025, the supplier provided updated results of its investigation, which found additional HV battery cell modules that were potentially produced with shifted electrodes."),
  E("December 10, 2025", "DECISION", "On December 10, 2025, the new information from the supplier was presented to the Volkswagen Product Safety Committee and a recall for additional vehicles built with the additional HV battery cell modules was decided."),
 ])

# 25V870 Gillig
gq = "11/03/2025 GILLIG was notified by company American Seating of a safety issue affecting wheelchair locking retractors manufactured by Q’Straint."
L["RCLRPT-25V870-2680.txt"] = dict(
 claims=[S1("Name: Qstraint"), S2("SUPPORTED", gq, name="Q’Straint")],
 cause=C("NOT_REPORTED"),
 upstream=U("NAMED", gq, names=["American Seating", "Q’Straint"]),
 events=[
  E("11/03/2025", "SUPPLIER_NOTICE", gq),
  E("12/12/2025", "INVESTIGATION_START", "12/12/2025 GILLIG completed population analysis and identified four (4) vehicles potentially affected."),
  E("12/12/2025", "DECISION", "12/12/2025 The GILLIG Safety Committee reviewed the issue and decided to file a safety recall with NHTSA."),
 ])

# 25V906 BMW
bq = "On December 18, 2025, BMW decided to conduct a voluntary safety recall."
L["RCLRPT-25V906-7035.txt"] = dict(
 claims=[S1("Name: BMW AG"), S2("SUPPORTED", bq, name="BMW")],
 cause=C("NOT_REPORTED"), upstream=U("NONE_MENTIONED"),
 events=[
  E("mid-October 2025", "FILER_AWARENESS", "In mid-October 2025, a field incident involving a Model Year 2025 BMW i4 was noted in which vehicle stalling had recently occurred several times."),
  N("OTHER", "Eventually, a restart was not possible."),
  E("early November", "INVESTIGATION_START", "In early November, an engineering investigation was initiated."),
  N("INVESTIGATION_START", "An analysis of the field vehicle, including electrical plug connections, wiring and cables, and vehicle charging connections was performed."),
  N("INVESTIGATION_START", "Diagnostics, including a review of fault codes, was conducted."),
  E("December", "OTHER", "In December, the analyses indicated that, on the field incident vehicle, the positive battery cable connection to the rear power distributor may not have been performed to specifications."),
  N("INVESTIGATION_START", "As a result, information from the vehicle assembly plant was requested and further analyses were performed."),
  N("OTHER", "This led to the finding that, on a small number of vehicles, it was possible that the positive battery cable connection to the rear power distributor may not have been performed to specifications."),
  N("INVESTIGATION_START", "Vehicle assembly information was reviewed to determine the number and production dates of potentially affected vehicles."),
  E("December 18, 2025", "DECISION", bq),
 ])

# 26V001 Volvo
L["RCLRPT-26V001-4623.txt"] = dict(
 claims=[S1("Name: Shandong Geely Sunwoda Power Battery Co."),
         S2("INSUFFICIENT", "Name: Shandong Geely Sunwoda Power Battery Co.", "block")],
 cause=C("SUPPORTED", "A process deviation that may result in the formation of lithium plating growth that could also lead to an internal cell short."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("2025-12-26", "OTHER", "A. Considered as a critical concern by CCMT* 2025-12-26"),
  E("2025-12-26", "DECISION", "B. Field Service Action decision confirmed by Volvo Car Corporation 2025-12-26"),
  E("July 2025", "FILER_AWARENESS", "In July 2025 Volvo Cars received the first report indicating potential overheating of HV-battery cell outside the USA."),
  N("INVESTIGATION_START", "An investigation was initiated to review the customer symptom and a possible root cause."),
  N("OTHER", "The investigation was escalated to the Critical Concern Action Process (CCAP)."),
  N("INVESTIGATION_START", "The issue was concluded as potentially critical and the Critical Concern Management Team (CCMT) initiated a technical investigation to conclude customer symptom, risk assessment and root cause."),
  N("OTHER", "Decision to start preparation and release and monitor was taken at the same time and a safety notice was released."),
  E("December 26th, 2025", "DECISION", "On the December 26th, 2025, the CCMT team took the decision to release a safety notification recall as it was judged as an increased risk towards motor vehicle safety."),
 ])

# 26V007 East
L["RCLRPT-26V007-7238.txt"] = dict(
 claims=[S1NR(), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "Improper weld penetration at the bumper horizontal to the bumper verticals."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("November 1, 2024", "OTHER", "November 1, 2024 - Start of under ride guards being robotically welded."),
  E("March 2025", "OTHER", "March 2025 - Program updated for robotic weld cell."),
  E("July 14, 2025", "FILER_AWARENESS", "July 14, 2025 - Customer reports bumper horizonal became dislodged."),
  E("October 21, 2025", "FILER_AWARENESS", "October 21, 2025 – NHTSA notified East of failed test."),
 ])

# 26V018 Lucid
L["RCLRPT-26V018-6626.txt"] = dict(
 claims=[S1NR(), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "Earlier versions of software could cause the intermittent delivery of vehicle power state and view signals to the camera system, causing the rearview image to fail to display."),
 upstream=U("NONE_MENTIONED"),
 events=[
  N("OTHER", "Lucid conducted testing for compliance with FMVSS 111 before the start of production of the Lucid Gravity and before the release of each software upgrade that Lucid understood would affect the rearview image."),
  N("OTHER", "After the sale of certified vehicles, Lucid determined that certain model year 2025–2026 Lucid Gravity vehicles operating on software versions prior to version 3.3.20 (the “Remedy Version”) may experience a blank rear view monitor screen or a blank screen with a warning when shifting to reverse"),
  E("October 2025", "FILER_AWARENESS", "Through its investigation of this issue, Lucid determined that in October 2025 Lucid engineers observed a software test vehicle with a blank rearview image when it was put in reverse."),
  N("INVESTIGATION_START", "Lucid launched an internal investigation to determine possible root causes for the issue."),
  E("November 2025", "FILER_AWARENESS", "In November 2025, another engineering vehicle was discovered with a similar issue."),
  E("November 12, 2025", "OTHER", "On November 12, 2025, Lucid issued a new OTA software release."),
  E("Later in November", "FILER_AWARENESS", "Later in November, a customer reported camera image issues using the new release."),
  E("December 2025", "FILER_AWARENESS", "By December 2025, the Lucid Quality Team was able to verify other customer cases with the rearview image issue."),
  N("OTHER", "A future software revision, to be included in version 3.3.20, was identified as a potential mitigation for the rearview image issues."),
  E("December 5", "OTHER", "On December 5, Lucid’s Product Safety Working Group (PSWG) met to receive an update on rearview camera issues."),
  E("December 10, 2025", "OTHER", "A stop sale was issued on December 10, 2025, while Lucid investigated if other vehicles in the field had the same issue."),
  N("OTHER", "Root causes were identified as signal handling issues related to vehicle power state and camera views along with fault recovery in the lower-level camera pipeline."),
  E("December 11, 2025", "OTHER", "On December 11, 2025, software version 3.3.20 was released to customers."),
  E("end of December", "OTHER", "By the end of December, Lucid had found 9 similar customer issues and the PSWG decided to refer the issue to the Product Safety Executive Council (PSEC) for consideration."),
  E("January 9, 2026", "DECISION", "On January 9, 2026, the PSEC met and determined that a noncompliance with FMVSS 111 existed in vehicles operating on software versions older than 3.3.20."),
 ])

# 26V059 FCA
L["RCLRPT-26V059-8421.txt"] = dict(
 claims=[S1NR("Name: See -Tow Module Supplier Information.pdf"), S2("NOT_REPORTED")],
 cause=C("NOT_REPORTED"), upstream=U("NONE_MENTIONED"),
 events=[
  E("August 28, 2025", "INVESTIGATION_START", "On August 28, 2025, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into some 2025-2026 MY Ram 1500/2500/3500, 2025-2026 MY RAM 3500/4500/5500 Cab Chassis, 2024-2026 MY Jeep Wagoneer S"),
  E("January 26, 2026", "DECISION", "On January 26, 2026, FCA US determined, through the Vehicle Regulations Committee, that a safety defect exists in certain vehicles."),
 ])

# 26V062 Ford
fq = "A supplier sorting error failed to detect the absence of washers during production."
L["RCLRPT-26V062-8099.txt"] = dict(
 claims=[S1("Name: Brugola Industriale USA INC"), S2("INSUFFICIENT", fq, "cause")],
 cause=C("SUPPORTED", fq),
 upstream=U("UNNAMED", fq, "cause"),
 events=[
  E("November 18, 2025", "FILER_AWARENESS", "On November 18, 2025, during the assembly of BEV-H high voltage (HV) battery pack bus bars at the Rawsonville Component Plant (RCP), an assembly line operator identified two threaded fasteners missing conical washers."),
  E("December 2, 2025", "OTHER", "On December 2, 2025, a Stop Ship was declared."),
  E("December 4, 2025", "OTHER", "On December 4, 2025, the topic was introduced to Ford’s Critical Concern Review Group (CCRG)."),
  N("INVESTIGATION_START", "The CCRG investigation reviewed the HV battery assembly process at RCP and determined that the potential exists for battery packs to have been built with fasteners missing the conical washers."),
  N("INVESTIGATION_START", "Following this discovery, Kansas City Assembly Plant (KCAP) and RCP initiated a tracing campaign."),
  N("OTHER", "It was determined through a review of supplier plant records that the subject population of vehicles in the field has the potential to contain BEV-H battery packs assembled with one or more non-conforming fasteners."),
  N("OTHER", "The CCRG investigation confirmed that insufficient clamp load of a HV bus bar can result in increased joint electrical resistance."),
  E("January 27, 2026", "DECISION", "On January 27, 2026, Ford’s Field Review Committee reviewed the concern and approved a field action."),
 ])

# 26V068 Hyundai
hy1 = "November 2025 On November 18, 2025, HMGMA notified NASO of a potential condition involving high voltage busbar bolts within certain BSA units supplied by MNAe."
hy2 = "December 2025 On December 18, 2025, HMGMA provided NASO with a list of potentially affected VINs."
L["RCLRPT-26V068-2387.txt"] = dict(
 claims=[S1("Name: Mobis North America Electrified (\"MNAe\")"),
         S2("SUPPORTED", "On November 18, 2025, HMGMA notified NASO of a potential condition involving high voltage busbar bolts within certain BSA units supplied by MNAe.", name="MNAe")],
 cause=C("SUPPORTED", "BSAs may have been reworked without confirmation of automated torque verification processes."),
 upstream=U("NAMED", "On November 18, 2025, HMGMA notified NASO of a potential condition involving high voltage busbar bolts within certain BSA units supplied by MNAe.", names=["MNAe"]),
 events=[
  E("November 18, 2025", "FILER_AWARENESS", "On November 18, 2025, HMGMA notified NASO of a potential condition involving high voltage busbar bolts within certain BSA units supplied by MNAe."),
  I("November 2025", "SUPPLIER_NOTICE", "According to the supplier, the issue was identified after a BSA unit failed an automated quality test during production, prompting further inspection which identified potentially under torqued busbar bolts.", hy1),
  I("November 2025", "INVESTIGATION_START", "Following notification, NASO initiated information gathering to understand the scope of the condition, the affected production processes, and potential flow out to the U.S. market.", hy1),
  E("December 18, 2025", "OTHER", "On December 18, 2025, HMGMA provided NASO with a list of potentially affected VINs."),
  I("December 2025", "INVESTIGATION_START", "NASO continued its investigation in coordination with HMC and MNAe.", hy2),
  I("December 2025", "OTHER", "During this period, NASO requested and reviewed additional information regarding the BSA manufacturing process, torque application at the relevant assembly stations, process data, rework flow procedures, and quality inspection practices.", hy2),
  I("December 2025", "SUPPLIER_NOTICE", "MNAe’s report confirmed that the issue could occur when BSAs were removed from the assembly line for rework and were subsequently reintroduced at a later stage allowing certain torque confirmation processes to be bypassed.", hy2),
  I("December 2025", "SUPPLIER_NOTICE", "MNAe further identified that the affected condition was limited to specific BSAs produced on one assembly line.", hy2),
  E("January 29, 2026", "DECISION", "January 29, 2026 NASO reviewed the supplier’s technical findings, traceability and test results and convened its North America Safety Decision Authority (“NASDA”), deciding to conduct a safety recall of the affected model year 2025–2026 Hyundai IONIQ 5 and 2026 IONIQ 9 vehicles"),
 ])

# 26V110 Toyota
tq = "Toyota identified that the supplier recently underwent a tooling change and the new tooling was missing the optical axis marking."
L["RCLRPT-26V110-5688.txt"] = dict(
 claims=[S1("Name: North American Lighting [“NAL”]"), S2("INSUFFICIENT", tq)],
 cause=C("NOT_REPORTED"), upstream=U("UNNAMED", tq),
 events=[
  E("November 2025", "FILER_AWARENESS", "In November 2025, during a vehicle audit the vehicle manufacturing plant observed that a vehicle’s headlamps were missing the optical axis marking."),
  N("OTHER", tq),
  N("OTHER", "Toyota issued a vehicle hold and repair activity at vehicle processing facilities for vehicles which may have been equipped with headlamps produced with this tooling."),
  N("OTHER", "Toyota identified certain vehicles had flowed out of the vehicle processing facilities to the market."),
  E("February 19, 2026", "DECISION", "Based on this information, Toyota determined on February 19, 2026 that the vehicles identified in Section 3 above were sold with headlamp assemblies that may not meet the requirements of FMVSS No. 108, paragraph S10.18.5.1."),
 ])

# ---- build + verify ----
out, errs = [], []
for fn in sorted(os.listdir(T)):
    if not fn.endswith(".txt") or fn.startswith("._"):
        continue
    fl, sec = sections(os.path.join(T, fn))
    lab = L[fn]
    obj = {"file": fl, "claims": lab["claims"], "cause": lab["cause"], "upstream": lab["upstream"], "events": lab["events"]}
    def chk(q, s, what):
        if not q:
            return
        if len(q) > 300: errs.append(f"{fn} {what}: too long {len(q)}")
        if norm(q) not in sec[s]: errs.append(f"{fn} {what}: not in {s}: {q[:80]}")
    for c in obj["claims"]:
        chk(c["quote"], c["section"], c["id"])
    chk(obj["cause"]["quote"], "cause", "cause")
    chk(obj["upstream"]["quote"], obj["upstream"]["section"], "upstream")
    for i, e in enumerate(obj["events"]):
        chk(e["quote"], "chronology", f"ev{i}")
        if e["date_text"] and not e["inherited_date"] and e["date_text"] not in e["quote"]:
            errs.append(f"{fn} ev{i}: date not in quote")
        if e["inherited_date"]:
            chk(e["entry_quote"], "chronology", f"ev{i} entry")
            if e["date_text"] not in e["entry_quote"]: errs.append(f"{fn} ev{i}: date not in entry")
    out.append(obj)

print("\n".join(errs) or "ALL QUOTES OK")
with open(os.path.join(D, "passB.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(len(out), "filings,", sum(len(o["events"]) for o in out), "events")
