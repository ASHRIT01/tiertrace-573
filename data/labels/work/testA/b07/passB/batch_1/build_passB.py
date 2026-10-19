import json, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def sections(path):
    raw = open(path, encoding="utf-8").read()
    fileline = re.search(r"^FILE: (.+)$", raw, re.M).group(1).strip()
    b = raw.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    c = raw.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    h = raw.split("=== CHRONOLOGY ===")[1]
    return fileline, {"block": norm(b), "cause": norm(c), "chronology": norm(h)}

def E(d, t, q):
    return {"date_text": d, "type": t, "quote": q, "inherited_date": False, "date_inferred": False}
def H(d, t, q, entry):
    return {"date_text": d, "type": t, "quote": q, "inherited_date": True, "entry_quote": entry, "date_inferred": False}
def I(t, q):
    return {"date_text": "", "type": t, "quote": q, "inherited_date": False, "date_inferred": True}

def S1(status, q):
    return {"id": "S1", "status": status, "quote": q, "section": "block" if q else ""}
def S2(status, q="", sec="", name=None):
    d = {"id": "S2", "status": status}
    if name is not None:
        d["name"] = name
    d["quote"] = q
    d["section"] = sec
    return d
def C(status, q, sec="cause"):
    return {"status": status, "quote": q, "section": sec if q else ""}
def U(kind, q="", sec="", names=None):
    return {"kind": kind, "names": names or [], "quote": q, "section": sec}

L = {}

# 25V407
e1 = "April – June 2025 On April 15, 2025, Ford’s Product Development Quality team identified a loose C-Pillar applique on an internal test vehicle."
L["RCLRPT-25V407-8066.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Cooper Standard Automotive Inc."),
         S2("INSUFFICIENT", "The components may detach due to inadequate application pressure of the components during assembly at the supplier facility that results in insufficient adhesive retention.", "cause")],
 cause=C("SUPPORTED", "The components may detach due to inadequate application pressure of the components during assembly at the supplier facility that results in insufficient adhesive retention."),
 upstream=U("UNNAMED", "The components may detach due to inadequate application pressure of the components during assembly at the supplier facility that results in insufficient adhesive retention.", "cause"),
 events=[
  E("April 2022 - May 2023", "INVESTIGATION_START", "April 2022 - May 2023 Ford’s Critical Concern Review Group (CCRG) investigated this concern and concluded that it did not present an unreasonable risk to motor vehicle safety."),
  E("April 15, 2025", "FILER_AWARENESS", "On April 15, 2025, Ford’s Product Development Quality team identified a loose C-Pillar applique on an internal test vehicle."),
  E("April 22, 2025", "INVESTIGATION_START", "On April 22, 2025, this issue was brought to Ford’s CCRG for review."),
  E("May 2025", "INVESTIGATION_START", "Throughout May 2025, CCRG and Ford’s engineering teams worked to better understand the factors that lead to the detachment of C-pillar applique and division bar looseness and detachment."),
  H("April – June 2025", "INVESTIGATION_START", "CCRG reviewed field and warranty data, and potential for occurrence at higher mileages in the future via statistical projections.", e1),
  H("April – June 2025", "INVESTIGATION_START", "Supplier process improvement actions were reviewed by Ford’s Supplier Technical Assistance team to assist in determining suspect population scoping.", e1),
  H("April – June 2025", "INVESTIGATION_START", "The investigation also included a new assessment of the risk factors that considered recent road hazard safety recalls and continued discussions with NHTSA on road hazard risks.", e1),
  E("June 6th, 2025", "DECISION", "On June 6th, 2025, Ford’s Field Review Committee reviewed the concern and approved a field action."),
 ])

# 25V410
L["RCLRPT-25V410-8258.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Tesla, Inc."),
         S2("SUPPORTED", "On June 10, 2025, having completed its investigation, Tesla made a determination to voluntarily recall the affected vehicles.", "chronology", name="Tesla")],
 cause=C("NOT_REPORTED", ""),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("May 12, 2025", "FILER_AWARENESS", "On May 12, 2025, as part of routine monitoring of field repairs, Tesla became aware of a customer complaint for a vehicle in which service found 2 of the 4 fasteners used to secure the seat back to the seat bottom missing on the driver’s seat."),
  E("May 13 through June 10, 2025", "INVESTIGATION_START", "From May 13 through June 10, 2025, Tesla investigated the effect and scope of the condition."),
  E("April 2, 2025", "OTHER", "During this period, Tesla learned that a production change introduced on April 2, 2025, unintentionally resulted in the ability to manually advance the seat assembly from the back-up manual assembly station,"),
  E("June 10, 2025", "DECISION", "On June 10, 2025, having completed its investigation, Tesla made a determination to voluntarily recall the affected vehicles."),
 ])

# 25V425
L["RCLRPT-25V425-5439.txt"] = dict(
 claims=[S1("NOT_REPORTED", ""), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "Keep the patio door from opening while in transit - manufacturing."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("June 17, 2025", "FILER_AWARENESS", "On June 17, 2025, during a routine Corporate Standards Audit, the concern was identified in the manufacturing plant."),
  E("June 18, 2025", "FILER_AWARENESS", "Forest River's Office of Corporate Compliance (\"OCC\") was notified on June 18, 2025."),
  E("June 19, 2025", "INVESTIGATION_START", "On June 19, 2025, OCC opened a research item into the concern."),
  I("INVESTIGATION_START", "OCC and the manufacturing plant began to confirm the vehicles involved."),
  E("June 20, 2025", "DECISION", "On June 20, 2025, Forest River's Corporate Committee voted to recall."),
 ])

# 25V426
L["RCLRPT-25V426-3816.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Hyundai Mobis"), S2("INSUFFICIENT", "Name: Hyundai Mobis", "block")],
 cause=C("SUPPORTED", "Voltage surges in the rearview camera power circuit over time may cause damage to the camera."),
 upstream=U("NOT_REPORTED", "See attached document titled “2020-2022MY Niro EV Rearview Camera Chronology”", "chronology"),
 events=[])

# 25V441
L["RCLRPT-25V441-5547.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: TE Connectivity"), S2("INSUFFICIENT", "Name: TE Connectivity", "block")],
 cause=C("SUPPORTED", "The high voltage battery Bussed Electrical Center (BEC) main contactor design and part-to-part variation is not robust to heat generated from multiple wide-open pedal and DC Fast-Charge events."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("October 6, 2023", "DECISION", "On October 6, 2023, Ford’s Field Review Committee approved field action 23V687 (23S56) to address a condition in which Direct Current (“DC”) fast charging and repeated wide open pedal events may cause the high voltage battery main contactors to overheat."),
  E("June 3, 2025", "INVESTIGATION_START", "In support of Ford’s obligations under paragraph 44 of the Ford consent order with NHTSA, Ford’s CCRG opened an investigation to review scoping of FSA 23S56/23V687 on June 3, 2025."),
  E("May 27, 2022", "OTHER", "The investigation identified that Bussed Electrical Center parts affected by this condition were taken out of production at Cuautitlan Assembly Plant (CSAP) for Extended Range non-GT variants on May 27, 2022."),
  E("June 20, 2025", "DECISION", "On June 20, 2025, Ford’s Field Review Committee reviewed the concern and approved an amendment to the 23V687 (23S56) field action."),
 ])

# 25V444
e_may = "May 29, 2025 – Oshkosh observes wrinkling on the airbag warning and roll-over warning labels which are placed on the sun visors of production vehicles located at the Oshkosh facility."
e_jun = "June 2025 – After identifying vehicles with the customer where the sun visor and rollover warning labels are wrinkled and starting to delaminate in certain locations, Oshkosh begins to focus on the thickness of the sun visor labels, the adhesive on them, and the surface material of the sun visor."
L["RCLRPT-25V444-3918.txt"] = dict(
 claims=[S1("NOT_REPORTED", ""), S2("NOT_REPORTED")],
 cause=C("NOT_REPORTED", ""),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("May 29, 2025", "FILER_AWARENESS", e_may),
  H("May 29, 2025", "INVESTIGATION_START", "Oshkosh begins to evaluate this condition to understand whether the wrinkling is limited to the vehicles observed at the Oshkosh facility or may exist in other vehicles and to ascertain the impact to the customer of this wrinkling.", e_may),
  E("June 2025", "INVESTIGATION_START", e_jun),
  H("June 2025", "INVESTIGATION_START", "Attention is given to their ability to remain permanently attached to the sun visor after installment.", e_jun),
  H("June 2025", "INVESTIGATION_START", "In addition, all labels present on the sun visor including the rollover warning label and electric shock warning label present on the BEV version of the vehicles, and their placement, are evaluated.", e_jun),
  E("June 19, 2025", "DECISION", "June 19, 2025 – After concluding that the airbag warning label may not remain permanently attached to the sun visor and other information is present on the same side of the sun visor as the airbag warning label Oshkosh determines that the sun visors do not meet certain labeling requirements of FMVSS"),
 ])

# 25V464
L["RCLRPT-25V464-0276.txt"] = dict(
 claims=[S1("NOT_REPORTED", ""), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "Manufacturing error."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("July 9, 2025", "FILER_AWARENESS", "On July 9, 2025, during a routine Corporate Standards Audit it was discovered that the LP gas hose was routed in a way that caused the hose to be against a sharp edge of the furnace."),
  E("July 10, 2025", "FILER_AWARENESS", "On July 10, 2025, Forest River's Office of Corporate Compliance was made aware of the concern and opened a research item."),
  E("July 11, 2025", "DECISION", "On July 11, 2025, Forest River's Corporate Committee voted to recall."),
 ])

# 25V470
L["RCLRPT-25V470-8715.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: BMW AG"),
         S2("SUPPORTED", "On July 9, 2025, in an abundance of caution, BMW decided to conduct a voluntary safety recall.", "chronology", name="BMW")],
 cause=C("NOT_REPORTED", ""),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("May 2023", "INVESTIGATION_START", "In May 2023, a quality review program was initiated regarding the high-voltage battery cell module assembly process."),
  I("INVESTIGATION_START", "An extensive evaluation involving millions of high-voltage battery cell module production records was performed."),
  E("October 2023", "INVESTIGATION_START", "In October 2023, a test program was initiated in order to determine the specific parameters of the assembly process for possible revision, including specific details of those parameters."),
  I("OTHER", "Further reviews of module production records and the assembly process identified potentially affected modules."),
  I("INVESTIGATION_START", "A mathematical model was developed to evaluate the performance of the modules during a vehicle’s lifetime."),
  E("January 2024", "INVESTIGATION_START", "As part of this process, in January 2024, information from field vehicles would start to be collected and analyzed on a continual basis."),
  E("May 2025", "OTHER", "In May 2025, analyses and statistical forecasting indicated that in the latter part of 2026, it could be possible, due to the repeated charging of the high-voltage battery, that damage to the frame of potentially affected modules could occur."),
  I("INVESTIGATION_START", "Further analyses were performed."),
  I("INVESTIGATION_START", "Vehicle assembly information was reviewed to determine the number and production dates of potentially affected vehicles."),
  E("July 9, 2025", "DECISION", "On July 9, 2025, in an abundance of caution, BMW decided to conduct a voluntary safety recall."),
 ])

# 25V487
q_sup487 = "In addition, MBAG, along with the supplier, analyzed possible deviations in the battery production process."
q_aug = "From August 2024, a risk assessment and a detailed temperature simulation were carried out in cooperation with the supplier, which, in early 2025, confirmed that a fire hazard can be ruled out in this context."
L["RCLRPT-25V487-2548.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Farasis Energy (Ganzhou) Co. Ltd."), S2("INSUFFICIENT", q_sup487, "chronology")],
 cause=C("SUPPORTED", "Due to a deviation in the production process at the supplier, the busbar might have been assembled with an unsuitable batch of screws."),
 upstream=U("UNNAMED", q_sup487, "chronology"),
 events=[
  E("2023", "FILER_AWARENESS", "During 2023, MBAG received isolated reports of complaints in the field regarding different allegations (e.g., warning messages)."),
  E("February 2024", "INVESTIGATION_START", "MBAG investigated and evaluated each reported incident to determine the cause and its impact until February 2024."),
  I("INVESTIGATION_START", "Thus, MBAG initiated a task force and carried out several investigations."),
  I("INVESTIGATION_START", "The high-voltage batteries of the reported field complaints were also opened and analyzed in detail."),
  I("INVESTIGATION_START", q_sup487),
  E("August 2024", "INVESTIGATION_START", q_aug),
  E("early 2025", "OTHER", q_aug),
  I("OTHER", "In parallel, MBAG concluded that an unsuitable batch of screws was the root cause of the complaints."),
  E("February 2025", "INVESTIGATION_START", "Starting in February 2025, further failure mechanisms were evaluated, especially regarding the question of whether and how the issue might result in a loss of propulsion."),
  E("April 2025", "INVESTIGATION_START", "In that regard, during April 2025, MBAG analyzed the sequence of events that could lead to driving impairments resulting from unsuitable screws."),
  I("INVESTIGATION_START", "After that, the potentially affected vehicles were identified and narrowed down on the basis of production data from the supplier, showing the screwing torque and angle."),
  E("July 18, 2025", "DECISION", "On July 18, 2025, MBAG determined that a potential safety risk cannot be ruled out and decided to conduct a recall."),
 ])

# 25V507
L["RCLRPT-25V507-9357.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: MITO KOGYO CO.,LTD"), S2("INSUFFICIENT", "Name: MITO KOGYO CO.,LTD", "block")],
 cause=C("SUPPORTED", "Salt water could penetrate and accumulate within the dust cap of the tailgate gas spring, leading to corrosion of the cylinder, which could become significant over time."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("October 2023", "FILER_AWARENESS", "In October 2023, Mitsubishi Motor Sales of Canada, Inc. (MMSCAN) received a Complaint Detail Report from Transport Canada (TC) regarding the rupture of a tailgate gas spring on a 2017 model year Outlander."),
  I("OTHER", "TC also inquired whether MMSCAN was aware of any similar incidents."),
  I("INVESTIGATION_START", "In response, MMSCAN and Mitsubishi Motors Corporation (MMC) initiated an analysis of field reports and warranty claims."),
  E("November 2023", "OTHER", "In November 2023, MMSCAN informed TC that no similar incidents had been reported."),
  E("December 2023", "INVESTIGATION_START", "In December 2023, MMC received the tailgate gas spring that was returned from Canada and initiated its investigation."),
  E("January to April 2024", "INVESTIGATION_START", "From January to April 2024, MMC continued investigating the returned tailgate gas spring, confirming that the cylinder of the tailgate gas spring was severely corroded."),
  I("INVESTIGATION_START", "MMC also conducted a replication test (Salt Spray Test) in an attempt to duplicate the corrosion phenomenon."),
  I("OTHER", "Eventually, MMC was unable to replicate the level of the significant corrosion observed on the returned tailgate gas spring during the test and otherwise to identify the root cause of the corrosion."),
  E("May 2024", "OTHER", "In May 2024, MMSCAN provided TC with the analysis result of the returned tailgate gas spring."),
  I("OTHER", "MMC decided to monitor the issue, as no similar incidents had been reported, and no root cause was identified."),
  E("October 2024", "FILER_AWARENESS", "In October 2024, MMSCAN received a second Complaint Detail Report from TC regarding a tailgate gas spring rupture on a 2018 model year Outlander PHEV."),
  E("November 2024 to January 2025", "INVESTIGATION_START", "From November 2024 to January 2025, MMC initiated an investigation of the returned tailgate gas spring from the second Canadian incident, and confirmed that the cylinder was severely corroded, consistent with the phenomenon observed in the first case."),
  I("OTHER", "MMSCAN provided TC with an interim analysis of the second returned tail gate gas spring."),
  E("February to April 2025", "INVESTIGATION_START", "From February to April 2025, MMC continued to analyze the second tailgate gas spring failure, including a replication test to attempt to identify the root cause of water penetration into the tailgate gas spring."),
  E("May 2025", "OTHER", "In May 2025, MMC confirmed from its analysis, including the replication test, that salt water could penetrate the tailgate gas spring, causing the cylinder to corrode, eventually resulting in rupture at the end of the cylinder upon significant corrosion."),
  E("May 2025", "FILER_AWARENESS", "Also in May 2025, MMC received two additional field reports from Canada potentially involving similar incidents of tailgate gas spring ruptures."),
  I("OTHER", "MMSCAN provided TC with the complete investigation results of the 2nd case, as well as information regarding the two additional Canadian field reports."),
  E("June and July 2025", "FILER_AWARENESS", "Between June and July 2025, MMC received six additional field reports of potentially similar incidents involving tailgate gas spring ruptures from Canada."),
  I("INVESTIGATION_START", "MMC continued analysis of additional field reports."),
  E("July 31, 2025", "DECISION", "On July 31, 2025, MMC determined that a field action was necessary, and advised Mitsubishi Motors North America, Inc. (MMNA) to conduct a safety recall in the Salt Belt region of the United States."),
 ])

# 25V521
L["RCLRPT-25V521-0601.txt"] = dict(
 claims=[S1("NOT_REPORTED", ""), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "In-sufficient vehicle validation of all vehicle variations."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("July 3, 2025", "FILER_AWARENESS", "July 3, 2025 a concern related to vehicle oversteer guidance is brought to the Product Safety organization and an investigation is opened."),
  E("July 21, 2025", "OTHER", "July 21, 2025 Product Safety Evaluation Committee is informed of early results of the investigation and that additional testing is requested."),
  E("July 28, 2025", "OTHER", "July 28, 2025 Product Safety Evaluation Committee meets and reviews investigation results and recommends that the issue be escalated to the Product Safety Committee as a potential product safety defect."),
  E("August 4, 2025", "DECISION", "August 4, 2025 Product Safety Committee is presented findings from the investigation and the recommendations from the Product Safety Evaluation Committee and makes the determination that a product safety defect exists, that a recall will be conducted"),
  E("August 11, 2025", "NHTSA_FILING", "August 11, 2025 DIR filed with NHTSA."),
 ])

# 25V533
L["RCLRPT-25V533-9464.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: MBAG"),
         S2("SUPPORTED", "In mid-July 2025, MBAG initiated investigations following an internal report describing an instance where the driver allegedly experienced noise from the steering system.", "chronology", name="MBAG")],
 cause=C("SUPPORTED", "Due to a production deviation, the bolt that secures the steering coupling might not be torqued to production specifications."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("mid-July 2025", "INVESTIGATION_START", "In mid-July 2025, MBAG initiated investigations following an internal report describing an instance where the driver allegedly experienced noise from the steering system."),
  I("OTHER", "The investigation revealed that the steering coupling bolt was not secured correctly."),
  I("OTHER", "Further investigations identified a gap in the production process, offering the possibility for employees to inadvertently omit vehicles in the steering coupling bolt torquing process."),
  E("early August", "INVESTIGATION_START", "Based on this discovery, potentially affected vehicles were identified, and their workshop histories were evaluated in early August."),
  I("INVESTIGATION_START", "Simultaneously, MBAG began evaluating potential consequences associated with an incorrectly secured steering coupling, and a plant action was initiated to check all vehicles that were still in MBAG’s possession."),
  E("August 13, 2025", "DECISION", "On August 13, 2025, MBAG determined that a potential safety risk cannot be ruled out and decided to conduct a recall."),
 ])

# 25V542
e542 = "July/August-2025 an audit was initiated to validate compliance with 217."
L["RCLRPT-25V542-8411.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Arow Global"), S2("INSUFFICIENT", "Name: Arow Global", "block")],
 cause=C("SUPPORTED", "This was caused by calculation errors when determining the number of egress windows required."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("July/August-2025", "INVESTIGATION_START", e542),
  H("July/August-2025", "FILER_AWARENESS", "During this audit, several calculation anomalies were identified.", e542),
  H("July/August-2025", "INVESTIGATION_START", "This led to a complete, detailed analysis of 217 compliance for all buses.", e542),
  H("July/August-2025", "OTHER", "Once completed, there were apparent inconsistencies with full compliance with 217.", e542),
  E("15-Aug-2025", "DECISION", "These findings were present to the Vehicle Safety Committee on 15-Aug-2025, which concurred a noncompliance recall should be issued."),
 ])

# 25V544
q_pe = "Ford provided responses to PE24-027 on November 18, 2024, and December 10, 2024."
L["RCLRPT-25V544-9834.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: HC QUERETARO SA DE CV"), S2("INSUFFICIENT", "Name: HC QUERETARO SA DE CV", "block")],
 cause=C("INSUFFICIENT", "The root cause of rear brake hose leaks has not been fully determined to date."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("March 18, 2021", "FILER_AWARENESS", "On March 18, 2021, the National Highway Traffic Safety Administration (NHTSA) contacted Ford regarding five Vehicle Owner Questionnaires (VOQs) alleging rear brake jounce hose leaks on 2016- 2017 Edge vehicles."),
  I("OTHER", "At that time, Ford identified 17 warranty claims for leaking rear brake jounce hoses on 2015-2017 Edge vehicles in the U.S., indicating an occurrence rate of 0.03 R/1000."),
  I("OTHER", "Ford continued to monitor field reports for issues relating to this concern as part of routine processes."),
  E("July 8, 2024", "FILER_AWARENESS", "On July 8, 2024, NHTSA contacted Ford regarding 37 VOQs received in the prior 36 months alleging rear brake jounce hose leaks in 2015 – 2017 Edge vehicles."),
  E("July 23, 2024", "INVESTIGATION_START", "On July 23, 2024, Ford’s Critical Concern Review Group (CCRG) opened an investigation into this concern."),
  I("OTHER", "At that time, Ford identified a repair rate of 0.16 R/1000 for rear brake jounce hose leaks and a 10-year/150,000-mile predicted cumulative failure probability of 0.12% on 2015-2018 Edge and 2016-2018 MKX vehicles in the U.S."),
  E("August 27, 2024", "OTHER", "On August 27, 2024, Ford met with NHTSA and shared investigation findings."),
  E("September 10, 2024", "OTHER", "On September 10, 2024, Ford’s CCRG assessed this concern as not an unreasonable risk to motor vehicle safety and closed its investigation based on findings that (1) customers would receive a red brake warning light before experiencing a reduction in rate of deceleration,"),
  E("October 3, 2024", "FILER_AWARENESS", "On October 3, 2024, NHTSA opened a Preliminary Evaluation (PE24-027) to “investigate allegations loss of braking ability in certain model year (MY) 2015-2017 Ford Edge vehicles”."),
  E("November 18, 2024", "OTHER", q_pe),
  E("December 10, 2024", "OTHER", q_pe),
  E("July 23, 2025", "OTHER", "On July 23, 2025, Ford had a meeting with NHTSA in which NHTSA provided a technical briefing on their analysis of material provided in Ford’s PE24-027 response and their concerns about rear brake jounce hoses on the subject vehicles."),
  E("July 29, 2025", "INVESTIGATION_START", "On July 29, 2025, the CCRG reopened their investigation."),
  E("August 15, 2025", "DECISION", "On August 15, 2025, Ford’s Field Review Committee reviewed the concern and approved a field action."),
 ])

# 25V562
L["RCLRPT-25V562-5431.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Altec"),
         S2("SUPPORTED", "Altec began to inspect all parts at production facilities and parts distribution centers to understand variation in crimp diameter.", "chronology", name="Altec")],
 cause=C("NOT_REPORTED", ""),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("July 11, 2025", "FILER_AWARENESS", "On July 11, 2025, a non-conforming crimp was found during production."),
  E("July 15, 2025", "INVESTIGATION_START", "On July 15, 2025, the quality team reviewed the incident report and immediately started a root cause investigation."),
  I("INVESTIGATION_START", "Altec began to inspect all parts at production facilities and parts distribution centers to understand variation in crimp diameter."),
  I("OTHER", "All potentially nonconforming stock was removed."),
  I("OTHER", "During the investigation, it was found that the potential start date for the non-conforming issue was outside the onsite containment, and there was a possibility that units shipped to customers could have a non-conforming crimp."),
  E("July 22, 2025", "INVESTIGATION_START", "On July 22, 2025, a potential field action investigation was opened to evaluate the occurrence, detectability, and identify the affected units."),
  I("INVESTIGATION_START", "Altec began reviewing production records, maintenance logs for the crimping machinery, and parts orders."),
  I("INVESTIGATION_START", "Additionally, Altec tested units in the field and interviewed operators during root cause analysis to identify a population of affected units."),
  E("August 22, 2025", "DECISION", "On August 22, 2025, Altec reviewed the information collected in the investigation and concluded that a potential defect affecting customer units was possible, and the affected population should be notified of the potential defect."),
 ])

# 25V565
q31 = "July 31- The harness manufacture (APC Manufacturing in Mexico) supplier of the harness had provided a generic brand 35-amp fuse, rather than the Bussman fuse specified on the harness drawing."
q4 = "August 4 – The fuse terminals were measured and determined to be thinner than a standard Bussman brand fuse."
q18 = "August 18 – All units in inventory with 8/14/2025 manufacture date or newer were remedied."
L["RCLRPT-25V565-4354.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: APC Manufacturing"), S2("SUPPORTED", q31, "chronology", name="APC Manufacturing")],
 cause=C("SUPPORTED", "The 35-amp macerator fuse supplied with the harness by APC Manufacturing was determined to be a brand fuse not matching the brand specified on the RRG drawing."),
 upstream=U("NAMED", q31, "chronology", names=["APC Manufacturing"]),
 events=[
  E("July 29", "FILER_AWARENESS", "July 29 - A motor home was in the repair shop, and it was reported by a technician that the 35-amp macerator fuse was deformed but the operation of the macerator did not seem to be affected."),
  I("INVESTIGATION_START", "Engineering was consulted to assist in the validation of the overall system operation."),
  I("OTHER", "The manufacturer of the waste macerator was contacted to discuss the situation."),
  E("July 31", "FILER_AWARENESS", q31),
  H("July 31", "OTHER", "Further discussion was to determine the brand of fuse and if they had issues with similar fuses.", q31),
  E("August 1", "SUPPLIER_NOTICE", "August 1 – APC Manufacturing confirmed this fuse was substituted in their harness, but no reports of similar issues."),
  E("August 4", "OTHER", q4),
  H("August 4", "INVESTIGATION_START", "Engineering began an investigation.", q4),
  E("August 6", "OTHER", "August 6 – Testing various fuse brands determined that the terminal thickness on the generic brand fuse was not as tight in the fuse block terminals as name brand fuses (Bussman or Littelfuse brands), causing a subpar connection and additional heat."),
  E("August 7", "FILER_AWARENESS", "August 7- A new development occurred– a REV RV battery control center review of the macerator fuse of earlier built model year units revealed that the installation orientation of the fuse blocks by RRG employees may not match the fuse block diagram key."),
  E("August 14", "OTHER", "August 14 – Update to the investigation: The generic 35-amp fuse provided by APC Manufacturing, installed to protect the macerator circuit can create a subpar connection and create heat, allowing the plastic housing to melt."),
  E("August 18", "OTHER", q18),
  H("August 18", "OTHER", "Results were being complied.", q18),
  E("August 22", "OTHER", "August 22 – The results of the investigation were sent to the internal safety committee for evaluation."),
  E("August 25", "OTHER", "August 25 – Investigation data forwarded to corporate team to review."),
  E("August 29", "DECISION", "August 29 - REV elected to proceed with a voluntary recall."),
 ])

# 25V574
L["RCLRPT-25V574-1873.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Component manufactured by FCA US LLC"),
         S2("SUPPORTED", "On August 28, 2025, FCA US determined, through the Vehicle Regulations Committee, a noncompliance with FVMSS No. 114 exists on all affected vehicles.", "chronology", name="FCA US")],
 cause=C("NOT_REPORTED", ""),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("July 15, 2025", "INVESTIGATION_START", "On July 15, 2025, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization opened an investigation into some 2024 - 2025MY Dodge Charger and Jeep Wagoneer S vehicles that may have been built with a mis-installed PPRS in the EDM."),
  E("July 2025", "INVESTIGATION_START", "During July 2025, FCA US TSRC met with FCA US engineering and manufacturing to review the issue, understand the failure mode, review customer records and determine the suspect population."),
  E("July 23, 2025", "FILER_AWARENESS", "On July 23, 2025, FCA US TSRC organization recognized an issue existed on certain vehicles related to the rollaway prevention, potentially resulting in a noncompliance with FMVSS No.114."),
  E("August 28, 2025", "DECISION", "On August 28, 2025, FCA US determined, through the Vehicle Regulations Committee, a noncompliance with FVMSS No. 114 exists on all affected vehicles."),
 ])

# 25V598
q598 = "Coordination, root cause analysis & testing with manufacturer and supplier"
e598 = "20. Jan 2023: Start of KTM internal investigation."
L["RCLRPT-25V598-1713.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Uno Minda Ltd."), S2("INSUFFICIENT", q598, "chronology")],
 cause=C("SUPPORTED", "Moisture can migrate into the electronic component of the throttle e-throttle and erode the electrical connection."),
 upstream=U("UNNAMED", q598, "chronology"),
 events=[
  E("Q3/Q4 2022", "FILER_AWARENESS", "Q3/Q4 2022: First Single Cases."),
  E("20. Jan 2023", "INVESTIGATION_START", e598),
  H("20. Jan 2023", "INVESTIGATION_START", q598, e598),
  E("01. Jan 2024", "OTHER", "01. Jan 2024: 100% camera base inspection to check PCBA after conformal coating"),
  E("01. Feb 2024", "OTHER", "01. Feb 2024: Automatic Cleaning of circuit board after PCBA & wire terminal soldering"),
  E("18. Sept 2024", "FILER_AWARENESS", "18. Sept 2024: First contact of Transport Canada regarding consumer report to TC"),
  E("25. Sept 2024", "INVESTIGATION_START", "25. Sept 2024: Vehicle inspection of reported vehicle"),
  E("03. Oct 2024", "INVESTIGATION_START", "03. Oct 2024: Transport Canada starts investigation"),
  E("10. Feb 2025", "FILER_AWARENESS", "10. Feb 2025: Transport Canada informs KTM about two additional reports"),
  E("11. Feb 2025", "OTHER", "11. Feb 2025: Transport Canada request warranty claim data."),
  E("13. Feb 2025", "OTHER", "13. Feb 2025: Meeting Transport Canada and KTM NA"),
  E("06. Mar 2025", "OTHER", "06. Mar 2025: Data shared with Transport Canada"),
  E("07. July 2025", "OTHER", "07. July 2025: Meeting request from Transport Canada"),
  E("02. Sept 2025", "OTHER", "02. Sept 2025: Meeting KTM HQ with Transport Canada"),
  E("03. Sept 2025", "DECISION", "03. Sept 2025: KTM HQ determination that a recall is needed"),
  E("05. Sept 2025", "OTHER", "05. Sept 2025: Notice of Defect filed with Transport Canada"),
  E("11. Sept 2025", "NHTSA_FILING", "11. Sept 2025: 573 Report filed with NHTSA"),
 ])

# 25V604
L["RCLRPT-25V604-9558.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Daimler Truck North America"),
         S2("SUPPORTED", "On September 4, 2025 DTNA decided to conduct a safety recall to address affected vehicles.", "chronology", name="DTNA")],
 cause=C("NOT_REPORTED", ""),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("August 14, 2025", "FILER_AWARENESS", "On August 14, 2025, Detroit Diesel Corporation (DDC) received a tie rod through the warranty return process that had been reported to have separated from the front axle."),
  I("INVESTIGATION_START", "An internal inspection by DDC and DTNA suggested that the cotter pin may not have been properly installed based on the presence of grease and debris in the cotter pin hole"),
  I("OTHER", "In the course of further investigation of this issue, it was discovered that the axle had undergone a rework process but did not have proper torque records from after the rework had been performed."),
  I("OTHER", "Other axles were identified that received rework on the tie rod ball joint and did not have records confirming proper torque had been applied during the rework process."),
  E("September 4, 2025", "DECISION", "On September 4, 2025 DTNA decided to conduct a safety recall to address affected vehicles."),
  E("October 16, 2025", "NHTSA_FILING", "On October 16, 2025, DTNA is submitting an amendment to the defect information report to provide remedy for this recall."),
 ])

# 25V640
q640 = "08/29/2025 Supplier informs International that there was an issue with its crank shaft assembly welding process in March 2025 but thought it had contained all suspect parts."
L["RCLRPT-25V640-8730.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: CVG"), S2("INSUFFICIENT", q640, "chronology")],
 cause=C("NOT_REPORTED", ""),
 upstream=U("UNNAMED", q640, "chronology"),
 events=[
  E("08/27/2025", "FILER_AWARENESS", "08/27/2025 Notified by Tulsa Bus plant that 2 buses were found with the left-side wiper not functioning."),
  E("08/29/2025", "OTHER", "08/29/2025 International initiates a delivery stop on school buses at the Tulsa Bus Assembly Plant and establishes the clean point."),
  E("08/29/2025", "SUPPLIER_NOTICE", q640),
  E("March 2025", "OTHER", q640),
  E("09/03/2025", "SUPPLIER_NOTICE", "09/03/2025 Supplier informs International that suspect parts were not quarantined and had been assembled into wiper modules and shipped to the Tulsa Bus Plant."),
  E("09/05/2025", "OTHER", "09/05/2025 Supplier completes review of its manufacturing records and determines that 50 pieces were assembled into 1,638 wiper modules over 24 different build lots ranging from 03/04/2025 thru 04/17/2025."),
  E("09/05/2025-09/17/2025", "OTHER", "09/05/2025-09/17/2025 International completes its inspection of 1,291 buses at the Tulsa Bus Assembly Plant and finds 229 suspect wiper modules ."),
  E("09/15/2025", "OTHER", "09/15/2025 International places a quality hold on all suspect wiper modules at its Parts Distribution Centers"),
  E("09/17/2025", "OTHER", "09/17/2025 International finalizes the suspect population."),
  E("09/18/2025", "DECISION", "09/18/2025 International declares a safety recall."),
 ])

# 25V646
e819 = "08/19/2025 NHTSA advises International that it intends to discuss the above referenced field service report at a forthcoming regularly scheduled meeting with the agency."
e829 = "08/29/2025 Review of internal drawings performed and confirms air line at issue was air dryer discharge line."
L["RCLRPT-25V646-9542.txt"] = dict(
 claims=[S1("NOT_REPORTED", ""), S2("NOT_REPORTED")],
 cause=C("NOT_REPORTED", ""),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("03/14/2025", "FILER_AWARENESS", "03/14/2025 International receives a Field Service Report where a national school bus fleet, “ … reports right side tire rubbing air hose when turning right…”"),
  E("03/17/2025", "INVESTIGATION_START", "03/17/2025 Initial analysis did not indicate a specific trend."),
  E("08/19/2025", "FILER_AWARENESS", e819),
  H("08/19/2025", "INVESTIGATION_START", "International again reviewed the content of the field service report and conducted further assessment of the issue.", e819),
  E("08/26/2025", "FILER_AWARENESS", "08/26/2025 A review of warranty data finds approximately 20 claims ,16 of which had occurred after the initial field service report."),
  E("08/29/2025", "OTHER", e829),
  H("08/29/2025", "OTHER", "International initiates a delivery stop on school buses at the Tulsa Bus Assembly Plant and establishes the clean point.", e829),
  E("08/29/2025-09/17/2025", "OTHER", "08/29/2025-09/17/2025 International completes inspection and repair of 946 buses at the Tulsa Bus Assembly Plant and finds that all units required additional clipping points to properly route the air line."),
  E("09/15/2025", "OTHER", "09/15/2025 International completes its investigation and confirms that clipping points were not included in the assembly drawings and bills of material."),
  E("09/18/2025", "OTHER", "09/18/2025 – International finalizes the suspect population."),
  E("09/19/2025", "DECISION", "09/19/2025 – International declares a safety recall."),
 ])

# 25V649
L["RCLRPT-25V649-8625.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Aptiv"),
         S2("INSUFFICIENT", "Production variances due to quality control at supplier including thinner than nominal wiring gauge.", "cause")],
 cause=C("SUPPORTED", "Production variances due to quality control at supplier including thinner than nominal wiring gauge."),
 upstream=U("NOT_REPORTED", "See attached document titled “2021-2023MY Sorento HVAC Wire Harness Chronology.”", "chronology"),
 events=[])

# 25V651
L["RCLRPT-25V651-2933.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Altec"),
         S2("SUPPORTED", "On September 10, 2025, Altec was notified that a customer experienced a platform detaching from the boom tip of an A-Class unit while the vehicle was in transit.", "chronology", name="Altec")],
 cause=C("NOT_REPORTED", ""),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("September 10, 2025", "FILER_AWARENESS", "On September 10, 2025, Altec was notified that a customer experienced a platform detaching from the boom tip of an A-Class unit while the vehicle was in transit."),
  I("INVESTIGATION_START", "Altec promptly initiated an investigation to determine the root cause, began containment measures, and inspected the affected unit."),
  E("September 16, 2025", "INVESTIGATION_START", "On September 16, 2025, a potential field action investigation was launched to review the results of the investigation."),
  E("September 19, 2025", "DECISION", "On September 19, 2025, Altec concluded that a field action was necessary to address the potential loose platform retaining plate bolts on units in the field."),
 ])

# 25V659
n20 = "November 20, 2024 – NHTSA conducted a New Car Assessment Program (“NCAP”) front barrier crash test involving a model year 2024 Santa Fe vehicle."
m25 = "March 2025 – HMC and NASO continued to review and discuss the NCAP test findings."
a24 = "April 24, 2025 – NASO issued a Field Investigation Request (“FIR”) to survey post-production vehicles for fitment of the starter motor terminal cover."
mj = "May to June 2025 – NASO reviewed HMMA installation standard for the terminal cover."
ja = "July to August 2025 – NASO coordinated additional surveys of port inventory and followed-up with HMMA on their associated assembly processes after NASOs visit."
L["RCLRPT-25V659-2787.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Hyundai Motor Manufacturing Alabama"), S2("SUPPORTED", mj, "chronology", name="HMMA")],
 cause=C("SUPPORTED", "The starter motor’s terminal cover may have been insufficiently installed during vehicle assembly."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("November 20, 2024", "OTHER", n20),
  H("November 20, 2024", "OTHER", "During post-test inspection, smoke was detected from the engine compartment, indicating potential thermal damage.", n20),
  H("November 20, 2024", "FILER_AWARENESS", "NHTSA notified Hyundai Automotive Technical Center, Inc. (“HATCI”) of the test results.", n20),
  H("November 20, 2024", "INVESTIGATION_START", "HATCI and HMC immediately began investigating possible reasons behind the thermal event.", n20),
  E("December 5, 2024", "FILER_AWARENESS", "December 5, 2024 – Hyundai’s North America Safety Office (“NASO”) received a Speak Up for Safety Report (“SUFS”) regarding the prior NCAP test result and thermal incident and began monitoring HATCI/HMC investigation into potential causality."),
  E("January 21, 2025", "INVESTIGATION_START", "January 21, 2025 – HATCI and HMC performed a joint inspection of the test vehicle at the test site, Calspan."),
  E("February 17, 2025", "INVESTIGATION_START", "February 17, 2025 – HMC performed an examination of parts recovered from the test vehicle."),
  E("March 2025", "INVESTIGATION_START", m25),
  H("March 2025", "OTHER", "During an in- person meeting in Korea, HMC reviewed its investigation findings with NASO and indicated a potential shorting condition created with the starter motor and adjacent componentry within the engine compartment.", m25),
  H("March 2025", "INVESTIGATION_START", "An in-house testing plan, mirroring the NCAP test conditions, was developed to test various conditions of the starter motor and contact made with components in the engine compartment.", m25),
  E("April 23, 2025", "OTHER", "April 23, 2025 – HMC shared bench test results that replicated a potential shorting mechanism through contact made between the exposed terminal of the starter motor and the cooling fan motor housing."),
  E("April 24, 2025", "INVESTIGATION_START", a24),
  H("April 24, 2025", "OTHER", "The survey results revealed a number of vehicles exhibited partial or no coverage of the terminal.", a24),
  H("April 24, 2025", "INVESTIGATION_START", "Based on this information, Hyundai began reviewing HMMA manufacturing records pertaining to the terminal cover installation process.", a24),
  E("May to June 2025", "INVESTIGATION_START", mj),
  H("May to June 2025", "INVESTIGATION_START", "NASO conducted an on-site review of the assembly process and observed their current production condition noting no issues with the work standard.", mj),
  E("July to August 2025", "INVESTIGATION_START", ja),
  H("July to August 2025", "INVESTIGATION_START", "HMC performed durability tests through various engine operations and road surface conditions to determine if the cover could become unseated over time.", ja),
  H("July to August 2025", "OTHER", "The test results revealed that a correctly installed terminal cover will remain in place.", ja),
  E("September 10, 2025", "OTHER", "September 10, 2025 – HMC provided confirmation that when the vehicle's starter motor terminal cover was installed correctly, a short circuit condition did not occur during testing."),
  E("September 25, 2025", "DECISION", "September 25, 2025, based on a final review of NASO's investigation findings to date, NASO convened its North America Safety Decision Authority (“NASDA”) and decided to conduct a safety recall of potentially affected U.S. market vehicles."),
 ])

# 25V663
q663 = "Altec informed the engine manufacturer, who investigated the incident and determined that the cause of the fire on the auxiliary engine remained inconclusive."
L["RCLRPT-25V663-9975.txt"] = dict(
 claims=[S1("SUPPORTED", "Name: Altec"),
         S2("SUPPORTED", "In October 2024, Altec was notified that an ST600 spray vehicle had caught fire while unattended and the fire had self-extinguished.", "chronology", name="Altec")],
 cause=C("NOT_REPORTED", ""),
 upstream=U("UNNAMED", q663, "chronology"),
 events=[
  E("October 2024", "FILER_AWARENESS", "In October 2024, Altec was notified that an ST600 spray vehicle had caught fire while unattended and the fire had self-extinguished."),
  I("INVESTIGATION_START", "Altec investigated the issue and found the electrical components of the auxiliary engine had been involved in the incident."),
  I("OTHER", q663),
  E("July 2025", "FILER_AWARENESS", "In July 2025, Altec was notified of two additional incidents similar to the one that occurred in October 2024."),
  I("FILER_AWARENESS", "The customer also provided a video from one of the incidents showing electrical arcing in the voltage regulator."),
  E("July", "INVESTIGATION_START", "Following the reports of the incidents in July, Altec initiated a root cause investigation to determine the cause of the auxiliary engine electrical component failures."),
  E("September 15, 2025", "FILER_AWARENESS", "On September 15, 2025, an additional incident was reported of a thermal event on an unattended vehicle that had self-extinguished."),
  E("September 23, 2025", "INVESTIGATION_START", "On September 23, 2025, a potential field action issue was opened to investigate the possibility of a safety- related issue and determine if it could affect additional units in the field."),
  E("September 26, 2025", "DECISION", "On September 26, 2025, after reviewing the reported incidents and the investigation results, Altec determined that a potential defect existed in vehicles in the possession of owners, and a recall should be issued to remedy the potential risk."),
 ])

# ---- build + verify ----
out, errs = [], []
files = sorted(f for f in os.listdir(T) if f.startswith("RCLRPT-") and f.endswith(".txt"))
for fn in files:
    fileline, sec = sections(os.path.join(T, fn))
    lab = L[fn]
    obj = {"file": fileline, "claims": lab["claims"], "cause": lab["cause"], "upstream": lab["upstream"], "events": lab["events"]}
    def chk(q, s, what):
        if not q:
            return
        if len(q) > 300:
            errs.append(f"{fn} {what}: too long {len(q)}")
        if norm(q) not in sec.get(s, ""):
            errs.append(f"{fn} {what}: quote not found in {s}: {q[:80]}")
    for c in obj["claims"]:
        chk(c["quote"], c["section"], c["id"])
    chk(obj["cause"]["quote"], obj["cause"]["section"], "cause")
    chk(obj["upstream"]["quote"], obj["upstream"]["section"], "upstream")
    last = -1
    for i, e in enumerate(obj["events"]):
        chk(e["quote"], "chronology", f"event{i}")
        if e.get("entry_quote"):
            chk(e["entry_quote"], "chronology", f"entry{i}")
            if e["date_text"] not in e["entry_quote"]:
                errs.append(f"{fn} entry{i}: date not in entry")
        elif e["date_text"] and e["date_text"] not in e["quote"]:
            errs.append(f"{fn} event{i}: date not in quote")
    out.append(obj)

if errs:
    print("\n".join(errs)); sys.exit(1)
with open(os.path.join(D, "passB.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written", len(out), "events", sum(len(o["events"]) for o in out))
