import json, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def sections(path):
    txt = open(path, encoding="utf-8").read()
    fileline = re.search(r"^FILE: (.+)$", txt, re.M).group(1).strip()
    blk = txt.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    cause = txt.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    chron = txt.split("=== CHRONOLOGY ===")[1]
    return fileline, {"block": norm(blk), "cause": norm(cause), "chronology": norm(chron)}


def C(id_, status, quote="", section="", name=None):
    d = {"id": id_, "status": status}
    if name is not None:
        d["name"] = name
    d["quote"] = quote
    d["section"] = section
    return d


def CA(status, quote, section="cause"):
    return {"status": status, "quote": quote, "section": section if quote else ""}


def U(kind, names, quote, section):
    return {"kind": kind, "names": names, "quote": quote, "section": section if quote else ""}


def E(date_text, type_, quote, entry=None, inferred=False):
    d = {"date_text": date_text, "type": type_, "quote": quote,
         "inherited_date": entry is not None}
    if entry is not None:
        d["entry_quote"] = entry
    d["date_inferred"] = inferred
    return d


def EI(type_, quote):
    return E("", type_, quote, inferred=True)


L = {}

# 1
e = "April 2023: Kawasaki Motors, Ltd (KML) received a report from Kawasaki Motors Corp., U.S.A. (KMC) that one of these vehicles had problems starting."
L["RCLRPT-23V515-4321.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Kawasaki Motors Ltd.", "block"),
            C("S2", "SUPPORTED", e, "chronology", name="Kawasaki Motors, Ltd (KML)")],
    cause=CA("SUPPORTED", "Error during installation of the alternator rotor and the alternator rotor bolt."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("April 2023", "FILER_AWARENESS", e),
            E("April 2023", "INVESTIGATION_START", "KML Quality Assurance Division started an investigation of the cause.", entry=e),
            E("June 2023", "FILER_AWARENESS", "June 2023: KML received a 2nd case report from Chinese distributor (KMSH) that “the engine cannot re- start”."),
            E("June 2023", "INVESTIGATION_START", "June 2023: KML inspected the vehicle which reported this 2nd incident of starting problems and found that the alternator rotor and the alternator rotor bolt were loose."),
            E("July 2023", "OTHER", "July 2023: After investigating the manufacturing process for this model, KML determined that the cause of this problem was improper degreasing of the crank shaft prior to installation of the alternator rotor or improper tightening of the alternator rotor bolt during the manufacturing process."),
            E("July 21, 2023", "DECISION", "July 21, 2023：KML decided to initiate a recall campaign.")])

# 2
L["RCLRPT-23V521-1631.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Valeo", "block"),
            C("S2", "INSUFFICIENT", "Name : Valeo", "block")],
    cause=CA("INSUFFICIENT", "Lucid is continuing to investigate the cause of the loosening of wiper arm nuts."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("December 2022", "FILER_AWARENESS", "In December 2022, Lucid received a report of a wiper arm not working in a vehicle brought to a Service Center."),
            EI("INVESTIGATION_START", "Lucid began investigating the issue and discovered 10 reports of similar issues between January and August 2022, then an increase of reported incidents through December 2022."),
            E("March 28, 2023", "OTHER", "Lucid’s Product Safety Working Group (PSWG) was first briefed on the issue on March 28, 2023."),
            EI("INVESTIGATION_START", "Lucid’s investigation continued in an attempt to identify the population of vehicles affected by wiper arm loosening."),
            EI("OTHER", "Concurrently, Lucid was testing potential countermeasures involving increased torque values."),
            E("May", "OTHER", "The PSWG received subsequent briefings in May and June 2023."),
            E("June 2023", "OTHER", "The PSWG received subsequent briefings in May and June 2023."),
            E("June 13", "OTHER", "Lucid implemented a permanent countermeasure of increasing the torque specification at its factory on June 13."),
            E("May", "OTHER", "Lucid briefed NHTSA about its investigation in May and July."),
            E("July", "OTHER", "Lucid briefed NHTSA about its investigation in May and July."),
            E("July 20", "DECISION", "The Lucid Product Safety Executive Council (PSEC) determined on July 20 that the wiper arm issue presented a noncompliance with FMVSS 104.")])

# 3
e1 = "04/13/2023 - 04/18/2023 - Chinook received an important safety recall from Cummins about the Onan QG 2800i being recalled."
L["RCLRPT-23V530-7086.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Chinook Motor Coach", "block"),
            C("S2", "SUPPORTED", e1, "chronology", name="Cummins")],
    cause=CA("SUPPORTED", "There is an inadequate specification of the fuel hose."),
    upstream=U("NAMED", ["Cummins"], e1, "chronology"),
    events=[E("04/13/2023", "SUPPLIER_NOTICE", e1),
            E("04/13/2023", "SUPPLIER_NOTICE", "Then notified by Cummins that they will be performing the recall.", entry=e1),
            E("04/18/2023", "INVESTIGATION_START", "04/18/2023 - 05/22/2023 - Chinook reviewed its records and identified affected Bayside models, then provided the information to Cummins to perform the recall and send out owner notification letters."),
            E("07/27/2023", "DECISION", "07/27/2023 - Chinook was notified and decided to conduct a safety campaign to address the affected Chinook Bayside models.")])

# 4
L["RCLRPT-23V564-3664.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : American Furukawa INC", "block"),
            C("S2", "INSUFFICIENT", "Name : American Furukawa INC", "block")],
    cause=CA("SUPPORTED", "There was a subcomponent specification error in the engineering drawing for the chassis harness which improperly called out for the use of a silicone wire seal with two large 2.45mm openings for the wires instead of one 2.45mm and one 1.55mm opening."),
    upstream=U("NOT_REPORTED", [], "Chronology uploaded separately.", "chronology"),
    events=[])

# 5
q5 = "Indian Motorcycle’s internal quality team investigated the suspect units, which identified a concern related to improper assembly of the fuel lines by the supplier."
L["RCLRPT-23V582-4641.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Cooper Standard", "block"),
            C("S2", "INSUFFICIENT", q5, "chronology")],
    cause=CA("SUPPORTED", "Fuel line was assembled with the internal flow control check valve in the wrong end of the fuel line and oriented in the wrong direction."),
    upstream=U("UNNAMED", [], q5, "chronology"),
    events=[E("June 2023", "FILER_AWARENESS", "In June 2023, Indian Motorcycle identified runability issues on a small quantity of units at the end of line dyno audit in production."),
            EI("INVESTIGATION_START", q5),
            EI("INVESTIGATION_START", "Thereafter, Indian Motorcycle began an investigation, which included outreach to the fuel line supplier and containment of suspect product still within Indian’s control."),
            E("July 2023", "INVESTIGATION_START", "In July 2023, Indian Motorcycle began internal testing of the fuel lines to further understand the impact to vehicle performance."),
            E("August 8, 2023", "DECISION", "On August 8, 2023, Indian Motorcycle’s Executive Review Committee decided that vehicles equipped with an improperly assembled fuel line by the supplier may result in a vehicle stall during operation")])

# 6
L["RCLRPT-23V684-9960.txt"] = dict(
    claims=[C("S1", "NOT_REPORTED", "Name : NR", "block"),
            C("S2", "NOT_REPORTED", "", "")],
    cause=CA("INSUFFICIENT", "A design change was made to this trailer."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("January 13, 2023", "FILER_AWARENESS", "January 13, 2023 customer Sefnco notified Pelsue of the first incident."),
            E("January 23, 2023", "OTHER", "January 23, 2023 a new design for these two models of trailer frames were released."),
            E("January 30, 2023", "OTHER", "January 30, 2023 the Service Bulletin describing the defect and the \"fix\" for trailers in the field was created."),
            E("August 23, 2023", "FILER_AWARENESS", "August 23, 2023 the second incident was reported."),
            E("August 23, 2023", "OTHER", "August 23, 2023 J & B Trailers in Lubbock, TX reported this defect to NHTSA."),
            E("September 11, 2023", "FILER_AWARENESS", "September 11, 2023 Dave Thornton (NHTSA) contacted Pelsue regarding the defect and spoke with Pelsue CEO Chris Munson."),
            E("September 21, 2023", "INVESTIGATION_START", "September 21, 2023 through filtering Work Orders in our ERP system Pelsue determined there were 117 Pelsue Tradesman Fiberlite POD trailers & 47 Pelsue Tradesman Fiberlite XL trailers potentially affected"),
            E("September 25, 2023", "OTHER", "September 25, 2023 Pelsue learned of the Safety Recalls Portal, NHTSA reporting requirements and the 573 Report."),
            E("September 29, 2023", "OTHER", "September 29, 2023 Pelsue created Vehicle Reports for both trailer models."),
            E("October 12, 2023", "NHTSA_FILING", "October 12, 2023 Pelsue submitted a Safety Recall on the Safety Recalls Portal.")])

# 7
e7 = "October 2023 - Chinook Motor Coach received Safety Recall Notice 22S48/NHTSA Recall 23V598 from Ford Motor Company."
L["RCLRPT-23V729-6413.txt"] = dict(
    claims=[C("S1", "NOT_REPORTED", "Name : NR", "block"),
            C("S2", "SUPPORTED", e7, "chronology", name="Ford Motor Company")],
    cause=CA("SUPPORTED", "Within the camera, fretting corrosion causes tin oxide formation on the internal camera connector due to thermally induced micro-movement between the tin-plated contact surfaces."),
    upstream=U("NAMED", ["Ford Motor Company", "Valeo"], e7, "chronology"),
    events=[E("October 2023", "SUPPLIER_NOTICE", e7),
            E("October 2023", "INVESTIGATION_START", "Chinook reviewed its records to determine which Ford Transit Vans are affected by this recall.", entry=e7),
            E("October 2023", "NHTSA_FILING", "Chinook then filed a recall with NHTSA for all affected Chinook Bayside Motorhomes.", entry=e7)])

# 8
q8 = "Alexis Fire Equipment was notified by Spartan Fire LLC of the possible safety defect along with the list of chassis/vehicles sold to Alexis Fire Equipment that could have the possible safety defect."
L["RCLRPT-23V748-7343.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : WABCO", "block"),
            C("S2", "INSUFFICIENT", "Name : WABCO", "block")],
    cause=CA("INSUFFICIENT", "Spartan Fire LLC has determined the inversion valve was determined to be out of specification, but confirmation of root cause is still under investigation."),
    upstream=U("NAMED", ["Spartan Fire LLC"], q8, "chronology"),
    events=[EI("SUPPLIER_NOTICE", q8),
            EI("OTHER", "All testing and decision for the safety defect recall was completed by Spartan File LLC.")])

# 9
e9 = "September 28, 2023: The product safety evaluation committee recommends raising this issue to the product safety committee."
L["RCLRPT-23V781-9407.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Nova Bus", "block"),
            C("S2", "SUPPORTED", "August 9, 2023: Nova Bus is informed of occurrences where the sunvisor fell.", "chronology", name="Nova Bus")],
    cause=CA("SUPPORTED", "Loctite not applied as required per Bill Of Material."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("August 9, 2023", "FILER_AWARENESS", "August 9, 2023: Nova Bus is informed of occurrences where the sunvisor fell."),
            E("September 05, 2023", "OTHER", "September 05, 2023: The issue is raised to the safety forum as a potential risk for evaluation"),
            E("September 07, 2023", "INVESTIGATION_START", "September 07, 2023: Nova Bus opens a formal potential safety related issue investigation."),
            E("September 28, 2023", "OTHER", e9),
            E("September 28, 2023", "OTHER", "Nova Bus initiates an internal factory campaign to inspect and remedy product.", entry=e9),
            E("October 10, 2023", "INVESTIGATION_START", "October 10, 2023: Nova Bus performs and inspection in the field to further understand the fault frequency."),
            E("November 16, 2023", "DECISION", "November 16, 2023: Product Safety Committee determination of product defect."),
            E("November 21, 2023", "NHTSA_FILING", "November 21, 2023: Nova Bus files 573 with NHTSA that a voluntary recall will be released to address the safety-related defect."),
            E("December 5, 2023", "NHTSA_FILING", "December 5, 2023: Nova Bus corrected errors in the model and production dates in vehicle information.")])

# 10
L["RCLRPT-23V796-1556.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Errecinque SRL", "block"),
            C("S2", "INSUFFICIENT", "Name : Errecinque SRL", "block")],
    cause=CA("SUPPORTED", "A defect in the manufacture of the low pressure fuel pipe assembly may allow the pipe to detach from a connection and leak fuel."),
    upstream=U("NOT_REPORTED", [], "for more information.", "chronology"),
    events=[])

# 11
L["RCLRPT-23V859-1885.txt"] = dict(
    claims=[C("S1", "NOT_REPORTED", "Name : NR", "block"),
            C("S2", "NOT_REPORTED", "", "")],
    cause=CA("NOT_REPORTED", "NR"),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("10/4/2023", "FILER_AWARENESS", "Doosan Portable Power received a field report on 10/4/2023 of a portable generator with both electric brake and battery disconnect options"),
            EI("INVESTIGATION_START", "Based on the field report, Doosan Portable Power initiated an internal investigation and determined a noncompliance with the connection point of the electrical brake harness on units with both electric brakes and battery disconnect options."),
            EI("OTHER", "It was determined the affect range of generators with both electric brakes and battery disconnect options were built between 1/2/2019 to 7/31/2023.")])

# 12
q12 = "All units in-house (25 units) have been updated to correct the issue, per Weldon's provided instructions."
L["RCLRPT-23V873-6101.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Weldon Division of Akron Brass", "block"),
            C("S2", "SUPPORTED", q12, "chronology", name="Weldon")],
    cause=CA("NOT_REPORTED", "NR"),
    upstream=U("NAMED", ["Weldon"], q12, "chronology"),
    events=[EI("SUPPLIER_NOTICE", "REV Ambulance Gorup Orlando, Inc. (REVO) warranty department received a Technical Service Bulletin (TSB), regarding Equipment recall 23E-084."),
            E("December 13th, 2023", "SUPPLIER_NOTICE", "REVO was notified on December 13th, 2023."),
            E("December 14th", "INVESTIGATION_START", "REVO conducted an inventory inspection on December 14th and determined that 235 units were affected.")])

# 13
q13 = "From February 17, 2023, through February 20, 2024, FCA US TSRC conducted an analysis of SABIC inflator ruptures and determined that the affected vehicles may have had moisture introduced into the inflator during supplier manufacturing"
L["RCLRPT-24E024-4323.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : JOYSON SAFETY SYSTEMS", "block"),
            C("S2", "INSUFFICIENT", q13, "chronology")],
    cause=CA("NOT_REPORTED", "NR"),
    upstream=U("NAMED", ["SABIC"], q13, "chronology"),
    events=[E("February 17, 2023", "INVESTIGATION_START", "On February 17, 2023, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into some 2018-2021 MY Dodge Charger and Chrysler 300 vehicles that may have been built with a suspect SABIC inflator that may rupture."),
            E("February 17, 2023", "INVESTIGATION_START", q13),
            E("February 20, 2024", "OTHER", q13),
            E("March 07, 2024", "DECISION", "On March 07, 2024, FCA US determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected units.")])

# 14
L["RCLRPT-24E026-6783.txt"] = dict(
    claims=[C("S1", "NOT_REPORTED", "Name : NR", "block"),
            C("S2", "NOT_REPORTED", "", "")],
    cause=CA("SUPPORTED", "Incorrect welding process and use of welding fixtures."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("1/26/2024", "FILER_AWARENESS", "During an FMVSS 207/210 test in the company’s test lab on 1/26/2024, the 2place GO-ES Spacer Saver Foldaway Seat was unable to sustain the test load on the shoulder belts."),
            E("1/29/2024", "INVESTIGATION_START", "Investigation of the production processes for these seats on 1/29/2024 determined the welding fixtures for the recliner mechanism were not being used properly."),
            E("December 8, 2023", "OTHER", "An experienced welder who had been welding this component left the company on December 8, 2023."),
            EI("OTHER", "Welder who took over this process was not effectively trained in the use of the welding fixtures and neglected to use the additional fixture that was needed to accurately locate the recliner mechanism relative to the seat back stop.")])

# 15
L["RCLRPT-24E043-6603.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Spyder Controls Corp", "block"),
            C("S2", "INSUFFICIENT", "Name : Spyder Controls Corp", "block")],
    cause=CA("SUPPORTED", "Applying voltage greater than 18V to the G9"),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("2020", "OTHER", "Original Recall (20E058) was conducted in 2020 where the G9 ECM failure was discovered, and recall was undertaken."),
            E("Friday 5/31/2024", "FILER_AWARENESS", "On Friday 5/31/2024 Firefly Integrations learned that there were 13 affected units that had not been part of the original recall in 2020."),
            EI("DECISION", "Firefly Integrations first verified the information with Foretravel Motorcoach and then determined that a recall for the remaining units was needed.")])

# 16
e16 = "05/25/24: Hendrickson received letter from its supplier, USK Internacional S.A. de C.V. (“USK”), advising it had shipped tie rod assemblies equipped with improperly hardened ball studs, resulting from an experimental heat treatment process."
L["RCLRPT-24E051-6147.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : USK Internacional S.A. de C.V.", "block"),
            C("S2", "SUPPORTED", e16, "chronology", name="USK Internacional S.A. de C.V. (“USK”)")],
    cause=CA("SUPPORTED", "Hendrickson’s supplier mixed improperly hardened ball studs, resulting from an experimental heat treatment process, with production-ready ball studs installed on tie rods assemblies shipped to Hendrickson and other manufacturers."),
    upstream=U("NAMED", ["USK Internacional S.A. de C.V."], e16, "chronology"),
    events=[E("05/25/24", "SUPPLIER_NOTICE", e16),
            E("05/25/24", "SUPPLIER_NOTICE", "USK identified the applicable manufacturing date codes for the suspect tie rod assemblies.", entry=e16),
            E("05/29/24", "OTHER", "05/29/24: Hendrickson completed its initial internal sort and containment of affected USK tie rod assemblies (Part Nos. 015537-2000 and 015537-2100) for use on lift axle suspension assemblies."),
            E("05/29/24", "OTHER", "05/29/24: Hendrickson contained all suspect Part No. 015537-2100 tie rod assemblies for use on lift axle suspension assemblies."),
            E("06/06/24", "OTHER", "06/06/24: Hendrickson located an additional shipment of suspect Part No. 015537-2100 tie rod assemblies received from USK, and informed USK accordingly."),
            E("06/11/24", "OTHER", "06/11/24: Hendrickson began conferring with its applicable vehicle manufacturer and equipment installer customers regarding the subject condition and affected lift axle suspension assemblies."),
            E("06/12/24", "OTHER", "06/12/24: Hendrickson began assisting its above-referenced customers with efforts to identify, inspect, and remedy as-needed, affected lift axle suspension assemblies.")])

# 17
q17 = "On December 12, 2022, NHTSA opened PE22-014 to investigate allegations of hard braking during certain events that Cruise reported to NHTSA under Standing General Order 2021-01."
L["RCLRPT-24E067-1013.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Cruise LLC", "block"),
            C("S2", "SUPPORTED", q17, "chronology", name="Cruise")],
    cause=CA("NOT_REPORTED", "NR"),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("December 12, 2022", "INVESTIGATION_START", q17),
            EI("FILER_AWARENESS", "Specifically, NHTSA noted that it had received three reports of rear-end collisions with Cruise AVs in situations where the Cruise ADS initiated a hard braking maneuver in response to another road user that was quickly approaching from the rear."),
            EI("OTHER", "Over the next eleven months, as part of PE22-014, Cruise responded to NHTSA’s information requests, producing various documents and videos, and holding discussions with the Agency."),
            E("January 29, 2024", "OTHER", "On January 29, 2024, Cruise met with NHTSA to discuss the status of PE22-014, including NHTSA’s preliminary review of the materials and data Cruise provided in 2023."),
            EI("OTHER", "NHTSA also provided insight into the peer information requests sent to other AV companies related to hard braking."),
            E("February 29, 2024", "OTHER", "On February 29, 2024, Cruise met with NHTSA and provided data demonstrating that the rate of occurrence for unexpected braking events in Cruise AVs is very low"),
            EI("OTHER", "Cruise also provided data demonstrating that various Cruise ADS software updates had improved ADS braking performance resulting in a significant reduction in unexpected braking."),
            E("May 9, 2024", "OTHER", "On May 9, 2024, Cruise met with NHTSA to follow-up on the discussion from February 29 regarding the low rate of occurrence of unexpected braking events and the effectiveness of Cruise’s software improvements."),
            E("July 17, 2024", "OTHER", "Further, on July 17, 2024, Cruise met with NHTSA and NHTSA requested that Cruise file a safety recall to close the PE based on software updates that Cruise had implemented.")])

# 18
e18 = "July 2024 - Continental determined there was an issue in the production plant during the specified dates."
L["RCLRPT-24E092-3134.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Continental Automotive Systems, Inc.", "block"),
            C("S2", "SUPPORTED", "December 2023 - Two damaged MK C1 brake systems were reported to Continental by Audi of Norway.", "chronology", name="Continental")],
    cause=CA("SUPPORTED", "Misalignment of screwing machine in manufacturing process."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("December 2023", "FILER_AWARENESS", "December 2023 - Two damaged MK C1 brake systems were reported to Continental by Audi of Norway."),
            E("January 2024", "INVESTIGATION_START", "January 2024 - Continental started an internal investigation into the root cause."),
            E("July 2024", "OTHER", e18),
            E("July 2024", "OTHER", "Other possible affected customers were informed.", entry=e18),
            E("August 19, 2024", "OTHER", "On August 19, 2024 Volkswagen Group of America, Inc. (Audi) filed a Recall Report (24V-621)."),
            E("October 23, 2024", "OTHER", "On October 23, 2024 - Volvo Car USA, LLC., filed a Recall Report."),
            EI("NHTSA_FILING", "Continental Automotive Systems, Inc. is providing this notification in accordance with its obligations as a component part manufacturer under Part 573.3(f)")])

# 19
L["RCLRPT-24V038-8261.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Suzuki Motor Corporation", "block"),
            C("S2", "INSUFFICIENT", "Name : Suzuki Motor Corporation", "block")],
    cause=CA("SUPPORTED", "The assembly process documentation lacked clarity and production-line worker training was insufficient, leading to assembly error."),
    upstream=U("NOT_REPORTED", [], "The chronology is provided as a separate document.", "chronology"),
    events=[])

# 20
L["RCLRPT-24V057-9009.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Hyundai WIA", "block"),
            C("S2", "INSUFFICIENT", "Name : Hyundai WIA", "block")],
    cause=CA("SUPPORTED", "Improperly heat-treated drive shaft."),
    upstream=U("NOT_REPORTED", [], "See attached document titled “2023-2024MY Niro EV and 2023MY EV6 Drive Shaft Chronology”.", "chronology"),
    events=[])

# 21
q21 = "12/15/2023 - LiveWire’s Service organization was notified of a report involving an alleged unexpected loss of propulsion on a LiveWire motorcycle."
e21 = "02/02/2024 – The TSC concluded its investigation and the root cause was determined to be related to software in the VSC."
L["RCLRPT-24V149-8136.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : LiveWire EV, LLC", "block"),
            C("S2", "SUPPORTED", q21, "chronology", name="LiveWire")],
    cause=CA("SUPPORTED", "On the affected population, the Vehicle Supervisory Controller (VSC) may initiate a shutdown of the electric vehicle powertrain due to exceeding software voltage thresholds."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("12/15/2023", "FILER_AWARENESS", q21),
            E("01/22/2024", "INVESTIGATION_START", "01/22/2024 - The Technical Subcommittee (TSC) launched a formal investigation of this issue."),
            E("01/23/2024", "INVESTIGATION_START", "01/23/2024 - 02/01/2024 - The TSC conducted a warranty/field service review, which identified two additional reports of a loss of propulsion that appeared to be potentially related to the Vehicle Supervisory Controller (VSC)."),
            E("02/02/2024", "OTHER", e21),
            E("02/02/2024", "OTHER", "The TSC escalated the matter to the Field Action Committee (FAC).", entry=e21),
            E("02/13/2024", "OTHER", "02/13/2024 – The FAC reviewed the TSC’s findings and analysis and escalated the matter to LiveWire’s Executive Decision Authority (EDA)."),
            E("02/16/2024", "DECISION", "02/16/2024 – Based upon the information developed during the investigation, the EDA authorized a recall to address this condition.")])

# 22
q22 = "December 28, 2023: Nova Bus was notified that a maintenance technician found evidence of arcing on the power cable to the alternator on a single bus."
L["RCLRPT-24V203-1211.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Nova Bus", "block"),
            C("S2", "SUPPORTED", q22, "chronology", name="Nova Bus")],
    cause=CA("SUPPORTED", "The assembly instructions did not clearly identify the required applied torque."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("December 28, 2023", "FILER_AWARENESS", q22),
            E("January 04, 2024", "INVESTIGATION_START", "January 04, 2024: A preliminary inspection of additional buses was performed."),
            E("January 08, 2024", "INVESTIGATION_START", "January 08, 2024: Nova Bus opened an investigation to determine the potential scope and risk level."),
            E("January 08, 2024", "OTHER", "January 08, 2024: An internal campaign issued to ensure the correct torque was applied to buses under manufacturing control."),
            E("January 10, 2024", "OTHER", "January 10, 2024: Product Safety Evaluation Committee evaluates the preliminary information."),
            E("January 18, 2024", "OTHER", "January 18, 2024: Product Safety Evaluation Committee raises the investigation to PSRI status and additional field information is gathered."),
            E("March 07, 2024", "OTHER", "March 07, 2024: Product Safety Evaluation Committee evaluates the investigation findings and raises to the Product Safety Committee."),
            E("March12, 2024", "DECISION", "March12, 2024: Product Safety Committee makes the determination of a product safety defect."),
            E("March 17, 2024", "NHTSA_FILING", "March 17, 2024: Nova Bus files DIR with NHTSA that a voluntary recall will be released to address the safety")])

# 23
L["RCLRPT-24V219-6791.txt"] = dict(
    claims=[C("S1", "NOT_REPORTED", "Name : NR", "block"),
            C("S2", "NOT_REPORTED", "", "")],
    cause=CA("SUPPORTED", "During an internal rework, some vehicles may have wrongly skipped the basic settings configuration of the high beam headlights."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("February 15, 2024", "FILER_AWARENESS", "On February 15, 2024 a report following quality controls indicated that some vehicles were missing the correct functionality of the high beam headlamps."),
            EI("INVESTIGATION_START", "An investigation was immediately launched which confirmed that the vehicles had undergone an internal rework after assembly release."),
            EI("OTHER", "Further analysis confirmed that a missing configuration step during rework was the cause for the missing functionality."),
            EI("OTHER", "Countermeasures were immediately implemented to ensure the correct configuration of vehicles in factory premises."),
            EI("INVESTIGATION_START", "Identification of potentially affected vehicles initiated and a compliance assessment was requested."),
            E("March 14, 2024", "OTHER", "On March 14, 2024 the results of investigation and assessments were presented in Lamborghini's Product Safety Committee."),
            EI("DECISION", "Out of abundance of caution the Product Safety Committee determined that a non-compliance with FMVSS108 which relates to vehicle safety cannot be ruled out and decided to conduct a voluntary recall.")])

# 24
q24 = "In early March 2024, Winnebago Product Safety found a defect in wiring on certain Access models."
L["RCLRPT-24V247-4988.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Winnebago Ind Inc.", "block"),
            C("S2", "SUPPORTED", q24, "chronology", name="Winnebago")],
    cause=CA("SUPPORTED", "Production incorrectly wired the GFCI outlet circuit, leading to unprotected outlets."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[E("early March 2024", "FILER_AWARENESS", q24),
            EI("INVESTIGATION_START", "Production was immediately notified and an investigation was opened."),
            E("March 28,2024", "DECISION", "On March 28,2024 the Product Safety Committee reviewed all available information and decided the issue presented an unreasonable risk to motor vehicle safety."),
            E("February 2, 2024", "FILER_AWARENESS", "The first submission occurred February 2, 2024.")])

# 25
q25 = "An investigation was opened and the supplier, Suburban, was notified."
q25b = "Winnebago has received claims/notices regarding these incidents on the following dates: 9/8/2022, 6/15/2023, 6/23/2023, 9/7/2023, 10/6/2023, and 1/9/2023"
L["RCLRPT-24V285-9407.txt"] = dict(
    claims=[C("S1", "SUPPORTED", "Name : Suburban Manufacturing", "block"),
            C("S2", "SUPPORTED", q25, "chronology", name="Suburban")],
    cause=CA("SUPPORTED", "The root cause was determined to be a manufacturing defect in the printed circuit board within the cooktop LED backlights."),
    upstream=U("NAMED", ["Suburban"], q25, "chronology"),
    events=[E("June 2023", "FILER_AWARENESS", "In June 2023, Winnebago was notified of two incidents related to melted LED light rings on stove knobs."),
            EI("INVESTIGATION_START", q25),
            EI("OTHER", "Winnebago continued to meet with the supplier over the next few months, working together to try and understand scope of the issue"),
            E("January 2024", "OTHER", "In January 2024, Winnebago escalated the issue to the Product Safety Committee."),
            E("January 26, 2024", "DECISION", "On January 26, 2024, the Product Safety Committee determined that the issue presents an unreasonable risk to safety.")]
           + [E(d, "FILER_AWARENESS", q25b) for d in ["9/8/2022", "6/15/2023", "6/23/2023", "9/7/2023", "10/6/2023", "1/9/2023"]])


# ---- verification and output ----
out = []
errs = []
for fn in sorted(x for x in os.listdir(T) if x.startswith("RCLRPT")):
    fileline, sec = sections(os.path.join(T, fn))
    lab = L[fn]

    def chk(q, s, what):
        if not q:
            return
        if len(q) > 300:
            errs.append(f"{fn} {what}: too long {len(q)}")
        if norm(q) not in sec[s]:
            errs.append(f"{fn} {what}: not found in {s}: {q[:80]}")

    for c in lab["claims"]:
        chk(c["quote"], c["section"], c["id"])
    chk(lab["cause"]["quote"], "cause", "cause")
    if lab["upstream"]["quote"]:
        chk(lab["upstream"]["quote"], lab["upstream"]["section"], "upstream")
    for i, ev in enumerate(lab["events"]):
        chk(ev["quote"], "chronology", f"event{i}")
        if ev["inherited_date"]:
            chk(ev["entry_quote"], "chronology", f"event{i}.entry")
            if ev["date_text"] not in ev["entry_quote"]:
                errs.append(f"{fn} event{i}: date not in entry")
        elif not ev["date_inferred"] and ev["date_text"] not in ev["quote"]:
            errs.append(f"{fn} event{i}: date not in quote")
    out.append({"file": fileline, "claims": lab["claims"], "cause": lab["cause"],
                "upstream": lab["upstream"], "events": lab["events"]})

if errs:
    print("\n".join(errs))
    sys.exit(1)
with open(os.path.join(D, "passB.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("ok", len(out), sum(len(o["events"]) for o in out))
