import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TX = os.path.join(HERE, "texts")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def sections(path):
    t = open(path, encoding="utf-8").read()
    fl = re.search(r"^FILE: (.+)$", t, re.M).group(1).strip()
    b = t.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    c = t.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    ch = t.split("=== CHRONOLOGY ===")[1]
    return fl, {"block": norm(b), "cause": norm(c), "chronology": norm(ch)}


def E(d, ty, q):
    return {"date_text": d, "type": ty, "quote": q, "inherited_date": False, "date_inferred": False}


def I(d, ty, q, entry):
    return {"date_text": d, "type": ty, "quote": q, "inherited_date": True, "entry_quote": entry, "date_inferred": False}


def N(ty, q):
    return {"date_text": "", "type": ty, "quote": q, "inherited_date": False, "date_inferred": True}


def S1(status, q):
    return {"id": "S1", "status": status, "quote": q, "section": "block" if q else ""}


def S2(status, q, sec, name=None):
    d = {"id": "S2", "status": status}
    if name:
        d["name"] = name
    d["quote"] = q
    d["section"] = sec
    return d


def C(status, q):
    return {"status": status, "quote": q, "section": "cause" if q else ""}


def U(kind, q, sec, names=None):
    return {"kind": kind, "names": names or [], "quote": q, "section": sec}


L = {}

# 26V193 Lucid
q_lucid_name = "Name: GKN Automotive / Dauch"
L["RCLRPT-26V193-7461.txt"] = dict(
    claims=[S1("SUPPORTED", q_lucid_name), S2("INSUFFICIENT", q_lucid_name, "block")],
    cause=C("SUPPORTED", "The primary cause of the issue was interruption of the torque operations during the adhesive curing window."),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("October 2025", "NHTSA_FILING", "In October 2025, Lucid filed a recall (SR-25-03-0) identifying an affected population of Air Pure RWD vehicles based on a lash detection algorithm that used vehicle telematics data to identify vehicles potentially at risk of a half-shaft disengagement while driving."),
        E("October 2025", "FILER_AWARENESS", "After the October 2025 recall decision was made, Lucid discovered additional vehicles that were not part of the October 2025 recall had experienced half-shaft disengagements."),
        N("OTHER", "The issue of the half-shaft disengagements in non-recalled vehicles was referred to Lucid’s Product Safety Working Group (PSWG) for consideration and evaluation."),
        N("INVESTIGATION_START", "As part of its investigation, the PSWG evaluated the sensitivity of the lash detection algorithm and scope of the October 2025 recall."),
        N("OTHER", "Based on its investigation, the PSWG identified 26 half-shaft issues that occurred on customer vehicles between October 2025 and February 2026 that it attributed to the same root cause as identified in the October 2025 recall."),
        N("INVESTIGATION_START", "Lucid reviewed the total customer incidents."),
        E("March 19, 2026", "OTHER", "The PSWG briefed this issue to Lucid’s Product Safety Executive Council (PSEC) on March 19, 2026."),
        N("DECISION", "The PSEC decided that there was an unreasonable risk to safety for Air Pure RWD vehicles manufactured before the July 25, 2025 clean point"),
    ])

# 26V203 Toyota
q = "Name: Denso Corporation"
L["RCLRPT-26V203-3945.txt"] = dict(
    claims=[S1("SUPPORTED", q), S2("INSUFFICIENT", q, "block")],
    cause=C("NOT_REPORTED", ""),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("June through September 2025", "INVESTIGATION_START", "From June through September 2025, Toyota reviewed different vehicle models equipped with a single speaker AVAS, that may have a certain software configuration"),
        E("May 2025", "FILER_AWARENESS", "because an internal evaluation test in May 2025 identified that a future model equipped with a single speaker AVAS and this software configuration did not meet the minimum requirements for other markets."),
        N("INVESTIGATION_START", "Thus, during this period, Toyota performed testing on these models and found that each of the test vehicles representing those models met the applicable requirements of FMVSS No. 141."),
        N("INVESTIGATION_START", "However, Toyota decided to conduct additional testing on the subject vehicles because, while the test vehicle met the FMVSS No. 141 targets, it did not meet Toyota’s internal margin targets."),
        E("October 2025", "INVESTIGATION_START", "In October 2025, Toyota performed on-vehicle sound verification testing using additional subject vehicles in each trim variation (which have different vehicle characteristics) to confirm the performance."),
        E("March 25, 2026", "DECISION", "After analysis of the test results and confirmation of the testing parameters/data, on March 25, 2026, Toyota determined that the vehicles identified in Section 3 above may not meet the reverse sound pressure level requirements specified in FMVSS No. 141, paragraph S5.2, Table 6."),
    ])

# 26V204 Ford wiper
q = "Ford also reviewed the supplier’s historic production data, including dimensional data."
L["RCLRPT-26V204-7221.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: TRICO COMPONENTES SA DE CV"), S2("INSUFFICIENT", q, "chronology")],
    cause=C("SUPPORTED", "The windshield wiper arm´s latch retention plate may have been incorrectly staked at the supplier."),
    upstream=U("UNNAMED", q, "chronology"),
    events=[
        E("January 15, 2026", "INVESTIGATION_START", "On January 15, 2026, an issue pertaining to stripped windshield wiper arm splines on certain Expedition and Navigator vehicles was brought to Ford´s Critical Concern Review Group for review."),
        E("2024", "FILER_AWARENESS", "which was conducted pursuant to the three-year recall lookback initiated as part of the Consent Order entered into by Ford and NHTSA in 2024, Ford observed an elevated warranty claim rate for Expedition and Navigator vehicles"),
        E("January and February 2026", "INVESTIGATION_START", "During January and February 2026, Ford conducted a read-across and assessed field performance data for vehicles that share the same knurl driver design and supplier."),
        N("INVESTIGATION_START", "Additionally, the team inspected field return parts to evaluate conformance to dimensional specifications, conducted Computer Aided Engineering stress analysis, and reproduced the failure of the returned parts."),
        N("INVESTIGATION_START", q),
        N("INVESTIGATION_START", "Based on the read-across findings, Ford expanded the investigation to include Super Duty vehicles manufactured within the same period as the suspect population of Expedition and Navigator vehicles."),
        E("March 2026", "OTHER", "In March 2026, the root cause was determined to be a combination of conditions that led to incorrect teeth engagement in the arm head-to-knurl interface"),
        N("OTHER", "Supplier records confirmed that the combination of conditions was present in Expedition, Navigator and Super Duty vehicles."),
        N("OTHER", "Ford verified these findings through statistical life warranty projections."),
        E("December 2022", "OTHER", "An improvement in production processes at the supplier in December 2022 addressed the issues that led to the defective wiper arms."),
        E("March 24, 2026", "DECISION", "On March 24, 2026, Ford’s Field Review Committee reviewed the concern and approved a field service action."),
    ])

# 26V205 Ford circlips
L["RCLRPT-26V205-4042.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Ford Motor Company"), S2("SUPPORTED", "On March 3, 2026, this was brought to Ford's Critical Concern Review Group (CCRG) for review.", "chronology", "Ford")],
    cause=C("SUPPORTED", "The equipment used to install piston circlips at the engine assembly plant was misaligned during circlip installation for a period of production."),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("February 24, 2026", "FILER_AWARENESS", "On February 24, 2026, manufacturing team members from Ford’s Dearborn Engine & Fuel Tank Plant (DEFTP) identified an engine with missing piston circlips during engine teardown performed as part of standard production audit testing."),
        E("March 3, 2026", "INVESTIGATION_START", "On March 3, 2026, this was brought to Ford's Critical Concern Review Group (CCRG) for review."),
        N("OTHER", "The investigation team determined the missing circlips resulted from a period of engine production in which the equipment used to install the clips was misaligned."),
        N("OTHER", "Additionally, during this period, the error-proofing station that inspects for circlip presence experienced a broken transducer which prevented the issue from being detected initially."),
        N("INVESTIGATION_START", "The CCRG and DEFTP team members reviewed engine plant and vehicle assembly plant production records as part of the investigation to determine the population of engines produced during this time and the vehicles they were installed in."),
        E("March 24, 2026", "DECISION", "On March 24, 2026, Ford's Field Review Committee reviewed the concern and approved a field action."),
    ])

# 26V213 GM Valeo
q = "GM’s investigation determined that, in October 2024, the rear-lamp assembly supplier made a software change to assist technicians performing a tire pressure monitor system (TPMS) learn process."
L["RCLRPT-26V213-6780.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Valeo Lighting Systems North America LLC"), S2("INSUFFICIENT", q, "chronology")],
    cause=C("SUPPORTED", "In October 2024, the rear-lamp assembly supplier made a software change to assist technicians performing a tire pressure monitor system (TPMS) learn process."),
    upstream=U("UNNAMED", q, "chronology"),
    events=[
        E("December 9, 2025", "FILER_AWARENESS", "On December 9, 2025, a GM employee submitted a report to GM’s Speak Up for Safety (SUFS) system following validation testing for the 2027 model year Corvette."),
        N("OTHER", "During the test, the vehicle failed to detect and notify the driver of an inoperative rear turn signal lamp."),
        E("January 27, 2026", "INVESTIGATION_START", "GM opened a product investigation on January 27, 2026."),
        E("October 2024", "OTHER", q),
        E("March 26, 2026", "DECISION", "GM’s Safety Field Action Decision Authority (SFADA) decided to conduct a noncompliance recall on March 26, 2026."),
    ])

# 26V215 Autocar
L["RCLRPT-26V215-9936.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Autocar"), S2("SUPPORTED", "February 10, 2026, during a routine internal inspection, Autocar personnel identified a defective unit.", "chronology", "Autocar")],
    cause=C("SUPPORTED", "An Autocar manufacturing error resulted in incorrect assembly of the winter front cover."),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("February 10, 2026", "FILER_AWARENESS", "February 10, 2026, during a routine internal inspection, Autocar personnel identified a defective unit."),
        E("February 11, 2026", "INVESTIGATION_START", "February 11, 2026, an investigation was initiated and continued through March 25, 2026, and a clean point established for production."),
        E("March 25, 2026", "OTHER", "February 11, 2026, an investigation was initiated and continued through March 25, 2026, and a clean point established for production."),
        E("March 26, 2026", "DECISION", "March 26, 2026, the investigation was concluded and all relevant information was presented to Autocar's management team, out of an abundance of caution, Autocar decided to perform a voluntary Safety Recall for all affected vehicles."),
    ])

# 26V236 Ford Bronco
L["RCLRPT-26V236-1914.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Ford Motor Company"), S2("SUPPORTED", "On December 4, 2025, this concern was brought into Ford’s Critical Concern Review Group (CCRG) for review.", "chronology", "Ford")],
    cause=C("SUPPORTED", "During a prior service repair, the joint between the transmission and transfer case was misaligned when the transmission was reassembled."),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("November 2025", "FILER_AWARENESS", "In November 2025, Ford assessed warranty claims related to transmission output shaft spline wear and transfer case input spline wear on 2022-2023 model year (MY) Bronco vehicles."),
        E("December 4, 2025", "INVESTIGATION_START", "On December 4, 2025, this concern was brought into Ford’s Critical Concern Review Group (CCRG) for review."),
        E("December 2025", "FILER_AWARENESS", "In December 2025, the CCRG’s investigation identified additional reports of similar spline wear in 2021- 2025MY vehicles, including reports describing a loss of power while driving and loss of park pawl engagement."),
        N("OTHER", "The CCRG identified a strong correlation between spline wear reports and a history of documented service repairs involving the removal of the transmission or transfer case."),
        E("January and February 2026", "INVESTIGATION_START", "During January and February 2026, the CCRG analyzed returned parts, completed computer-aided engineering (CAE) simulations, and conducted physical testing to conclude the root cause of the spline wear is misalignment in the joint between the transfer case and transmission."),
        N("OTHER", "Physical vehicle testing found that an induced misalignment in this joint resulted in spline wear patterns consistent with those observed on warranty failures in the field."),
        E("February 26, 2026", "OTHER", "On February 26, 2026, Ford’s workshop manuals were updated to ensure that the transmission and transfer case are properly aligned when they are reassembled during service repairs."),
        N("INVESTIGATION_START", "The CCRG searched warranty data on Bronco vehicle production until the workshop manual update and found 4,922 Bronco vehicles in the US with documented transmission or transfer case-related repairs during this time period."),
        E("April 7, 2026", "DECISION", "On April 7, 2026, Ford’s Field Review Committee reviewed the concern and approved a field service action."),
    ])

# 26V238 Ford Ranger sunvisor
q = "During November and December 2025, the CCRG reviewed wiring harness specifications and installation procedures of the sunvisor and headliner suppliers with two notable findings."
L["RCLRPT-26V238-6269.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Versigent"), S2("INSUFFICIENT", q, "chronology")],
    cause=C("SUPPORTED", "The sunvisor or headliner wiring harnesses may become damaged as the result of excessive harness tape thickness or improper harness positioning during install."),
    upstream=U("UNNAMED", q, "chronology"),
    events=[
        E("October 31, 2025", "FILER_AWARENESS", "On October 31, 2025, Ford reviewed inspection results from a fire in the right A-pillar area on a 2024 model year (MY) Ranger vehicle."),
        E("November 6, 2025", "INVESTIGATION_START", "On November 6, 2025, this concern was brought into Ford’s Critical Concern Review Group (CCRG) for review."),
        E("November and December 2025", "INVESTIGATION_START", q),
        N("OTHER", "Firstly, supplier control records showed a thickness of protective tape around the headliner wiring circuit that exceeded the width of a section of a sheet metal opening where the wiring passed through."),
        E("January and February 2026", "INVESTIGATION_START", "In January and February 2026, the CCRG conducted flammability assessment testing that showed all potentially affected materials met flammability requirements and were not combustible."),
        N("OTHER", "However, analysis of the electrical system design indicated that repetitive Body Control Module (BCM) re-starts after the sunvisor lamp circuit DTC is set may cause repeated shorts and arcing over time, building up soot and eventually causing fire."),
        E("April 7, 2026", "DECISION", "On April 7, 2026, Ford’s Field Review Committee reviewed the concern and approved a field service action."),
    ])

# 26V245 Blue Bird
ent = "January 2026: Blue Bird had a meeting with Transport Canada to understand windshield wiper issues they found during an inspection."
qs = "Blue Bird started its internal investigation to evaluate if the issue was related to a supplier quality spill or an internal assembly process."
L["RCLRPT-26V245-1061.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Blue Bird"), S2("SUPPORTED", ent, "chronology", "Blue Bird")],
    cause=C("SUPPORTED", "As a result of a non-conformance in the manufacturing protocol, the securing nuts on the all-weather wiper blade assemblies may not have been properly tightened."),
    upstream=U("UNNAMED", qs, "chronology"),
    events=[
        E("January 2026", "FILER_AWARENESS", ent),
        I("January 2026", "INVESTIGATION_START", qs, ent),
        E("March 2026", "OTHER", "March 2026: Blue Bird informed Transport Canada that the issue was assembly process related and was identifying the impacted population."),
        E("April 2026", "NHTSA_FILING", "April 2026: Blue Bird submitted a defect report."),
    ])

# 26V253 Hexagon Purus
q = "December 2025 – A third party test laboratory that was engaged by Hexagon Purus to conduct"
L["RCLRPT-26V253-0939.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Hexagon Purus"), S2("SUPPORTED", q, "chronology", "Hexagon Purus")],
    cause=C("SUPPORTED", "The primary and secondary air pressure sensors are being incorrectly translated and displayed to the driver."),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[E("December 2025", "OTHER", q)])

# 26V262 FCA
q = "Name: Valeo North America"
L["RCLRPT-26V262-9341.txt"] = dict(
    claims=[S1("SUPPORTED", q), S2("INSUFFICIENT", q, "block")],
    cause=C("NOT_REPORTED", ""),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("March 10, 2026", "INVESTIGATION_START", "On March 10, 2026, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into inoperative instrument panel clusters in 2024- 2025 MY Jeep Wagoneer S and Dodge Charger Daytona vehicles."),
        E("March 2026 and April 2026", "OTHER", "Between March 2026 and April 2026, FCA US TSRC met with FCA US Engineering to review the issue, understand potential failure modes, and to determine the suspect population."),
        E("April 1, 2026", "OTHER", "On April 1, 2026, FCA US TSRC organization recognized that a vehicle build issue existed on certain vehicles related to inoperative instrument panel clusters potentially resulting in a noncompliance with FMVSS Nos. 571.108, 571.126, 571.135, 571.138, and 571.208."),
        E("April 16, 2026", "DECISION", "On April 16, 2026, FCA US determined, through the Vehicle Regulations Committee, that noncompliances to various Federal Motor Vehicle Safety Standards exist in certain vehicles."),
    ])

# 26V263 JLR
q = "On 27 March 2026, following information received from the fuel tank supplier that a fuel tank had failed the end-of-line leak test, a Product Safety and Compliance Committee (PSCC) investigation was opened."
L["RCLRPT-26V263-6693.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: OP Mobility"), S2("INSUFFICIENT", q, "chronology")],
    cause=C("NOT_REPORTED", ""),
    upstream=U("UNNAMED", q, "chronology"),
    events=[
        E("27 March 2026", "SUPPLIER_NOTICE", q),
        N("OTHER", "The PSCC heard that the affected tank had been quarantined and not supplied to JLR for use in series production, but that analysis was ongoing at the supplier to establish the risk to fuel tanks in the remainder of the batch."),
        E("10 April 2026", "OTHER", "On 10 April 2026, following completion of testing and analysis at the supplier, JLR’s PSCC reconvened to discuss the results."),
        N("OTHER", "The PSCC was informed that anomalous material extrusion results had been detected in a number of fuel tanks and, whilst they had passed their end-of-line leak tests, it was likely that the wall thickness was below the intended specification."),
        N("OTHER", "It was confirmed that these tanks had been used in series vehicle production, and work was started to establish the locations of the affected vehicles and the matter was referred to the PSCC Decision Forum."),
        E("16 April 2026", "DECISION", "On 16 April 2026, the PSCC Decision Forum met and instructed a safety recall be launched to remedy the identified vehicles."),
    ])

# 26V268 Ford seat bolts
q = "Upon investigation, CCRG discovered the torque check at the supplier was performed before the thread adhesive patch was fully cured, preventing full effectiveness of the adhesive patch."
L["RCLRPT-26V268-9028.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Magna Seating Inc."), S2("INSUFFICIENT", q, "chronology")],
    cause=C("SUPPORTED", "The seat structure assembly supplier initiated a process to check the torque of the front seat frame height adjustment pivot bolts."),
    upstream=U("UNNAMED", q, "chronology"),
    events=[
        E("October 17, 2025", "DECISION", "On October 17, 2025, Ford approved safety recall 25SB5 (NHTSA 25V721) to address a population of vehicles produced from 2020 to 2022 with front seat pivot bolts that may be loose."),
        N("OTHER", "Ford’s Critical Concern Review Group (CCRG) continued to monitor an additional population of vehicles that were produced in 2024 and 2025 during the time a torque check for the front seat pivot bolts was in place at the seat structure assembly supplier."),
        E("March 13, 2026", "FILER_AWARENESS", "On March 13, 2026, the CCRG confirmed an increasing number of warranty reports for the monitor period."),
        N("OTHER", q),
        N("INVESTIGATION_START", "The CCRG investigation studied the design and performance of the joint and determined that the compromised thread adhesive patch, in conjunction with vibration associated with road loads, may result in a reduced break-way torque that can lead to loosening of the front seat pivot bolts."),
        E("April 21, 2026", "DECISION", "On April 21, 2026, Ford’s Field Review Committee reviewed the concern and approved a field service action."),
    ])

# 26V271 Roadtrek
L["RCLRPT-26V271-4869.txt"] = dict(
    claims=[S1("NOT_REPORTED", ""), S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "The catch's outside diameter is bigger than the inside diameter (mating surface) of the primary safety latch."),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("09thApril2026", "FILER_AWARENESS", "Upon hearing about on social media (Facebook) in an RV group on 09thApril2026, S&W department brought the concern to Roadtrek Engineering department."),
        N("INVESTIGATION_START", "After further investigation was completed and it was determined under high wind and/or bumpy road condition the primary latching mechanism potentially becomes disengaged."),
    ])

# 26V272 Newmar
L["RCLRPT-26V272-8617.txt"] = dict(
    claims=[S1("NOT_REPORTED", ""), S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "The screws used to secure the chin spoiler may lose torque over time, which can cause the chin spoiler to loosen or detach."),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("3/25/26", "FILER_AWARENESS", "Newmar received a field report on 3/25/26 indicating a chin spoiler had loosened and detached on a Freedom Aire unit."),
        N("INVESTIGATION_START", "Newmar initiated an investigation and identified additional report of chin spoiler loosening."),
        E("3/25/26", "OTHER", "A production change was implemented on 3/25/26 to replace screws with pop-rivets."),
        E("12/16/25", "FILER_AWARENESS", "In addition to the field report on 3/25/26, Newmar is aware of one additional service claim for a loose chin spoiler on 12/16/25."),
        E("4/21/26", "OTHER", "Following internal review, a Brand Action Committee met on 4/21/26 and determined the issue should go to Product Safety Committee."),
        E("4/22/26", "DECISION", "The Product Safety Committee met on 4/22/26 and determined a safety defect exists and initiated this recall."),
    ])

# 26V279 New Flyer
q = "17-Apr-2026, during Early Warning Report generation, a Field Report from Mar-2026 was identified that indicated the dash lamps were not illuminated during night-run on an order of buses."
L["RCLRPT-26V279-2878.txt"] = dict(
    claims=[S1("NOT_REPORTED", ""), S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "The programming used an incorrect signal which did not illuminate the speedometer."),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("17-Apr-2026", "FILER_AWARENESS", q),
        E("Mar-2026", "FILER_AWARENESS", q),
        E("20 to 24-Apr-2026", "INVESTIGATION_START", "20 to 24-Apr-2026 information was gathered to verify the issue and was determined to be an incorrect program."),
        E("27-Apr-2026", "DECISION", "27-Apr-2026 the issue was raised to the Vehicle Safety Committee culminating in a consensus to issue a noncompliance recall."),
    ])

# 26V295 Forest River
ent = "May 4, 2026, Forest River’s office of Corporate Compliance was notified of a concern that was discovered at the factory when changing an interior panel that had been damaged in manufacturing."
L["RCLRPT-26V295-7913.txt"] = dict(
    claims=[S1("NOT_REPORTED", ""), S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "Manufacturing Error."),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("May 4, 2026", "FILER_AWARENESS", ent),
        I("May 4, 2026", "OTHER", "When they removed the panel, they found the vent pipe was not plumbed all the way through the roof of the vehicle.", ent),
        I("May 4, 2026", "INVESTIGATION_START", "The same day, the manufacturing plant notified OCC of concern; OCC opened a research item.", ent),
        E("May 11, 2026", "DECISION", "On May 11, 2026, Forest River’s Corporate Committee voted to recall."),
    ])

# 26V307 Hyundai ARC
qarc = "September – Hyundai’s North America Safety Office (“NASO”) received ARC’s response and files under the provisions of the Protective Agreement issued on August 24, 2023, in EA16-003."
e_oct = "October – NASO engaged Northrup Grumman (“NG”) for airbag inflator condition/performance investigation support."
e_nov = "November – NASO engaged a third-party for support in recovering airbag inflators for study from recyclers across the U.S."
e_dec19 = "December 19 – Hyundai submitted its response to NHTSA’s Initial Decision issued in EA16-003."
e_janfeb24 = "January through February – NASO began preparation for on-site inspection procedures of recovery parts with its Safety Testing & Investigation Laboratory (“STIL”)."
e_aprjun = "April through June – NASO continued recovering parts for analysis by the STIL and procured the supplier approval drawings associated with the subject inflators."
e_jul29 = "July 29 – NASO began preparing to execute recovery parts forwarding to NG for dissection and analysis."
e_augdec = "August through December – The STIL began shipping specifically selected inflators based on propellant condition or anomalies, such as weld flash to NG."
e_novdec = "November through December – NG informed NASO of preliminary findings, which included scans of abnormal propellant appearance and non-homogeneous structure in some inflators."
e_janmar = "January through March – NG continued investigative activities into abnormal propellant identified through recovery part dissections, including 3D volumetric density measurement, FTIR analysis, and micro-CT scans."
e_apraug = "April through August – NG continued its investigation through crush and closed-bomb testing of lower-density propellant wafers."
e_janfeb26 = "January through February – NG continued with validation efforts of its analysis findings."
e_marapr = "March through April – The STIL performed 60-L tank deployment testing on inflators obtained from suspect production lots confirmed by ARC."
L["RCLRPT-26V307-4656.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: ARC Automotive, Inc."), S2("SUPPORTED", qarc, "chronology", "ARC")],
    cause=C("INSUFFICIENT", "Root cause is under investigation."),
    upstream=U("NAMED", qarc, "chronology", ["ARC"]),
    events=[
        E("September", "SUPPLIER_NOTICE", qarc),
        E("August 24, 2023", "OTHER", qarc),
        I("September", "INVESTIGATION_START", "NASO began investigating potential impact to U.S. market vehicles equipped with dual-stage hybrid inflators produced by ARC, monitoring field data and establishing routine (weekly) reviews of airbag-related claims and customer complaints.", qarc),
        E("October", "OTHER", e_oct),
        E("October 23, 2023", "OTHER", "An initial meeting to develop and review the full investigation plan was held with NG on October 23, 2023."),
        E("November", "OTHER", e_nov),
        I("November", "OTHER", "The initial target for recovery was set to 1,000 units from specific vehicles grades/trims.", e_nov),
        E("December 14", "OTHER", "December 14 – NASO met with NHTSA’s Office of Defects Investigation (“ODI”) for a full update of its investigation plan and planned partnerships."),
        E("December 19", "OTHER", e_dec19),
        I("December 19", "OTHER", "Hyundai also joined the Comments of Safety Professionals filed on the same date.", e_dec19),
        E("January through February", "INVESTIGATION_START", e_janfeb24),
        I("January through February", "OTHER", "100 parts were recovered during this period.", e_janfeb24),
        E("March 13", "OTHER", "March 13 – The STIL developed and implemented advanced CT methodologies based on input from Northrop Grumman, focusing on gray value and weld flash."),
        E("April 10", "OTHER", "April 10 – NASO met with ODI for an update of its findings to date."),
        E("April through June", "OTHER", e_aprjun),
        E("June-end", "OTHER", "By June-end, over 800 inflators were recovered for study."),
        E("July 29", "OTHER", e_jul29),
        I("July 29", "OTHER", "Joint weekly meetings to review findings and parts logistics were initiated.", e_jul29),
        E("August through December", "OTHER", e_augdec),
        I("August through December", "OTHER", "Additionally, an estimated 30 parts were sent to Baker Hughes, to validate STIL CT scanning capabilities.", e_augdec),
        E("October", "OTHER", "October – Hyundai submitted its response to NHTSA’s Supplemental Initial Decision issued in EA16-003."),
        E("November through December", "OTHER", e_novdec),
        E("December 3", "OTHER", "NASO visited NG’s inspection facilities to confirm dissection procedures and findings on December 3."),
        E("January 5", "OTHER", "January 5 – NASO requested information from ARC regarding propellant observations based on initial findings from Northrup Grumman."),
        E("January through March", "INVESTIGATION_START", e_janmar),
        I("January through March", "OTHER", "During this period, all identified abnormal propellant wafers could be traced to a specific production lot.", e_janmar),
        E("March 17", "OTHER", "March 17 – NASO met with ARC to review its preliminary findings."),
        E("April through August", "INVESTIGATION_START", e_apraug),
        I("April through August", "OTHER", "Initial findings indicated lower mechanical strength and faster burn rate in these wafers.", e_apraug),
        E("September 16", "OTHER", "September 16 – Identified low-density wafers from suspect production lots were forwarded by NG to ARC for further analysis."),
        E("September 17", "OTHER", "September 17 – NASO met with ODI for an update of its findings to date."),
        E("October through November", "OTHER", "October through November – NASO continued meeting with ARC to review recovery part analysis findings and the results of replication testing performed by ARC."),
        E("December 16", "OTHER", "December 16 – NASO initiated a special customer outreach to owners with vehicles known to contain inflators from specific production lots."),
        E("January through February", "INVESTIGATION_START", e_janfeb26),
        I("January through February", "OTHER", "NASO continued meeting with ARC to review and complete open investigation action items.", e_janfeb26),
        I("January through February", "SUPPLIER_NOTICE", "During this period, ARC acknowledged lower-density propellant wafer production limited to certain lots", e_janfeb26),
        E("February 17", "OTHER", "February 17 – NASO met with NG to discuss findings to date."),
        E("March through April", "INVESTIGATION_START", e_marapr),
        E("April 30", "OTHER", "The STIL’s findings were shared with NASO on April 30."),
        E("May 7", "DECISION", "May 7 – Based on its investigation findings to date, including the recent tank testing performed at the STIL, NASO’s North America Safety Decision Authority (“NASDA”) convened to review the complete findings and decided to conduct a safety recall of affected vehicles in the U.S."),
        E("July 10", "NHTSA_FILING", "July 10 - Based on updated information regarding remedy availability, Hyundai is amending the current remedy notification schedule."),
    ])

# 26V310 Altec
q = "On April 8, 2026, Altec identified that on a unit in production equipped with ePTO that the emergency stop at the ground controls did not function to disable all hydraulic functions when activated."
L["RCLRPT-26V310-8416.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Altec Industries Inc."), S2("SUPPORTED", q, "chronology", "Altec")],
    cause=C("NOT_REPORTED", ""),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("April 8, 2026", "FILER_AWARENESS", q),
        N("INVESTIGATION_START", "Altec opened a root cause investigation to determine the cause of the issue."),
        N("OTHER", "Altec identified that the unit had been wired incorrectly and that the schematics on the affected unit had the incorrect wiring harness design."),
        E("April 16, 2026", "INVESTIGATION_START", "On April 16, 2026, after determining the cause of the issue, a potential field action investigation was opened to determine whether risk to units in the field existed and to identify all units potentially affected by the harness design."),
        E("May 8, 2026", "DECISION", "On May 8, 2026, Altec determined that an issue existed in units in the field, and unit owners should be notified."),
    ])

# 26V313 Keystone / Lippert
ent = "05/08/2026 – Report was made."
qlci = "LCI notified Keystone RV that they have identified a potential concern involving shock bolts on the Curt Touring Suspension System installed on specific Lippert chassis."
L["RCLRPT-26V313-6868.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Lippert"), S2("SUPPORTED", qlci, "chronology", "LCI")],
    cause=C("SUPPORTED", "Improperly torqued shock bolts may damage or break the bolt if over torqued and may vibrate loose if under torqued."),
    upstream=U("NAMED", qlci, "chronology", ["LCI", "Lippert"]),
    events=[
        E("05/08/2026", "FILER_AWARENESS", ent),
        I("05/08/2026", "SUPPLIER_NOTICE", qlci, ent),
        I("05/08/2026", "OTHER", "Sporadic instances of improper torque have been identified.", ent),
        E("05/08/2026", "INVESTIGATION_START", "05/08/2026 – Investigation opened to determine scope and range of units affected."),
        E("05/15/2026", "DECISION", "05/15/2026 – Keystone Safety Committee reviewed the information and concluded that the data reviewed indicated a unanimous vote for a voluntary recall."),
        E("05/15/2026", "OTHER", "05/15/2026 – Investigation concluded and scope completed."),
    ])

# 26V323 Wabash
ent = "4/21/2026 - Wabash learned that a customer was cited for missing conspicuity material on the rear of the trailer."
L["RCLRPT-26V323-5712.txt"] = dict(
    claims=[S1("NOT_REPORTED", ""), S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "Conspicuity tape was inadvertently omitted from affected platform trailers."),
    upstream=U("NONE_MENTIONED", "", ""),
    events=[
        E("4/21/2026", "FILER_AWARENESS", ent),
        I("4/21/2026", "INVESTIGATION_START", "The concern was entered into Wabash’s quality system for review.", ent),
        E("4/22/2026", "INVESTIGATION_START", "4/22/2026 - Wabash reviewed photographs from the customer and noted the absence of conspicuity tape across the width of the rear deck."),
        E("4/23-5/14/2026", "INVESTIGATION_START", "4/23-5/14/2026 - Wabash investigated warranty, sales, and manufacturing information and escalated the issue to the Product Safety Committee to evaluate compliance with FMVSS 108 and the potential scope of the issue."),
        E("5/15/2026", "DECISION", "5/15/2026 - Based on the Product Safety Committee’s investigation, Wabash determined that the affected populations of trailers may not comply with FMVSS 108 S8.2."),
    ])

# 26V325 GM Joyson
q = "On May 14, 2026, GM’s Safety Field Action Decision Authority (SFADA) decided to conduct a safety recall of RRAB containing inflators from the same supplier production lot (D273A) as the Silverado field incident."
L["RCLRPT-26V325-1775.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Joyson Safety Systems"), S2("INSUFFICIENT", q, "chronology")],
    cause=C("SUPPORTED", "GM believes the root cause relates to two potential supplier manufacturing defects occurring together— a small crack in the inflator canister introduced during manufacturing along with a small amount of water inadvertently being left in the canister after the washing process"),
    upstream=U("UNNAMED", q, "chronology"),
    events=[
        E("April 13, 2026", "FILER_AWARENESS", "On April 13, 2026, a GM investigator submitted a report to GM’s Speak Up For Safety (SUFS) program following a report from a dealer that a 2019 Chevrolet Silverado experienced a potential rupture of the right-side roof-rail airbag (RRAB) while the vehicle was parked and unattended."),
        E("May 14, 2026", "DECISION", q),
        E("June 22, 2026", "FILER_AWARENESS", "On June 22, 2026, GM become aware of a potential rupture of the left-side RRAB in a 2018 Chevrolet Silverado while the vehicle was parked and unattended."),
        E("August 6, 2026", "DECISION", "On August 6, 2026, GM's SFADA decided to expand the prior safety recall to include vehicles built with RRABs containing inflators from supplier production lot C314B."),
    ])

# 26V333 Coach and Equipment
q = "The Q'Straint company, (the equipment manufacturer) issued a recall #22E022 for defective QRT-360 Wheelchair Restraints."
L["RCLRPT-26V333-4875.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Q'Straint"), S2("SUPPORTED", q, "chronology", "Q'Straint")],
    cause=C("SUPPORTED", "The retractor auto-lock function fails."),
    upstream=U("NAMED", q, "chronology", ["Q'Straint"]),
    events=[
        N("OTHER", q),
        E("5/19/2026", "SUPPLIER_NOTICE", "We received the recall notification letter 5/19/2026."),
        E("5/20/2026", "DECISION", "We as the vehicle manufacturer are required to issue a recall for the vehicles involved and started the recall process on 5/20/2026."),
    ])

# 26V347 Forest River Bus
q = "On May 14, 2026, Forest River's Office of Corporate Compliance was notified by Q'Straint, that they would be recalling certain retractor products."
L["RCLRPT-26V347-0355.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Q'Straint"), S2("SUPPORTED", q, "chronology", "Q'Straint")],
    cause=C("INSUFFICIENT", "Unknown - Vendor Recall."),
    upstream=U("NAMED", q, "chronology", ["Q'Straint"]),
    events=[
        E("May 14, 2026", "SUPPLIER_NOTICE", q),
        E("May 18, 2026", "INVESTIGATION_START", "On May 18, 2026, research began into finding out which brands used Q'Straints products within their defined dates of recall."),
        E("May 26, 2026", "OTHER", "On May 26, 2026, OCC and the plant confirmed the vehicles and usage of the recalled components."),
        E("August 14, 2026", "FILER_AWARENESS", "On August 14, 2026 NHTSA reached out to Forest River's Office of Corporate Compliance about additional units in the recall."),
        N("OTHER", "Forest River responded that ongoing research was happening."),
        E("August 27, 2026", "OTHER", "On August 27, 2026 Research concluded and Forest River's Office of Corporate Compliance was able to identify units that are being added to the recall."),
    ])

# 26V349 ARBOC
q = "14-May-2026: ARBOC was formally advised by Q’Straint – supplier of the suspect restraints – that an equipment recall had been issued (26E022) due to some restraints distributed to ARBOC may not fully lock."
L["RCLRPT-26V349-0404.txt"] = dict(
    claims=[S1("SUPPORTED", "Name: Q'Straint"), S2("SUPPORTED", q, "chronology", "Q’Straint")],
    cause=C("SUPPORTED", "Sticking of the auto release function due to interference between internal components."),
    upstream=U("NAMED", q, "chronology", ["Q’Straint"]),
    events=[
        E("14-May-2026", "SUPPLIER_NOTICE", q),
        E("14-May-2026", "OTHER", "14-May-2026: ARBOC discussed the issue with Q’Straint telephonically to get clarity on the check/test method."),
        E("15-May-2026", "INVESTIGATION_START", "15-May-2026: ARBOC begins to confirm what buses may be affected by the suspect restraints."),
        E("22-May-2026", "DECISION", "22-May-2026: ARBOC holds a Special Safety Committee meeting; concurrence was provided to issue this recall."),
    ])


def main():
    out, errs = [], []
    files = sorted(f for f in os.listdir(TX) if f.startswith("RCLRPT") and f.endswith(".txt"))
    for f in files:
        fl, sec = sections(os.path.join(TX, f))
        lab = L[f]

        def chk(q, s, where):
            if not q:
                return
            if len(q) > 300:
                errs.append(f"{f} {where}: too long {len(q)}")
            if s not in sec or norm(q) not in sec[s]:
                errs.append(f"{f} {where}: quote not in {s}: {q[:80]}")

        for c in lab["claims"]:
            chk(c["quote"], c["section"], c["id"])
        chk(lab["cause"]["quote"], "cause", "cause")
        chk(lab["upstream"]["quote"], lab["upstream"]["section"], "upstream")
        for i, e in enumerate(lab["events"]):
            chk(e["quote"], "chronology", f"ev{i}")
            if e["date_text"] and e["date_text"] not in e["quote"] and not e["inherited_date"]:
                errs.append(f"{f} ev{i}: date not in quote")
            if e["inherited_date"]:
                chk(e["entry_quote"], "chronology", f"ev{i}-entry")
                if e["date_text"] not in e["entry_quote"]:
                    errs.append(f"{f} ev{i}: date not in entry quote")
        out.append({"file": fl, "claims": lab["claims"], "cause": lab["cause"],
                    "upstream": lab["upstream"], "events": lab["events"]})
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    with open(os.path.join(HERE, "passB.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("ok", len(out), sum(len(o["events"]) for o in out))


main()
