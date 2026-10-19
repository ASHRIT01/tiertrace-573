import json, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def sections(path):
    txt = open(path, encoding="utf-8").read()
    f = re.search(r"^FILE: (.+)$", txt, re.M).group(1).strip()
    b = txt.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    c = txt.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    ch = txt.split("=== CHRONOLOGY ===")[1]
    return f, {"block": norm(b), "cause": norm(c), "chronology": norm(ch)}

def E(d, t, q):
    return {"date_text": d, "type": t, "quote": q, "inherited_date": False, "date_inferred": False}

def I(d, t, q, e):
    return {"date_text": d, "type": t, "quote": q, "inherited_date": True, "entry_quote": e, "date_inferred": False}

def N(t, q):
    return {"date_text": "", "type": t, "quote": q, "inherited_date": False, "date_inferred": True}

def S1(q, ok=True):
    return {"id": "S1", "status": "SUPPORTED" if ok else "NOT_REPORTED", "quote": q, "section": "block" if q else ""}

def S2(status, name, q, sec):
    d = {"id": "S2", "status": status}
    if status == "SUPPORTED":
        d["name"] = name
    d["quote"] = q
    d["section"] = sec
    return d

def C(status, q):
    return {"status": status, "quote": q, "section": "cause" if q else ""}

def U(kind, names, q, sec):
    return {"kind": kind, "names": names, "quote": q, "section": sec if q else ""}

L = {}

# 23V396
L["RCLRPT-23V396-2407.txt"] = dict(
    claims=[S1("Name : Central Plains Industries"),
            S2("INSUFFICIENT", None, "Name : Central Plains Industries", "block")],
    cause=C("SUPPORTED", "The weld joint was improperly welded."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("November 23, 2021", "FILER_AWARENESS", "On November 23, 2021 it was discovered on a Terex test unit that the subframe insert welds had failed."),
        N("INVESTIGATION_START", "Analysis of the failed subframe showed inadequate welds attaching the insert tubes into the subframe."),
        E("November 29, 2021", "INVESTIGATION_START", "On November 29, 2021, a subframe was pulled from inventory and the welds inspected which also showed inadequate weld penetration attaching the insert tubes into the subframe."),
        E("November 30, 2021", "OTHER", "On November 30, 2021 all in stock and in process subframes of part number 625726 were identified and rework began."),
        E("December 2, 2021", "OTHER", "Development of a potential field fix began on December 2, 2021."),
        E("May 23, 2023", "OTHER", "Validation of the field fix was completed on May 23, 2023."),
        E("June 1, 2023", "DECISION", "Even though there are no reports of issues, a decision to recall was made on June 1, 2023."),
    ])

# 23V405
L["RCLRPT-23V405-2388.txt"] = dict(
    claims=[S1("Name : Mercedes-Benz AG"),
            S2("SUPPORTED", "MBAG", "In October 2022, MBAG launched initial investigations based on an isolated field report indicating a malfunction of the electrical drivetrain possibly referring to a loss of propulsion.", "chronology")],
    cause=C("SUPPORTED", "Due to a deviation in the development process, the electric drivetrain software may improperly respond in the event of a detected fault at a specific plug connector within the electric drive."),
    upstream=U("UNNAMED", [], "Immediately, analyses were started together with the supplier to determine the root cause.", "chronology"),
    events=[
        E("October 2022", "INVESTIGATION_START", "In October 2022, MBAG launched initial investigations based on an isolated field report indicating a malfunction of the electrical drivetrain possibly referring to a loss of propulsion."),
        N("INVESTIGATION_START", "Immediately, analyses were started together with the supplier to determine the root cause."),
        E("December 2022", "INVESTIGATION_START", "These analyses, including related tests, continued until December 2022."),
        N("OTHER", "It was concluded that the observed failures were resulting from fault management response logic."),
        N("INVESTIGATION_START", "MBAG used field data to identify the scenarios in which the malfunction might occur."),
        N("INVESTIGATION_START", "Detailed analyses on the possible consequences depending on the software version of the electric drivetrain were performed."),
        N("INVESTIGATION_START", "Subsequently, further analyses were done to identify potentially affected vehicles."),
        E("May 26, 2023", "DECISION", "On May 26, 2023, MBAG determined that a potential safety risk cannot be ruled out and decided to conduct a recall."),
        E("October 5, 2022", "FILER_AWARENESS", "MBAG is currently aware of 2 field reports, including warranty claims, received on October 5, 2022 and October 24, 2022 from the US."),
        E("October 24, 2022", "FILER_AWARENESS", "MBAG is currently aware of 2 field reports, including warranty claims, received on October 5, 2022 and October 24, 2022 from the US."),
    ])

# 23V408
L["RCLRPT-23V408-4127.txt"] = dict(
    claims=[S1("Name : Suburban Manufacturing Co"),
            S2("SUPPORTED", "Suburban", "We were notified by our supplier of the Suburban cooktop on May 1, 2023.", "chronology")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NAMED", ["Suburban"], "We were notified by our supplier of the Suburban cooktop on May 1, 2023.", "chronology"),
    events=[
        E("May 1, 2023", "SUPPLIER_NOTICE", "We were notified by our supplier of the Suburban cooktop on May 1, 2023."),
    ])

# 23V422
t1 = "On June 1, 2023, Tesla began investigating the Semi door lock behavior after the software team flagged a potential noncompliance with the rear-hinged-door logic during a routine internal software-compliance audit conducted for quality assurance purposes."
t3 = "On June 6, 2023, Tesla completed its review and made a voluntary recall determination to remedy a noncompliance with FMVSS 206, S.4.1.2.3."
L["RCLRPT-23V422-8709.txt"] = dict(
    claims=[S1("Name : Tesla, Inc."),
            S2("SUPPORTED", "Tesla", t1, "chronology")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("June 1, 2023", "INVESTIGATION_START", t1),
        E("June 2, 2023", "OTHER", "On June 2, 2023, in parallel to the investigation, Tesla began developing a software remedy for the potential noncompliance."),
        E("June 6, 2023", "DECISION", t3),
        I("June 6, 2023", "OTHER", "On the same day, Tesla completed development of the software remedy as described below.", t3),
        I("June 6, 2023", "OTHER", "Tesla’s Homologation team evaluated the software remedy and determined the software fix to be compliant with FMVSS 206, S.4.1.2.3.", t3),
    ])

# 23V483
L["RCLRPT-23V483-6594.txt"] = dict(
    claims=[S1("Name : Cummins Inc."),
            S2("SUPPORTED", "Cummins", "In mid-April Cummins notified Industrial Video & Control of recall 23E030.", "chronology")],
    cause=C("SUPPORTED", "As stated in Cummins Recall 23E-030, \"The cause of the issue is an inadequate specification of the fuel hose.\""),
    upstream=U("NAMED", ["Cummins"], "In mid-April Cummins notified Industrial Video & Control of recall 23E030.", "chronology"),
    events=[
        E("mid-April", "SUPPLIER_NOTICE", "In mid-April Cummins notified Industrial Video & Control of recall 23E030."),
        N("INVESTIGATION_START", "An investigation was opened to determine impacted units."),
    ])

# 23V524
h1 = "June 1, 2023 Honda identified an incorrect certification label during a quality inspection and began to investigate the issue."
L["RCLRPT-23V524-5492.txt"] = dict(
    claims=[S1("Name : American Honda Motor Co., Inc."),
            S2("SUPPORTED", "Honda", h1, "chronology")],
    cause=C("SUPPORTED", "During a failure of the primary certification label printer, a backup label printer incorrectly printed information without being properly reset and configured for the US model."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("June 1, 2023", "FILER_AWARENESS", h1),
        E("June 5, 2023", "INVESTIGATION_START", "June 5, 2023 Honda investigated the affected population of vehicles."),
        E("July 20, 2023", "DECISION", "July 20, 2023 Honda determined that a FMVSS noncompliance existed and decided to conduct a noncompliance recall."),
    ])

# 23V539
p1 = "Provan RV Industries was notified by our regional Cummins sales rep on 4/13/2023 that there was a recall on the generators we purchase."
p2 = "7/13/2023 We decided to reach out Cummins to request a cross reference of serial numbers and invoice dates."
L["RCLRPT-23V539-2363.txt"] = dict(
    claims=[S1("Name : Cummins, Inc"),
            S2("SUPPORTED", "Cummins", p1, "chronology")],
    cause=C("SUPPORTED", "The cause of the issue is an inadequate fuel hose and clamp provided and installed by Cummins Onan."),
    upstream=U("NAMED", ["Cummins", "Cummins Onan"], p1, "chronology"),
    events=[
        E("4/13/2023", "SUPPLIER_NOTICE", p1),
        N("OTHER", "We verified no current generators in stock were on the recall serial number list."),
        N("OTHER", "Then we developed a plan to track down the generators with the effected serial numbers."),
        E("7/13/2023", "OTHER", p2),
        I("7/13/2023", "INVESTIGATION_START", "Upon receipt of this list, we reviewed our receiving log and entered the dates that we received the generator and cross referenced those dates to our internal production tracking software.", p2),
        E("7/29/2023", "OTHER", "7/29/2023 Once we were confident that we identified all potential effected customers, we generated the draft recall report and recall letter."),
    ])

# 23V547
L["RCLRPT-23V547-9794.txt"] = dict(
    claims=[S1("Name : Lippert Components Inc."),
            S2("INSUFFICIENT", None, "Name : Lippert Components Inc.", "block")],
    cause=C("SUPPORTED", "Starcraft RV production may have installed a standard window instead of an emergency egress window in the slide-out over the sofa."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("May 25, 2023", "FILER_AWARENESS", "May 25, 2023 an internal communication was received from our codes and standards team informing Jayco compliance that there were 17 trailers that may have been built with no secondary means of escape."),
        E("June 5, 2023", "OTHER", "June 5, 2023 the Warranty Incident Review Committee (WIRC) discussed this incident and elevated to the Corrective and Preventive Action Committee (CPAC)."),
        E("June 7, 2023", "OTHER", "June 7, 2023 CPAC met to discuss this incident and elevated this incident to the Safety Steering Committee (SSC), pending an internal investigation of the incident."),
        E("July 27, 2023", "DECISION", "July 27, 2023 SSC met and voted that a safety recall was appropriate for this incident."),
    ])

# 23V557
L["RCLRPT-23V557-4321.txt"] = dict(
    claims=[S1("Name : Samsong"),
            S2("INSUFFICIENT", None, "Both seatbelts were sent to the supplier for analysis.", "chronology")],
    cause=C("SUPPORTED", "The affected seat belt assemblies were improperly assembled during inventory re-work by the supplier."),
    upstream=U("UNNAMED", [], "Both seatbelts were sent to the supplier for analysis.", "chronology"),
    events=[
        E("June 27, 2023", "FILER_AWARENESS", "On June 27, 2023, HMC informed NASO of a condition detected during analysis of two (2) seat belt assembly warranty returns from certain model year 2023 Genesis GV60 vehicles in the U.S. market."),
        N("INVESTIGATION_START", "Both seatbelts were sent to the supplier for analysis."),
        N("SUPPLIER_NOTICE", "The supplier provided information that the recovered seatbelts came from a suspect lot that had been reworked postproduction, resulting in an out-of-specification cam rib on the ALR mechanism that prevents extension of the seat belt webbing after initial ALR engagement."),
        E("July 29, 2023", "DECISION", "On July 29, 2023, NASO finalized its analysis and convened its North America Safety Decision Authority confirming the condition involving the ALR in the subject vehicles does not comply with the requirements set forth in FMVSS No. 208 and 209 of C.F.R. 49."),
        N("DECISION", "Based on this information, NASO decided to conduct a noncompliance recall of all affected model year 2023 Genesis GV60 vehicles in the U.S. and Canada."),
    ])

# 23V558
L["RCLRPT-23V558-1590.txt"] = dict(
    claims=[S1("Name : NR", ok=False),
            S2("NOT_REPORTED", None, "", "")],
    cause=C("SUPPORTED", "The awning may not be adequately attached to the vehicle."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("July 27, 2023", "FILER_AWARENESS", "On July 27, 2023, Forest River's Office of Corporate Compliance (\"OCC\") was contacted by the manufacturing division with a concern of the awning installation."),
        N("INVESTIGATION_START", "The same day, OCC opened a research item."),
        N("FILER_AWARENESS", "It was noted that the manufacturing plant had received three complaints between May 2023 and July 2023 indicating that the awning leg was touching the vehicle entry door."),
        E("July 31, 2023", "OTHER", "On July 31, 2023, OCC met with the manufacturing plant and reviewed the installation of the awning."),
        E("August 4, 2023", "DECISION", "On August 4, 2023, Forest Rivers Corporate Recall Committee voted to recall."),
    ])

# 23V595
fsup = "Further supplier investigation and statistical analysis indicated that the failed parts were limited to one induction heat machine where maintenance personnel entered an incorrect offset value for the 10.5-inch left rear axle shaft."
L["RCLRPT-23V595-8061.txt"] = dict(
    claims=[S1("Name : Mid-West Forge Corporation"),
            S2("INSUFFICIENT", None, fsup, "chronology")],
    cause=C("SUPPORTED", "Personnel at the axle shaft supplier entered an incorrect process parameter into one of the two machines that perform electromagnetic induction heat treatment of the subject left rear axle shafts."),
    upstream=U("UNNAMED", [], fsup, "chronology"),
    events=[
        E("August 10, 2023", "INVESTIGATION_START", "On August 10, 2023, an issue pertaining to left rear axle shaft fractures on 2023 model year F-250 and F-350 Super Duty vehicles equipped with single rear wheels and 10.5-inch rear axles was brought to Ford’s Critical Concern Review Group for review."),
        N("FILER_AWARENESS", "These failures were identified by Kentucky Truck Plant through monitoring of warranty claims."),
        N("INVESTIGATION_START", "Two axle shafts returned through warranty were sent to Ford’s metallurgical lab for failure analysis."),
        N("OTHER", "Laboratory analysis determined that the axle shafts did not meet Ford’s torsional yield and case depth design specifications in the fractured area."),
        N("INVESTIGATION_START", fsup),
        E("August 18, 2023", "DECISION", "On August 18, 2023, Ford’s Field Review Committee reviewed the concern and approved a field action."),
    ])

# 23V597
cep = "CAP determined the leak was the result of a cut o-ring installed by Ford’s Cleveland Engine Plant (CEP)."
L["RCLRPT-23V597-6273.txt"] = dict(
    claims=[S1("Name : Ford Motor Company"),
            S2("SUPPORTED", "Ford", cep, "chronology")],
    cause=C("SUPPORTED", "Ford reused turbo oil supply lines that had the o-ring replaced."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("July 30, 2023", "FILER_AWARENESS", "On July 30, 2023, Ford’s Chicago Assembly Plant (CAP) identified oil leaking at the turbo oil supply line to cylinder block interface on a 2023 Explorer with 2.3L GTDI engine."),
        N("OTHER", cep),
        E("August 6, 2023", "INVESTIGATION_START", "On August 6, 2023, Ford’s Critical Concern Review Group (CCRG) opened an investigation pertaining to this issue."),
        N("INVESTIGATION_START", "CEP reviewed their manufacturing records and determined the suspect population has a distinct torque run- down signature."),
        N("OTHER", "CEP identified 36 total suspect 2.3L GTDI engines from a review of the torque rundown signatures."),
        N("OTHER", "Ford’s CCRG determined that 10 vehicles with suspect engines were shipped to dealers without inspection or repair, and the other 26 engines were contained at CEP or CAP."),
        E("August 18, 2023", "DECISION", "On August 18, 2023, Ford’s Field Review Committee reviewed the concern and approved a field action."),
    ])

# 23V641
f2 = "From April 25, 2023, through August 11, 2023, FCA US TSRC met with FCA US engineering to review the issue, understand part design and failure mode, and to determine the suspect population."
L["RCLRPT-23V641-2572.txt"] = dict(
    claims=[S1("Name : Aisin World Corporation of America"),
            S2("INSUFFICIENT", None, "Name : Aisin World Corporation of America", "block")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("April 24, 2023", "FILER_AWARENESS", "On April 24, 2023, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization was notified of a potential issue related to the AGS on some Jeep Wrangler and Jeep Gladiator vehicles."),
        E("April 25, 2023", "INVESTIGATION_START", f2),
        E("August 11, 2023", "INVESTIGATION_START", f2),
        E("August 16, 2023", "OTHER", "On August 16, 2023, the FCA US TSRC organization recognized a vehicle build issue existed on certain vehicles related to a condition that can lead to the lack of rearview visibility and rearview lamps, potentially causing a noncompliance with FMVSS No. 111 and No. 108."),
        E("September 11, 2023", "DECISION", "On September 11, 2023, FCA US determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected vehicles."),
    ])

# 23V649
L["RCLRPT-23V649-3598.txt"] = dict(
    claims=[S1("Name : Donghee Mexico"),
            S2("INSUFFICIENT", None, "Improperly welded joint by supplier.", "cause")],
    cause=C("SUPPORTED", "Improperly welded joint by supplier."),
    upstream=U("NOT_REPORTED", [], "See attached document titled “2023MY Forte Right Front Lower Control Arm Chronology.”", "chronology"),
    events=[])

# 23V650
aud = "Additionally, vehicle/component inventory audits performed by HMC and the supplier found thirty-one (31) additional defective retractors for use in model year 2024 Hyundai Kona vehicles."
drc = "HMA’s Data Review Committee (“DRC”) and Technical Review Committee (“TRC”) conducted assessments of frequency and risk regarding the potential defect condition from August 30, 2023 through September 15, 2023."
L["RCLRPT-23V650-5650.txt"] = dict(
    claims=[S1("Name : Joyson Safety Systems Korea"),
            S2("INSUFFICIENT", None, aud, "chronology")],
    cause=C("SUPPORTED", "The pin used to fasten the retainer cover to the seatbelt retractor might not have been installed properly by the supplier."),
    upstream=U("UNNAMED", [], aud, "chronology"),
    events=[
        E("August 24, 2023", "FILER_AWARENESS", "On August 24, 2023, HMA’s port quality team issued a Quality Information Report (“QIR”) indicating a seatbelt assembly on a model year 2024 Hyundai Kona vehicle that partially separated resulting in an inability to extend/retract the seat belt webbing."),
        E("August 30, 2023", "INVESTIGATION_START", drc),
        E("September 15, 2023", "INVESTIGATION_START", drc),
        N("INVESTIGATION_START", aud),
        E("September 15, 2023", "DECISION", "On September 15, 2023, NASO quickly convened its North America Safety Decision Authority to review its investigation findings and determined that the inability to properly use the rear seat belts poses a failure to comply with the requirements set forth in FMVSS No. 208,"),
        N("DECISION", "Based on this review, NASO decided to conduct a noncompliance recall of all affected vehicles in the U.S."),
    ])

# 23V653
def pe(d, t, q):
    return E(d, t, q)
pt = {}
L["RCLRPT-23V653-1716.txt"] = dict(
    claims=[S1("Name : Peterbilt Motors Co."),
            S2("SUPPORTED", "Peterbilt", "8/25/23: Test data was presented/discussed to Peterbilt Safety and Compliance.", "chronology")],
    cause=C("SUPPORTED", "An inconsistent length of the U-bolt may lead to contact with the fuel tank and eventually wear a hole in it."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("6/6/23", "FILER_AWARENESS", "6/6/23: Issue first brought up to Safety and Compliance"),
        E("6/12/23", "INVESTIGATION_START", "6/12/23: Engineer visited CVS to view recently manufactured tractors."),
        I("6/12/23", "OTHER", "Found 5 close related cases.", "6/12/23: Engineer visited CVS to view recently manufactured tractors."),
        E("6/16/23", "INVESTIGATION_START", "6/16/23: Engineer talked with design engineering to understand the history of the parts involved."),
        E("6/17/23", "INVESTIGATION_START", "6/17/23: Engineer visited manufacturing to understand the process of installation."),
        I("6/17/23", "OTHER", "Engineer received plant process document.", "6/17/23: Engineer visited manufacturing to understand the process of installation."),
        E("6/26/23", "INVESTIGATION_START", "6/26/23: Warranty search completed."),
        I("6/26/23", "FILER_AWARENESS", "Found 7 warranty claims stating checked U-bolt hitting the fuel tank.", "6/26/23: Warranty search completed."),
        I("6/26/23", "OTHER", "Reassembled and checked clearances.", "6/26/23: Warranty search completed."),
        E("6/19/23", "OTHER", "6/19/23: Engineer talked with warranty containment to understand changes to improve future tractors based on root cause found."),
        E("6/27/23", "OTHER", "6/27/23: Presented investigation to safety committee."),
        E("7/7/23", "OTHER", "7/7/23: Engineering finished gathering information asked from safety committee."),
        E("7/11/23", "OTHER", "7/11/23: Presented investigation to safety committee."),
        I("7/11/23", "OTHER", "Testing was requested.", "7/11/23: Presented investigation to safety committee."),
        E("7/13/23", "INVESTIGATION_START", "7/13/23: Reached out to PTC about testing and communicated the dynamic gap study requested"),
        E("7/20/23", "OTHER", "7/20/23: Engineering submitted RTS to PTC for assignment."),
        I("7/20/23", "OTHER", "Parts shipped to PTC for further test.", "7/20/23: Engineering submitted RTS to PTC for assignment."),
        E("7/25/23", "OTHER", "7/25/23: Parts arrived at PTC for testing."),
        E("8/15/23", "OTHER", "8/15/23: PTC finished attaching parts to a test tractor."),
        I("8/15/23", "OTHER", "Instrumentation attached on the truck for testing.", "8/15/23: PTC finished attaching parts to a test tractor."),
        E("8/22/23", "INVESTIGATION_START", "8/22/23: Initial test was completed, and the data was collected."),
        E("8/25/23", "OTHER", "8/25/23: Test data was presented/discussed to Peterbilt Safety and Compliance."),
        E("9/1/23", "INVESTIGATION_START", "9/1/23: Population was scanned for errors."),
        I("9/1/23", "INVESTIGATION_START", "Final Warranty Search", "9/1/23: Population was scanned for errors."),
        E("9/5/23", "OTHER", "9/5/23: Present investigation to partial safety committee."),
        I("9/5/23", "OTHER", "Attendees requested additional engineering review of chassis layouts.", "9/5/23: Present investigation to partial safety committee."),
        E("9/21/23", "OTHER", "9/21/23: Safety Committee reviewed chassis layouts."),
        E("9/25/23", "OTHER", "9/25/23: Separate review with remaining safety committee members."),
        I("9/25/23", "DECISION", "Conclusion was to issue a recall.", "9/25/23: Separate review with remaining safety committee members."),
    ])

# 23V656
a2 = "June 27, 2023, through August 31, 2023, Autocar inspected 176 additional units and zero defects were found."
L["RCLRPT-23V656-4926.txt"] = dict(
    claims=[S1("Name : Autocar LLC"),
            S2("SUPPORTED", "Autocar", a2, "chronology")],
    cause=C("SUPPORTED", "A manufacturing error resulted in the steering column shaft pinch bolt installation error."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("June 5, 2023", "FILER_AWARENESS", "June 5, 2023, during an internal audit, it was determined that a steering column pinch bolt was not properly secured, and an internal investigation was initiated."),
        E("June 27, 2023", "INVESTIGATION_START", a2),
        E("August 31, 2023", "INVESTIGATION_START", a2),
        E("September 21, 2023", "DECISION", "September 21, 2023, the information was presented to Autocar's management team and out of an abundance of caution, Autocar decided to perform a voluntary safety recall for all affected units."),
    ])

# 23V690
v1 = "September 18, 2023 Volvo Product Safety Office receives a report of a potential issue in our factory with a critical joint and a formal investigation is opened."
L["RCLRPT-23V690-6126.txt"] = dict(
    claims=[S1("Name : Volvo Trucks"),
            S2("SUPPORTED", "Volvo", v1, "chronology")],
    cause=C("SUPPORTED", "Inadequate process control of torque and torque auditing within our assembly facilities."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("September 18, 2023", "FILER_AWARENESS", v1),
        E("October 2, 2023", "OTHER", "October 2, 2023 Findings from the investigation are reviewed by the Product Safety Evaluation Committee and the recommendation is that this is be brought to Product Safety Committee as a potential product safety defect."),
        E("October 9, 2023", "DECISION", "October 9, 2023 The Product Safety Committee meets and decides that a product safety defect exists."),
        E("October 14, 2023", "NHTSA_FILING", "October 14, 2023 573 Report filed with NHTSA"),
    ])

# 23V699
ac1 = "September 12, 2023, during an internal inspection, Autocar personnel identified three units equipped with the suspect pressure switch, not included in recall 23V400 suspect population and began investigation."
ac2 = "October 10, 2023, the investigation completed and determined 104 units not included in 23V400 could be suspect."
L["RCLRPT-23V699-7039.txt"] = dict(
    claims=[S1("Name : Autocar LLC"),
            S2("SUPPORTED", "Autocar", ac1, "chronology")],
    cause=C("SUPPORTED", "An Autocar internal process error."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("September 12, 2023", "FILER_AWARENESS", ac1),
        E("October 10, 2023", "OTHER", ac2),
        I("October 10, 2023", "DECISION", "Out of an abundance of caution, Autocar decided to perform a voluntary safety recall for all affected units.", ac2),
    ])

# 23V703
tx1 = "On June 20, 2023, the Terex South Dakota, Inc production team discovered that the wrong bolts and wrong torque may have been used on previously installed machines for attaching the pedestal to sub-base."
L["RCLRPT-23V703-2054.txt"] = dict(
    claims=[S1("Name : Terex South Dakota, Inc"),
            S2("SUPPORTED", "Terex South Dakota, Inc", tx1, "chronology")],
    cause=C("SUPPORTED", "The bolts used may have been the incorrect grade and may have been torqued to the incorrect value."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("June 20, 2023", "FILER_AWARENESS", tx1),
        N("OTHER", "All in process machines were checked and verified to have the correct bolts and torque."),
        E("August 29, 2023", "INVESTIGATION_START", "An engineering analysis was completed on August 29, 2023 that determined the lower bolt torque was inadequate."),
        N("OTHER", "Development of the field fix began at that time."),
        E("October 12, 2023", "DECISION", "Even though there are no reports of issues, a decision to recall was made on October 12, 2023."),
    ])

# 23V708
psw = "The PSWG met again with Engineering in September and early October and decided to escalate the issue to Lucid's Product Safety Executive Council (PSEC)."
L["RCLRPT-23V708-4418.txt"] = dict(
    claims=[S1("Name : NR", ok=False),
            S2("NOT_REPORTED", None, "", "")],
    cause=C("SUPPORTED", "The issue was introduced by a software change in version 2.1.0 which removed temperature monitoring and control in certain situations and vehicle modes."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("August 1, 2023", "FILER_AWARENESS", "On August 1, 2023, a Lucid Air customer experienced charring of a rear seat."),
        E("August 3", "OTHER", "Lucid Engineering briefed Lucid’s Product Safety Working Group (PSWG) about the issue on August 3, after which, Engineering continued its analysis of the risk of harm from the issue."),
        N("FILER_AWARENESS", "One customer reported a burned finger after touching the discolored rear seat surface."),
        E("September", "OTHER", psw),
        E("early October", "OTHER", psw),
        E("October 4", "OTHER", "As of October 4, Affected S/W Versions are no longer being installed on or transmitted to any vehicles."),
        E("October 12", "DECISION", "On October 12, the PSEC determined that the lack of rear seat heater temperature control in certain non-driving vehicle modes presented an unreasonable risk to safety for owners of Lucid Air vehicles still on Affected S/W Versions."),
    ])

# 23V716
b2 = "From October 2022, through January 2023, FCA US TSRC analyzed warranty claims, customer records, and vehicle history to identify incidents of third-row seat belt buckles being damaged during assembly."
b3 = "From January 2023, through June 2023, FCA US TSRC held initial meetings with FCA US Interior Engineering, and ongoing meetings with FCA US Restraints Engineering and Manufacturing to continue to review the issue and understand the potential consequence."
b4 = "From June 2023, through September 2023, FCA US TSRC finalized discussions with FCA US Restraints Engineering, Interior Engineering, and Manufacturing and determined the suspect population."
L["RCLRPT-23V716-5715.txt"] = dict(
    claims=[S1("Name : AUTOLIV NORTH AMERICA INC"),
            S2("INSUFFICIENT", None, "Name : AUTOLIV NORTH AMERICA INC", "block")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("October 20, 2022", "FILER_AWARENESS", "On October 20, 2022, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization was notified of a potential issue related to third-row seat belt buckles being damaged or scratched in some 2022 MY Jeep Wagoneer and Jeep Grand Wagoneer vehicles."),
        E("October 2022", "INVESTIGATION_START", b2),
        E("January 2023", "INVESTIGATION_START", b2),
        I("October 2022", "OTHER", "In parallel, FCA US TSRC held initial meetings with FCA US Restraints Engineering and Manufacturing to review the issue, understand the part design, assembly process, and failure mode.", b2),
        E("January 2023", "OTHER", b3),
        E("June 2023", "OTHER", b3),
        E("June 2023", "OTHER", b4),
        E("September 2023", "OTHER", b4),
        E("September 27, 2023", "OTHER", "On September 27, 2023, the FCA US TSRC organization recognized a vehicle build issue existed on certain vehicles related to third-row seat belt buckles being inaccessible or damaged, potentially resulting in a noncompliance with FMVSS No. 208 Occupant Crash Protection"),
        E("October 19, 2023", "DECISION", "On October 19, 2023, FCA US determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected vehicles."),
    ])

# 23V732
mb2 = "MBAG initiated a technical investigation, including the potential impact of not including the wear inspection gauge."
L["RCLRPT-23V732-5995.txt"] = dict(
    claims=[S1("Name : MBAG"),
            S2("SUPPORTED", "MBAG", mb2, "chronology")],
    cause=C("SUPPORTED", "Due to a documentation error in the production control system, the potentially affected vehicles might not be equipped with the inspection gauge for checking the wear of the rear axle brake pads and the respective information in the owner's manual might be missing."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("February 2020", "FILER_AWARENESS", "In February 2020, MBAG after sales department was first made aware through internal analyses for quality assurance that the inspection gauge for checking the wear of the brake pads on the rear axle and the respective information in the owner's manual for using this inspection gauge"),
        N("INVESTIGATION_START", mb2),
        N("INVESTIGATION_START", "During the analysis process, MBAG investigated potential technical impacts of the described issue in connection with the conditions of the braking system."),
        N("OTHER", "MBAG found that, due to the brake force distribution, the brake pads on the front axle wear out sooner than the rear axle brake pads."),
        N("INVESTIGATION_START", "In addition, internal vehicle test data was analyzed."),
        N("OTHER", "This analysis showed that even with completely worn brake pads on the rear axle, the potentially affected vehicles would still meet the legal performance requirements for stopping distance in accordance with the FMVSS 135, S7.5.3."),
    ])

# 23V750
vw1 = "May 2023: internal CoP tests (Conformity of Production) resulted in not OK tests."
vw2 = "June - August 2023: Intensive testing conducted."
vw3 = "September 08, 2023: Topic presented to the Volkswagen Product Safety Committee."
vw4 = "November 01, 2023: Topic presented to the Volkswagen Product Safety Committee again."
L["RCLRPT-23V750-4558.txt"] = dict(
    claims=[S1("Name : Automotive Mexico Body Systems"),
            S2("INSUFFICIENT", None, "Supplier contacted for clarification.", "chronology")],
    cause=C("INSUFFICIENT", "The root cause is currently not known."),
    upstream=U("UNNAMED", [], "Supplier contacted for clarification.", "chronology"),
    events=[
        E("May 2023", "FILER_AWARENESS", vw1),
        I("May 2023", "OTHER", "Supplier contacted for clarification.", vw1),
        E("June", "INVESTIGATION_START", vw2),
        E("August 2023", "INVESTIGATION_START", vw2),
        I("June", "INVESTIGATION_START", "Analysis together with supplier and other laboratories.", vw2),
        I("June", "OTHER", "Test setup discussed.", vw2),
        E("September 08, 2023", "OTHER", vw3),
        I("September 08, 2023", "OTHER", "The Committee issued a task for additional technical clarification and evaluation of options.", vw3),
        E("November 01, 2023", "OTHER", vw4),
        I("November 01, 2023", "DECISION", "Out of an abundance of caution, due to inconsistent test results, a noncompliance recall was decided because the interior sunshade covering the panoramic glass roof may not consistently meet the requirements of FMVSS 302.", vw4),
        E("December 04, 2023", "OTHER", "December 04, 2023: Volkswagen identified an internal system error that filtered out Puerto Rico market vehicles from the U.S. market population."),
    ])

# 23V754
s1 = "August 30, 2023 – The supplier identified quench cracking on the outer diameter of the outer race during magnetic particle inspection."
s2 = "September 14, 2023 – After a reevaluation of scope, the supplier determined that affected product had been shipped to Subaru."
s3 = "October 2023 – The supplier presented their findings of the scope of affected parts shipments."
s4 = "November 2, 2023 – For the entire population of potentially affected vehicles, Subaru is not aware of any field reports, warranty claims, or VOQs."
L["RCLRPT-23V754-7121.txt"] = dict(
    claims=[S1("Name : NTN Corporation"),
            S2("INSUFFICIENT", None, s1, "chronology")],
    cause=C("SUPPORTED", "A hole in a water pipe caused a reduction in the flow rate of cooling water around the outer race during the heat treatment process on the supplier’s manufacturing line, resulting in improper cooling to the inner surface of the race and causing quench cracking to the outer surface of the race."),
    upstream=U("UNNAMED", [], s1, "chronology"),
    events=[
        E("August 30, 2023", "OTHER", s1),
        I("August 30, 2023", "OTHER", "The supplier’s initial findings indicated that there had been no outflow to Subaru.", s1),
        E("September 14, 2023", "OTHER", s2),
        I("September 14, 2023", "SUPPLIER_NOTICE", "Subaru received information from the supplier indicating a crack on the surface of an outer race of the front drive shaft assembly.", s2),
        I("September 14, 2023", "INVESTIGATION_START", "Subaru and the supplier initiated a joint study to determine the safety impact of a crack in the outer race.", s2),
        E("October 2023", "SUPPLIER_NOTICE", s3),
        I("October 2023", "INVESTIGATION_START", "Subaru worked with the part supplier to trace the affected parts based on the lot number information.", s3),
        I("November 2, 2023", "DECISION", "However, out of an abundance of caution, Subaru decided to conduct a safety recall.", s4),
    ])

# ---- build + verify ----
out, errs = [], []
files = sorted(f for f in os.listdir(T) if f.startswith("RCLRPT-") and f.endswith(".txt"))
assert len(files) == 25, files
for fn in files:
    fname, sec = sections(os.path.join(T, fn))
    lab = L[fn]
    def chk(q, s, what):
        if not q:
            return
        if len(q) > 300:
            errs.append(f"{fn} {what}: too long {len(q)}")
        if norm(q) not in sec[s]:
            errs.append(f"{fn} {what}: quote not in {s}: {q[:80]}")
    for c in lab["claims"]:
        chk(c["quote"], c["section"], c["id"])
    chk(lab["cause"]["quote"], "cause", "cause")
    if lab["upstream"]["quote"]:
        chk(lab["upstream"]["quote"], lab["upstream"]["section"], "upstream")
    for i, e in enumerate(lab["events"]):
        chk(e["quote"], "chronology", f"ev{i}")
        if e["date_text"] and e["date_text"] not in norm(e["quote"]) and not e["inherited_date"]:
            errs.append(f"{fn} ev{i}: date not in quote")
        if e["inherited_date"]:
            chk(e["entry_quote"], "chronology", f"ev{i} entry")
            if e["date_text"] not in e["entry_quote"]:
                errs.append(f"{fn} ev{i}: date not in entry_quote")
    out.append({"file": fname, "claims": lab["claims"], "cause": lab["cause"],
                "upstream": lab["upstream"], "events": lab["events"]})

if errs:
    print("\n".join(errs))
    sys.exit(1)
with open(os.path.join(D, "passB.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("ok", len(out), sum(len(o["events"]) for o in out))
