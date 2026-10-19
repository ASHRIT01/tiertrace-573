import json
D=[
("D001","X","In March 2024, the supplier identified a deviation in the production process of the welding material was causing the observed deviation","The welding-material supplier reports its finding (root cause and affected batch) to MBAG: a supplier finding = SUPPLIER_NOTICE."),
("D002","Y","Based on this determination from April through August 2024, MBAG analyzed the potential effects of the suspect welding material on the integral carrier. These analyses included thorough material testing and simulations.","Analysis/testing conducted to determine effects and scope = INVESTIGATION_START."),
("D003","Y","GM’s investigation identified 272 potentially related field complaints, which were received by GM between May 5, 2024, and August 15, 2024.","May 5-Aug 15 only bounds the data window of complaints; it is not an event date, so no Aug 15-dated event."),
("D004","NEITHER","On September 17, 2024, a driver delivering a completed unit to a customer experienced a thermal event during the trip.","The dated sentence reports an occurrence, so the event exists (null is wrong); but the sentence itself does not report a notice reaching the filer (that is the next, undated sentence), so the type is OTHER."),
("D005","X","On October 9, 2024, during a routine Standards Manager Inspection of the plant, the Standards Manager found the manufacturing plant had more than the single unit affected.","Internal inspection/audit finding reaching the filer = FILER_AWARENESS."),
("D006","X","On October 15, 2024, it was discovered that manufacturing had been installing the washer prep without the anti-siphon vent consistently.","Rules list 'discovered' as FILER_AWARENESS."),
("D007","Y","On October 18, 2024. Forest River's Corporate Committee voted to recall.","The dated fragment alone reports no action; the dated item is the vote to recall = DECISION."),
("D008","CONTESTED","09-24-24: Cummins’ 573 filed with NHTSA; copy provided to Kenworth S&C.","Rules list 'a supplier's own filing' as OTHER but also 'received a recall notice from X'/supplier tells filer of its own recall as SUPPLIER_NOTICE; this sentence reports both."),
("D009","X","The cause of the issue is currently under continued investigation.","Cause not yet known = INSUFFICIENT."),
("D010","X","Two cases were reported as accidents with the loss of the respective wheels but without any deaths or injuries (Sept. 23rd & Oct. 15th).","Reports of incidents reaching Porsche = FILER_AWARENESS."),
("D011","Y","Two cases were reported as accidents with the loss of the respective wheels but without any deaths or injuries (Sept. 23rd & Oct. 15th).","Reports of incidents reaching Porsche = FILER_AWARENESS."),
("D012","Y","March 2020 – January 2021 Honda received quality reports of the issue and began to investigate.","The sentence first reports receipt of quality reports (first awareness); investigating follows from it. FILER_AWARENESS is the primary action."),
("D013","X","February 2022 – August 2022 Honda received additional reports and began to reanalyze and investigate the issue","Receipt of additional reports = later FILER_AWARENESS; kept consistent with D012 (primary action is receipt)."),
("D014","Y","Honda continued to investigate the issue.","Investigation conducted (continued) counts as INVESTIGATION_START ('opened, started or conducted')."),
("D015","Y","In October of 2024, the instrument panel engineering team conducted a read-across for label releases, which revealed that the release issue started with the 2020MY Explorer and Aviator launch","Read-across analysis conducted to determine scope = INVESTIGATION_START; Y's quote is cut at an ' and ' clause boundary."),
("D016","Y","Concern was related to a crease in the pad, that caused a short circuit.","Description of the concern with no action or occurrence; not an event."),
("D017","NEITHER","From August 2023 throughout November 2023, after various discussions and testing performed by the software supplier, the supplier itself stated that","Supplier stating its finding to the filer is an event of type SUPPLIER_NOTICE (not OTHER); date is the written range."),
("D018","X","On November 22, 2023, at Vehicle Regulation Committee (VRC), Maserati spA decided, based on supplier’s statement to put the investigation in monitoring status","Dated action (committee decision to monitor, not a recall decision) is an event of type OTHER."),
("D019","Y","FCA US TSRC held regular meetings with FCA US Engineering and Supplier Quality to understand all potential failure modes","'Supplier Quality' is an internal FCA US department, not a supply-chain party; narrative names no supplier, cause is NR."),
("D020","X","On October 09, 2024, the FCA US TSRC organization recognized a front seat SAB squib connector issue existed on certain vehicles related to improper securement of the connectors","Filer recognizing/becoming aware of the specific squib connector issue = FILER_AWARENESS (decision to recall came later)."),
("D021","NEITHER","From October 2023, through September 2024, FCA US TSRC held regular meetings with FCA US Engineering and Supplier Quality to understand all potential failure modes of the issue and determine the suspect population.","Event exists and is an investigation of cause/scope (INVESTIGATION_START), but date_text should be the written range, not just its start."),
("D022","Y","11/25/2024 – Keystone Safety Committee reviewed the information and concluded that the data reviewed indicated a unanimous vote for a voluntary recall.","Committee vote for recall = DECISION."),
("D023","Y","Investigation called for to determine affected unit range.","Investigation opened to determine scope = INVESTIGATION_START."),
("D024","X","While the vehicle is in motion, passengers wearing the seat belts may experience the seat belt is delayed in retracting.","Cause field describes only the symptom, no cause or mechanism; not SUPPORTED."),
]
corr={
"D004":{"date_text":"September 17, 2024","type":"OTHER","quote":"On September 17, 2024, a driver delivering a completed unit to a customer experienced a thermal event during the trip.","inherited_date":False,"date_inferred":False},
"D017":{"date_text":"August 2023 throughout November 2023","type":"SUPPLIER_NOTICE","quote":"From August 2023 throughout November 2023, after various discussions and testing performed by the software supplier, the supplier itself stated that “although Maserati Grecale and Granturismo software contains the deviation","inherited_date":False,"date_inferred":False},
"D021":{"date_text":"October 2023, through September 2024","type":"INVESTIGATION_START","quote":"From October 2023, through September 2024, FCA US TSRC held regular meetings with FCA US Engineering and Supplier Quality to understand all potential failure modes of the issue and determine the suspect population.","inherited_date":False,"date_inferred":False},
}
out=[]
for i,d,q,r in D:
    o={"item_id":i,"decision":d,"quote":q,"reason":r}
    if i in corr:o["corrected"]=corr[i]
    out.append(o)
json.dump(out,open("decisions.json","w"),ensure_ascii=False,indent=1)
