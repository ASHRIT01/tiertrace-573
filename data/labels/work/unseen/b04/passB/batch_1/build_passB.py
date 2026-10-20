import json, os, re
D = os.path.dirname(os.path.abspath(__file__))

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def sections(fn):
    t = open(os.path.join(D, "texts", fn), encoding="utf-8").read()
    b = t.split("=== COMPONENT MANUFACTURER BLOCK ===")[1].split("=== DESCRIPTION OF THE CAUSE ===")[0]
    c = t.split("=== DESCRIPTION OF THE CAUSE ===")[1].split("=== CHRONOLOGY ===")[0]
    h = t.split("=== CHRONOLOGY ===")[1]
    fl = re.search(r"^FILE: (\S+)", t, re.M).group(1)
    return fl, {"block": norm(b), "cause": norm(c), "chronology": norm(h)}

def E(date, typ, quote, entry=None, inf=False):
    d = {"date_text": date, "type": typ, "quote": quote, "inherited_date": entry is not None}
    if entry is not None:
        d["entry_quote"] = entry
    d["date_inferred"] = inf
    return d

def S1(q):
    return {"id": "S1", "status": "SUPPORTED", "quote": q, "section": "block"}
S1NR = {"id": "S1", "status": "NOT_REPORTED", "quote": "", "section": "block"}
def S2(st, name, q, sec):
    d = {"id": "S2", "status": st}
    if name: d["name"] = name
    d["quote"] = q; d["section"] = sec
    return d
S2NR = {"id": "S2", "status": "NOT_REPORTED", "quote": "", "section": ""}
def C(st, q):
    return {"status": st, "quote": q, "section": "cause"}
def U(kind, names=(), q="", sec=""):
    return {"kind": kind, "names": list(names), "quote": q, "section": sec}

L = {}

# 1
q1 = "On April 22, 2025, Bendix was made aware that Nova Bus had submitted Defect Information Reports to NHTSA (24V-558, 24V559 and 25E-027) related to the performance of certain brake chambers produced by Knorr-Bremse."
L["RCLRPT-25E048-6886.txt"] = ([S1("Name: Knorr-Bremse"), S2("SUPPORTED", "Knorr-Bremse", q1, "chronology")],
 C("SUPPORTED", "This piston style parking brake chamber part number K038830N00 was built with a piston seal that was found to leak intermittently internally due to material, manufacturing variation, and environmental conditions."),
 U("NAMED", ["Knorr-Bremse"], q1, "chronology"),
 [E("April 22, 2025", "FILER_AWARENESS", q1),
  E("2021", "OTHER", "Knorr-Bremse had previously reviewed this issue with Nova Bus in 2021 and the parties concluded the performance of the brake chamber did not amount to an unreasonable risk to safety due to the low severity of any risk (no potential for unexpected brake application or risk of fire)"),
  E("July 29, 2025", "DECISION", "Following Nova Bus’ determination that a safety defect exists in these parts and in order to support its campaign, on July 29, 2025, Bendix decided to conduct a recall to address the aftermarket parts that it sells to distributors and end- customers.")])

# 2
a = "January 2023 - June 2023: Bosch notified ZF of a concern with iTCU weld integrity on its E-Modules supplied to BMW, discovered during certain quality assurance tests."
s9 = "September 2023 - November 2023: ZF worked with both customers (BMW and Stellantis) to investigate the issue."
au = "August 2024: Following Stellantis's recall, NHTSA contacted ZF and asked whether ZF supplied the subject components to additional U.S.-based vehicle manufacturers."
se = "September 4-9, 2025: ZF received a follow-up inquiry form NHTSA's Recall Management Division, again asking whether ZF supplied the subject components to other vehicle manufacturers."
s5 = "September 5 - 16, 2025: ZF reviewed records to confirm regulatory requirements."
L["RCLRPT-25E058-9353.txt"] = ([S1("Name: Robert Bosch GmbH"), S2("SUPPORTED", "Bosch", a, "chronology")],
 C("SUPPORTED", "Based on ZF's investigation, Bosch identified an issue with their electrode maintenance procedures, thereby causing the iTCUs at issue to be produced out of specification."),
 U("NAMED", ["Bosch"], a, "chronology"),
 [E("January 2023 - June 2023", "SUPPLIER_NOTICE", a),
  E("January 2023 - June 2023", "INVESTIGATION_START", "ZF jointly investigated the potential issue with Bosch, including engineering analysis and inspection / analysis of affected parts.", a),
  E("July 2023", "OTHER", "July 2023: ZF informed BMW about a potential concern involving the iTCUs with Bosch E-Modules."),
  E("July 2023 - September 2023", "INVESTIGATION_START", "July 2023 - September 2023: ZF jointly investigated the issue with BMW, including further testing and analysis of parts, photo-microscopy and shaker tests to evaluate long-term durability."),
  E("September 2023", "SUPPLIER_NOTICE", "September 2023: Bosch reported concerns with additional E-Modules, this time affecting Stellantis and five additional OEMs of vehicles outside the U.S. Market."),
  E("September 2023 - November 2023", "INVESTIGATION_START", s9),
  E("September 2023 - November 2023", "INVESTIGATION_START", "Collaborative investigation and analyses were conducted, including failure modes and affects analyses, review of field information, production process testing details, production lot information, and scope parameters.", s9),
  E("November 29, 2023", "OTHER", "November 29, 2023: BMW initiated a recall of 552 vehicles containing ZF iTCU units with suspect Bosch E-Modules (23V-821)."),
  E("November 2023 - May 2024", "INVESTIGATION_START", "November 2023 - May 2024: Further collaborative investigation and analyses were conducted with Stellantis."),
  E("May 31, 2024", "OTHER", "May 31, 2024: Stellantis initiated a recall of 234 vehicles containing ZF iTCU units with suspect Bosch E-Modules (24V-413)."),
  E("August 2024", "FILER_AWARENESS", au),
  E("August 2024", "OTHER", "ZF advised NHTSA that no additional vehicle manufacturers (beyond BMW and Stellantis) received these parts.", au),
  E("September 4-9, 2025", "FILER_AWARENESS", se),
  E("September 4-9, 2025", "OTHER", "ZF again advised NHTSA that these parts were supplied only to BMW and Stellantis.", se),
  E("September 4-9, 2025", "OTHER", "NHTSA then requested that ZF file a 573 report based upon the reports submitted by BMW (23V-821) and Stellantis (24V-413).", se),
  E("September 5 - 16, 2025", "OTHER", s5),
  E("September 5 - 16, 2025", "NHTSA_FILING", "Based on the recalls conducted by BMW and Stellantis, ZF is providing this defect information report under 49 CFR 573.3(f).", s5)])

# 3
q3 = "Following a review in late October 2025, Bendix identified certain ECU part numbers that were believed to be obsolete that were still active in Bendix internal systems."
L["RCLRPT-25E073-6952.txt"] = ([S1("Name: Bendix Commercial Vehicle Systems"), S2("SUPPORTED", "Bendix", q3, "chronology")],
 C("NOT_REPORTED", ""), U("NONE_MENTIONED"),
 [E("late October 2025", "FILER_AWARENESS", q3),
  E("", "INVESTIGATION_START", "Bendix performed a query which identified approximately 2,300 parts with the same or substantially similar software to the ECUs that are the subject of NHTSA Recall 24E-086 had inadvertently been sold as aftermarket equipment.", inf=True),
  E("October 31, 2025", "DECISION", "On October 31, 2025, Bendix decided to conduct a safety recall to address these additional units.")])

# 4
L["RCLRPT-25E076-9018.txt"] = ([S1NR, S2NR],
 C("SUPPORTED", "A machining operation to standardize gear teeth height was not completed for 98 gears ."), U("NONE_MENTIONED"),
 [E("8/27/2025", "FILER_AWARENESS", "8/27/2025 Initial notification from customer that differentials were generating a ratcheting noise"),
  E("9/1/2025", "INVESTIGATION_START", "9/1/2025 Containment and root cause investigation started at manufacturing plants) for p/n Q14022- 010 (aftermarket differential); Requests sent to customers to place all parts with p/n on-hold pending further notice"),
  E("9/10/2025", "OTHER", "9/10/2025 sample parts from customers received at manufacturing plant; Requested customers return all parts they currently have in stock (regardless of part number or date of build)"),
  E("9/11/2025", "OTHER", "9/11/2025 discovered during investigation at gear manufacturing plant that some samples of part number Q47170 (gear) have oversize teeth"),
  E("9/16/2025", "OTHER", "9/16/2025 Investigation confirmed total population of 98 gears did not complete machining operation for teeth height"),
  E("5/22/2025", "OTHER", "Total population of 98 gears was shipped to differential assembly plant on 5/22/2025"),
  E("9/22/2025", "OTHER", "9/22/2025 Population of suspect differentials is expanded to p/n Q14022-010, Q14023-010, Q14032- 010, Q14033-010; as they all are determined to use the same Q47170 (gear) – total suspect differential population now 298 parts"),
  E("10/9/2025", "INVESTIGATION_START", "10/9/2025 to present– additional engineering testing and analysis to confirm issue and reconfirm total scope")])

# 5
L["RCLRPT-25V006-1666.txt"] = ([S1("Name : Hyundai Mobis"), S2("INSUFFICIENT", None, "Name : Hyundai Mobis", "block")],
 C("SUPPORTED", "A software logic error"), U("NOT_REPORTED"), [])

# 6
L["RCLRPT-25V068-2775.txt"] = ([S1("Name : AUTOLIV SHANGHAI (CTC) VEHICLE SAFETY-SY"), S2("INSUFFICIENT", None, "Name : AUTOLIV SHANGHAI (CTC) VEHICLE SAFETY-SY", "block")],
 C("SUPPORTED", "The head of the dummy was stopped by the passenger airbag as well as the inflatable curtain towards the A-pillar, but still resulted in NIJ criteria exceeding specified limits."),
 U("NONE_MENTIONED"),
 [E("January 9, 2025", "OTHER", "On January 9, 2025, the final verification crash test was performed according to FMVSS 208, “Occupant Crash Protection, Paragraph S5.1.2.a.2, Unbelted Test Front impact 40 kph, 30 Degrees Right.”"),
  E("", "FILER_AWARENESS", "The NIJ criteria failed to meet legal limits.", inf=True),
  E("", "INVESTIGATION_START", "Zeekr immediately launched an investigation to determine the root cause and understand why this had not been found during previous testing.", inf=True),
  E("", "OTHER", "The result of the investigation revealed a difference in dummy trajectory towards the IC and PAB, resulting in an impact of the head to an unintended area of the IC, which caused the higher NIJ values.", inf=True),
  E("January 31, 2025", "DECISION", "An assessment of the noncompliance risk was started and following the results, the issue was escalated to the top management of Zeekr Technology Europe on January 31, 2025 with a subsequent determination of noncompliance."),
  E("February 4, 2025", "OTHER", "Zeekr US was informed the same day and the global management team was informed at the Critical Concerns Management Team (CCMT) meeting on February 4, 2025."),
  E("", "DECISION", "A decision was made to notify NHTSA and remedy all vehicles before delivery to the customer.", inf=True)])

# 7
dec = "December, 2024 : During the investigation, the safety office team notices a potential non-compliance affecting more vehicles than those of the specific customer."
L["RCLRPT-25V101-2428.txt"] = ([S1("Name: Arow Global"), S2("INSUFFICIENT", None, "Name: Arow Global", "block")],
 C("SUPPORTED", "Incorrect amount of emergency exits included in vehicle design."), U("NONE_MENTIONED"),
 [E("October 29th, 2024", "OTHER", "October 29th, 2024 : Customer Project Manager files a client request to replaced fixed windows by openable windows on buses in service for ventilation purposes."),
  E("November 12th, 2024", "OTHER", "November 12th, 2024 : Engineering evaluates the request."),
  E("November 21st, 2024", "FILER_AWARENESS", "November 21st, 2024: Nova Bus engineering notices a potential non-compliance to FVMSS 217 with client bus configuration and informs the safety office."),
  E("November 29th, 2024", "INVESTIGATION_START", "November 29th, 2024: Nova Bus opens a formal potential safety related issue investigation."),
  E("December, 2024", "OTHER", dec),
  E("December, 2024", "INVESTIGATION_START", "Similar configurations are screened through to identify other potential affected vehicles.", dec),
  E("January 16th, 2025", "OTHER", "January 16th, 2025: Product Safety Evaluation Committee evaluates the information and decides to raise to Product Safety Committee."),
  E("January 21st, 2025", "OTHER", "January 21st, 2025: Product Safety Committee requests additional information and clarifications."),
  E("February 11th, 2025", "DECISION", "February 11th, 2025 : Product Safety Committee determination of a non-compliance to FMVSS 217."),
  E("February 17th, 2025", "NHTSA_FILING", "February 17th, 2025: Nova Bus files 573 with NHTSA that a voluntary recall will be released to address the non-compliance.")])

# 8
q8 = "On April 25, 2025, a MORryde sales representative informed KZ of the recall."
L["RCLRPT-25V292-4296.txt"] = ([S1("Name : MORryde"), S2("SUPPORTED", "MORryde", q8, "chronology")],
 C("SUPPORTED", "The receiving bracket for the step was not built properly with the locking component."),
 U("NAMED", ["MORryde"], q8, "chronology"),
 [E("April 25, 2025", "SUPPLIER_NOTICE", q8),
  E("", "OTHER", "All affected units in the yard were placed on hold.", inf=True),
  E("April 27", "SUPPLIER_NOTICE", "On April 27, KZ received official notification via email from MORryde regarding the recall."),
  E("May 1st", "DECISION", "KZ's safety committee met on May 1st and agreed to issue a recall.")])

# 9
L["RCLRPT-25V342-8629.txt"] = ([S1NR, S2NR],
 C("SUPPORTED", "Based on a deviation from standard manufacturing processes, trucks that were built during a turn signal switch part shortage, had the steering wheel assembled out of its normal station."),
 U("NONE_MENTIONED"),
 [E("May 19, 2025", "FILER_AWARENESS", "On or around May 19, 2025, Battle Motors was notified by one of its customers, that a steering wheel was noted as being loose during a routine inspection by the operator."),
  E("", "OTHER", "During the repair process, the techician noted that no torque seal was present, indicating that the nut was not properly torqued to specification and was indeed found to be loose.", inf=True),
  E("", "OTHER", "The fleet manager had the remaining units of the same vintage inspected and found one other unit with a loose retaining nut and no torque seal.", inf=True),
  E("", "OTHER", "All other units were found to be within specification with torque seal indicating proper torque.", inf=True),
  E("", "INVESTIGATION_START", "Battle Motors reviewed the issue and determined that during the manufacturing process of the units in question a part shortage existed for the turn signal switch resulting in a deviation from standard manufactung practices, to continue production.", inf=True),
  E("", "OTHER", "Units at the factory were inspected and no defects were found, as well as a coursey units produced before and after the suspected time period with no issues found.", inf=True),
  E("", "DECISION", "As a result Battle Motors has determined that a inspection and potential retorque is necessary for the potential units involved.", inf=True)])

# 10
q10 = "AMO called the supplier of the shackle nut, Mid-States Bolt & Screw Company, to report the condition and ask for technical assistance to investigate it."
L["RCLRPT-25V468-3921.txt"] = ([S1("Name: Mid-States Bolt & Screw Company"), S2("SUPPORTED", "Mid-States Bolt & Screw Company", q10, "chronology")],
 C("SUPPORTED", "The shackle nut locking feature does not secure the axle bolt as intended."),
 U("NAMED", ["Mid-States Bolt & Screw Company"], q10, "chronology"),
 [E("May 13, 2025", "FILER_AWARENESS", "On May 13, 2025, an operator installing the axle to the trailer chassis noticed that an installed shackle nut did not lock and was able to be unsecured by hand."),
  E("", "FILER_AWARENESS", "The operator reported the condition.", inf=True),
  E("", "OTHER", q10, inf=True),
  E("May 14, 2025", "OTHER", "On May 14, 2025, a Loctite adhesive was added to the operation to secure the shackle nut to the axle bolt."),
  E("", "OTHER", "The Loctite proved effective in securing the nut to the bolt.", inf=True),
  E("", "OTHER", "VINS were recorded of when the Loctite process was incorporated in production.", inf=True),
  E("", "INVESTIGATION_START", "A review of manufacturing and supply records was conducted to identify when the suspect supply of shackle nuts was used in production.", inf=True),
  E("", "OTHER", "Based on these reviews, AMO was able to determine the potentially affected population.", inf=True),
  E("May 20, 2025", "OTHER", "On May 20, 2025, AMO contacted customers asking them to inspect trailers still in their possession to identify whether any nuts had loosened."),
  E("May 21, 2025", "OTHER", "On May 21, 2025, AMO contacted NHTSA about the proper process for reporting the potential loose nut condition."),
  E("", "OTHER", "NHTSA instructed AMO that the supplier of the nut would be responsible for any required recall actions.", inf=True),
  E("May 26, 2025", "OTHER", "On May 26, 2025, AMO consulted legal counsel about their responsibilities under the Safety Act."),
  E("May 27,2025", "INVESTIGATION_START", "On May 27,2025, a Mid-States representative visited the AMO facility and conducted inspections and testing."),
  E("June 2, 2025", "SUPPLIER_NOTICE", "On June 2, 2025, a Mid-States representative contacted AMO with the results of the inspections and testing."),
  E("", "SUPPLIER_NOTICE", "Mid-States indicated they could replicate the loose nut condition and the inability of certain nuts to remain securely locked.", inf=True),
  E("", "OTHER", "AMO continued to monitor field reports and customer reports for potential loose nuts or other indications of unsecured axles.", inf=True),
  E("July 10, 2025", "DECISION", "On July 10, 2025, AMO decided, in the abundance of cautious, to file a part 573 report to NHTSA and plans to conduct a safety recall to address the potential that nuts may become unsecured over time in service.")])

# 11
j = "January – February 2025: Grech RV seeks input from Fiamma concerning instances of inadvertent awning deployment."
jn = "June 24, 2025: Grech RV received notification from the awning supplier, Fiamma, Inc., of an incident of unintended awning deployment."
L["RCLRPT-25V491-8213.txt"] = ([S1("Name: Fiamma Inc."), S2("SUPPORTED", "Fiamma", j, "chronology")],
 C("SUPPORTED", "Torque from awning motor applied to the winch may cause damage to interior gears."),
 U("NAMED", ["Fiamma"], jn, "chronology"),
 [E("January – February 2025", "OTHER", j),
  E("January – February 2025", "SUPPLIER_NOTICE", "Fiamma denied the existence of a manufacturing defect.", j),
  E("June 24, 2025", "SUPPLIER_NOTICE", jn),
  E("June 24, 2025", "INVESTIGATION_START", "Grech reviews the circumstances of this incident and undertakes an investigation into the subject awning.", jn),
  E("July 1, 2025", "FILER_AWARENESS", "July 1, 2025: While Grech RV is conducting its review of the incident and company data, Grech receives an email inquiry from NHTSA regarding VOQ #11668764."),
  E("July 17, 2025", "OTHER", "July 17, 2025: Grech RV provides information to NHTSA in response to its email inquiry regarding VOQ #11668764."),
  E("July 23, 2025", "OTHER", "July 23, 2025: Grech RV provides additional information to NHTSA stemming from its email inquiry."),
  E("September 2023", "FILER_AWARENESS", "Grech RV has received 19 warranty claims involving alleged inadvertent awning deployment, the first of which was received in September 2023.")])

# 12
q12 = "Insufficient application of the adhesive layer between the garnish face plate and base of the molding by the supplier."
L["RCLRPT-25V493-6422.txt"] = ([S1("Name: Keumgang Chemical"), S2("INSUFFICIENT", None, q12, "cause")],
 C("SUPPORTED", q12), U("UNNAMED", [], q12, "cause"), [])

# 13
L["RCLRPT-25V497-2087.txt"] = ([S1NR, S2NR],
 C("SUPPORTED", "Vehicles in the recall population are assembled without standard wire harnesses."), U("NONE_MENTIONED"),
 [E("May 23, 2025", "FILER_AWARENESS", "On May 23, 2025, Brinkley RV received a unit for service repairs."),
  E("", "OTHER", "During the repair process, it was determined that an unsecured wire was pinched between a holding tank and an underlying support member.", inf=True),
  E("", "INVESTIGATION_START", "Upon review of this information, Brinkley RV launched an investigation to determine possible risk.", inf=True),
  E("July 24, 2025", "DECISION", "On July 24, 2025, Brinkley RV Safety Committee was presented the results of the investigation and voted unanimously to recall the affected units.")])

# 14
h1 = "8/25/2025 – Initial hose reel detachment observed in the field on one fire truck."
L["RCLRPT-25V558-2502.txt"] = ([S1("Name: Midwest Fire"), S2("INSUFFICIENT", None, "Name: Midwest Fire", "block")],
 C("NOT_REPORTED", ""), U("NONE_MENTIONED"),
 [E("8/25/2025", "FILER_AWARENESS", h1),
  E("8/25/2025", "OTHER", "Photographs and service reports were collected.", h1),
  E("8/25/2025", "FILER_AWARENESS", "8/25/2025 – Warranty/service report submitted documenting the fractured mounting plate (3/16” 5052-H32 aluminum)."),
  E("8/28/25", "INVESTIGATION_START", "8/28/25 – Engineering review initiated to assess the mounting plate design, bend radius, and potential fatigue concerns."),
  E("8/28/2025", "OTHER", "8/28/2025 – Team inspection confirmed fracture at bend radius was the failure mode, likely caused by stress concentration and vibration during service."),
  E("8/28/2025", "INVESTIGATION_START", "8/28/2025 – Broader fleet review conducted; 36 trucks identified for containment and inspection."),
  E("8/28/2025", "DECISION", "8/28/2025 – Management meeting held to determine recall action; consensus reached that defect relates to motor vehicle safety due to potential for hose reel detachment."),
  E("8/28/2025", "NHTSA_FILING", "8/28/2025 – Defect report prepared and submitted through Part 573 recall portal.")])

# 15
i1 = "6/19/2025 – International receives notice that a New York DOT inspector fails a bus due to the absence of a floor side reinforcement."
i2 = "6/24/2025 –Notwithstanding the conclusion that the bus described above did not require a reinforcement, out of an abundance of caution, International initiates a delivery stop on school buses at the Tulsa Bus Assembly Plant"
L["RCLRPT-25V580-8142.txt"] = ([S1NR, S2NR], C("NOT_REPORTED", ""), U("NONE_MENTIONED"),
 [E("6/19/2025", "FILER_AWARENESS", i1),
  E("6/19/2025", "OTHER", "Upon further review, it was determined that this bus did not require a floor side reinforcement based on its configuration.", i1),
  E("6/24/2025", "OTHER", i2),
  E("6/24/2025", "OTHER", "International identifies 10 such vehicles.", i2),
  E("6/25 - 7/7/2025", "OTHER", "6/25 - 7/7/2025 – Tulsa Bus Assembly Plant inspects the 10 buses on delivery stop, finding one bus built without the floor side reinforcement which was then added to the bus."),
  E("7/8/2025", "INVESTIGATION_START", "7/8/2025 – International reviews the findings from the DOT inspection and delivery stop inspections and determines that it will conduct a comprehensive review of bus floor plans to identify those buses, which by design, should have the reinforcement installed"),
  E("7/8/2025-8/22/2025", "INVESTIGATION_START", "7/8/2025-8/22/2025 - International conducts comprehensive bus floor plan analysis to determine which buses, by design, should have the reinforcement installed and performs a limited field inspection."),
  E("8/22/2025-8/27/2025", "INVESTIGATION_START", "8/22/2025-8/27/2025- International conducts a review of data from previous compliance tests to determine if the presence of the reinforcement was necessary to meet the force requirements of FMVSS 210 S4.2.2 and 222 S5.1.4."),
  E("8/28/2025", "DECISION", "8/28/2025 – Based on review of the information gathered in the course of the investigation, International declares a non-compliance recall.")])

# 16
w1 = "08/15/2025 - Wabash's Manufacturing team reported to the Wabash warranty team that 10 trailers left our facility with the incorrect rear impact guards installed."
w2 = "08/26/2025 - A Wabash warranty representative visited the dealer and inspected all 10 vehicles to assure the correct bumpers were properly installed."
L["RCLRPT-25V625-0070.txt"] = ([S1("Name: Wabash National"), S2("SUPPORTED", "Wabash", w1, "chronology")],
 C("SUPPORTED", "Engineering called out an incorrect rear impact guard for this vehicle configuration"), U("NONE_MENTIONED"),
 [E("08/15/2025", "FILER_AWARENESS", w1),
  E("08/15/2025", "OTHER", "These trailers were shipped to a nearby dealer.", w1),
  E("08/15/2025", "OTHER", "The dealer was notified of the situation, and the vehicles were locked down until replacement parts could be supplied.", w1),
  E("08/15/2025", "OTHER", "A concern response (CR) was entered into the system to bring awareness to the Product Safety Team, (PST).", w1),
  E("08/18/2025", "INVESTIGATION_START", "08/18/2025 - The first Concern response meeting was held, and investigations were started."),
  E("08/19/2025", "OTHER", "08/19/2025 - The cause of the manufacturing error was investigated and corrected."),
  E("08/26/2025", "OTHER", w2),
  E("08/26/2025", "OTHER", "The PST held its bi-weekly meeting and discussed.", w2),
  E("09/08/2025", "OTHER", "09/08/2025 - During the bi-weekly safety meeting, the PST evaluated this condition as a potential FMVSS 224 noncompliance and voted to escalate the situation to the Product Safety Committee (PSC)"),
  E("09/12/2025", "DECISION", "09/12/2025 - Although all the subject vehicles were remedied prior to delivery to owners, the PSC voted to declare this condition as an FMVSS 224 noncompliance and to submit this 573-noncompliance report.")])

# 17
k3 = "09/30/2025 International completes weighing of buses."
k4 = "10/1/2025-10/29/2025 International updates the weight estimator with the information obtained from the verification activities."
L["RCLRPT-25V783-5866.txt"] = ([S1NR, S2NR], C("NOT_REPORTED", ""), U("NONE_MENTIONED"),
 [E("09/22/2025", "FILER_AWARENESS", "09/22/2025 International identifies a condition where school buses, when loaded as per 49 CFR Part 567.4 (g)(3), might exceed the value printed on the label and opens an investigation into the issue."),
  E("09/23/2025-09/29/2025", "INVESTIGATION_START", "09/23/2025-09/29/2025 International identifies buses to be weighed across multiple configurations to study weight estimate accuracy."),
  E("09/30/2025", "OTHER", k3),
  E("09/30/2025", "OTHER", "Upon physical weight verification, International determines that buses were found to be lighter than the initial estimated weight.", k3),
  E("10/1/2025-10/29/2025", "OTHER", k4),
  E("10/1/2025-10/29/2025", "INVESTIGATION_START", "Additional physical bus weight verification audits were conducted to further refine the accuracy of the weight estimator across additional configurations.", k4),
  E("10/1/2025-10/29/2025", "OTHER", "Necessary adjustments to weight estimator were completed based on these audits.", k4),
  E("10/31/2025", "DECISION", "10/31/2025 International determines certain bus configurations, when loaded as per 49 CFR 567.4(g)(3), could exceed the recorded Gross Vehicle Weight Rating (GVWR) printed on the label."),
  E("11/06/2025", "OTHER", "11/06/2025 International finalizes the suspect population."),
  E("11/06/2025", "DECISION", "11/06/2025 International declares a safety recall."),
  E("02/24/2026", "OTHER", "02/24/2026 International finalizes recall remedy"),
  E("03/17/2026", "OTHER", "03/17/2026 International finalizes remedy launch date")])

# 18
m4 = "Since vehicles built at Micro Bird USA LLC are manufactured with the same material and procedures as those built by Corporation Micro Bird Inc., it was decided on December 2, 2025, to recall the vehicles equipped with a Spheros air conditioning system,"
L["RCLRPT-25V843-5844.txt"] = ([S1("Name: Spheros North America Inc"), S2("SUPPORTED", "Spheros", m4, "chronology")],
 C("NOT_REPORTED", ""), U("NAMED", ["Spheros"], m4, "chronology"),
 [E("October 2025", "FILER_AWARENESS", "Following reports in October 2025 regarding localized heat damages to the air conditioning control in a vehicle manufactured in March 2025 by Corporation Micro Bird Inc. in Drummondville, an investigation was launched to determine the source of the incidents."),
  E("September 23, 2024", "FILER_AWARENESS", "It was then discovered that a claim for heat damages had been submitted in September 23, 2024, for similar circumstances."),
  E("", "OTHER", "It was determined, from the location of the damages on the board for the March 2025 vehicle, that the connection between the power cable and the power stud becoming loose was probably the cause of the damages and fire incidents.", inf=True),
  E("December 2, 2025", "DECISION", m4)])

# 19
l2 = "12/15/2025 – Investigation opened."
L["RCLRPT-26E004-0495.txt"] = ([S1("Name: Lippert"), S2("SUPPORTED", "Lippert", "Quality inspection and containment done at all Lippert manufacturing facilities of the windows for Blue Bird.", "chronology")],
 C("SUPPORTED", "During production, the DOT etching was not applied with sufficient depth, resulting in the designator being illegible."),
 U("NONE_MENTIONED"),
 [E("12/15/2025", "FILER_AWARENESS", "12/15/2025 – Report was made by Blue Bird Corporation Busses after a bus was inspected at the border and found the DOT designator on a window illegible."),
  E("12/15/2025", "INVESTIGATION_START", l2),
  E("12/15/2025", "OTHER", "Quality inspection and containment done at all Lippert manufacturing facilities of the windows for Blue Bird.", l2),
  E("12/16/20205", "OTHER", "12/16/20205 –Quality inspection begins at Blue Bird facility."),
  E("1/6/2026", "INVESTIGATION_START", "1/6/2026 – Investigation opened to determine scope and range of components."),
  E("1/15/2026", "OTHER", "1/15/2026 – Investigation concluded."),
  E("1/16/2026", "NHTSA_FILING", "1/16/2026 – Recall Filed."),
  E("2/18/2026", "NHTSA_FILING", "2/18/2026 – Updated Remedy")])

# 20
p_c = "Prevost sold driver-side exterior rearview mirrors in the aftermarket that were outside of design specifications."
p1 = "September 2025 Prevost was informed by the supplier that certain driver-side rearview mirrors were potentially manufactured with dimensions not meeting the required specifications."
p2 = "November 2025 Rearview mirrors exhibiting abnormal play were identified during Prevost vehicle production."
p3 = "2026-02-03 Case was presented on Volvo Product Safety Evaluation Committee (PSEC) to evaluate if there is a potential safety-related issue."
p4 = "2026-02-04 Testing activities were completed."
p5 = "2026-02-06 Case was presented on Volvo Product Safety Evaluation Committee (PSEC) to evaluate if there is a potential safety-related issue."
p6 = "2026-02-12 Case was presented to Volvo Product Safety Committee (PSC)."
L["RCLRPT-26E008-5432.txt"] = ([S1("Name: Prevost"), S2("SUPPORTED", "Prevost", p_c, "cause")],
 C("SUPPORTED", p_c), U("UNNAMED", [], p1, "chronology"),
 [E("September 2025", "SUPPLIER_NOTICE", p1),
  E("November 2025", "FILER_AWARENESS", p2),
  E("November 2025", "INVESTIGATION_START", "An internal Prevost investigation was opened to identify the root cause and to determine if the issue is potentially safety related.", p2),
  E("2025-12-15", "INVESTIGATION_START", "2025-12-15 Prevost initiated durability testing of the subject driver-side exterior rearview mirrors."),
  E("2026-02-03", "OTHER", p3),
  E("2026-02-03", "OTHER", "It was concluded that further investigation was required to complete the assessment.", p3),
  E("2026-02-04", "OTHER", p4),
  E("2026-02-04", "OTHER", "Analysis of the results indicated that the dimensional variation may increase the risk of mirror detachment.", p4),
  E("2026-02-06", "OTHER", p5),
  E("2026-02-06", "OTHER", "Decision made to raise the potential safety-related issue to Volvo Product Safety Committee (PSC) for review and determination.", p5),
  E("2026-02-12", "OTHER", p6),
  E("2026-02-12", "DECISION", "It was concluded that there was a safety-related defect, and that a recall is needed.", p6),
  E("2026-02-19", "NHTSA_FILING", "2026-02-19 Defect Information Report submitted to authorities.")])

# 21
d2 = "March 2025 - January 2026 - Internal analysis at Daimler Buses to determine the cause and the remedy."
dq = "Clarification with the supplier regarding which delivery batches are affected."
L["RCLRPT-26V063-7895.txt"] = ([S1("Name: ZF CV Distribution Germany GmbH & Co. KG"), S2("INSUFFICIENT", None, dq, "chronology")],
 C("SUPPORTED", "An excessively large bore diameter in a component of the door control valve."),
 U("UNNAMED", [], dq, "chronology"),
 [E("March 24, 2025", "FILER_AWARENESS", "March 24, 2025 - Defect detection by internal quality controls."),
  E("March 2025 - January 2026", "INVESTIGATION_START", d2),
  E("March 2025 - January 2026", "OTHER", dq, d2),
  E("March 2025 - January 2026", "INVESTIGATION_START", "Investigation of the affected vehicles.", d2),
  E("January 29, 2026", "DECISION", "January 29, 2026 - Daimler Buses GmbH decided a recall regarding this issue at Mercedes-Benz Tourrider Business and Tourrider Premium coaches.")])

# 22
r1 = "2025-12-01 One improperly installed passenger seat anchorage was identified during an internal Prevost production audit."
r6 = "2026-01-14 Case was presented on Volvo Product Safety Evaluation Committee (PSEC) to evaluate if there is a potential safety-related issue."
r8 = "2026-01-22 Final internal inspection results were obtained."
r10 = "2026-02-03 Case was presented on Volvo Product Safety Evaluation Committee (PSEC) to evaluate if there is a potential safety-related issue."
r12 = "2026-02-12 Case was presented to Volvo Product Safety Committee (PSC)."
wc = "Two warranty claims potentially related to this issue were received on November 18 and December 18, 2025."
L["RCLRPT-26V093-5181.txt"] = ([S1("Name: Prevost"), S2("SUPPORTED", "Prevost", r1, "chronology")],
 C("SUPPORTED", "The seat installation process was not revised to reflect changes associated with the seat design, which may have resulted in improper anchorage installation."),
 U("NONE_MENTIONED"),
 [E("2025-12-01", "FILER_AWARENESS", r1),
  E("2025-12-02", "INVESTIGATION_START", "2025-12-02 Internal Prevost investigation was opened to identify the root cause and to determine if the issue is potentially safety-related."),
  E("2025-12-10", "INVESTIGATION_START", "2025-12-10 An internal inspection was initiated on a sample of vehicles to assess whether the audit finding was an isolated occurrence."),
  E("2025-12-22", "OTHER", "2025-12-22 Preliminary results of the internal inspection were obtained."),
  E("2026-01-14", "OTHER", r6),
  E("2026-01-14", "OTHER", "It was concluded that further investigation was required to complete the assessment.", r6),
  E("2026-01-22", "OTHER", r8),
  E("2026-01-22", "OTHER", "Approximately 8% of the inspected vehicles had at least one improperly installed seat anchorage.", r8),
  E("2026-02-03", "OTHER", r10),
  E("2026-02-03", "OTHER", "Decision made to raise the potential safety-related issue to Volvo Product Safety Committee (PSC) for review and determination.", r10),
  E("2026-02-12", "OTHER", r12),
  E("2026-02-12", "DECISION", "It was concluded that there was a safety-related defect, and that a recall is needed.", r12),
  E("2026-02-17", "NHTSA_FILING", "2026-02-17 Defect Information Report submitted to authorities."),
  E("November 18", "FILER_AWARENESS", wc),
  E("December 18, 2025", "FILER_AWARENESS", wc)])

# 23
L["RCLRPT-26V105-2893.txt"] = ([S1("Name: DAS North America"), S2("INSUFFICIENT", None, "Name: DAS North America", "block")],
 C("SUPPORTED", "Improperly manufactured front seatback recliner."), U("NOT_REPORTED"), [])

out = []
errs = []
for fn in sorted(L):
    fl, sec = sections(fn)
    claims, cause, up, events = L[fn]
    obj = {"file": fl, "claims": claims, "cause": cause, "upstream": up, "events": events}
    out.append(obj)
    def chk(q, s, what):
        if not q: return
        if len(q) > 300: errs.append((fn, what, "len", len(q)))
        if norm(q) not in sec[s]: errs.append((fn, what, "notfound", q[:80]))
    for c in claims: chk(c["quote"], c["section"], c["id"])
    chk(cause["quote"], "cause", "cause")
    if up["quote"]: chk(up["quote"], up["section"], "upstream")
    for i, e in enumerate(events):
        chk(e["quote"], "chronology", "ev%d" % i)
        if e.get("entry_quote"):
            chk(e["entry_quote"], "chronology", "entry%d" % i)
            if e["date_text"] not in e["entry_quote"]: errs.append((fn, i, "date not in entry"))
        elif e["date_text"] and e["date_text"] not in e["quote"]:
            errs.append((fn, i, "date not in quote"))
missing = set(f for f in os.listdir(os.path.join(D, "texts")) if f.startswith("RCLRPT")) - set(L)
print("missing", missing)
print("errors", errs)
json.dump(out, open(os.path.join(D, "passB.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), sum(len(o["events"]) for o in out))
