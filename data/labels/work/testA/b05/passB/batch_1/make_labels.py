import json, re, os, sys
D = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(D, "texts")

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def sections(path):
    raw = open(path, encoding="utf-8").read()
    fl = re.search(r"^FILE: (.+)$", raw, re.M).group(1).strip()
    b = raw.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    c = raw.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    ch = raw.split("=== CHRONOLOGY ===")[1]
    return fl, {"block": norm(b), "cause": norm(c), "chronology": norm(ch)}

def S1(q, st="SUPPORTED"):
    return {"id": "S1", "status": st, "quote": q, "section": "block" if q else ""}
def S2(st, q="", sec="", name=None):
    d = {"id": "S2", "status": st}
    if name: d["name"] = name
    d["quote"] = q; d["section"] = sec if q else ""
    return d
def C(st, q):
    return {"status": st, "quote": q, "section": "cause" if q else ""}
def U(kind, q="", sec="", names=None):
    return {"kind": kind, "names": names or [], "quote": q, "section": sec if q else ""}
def E(dt, ty, q):
    return {"date_text": dt, "type": ty, "quote": q, "inherited_date": False, "date_inferred": False}
def I(ty, q):
    return {"date_text": "", "type": ty, "quote": q, "inherited_date": False, "date_inferred": True}
def H(dt, ty, q, eq):
    return {"date_text": dt, "type": ty, "quote": q, "inherited_date": True, "entry_quote": eq, "date_inferred": False}

L = {}
L["RCLRPT-24V636-2894"] = dict(
 claims=[S1("Name : Ford Motor Company"), S2("SUPPORTED", "On August 16 2024, Ford’s Field Review Committee reviewed the concern and approved a field action.", "chronology", "Ford")],
 cause=C("SUPPORTED", "A late change was made to this specific vehicle configuration and the incomplete vehicle label and the incomplete vehicle document were not modified to reflect the updated front gross axle weight rating."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("July 11, 2024", "FILER_AWARENESS", "On July 11, 2024, an issue pertaining to a Front Gross Axle Weight Rating (FGAWR) discrepancy on Incomplete Vehicle Labels (IVL) of 2024 Ford Transit vehicles was brought to Ford’s Critical Concern Review Group (CCRG)."),
  I("OTHER", "The investigation determined that due to an oversight during Ford’s label review process, incomplete 2024 Transit cut-away vehicles equipped with 1,875kg FGAWR axles,"),
  I("OTHER", "Based on Computer Aided Engineering (CAE) analysis, Ford concluded that the fatigue life of the front steering knuckles will be reduced if the front axle of an affected vehicle is loaded to the incorrectly listed 2,100kg FGAWR."),
  E("August 16 2024", "DECISION", "On August 16 2024, Ford’s Field Review Committee reviewed the concern and approved a field action."),
 ])
q658 = "As an immediate reaction, in early 2024, MBAG launched an investigation together with the supplier of the welding material to analyze the nature of the deviation."
L["RCLRPT-24V658-4420"] = dict(
 claims=[S1("Name : Safra SpA"), S2("INSUFFICIENT", q658, "chronology")],
 cause=C("SUPPORTED", "Due to a deviation in the production process at a welding material supplier, the material of the welds on certain integral carriers might not meet specifications."),
 upstream=U("UNNAMED", q658, "chronology"),
 events=[
  E("January 2024", "FILER_AWARENESS", "In January 2024, MBAG became aware of a potential deviation in the welding process of a single integral carrier, resulting in an increased occurrence of welding splatter."),
  E("early 2024", "INVESTIGATION_START", q658),
  I("OTHER", "In parallel, MBAG initiated plant campaigns to rework vehicles still in access to MBAG."),
  E("March 2024", "SUPPLIER_NOTICE", "In March 2024, the supplier identified a deviation in the production process of the welding material was causing the observed deviation and determined a batch of potentially affected welding material."),
  E("April through August 2024", "INVESTIGATION_START", "Based on this determination from April through August 2024, MBAG analyzed the potential effects of the suspect welding material on the integral carrier."),
  I("OTHER", "Based on the affected batch of welding materials, MBAG determined the potentially affected vehicle population."),
  E("August 30, 2024", "DECISION", "On August 30, 2024, MBAG determined that a potential safety risk could not be ruled out and decided to conduct a recall."),
 ])
L["RCLRPT-24V666-8037"] = dict(
 claims=[S1("Name : NR", "NOT_REPORTED"), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "The current heat shield does not adequately protect the LP tank from the chassis exhaust."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("8/29", "FILER_AWARENESS", "8/29 – Thor Motor Coach engineering performed a production code audit and found the LP tank heat shield did not pass due to location of chassis exhaust."),
  E("9/5", "DECISION", "9/5 – TMC safety committee agreed a recall will need issued."),
 ])
q671 = "After discussions with Storyteller’s supplier, it was determined that the spare tire mount fasteners were not installed by the supplier to specification."
L["RCLRPT-24V671-1934"] = dict(
 claims=[S1("Name : Summit Products"), S2("INSUFFICIENT", q671, "chronology")],
 cause=C("SUPPORTED", "Storyteller’s vendor did not install the fasteners into the spare tire mount plate to the appropriate specification."),
 upstream=U("UNNAMED", q671, "chronology"),
 events=[
  E("August 29th, 2024", "FILER_AWARENESS", "On August 29th, 2024, Storyteller’s Customer Service Team received a report of a customer’s spare tire mount failing."),
  E("August 30th", "INVESTIGATION_START", "Storyteller’s Safety Committee met on August 30th to open an investigation."),
  I("OTHER", q671),
  E("September 6th", "DECISION", "Storyteller’s Safety Committee met on September 6th and voted to issue a recall."),
 ])
q673 = "On August 16, 2024, GM opened a product investigation into this condition after receiving five VOQs from NHTSA (on July 12, 2024) and an employee Speak Up For Safety (SUFS) report (on July 15, 2024)."
L["RCLRPT-24V673-2026"] = dict(
 claims=[S1("Name : Hasco Vision Technology CO LTD"), S2("INSUFFICIENT", "Name : Hasco Vision Technology CO LTD", "block")],
 cause=C("SUPPORTED", "A defect in the headlamp’s internal software may cause the headlamp to flicker."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("August 16, 2024", "INVESTIGATION_START", q673),
  E("July 12, 2024", "FILER_AWARENESS", q673),
  E("July 15, 2024", "FILER_AWARENESS", q673),
  I("FILER_AWARENESS", "GM’s investigation identified 272 potentially related field complaints, which were received by GM between May 5, 2024, and August 15, 2024."),
  E("August 28-29, 2024", "OTHER", "GM Engineering was able to observe the alleged condition on two company owned vehicles on August 28-29, 2024."),
  E("September 5, 2024", "DECISION", "On September 5, 2024, GM’s Safety Field Action Decision Authority (SFADA) decided to conduct a noncompliance recall."),
 ])
q686 = "The SCCM supplier shipped noncompliant parts to Rivian."
L["RCLRPT-24V686-2089"] = dict(
 claims=[S1("Name : Merit Automotive Electronics Systems"), S2("INSUFFICIENT", q686, "cause")],
 cause=C("SUPPORTED", q686),
 upstream=U("UNNAMED", q686, "cause"),
 events=[
  E("September 06, 2024", "DECISION", "On September 06, 2024, Rivian reviewed the potentially missing SCCM content compared to the requirements and determined that a potential noncompliance to FMVSS No. 101, Controls and displays cannot be ruled out."),
 ])
L["RCLRPT-24V688-3680"] = dict(
 claims=[S1("Name : MBAG"), S2("SUPPORTED", "MBAG then conducted analyses of the potential safety consequences of this issue.", "chronology", "MBAG")],
 cause=C("SUPPORTED", "Due to a deviation in the software development process, the synchronization between the MBUX multimedia system and the parking control unit might be impaired."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("November 2023", "FILER_AWARENESS", "In November 2023, standard system tests on internal vehicles found that specific parking assistance systems might be deactivated without notice."),
  E("November 2023 to January 2024", "INVESTIGATION_START", "From November 2023 to January 2024, investigations were started to identify the root cause."),
  I("OTHER", "Analyses determined that a deviation in the vehicle's software might result in a synchronization problem between the MBUX multimedia system and the parking control."),
  E("January 2024", "INVESTIGATION_START", "Starting in January 2024, analyses on the possible consequences of the observed issue were performed."),
  I("OTHER", "Additional and more detailed tests were found to be necessary to get a deeper understanding of the issue and the possible consequences."),
  I("OTHER", "These tests determined that the cross-traffic-alert might also be affected by the deviation."),
  I("INVESTIGATION_START", "MBAG then conducted analyses of the potential safety consequences of this issue."),
  I("OTHER", "These studies determined that in the event of a cross-traffic-alert (which is activated when an oncoming road user is detected while the vehicle is exiting a parking space)"),
  E("August 2024", "OTHER", "The potentially affected vehicle population was determined throughout August 2024."),
  I("INVESTIGATION_START", "In parallel, a possible non-compliance was thoroughly examined."),
  E("September 6th, 2024", "DECISION", "On September 6th, 2024, MBAG determined that a potential safety risk cannot be ruled out and decided to conduct a recall."),
 ])
q706 = "The issue was reported to Oliva Torras and analysis of the possible causes was initiated, both by Oliva Torras and Micro Bird."
L["RCLRPT-24V706-2031"] = dict(
 claims=[S1("Name : Oliva Torras"), S2("SUPPORTED", q706, "chronology", "Oliva Torras")],
 cause=C("NOT_REPORTED", "NR"),
 upstream=U("NAMED", q706, "chronology", ["Oliva Torras", "GM"]),
 events=[
  E("June 2024", "FILER_AWARENESS", "In June 2024, during inspection, an unusual noise coming from the engine drive belt was reported."),
  I("INVESTIGATION_START", "Cursory investigation identified that this might be linked to the installation of a second air conditioning compressor."),
  I("INVESTIGATION_START", q706),
  I("OTHER", "Initially, the cause was identified as an increase of tension of the engine drive belt on the idler pulleys."),
  I("OTHER", "But after more tests, it was determined that the tensioner provided by Oliva Torras and that replaced the tensioner installed originally by GM, was not strong enough to correctly maintain the tension in the engine drive belt,"),
  E("September 16, 2024", "DECISION", "After identification of the defect and its safety risk, on September 16, 2024, it was decided to recall all the vehicles delivered with the identified second air conditioning compressor."),
 ])
L["RCLRPT-24V743-7902"] = dict(
 claims=[S1("Name : Altec Industries Inc."), S2("SUPPORTED", "The driver notified Altec of the incident, and the subject unit was transported to an Altec service center to investigate the cause.", "chronology", "Altec")],
 cause=C("NOT_REPORTED", "NR"),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("September 17, 2024", "OTHER", "On September 17, 2024, a driver delivering a completed unit to a customer experienced a thermal event during the trip."),
  I("FILER_AWARENESS", "The driver notified Altec of the incident, and the subject unit was transported to an Altec service center to investigate the cause."),
  I("OTHER", "The service center found hydraulic hoses from an engine-mounted clutch pump routed near the engine exhaust manifold had been overheated and began to burn."),
  E("September 20, 2024", "INVESTIGATION_START", "On September 20, 2024, an investigation was opened to determine the root cause and whether additional units could be affected."),
  I("OTHER", "The investigation found that certain units had the hydraulic hoses improperly routed through the engine compartment, locating them within the minimum recommended clearance of hot exhaust components and that affected units could be in the field."),
  E("September 27, 2024", "DECISION", "On September 27, 2024, after reviewing the incident, investigation, and the build history of the units, Altec determined that a potential defect could exist."),
 ])
L["RCLRPT-24V765-9156"] = dict(
 claims=[S1("Name : OSLV ITALIA SRL"), S2("INSUFFICIENT", "Name : OSLV ITALIA SRL", "block")],
 cause=C("SUPPORTED", "Due to raw material properties variability combined with dimensioning limits of the wiper lever connecting rod, it could start to deform and eventually fail."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("September 2024", "FILER_AWARENESS", "In September 2024, during internal controls in the factory, Lamborghini identified a potential issue regarding the passenger windshield wiper system."),
  I("OTHER", "The separation of the wiper arm connecting rod from the wiper motor was observed in some cars during quality controls."),
  I("INVESTIGATION_START", "Lamborghini immediately began an investigation of the issue."),
  I("OTHER", "Analysis demonstrated reduced performance of the wiper arm connecting rod."),
  I("FILER_AWARENESS", "During the analysis period, Lamborghini identified 6 warranty claims related to this issue worldwide."),
  E("October 8, 2024", "DECISION", "On October 8, 2024, the Lamborghini Product Safety Committee determined that a defect related to motor vehicle safety exists and decided to conduct a voluntary safety recall."),
 ])
L["RCLRPT-24V775-3530"] = dict(
 claims=[S1("Name : NR", "NOT_REPORTED"), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "Manufacturing error."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("September 9, 2024", "FILER_AWARENESS", "On September 9, 2024, Forest River's Pre-Delivery Inspection plant found that a model did not have an anti- siphon vent plant installed in the washer prep area."),
  E("October 9, 2024", "FILER_AWARENESS", "On October 9, 2024, during a routine Standards Manager Inspection of the plant, the Standards Manager found the manufacturing plant had more than the single unit affected."),
  I("FILER_AWARENESS", "The same day Forest River's Office of Corporate Compliance was contacted by the Standards Manager."),
  I("INVESTIGATION_START", "A research item was opened into the concern."),
  E("October 15, 2024", "OTHER", "On October 15, 2024, it was discovered that manufacturing had been installing the washer prep without the anti-siphon vent consistently."),
  E("October 18, 2024", "DECISION", "On October 18, 2024. Forest River's Corporate Committee voted to recall."),
 ])
e789a = "09-17-24: Safety and compliance notified."
e789b = "10-08-24: Safety committee meeting held."
L["RCLRPT-24V789-9845"] = dict(
 claims=[S1("Name : Cummins, Inc."), S2("SUPPORTED", "09-27-24: Cummins provided explanation for remaining PACCAR questions.", "chronology", "Cummins")],
 cause=C("SUPPORTED", "Defective parts have incomplete heat treat scale removal and nonconforming shot peening coverage, resulting in low fatigue strength."),
 upstream=U("NAMED", "09-27-24: Cummins provided explanation for remaining PACCAR questions.", "chronology", ["Cummins"]),
 events=[
  E("09-17-24", "FILER_AWARENESS", e789a),
  H("09-17-24", "INVESTIGATION_START", "Investigation opened.", e789a),
  E("09-24-24", "SUPPLIER_NOTICE", "09-24-24: Cummins’ 573 filed with NHTSA; copy provided to Kenworth S&C."),
  E("9-22-24", "OTHER", "9-22-24: Cummins’ lists of affected engines for Kenworth and Peterbilt provided; work started to align provided engine serial numbers with Kenworth and Peterbilt chassis."),
  E("09-27-24", "OTHER", "09-27-24: Cummins provided explanation for remaining PACCAR questions."),
  E("10-08-24", "OTHER", e789b),
  H("10-08-24", "DECISION", "All members in attendance concur with Cummins that a safety related defect exists and that the affected population shall be recalled.", e789b),
  E("10-16-24", "DECISION", "10-16-24: Final members of Safety Committee provided concurrence that safety related defect exists and that the affected population shall be recalled."),
 ])
L["RCLRPT-24V809-8433"] = dict(
 claims=[S1("Name : Hirschvogel Holding GmbH"), S2("INSUFFICIENT", "Name : Hirschvogel Holding GmbH", "block")],
 cause=C("INSUFFICIENT", "The cause of the issue is currently under continued investigation."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("September and mid-Oct., 2024", "FILER_AWARENESS", "Between September and mid-Oct., 2024, Porsche became aware of 4 incidents in the U.S. attributable to center lock fractures."),
  E("Sept. 6th", "OTHER", "One case happened during the tightening process in the workshop after a regular wheel replacement was carried out (Sept. 6th)."),
  E("Sept 23rd", "OTHER", "Another case was identified by unnormal vibrations while driving at highway speeds (Sept 23rd)."),
  E("Sept. 23rd", "FILER_AWARENESS", "Two cases were reported as accidents with the loss of the respective wheels but without any deaths or injuries (Sept. 23rd & Oct. 15th)."),
  E("Oct. 15th", "FILER_AWARENESS", "Two cases were reported as accidents with the loss of the respective wheels but without any deaths or injuries (Sept. 23rd & Oct. 15th)."),
  E("Oct. 21st", "DECISION", "Although the cause remains under investigation, Porsche decided on Oct. 21st to conduct a safety recall and ask customers to stop use on the subject vehicles."),
 ])
e820 = "May 22, 2024 – October 7, 2024 Honda continued to investigate, with a focus on the potential for and impact of bolt loosening."
e820b = "August 12, 2024 Honda received NHTSA VOQ reports of a vehicle stalling and the rider falling."
L["RCLRPT-24V820-7053"] = dict(
 claims=[S1("Name : Saga Tekkosho Co., Ltd."), S2("INSUFFICIENT", "Name : Saga Tekkosho Co., Ltd.", "block")],
 cause=C("SUPPORTED", "During vehicle development, the primary gear specifications did not account for certain riding conditions involving on-off throttle applications."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("March 2020 – January 2021", "FILER_AWARENESS", "March 2020 – January 2021 Honda received quality reports of the issue and began to investigate."),
  E("January 2021 – February 2021", "OTHER", "January 2021 – February 2021 Honda analyzed the issue and decided to improve the toughness of the bolt, despite not knowing the cause of the issue, nor the potential incidences which may occur."),
  E("March 2, 2021", "FILER_AWARENESS", "March 2, 2021 Honda received an additional quality report of the issue and continued to investigate."),
  E("February 2022 – August 2022", "FILER_AWARENESS", "February 2022 – August 2022 Honda received additional reports and began to reanalyze and investigate the issue, focusing on potential conditions causing vehicle stress."),
  E("September 2022 – November 2023", "INVESTIGATION_START", "September 2022 – November 2023 Honda obtained relevant data and continued to investigate and analyze the issue."),
  E("October 2022 – March 2024", "FILER_AWARENESS", "October 2022 – March 2024 Honda received additional quality reports of the issue."),
  E("March 25, 2024", "INVESTIGATION_START", "March 25, 2024 Honda continued to investigate the cause of the issue."),
  E("May 22, 2024 – October 7, 2024", "INVESTIGATION_START", e820),
  H("May 22, 2024 – October 7, 2024", "OTHER", "Honda determined that bolt loosening was not an applicable variable for the issue.", e820),
  E("August 12, 2024", "FILER_AWARENESS", e820b),
  H("August 12, 2024", "INVESTIGATION_START", "Honda continued to investigate the issue.", e820b),
  E("September 10-18, 2024", "FILER_AWARENESS", "September 10-18, 2024 Honda received additional reports, including a NHTSA VOQ involving customer injury."),
  E("September 18, 2024", "FILER_AWARENESS", "September 18, 2024 NHTSA urged Honda to conduct a safety recall."),
  E("October 3, 2024", "INVESTIGATION_START", "October 3, 2024 Honda refocused its investigation and analysis efforts from stress measurements of the vehicle to the bolt."),
  E("October 24, 2024", "DECISION", "October 24, 2024 Honda determined that a defect related to motor vehicle safety existed and decided to conduct a safety recall."),
 ])
L["RCLRPT-24V826-8574"] = dict(
 claims=[S1("Name: Winnebago Ind Inc."), S2("SUPPORTED", "In late August, Winnebago Product Safety was notified of a concern where a hood bracket had separated from the vehicle in transit.", "chronology", "Winnebago")],
 cause=C("SUPPORTED", "On certain Winnebago vehicles the adhesive application was incorrectly applied or had incorrect prep work performed."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("late August", "FILER_AWARENESS", "In late August, Winnebago Product Safety was notified of a concern where a hood bracket had separated from the vehicle in transit."),
  I("INVESTIGATION_START", "An investigation was subsequently opened."),
  I("FILER_AWARENESS", "During the investigation, 344 total claims were identified, with some instances of completely detached hood brackets."),
  E("October 25, 2024", "DECISION", "On October 25, 2024, the Product Safety Committee met and decided the defect presented an unreasonable risk to safety."),
 ])
L["RCLRPT-24V852-6661"] = dict(
 claims=[S1("Name : Ford Motor Company"), S2("SUPPORTED", "On November 1, 2024, Ford’s Field Review Committee reviewed the concern and approved a field action.", "chronology", "Ford")],
 cause=C("SUPPORTED", "The dashboard airbag warning label was incorrectly released in Ford’s engineering release system for certain export markets."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("September 17, 2024", "FILER_AWARENESS", "On September 17, 2024, an issue pertaining to missing dashboard airbag warning labels was brought to Ford’s Critical Concern Review Group (CCRG) for review."),
  I("FILER_AWARENESS", "The issue was discovered during an audit of 2025MY Explorer and Aviator export vehicles."),
  I("OTHER", "Further investigation showed that the label was not released correctly in the Ford engineering release system for US Territories and Government/Military export vehicles, which require the label."),
  E("October of 2024", "INVESTIGATION_START", "In October of 2024, the instrument panel engineering team conducted a read-across for label releases, which revealed that the release issue started with the 2020MY Explorer and Aviator launch"),
  I("DECISION", "Ford’s CCRG reviewed the FMVSS 208 requirements and determined that the affected export vehicles do not comply with section 4.5.1(e) Labeling and Owners Guide Information."),
  E("November 1, 2024", "DECISION", "On November 1, 2024, Ford’s Field Review Committee reviewed the concern and approved a field action."),
 ])
L["RCLRPT-24V860-6666"] = dict(
 claims=[S1("Name : NR", "NOT_REPORTED"), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "The fuel tank may have been altered prior to vehicle sale resulting in holes being present in the tank."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("September 26, 2024", "FILER_AWARENESS", "On September 26, 2024 IMC received a dealer report of a hole present in a fuel tank."),
  E("October 10, 2024", "OTHER", "On October 10, 2024 IMC reviewed internal records and determined the vehicle had been previously altered during vehicle certification testing."),
  I("INVESTIGATION_START", "Thereafter, additional review was conducted of units that had undergone the same certification testing, resulting in the identification of 4 total vehicles that were converted for sale in the US after undergoing certification testing."),
  E("October 24, 2024", "INVESTIGATION_START", "On October 24, 2024, IMC began an investigation."),
  E("November 7, 2024", "DECISION", "On November 7, 2024, IMC’s Executive Review Committee decided that the altered fuel tank concern resulted in a safety-related defect."),
 ])
e863 = "11/1/2024 – 11/10/2024: Units were repaired by Grand Design, prior to shipping."
L["RCLRPT-24V863-6452"] = dict(
 claims=[S1("Name : Dave Carter & Associates"), S2("INSUFFICIENT", "Name : Dave Carter & Associates", "block")],
 cause=C("SUPPORTED", "Improper install of the battery warmer"),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("10/28/2024", "FILER_AWARENESS", "10/28/2024: Production identified a concern related to battery warming pads on the motorized Lineage line."),
  E("11/1/2024 – 11/10/2024", "OTHER", e863),
  H("11/1/2024 – 11/10/2024", "OTHER", "Proper install instructions identified.", e863),
  E("11/11/2024", "DECISION", "11/11/2024: Grand Design votes to recall shipped units"),
 ])
q892 = "From August 2023 throughout November 2023, after various discussions and testing performed by the software supplier,"
L["RCLRPT-24V892-6729"] = dict(
 claims=[S1("Name : Robert Bosch GmbH"), S2("INSUFFICIENT", q892, "chronology")],
 cause=C("NOT_REPORTED", "NR"),
 upstream=U("UNNAMED", q892, "chronology"),
 events=[
  E("July 2023", "FILER_AWARENESS", "In July 2023, Maserati was informed by parent company Stellantis NA about a potential issue affecting Central Vision Processing/Park assist Module (“CVPAM”) software (version 4.4)."),
  I("INVESTIGATION_START", "MNA immediately opened an internal investigation."),
  E("August 2023 throughout November 2023", "SUPPLIER_NOTICE", "From August 2023 throughout November 2023, after various discussions and testing performed by the software supplier, the supplier itself stated that “although Maserati Grecale and Granturismo software contains the deviation,"),
  E("November 22, 2023", "OTHER", "On November 22, 2023, at Vehicle Regulation Committee (VRC), Maserati spA decided, based on supplier’s statement to put the investigation in monitoring status in order to verify that the condition did not exist in the field."),
  E("September 2024", "INVESTIGATION_START", "In September 2024, after a deep analysis of field data, Maserati SpA re-opened the investigation based on 10 suspected warranty claims."),
  E("November the 19th 2024", "DECISION", "On November the 19th 2024, Maserati S.p.A. determined, through the VRC to conduct a Voluntary Safety Recall for all affected vehicles."),
 ])
L["RCLRPT-24V897-2591"] = dict(
 claims=[S1("Name : Magna International"), S2("INSUFFICIENT", "Name : Magna International", "block")],
 cause=C("NOT_REPORTED", "NR"),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("April 25, 2023", "FILER_AWARENESS", "On April 25, 2023, the FCA US LLC (\"FCA US\") Technical Safety and Regulatory Compliance (\"TSRC\") organization was notified of a potential issue related to improperly secured seat wiring connectors"),
  E("May 2023, through October 2023", "INVESTIGATION_START", "From May 2023, through October 2023, FCA US TSRC reviewed warranty data, vehicle production records, field records, and customer assistance records to understand potential customer consequence."),
  E("October 2023, through September 2024", "OTHER", "From October 2023, through September 2024, FCA US TSRC held regular meetings with FCA US Engineering and Supplier Quality to understand all potential failure modes of the issue and determine the suspect population."),
  E("October 09, 2024", "OTHER", "On October 09, 2024, the FCA US TSRC organization recognized a front seat SAB squib connector issue existed on certain vehicles related to improper securement of the connectors, potentially resulting in a noncompliance with FMVSS No. 214."),
  E("November 21, 2024", "DECISION", "On November 21, 2024, FCA US determined, through the Vehicle Regulations Committee, to conduct a voluntary safety recall of the affected vehicles."),
 ])
q899 = "11/18/2024 – Report was made phone call from vendor due to an audit."
e899a = "11/18/2024 – Investigation opened."
e899b = "11/25/2024 – Keystone Safety Committee reviewed the information and concluded that the data reviewed indicated a unanimous vote for a voluntary recall."
L["RCLRPT-24V899-7356"] = dict(
 claims=[S1("Name : Lippert"), S2("INSUFFICIENT", q899, "chronology")],
 cause=C("SUPPORTED", "The fasteners used to assemble the Helux pin box may not have been properly torqued."),
 upstream=U("UNNAMED", q899, "chronology"),
 events=[
  E("11/18/2024", "SUPPLIER_NOTICE", q899),
  E("11/18/2024", "INVESTIGATION_START", e899a),
  H("11/18/2024", "OTHER", "All affected units were put on hold and yard was inspected and all units on the yard were fixed.", e899a),
  E("11/25/2024", "DECISION", e899b),
  H("11/25/2024", "INVESTIGATION_START", "Investigation called for to determine affected unit range.", e899b),
  E("11/26/2024", "OTHER", "11/26/2024 – Investigation concluded and scope completed."),
 ])
L["RCLRPT-24V919-6910"] = dict(
 claims=[S1("Name : Roadtrek Inc."), S2("INSUFFICIENT", "Name : Roadtrek Inc.", "block")],
 cause=C("INSUFFICIENT", "While the vehicle is in motion, passengers wearing the seat belts may experience the seat belt is delayed in retracting."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("25thNov2024", "FILER_AWARENESS", "Upon quality audit on 25thNov2024, quality found a van that had a seat belt on the 2nd row seat that had delay retracting issue."),
  I("OTHER", "After further investigation was completed and it was determined under certain conditions that the seat foam could impede with seat belt retractility."),
 ])
L["RCLRPT-24V937-9596"] = dict(
 claims=[S1("Name : NR", "NOT_REPORTED"), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "BCM software calibrations were not properly implemented in production for the 2025 model year."),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("October 17, 2024", "FILER_AWARENESS", "On October 17, 2024, a GM engineer submitted this issue to GM’s Speak Up For Safety (SUFS) program after an audit revealed that BCM calibrations for the pedestrian alert feature were released incorrectly for certain 2025 model year Silverado EV vehicles."),
  E("October 29, 2024", "INVESTIGATION_START", "GM opened a product investigation on October 29, 2024."),
  I("OTHER", "GM’s investigation determined that the body control module (BCM) software calibrations for the pedestrian alert feature on the 2025 model year Silverado EV work truck (WT) trimline were not properly implemented in production."),
  I("OTHER", "Testing indicated that, as a result of the incorrect calibration, vehicles in the field may not meet certain volume requirements of S5.2 of FMVSS 141."),
  E("December 12, 2024", "DECISION", "On December 12, 2024, GM’s Safety Field Action Decision Authority (SFADA) decided to conduct a noncompliance recall."),
 ])
e949 = "September – November 2024 On September 12, 2024, Ford received a Global Common Quality Indicator System (GCQIS) incident report pertaining to a missing left front upper control arm ball joint nut on a 2024 model year F-150 BEV vehicle."
L["RCLRPT-24V949-7212"] = dict(
 claims=[S1("Name : Ford Motor Company"), S2("SUPPORTED", "On December 13, 2024, Ford’s Field Review Committee reviewed the concern and approved a field action.", "chronology", "Ford")],
 cause=C("SUPPORTED", "The nut on the upper control arm ball joint may not have achieved the correct torque due to variation in the alignment or orientation between the fastening tool and the fastener that may have induced lateral forces on the tool,"),
 upstream=U("NONE_MENTIONED"),
 events=[
  E("September 12, 2024", "FILER_AWARENESS", "On September 12, 2024, Ford received a Global Common Quality Indicator System (GCQIS) incident report pertaining to a missing left front upper control arm ball joint nut on a 2024 model year F-150 BEV vehicle."),
  H("September – November 2024", "OTHER", "The customer reported that at 639 miles they experienced intermittent vibration while driving at highway speed before the vehicle suddenly made an uncommanded left turn into a side rail.", e949),
  H("September – November 2024", "OTHER", "Upon inspection, the dealer technician discovered the upper control arm nut was missing and the joint had separated from the knuckle.", e949),
  E("October 3, 2024", "INVESTIGATION_START", "On October 3, 2024, Ford’s Critical Concern Review Group (CCRG) opened its investigation into this issue."),
  I("INVESTIGATION_START", "The CCRG investigation included a review of the assembly plant retorquing station data when 100% torque inspection was in place."),
  I("OTHER", "Based on a review of this data, CCRG was able to determine that certain vehicles built between November 6, 2023 and February 12, 2024, may have failed to achieve the required torque"),
  I("OTHER", "CCRG was able to confirm that the suspect vehicle population, including the vehicle that experienced an accident, were built within this date range."),
  E("December 13, 2024", "DECISION", "On December 13, 2024, Ford’s Field Review Committee reviewed the concern and approved a field action."),
 ])
L["RCLRPT-24V963-3467"] = dict(
 claims=[S1("", "NOT_REPORTED"), S2("NOT_REPORTED")],
 cause=C("SUPPORTED", "Orange EV did not properly conduct a visibility assessment after offering beavertails as an option."),
 upstream=U("NOT_REPORTED", "Please see the attached Part 573 Defect Information Report for the full chronology.", "chronology"),
 events=[])

out = []
errs = 0
files = sorted(f for f in os.listdir(T) if f.startswith("RCLRPT") and f.endswith(".txt"))
assert len(files) == 25, len(files)
for f in files:
    key = f[:-4]
    fl, sec = sections(os.path.join(T, f))
    lab = L[key]
    obj = {"file": fl, "claims": lab["claims"], "cause": lab["cause"], "upstream": lab["upstream"], "events": lab["events"]}
    def chk(q, s, what):
        global errs
        if not q: return
        if len(q) > 300: print(key, what, "TOO LONG", len(q)); errs += 1
        if norm(q) not in sec[s]: print(key, what, "NOT FOUND in", s, ":", q); errs += 1
    for c in obj["claims"]: chk(c["quote"], c["section"], c["id"])
    chk(obj["cause"]["quote"], obj["cause"]["section"], "cause")
    chk(obj["upstream"]["quote"], obj["upstream"]["section"], "upstream")
    for i, e in enumerate(obj["events"]):
        chk(e["quote"], "chronology", "ev%d" % i)
        if e["date_text"] and not e["inherited_date"] and e["date_text"] not in e["quote"]: print(key, i, "date not in quote"); errs += 1
        if e.get("inherited_date"):
            chk(e["entry_quote"], "chronology", "entry%d" % i)
            if e["date_text"] not in e["entry_quote"]: print(key, i, "date not in entry"); errs += 1
    out.append(obj)
print("errors", errs)
if errs == 0:
    json.dump(out, open(os.path.join(D, "passB.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", len(out), "events", sum(len(o["events"]) for o in out))
