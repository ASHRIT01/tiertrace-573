import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEXTS = os.path.join(HERE, "texts")


def E(d, t, q):
    return {"date_text": d, "type": t, "quote": q, "inherited_date": False, "date_inferred": False}


def I(d, t, q, eq):
    return {"date_text": d, "type": t, "quote": q, "inherited_date": True, "entry_quote": eq, "date_inferred": False}


def N(t, q):
    return {"date_text": "", "type": t, "quote": q, "inherited_date": False, "date_inferred": True}


def S1(status, q):
    return {"id": "S1", "status": status, "quote": q, "section": "block"}


def S2(status, q, sec, name=None):
    d = {"id": "S2", "status": status}
    if name:
        d["name"] = name
    d["quote"] = q
    d["section"] = sec
    return d


def C(status, q):
    return {"status": status, "quote": q, "section": "cause"}


def U(kind, names, q, sec):
    return {"kind": kind, "names": names, "quote": q, "section": sec}


L = {}

# 1
f = "RCLRPT-25E013-1210"
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : Joyson Safety System"),
            S2("SUPPORTED", "JSS continued its investigation into the issue and thereafter concluded that parts from the entire inflator production run may be affected.", "chronology", "JSS")],
    cause=C("INSUFFICIENT", "JSS continues to investigate root cause but has found elevated moisture in the propellant and reduced propellant densities in parts from the affected production lot."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("November 13, 2024", "OTHER", "On November 13, 2024, VW recalled vehicles outside of the United States to replace affected head curtain airbags manufactured in a specific production lot following a field report."),
        N("INVESTIGATION_START", "JSS continued its investigation into the issue and thereafter concluded that parts from the entire inflator production run may be affected."),
        N("FILER_AWARENESS", "Subsequently, JSS was informed that one vehicle with a potentially affected part may be in the United States."),
        E("February 13, 2025", "DECISION", "On February 13, 2025, JSS's Product Safety Committee decided to file this report based on the information provided by VW."),
    ])

# 2
f = "RCLRPT-25E018-7359"
e715 = "July 15, 2025: Due to a data traceability investigation, BorgWarner notified Cummins that the total number of suspect packs is now 31, not 19."
L[f] = dict(
    claims=[S1("SUPPORTED", "Name: BorgWarner"),
            S2("SUPPORTED", "February 14, 2025: BorgWarner notified the Accelera Supplier Quality function of a quality issue", "chronology", "BorgWarner")],
    cause=C("SUPPORTED", "Supplier had inadequate manufacturing process control for internal fasteners."),
    upstream=U("NAMED", ["BorgWarner"], "February 14, 2025: BorgWarner notified the Accelera Supplier Quality function of a quality issue", "chronology"),
    events=[
        E("February 14, 2025", "SUPPLIER_NOTICE", "February 14, 2025: BorgWarner notified the Accelera Supplier Quality function of a quality issue"),
        E("February 21, 2025", "OTHER", "February 21, 2025: Discussion was initiated with the Accelera Product Safety team"),
        E("February 24, 2025", "OTHER", "February 24, 2025: Follow-up discussion was conducted with BorgWarner"),
        E("March 4, 2025", "DECISION", "March 4, 2025: Although Cummins neither manufactured the subject batteries nor assembled them into the drivetrain itself, the issue was reviewed by the Cummins Product Safety Defect Board (PSDB) and, based upon information available to date, the PSDB authorized this defect notification"),
        E("July 15, 2025", "SUPPLIER_NOTICE", e715),
        I("July 15, 2025", "OTHER", "Review by Cummins confirmed that 2 of these packs are in buses not in the original identified population, with the remaining additional packs still within the 103 already identified buses in the recall.", e715),
        I("July 15, 2025", "OTHER", "As such the total recall population was increased to 105.", e715),
        E("August 11, 2025", "SUPPLIER_NOTICE", "August 11, 2025: BorgWarner notified the Cummins Accelera Supplier Quality function that as a corrective action to missing manufacturing data, a new traceability system was introduced"),
        E("August 12, 2025", "OTHER", "August 12, 2025: Cummins submitted requests to BorgWarner to explain the new traceability system and to populate a spreadsheet for each battery pack supplied to Accelera"),
        E("August 21, 2025", "SUPPLIER_NOTICE", "August 21, 2025: BorgWarner provided responses to the Cummins Accelera Supplier Quality function."),
        E("August 25, 2025", "OTHER", "August 25, 2025: The Accelera service function confirmed the two additional battery packs are installed in vehicles located in the United States, necessitating an updated recall notification with NHTSA."),
    ])

# 3
f = "RCLRPT-25E064-2115"
L[f] = dict(
    claims=[S1("SUPPORTED", "Name: Marelli"),
            S2("INSUFFICIENT", "Name: Marelli", "block")],
    cause=C("NOT_REPORTED", ""),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("May 14, 2025", "INVESTIGATION_START", "On May 14, 2025, Stellantis Europe Customer Experience (\"CX\") opened an investigation for a potential issue related to rearview camera image not displaying in some 2020-2025 MY Alfa Romeo Giulia and Stelvio vehicles."),
        E("May 2025", "INVESTIGATION_START", "From May 2025, through June 2025, Stellantis Europe CX reviewed warranty data, field reports, and customer assistance records to understand potential customer consequence."),
        E("June 2025", "INVESTIGATION_START", "From June 2025, through July 2025, Stellantis Europe CX and Stellantis Europe Supplier Quality conducted tests to reproduce the issue and identify potential failure modes."),
        E("July 2025", "OTHER", "From July 2025, through September 2025, Stellantis Europe CX held regular meetings with Stellantis Europe Engineering and Stellantis Europe Supplier Quality to review manufacturing and quality control processes, part design, and production records"),
        E("September 25, 2025", "OTHER", "On September 25, 2025, Stellantis Europe CX organization recognized a vehicle build issue existed on certain vehicles related to the backup camera image not displaying, potentially causing a noncompliance with FMVSS No. 111."),
        E("September 30, 2025", "DECISION", "On September 30, 2025, Stellantis Europe S.p.A determined, through the Vehicle Regulations Committee, that a noncompliance to a Federal Motor Vehicle Safety Standard exists in certain motor vehicle equipment."),
    ])

# 4
f = "RCLRPT-25E071-3446"
gen = "At the supplier’s factory in Italy, a separation fence used to separate finished products from unfinished products was removed during the installation of new equipment."
e716 = "July 16, 2024 Honda received report of the issue in the Japanese market when the lug seat inserts were found missing during routine inspection of a customer’s vehicle."
L[f] = dict(
    claims=[S1("SUPPORTED", "Name: Honda Access Europe"),
            S2("INSUFFICIENT", gen, "cause")],
    cause=C("SUPPORTED", gen),
    upstream=U("UNNAMED", [], gen, "cause"),
    events=[
        E("July 16, 2024", "FILER_AWARENESS", e716),
        I("July 16, 2024", "INVESTIGATION_START", "Honda began to investigate and analyze the issue.", e716),
        E("August 7, 2024", "OTHER", "August 7, 2024 Honda conducted a check of units in US inventory and determined all wheels had the lug seat inserts present."),
        E("August – October 2024", "INVESTIGATION_START", "August – October 2024 Honda continued to investigate and analyze the issue."),
        E("November 15, 2024", "OTHER", "November 15, 2024 Honda began to evaluate potential measures for the Japanese market."),
        E("January – April 2025", "INVESTIGATION_START", "January – April 2025 Honda continued to investigate and analyze the issue."),
        E("May 12, 2025", "INVESTIGATION_START", "May 12, 2025 Honda began to consider wheels in the US market and continued to investigate the issue."),
        E("June 4, 2025", "INVESTIGATION_START", "June 4, 2025 Honda began to analyze the potential population of vehicles impacted in global markets, including the US."),
        E("October 23, 2025", "DECISION", "October 23, 2025 Honda determined that a defect related to motor vehicle safety and decided to conduct a safety recall."),
    ])

# 5
f = "RCLRPT-25V001-4568"
e1 = "This issue was first observed by Aston Martin 28th October."
sw = "The software fault was identified as part of software updates adopted in production from March 2024 and as part of a service campaign launched in October 2024."
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : ART SpA."),
            S2("INSUFFICIENT", "Name : ART SpA.", "block")],
    cause=C("SUPPORTED", "The root cause results from a software fault that affects application launch priorities."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("28th October", "FILER_AWARENESS", e1),
        I("28th October", "INVESTIGATION_START", "This opened an investigation", e1),
        E("March 2024", "OTHER", sw),
        E("October 2024", "OTHER", sw),
        N("OTHER", "The Company’s Technical Review Group (TRG) met regularly throughout the investigation."),
        E("20th December 2024", "OTHER", "The Company’s Critical Concerns Review Group (CCRG) met on 20th December 2024 to assess the nature and scope of potential concerns related to the software non-compliance."),
        N("OTHER", "The CCRG reviewed the technical data and recommended the matter should be reviewed by the Recall Committee."),
        E("24th December 2024", "DECISION", "The Recall Committee convened on 24th December 2024 and determined that: a. a non-compliance could occur in the relevant vehicle population;"),
    ])

# 6
f = "RCLRPT-25V023-3132"
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : Pirelli Tire, LLC"),
            S2("SUPPORTED", "DAG (MBAG) informed Pirelli Deutschland GmbH about the testing result on January 18, 2019.", "chronology", "Pirelli")],
    cause=C("SUPPORTED", "Due to a production deviation at the supplier, a certain batch of Pirelli Cinturato tires were marked with a maximum permissible inflation pressure of 340 kPa, despite being engineered to have a higher maximum inflation pressure of 350 kPa."),
    upstream=U("NAMED", ["Pirelli", "Pirelli Deutschland GmbH"], "DAG (MBAG) informed Pirelli Deutschland GmbH about the testing result on January 18, 2019.", "chronology"),
    events=[
        E("January 15, 2019", "FILER_AWARENESS", "On January 15, 2019, Daimler AG [(“DAG”) now known as MBAG] received information from the Korean authority (KATRI) that when testing a Pirelli Cinturato tire (tire size 245/45R18 100 Y) installed on a Mercedes vehicle,"),
        E("January 18, 2019", "OTHER", "DAG (MBAG) informed Pirelli Deutschland GmbH about the testing result on January 18, 2019."),
        N("INVESTIGATION_START", "Representatives of DAG (MBAG), Pirelli and KATRI reviewed the test methodology used by KATRI and Pirelli found that the tires had been incorrectly marked with a maximum tire pressure of 340 kPa instead of 350 kPa."),
        E("February 26, 2019", "SUPPLIER_NOTICE", "On February 26, 2019, Pirelli informed DAG (MBAG) that it had determined that the tires did not comply with the marking requirements of FMVSS 139, S5.5"),
        E("March 27, 2019", "OTHER", "DAG (MBAG) determined that this noncompliance was inconsequential as it relates to motor vehicle safety, and submitted a petition for inconsequential noncompliance on March 27, 2019."),
        E("December 7, 2022", "FILER_AWARENESS", "On December 7, 2022, NHTSA notified MBAG that it intended to deny MBAG’s petition for inconsequentiality."),
        E("December 9, 2022", "OTHER", "Subsequently, on December 9, 2022, the denial was published in the Federal Register."),
        E("December 20, 2022", "OTHER", "Pirelli filed an appeal of that denial on December 20, 2022."),
        N("OTHER", "MBAG filed a request for a stay of its related recall pending a decision on the appeal, which NHTSA allowed."),
        E("January 10, 2025", "OTHER", "The Pirelli appeal was denied by NHTSA on January 10, 2025."),
        E("January 17, 2025", "NHTSA_FILING", "Consequently, MBAG is submitting a new Noncompliance Information Report on January 17, 2025."),
        N("DECISION", "MBAG will conduct a recall to remedy affected vehicles."),
    ])

# 7
f = "RCLRPT-25V027-7244"
L[f] = dict(
    claims=[S1("NOT_REPORTED", "Name : NR"),
            S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "Engineering error."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("June 17, 2024", "FILER_AWARENESS", "On June 17, 2024, Forest River's Office of Corporate Compliance (\"OCC\") received an email from NHTSA on behalf of a state inspector, which indicated that a transit bus had egress handles and labels were not easily accessible as required by FMVSS 571.217."),
        E("June 20, 2024", "INVESTIGATION_START", "On June 20, 2024, OCC opened a research item into the concern and met with the manufacturing plant."),
        E("June 24, 2024", "INVESTIGATION_START", "On June 24, 2024, through June 28, 2024, the manufacturing plant and OCC continued to research the concern."),
        E("July 2, 2024", "DECISION", "On July 2, 2024, during an emergency meeting, the Corporate Safety Committee voted to recall."),
        E("July 3, 2024", "OTHER", "On July 3, 2024, During the final review of the scope, OCC and the Manufacturing Plant determined that the Starcraft Allstar was listed as the recalled model whereas it should have been the Starcraft Starlite only."),
        N("OTHER", "Further details were able to lower the scope from 100 vehicles to 62 vehicles."),
        E("September 11, 2024", "NHTSA_FILING", "On September 11, 2024, Forest River amended the recall to reflect dealers only within the scope of vehicles."),
        E("January 14, 2025", "OTHER", "On January 14, 2025, Forest River noticed a clerical error in the data."),
        N("OTHER", "Forest River is increasing the scope to 99 vehicles."),
        E("January 21, 2025", "FILER_AWARENESS", "On January 21, 2025, Forest River received an email from NHTSA requesting a new recall be filed due to the age of the recall, the additional model being added and increase in population,"),
        E("January 22, 2025", "NHTSA_FILING", "On January 22, 2025, Forest River filed a new recall for the amended population."),
        E("March 19, 2025", "OTHER", "On March 19, 2025, Forest River noticed a clerical error in the data."),
        N("NHTSA_FILING", "Forest River is amending the recall to increase the scope which includes 24 vehicles located at a single Dealer."),
    ])

# 8
f = "RCLRPT-25V032-4431"
aq = "The supplier of the center information display unit, Alps Alpine North America, Inc., informed Honda the software settings contained a programming defect which occurs when the transmission is shifted out of reverse and into another drive position within a certain time."
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : Alps Alpine North America, Inc."),
            S2("SUPPORTED", aq, "cause", "Alps Alpine North America, Inc.")],
    cause=C("SUPPORTED", aq),
    upstream=U("NAMED", ["Alps Alpine North America, Inc."], aq, "cause"),
    events=[
        E("October 23, 2024", "FILER_AWARENESS", "October 23, 2024 Honda discovered a potential issue with the center information display during a production vehicle review and informed the supplier, who began to investigate and analyze the issue."),
        E("December 16, 2024", "SUPPLIER_NOTICE", "December 16, 2024 Honda received an update from the supplier."),
        E("December 19, 2024", "INVESTIGATION_START", "December 19, 2024 Honda analyzed the information provided by the supplier."),
        E("January 16, 2025", "DECISION", "January 16, 2025 Honda determined that a defect related to motor vehicle safety and FMVSS noncompliance existed and decided to conduct a safety and noncompliance recall."),
    ])

# 9
f = "RCLRPT-25V037-7272"
L[f] = dict(
    claims=[S1("NOT_REPORTED", "Name : NR"),
            S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "The cause of the failures is improper sealing of the chassis harness."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("March 2024", "FILER_AWARENESS", "Beginning in March 2024, dealers in several countries overseas began to notice some trucks arrive from the manufacturer with condensation on the fuse box cover."),
        E("March", "FILER_AWARENESS", "Between March and July, dealers had submitted a total of 15 product quality reports to MFTBC."),
        N("INVESTIGATION_START", "During that time, MFTBC was researching the cause of the condensation and determined that water leaked into the wiring harness."),
    ])

# 10
f = "RCLRPT-25V100-5055"
eja = "July – August 2024: Five further engine compartment thermal cases are received."
ed3 = "December 3, 2024: Topic discussed in technical clarification meeting."
ef10 = "February 10, 2025: Topic discussed at the Volkswagen Product Safety Committee."
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : POLYTEC CAR STYLING"),
            S2("INSUFFICIENT", "Name : POLYTEC CAR STYLING", "block")],
    cause=C("SUPPORTED", "Improper fixation of the engine cover after engine maintenance or vehicle service."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("October 3, 2023", "FILER_AWARENESS", "October 3, 2023: First potentially relevant engine compartment thermal case received by Volkswagen; however, the root cause was not able to be determined."),
        E("July – August 2024", "FILER_AWARENESS", eja),
        I("July – August 2024", "OTHER", "Two of these cases were determined to be the caused by of improperly installed engine covers after vehicle maintenance service.", eja),
        E("October – November 2024", "FILER_AWARENESS", "October – November 2024: An additional engine compartment thermal case received; VW conducts analysis to evaluate engine covers on in-use pool vehicles."),
        E("December 3, 2024", "OTHER", ed3),
        I("December 3, 2024", "INVESTIGATION_START", "Additional information sought regarding root cause of the thermal cases, the influence of the engine cover, the effects of pre-damage to the engine cover, and the influence of vehicle service.", ed3),
        E("December 4, 2024", "INVESTIGATION_START", "December 4, 2024 – January 15, 2025: Further analysis conducted into the factors necessary to trigger the events, influence of service technician handling, instructions for engine cover removal, the impact of driving behavior on the engine cover, and internal part release testing results."),
        E("January 16, 2025", "OTHER", "January 16, 2025: Topic discussed at the NAR Volkswagen Product Safety Committee and escalated to the Volkswagen Product Safety Committee for a determination."),
        E("February 5, 2025", "OTHER", "February 5, 2025: Topic discussed at the Volkswagen Product Safety Committee and further task to clarify affected population was assigned."),
        E("February 10, 2025", "OTHER", ef10),
        I("February 10, 2025", "DECISION", "Based on the thermal events in the field, and because the risk of the engine cover coming loose after vehicle service could not be ruled out, a recall was decided to mitigate the potential safety risk.", ef10),
    ])

# 11
f = "RCLRPT-25V102-4724"
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : Volvo Trucks"),
            S2("SUPPORTED", "February 12, 2025 Volvo Product Safety Product Committee reviews information and determines that a product non-compliance exists.", "chronology", "Volvo")],
    cause=C("SUPPORTED", "In-sufficient control of non-conforming vehicles within our factory."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("February 6, 2025", "OTHER", "February 6, 2025 Volvo Product Compliance Committee meets and reviews a case of specific vehicles built with back of cab and end of frame air were transferred without being compliant to FMVSS 121"),
        E("February 12, 2025", "DECISION", "February 12, 2025 Volvo Product Safety Product Committee reviews information and determines that a product non-compliance exists."),
        E("February 18, 2025", "NHTSA_FILING", "February 18, 2025 573 filed with NHTSA."),
    ])

# 12
f = "RCLRPT-25V103-1864"
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : Panasonic Automotive Systems"),
            S2("INSUFFICIENT", "Name : Panasonic Automotive Systems", "block")],
    cause=C("SUPPORTED", "Based on consideration of field complaints of rearview camera issues and comparisons to the updated software version, it is assumed that the affected versions of the software contained certain bugs that could lead to a delayed rearview image or blackscreen when reversing,"),
    upstream=U("NOT_REPORTED", [], "Please see chronology document uploaded to NHTSA portal.", "chronology"),
    events=[])

# 13
f = "RCLRPT-25V112-9017"
L[f] = dict(
    claims=[S1("NOT_REPORTED", "Name : NR"),
            S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "Engineering Error."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("February 14, 2025", "FILER_AWARENESS", "On February 14, 2025, Forest River's Office of Corporate Compliance (\"OCC\") found a vehicle with an under- rated coupler capacity during a safety chain audit from a separate research concern."),
        N("INVESTIGATION_START", "A research item was opened into the concern."),
        E("February 21, 2025", "DECISION", "On February 21, 2025, Forest River's Corporate Safety Committee voted to recall."),
        N("OTHER", "A Stop Sale Notice is being issued today as well."),
    ])

# 14
f = "RCLRPT-25V118-5335"
gq = "April 2024: As a result of an investigation at the battery supplier, KML found that the anchor for the terminal inside the drive battery connector was missing."
em = "March 2024: Kawasaki Motors, Ltd (KML) Quality Assurance Division found that an NX011A vehicle stalled due a loss of power during an periodic regular running test."
ea = "August 2024: The supplier conducted an inspection of battery inventory with manufacturing dates before June 2024 when the assembly inspection process was implemented."
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : Forsee Power Japan GK"),
            S2("INSUFFICIENT", gq, "chronology")],
    cause=C("SUPPORTED", "Improper manufacturing process of the drive batteries."),
    upstream=U("UNNAMED", [], gq, "chronology"),
    events=[
        E("March 2024", "FILER_AWARENESS", em),
        I("March 2024", "OTHER", "The terminal of the drive battery connector was found to be caved in.", em),
        E("April 2024", "INVESTIGATION_START", gq),
        E("May 2024", "INVESTIGATION_START", "May 2024: The supplier began inspecting its inventory for this fault."),
        E("August 2024", "INVESTIGATION_START", ea),
        I("August 2024", "OTHER", "This inspection uncovered one additional battery with a terminal that could cave in due to the lack of an anchor.", ea),
        E("February 19, 2025", "DECISION", "February 19, 2025：Because KML cannot guarantee that there are not more defective units in the field, KML decided to initiate a recall campaign."),
    ])

# 15
f = "RCLRPT-25V119-7599"
ej = "January 28, 2025 - Grand Design Dealer submitted claim for bad bearings on a 2025 Serenova."
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : Mor-Ryde"),
            S2("SUPPORTED", "Grand Design notified Mor-Ryde through normally warranty process.", "chronology", "Mor-Ryde")],
    cause=C("SUPPORTED", "Grand Design was notified by MorRyde that some independent suspension components, supplied to Grand Design, may have a castle nut that is over torqued on the axle spindle."),
    upstream=U("NAMED", ["Mor-Ryde"], "Grand Design notified Mor-Ryde through normally warranty process.", "chronology"),
    events=[
        E("January 28, 2025", "FILER_AWARENESS", ej),
        I("January 28, 2025", "OTHER", "Grand Design notified Mor-Ryde through normally warranty process.", ej),
        E("January 30, 2025", "INVESTIGATION_START", "January 30, 2025 - February 5, 2025 – Mor-Ryde inspected Grand Design units online and in dealer storage lot."),
        E("February 7, 2025", "OTHER", "February 7, 2025 - Grand Design spoke with Mor-Ryde and recommended that Mor-Ryde submit for equipment recall."),
        E("February 10, 2025", "OTHER", "February 10, 2025 – Mor-Ryde Safety Committee met and voted to issue a safety recall."),
        E("February 11, 2025", "INVESTIGATION_START", "February 11, 2025 - Mor-Ryde began internal investigation."),
        E("February 19, 2025", "OTHER", "February 19, 2025 - Mor-Ryde shared their company warranty contact details and written repair instructions, with Grand Design."),
        E("February 20, 2025", "DECISION", "February 20, 2025 - Grand Design Safety Committee met and voted to issue a safety recall."),
    ])

# 16
f = "RCLRPT-25V132-5563"
L[f] = dict(
    claims=[S1("SUPPORTED", "Name: Ford Motor Company"),
            S2("SUPPORTED", "On February 21, 2025, Ford’s Field Review Committee reviewed the concern and approved a field action", "chronology", "Ford")],
    cause=C("SUPPORTED", "The dealer instructions to complete the recall instruct the technician to upload the latest software using the service tool, which downloads the latest software from Ford for installation on the vehicle."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("November 26, 2024", "FILER_AWARENESS", "On November 26, 2024, an issue pertaining to incomplete software recall remedies was brought to Ford’s Critical Concern Group (CCRG) for review."),
        N("FILER_AWARENESS", "This issue was initially identified in a Quality Office forum, where an audit was requested for software part numbers applied to a vehicle remedied under a sample of field service actions (FSAs)."),
        N("INVESTIGATION_START", "Initial review of three FSAs revealed insufficient data to confirm correct software application across all FSAs using the FDRS service tool."),
        N("INVESTIGATION_START", "Further investigation was deemed necessary."),
        E("December 2024", "INVESTIGATION_START", "In December 2024, a cross-functional team was formed to audit all software FSAs that used the FDRS service tool, with its first focus being on safety and compliance FSAs."),
        N("OTHER", "Templates were created to track software lineage part numbers."),
        E("December 19, 2024", "OTHER", "On December 19, 2024, Ford informed NHTSA of this concern -- the service tool data confirmed that the software state on the service tool at the time of installation matches the FSA software release for most vehicles."),
        N("OTHER", "Ford discussed with NHTSA its plan to address the mismatched vehicles."),
        E("January 2025", "OTHER", "In January 2025, the cross- functional team created database records to store all software lineage part numbers for previously launched FSAs."),
        N("INVESTIGATION_START", "The team then began auditing the current software level for every VIN repaired under several previously launched FSAs."),
        E("February 17, 2025", "OTHER", "On February 17, 2025, the cross-functional team completed the audit of 22S17 and brought the results to Ford’s CCRG for review, concluding that 97.1% of the repairs conducted under 22S17 had the correct software installed."),
        N("OTHER", "The team identified the specific vehicles that were recorded as receiving the remedy, but have software listed that does not remedy the safety defect."),
        E("February 21, 2025", "DECISION", "On February 21, 2025, Ford’s Field Review Committee reviewed the concern and approved a field action"),
        E("November 17, 2025", "FILER_AWARENESS", "On November 17, 2025, a bug in the audit dashboard logic for FSA audits was discovered."),
        N("INVESTIGATION_START", "A review of the vehicles shown as repaired was conducted after this bug was identified resulting in the identification of VINs incorrectly closed as repaired without receiving the FSA remedy."),
        E("December 11, 2025", "DECISION", "On December 11, 2025, Ford’s Field Review Committee reviewed the concern and approved an amendment to this field action."),
    ])

# 17
f = "RCLRPT-25V164-5067"
f6 = "On February 6, 2025, an issue pertaining to certain 10R transmissions was brought to Ford’s Critical Concern Review Group for review after Ford learned of a 2025 MY Mustang that experienced a transmission failure at Flat Rock Assembly Plant (FRAP) on January 31, 2025."
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : Ford Motor Company"),
            S2("SUPPORTED", "On March 7, 2025, Ford’s Field Review Committee reviewed the concern and approved a field action.", "chronology", "Ford")],
    cause=C("SUPPORTED", "Ford has identified two bores within the Outer Valve Body (OVB) of the transmission main control whose diameter and circularity dimensions did not meet the engineering print specification."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("February 6, 2025", "FILER_AWARENESS", f6),
        E("January 31, 2025", "OTHER", f6),
        N("OTHER", "On that same day, Ford issued a Stop Ship for 2025MY F150 ICE/HEV, Bronco, Ranger, Mustang, Explorer, and Aviator models containing these 10R transmissions."),
        N("FILER_AWARENESS", "Ford learned that other vehicles, with 10R transmissions machined at the same Outer Valve Body (OVB) machining center at Livonia Transmission Plant (LTP), exhibited similar symptoms."),
        N("INVESTIGATION_START", "The suspect transmission was returned to LTP for testing and analysis."),
        N("OTHER", "This analysis determined that the E-Clutch shift solenoid in the OVB in the main control assembly (MCA) was stuck ON due to out-of-specification machining."),
        N("INVESTIGATION_START", "Ford’s investigation utilized plant process run data from the suspect machining center to create a Machine Integrated Learning and Optimization (MILO) model that was successfully able to detect individual OVB units that were likely to experience this condition."),
        N("INVESTIGATION_START", "Ford engineering and CCRG team members conducted evaluations of vehicles equipped with suspect parts from the identified production population and confirmed the symptoms as described by field reports."),
        E("March 7, 2025", "DECISION", "On March 7, 2025, Ford’s Field Review Committee reviewed the concern and approved a field action."),
    ])

# 18
f = "RCLRPT-25V217-8601"
mq = "In the Isuzu EVs, the electric drive motor manufacturer prefills the EV drive motor cooling circuit with Valvoline G40 coolant."
L[f] = dict(
    claims=[S1("SUPPORTED", "Name: Aisin Corporation"),
            S2("INSUFFICIENT", mq, "cause")],
    cause=C("INSUFFICIENT", "Although Isuzu has not definitively identified the root cause, it believes, based on its investigation, that the Valvoline Zerex Dex Cool coolant in these vehicles may react with additives in the Valvoline G40 coolant and components within the EV drive motor cooling system,"),
    upstream=U("NAMED", ["Valvoline"], mq, "cause"),
    events=[
        E("January 23, 2025", "FILER_AWARENESS", "On January 23, 2025, Isuzu received a Technical Assistance Case reporting loss of vehicle propulsion on a NRR EV truck."),
        N("INVESTIGATION_START", "Isuzu promptly began an investigation, including collecting relevant parts and conducting duplication testing."),
        E("February", "INVESTIGATION_START", "In February, Isuzu continued its investigation."),
        N("FILER_AWARENESS", "Six additional reports of reduced power mode related to loss of propulsion were received."),
        N("OTHER", "Upon inspecting the incident vehicles, Isuzu observed small black debris floating in the coolant tank of one vehicle, and black gel-like material adhered to the metal rotor shaft of the EV drive motor/system coolant pump on other vehicles."),
        N("OTHER", "Isuzu also confirmed that the incident vehicles lost all vehicle propulsion when the coolant pump rotor seized to the pump shaft."),
        N("OTHER", "Testing confirmed that the black gel-like deposits found inside the coolant pumps of affected vehicles contained components derived from the coolant."),
        E("March", "INVESTIGATION_START", "In March, Isuzu focused its investigation on the coolant used in the coolant system, including reproduction testing to confirm contribution of the specific coolant used in the NRR EV trucks in the United States."),
        N("OTHER", "Isuzu’s investigation also revealed that NRR EV trucks manufactured in Japan use a different coolant in the cooling system and have had no incidents of pump seizure."),
        E("April 1, 2025", "DECISION", "On April 1, 2025, Isuzu made a decision to conduct a safety-related recall to address this issue."),
    ])

# 19
f = "RCLRPT-25V222-7359"
iq = "The U-bolt supplier, IMT Standens, was contacted to discuss the situation to determine whether these U-bolts were different from previously delivered units."
two = "During two separate instances of vehicle preparation before delivery (January 27 and February 12, 2025), GM vehicles that have been equipped with supplemental suspension blades were found in the yard with a broken U-bolt."
mar = "Following the information that After-sales service had received two claims in March 2025 concerning U-bolts breakage and the discovery of another occurrence in the yard, it was decided on March 28, to temporarily stop installing supplemental suspension blades"
L[f] = dict(
    claims=[S1("SUPPORTED", "Name: IMT Standens"),
            S2("SUPPORTED", iq, "chronology", "IMT Standens")],
    cause=C("NOT_REPORTED", ""),
    upstream=U("NAMED", ["IMT Standens", "GM"], iq, "chronology"),
    events=[
        E("January 27", "FILER_AWARENESS", two),
        E("February 12, 2025", "FILER_AWARENESS", two),
        N("OTHER", iq),
        N("INVESTIGATION_START", "At the same time, some U-bolts were sent for analysis to the Canadian Material Testing Bureau to determine whether there was an issue with the material of the U-bolts."),
        N("OTHER", "The results were not conclusive in both instances."),
        E("March 2025", "FILER_AWARENESS", mar),
        E("March 28", "OTHER", mar),
        E("April 1, 2025", "DECISION", "Even though the source cause of the breakage has not been identified, it was decided, on April 1, 2025, to recall the GM vehicles in which the GM original U-bolts were replaced with IMT Standens U-bolts."),
    ])

# 20
f = "RCLRPT-25V295-2205"
L[f] = dict(
    claims=[S1("SUPPORTED", "Name: Daimler Truck North America"),
            S2("SUPPORTED", "On April 30, 2025, out of an abundance of caution, DTNA decided to conduct a recall for this issue.", "chronology", "DTNA")],
    cause=C("NOT_REPORTED", ""),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("early April 2025", "FILER_AWARENESS", "In and around early April 2025, DTNA identified an issue related to the tool used to verify air tank capacity and initiated a product investigation."),
        N("INVESTIGATION_START", "DTNA’s review of vehicle specifications and volume calculations revealed a potential issue relating to air chamber and air tank sizing requirements where certain vehicles may have been produced with an undersized air reservoir capacity in relation to brake chamber volume"),
        N("OTHER", "DTNA also identified that the verification tool intended to send automatic alerts in the event of insufficient air capacity was not performing as intended."),
        E("April 30, 2025", "DECISION", "On April 30, 2025, out of an abundance of caution, DTNA decided to conduct a recall for this issue."),
        E("June 23, 2025", "NHTSA_FILING", "On June 23, 2025 DTNA amended its Part 573 Report to provide a description of the final remedy for this recall."),
        E("July 7, 2025", "NHTSA_FILING", "On July 7, 2025 DTNA resubmitted the earlier-submitted dates."),
    ])

# 21
f = "RCLRPT-25V297-4164"
L[f] = dict(
    claims=[S1("SUPPORTED", "Name : Marelli"),
            S2("INSUFFICIENT", "Name : Marelli", "block")],
    cause=C("NOT_REPORTED", "NR"),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("March 27, 2025", "INVESTIGATION_START", "On March 27, 2025, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation for a potential issue related to a delay in the PRND display in the 3.5\" cluster in some 2025 MY Ram 2500 and 3500 vehicles."),
        E("March 2025", "OTHER", "From March 2025, through April 2025, FCA US TSRC met with FCA US engineering and supplier quality to review the issue, understand the failure mode, and to determine the suspect population."),
        E("April 16, 2025", "OTHER", "On April 16, 2025, the FCA US TSRC organization recognized a vehicle build issue exists on certain vehicles related to a delay in the PRND in the 3.5\" cluster display, potentially resulting in a non-compliance with FMVSS 101."),
        E("May 01, 2025", "DECISION", "On May 01, 2025, FCA US determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected vehicles."),
    ])

# 22
f = "RCLRPT-25V307-4487"
L[f] = dict(
    claims=[S1("NOT_REPORTED", "Name : NR"),
            S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "Manufacturing Error"),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("May 5, 2025", "FILER_AWARENESS", "On May 5, 2025, Forest River's Office of Corporate Compliance (\"OCC\") was notified that during a routine Pre- Delivery Inspection (\"PDI\") at the Forest River PDI Center that the concern was discovered."),
        N("INVESTIGATION_START", "OCC opened a research item."),
        E("May 9, 2025", "DECISION", "On May 9, 2025, Forest River's Corporate Committee voted to recall."),
    ])

# 23
f = "RCLRPT-25V377-7112"
e512 = "5/12/2025 A Starcraft RV dealer sent an email regarding two lot units that had a GVWR listed at 7995 lbs. built with 7600 lbs. safety chains specific to the Starcraft Autumn Ridge 26BHS Travel Trailers."
L[f] = dict(
    claims=[S1("NOT_REPORTED", ""),
            S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "There was a discrepancy regarding safety chain weight ratings listed on the Jayco Engineering data sheet and prints."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("5/12/2025", "FILER_AWARENESS", e512),
        I("5/12/2025", "INVESTIGATION_START", "Jayco engineering started an Investigation immediately.", e512),
        I("5/12/2025", "OTHER", "Jayco Inc. engineering determined that the 7600 lbs. safety chains are underrated on these specific trailers and need to be replaced with the 11,700 lbs. safety chains.", e512),
        E("5/19/2025", "OTHER", "5/19/2025 The Warranty Incident Review Committee (WIRC) discussed the incident and elevated it to CPAC."),
        E("5/29/2025", "OTHER", "5/29/2025 The Corrective Preventive Action Committee (CPAC) discussed the incident and elevated it to SSC."),
        E("5/30/2025", "DECISION", "5/30/2025 The Safety Steering Committee (SSC) met and voted to proceed with filing a safety recall with NHTSA."),
    ])

# 24
f = "RCLRPT-25V378-0084"
L[f] = dict(
    claims=[S1("NOT_REPORTED", ""),
            S2("NOT_REPORTED", "", "")],
    cause=C("SUPPORTED", "Due to a temporary shortage of production personnel, the standard fuel feed hose installation process was divided into two separate tasks."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("May 4, 2025", "FILER_AWARENESS", "May 4, 2025 Honda found a fuel leak in a CR-V Hybrid during a production quality inspection and began to investigate."),
        E("May 5-8, 2025", "INVESTIGATION_START", "May 5-8, 2025 Honda inspected completed production vehicles to identify other vehicles with leaks"),
        E("May 14, 2025", "INVESTIGATION_START", "May 14, 2025 Honda continued to investigate and analyze the issue."),
        E("May 16, 2025", "INVESTIGATION_START", "May 16, 2025 Honda investigated the population of affected vehicles."),
        E("May 29, 2025", "DECISION", "May 29, 2025 Honda determined that a defect related to motor vehicle safety and FMVSS noncompliance existed and decided to conduct a safety and noncompliance recall."),
    ])

# 25
f = "RCLRPT-25V381-4395"
L[f] = dict(
    claims=[S1("SUPPORTED", "Name: Q'Straint"),
            S2("INSUFFICIENT", "Name: Q'Straint", "block")],
    cause=C("SUPPORTED", "The root cause analysis determined that torque tools used during the manufacturing installation process came out of calibration resulting in lower torque being applied to the fasteners."),
    upstream=U("NONE_MENTIONED", [], "", ""),
    events=[
        E("May 28th", "FILER_AWARENESS", "On May 28th, we received a report from a customer indicating that an occupant restraint puck in one of their units was loose."),
        N("INVESTIGATION_START", "This prompted an immediate investigation into our internal processes and inventory."),
        N("OTHER", "The Quality Process Team discovered that improperly calibrated torque tools were used by the installers of the puck."),
        N("OTHER", "Consequently, all inventory on the lot was pulled, inspected, and corrected by removing the bolts, applying blue thread locker, and using a properly calibrated torque wrench to reinstall the bolts to the manufacturer's specified torque of 40 ft-lbs."),
        E("May 29th", "OTHER", "All on-site inventory was repaired, and an internal process was established on May 29th to ensure that torque tools remain within specification going forward."),
        E("May 30th", "INVESTIGATION_START", "Starting May 30th, we dispatched representatives from our service and quality teams to dealer network lots to inspect previously built inventory."),
        E("June 3rd", "OTHER", "Through the inspection of unsold units, it was determined on June 3rd that the window of effect was from January 6, 2025 through May 29, 2025"),
    ])


# ---------------- build + verify ----------------
def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def sections(path):
    txt = open(path, encoding="utf-8").read()
    first = txt.splitlines()[0]
    assert first.startswith("FILE: ")
    fname = first[6:].strip()
    blk = txt.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    cause = txt.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    chron = txt.split("=== CHRONOLOGY ===")[1]
    return fname, {"block": norm(blk), "cause": norm(cause), "chronology": norm(chron)}


out = []
errs = []
for stem in sorted(L):
    fname, sec = sections(os.path.join(TEXTS, stem + ".txt"))
    lab = L[stem]
    obj = {"file": fname, "claims": lab["claims"], "cause": lab["cause"], "upstream": lab["upstream"], "events": lab["events"]}

    def chk(q, s, what):
        if q == "":
            return
        if len(q) > 300:
            errs.append(f"{stem} {what}: too long {len(q)}")
        if norm(q) != q:
            errs.append(f"{stem} {what}: not normalized")
        if s not in sec or q not in sec[s]:
            errs.append(f"{stem} {what}: quote not found in {s}: {q[:80]}")

    for c in obj["claims"]:
        chk(c["quote"], c["section"], c["id"])
    chk(obj["cause"]["quote"], "cause", "cause")
    chk(obj["upstream"]["quote"], obj["upstream"]["section"], "upstream")
    for i, ev in enumerate(obj["events"]):
        chk(ev["quote"], "chronology", f"ev{i}")
        if not ev["date_inferred"] and ev["date_text"] not in ev["quote"] and not ev["inherited_date"]:
            errs.append(f"{stem} ev{i}: date_text not in quote")
        if ev["inherited_date"]:
            chk(ev["entry_quote"], "chronology", f"ev{i}-entry")
            if ev["date_text"] not in ev["entry_quote"]:
                errs.append(f"{stem} ev{i}: date_text not in entry_quote")
    out.append(obj)

if errs:
    print("\n".join(errs))
    sys.exit(1)
with open(os.path.join(HERE, "passB.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("ok", len(out), sum(len(o["events"]) for o in out))
