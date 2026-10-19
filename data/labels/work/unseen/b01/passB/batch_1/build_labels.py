import json, re, os, sys
D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")
def norm(s): return re.sub(r"\s+", " ", s).strip()
def sections(fn):
    txt = open(os.path.join(T, fn), encoding="utf-8").read()
    file_line = re.search(r"^FILE: (.+)$", txt, re.M).group(1).strip()
    blk = txt.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    cause = txt.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    chron = txt.split("=== CHRONOLOGY ===")[1]
    return file_line, {"block": norm(blk), "cause": norm(cause), "chronology": norm(chron)}

def C(st, q="", sec=""): return {"status": st, "quote": q, "section": sec}
def E(d, t, q, inh=None, inf=False):
    e = {"date_text": d, "type": t, "quote": q, "inherited_date": bool(inh), "date_inferred": inf}
    if inh: e["entry_quote"] = inh
    return e
def I(t, q): return E("", t, q, inf=True)

L = {}
# 1
L["RCLRPT-23E020-3987.txt"] = dict(
 s1=C("NOT_REPORTED","Name : NR","block"), s2=C("NOT_REPORTED"), s2name=None,
 cause=C("NOT_REPORTED","NR","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[E("December, 2021","FILER_AWARENESS","Following reporting of an overheating incident in December, 2021, Orpak undertook to conduct internal and independent testing of the DataPass Plus devices up through May, 2022."),
     E("May, 2022","INVESTIGATION_START","Following reporting of an overheating incident in December, 2021, Orpak undertook to conduct internal and independent testing of the DataPass Plus devices up through May, 2022."),
     I("OTHER","Based on the testing conducted, Orpak was unable to replicate the defect reported in the overheating incident, but Orpak identified a potential anomaly in the de-paneling process used to manufacture certain units that could cause capacitor cracking."),
     E("early 2023","DECISION","In early 2023, two more overheating incidents were reported and Orpak determined to undertake a recall, while continuing to investigate any potential defect.")])
# 2
e1="12/12/2022 - RCM / 8D # CC23-0034 was opened for improper keeper installation on front axles by Laurinburg."
L["RCLRPT-23E031-5488.txt"] = dict(
 s1=C("NOT_REPORTED","Name : NR","block"), s2=C("NOT_REPORTED"), s2name=None,
 cause=C("SUPPORTED","Installing the keepers on the pro-torque nut is a manual process and the standard operating procedure was not followed by the operator.","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[E("12/12/2022","FILER_AWARENESS","12/12/2022 – Notified by customer that it was observed that the orange keeper was not installed correctly from the Meritor factory on some of the ProTorq® spindle nuts."),
     E("12/12/2022","INVESTIGATION_START",e1),
     E("12/12/2022","OTHER","Front axle quality technicians were assigned to validate engagement of keepers and capture pictures of keeper installation and on all ProTorq® spindle nuts built on the front axle line.", e1),
     E("12/21/2022","INVESTIGATION_START","12/21/2022 – Engineering began working on analysis involving improper keeper installation reported by customer."),
     E("1/11/2023","OTHER","1/11/2023 – Engineering provide summary of investigation to product safety and compliance counsel and continued investigation."),
     E("2/6/2023","DECISION","2/6/2023 – Meritor Product Safety and Compliance Committee reviewed engineering technical position conclusion and determined a possible safety related concern has been identified and impacted customers should be notified."),
     E("3/23/2023","OTHER","3/23/2023 – Meritor notified that Spartan Fire filed a 573 Defect Report with NHTSA."),
     E("3/31/2023","OTHER","3/31/2023 – Meritor notified that Capacity of Texas filed a 573 Defect Report with NHTSA.")])
# 3
L["RCLRPT-23E033-7392.txt"] = dict(
 s1=C("SUPPORTED","Name : 3M Company","block"),
 s2=C("SUPPORTED","As part of its normal quality control procedures, 3M tested a sample of sheeting from the lot in question during December 2022.","chronology"), s2name="3M",
 cause=C("NOT_REPORTED","NR","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[E("December 2022","INVESTIGATION_START","As part of its normal quality control procedures, 3M tested a sample of sheeting from the lot in question during December 2022."),
     I("FILER_AWARENESS","The third-party lab contacted 3M by email and informed 3M that this sheeting did not pass the retroreflection requirement.")])
# 4
s4="Between October 2023 and December of 2023, Hyundam continued to inspect and evaluate fuel pumps recovered by Hyundai and Mercedes-Benz."
q4u="Additional investigation continued into early 2024, which resulted in additional raw material lots of the sub- supplier identified as being potentially affected by the subject condition."
L["RCLRPT-23E068-9689.txt"] = dict(
 s1=C("SUPPORTED","Name : Hyundam Industrial","block"),
 s2=C("SUPPORTED","On September 18, 2023, Hyundam submitted Recall Report 23E-068.","chronology"), s2name="Hyundam",
 cause=C("SUPPORTED","The fuel pump impellers produced from certain lots between January 2021 and February 2022 were made of certain raw materials which were at lower levels than the raw materials used in other lots","cause"),
 up=("UNNAMED",[], q4u, "chronology"),
 ev=[E("September 18, 2023","NHTSA_FILING","On September 18, 2023, Hyundam submitted Recall Report 23E-068."),
     E("October 10, 2023","NHTSA_FILING","Hyundam amended its Recall Report on October 10, 2023 to specify the estimated percentage of products with defect."),
     E("October 2023","INVESTIGATION_START",s4),
     E("December of 2023","INVESTIGATION_START",s4),
     E("early 2024","INVESTIGATION_START",q4u),
     I("INVESTIGATION_START","Hyundam continued to work with Hyundai and Mercedes-Benz to monitor and evaluate fuel pumps containing product from the additional raw material lots of the sub-supplier."),
     I("DECISION","Hyundam decided to amend its recall to address the additional products potentially affected by the subject condition.")])
# 5
L["RCLRPT-23E072-1814.txt"] = dict(
 s1=C("SUPPORTED","Name : Precision Circuits","block"),
 s2=C("SUPPORTED","Precision Circuits was contacted immediately and advised of the error.","chronology"), s2name="Precision Circuits",
 cause=C("SUPPORTED","Precision Circuits utilized/installed the incorrect wire gauge in its Power Control System for the 50 amp service application required by Brinkley Model G.","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[E("Thursday, September 21, 2023","FILER_AWARENESS","On Thursday, September 21, 2023, during an electrical audit performed at Brinkley RV, it was discovered that the neutral wire for the Power Control System was undersized for a 50 Amp service system."),
     I("OTHER","The neutral wire was discovered to be 10 gauge during the audit."),
     I("FILER_AWARENESS","Precision Circuits was contacted immediately and advised of the error."),
     E("September 22, 2023","INVESTIGATION_START","Thereafter, Precision Circuits traveled to Brinkley RV on September 22, 2023 to review the application and to confirm that the wire in fact was undersized."),
     I("OTHER","Immediate corrective action was taken at the Precision Circuits production facility to ensure no other components were built with the undersized wiring."),
     I("OTHER","All Brinkley RV Model G units located on Brinkley RV premises were subjected to a stop ship to permit all units to be remedied prior to shipment."),
     I("INVESTIGATION_START","In parallel, Precision Circuits also performed lab testing to evaluate the risk related to amperage draw and temperature and found that the wire was at no risk of component failure or fire hazard when continuously subjected to 50Amps of power."),
     I("DECISION","Despite this determination by Precision Circuits, Brinkley RV and Precision Circuits both still agreed that changing to the 6 gauge neutral wire is necessary and should be performed to be in compliance with applicable code.")])
# 6
L["RCLRPT-23E073-6451.txt"] = dict(
 s1=C("NOT_REPORTED","Name : NR","block"), s2=C("NOT_REPORTED"), s2name=None,
 cause=C("INSUFFICIENT","HL Mando’s investigation is continuing and HL Mando has not determined the presence of a defect in the HECU/ABS modules.","cause"),
 up=("NOT_REPORTED",[], "", ""), ev=[])
# 7
L["RCLRPT-23E082-7103.txt"] = dict(
 s1=C("SUPPORTED","Name : Trans-Air Manufacturing","block"),
 s2=C("INSUFFICIENT","Name : Trans-Air Manufacturing","block"), s2name=None,
 cause=C("SUPPORTED","The mounts allow the compressors to hang too low and may contact the vehicles optional front stabilizer bar.","cause"),
 up=("NAMED",["Ford"],"After a lot of research it was determined that the models that Ford sent us did not have stabilizer bar.","chronology"),
 ev=[E("August of 2022","FILER_AWARENESS","In August of 2022 we received a report of a non delivered vehicle with (13cid) compressors hitting stabilizer bar."),
     I("OTHER","After a lot of research it was determined that the models that Ford sent us did not have stabilizer bar."),
     I("OTHER","We prototyped numerous mounts until we developed one that was acceptable to our quality and engineering departments."),
     E("October of 2023","FILER_AWARENESS","We were under the impression that there were no other issues, until we received a report of a failure in October of 2023 on a bus with 10cid compressors."),
     I("OTHER","At that point we reached out to Starcraft for their assistance with gaining dealer information for the 36 VINs")])
# 8
L["RCLRPT-23E086-7725.txt"] = dict(
 s1=C("SUPPORTED","Name : Cruise LLC","block"),
 s2=C("SUPPORTED","Cruise immediately began an investigation of the incident.","chronology"), s2name="Cruise",
 cause=C("NOT_REPORTED","NR","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[E("October 2, 2023","FILER_AWARENESS","On October 2, 2023, a Cruise AV, operating in driverless mode, was involved in a collision in which a human- driven vehicle collided with a pedestrian and propelled the pedestrian into the immediate path of the Cruise AV."),
     I("OTHER","After coming to an initial stop, the AV attempted to pull over out of traffic, pulling the individual forward."),
     I("INVESTIGATION_START","Cruise immediately began an investigation of the incident."),
     E("October 3, 2023","OTHER","On October 3, 2023, Cruise met with the California Department of Motor Vehicles (“DMV”), National Highway Traffic Safety Administration (“NHTSA”), and other San Francisco officials to discuss the incident"),
     I("OTHER","Cruise also reported the incident to NHTSA that same day, in accordance with NHTSA’s Standing General Order."),
     I("OTHER","In the course of its investigation of the incident, Cruise determined that the ADS attempted to pull over after the collision, rather than remain stationary, as a result of the issue described in this notice."),
     I("INVESTIGATION_START","Cruise continued its evaluation of the AV’s post-collision response to ascertain whether and under what circumstances the issue could recur by conducting a broad review of historical driving data"),
     E("October 23, 2023","INVESTIGATION_START","On October 23, 2023, Cruise completed its review and immediately initiated an assessment of the safety risk associated with the findings.")])
# 9
L["RCLRPT-23V008-6503.txt"] = dict(
 s1=C("SUPPORTED","Name : Gratimax, LLC dba McElrath Trailers","block"),
 s2=C("SUPPORTED","On December 8, 2022, Gratimax was notified by its customer, Vermeer MV Solutions, Inc., of a possible compliance issue relating to the design of the affected trailers.","chronology"), s2name="Gratimax",
 cause=C("SUPPORTED","The cause is due to the original design by Vermeer MV Solutions, Inc. which is the customer of McElrath Trailers.","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[E("December 8, 2022","FILER_AWARENESS","On December 8, 2022, Gratimax was notified by its customer, Vermeer MV Solutions, Inc., of a possible compliance issue relating to the design of the affected trailers."),
     I("INVESTIGATION_START","An investigation of the design was opened at that time, including review of applicable regulations, standards, manufacturing documents, and design files, and production of the affected trailers was placed on hold."),
     E("January 4, 2023","DECISION","On January 4, 2023, Gratimax decided that a non- compliance with FMVSS 108 and 224 existed.")])
# 10
L["RCLRPT-23V009-5168.txt"] = dict(
 s1=C("NOT_REPORTED","Name : NR","block"), s2=C("NOT_REPORTED"), s2name=None,
 cause=C("SUPPORTED","During a recent quality system audit it was noted that a detailed installation drawing, complete with weld symbols, was not provided to production personnel for this winch installation.","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[I("FILER_AWARENESS","During a recent quality system audit it was noted that a detailed installation drawing, complete with weld symbols, was not provided to production personnel for this winch installation.")])
# 11
L["RCLRPT-23V035-6346.txt"] = dict(
 s1=C("SUPPORTED","Name : Adient","block"), s2=C("INSUFFICIENT","Name : Adient","block"), s2name=None,
 cause=C("SUPPORTED","Incorrect length of second row seat side airbag wire harness allows contact to seat frame when seat is folded/adjusted.","cause"),
 up=("NOT_REPORTED",[], "", ""), ev=[])
# 12
q12="BRP found that there was a high probability that the issue was due to a wrong plastic injection control for the mirror housings by its supplier for a batch molded in April 2022."
L["RCLRPT-23V053-3046.txt"] = dict(
 s1=C("SUPPORTED","Name : Zadi","block"), s2=C("INSUFFICIENT",q12,"chronology"), s2name=None,
 cause=C("SUPPORTED",q12,"cause"),
 up=("UNNAMED",[], q12, "chronology"),
 ev=[E("end of November 2022","FILER_AWARENESS","At the end of November 2022, BRP confirmed a trend of high warranty rates of mirror falling from the housing."),
     I("FILER_AWARENESS","While most of the mirrors were found in the bottom of the crate at dealership, BRP received reports of mirrors falling while riding representing 9% of the overall claims."),
     I("INVESTIGATION_START","In trying to understand the trend, BRP made various tests and validations."),
     I("OTHER",q12),
     E("January 27, 2023","DECISION","With all the information collected and analyzed, BRP decided on January 27, 2023 had enough information to report and wants to proceed with a safety recall."),
     E("Week of April 3","FILER_AWARENESS","Update 4:MY23:Week of April 3:BRP found one lens dislodged from the mirror housing in a box of 96 parts for MY2023."),
     I("OTHER","Inspection of the 96 parts identified inadequate molding dates as required by BRP and agreed by the supplier."),
     I("OTHER","Then, BRP inspected of 621 vehicles in its production yard and found 140 vehicles with mirror housing(s) from an inadequate molding date."),
     E("May 3","DECISION","With all the information collected and analyzed, BRP decided on May 3, it had enough information to report and recall.")])
# 13
j15="January 15, 2023: A new team comprised of engineering and quality dedicated personnel overseeing issues was installed and a status review of issues was conducted during the first two weeks of January 2023."
o22="October 2022: An internal meeting was held to review this issue."
f8="February 8, 2023: An internal meeting was held with the engineering, operations, and quality dedicated team to further review this issue."
L["RCLRPT-23V095-6996.txt"] = dict(
 s1=C("SUPPORTED","Name : CHONGQING ZONGSHEN AUTOMOBILE INDUSTRY C","block"),
 s2=C("INSUFFICIENT","Name : CHONGQING ZONGSHEN AUTOMOBILE INDUSTRY C","block"), s2name=None,
 cause=C("NOT_REPORTED","NR","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[E("August 2022","FILER_AWARENESS","August 2022: ElectraMeccanica received complaints related to loss of propulsion."),
     E("September 2022","FILER_AWARENESS","September 2022: Additional complaints were received."),
     E("October 2022","OTHER",o22),
     E("October 2022","INVESTIGATION_START","Engineering team instructed to conduct further investigation.",o22),
     E("January 15, 2023","OTHER",j15),
     E("first two weeks of January 2023","OTHER",j15),
     E("January 30, 2023","OTHER","January 30, 2023: The engineering and quality dedicated team gathered again, and updated data and information related to the propulsion issue."),
     E("February 8, 2023","OTHER",f8),
     E("February 8, 2023","OTHER","Decision: escalate to executive team.",f8),
     E("February 9, 2023","DECISION","February 9, 2023: An internal meeting was held with executives, and it was determined to conduct a voluntary recall of the affected vehicles.")])
# 14
n1="2/23/2023 NEWELL COACH NOTICED A COACH'S TAILIGHTS NOT DISPLAYING WHILE SLOWING DOWN ONTHE PROPERTY."
L["RCLRPT-23V147-7099.txt"] = dict(
 s1=C("NOT_REPORTED","Name : NR","block"), s2=C("NOT_REPORTED"), s2name=None,
 cause=C("SUPPORTED","INCORRECT ASSEMBLY DURING MANUFACTURING","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[E("2/23/2023","FILER_AWARENESS",n1),
     E("2/23/2023","INVESTIGATION_START","NEWELL IMMEDIATELY CONDUCTED A QUALITY REVIEW AND DETERMINDED THE INSTALLATION OF AN ADDITIONAL BRAKE SWITCH TO ACCOMODATE A REQUIRED BRAKE SIGNAL FOR THE PUSH BUTTON START IGINTION WAS MISS WIRED, INADVERTENTLY BYPASSING THE ORIGNIAL BRAKE SWITCH",n1)])
# 15
t1="Mar. 2, 2023 - Terex Advance Mixer and Meritor had a conference call where Meritor shared that 20 axles that where shipped to Terex Advance Mixer had a defect."
t2="Mar. 7,2023 - After internal discussions and analysis of the Meritor information, Terex Advance Mixer deemed this condition to be safety related."
L["RCLRPT-23V148-5089.txt"] = dict(
 s1=C("SUPPORTED","Name : Meritor, Inc","block"), s2=C("SUPPORTED",t1,"chronology"), s2name="Meritor",
 cause=C("NOT_REPORTED","NR","cause"),
 up=("NAMED",["Meritor"],t1,"chronology"),
 ev=[E("Mar. 2, 2023","SUPPLIER_NOTICE",t1), E("Mar. 7,2023","DECISION",t2),
     E("Mar. 7,2023","NHTSA_FILING","Therefore, a 573 defect report was initiated.",t2)])
# 16
k2="Lippert informed Renegade RV and Rev Recreation Group on 2/23/2023 of their decision to file equipment recall 23E-008 with NHTSA."
L["RCLRPT-23V161-6181.txt"] = dict(
 s1=C("SUPPORTED","Name : Lippert","block"), s2=C("SUPPORTED",k2,"chronology"), s2name="Lippert",
 cause=C("INSUFFICIENT","Defective part.","cause"),
 up=("NAMED",["Lippert"],k2,"chronology"),
 ev=[I("OTHER","Lippert determined an issue which relates to motor vehicle safety may exist in certain entry doors for motorized RV product built with Global Link Motorized Rotary Latch MRL-41210-2006."),
     E("2/23/2023","SUPPLIER_NOTICE",k2),
     I("INVESTIGATION_START","Renegade and REV Recreation Group began an investigation into the units affected and compiled a list of potentially affected vehicles.")])
# 17
c1="On March 2, 2023 – REV Group received communication from Meritor of a potential issue with their pro-torque nut keeper installation."
L["RCLRPT-23V219-8343.txt"] = dict(
 s1=C("SUPPORTED","Name : Meritor","block"), s2=C("SUPPORTED",c1,"chronology"), s2name="Meritor",
 cause=C("SUPPORTED","Installing the keepers on the pro-torque nut is a manual process and standard procedure was not followed at Meritor.","cause"),
 up=("NAMED",["Meritor"],c1,"chronology"),
 ev=[E("March 2, 2023","SUPPLIER_NOTICE",c1),
     E("March 2 – 15, 2023","OTHER","March 2 – 15, 2023 – REV Group relayed this information to Spartan Fire and confirmed with Meritor that Spartan was the only business unit affected."),
     E("March 15, 2023","INVESTIGATION_START","On March 15, 2023 - A Defect Investigation Report was generated and escalated to REV Group Management."),
     E("March 21, 2023","DECISION","March 21, 2023 – REV Group Recall Committee approved a voluntary recall for this issue."),
     E("March 24, 2023","SUPPLIER_NOTICE","On March 24, 2023 - Meritor notified REV Group that Capacity of Texas was also affected."),
     E("March 24, 2023","INVESTIGATION_START","On March 24, 2023 - Capacity of Texas started an investigation to gather pertinent information to file its own recall.")])
# 18
p31="2023-03-31 Case was presented on Volvo PSWG."
p03="2023-03-03 Case was presented to Volvo PSC."
L["RCLRPT-23V245-8278.txt"] = dict(
 s1=C("NOT_REPORTED","Name : NR","block"), s2=C("NOT_REPORTED"), s2name=None,
 cause=C("SUPPORTED","During the vehicle manufacturing, Prevost assembly line workers installed unsuitable grommets on certain vehicles (production issue).","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[E("2023-03-28","FILER_AWARENESS","2023-03-28 Issue identified in production during the final verification at the end of the assembly line."),
     E("2023-03-28","INVESTIGATION_START","2023-03-28 Internal Prevost investigation was opened to identify the root cause and to determine if vehicles were delivered with this issue."),
     E("2023-03-30","OTHER","2023-03-30 Delivery Stop was issued to stop the delivery of new vehicles until the investigation is completed and corrective actions are implemented."),
     E("2023-03-31","OTHER",p31),
     E("2023-03-31","OTHER","Decision made to raise the potential safety issue to Volvo Product Safety Committee (PSC) for review and determination.",p31),
     E("2023-03-31","OTHER","2023-03-31 Internal campaign was launched to solve the issue on all vehicles in production before being delivered."),
     E("2023-03-03","OTHER",p03),
     E("2023-03-03","DECISION","It was concluded that there was a safety related defect and that a recall is needed.",p03),
     E("2023-04-06","NHTSA_FILING","2023-04-06 Safety Recall report submitted to authorities.")])
# 19
L["RCLRPT-23V329-1334.txt"] = dict(
 s1=C("SUPPORTED","Name : T.ERRE Srl","block"), s2=C("INSUFFICIENT","Name : T.ERRE Srl","block"), s2name=None,
 cause=C("SUPPORTED","Unintended contact between the fuel tank connecting pipe and the high-voltage battery protection cover allowed the formation of corrosion on the pipe due to a chemical reaction between aluminum and inox steel","cause"),
 up=("NOT_REPORTED",[], "", ""), ev=[])
# 20
L["RCLRPT-23V448-5435.txt"] = dict(
 s1=C("NOT_REPORTED","Name : NR","block"), s2=C("NOT_REPORTED"), s2name=None,
 cause=C("NOT_REPORTED","NR","cause"),
 up=("NONE_MENTIONED",[], "", ""),
 ev=[E("December 2022","INVESTIGATION_START","December 2022: Opening of an investigation following several cases of cracks and damaged HV harnesses detected in service."),
     E("June 2023","FILER_AWARENESS","June 2023: New cases of in-service vehicles with cracks in the firewall leading to damage to the cables running under the tank were reported."),
     E("June 22, 2023","DECISION","June 22, 2023: Confirmation that the firewall cracks represent a defect regarding the Motor Vehicle Safety Regulations and approval of the recall proposal by Lion Electric's Safety Committee.")])
# 21
v27="2023-01-27 Internal Prevost investigation was opened to identify the root cause and to determine if the issue is potentially safety related."
wc="The warranty claims were received on 2022-03-30, 2022-07-21, 2022-12-21, 2022-12-21, and on 2023-02-14."
v13="2023-06-13 Prevost’s Safety Office reviewed the preliminary results of the survey completed by the seat supplier."
v627="2023-06-27 Case was presented on Volvo Product Safety Evaluation Committee (PSEC) to evaluate if there is a potential safety related issue."
v706="2023-07-06 Case was presented to Volvo Product Safety Committee (PSC)."
v227="2023-02-27 Prevost requested the seat supplier to perform a survey on potentially affected vehicles to support the ongoing investigation."
L["RCLRPT-23V475-7264.txt"] = dict(
 s1=C("SUPPORTED","Name : United Safety & Survivability Corp.","block"), s2=C("INSUFFICIENT",v227,"chronology"), s2name=None,
 cause=C("SUPPORTED","The defect results from a supplier quality issue (inadequate bolt torquing during seat assembly from supplier).","cause"),
 up=("UNNAMED",[], v227, "chronology"),
 ev=[E("2023-01-26","FILER_AWARENESS","2023-01-26 One field report involving two MY2021 Prevost X3-45 vehicles was received."),
     E("2023-01-27","INVESTIGATION_START",v27),
     E("2023-01-27","INVESTIGATION_START","As part of the investigation, warranty data was analyzed and five warranty claims potentially related to this issue were identified, all on MY2021 Prevost X3-45 Commuter.",v27),
     E("2022-03-30","FILER_AWARENESS",wc), E("2022-07-21","FILER_AWARENESS",wc),
     E("2022-12-21","FILER_AWARENESS",wc), E("2023-02-14","FILER_AWARENESS",wc),
     E("2023-02-27","INVESTIGATION_START",v227),
     E("2023-06-13","OTHER",v13),
     E("2023-06-13","SUPPLIER_NOTICE","According to the supplier, approximately 63% of the inspected vehicles had at least one loose or disengaged seat recline mechanism bolt.",v13),
     E("2023-06-27","OTHER",v627),
     E("2023-06-27","OTHER","Decision made to raise the potential safety issue to Volvo Product Safety Committee (PSC) for review and determination.",v627),
     E("2023-07-06","OTHER",v706),
     E("2023-07-06","DECISION","It was concluded that there was a safety related issue and that a recall is needed.",v706),
     E("2023-07-11","NHTSA_FILING","2023-07-11 Defect Information Report submitted to authorities."),
     E("2023-08-17","NHTSA_FILING","2023-08-17: Added Prevost's identification code for this recall.")])
# 22
q22="The hose assembly manufacturer sourced fittings from a different tier-2 supplier and they were improper."
n605="2023-06-05: 2 additional power steering hose failures are reported from the same customer."
n629="2023-06-29: Analysis of the new information vs the 23V054 Safety Recall about power steering hose separation is completed."
L["RCLRPT-23V481-6313.txt"] = dict(
 s1=C("SUPPORTED","Name : Connectall Ltd","block"), s2=C("INSUFFICIENT",q22,"cause"), s2name=None,
 cause=C("SUPPORTED",q22,"cause"),
 up=("UNNAMED",[], q22, "cause"),
 ev=[E("2023-04-13","FILER_AWARENESS","2023-04-13: A power steering hose failure is reported from a customer to Nova Bus."),
     E("2023-06-05","FILER_AWARENESS",n605),
     E("2023-06-05","OTHER","A field report is created.",n605),
     E("2023-06-15","INVESTIGATION_START","2023-06-15: Nova Bus Product Safety Working Group is informed, investigation opened."),
     E("2023-06-29","OTHER",n629),
     E("2023-06-29","OTHER","Nova Bus Product Safety Working Group decides to raise this new situation to the Nova Bus Product Safety Committee.",n629),
     E("2023-07-05","DECISION","2023-07-05: Nova Bus Product Safety Committee determines a Safety-Related Defect exits."),
     E("2023-07-12","OTHER","2023-07-12: The affected vehicle population in service and at the plants is confirmed."),
     E("2023-07-12","NHTSA_FILING","2023-07-12: Nova Bus submits a vehicle recall report to NHTSA.")])
# 23
pw1="Pleasure-Way Industries Ltd was officially notified by Cummins of recall 23E-030 April 13, 2023."
pw2="January 18 - 22, 2023 Cummins had indication that there had been fuel line failures out in the field these where brought to their attention during the Tampa RV Super show."
L["RCLRPT-23V493-9698.txt"] = dict(
 s1=C("SUPPORTED","Name : Cummins Inc.","block"), s2=C("SUPPORTED",pw1,"chronology"), s2name="Cummins",
 cause=C("SUPPORTED","Per Recall 23E030; \"The cause of the issue is an inadequate specification of fuel hose.\"","cause"),
 up=("NAMED",["Cummins"],pw1,"chronology"),
 ev=[E("April 13, 2023","SUPPLIER_NOTICE",pw1),
     E("January 18 - 22, 2023","OTHER",pw2),
     E("January 23 - Feb 10, 2023","OTHER","Pleasure-Way had also notified Cummins of generators with fuel leaks January 23 - Feb 10, 2023."),
     E("January 18 - 22, 2023","OTHER","Pleasure-Way removed these generators from the vehicles and sent them back to Cummins for analysis.",pw2),
     E("March 28, 2023","OTHER","Cummins conducted a review and testing of the product and concluded on March 28, 2023 that a defect existed."),
     E("April 6, 2023","SUPPLIER_NOTICE","April 6, 2023 Cummins sent a list of QG2800i generator serial numbers that had been supplied to Pleasure- Way."),
     E("April 13, 2023","OTHER","April 13, 2023 the official recall was launched by Cummins.")])
# 24
sh="SAF Holland notified us of the issue with Tire Pilot Plus(TPP) officially on 7/10/2023."
L["RCLRPT-23V497-8020.txt"] = dict(
 s1=C("SUPPORTED","Name : SAF Holland","block"), s2=C("SUPPORTED",sh,"chronology"), s2name="SAF Holland",
 cause=C("SUPPORTED","Electronic Controller can open the check valves in the tire inflation hoses causing the tires to lose air pressure and deflate.","cause"),
 up=("NAMED",["SAF Holland"],sh,"chronology"),
 ev=[E("7/10/2023","SUPPLIER_NOTICE",sh)])
# 25
cu="Cummins informed us of recall on April 13 2023."
L["RCLRPT-23V498-4108.txt"] = dict(
 s1=C("SUPPORTED","Name : Cummins Inc","block"), s2=C("SUPPORTED",cu,"chronology"), s2name="Cummins",
 cause=C("SUPPORTED","inadequate specification of fuel hose","cause"),
 up=("NAMED",["Cummins"],cu,"chronology"),
 ev=[E("April 13 2023","SUPPLIER_NOTICE",cu),
     I("OTHER","They received reports of fuel leaks on the Onan generators 2800")])

out=[]; errs=[]
files = sorted(f for f in os.listdir(T) if f.endswith(".txt") and not f.startswith("._"))
assert set(files)==set(L), set(files)^set(L)
def chk(fn, secs, q, sec, what):
    if q=="": return
    if len(q)>300: errs.append((fn,what,"len",len(q)))
    if norm(q) not in secs[sec]: errs.append((fn,what,q[:80]))
for fn in files:
    fl, secs = sections(fn); d=L[fn]
    s1=dict(id="S1", **d["s1"]); s2={"id":"S2","status":d["s2"]["status"]}
    if d["s2name"]: s2["name"]=d["s2name"]
    s2.update(quote=d["s2"]["quote"], section=d["s2"]["section"])
    k,names,uq,us=d["up"]
    up={"kind":k,"names":names,"quote":uq,"section":us}
    for c,w in ((d["s1"],"S1"),(d["s2"],"S2"),(d["cause"],"cause"),({"quote":uq,"section":us},"up")):
        chk(fn,secs,c["quote"],c["section"],w)
    for i,e in enumerate(d["ev"]):
        chk(fn,secs,e["quote"],"chronology",f"ev{i}")
        if e["date_text"] and e["date_text"] not in e["quote"] and not e["inherited_date"]: errs.append((fn,i,"date not in quote"))
        if e["inherited_date"]:
            chk(fn,secs,e["entry_quote"],"chronology",f"ent{i}")
            if e["date_text"] not in e["entry_quote"]: errs.append((fn,i,"date not in entry"))
    out.append({"file":fl,"claims":[s1,s2],"cause":d["cause"],"upstream":up,"events":d["ev"]})
print("ERRORS:",errs)
json.dump(out, open(os.path.join(D,"passB.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), sum(len(o["events"]) for o in out))
