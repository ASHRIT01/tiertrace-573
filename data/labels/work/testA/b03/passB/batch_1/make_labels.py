import json, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def sections(fn):
    txt = open(os.path.join(T, fn), encoding="utf-8").read()
    file_line = re.search(r"^FILE: (.+)$", txt, re.M).group(1).strip()
    b = txt.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    c = txt.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    h = txt.split("=== CHRONOLOGY ===")[1]
    return file_line, {"block": norm(b), "cause": norm(c), "chronology": norm(h)}


def S1(q, status="SUPPORTED"):
    return {"id": "S1", "status": status, "quote": q, "section": "block" if q else ""}


def S2(status, name="", q="", sec=""):
    d = {"id": "S2", "status": status}
    if status == "SUPPORTED":
        d["name"] = name
    d["quote"] = q
    d["section"] = sec
    return d


def C(status, q, sec="cause"):
    return {"status": status, "quote": q, "section": sec if q else ""}


def U(kind, names=None, q="", sec=""):
    return {"kind": kind, "names": names or [], "quote": q, "section": sec}


def E(date, typ, q):
    return {"date_text": date, "type": typ, "quote": q, "inherited_date": False, "date_inferred": False}


def EI(typ, q):
    return {"date_text": "", "type": typ, "quote": q, "inherited_date": False, "date_inferred": True}


def EH(date, typ, q, entry):
    return {"date_text": date, "type": typ, "quote": q, "inherited_date": True, "entry_quote": entry, "date_inferred": False}


L = {}

# ---------------- 23V787
L["RCLRPT-23V787-5200.txt"] = dict(
    claims=[S1("Name : SAMSUNG SDI AMERICA INC"),
            S2("INSUFFICIENT", q="Name : SAMSUNG SDI AMERICA INC", sec="block")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NONE_MENTIONED"),
    events=[
        E("May 12, 2023", "INVESTIGATION_START", 'On May 12, 2023, the FCA US LLC ("FCA US") Technical Safety and Regulatory Compliance ("TSRC") organization opened an investigation after receiving two field reports of 2021 MY Jeep Wrangler PHEVs with fires originating from the HV battery.'),
        E("May 2023", "OTHER", "In May 2023, FCA US requested buybacks of both vehicles for further analysis."),
        E("May 2023, to September 2023", "FILER_AWARENESS", "From May 2023, to September 2023, FCA US received five additional reports of 2021-2022 MY Jeep Wrangler PHEVs with fires originating from the HV battery and requested buybacks of these vehicles for further analysis."),
        E("October 2023", "INVESTIGATION_START", "In October 2023, FCA US received two vehicle buybacks and have disassembled the HV battery packs."),
        E("November 16, 2023", "DECISION", "On November 16, 2023, FCA US determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected vehicles."),
    ])

# ---------------- 23V798
L["RCLRPT-23V798-4906.txt"] = dict(
    claims=[S1("Name : Truck Pro"), S2("INSUFFICIENT", q="Name : Truck Pro", sec="block")],
    cause=C("SUPPORTED", "The inversion valve was determined to be out of specification for the piston concentricity due to a machining issue."),
    upstream=U("NONE_MENTIONED"),
    events=[
        E("September 8, 2023", "INVESTIGATION_START", "September 8, 2023 – KME started internal investigation due to other REV Group business units having an affected population to determine if KME may be affected as well."),
        E("September 26, 2023", "OTHER", "September 26, 2023 – KME verified inventory and trucks in production with green mark on data tag."),
        E("November 22, 2023", "DECISION", "November 22, 2023 – KME determined potential population of affected trucks and decided that a voluntary recall should be issued."),
    ])

# ---------------- 23V801
L["RCLRPT-23V801-2565.txt"] = dict(
    claims=[S1("Name : NR", "NOT_REPORTED"), S2("NOT_REPORTED")],
    cause=C("SUPPORTED", "An Over-the-Air software update introduced incorrect software logic that caused user-selectable drive modes, including ESC status, to carry over between ignition cycles instead of returning to default ESC operation with each ignition cycle."),
    upstream=U("NONE_MENTIONED"),
    events=[
        E("November 9, 2023", "INVESTIGATION_START", "On November 9, 2023, an issue pertaining to the persistence of user-selected drive modes, including ESC status, between ignition cycles on certain 2022 and 2023 model year Ford Lightning vehicles was brought to Ford’s Critical Concern Review Group (CCRG) for review."),
        E("weekend of October 27, 2023", "FILER_AWARENESS", "The carry over of drive modes between ignition cycles was first identified during the weekend of October 27, 2023, when Ford personnel noticed that the last selected drive mode began to carry over between ignition cycles"),
        E("October 27, 2023", "OTHER", "The OTA software deployments were halted on October 27, 2023 for an unrelated concern."),
        EI("OTHER", "The CCRG investigation determined that the SYNC 1.9.4 update caused the reduced ESC function tied to Off-Road mode to carry over between drive cycles without user input instead of returning to default ESC operation with each drive cycle."),
        EI("OTHER", "The CCRG reviewed the certain exclusions in Section 5.4.1 of FMVSS No. 126, but determined that they do not apply to these F-150 Lightnings."),
        EI("OTHER", "CCRG reviewed the deployment records for the OTA and determined that 5,118 number of vehicles received the OTA update version 6.3.0."),
        E("November 17, 2023", "DECISION", "On November 17, 2023, Ford’s Field Review Committee reviewed the concern and approved a field action."),
    ])

# ---------------- 23V818
L["RCLRPT-23V818-7970.txt"] = dict(
    claims=[S1("Name : Weldon Division of Akron Brass"),
            S2("SUPPORTED", "Weldon", "On November 15, 2023 – KME received information from Weldon regarding recall number 23E-084.", "chronology")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NAMED", ["Weldon"], "On November 15, 2023 – KME received information from Weldon regarding recall number 23E-084.", "chronology"),
    events=[
        E("early October 2023", "OTHER", "In early October 2023, Weldon was notified that external wiring in a vehicle using the node had melted."),
        E("mid-October", "INVESTIGATION_START", "The part was returned to Weldon for analysis in mid-October where it was found that when an external short circuit occurred, the electrical output did not shut down as specified."),
        EI("INVESTIGATION_START", "Weldon conducted testing and analysis of the version of the node used in the vehicle as well as prior versions of the node"),
        EI("OTHER", "Weldon found that the calibration was previously updated in production, but was not considered to pose a broader concern at the time."),
        E("October 24, 2023", "OTHER", "On October 24, 2023, Weldon decided to conduct a safety recall to address the issue."),
        E("November 15, 2023", "SUPPLIER_NOTICE", "On November 15, 2023 – KME received information from Weldon regarding recall number 23E-084."),
        EI("OTHER", "Engineering reviewed potential population and inventory reviewed."),
        E("November 27, 2023", "OTHER", "November 27, 2023 – KME determined the final population."),
        EH("November 27, 2023", "OTHER", "The issue was escalated to REV Group Management.", "November 27, 2023 – KME determined the final population."),
        E("November 29, 2023", "DECISION", "November 29, 2023 – REV’s senior leadership approved a voluntary recall for this issue."),
        E("January 12, 2024", "NHTSA_FILING", "On January 12, 2024 – The KME population of 20 vehicles was removed from recall 23V808 and added to recall 23V818 after completing audit of build location."),
    ])

# ---------------- 23V848
L["RCLRPT-23V848-6524.txt"] = dict(
    claims=[S1("Name : Ford Motor Company"),
            S2("SUPPORTED", "Ford", "On November 21, 2023, Ford’s Critical Concern Review group reviewed an issue pertaining to the rear turn signal outage notification strategy on 2022 – 2024 model year Maverick vehicles.", "chronology")],
    cause=C("SUPPORTED", "The Body Control Module (BCM) software’s turn signal outage detection logic was not configured to detect for an outage of one bulb on each circuit."),
    upstream=U("NONE_MENTIONED"),
    events=[
        E("November 21, 2023", "INVESTIGATION_START", "On November 21, 2023, Ford’s Critical Concern Review group reviewed an issue pertaining to the rear turn signal outage notification strategy on 2022 – 2024 model year Maverick vehicles."),
        EI("FILER_AWARENESS", "The Systems Engineering and Validation team discovered this issue during future model development testing."),
        EI("INVESTIGATION_START", "The Hermosillo Assembly Plant (HSAP) Plant Vehicle Team (PVT) and Systems Engineering and Lighting teams evaluated this concern on 2022-2024 model year vehicles and confirmed the issue is present for this model year range."),
        EI("OTHER", "Ford’s CCRG issued a stop ship for concern."),
        E("December 8, 2023", "DECISION", "On December 8, 2023, Ford’s Field Review Committee reviewed the concern and approved a field action."),
    ])

# ---------------- 23V854
L["RCLRPT-23V854-1196.txt"] = dict(
    claims=[S1("Name : Mercedes-Benz AG"),
            S2("SUPPORTED", "MBAG", "In June 2020, MBAG received isolated cases from the field describing instances in which the front roof panel forward of the panoramic sunroof had allegedly detached from the vehicle.", "chronology")],
    cause=C("SUPPORTED", "Due to a deviation in the workshop process, the front panels may not have been bonded according to specifications during a prior repair."),
    upstream=U("NONE_MENTIONED"),
    events=[
        E("June 2020", "FILER_AWARENESS", "In June 2020, MBAG received isolated cases from the field describing instances in which the front roof panel forward of the panoramic sunroof had allegedly detached from the vehicle."),
        EI("INVESTIGATION_START", "MBAG launched an investigation and was able to verify from its internal documentation that in these isolated cases the wrong adhesive was used to bond the panels during a previous repair."),
        EI("INVESTIGATION_START", "MBAG also began to analyze its internal data related to detachment of the front roof panel to understand whether the incidents were indicative of a broader trend or isolated events"),
        EI("INVESTIGATION_START", "MBAG began to analyze whether there was a more systemic issue and whether it was related to a prior repair of the front roof panel."),
        E("late 2020 and into the first quarter of 2021", "INVESTIGATION_START", "MBAG’s technical analysis was carried out from late 2020 and into the first quarter of 2021"),
        EI("INVESTIGATION_START", "Test setups were prepared by recreating various repair scenarios where an incorrect pre-treatment and bonding adhesives other than the one specific adhesive that had been approved for this repair."),
        EI("INVESTIGATION_START", "Sample roof panels were also returned from the field and analyzed which indicated how the pre-treatment, cleaning and primer application were actually being applied by Mercedes- Benz workshops and any third-party sublets and confirmed that there were deviations from the repair procedures."),
    ])

# ---------------- 23V855
q855 = "BRP also promptly contacted its fuel pump supplier to start a joint analysis."
L["RCLRPT-23V855-3267.txt"] = dict(
    claims=[S1("Name : Robert Bosch LLC."), S2("INSUFFICIENT", q=q855, sec="chronology")],
    cause=C("SUPPORTED", "It was found that the “new” source of material for the impeller could cause it to swell and come in interference with the housing."),
    upstream=U("UNNAMED", [], q855, "chronology"),
    events=[
        E("August 2023", "FILER_AWARENESS", "In August 2023, Transport Canada informed BRP of received reports of fuel pumps malfunction."),
        EI("INVESTIGATION_START", "BRP reviewed all the TC reports, reanalyzed its network data, contacted customers, and collected fuel pumps from the field."),
        EI("INVESTIGATION_START", q855),
        E("August to December 2023", "INVESTIGATION_START", "The investigation took place from August to December 2023."),
        EI("SUPPLIER_NOTICE", "During this time, BRP was informed by its supplier that changes were made as to the source of the raw material used to produce the impeller over the years (initial source, new source and back to the initial source)."),
        EI("OTHER", "It was found that the “new” source of material for the impeller could cause it to swell and come in interference with the housing."),
        EI("INVESTIGATION_START", "BRP worked to confirm its supplier’s findings and to identify when those fuel pumps were installed on its vehicles and sold as service parts."),
        EI("FILER_AWARENESS", "BRP was also contacted by NHTSA during this period following reports from customers as well."),
        E("December 11, 2023", "DECISION", "With all the information collected and analyzed, BRP decided on December 11, 2023, that it had enough information to report and wants to proceed with a safety recall."),
    ])

# ---------------- 23V877
L["RCLRPT-23V877-5210.txt"] = dict(
    claims=[S1("Name : Hyundai Motor Manufacturing Alabama"),
            S2("INSUFFICIENT", q="Name : Hyundai Motor Manufacturing Alabama", sec="block")],
    cause=C("INSUFFICIENT", "Undetermined."),
    upstream=U("NOT_REPORTED", [], "See attached document titled “2011MY Sorento Engine Compartment Chronology”.", "chronology"),
    events=[])

# ---------------- 23V882
q882 = "On November 8, 2023, Nissan received notification from the supplier (JTEKT) about an incident involving another OEM vehicle regarding a steering gear assembly."
e882 = "November 2023 through December 2023 - Nissan began an internal investigation into the issue together with the supplier."
L["RCLRPT-23V882-8764.txt"] = dict(
    claims=[S1("Name : JTEKT Automotive"), S2("SUPPORTED", "JTEKT", q882, "chronology")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NAMED", ["JTEKT"], q882, "chronology"),
    events=[
        E("November 8, 2023", "SUPPLIER_NOTICE", q882),
        EI("SUPPLIER_NOTICE", "The supplier indicated that the subject steering gear assembly is also supplied to Nissan."),
        E("November 2023 through December 2023", "INVESTIGATION_START", e882),
        EH("November 2023 through December 2023", "OTHER", "Based on supplier provided data, a suspect window was identified concerning the tool that produced the potentially affected subject steering gear assemblies.", e882),
        EH("November 2023 through December 2023", "OTHER", "Within this window, 6 units were identified out of 1,213 parts produced using the suspect tool.", e882),
        EH("November 2023 through December 2023", "OTHER", "Nissan matched the 6 units to VINs based on serial number.", e882),
        EH("November 2023 through December 2023", "OTHER", "One (1) vehicle produced for Dubai market was captured with a Nissan port modification activity.", e882),
        E("December 14, 2023", "DECISION", "December 14, 2023 – Based on the foregoing, Nissan decided to conduct a safety recall campaign to remedy the remaining 5 affected vehicles in the U.S. market."),
    ])

# ---------------- 24E012
q012 = "Carrier quickly commenced an internal investigation, and began working with Kubota, to determine the cause of the thermal events through field and lab testing."
L["RCLRPT-24E012-8633.txt"] = dict(
    claims=[S1("Name : Kubota Corporation"), S2("SUPPORTED", "Kubota", q012, "chronology")],
    cause=C("INSUFFICIENT", "Carrier is still investigating the root cause of this issue."),
    upstream=U("NAMED", ["Kubota"], q012, "chronology"),
    events=[
        E("mid-January 2024", "FILER_AWARENESS", "In mid-January 2024, Carrier was made aware of two reports of RG genset units, belonging to the same customer, that had failed from thermal events believed to originate in the Diesel Oxidation Catalyst (DOC) located in the Kubota engine for each unit."),
        EI("INVESTIGATION_START", q012),
        E("February 4, 2024", "FILER_AWARENESS", "On February 4, 2024, Carrier was advised of a third report involving a UG genset unit that belonged to a different customer."),
        EI("OTHER", "Following this third event, Carrier moved quickly to suggest to its customers with these models to ground all units in their possession as soon as possible."),
        E("February 6", "DECISION", "After internal meetings of all safety stakeholders following the third event, Carrier determined that a reportable issue existed in the subject genset units on February 6."),
        E("February 9", "NHTSA_FILING", "Carrier now files this 573 report on February 9."),
    ])

# ---------------- 24E029
L["RCLRPT-24E029-4277.txt"] = dict(
    claims=[S1("Name : TOURATECH GmbH"), S2("INSUFFICIENT", q="Name : TOURATECH GmbH", sec="block")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NOT_REPORTED", [], "Due to character space limitations in this free text field, please refer to the separate document containing the chronology.", "chronology"),
    events=[])

# ---------------- 24E030
q030 = "During this period, Eberspaecher also initiated a sales stop on February 9, 2024 and rework of the component in their sales network on February 16, 2024 to address the defect."
L["RCLRPT-24E030-1138.txt"] = dict(
    claims=[S1("Name : NR", "NOT_REPORTED"), S2("NOT_REPORTED")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NONE_MENTIONED"),
    events=[
        E("January 30, 2024", "FILER_AWARENESS", "On January 30, 2024, a potential component defect was identified that was not initially known to be safety-related."),
        E("February 8, 2024 and February 29, 2024", "INVESTIGATION_START", "Eberspaecher Climate Control Systems International GmbH (Eberspaecher) conducted a risk assessment of the component between February 8, 2024 and February 29, 2024."),
        E("February 9, 2024", "OTHER", q030),
        E("February 16, 2024", "OTHER", q030),
        E("March 6, 2024", "OTHER", "Starting March 6, 2024, Eberspaecher began informing its subsidiaries, general agents, and customers of the defect."),
        E("March 11, 2024", "OTHER", "Beginning March 11, 2024, Eberspaecher started to set up meetings with key customers for the US and Canadian market to define a rework strategy."),
        E("March 2024", "OTHER", "Eberspaecher also consulted with US counsel in March 2024."),
        E("March 21, 2024", "DECISION", "On March 21, 2024 it was determined that NHTSA should be notified of the safety-related defect."),
        E("March 27, 2024", "NHTSA_FILING", "Subsequently, Eberspaecher submitted its Part 573 notification on March 27, 2024."),
    ])

# ---------------- 24E041
q041 = "In October 2022, following a notification by RH Sheppard that it had determined a defect existed in certain steering gear assemblies, Oshkosh conducted a recall of vehicles equipped with potentially defective parts (22E-073)."
L["RCLRPT-24E041-7047.txt"] = dict(
    claims=[S1("Name : R.H. Sheppard Co., Inc."), S2("SUPPORTED", "RH Sheppard", q041, "chronology")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NAMED", ["RH Sheppard"], q041, "chronology"),
    events=[
        E("October 2022", "SUPPLIER_NOTICE", q041),
        E("February 2024", "OTHER", "In February 2024, RH Sheppard extended the scope of the recall to include additional steering gear assemblies that were not included in its original recall."),
        EI("FILER_AWARENESS", "The expansion of the RH Sheppard recall was brought to Oshkosh's attention and after investigating whether any of the additional recalled parts were installed in Oshkosh vehicles, Oshkosh concluded that any affected components were used as service or aftermarket replacement parts only."),
        E("May 30, 2024", "DECISION", "On May 30, 2024, Oshkosh decided to conduct a recall of the additional set of steering gear assemblies identified by RH Sheppard."),
    ])

# ---------------- 24E068
q068k = "with the suspect parts coming from a discrete batch of 1,000 bolts received from component vendor Kelko Products Company on or about 9.13.23 thereby prompting this voluntary recall."
q068i = "Investigation and sampling of inventory during June and July 2024 indicated a hydrogen embrittlement failure mode different than the suspected fatigue mode addressed in SPL service bulletin/manufacturer communication SB-23-01 (filed 8.2.23)"
L["RCLRPT-24E068-9308.txt"] = dict(
    claims=[S1("Name : Kelko Products Company"), S2("SUPPORTED", "Kelko Products Company", q068k, "chronology")],
    cause=C("SUPPORTED", "Suspect process control faults by vendor within an unknown number of the two 6.35” black zinc coated tapered stud bolts in each kit resulting in suspected inclusions and hydrogen embrittelment."),
    upstream=U("NAMED", ["Kelko Products Company"], q068k, "chronology"),
    events=[
        E("the months leading up to July 2024", "FILER_AWARENESS", "In the months leading up to July 2024, SPL received field reports of the identified 6.35” black zinc coated cap bolts breaking during initial installation and torquing."),
        E("June and July 2024", "INVESTIGATION_START", q068i),
        E("8.2.23", "OTHER", q068i),
        E("9.13.23", "OTHER", q068k),
    ])

# ---------------- 24E071
L["RCLRPT-24E071-6470.txt"] = dict(
    claims=[S1("Name: ICM Controls"),
            S2("SUPPORTED", "ICM Controls", "GE Appliances first contacted ICM Controls on June 3, 2024 to report the incident", "chronology")],
    cause=C("INSUFFICIENT", "In coordination with ICM Controls, GE Appliances is still investigating the root cause of the failure mechanism, including soliciting failure analysis from ICM Controls regarding the failure mechanism occurring in the ICM870-16A-BH5400 soft start controller."),
    upstream=U("NAMED", ["ICM Controls"], "GE Appliances first contacted ICM Controls on June 3, 2024 to report the incident", "chronology"),
    events=[
        E("May 15, 2024", "FILER_AWARENESS", "GE Appliances incorporated the ICM870-16A-BH5400 soft start into multiple models of its recreational vehicle air conditioning units without a reported thermal incident until May 15, 2024."),
        E("June 3, 2024", "OTHER", "GE Appliances first contacted ICM Controls on June 3, 2024 to report the incident"),
        E("June 18, 2024", "SUPPLIER_NOTICE", "On June 18, 2024, ICM Controls responded, indicating that it had not previously received any report of any such thermal event in this type of application."),
        EI("INVESTIGATION_START", "GE Appliances subsequently shipped this soft start to ICM Controls for further failure analysis."),
        E("July 3, 2024 and August 16, 2024", "FILER_AWARENESS", "Between July 3, 2024 and August 16, 2024, GE Appliances received 10 reports of thermal events in GE Appliances RVAC units."),
        EI("INVESTIGATION_START", "GE Appliances made every effort to obtain additional information, including artifact evidence, from each of these events"),
        E("July 17, 2024", "FILER_AWARENESS", "Additionally, GE Appliances received insurance claims on July 17, 2024 and July 23, 2024 alleging RV property damage from fires originating in an GE Appliances RVAC unit"),
        E("July 23, 2024", "FILER_AWARENESS", "Additionally, GE Appliances received insurance claims on July 17, 2024 and July 23, 2024 alleging RV property damage from fires originating in an GE Appliances RVAC unit"),
        EI("NHTSA_FILING", "Upon receiving and analyzing the evidence related to these incidents, GE Appliances filed the instant report."),
    ])

# ---------------- 24E083
L["RCLRPT-24E083-7160.txt"] = dict(
    claims=[S1("Name : Magna International Inc"), S2("INSUFFICIENT", q="Name : Magna International Inc", sec="block")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NONE_MENTIONED"),
    events=[
        E("July 21, 2023", "FILER_AWARENESS", 'On July 21, 2023, the FCA US LLC ("FCA US") Technical Safety and Regulatory Compliance ("TSRC") organization became aware that some 2020 through 2023 MY Ram 1500 Classic trucks may be equipped with a driver side heated trailer tow rearview mirror'),
        E("July 2023, through September 2024", "INVESTIGATION_START", "From July 2023, through September 2024, FCA US TSRC conducted an analysis of detached driver side heated trailer tow mirror glass failure patterns and vehicle history"),
        E("September 18, 2024", "OTHER", "On September 18, 2024, the FCA US TSRC organization recognized that a vehicle build issue existed on certain vehicles related to a condition that can lead to a detached driver side heated trailer tow mirror glass, potentially resulting in a noncompliance with FMVSS No. 111."),
        E("October 03, 2024", "DECISION", "On October 03, 2024, FCA US determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected units."),
    ])

# ---------------- 24E095
q095 = "From September 27, 2024, through October 1, 2024, the Stellantis Europe S.p.A CX organization reviewed supplier data, warranty records, and determined the suspect period on affected vehicles."
L["RCLRPT-24E095-2052.txt"] = dict(
    claims=[S1("Name : Manufactured by Stellantis Europe"),
            S2("SUPPORTED", "Stellantis Europe S.p.A", "On September 27, 2024, the Stellantis Europe S.p.A Customer Experience (\"CX\") department opened an investigation as a result of warranty cases related to brake pedal assemblies collapsing during normal driving.", "chronology")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("UNNAMED", [], q095, "chronology"),
    events=[
        E("September 27, 2024", "INVESTIGATION_START", "On September 27, 2024, the Stellantis Europe S.p.A Customer Experience (\"CX\") department opened an investigation as a result of warranty cases related to brake pedal assemblies collapsing during normal driving."),
        E("September 27, 2024, through October 1, 2024", "INVESTIGATION_START", q095),
        E("October 2, 2024", "DECISION", "On October 2, 2024, Stellantis Europe S.p.A determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected vehicles."),
        E("October 9, 2024", "OTHER", "On October 9, 2024, Stellantis Europe S.p.A determined, through the Vehicle Regulations Committee, to add additional vehicles to the suspect population."),
        E("October 2024, through November 2024", "INVESTIGATION_START", "From October 2024, through November 2024, Stellantis Europe S.p.A reviewed service part sales records to determine if any suspect parts were sold in the United States market."),
        E("November 6, 2024", "DECISION", "On November 6, 2024, FCA US determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected units."),
    ])

# ---------------- 24E097
q097 = "Based on photos of the failed tire mount, our manufacturing partner concluded that the interim weld technician had likely used tubing that did not meet our specifications."
L["RCLRPT-24E097-7957.txt"] = dict(
    claims=[S1("Name : Silver Star Industries"), S2("INSUFFICIENT", q=q097, sec="chronology")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("UNNAMED", [], q097, "chronology"),
    events=[
        E("August 31, 2023", "FILER_AWARENESS", "On August 31, 2023, we received notice from an owner that the weld on his rear tire mount had failed."),
        EI("INVESTIGATION_START", "We immediately began an investigation and determined that this owner’s tire mount was part of a batch of three manufactured in January 2022."),
        EI("SUPPLIER_NOTICE", q097),
        EI("SUPPLIER_NOTICE", "The manufacturer stated this was likely the only tire mount produced by the interim weld technician."),
        EI("OTHER", "As a result, we treated this as a warranty issue, sent the owner a newly-updated replacement tire mount, and took immediate steps to enhance quality control processes."),
        EI("OTHER", "Additionally, we updated the design of the rear tire mount to incorporate redundant safety features, ensuring multiple welds would have to fail for the mount to pose any safety risk."),
        E("October 30, 2024", "FILER_AWARENESS", "On October 30, 2024, we received notice from a second owner regarding a weld failure on his rear tire mount."),
        EI("DECISION", "Recognizing the potential safety implications, we reclassified the issue as a product defect and out of an abundance of caution, initiated a recall for all tire mounts with the original design"),
    ])

# ---------------- 24E099
e099a = "August 31, 2024: Agility’s engineering team was advised of a report from a customer that the manual cylinder valve on a CNG fuel system experienced a leak."
e099b = "September 12 – November 13, 2024: Valves were sent to Agility engineering and a root cause investigation was initiated, which included the following activities: review of high magnification photos and analysis from engineering teams; regular meetings with the supplier, OMB-Saleri S.P.A. (“OMB”);"
L["RCLRPT-24E099-7080.txt"] = dict(
    claims=[S1("Name : OMB-Saleri S.P.A."), S2("SUPPORTED", "OMB-Saleri S.P.A.", e099b, "chronology")],
    cause=C("INSUFFICIENT", "The root cause of the stress corrosion cracking is still under investigation."),
    upstream=U("NAMED", ["OMB-Saleri S.P.A."], e099b, "chronology"),
    events=[
        E("August 31, 2024", "FILER_AWARENESS", e099a),
        E("6/19/2024", "OTHER", "A review of service records revealed two additional failure reports (failure dates 6/19/2024 and 8/19/2024)."),
        E("8/19/2024", "OTHER", "A review of service records revealed two additional failure reports (failure dates 6/19/2024 and 8/19/2024)."),
        EH("August 31, 2024", "OTHER", "Arrangements were made to obtain the valves for analysis.", e099a),
        E("September 12 – November 13, 2024", "INVESTIGATION_START", e099b),
        EH("September 12 – November 13, 2024", "FILER_AWARENESS", "During this period, three additional valve failures were reported.", e099b),
        EH("September 12 – November 13, 2024", "OTHER", "Based upon the results of the investigation to date, Agility’s engineering team recommended that the matter be escalated to Agility’s Safety Committee for consideration.", e099b),
        E("November 13, 2024", "DECISION", "November 13, 2024: Agility’s Safety Committee decided to initiate a safety recall to address this condition."),
    ])

# ---------------- 24V039
q039 = "On December 21st, the supplier started inspection of their inventory and initiated a root cause analysis to include a review of their production process, parts handling procedures, and quality assurance controls."
L["RCLRPT-24V039-2530.txt"] = dict(
    claims=[S1("Name : LEONI AG"), S2("INSUFFICIENT", q=q039, sec="chronology")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("UNNAMED", [], q039, "chronology"),
    events=[
        E("December 20, 2023", "FILER_AWARENESS", "On December 20, 2023, during a pre-delivery inspection (PDI) at one of the Rolls-Royce motor cars dealers, adhesive residue was noticed on the ground connection cable, specifically on the connector eyelet which attaches to the front electric motor."),
        EI("INVESTIGATION_START", "An engineering investigation was initiated, and all potentially affected vehicles within the vehicle assembly plant were blocked."),
        E("December 21st", "INVESTIGATION_START", q039),
        E("January 11th", "OTHER", "As a precaution, on January 11th, a vehicle delivery stop was issued."),
        E("January 17, 2024", "DECISION", "On January 17, 2024, Rolls-Royce decided to conduct a voluntary safety recall."),
    ])

# ---------------- 24V046
L["RCLRPT-24V046-1641.txt"] = dict(
    claims=[S1("Name : Winnebago Ind Inc."),
            S2("SUPPORTED", "Winnebago", "In January 2024, Winnebago Product Safety found a defect in wiring on Access models.", "chronology")],
    cause=C("SUPPORTED", "The breakaway switch power wire is connected to ground rather than constant power."),
    upstream=U("NONE_MENTIONED"),
    events=[
        E("January 2024", "FILER_AWARENESS", "In January 2024, Winnebago Product Safety found a defect in wiring on Access models."),
        EI("INVESTIGATION_START", "Production was immediately notified, and the wiring was inspected."),
        EI("OTHER", "Upon inspection, it was determined the breakaway switch wiring was incorrect and the testing equipment experienced a fault setting."),
        E("January 26, 2024", "DECISION", "On January 26, 2024 the Product Safety Committee decided the issue presented an unreasonable risk to motor vehicle safety."),
        E("November 14, 2023", "FILER_AWARENESS", "The first submission occurred November 14, 2023."),
    ])

# ---------------- 24V047
L["RCLRPT-24V047-5176.txt"] = dict(
    claims=[S1("Name : NR", "NOT_REPORTED"), S2("NOT_REPORTED")],
    cause=C("SUPPORTED", "Manufacturing error."),
    upstream=U("NONE_MENTIONED"),
    events=[
        E("January 24, 2024", "FILER_AWARENESS", "On January 24, 2024, the manufacturing plant was reviewing the installation of the furnace cold air return and number of heat ducts being used due to an internal Pre-Delivery Inspection (\"PDI\") inspection."),
        E("January 25, 2024", "INVESTIGATION_START", "On January 25, 2024, the manufacturing plant contacted Forest River's Office of Corporate Compliance (\"OCC\") and a research item was opened."),
        E("January 26, 2024", "DECISION", "On January 26, 2024, Forest River's Corporate Recall Committee voted to recall."),
    ])

# ---------------- 24V077
q077 = "Fatigue cracking due to damage to the valve spring during manufacture by the supplier."
L["RCLRPT-24V077-1532.txt"] = dict(
    claims=[S1("Name : Daewonkangup"), S2("INSUFFICIENT", q=q077, sec="cause")],
    cause=C("SUPPORTED", q077),
    upstream=U("NOT_REPORTED", [], "See attached document titled “2024MY Telluride Engine Valve Spring Chronology.”", "chronology"),
    events=[])

# ---------------- 24V143
q143 = "Weld locations of mounting brackets and length of parking brake control rods were out of specification during supplier manufacture of floor-mounted mechanical brake assemblies."
L["RCLRPT-24V143-7520.txt"] = dict(
    claims=[S1("Name : Orscheln Products LLC"), S2("INSUFFICIENT", q=q143, sec="cause")],
    cause=C("SUPPORTED", q143),
    upstream=U("NOT_REPORTED", [], "Chronology is provided as an attachment.", "chronology"),
    events=[])

# ---------------- 24V164
q164 = "01/18/2024 – R. H. Sheppard communicates to Navistar of finding a steering gear sector shaft with less than the required hardness during shot peen operation."
L["RCLRPT-24V164-6230.txt"] = dict(
    claims=[S1("Name : R. H. Sheppard"), S2("SUPPORTED", "R. H. Sheppard", q164, "chronology")],
    cause=C("SUPPORTED", "As reported by R. H. Sheppard in recall 24E-010, “heat treating may have not been properly performed on some lots of sector shafts resulting in lower than expected hardness for the gear teeth."),
    upstream=U("NAMED", ["R. H. Sheppard"], q164, "chronology"),
    events=[
        E("01/18/2024", "SUPPLIER_NOTICE", q164),
        E("01/18/2024", "OTHER", "01/18/2024 – Navistar initiates ship hold of all loose steering gears and vehicles at the assembly plants, finding 785 suspect gears out of 1,037 suspect gears, and established clean point at the Escobedo and San Antonio assembly plants."),
        E("01/18/2024 through 02/20/2024", "INVESTIGATION_START", "01/18/2024 through 02/20/2024 – Navistar conducts a search of manufacturing records to identify vehicles built with a suspect steering gear serial number."),
        E("02/07/2024", "OTHER", "02/07/2024 – Navistar Product Safety, Engineering, and supplier quality meet with R. H. Sheppard to review and discuss the failure mode, root cause, lot code and steering gear serial number data collected by R. H. Sheppard."),
        E("02/09/2024", "SUPPLIER_NOTICE", "02/09/2024 – Navistar receives R.H. Sheppard’s 573 defect report for 24E-010."),
        E("02/21/2024", "OTHER", "02/21/2024 – Navistar completes its review of manufacturing records and finalizes the Suspect Population"),
        E("02/22/2024", "DECISION", "02/22/2024 – Navistar declares a Safety Recall."),
        E("4/8/2024", "NHTSA_FILING", "4/8/2024 -- Updated recall schedule on this defect report."),
    ])

# ---------------- build + verify
out, errs = [], []
files = sorted(f for f in os.listdir(T) if f.startswith("RCLRPT-") and f.endswith(".txt"))
assert set(files) == set(L), set(files) ^ set(L)


def chk(fn, where, q, sec, S):
    if not q:
        return
    if len(q) > 300:
        errs.append(f"{fn} {where}: len {len(q)}")
    if sec not in S or norm(q) not in S[sec]:
        errs.append(f"{fn} {where}: quote not in {sec}: {q[:80]}")


for fn in files:
    fl, S = sections(fn)
    lab = L[fn]
    obj = {"file": fl, "claims": lab["claims"], "cause": lab["cause"], "upstream": lab["upstream"], "events": lab["events"]}
    for c in obj["claims"]:
        chk(fn, c["id"], c["quote"], c["section"], S)
    chk(fn, "cause", obj["cause"]["quote"], obj["cause"]["section"], S)
    chk(fn, "upstream", obj["upstream"]["quote"], obj["upstream"]["section"], S)
    for i, e in enumerate(obj["events"]):
        chk(fn, f"ev{i}", e["quote"], "chronology", S)
        if e["date_text"] and not e["inherited_date"] and e["date_text"] not in norm(e["quote"]):
            errs.append(f"{fn} ev{i}: date not in quote")
        if e["inherited_date"]:
            chk(fn, f"ev{i}.entry", e["entry_quote"], "chronology", S)
            if e["date_text"] not in e["entry_quote"]:
                errs.append(f"{fn} ev{i}: date not in entry_quote")
    out.append(obj)

if errs:
    print("\n".join(errs))
    sys.exit(1)
with open(os.path.join(D, "passB.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("ok", len(out), sum(len(o["events"]) for o in out))
