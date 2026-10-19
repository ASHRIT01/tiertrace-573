import json, re, os, sys

D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def sections(fn):
    txt = open(os.path.join(T, fn), encoding="utf-8").read()
    file_line = re.search(r"^FILE:\s*(\S+)", txt, re.M).group(1)
    b = txt.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    c = txt.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    ch = txt.split("=== CHRONOLOGY ===")[1]
    return file_line, {"block": norm(b), "cause": norm(c), "chronology": norm(ch)}

L = []

def ev(t, q, d="", mode="own", entry=None):
    e = {"date_text": d, "type": t, "quote": q}
    if mode == "own":
        e["inherited_date"] = False; e["date_inferred"] = False
    elif mode == "inh":
        e["inherited_date"] = True; e["entry_quote"] = entry; e["date_inferred"] = False
    else:
        e["date_text"] = ""; e["inherited_date"] = False; e["date_inferred"] = True
    return e

def add(fn, s1, s2, cause, up, events):
    L.append((fn, s1, s2, cause, up, events))

# ---------- Ford software-audit chronology (26V369/370/374) ----------
def ford_common(fsa):
    return [
        ev("FILER_AWARENESS", "On November 26, 2024, an issue pertaining to incomplete software recall remedies was brought to Ford’s Critical Concern Group (CCRG) for review.", "November 26, 2024"),
        ev("FILER_AWARENESS", "This issue was initially identified in a Quality Office forum, where an audit was requested for software part numbers applied to vehicles remedied under a sample of field service actions (FSAs).", mode="inf"),
        ev("OTHER", "Initial review of three FSAs revealed insufficient data to confirm correct software application across all FSAs using the current field service tool, known as FDRS.", mode="inf"),
        ev("INVESTIGATION_START", "CCRG decided to conduct further investigation.", mode="inf"),
        ev("INVESTIGATION_START", "In December 2024, a cross-functional team was formed to audit all software FSAs that used the FDRS service tool, with its first focus being on safety and compliance FSAs.", "December 2024"),
        ev("OTHER", "Templates were created to track software lineage part numbers.", mode="inf"),
        ev("OTHER", "On December 19, 2024, Ford informed NHTSA of this concern -- the service tool data confirmed that the software state on the service tool at the time of installation matches the FSA software release for most vehicles.", "December 19, 2024"),
        ev("OTHER", "Ford discussed with NHTSA its plan to address the mismatched vehicles.", mode="inf"),
        ev("OTHER", "In January 2025, the cross-functional team created database records to store all software lineage part numbers for previously launched FSAs.", "January 2025"),
        ev("INVESTIGATION_START", "The team then began auditing the current software level for every VIN repaired under several previously launched FSAs.", mode="inf"),
        ev("FILER_AWARENESS", "In March 2025, during a comprehensive audit of software-related FSAs dating back to 2017, discrepancies were identified during the transition between the legacy field service tool, known as IDS, and the new FDRS service tool.", "March 2025"),
        ev("OTHER", "The audit revealed that implementation inconsistencies found in FDRS could also be present within the IDS software as well as a significant lack of historical data.", mode="inf"),
        ev("INVESTIGATION_START", "Further investigation was deemed necessary.", mode="inf"),
        ev("INVESTIGATION_START", "In November 2025, a harvest program was approved to assess the success of remedies applied using the IDS tool for programs administered during this transition period.", "November 2025"),
        ev("OTHER", "Results of this harvest program showed that in some FSAs, the intended remedy software may not have been successfully applied to all vehicles.", mode="inf"),
        ev("OTHER", "On April 16, 2026, the matter was presented to the Critical Concern Review Group (CCRG).", "April 16, 2026"),
        ev("OTHER", "The CCRG determined that several FSAs that had a recall remedy implemented using the IDS tool may have been closed without that remedy being installed.", mode="inf"),
        ev("INVESTIGATION_START", "As a result, an activity was initiated to verify the software levels of vehicles that previously received these FSA repairs.", mode="inf"),
        ev("OTHER", f"On May 27, 2026, Ford's audit team confirmed that the software state matched the FSA software release in a subset of vehicles out of the total population of completed FSA {fsa} remedy repairs.", "May 27, 2026"),
        ev("DECISION", "On June 2, 2026, Ford’s Field Review Committee reviewed the concern and approved a field action.", "June 2, 2026"),
    ]

FORD_S1 = {"id": "S1", "status": "SUPPORTED", "quote": "Name: Ford Motor Company", "section": "block"}
FORD_S2 = {"id": "S2", "status": "SUPPORTED", "name": "Ford", "quote": "On June 2, 2026, Ford’s Field Review Committee reviewed the concern and approved a field action.", "section": "chronology"}
NONE_UP = {"kind": "NONE_MENTIONED", "names": [], "quote": "", "section": ""}
CAUSE_NR = {"status": "NOT_REPORTED", "quote": "", "section": "cause"}
S1_NR = {"id": "S1", "status": "NOT_REPORTED", "quote": "", "section": "block"}
S2_NR = {"id": "S2", "status": "NOT_REPORTED", "quote": "", "section": ""}

def S1(name):
    return {"id": "S1", "status": "SUPPORTED", "quote": f"Name: {name}", "section": "block"}
def S2sup(name, q, sec="chronology"):
    return {"id": "S2", "status": "SUPPORTED", "name": name, "quote": q, "section": sec}
def S2ins(q, sec):
    return {"id": "S2", "status": "INSUFFICIENT", "quote": q, "section": sec}
def C(status, q):
    return {"status": status, "quote": q, "section": "cause"}

add("RCLRPT-26V369-8635.txt", FORD_S1, FORD_S2,
    C("SUPPORTED", "Affected vehicles are equipped with a CPV that may stick open."), NONE_UP,
    ford_common("18S32") + [
        ev("FILER_AWARENESS", "On June 12, 2026, following an investigation into the 18S32 workflow, Ford discovered that the population for 26S40 did not include certain affected VINs that fall outside of the US but are located in US federal territories.", "June 12, 2026"),
        ev("DECISION", "On July 7, 2026, Ford’s Field Review Committee reviewed the concern and approved an amendment to the population of the field action.", "July 7, 2026"),
    ])

add("RCLRPT-26V370-0555.txt", FORD_S1, FORD_S2,
    C("SUPPORTED", "Immediately after engine start-up in cold ambient temperatures, the power supply within the eight inch instrument cluster productivity screen may be unable to maintain electrical output control."),
    NONE_UP, ford_common("17C01"))

add("RCLRPT-26V374-8779.txt", FORD_S1, FORD_S2,
    C("INSUFFICIENT", "The power window system configuration may exceed the regulatory requirement for remote actuation closing force, increasing the risk of injury."),
    NONE_UP, ford_common("16C12"))

q = "On or about May 7, 2026, Farber Specialty Vehicles was contacted by Weldon, a division of Akron Brass, and notified that UV800 touch screens may contain a defect that"
add("RCLRPT-26V395-0079.txt", S1("AKRON BRASS COMPANY"), S2sup("Akron Brass", q),
    C("INSUFFICIENT", "Not disclosed by the manufacturer."),
    {"kind": "NAMED", "names": ["Weldon", "Akron Brass"], "quote": q, "section": "chronology"},
    [ev("SUPPLIER_NOTICE", q, "May 7, 2026")])

e519 = "May 19, 2026 an update was made to the manufacturing documentation system updating the VIN Labels."
add("RCLRPT-26V397-4460.txt", S1("Indian Motorcycle Company LLC"),
    S2sup("IMC", "On May 18, 2026, in an audit for information documentation, IMC found a discrepancy on the VIN Label for Indian Chief Vintage models."),
    C("SUPPORTED", "Incorrect VIN label information was populated in the Motorcycle Data Sheet and was not corrected during compliance and engineering review."),
    NONE_UP, [
        ev("FILER_AWARENESS", "On May 18, 2026, in an audit for information documentation, IMC found a discrepancy on the VIN Label for Indian Chief Vintage models.", "May 18, 2026"),
        ev("OTHER", e519, "May 19, 2026"),
        ev("INVESTIGATION_START", "Vehicles built on or after May 20, 2026 were produced with corrected VIN labels and in conjunction, IMC started an investigation.", "May 19, 2026", "inh", e519),
        ev("DECISION", "June 15, 2026 the IMC Executive Review Committee reviewed and agreed upon a violation of", "June 15, 2026"),
    ])

e604 = "6/4/2026: Further investigation found that the PRW instructions called for photographic evidence of the threadlocker and that the documentation for the customer truck at issue was not consistent with the instructions and the record was inconclusive."
e617 = "6/17/2026: Harbinger’s Vehicle Safety Committee met on 6/17/26 and determined this condition could pose an unreasonable risk to public safety in violation of the Safety Act"
e728 = "7/28/2026 - 9/10/2026: Harbinger Engineering evaluated whether the cause of the missing ERCB bolts was the same underlying condition as seen in the initial recalled vehicles, and determined that it was likely the result of the same condition."
add("RCLRPT-26V405-2481.txt", S1_NR, S2_NR,
    C("SUPPORTED", "The documentation required to confirm application of the chemical threadlocker was insufficient for the affected vehicles, leaving its application unconfirmable."),
    NONE_UP, [
        ev("FILER_AWARENESS", "9/16/2025: Steering gear mounting bolts found loose on two (2) vehicles during initial vehicle validation testing; one (1) reported with loose steering feel and one (1) reported with poor alignment.", "9/16/2025"),
        ev("OTHER", "9/22/2025: To address the above issue, PRW-8649 (factory product rework) was issued to apply threadlocker to all vehicles already produced.", "9/22/2025"),
        ev("OTHER", "9/24/2025: A clean point was established as of VIN 7ZN5S25A4SG000357 for the production line on 9/24/2025 (the “Clean Point”).", "9/24/2025"),
        ev("FILER_AWARENESS", "5/4/2026: A customer vehicle experienced steering looseness, and initial investigation found the cause to be the steering gear box fasteners had become loose.", "5/4/2026"),
        ev("INVESTIGATION_START", "5/5-6/2026: An internal investigation was initiated, establishing that the threadlocker had not been applied despite documentation to the contrary in the PRW record, and the picture requirement in the PRW work instruction was modified for clarity.", "5/5-6/2026"),
        ev("OTHER", e604, "6/4/2026"),
        ev("OTHER", "Further study of the PRW records showed that the majority of the VINs listed in the PRW had either no picture or a picture inconsistent with the instructions and were therefore inconclusive.", "6/4/2026", "inh", e604),
        ev("DECISION", e617, "6/17/2026"),
        ev("FILER_AWARENESS", "Subsequent to the original Part 573 submission, three (3) vehicles outside the initially identified population presented related conditions.", "6/17/2026", "inh", e617),
        ev("DECISION", "Although none of these vehicles had received the initial recall remedy, Harbinger elected out of an abundance of caution to expand the population of potentially affected vehicles and to revise the remedy.", "6/17/2026", "inh", e617),
        ev("FILER_AWARENESS", "7/28/2026: Customer 1 brought a truck to the dealer for an unrelated repair; during inspection the dealer found a missing ERCB bolt.", "7/28/2026"),
        ev("FILER_AWARENESS", "7/30/2026: Customer 2 complained of steering play, and dealer inspection of the vehicle found 3 missing ERCB bolts.", "7/30/2026"),
        ev("FILER_AWARENESS", "8/24/2026: Customer 3 complained of alignment issues, and dealer inspection found 2 missing ERCB bolts.", "8/24/2026"),
        ev("INVESTIGATION_START", e728, "7/28/2026 - 9/10/2026"),
        ev("OTHER", "To better repair the condition, Harbinger developed and validated a new remedy that increases the friction between the ERCB and the mounting member and changes the torque procedure to torque to angle for higher accuracy.", "7/28/2026 - 9/10/2026", "inh", e728),
        ev("DECISION", "9/10/2026: Harbinger’s Technical Review Committee met on September 10, 2026 and determined that it would proceed with an amendment to the current Part 573 recall to better address the condition.", "9/10/2026"),
    ])

add("RCLRPT-26V407-5609.txt", S1("Daimler Truck North America"),
    S2sup("DTNA", "On June 24, 2026, DTNA determined that a defect related to motor vehicle safety may exist."),
    CAUSE_NR, NONE_UP, [
        ev("INVESTIGATION_START", "Following feedback from a dealer about a potential issue with the entrance door, on May 27, 2026, DTNA initiated a review of the issue.", "May 27, 2026"),
        ev("OTHER", "On May 30, 2026, vehicles at the manufacturing facility were placed in containment as a precaution.", "May 30, 2026"),
        ev("INVESTIGATION_START", "From June 2 to June 16, 2026, DTNA engineering teams evaluated door system performance and confirmed the condition described by the dealer could be reproduced under defined operating sequences.", "June 2 to June 16, 2026"),
        ev("INVESTIGATION_START", "From June 15 to June 22, 2026, DTNA conducted warranty claims and field report analysis, which identified some potentially related reports.", "June 15 to June 22, 2026"),
        ev("OTHER", "Through continued analysis, engineering determined the condition was caused by improper timer relay behavior and identified a design incompatibility between a relay requiring a momentary input signal and a maintained-contact door switch.", mode="inf"),
        ev("DECISION", "On June 24, 2026, DTNA determined that a defect related to motor vehicle safety may exist.", "June 24, 2026"),
        ev("NHTSA_FILING", "On July 30, 2026, DTNA updated its Defect Information Report to include a description of the recall remedy.", "July 30, 2026"),
        ev("NHTSA_FILING", "On August 25, 2026, DTNA further amended the Defect Information report by updating the description of the recall remedy, listing the planned interim owner notification dates, and updating the planned final owner notification dates.", "August 25, 2026"),
    ])

add("RCLRPT-26V409-2533.txt", S1("Altec Industries Inc"),
    S2sup("Altec", "In May 2026, Altec identified a potential issue with a weight study that was not completed correctly."),
    CAUSE_NR, NONE_UP, [
        ev("FILER_AWARENESS", "In May 2026, Altec identified a potential issue with a weight study that was not completed correctly.", "May 2026"),
        ev("INVESTIGATION_START", "A root cause investigation was opened.", mode="inf"),
        ev("OTHER", "During the root cause analysis, Altec identified that additional units could be affected by incorrect weight studies.", mode="inf"),
        ev("INVESTIGATION_START", "On May 27, 2026, a potential field action investigation was initiated to identify field units and the potential risk to owners if the reduced pole rack capacity was not communicated correctly.", "May 27, 2026"),
        ev("DECISION", "After identifying the specific jobs that could have been shipped with incorrect ratings, on June 19, 2026, Altec determined that a field action was needed to communicate the risk", "June 19, 2026"),
    ])

add("RCLRPT-26V413-6519.txt", S1("FCA US"),
    S2sup("FCA US", "On June 25, 2026, FCA US determined, through the Vehicle Regulations Committee, that a noncompliance to Federal Motor Vehicle Safety Standard No. 102 exists in certain vehicles."),
    CAUSE_NR, NONE_UP, [
        ev("INVESTIGATION_START", "On November 04, 2025, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into some 2022-2024 MY Jeep Grand Cherokee, Grand Cherokee L, Wagoneer, and Wagoneer L vehicles", "November 04, 2025"),
        ev("INVESTIGATION_START", "From November 2025, through June 2026, FCA US TSRC reviewed warranty data, field records, and customer assistance records to understand potential customer consequence and vehicle scope.", "November 2025, through June 2026"),
        ev("OTHER", "From November 2025, through June 2026, FCA US TSRC held regular meetings with FCA US Engineering, Manufacturing, and Supplier Operations to understand all potential failure modes related to the shifter module display performance.", "November 2025, through June 2026"),
        ev("OTHER", "On June 10, 2026, FCA US TSRC organization recognized that a vehicle build issue existed on certain vehicles related to a shifter module display not indicating the gear positions and the relationship to each other, potentially resulting in a noncompliance with FMVSS No.102.", "June 10, 2026"),
        ev("DECISION", "On June 25, 2026, FCA US determined, through the Vehicle Regulations Committee, that a noncompliance to Federal Motor Vehicle Safety Standard No. 102 exists in certain vehicles.", "June 25, 2026"),
    ])

add("RCLRPT-26V415-6798.txt", S1("Harman International"),
    S2ins("Name: Harman International", "block"),
    C("SUPPORTED", "Loss of Pedestrian Alert function can occur due a software issue within the DSP module or an additional non-DSP related causal factor that is still under investigation."),
    NONE_UP, [
        ev("FILER_AWARENESS", "On February 19, 2026, an issue pertaining to loss of Acoustic Vehicle Alerting System (AVAS) (also referred to as Pedestrian Alert System (PAS)) function on vehicles that had previously received the remedy for Ford’s Safety Recall 25SA2 was brought to Ford’s Critical Concern Review Group for review.", "February 19, 2026"),
        ev("OTHER", "The remedy for 25SA2 was a software update that Ford made available through dealer service on October 29, 2025.", "October 29, 2025"),
        ev("OTHER", "On February 26, 2026, CCRG requested a pause in the deployment of this service remedy due to post-recall complaints for the loss of PAS functionality.", "February 26, 2026"),
        ev("INVESTIGATION_START", "In March and April 2026, CCRG analyzed warranty claims and began its technical investigation.", "March and April 2026"),
        ev("OTHER", "First, CCRG binned the post-recall complaints against the different audio architectures.", mode="inf"),
        ev("OTHER", "The team identified a potential software issue within the 24-channel DSP system on Nautilus HEV vehicles that can cause a loss of PAS function.", mode="inf"),
        ev("INVESTIGATION_START", "CCRG continued its investigation.", mode="inf"),
        ev("OTHER", "In May and June 2026, CCRG identified an additional concern that appears to affect all audio systems on the Nautilus HEV and Explorer HEV vehicle variants and leads to intermittent loss of PAS function.", "May and June 2026"),
        ev("DECISION", "On June 23, 2026, Ford’s Field Review Committee reviewed the concerns and approved a field action; however, the remedy was not fully described as more root cause investigation was needed.", "June 23, 2026"),
        ev("OTHER", "By late June and July 2026, Ford’s Audio and IVI teams determined that the additional PAS system concern is related to a transient interaction between the ACM and the Accessory Protocol Interface Module (APIM) rather than a persistent hardware defect.", "late June and July 2026"),
        ev("OTHER", "Analysis of CAN message history on test vehicles led to the understanding that DTCs typically occur during initialization of the audio bus at vehicle start.", mode="inf"),
        ev("OTHER", "Additional analysis of retail vehicle connected data found that most audio system faults take place while the vehicle is in Park.", mode="inf"),
        ev("DECISION", "On July 21, 2026, Ford’s Field Review Committee reviewed the proposed remedy and approved an amendment to the 26S51 field action.", "July 21, 2026"),
    ])

e65 = "6/5/26: Jayco engineering informed Compliance via email of a situation where the front dinette securement was not installed."
e68 = "6/8/26: The incident was reviewed by the Warranty Incident Review Committee (WIRC)."
add("RCLRPT-26V416-1095.txt", S1("GLOBAL LINK DISTRIBUTION,CORP."),
    S2ins("Name: GLOBAL LINK DISTRIBUTION,CORP.", "block"),
    C("SUPPORTED", "The front dinette brackets were not installed causing the front dinette not to be secure."),
    NONE_UP, [
        ev("FILER_AWARENESS", e65, "6/5/26"),
        ev("OTHER", "Engineering provided a preliminary scope of 26 and a preliminary instruction.", "6/5/26", "inh", e65),
        ev("OTHER", e68, "6/8/26"),
        ev("OTHER", "The members of WIRC decided to elevate it to the Corrective and Preventive Action Committee (CPAC) due to failing to meet FMVSS code 207 - Seating Systems", "6/8/26", "inh", e68),
        ev("OTHER", "6/17/26: The Corrective and Preventive Action Committee (CPAC) met to discuss this incident and elevated it to the Safety Steering Committee (SSC).", "6/17/26"),
        ev("DECISION", "6/25/26: The Safety Steering Committee (SSC) met and voted in favor of proceeding with a noncompliance recall for failure to comply with the requirements of 49 CFR § 571.207 - Seating Systems.", "6/25/26"),
    ])

eFeb = "February 2026 - The supplier conducted an initial teardown and evaluation of the suspect control valve assembly."
eMar = "March 2026 – Nissan initiated a targeted warranty return parts collection."
eApr = "April 2026 through May 2026 - Nissan conducted a horizontal confirmation audit to determine the scope of potentially affected vehicles, including export markets and other vehicle lines."
qJ = "Nissan, along with the transmission supplier (JATCO), initiated an investigation."
add("RCLRPT-26V419-3539.txt", S1("Valeo CDA (Thailand) Ltd."),
    S2sup("Valeo Thailand", "The investigation confirmed that JATCO Mexico was exclusive in utilizing the affected inhibitor switch manufactured at Valeo Thailand."),
    CAUSE_NR,
    {"kind": "NAMED", "names": ["JATCO", "JATCO Mexico", "Valeo Thailand"], "quote": qJ, "section": "chronology"}, [
        ev("FILER_AWARENESS", "On January 26, 2026, during a routine end-of-line vehicle quality confirmation check at Nissan’s Smyrna, Tennessee assembly plant, a technician identified an issue on a model year 2026 Nissan Rogue vehicle.", "January 26, 2026"),
        ev("INVESTIGATION_START", qJ, mode="inf"),
        ev("INVESTIGATION_START", eFeb, "February 2026"),
        ev("OTHER", "Initial findings indicated a lack of electrical contact between Terminal Block SW#2 within the inhibitor switch of the transmission control valve assembly.", "February 2026", "inh", eFeb),
        ev("FILER_AWARENESS", "On February 20, 2026, Nissan received a field warranty report describing a similar condition.", "February 20, 2026"),
        ev("INVESTIGATION_START", "Nissan initiated a dealership investigation to evaluate the vehicle, to duplicate the concern and to collect data where DTCs P0780 and P0705 were confirmed.", mode="inf"),
        ev("OTHER", "The subject part was collected and returned to the supplier for analysis.", mode="inf"),
        ev("OTHER", eMar, "March 2026"),
        ev("INVESTIGATION_START", "Throughout this month the supplier collected and analyzed a total of five (5) failed parts returned from the field and three (3) failed parts returned from the plant.", "March 2026", "inh", eMar),
        ev("SUPPLIER_NOTICE", "JATCO determined that all verified failed components were manufactured from October 17, 2025 to October 18, 2025.", "March 2026", "inh", eMar),
        ev("OTHER", "A review of the sub-supplier’s manufacturing process for the inhibitor switch found that a locator pin may have broken on the production line on October 17, 2025.", "October 17, 2025"),
        ev("OTHER", "In response, part sorting and yard audits were initiated based on the affected date code.", mode="inf"),
        ev("INVESTIGATION_START", "JATCO conducted traceability analysis to identify control valve assemblies containing suspect inhibitor switches (produced October 17–18, 2025) and link them to specific continuously variable transmissions (CVTs).", mode="inf"),
        ev("OTHER", "The supplier part audit and Smyrna plant vehicle audit identified 76 suspect parts (42 vehicles and 3 CVTs at Nissan North America Smyrna Plant, and 31 control valve assemblies at JATCO Mexico).", mode="inf"),
        ev("INVESTIGATION_START", "At the end of March 2026, Nissan initiated testing and evaluation of suspect parts, including electrical resistance checks, teardown inspections, motor bench testing, and vehicle dynamic testing.", "end of March 2026"),
        ev("OTHER", "Technical analysis confirmed the terminal misalignment of the SW2 slider inside the inhibitor switch resulting in electrical discontinuity.", mode="inf"),
        ev("OTHER", "The subject concern was successfully replicated during both the motor bench and dynamic vehicle testing.", mode="inf"),
        ev("INVESTIGATION_START", eApr, "April 2026 through May 2026"),
        ev("OTHER", "The investigation confirmed that JATCO Mexico was exclusive in utilizing the affected inhibitor switch manufactured at Valeo Thailand.", "April 2026 through May 2026", "inh", eApr),
        ev("OTHER", "While the Kicks and Sentra vehicle models utilize the same transmission assembly line, production records verified that no units for those specific models were manufactured during the identified manufacturing window.", "April 2026 through May 2026", "inh", eApr),
        ev("SUPPLIER_NOTICE", "During this time, the tier-3 supplier confirmed that a total of 4,020 inhibitor switches were made during the identified manufacturing window.", "April 2026 through May 2026", "inh", eApr),
        ev("OTHER", "Traceability data confirmed that the first vehicle built using a transmission made during the identified manufacturing window occurred on January 13, 2026.", "April 2026 through May 2026", "inh", eApr),
        ev("INVESTIGATION_START", "Concurrently, Nissan conducted an internal safety and compliance evaluation of the subject condition.", mode="inf"),
        ev("OTHER", "Nissan identified certain FMVSS requirements related to illumination of the gear selection that may be impacted by this condition.", mode="inf"),
        ev("DECISION", "June 23, 2026 - Nissan decided to conduct a voluntary non-compliance recall on vehicles equipped with the subject control valve assembly in the U.S. market.", "June 23, 2026"),
    ])

add("RCLRPT-26V420-2030.txt", S1_NR, S2_NR,
    C("SUPPORTED", "Due to a deviation in the development process, certain vehicles might not meet the specifications regarding minimum volume level of the pedestrian alert sound."),
    NONE_UP, [
        ev("FILER_AWARENESS", "On June 18, 2026, during an internal compliance review, TEKO identified a potential issue involving the FMVSS No. 141 requirements and began reviewing production, assembly, and vehicle configuration records for the potentially affected vehicle population.", "June 18, 2026"),
        ev("OTHER", "On June 23, 2026, based on that review, TEKO confirmed that certain vehicles may have been delivered for sale without an installed AVAS and evaluated potential corrective and preventive actions.", "June 23, 2026"),
        ev("DECISION", "On June 25, 2026, following approval by executive management, TEKO determined that a noncompliance existed and decided to conduct a voluntary recall to provide and install the AVAS on the affected vehicles.", "June 25, 2026"),
    ])

add("RCLRPT-26V421-6272.txt", S1("Marelli North America"),
    S2ins("Name: Marelli North America", "block"),
    CAUSE_NR, NONE_UP, [
        ev("INVESTIGATION_START", "On April 16, 2026, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into some 2026 MY Ram 1500 vehicles with premium headlamp assemblies (LM6) that may experience intermittent Parking Lamps and DRLs.", "April 16, 2026"),
        ev("OTHER", "From April 2026 through May 2026, FCA US TSRC met with FCA US Engineering to understand root cause, customer consequence and vehicle scope.", "April 2026 through May 2026"),
        ev("INVESTIGATION_START", "From April 2026 through May 2026, FCA US TSRC conducted an analysis of field records and customer assistance records to understand potential customer consequences.", "April 2026 through May 2026"),
        ev("OTHER", "On June 10, 2026, FCA US TSRC organization recognized that a vehicle build issue existed on certain vehicles related to premium headlamp assemblies, potentially resulting in a noncompliance with FMVSS No. 108.", "June 10, 2026"),
        ev("DECISION", "On June 25, 2026, FCA US determined, through the Vehicle Regulations Committee, that a noncompliance to Federal Motor Vehicle Safety Standard No. 108 exists in certain vehicles.", "June 25, 2026"),
    ])

e0617 = "2026-06-17 A production technician brought it to the attention of the Engineering team that a bolt was protruding from the underside of the floor that is above the fuel tank."
add("RCLRPT-26V428-5975.txt", S1_NR, S2_NR,
    C("SUPPORTED", "A mounting bolt for the cot retention system may be too long and therefore contact the fuel line above the fuel tank."),
    NONE_UP, [
        ev("FILER_AWARENESS", e0617, "2026-06-17"),
        ev("INVESTIGATION_START", "An investigation occurred and determined that the bolt may contact the fuel line.", "2026-06-17", "inh", e0617),
        ev("INVESTIGATION_START", "2026-06-18 An analysis of all our ambulance models was conducted, and it was determined that only this model was affected.", "2026-06-18"),
    ])

add("RCLRPT-26V436-4136.txt", S1("Subaru of America, Inc."),
    S2sup("Subaru", "June 30, 2026 – Subaru decided to conduct a non-compliance recall."),
    CAUSE_NR, NONE_UP, [
        ev("FILER_AWARENESS", "May 12, 2026 - Subaru was notified by NHTSA of a potential issue relating to the stated rear axle GAWR on the Part 567 certification label.", "May 12, 2026"),
        ev("OTHER", "June 4, 2026 - Subaru met with NHTSA staff in order to discuss the details of this concern.", "June 4, 2026"),
        ev("INVESTIGATION_START", "June 5, 2026 through June 23, 2026 – Subaru conducted an investigation of the calculated GAWR ratings for all Subaru vehicles dating back to 2003.", "June 5, 2026 through June 23, 2026"),
        ev("DECISION", "June 30, 2026 – Subaru decided to conduct a non-compliance recall.", "June 30, 2026"),
    ])

qH = "On July 1st Wabash Warranty received a recall notice from Hiab advising that four liftgates were delivered to Wabash through 2024 and 2025."
add("RCLRPT-26V449-4273.txt", S1("Hiab USA Inc."), S2sup("Hiab", qH),
    C("SUPPORTED", "The hydraulic cylinders on the MDV liftgates could operate asymmetrically and the platform could move in an uneven fashion."),
    {"kind": "NAMED", "names": ["Hiab"], "quote": qH, "section": "chronology"}, [
        ev("SUPPLIER_NOTICE", qH, "July 1st"),
        ev("INVESTIGATION_START", "July 2nd, a search was completed for all vehicles equipped with the effected models of liftgates all four were matched to vehicles that were delivered to customers between 2024 and 2025.", "July 2nd"),
    ])

add("RCLRPT-26V455-3228.txt", S1("Nissan Shatai Kyusyu Co., Ltd."),
    S2ins("Name: Nissan Shatai Kyusyu Co., Ltd.", "block"),
    CAUSE_NR, NONE_UP, [
        ev("FILER_AWARENESS", "In May 2025, During the development phase of a new vehicle model, Nissan identified a discrepancy between the regulatory language specified in FMVSS 110 and the corresponding NHTSA Test Procedure.", "May 2025"),
        ev("INVESTIGATION_START", "Nissan initiated an investigation into this potential concern.", mode="inf"),
        ev("OTHER", "During the Summer of 2025, an initial review indicated that Nissan’s engineering standards defined requirements based on the original regulatory statement.", "Summer of 2025"),
        ev("OTHER", "By August 2025, Nissan initiated internal discussions regarding the interpretation of the standard (FMVSS 110) and how it relates to the calculation of the GAWR.", "August 2025"),
        ev("INVESTIGATION_START", "In Early 2026, Nissan initiated a comprehensive regulatory assessment to evaluate the potential risk of the calculated GAWR.", "Early 2026"),
        ev("OTHER", "Additionally, a production countermeasure consisting of a revision to the GAWR values printed on the vehicle certification was implemented and a formal label correction notification was issued to the plant.", mode="inf"),
        ev("OTHER", "On March 16, 2026, the revised label countermeasure was successfully adopted into current vehicle production.", "March 16, 2026"),
        ev("INVESTIGATION_START", "April 2026 through May 2026, Nissan initiated a horizontal evaluation to identify the scope of potentially affected vehicles.", "April 2026 through May 2026"),
        ev("OTHER", "In June 2026, Nissan conducted a remedy feasibility study to evaluate the performance, adhesion, and long-term quality of utilizing an overlay label as a field remedy.", "June 2026"),
        ev("OTHER", "Additionally, by the end of June, Nissan concluded the horizontal confirmation audit and confirmed the scope of potentially affected vehicles, including other vehicle model years and export markets.", "end of June"),
        ev("DECISION", "July 8, 2026 - Nissan decided to conduct a voluntary recall campaign to remedy the potentially affected vehicles in the U.S. market.", "July 8, 2026"),
    ])

add("RCLRPT-26V474-5478.txt", S1("HH Technologies"),
    S2ins("Name: HH Technologies", "block"),
    C("SUPPORTED", "Water intrusion has been observed within the high-voltage (HV) cabinet during periods of prolonged heavy rainfall and high humidity."),
    NONE_UP, [
        ev("FILER_AWARENESS", "In March of 2026, Heil service technicians identified the potential for moisture in the control panel to be the root cause of performance interruption and further investigation began.", "March of 2026"),
        ev("OTHER", "Once confirmed, engineering began to address the design and developed an additional sealed compartment that reinforces against moisture ingress.", mode="inf"),
        ev("OTHER", "This design was prototyped and tested in late June, 2026.", "late June, 2026"),
        ev("DECISION", "Furthermore, the consensus was reached that this should be retroactive as opposed to a running change at the end of June (June 25, 2026) triggering this recall.", "June 25, 2026"),
    ])

add("RCLRPT-26V478-7478.txt", S1("GKS GmbH Schliess Systems"),
    S2ins("Name: GKS GmbH Schliess Systems", "block"),
    CAUSE_NR, NONE_UP, [
        ev("FILER_AWARENESS", "In April 2025, BMW became aware of an increasing number of ignition locks on S 1000 RR models replaced under warranty.", "April 2025"),
        ev("INVESTIGATION_START", "An engineering investigation was initiated.", mode="inf"),
        ev("OTHER", "Field parts were requested to be returned for analysis.", mode="inf"),
        ev("INVESTIGATION_START", "Between May and November, parts were returned, and analyzed.", "May and November"),
        ev("OTHER", "Preliminary information suggested that vibration-induced wear on the contact pin within the ignition lock could occur.", mode="inf"),
        ev("INVESTIGATION_START", "Further investigations were initiated as a systematic pattern was not yet clear from an examination of the field cases.", mode="inf"),
        ev("INVESTIGATION_START", "Among other factors, the possible influence of decoupling of the fork bridge was analyzed using NVH profiles, and comparing these profiles with S 1000 RR model updates that had occurred since 2018.", mode="inf"),
        ev("INVESTIGATION_START", "Additional evaluations involved comparing these analyses with other, similar, four- cylinder models.", mode="inf"),
        ev("INVESTIGATION_START", "Between November 2025 and April 2026, the investigation continued, and was focused on analysis of the wear process of the contact pin.", "November 2025 and April 2026"),
        ev("INVESTIGATION_START", "In April 2026, a detailed analysis involving field data, and statistical forecasting, was initiated.", "April 2026"),
        ev("DECISION", "On July 16, 2026, BMW decided to conduct a voluntary safety recall.", "July 16, 2026"),
    ])

qGM = "On April 9, 2026, a GM engineer submitted a report through GM’s Speak Up for Safety (SUFS) program after the wheel supplier notified GM that certain steel wheels may have been shipped to GM’s assembly plant without meeting GM’s internal fatigue-testing requirements."
add("RCLRPT-26V496-1031.txt", S1("Topy America Inc."),
    S2ins(qGM, "chronology"),
    C("SUPPORTED", "A manufacturing process at the supplier to form vent holes in the wheel disc may not have been properly adjusted."),
    {"kind": "UNNAMED", "names": [], "quote": qGM, "section": "chronology"}, [
        ev("FILER_AWARENESS", qGM, "April 9, 2026"),
        ev("INVESTIGATION_START", "GM opened a product investigation on May 19, 2026.", "May 19, 2026"),
        ev("SUPPLIER_NOTICE", "During continuous conformance fatigue testing, the supplier found hairline cracks and traced the condition to the piercing/coining process that forms the outer ring of the vent holes in the wheel disc.", mode="inf"),
        ev("OTHER", "GM’s investigation identified Silverado EV and Sierra EV vehicles that may have received one or more wheels from the supplier’s suspect lots.", mode="inf"),
        ev("DECISION", "On July 23, 2026, GM’s Safety Field Action Decision Authority (SFADA) decided to conduct a safety recall.", "July 23, 2026"),
    ])

eA = "April 20, 2026, during a routine inspection, Autocar personnel identified a unit with missing fasteners at the ABS ECU."
add("RCLRPT-26V501-8521.txt", S1("Autocar"), S2sup("Autocar", eA),
    C("SUPPORTED", "An Autocar manufacturing error resulted in the ABS ECU not properly secured."),
    NONE_UP, [
        ev("FILER_AWARENESS", eA, "April 20, 2026"),
        ev("INVESTIGATION_START", "The unit was corrected and an investigation initiated.", "April 20, 2026", "inh", eA),
        ev("INVESTIGATION_START", "May 12, 2026, through July 10, 2026, the investigation continued.", "May 12, 2026, through July 10, 2026"),
        ev("DECISION", "July 23, 2026, all relevant information was presented to Autocar's management team and out of an abundance of caution, Autocar decided to perform a voluntary Safety Recall for all suspect units.", "July 23, 2026"),
    ])

add("RCLRPT-26V503-1662.txt", S1_NR, S2_NR,
    C("SUPPORTED", "Manufacturing Error."), NONE_UP, [
        ev("FILER_AWARENESS", "On July 24, 2026, Forest River's Office of Corporate Compliance (\"OCC\") was notified that vehicles may have been manufactured without proper overcurrent protection at the house battery that power multiple mini-breakers, feeding multiple 12V components.", "July 24, 2026"),
        ev("OTHER", "On July 28, 2026, OCC and the plant discovered that some vehicles may have been shipped.", "July 28, 2026"),
        ev("DECISION", "On August 3, 2026, Forest Rivers Corporate Committee voted to recall.", "August 3, 2026"),
    ])

add("RCLRPT-26V510-6191.txt",
    {"id": "S1", "status": "NOT_REPORTED", "quote": "Name: See - Seat Belt Assembly Supplier.pdf", "section": "block"},
    S2_NR, CAUSE_NR, NONE_UP, [
        ev("OTHER", "In April 2026, FCA US notified Stellantis Europe S.p.A (\"Stellantis Europe\") of a potential issue related to rear seat belt retractor malfunction concerning 2023-2025 MY Dodge Hornet and 2023- 2026 Alfa Romeo Tonale.", "April 2026"),
        ev("INVESTIGATION_START", "On May 4, 2026, Stellantis Europe opened an investigation related to 2023-2025 Dodge Hornet and 2023-2026 Alfa Romeo Tonale rear seat belt retractor malfunction.", "May 4, 2026"),
        ev("INVESTIGATION_START", "From May 2026 to June 2026, Stellantis Europe Engineering reviewed information related to those claims and looked into the previous topics known in Europe.", "May 2026 to June 2026"),
        ev("OTHER", "On July 1, 2026, Stellantis Europe S.p.A organization recognized that the defect may occur on particular conditions due to a weakness in the design.", "July 1, 2026"),
        ev("DECISION", "On July 30, 2026, Stellantis Europe determined, through the Vehicle Regulations Committee, that a safety defect exists in certain vehicles.", "July 30, 2026"),
    ])

qW = "U. S. Truck Body was advised on 5/18/2026 via email by Waltco Liftgates (Haib USA, Inc.) that the hydraulic liftgates were defective."
add("RCLRPT-26V517-1639.txt", S1("Hiab USA Inc."), S2sup("Waltco Liftgates (Haib USA, Inc.)", qW),
    C("INSUFFICIENT", "Unknown"),
    {"kind": "NAMED", "names": ["Waltco Liftgates", "Haib USA, Inc."], "quote": qW, "section": "chronology"}, [
        ev("SUPPLIER_NOTICE", qW, "5/18/2026"),
    ])

# ---------- build + verify ----------
out, errs = [], []
for fn, s1, s2, cause, up, events in L:
    fl, sec = sections(fn)
    def chk(q, s, what):
        if q == "":
            return
        if len(q) > 300:
            errs.append(f"{fn} {what}: too long {len(q)}")
        if s not in sec or norm(q) not in sec[s]:
            errs.append(f"{fn} {what}: quote not in {s}: {q[:80]}")
    chk(s1["quote"], "block", "S1")
    chk(s2["quote"], s2["section"], "S2")
    chk(cause["quote"], "cause", "cause")
    chk(up["quote"], up["section"], "upstream")
    for i, e in enumerate(events):
        chk(e["quote"], "chronology", f"ev{i}")
        if not e["date_inferred"]:
            ref = e["entry_quote"] if e["inherited_date"] else e["quote"]
            if e["date_text"] not in ref:
                errs.append(f"{fn} ev{i}: date '{e['date_text']}' not in quote")
            if e["inherited_date"]:
                chk(e["entry_quote"], "chronology", f"ev{i} entry")
    out.append({"file": fl, "claims": [s1, s2], "cause": cause, "upstream": up, "events": events})

if errs:
    print("\n".join(errs)); sys.exit(1)
with open(os.path.join(D, "passB.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("ok", len(out), sum(len(o["events"]) for o in out))
