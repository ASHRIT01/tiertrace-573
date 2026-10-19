import json
A="April – June 2025 On April 15, 2025, Ford’s Product Development Quality team identified a loose C-Pillar applique on an internal test vehicle."
D=[
("D001","X","On April 15, 2025, Ford’s Product Development Quality team identified a loose C-Pillar applique on an internal test vehicle.","Sentence has its own date (April 15, 2025); internal discovery of the problem is FILER_AWARENESS, not OTHER."),
("D002","Y","CCRG reviewed field and warranty data, and potential for occurrence at higher mileages in the future via statistical projections.","Undated sentence inside the 'April – June 2025' entry inherits that date; review of field/warranty data and projections is analysis of scope (INVESTIGATION_START). X types the April 15 discovery as OTHER, which is wrong."),
("D003","Y","On April 22, 2025, this issue was brought to Ford’s CCRG for review.","Issue already known to Ford; bringing it to the review group opens a review/investigation (INVESTIGATION_START) rather than a new report reaching the filer."),
("D004","Y","Throughout May 2025, CCRG and Ford’s engineering teams worked to better understand the factors that lead to the detachment","Y's quote is verbatim (X drops 'Throughout'); work to understand the factors leading to detachment is cause analysis (INVESTIGATION_START)."),
("D005","X","Supplier process improvement actions were reviewed by Ford’s Supplier Technical Assistance team to assist in determining suspect population scoping.","Review conducted to determine population scope is INVESTIGATION_START; the entry is 'April – June 2025' (the 'Throughout May 2025' sentence does not begin with a date, so it does not start a new entry). Y uses a May 2025 entry and OTHER."),
("D006","Y","The investigation also included a new assessment of the risk factors that considered recent road hazard safety recalls","Undated sentence in the 'April – June 2025' entry; risk assessment conducted as part of the investigation is INVESTIGATION_START. X uses a non-existent May 2025 entry and OTHER."),
("D007","Y","This conclusion was based on the assessment that the involved parts did not represent a significant risk while falling to the ground","Explains the basis of an earlier conclusion; a description/rationale with no new action, so not an event."),
("D008","NEITHER","The investigation also included a new assessment of the risk factors that considered recent road hazard safety recalls","The event exists, but it inherits the 'April – June 2025' entry date (no entry begins with 'May 2025'; the sentence reads 'Throughout May 2025') and is INVESTIGATION_START."),
("D009","X","These warranty claims were received between June 17, 2020, and April 14, 2025.","Status/data-window statement that bounds the warranty claim count, not an action; no event."),
("D010","X","On October 6, 2023, Ford’s Field Review Committee approved field action 23V687 (23S56)","Approval of a field action is the decision to recall (DECISION)."),
("D011","Y","The original 23S56/23V687 recall population erroneously used a population cutoff point of May 24th, 2022.","Production cutoff date bounding the population; a description, not an action, so no event."),
("D012","Y","These claims were received between October 6, 2022 and February 17, 2025.","Data window for a status count of claims; not an event."),
("D013","X","Oshkosh begins to evaluate this condition to understand whether the wrinkling is limited to the vehicles observed at the Oshkosh facility or may exist in other vehicles","Start of an evaluation to determine scope is INVESTIGATION_START."),
("D014","Y","Oshkosh begins to focus on the thickness of the sun visor labels, the adhesive on them, and the surface material of the sun visor.","Main action is the start of focused analysis of the labels to find the cause (INVESTIGATION_START)."),
("D015","Y","Attention is given to their ability to remain permanently attached to the sun visor after installment.","Analysis conducted as part of the investigation into the cause; INVESTIGATION_START (opened or conducted)."),
("D016","Y","all labels present on the sun visor including the rollover warning label and electric shock warning label present on the BEV version of the vehicles, and their placement, are evaluated.","Evaluation of labels and placement is analysis conducted to determine cause/scope (INVESTIGATION_START)."),
("D017","X","In October 2023, a test program was initiated in order to determine the specific parameters of the assembly process for possible revision","Stated purpose is to define revised assembly parameters (a production/process change), not to find the cause or scope; OTHER."),
("D018","Y","As part of this process, in January 2024, information from field vehicles would start to be collected and analyzed on a continual basis.","Field data collection and analysis to evaluate module performance (scope/risk) is analysis started, INVESTIGATION_START."),
("D019","Y","The process would continue for all modules produced up to June 2024, as updated parameters would not be defined until that time.","June 2024 bounds a production window; the sentence describes the scope of a process, no action on that date; not an event."),
("D020","Y","MBAG investigated and evaluated each reported incident to determine the cause and its impact until February 2024.","Investigation conducted to determine the cause is INVESTIGATION_START."),
("D021","Y","From August 2024, a risk assessment and a detailed temperature simulation were carried out in cooperation with the supplier","The filer and supplier jointly carried out analysis; the supplier is not telling the filer about the problem, so INVESTIGATION_START, not SUPPLIER_NOTICE."),
("D022","Y","Starting in February 2025, further failure mechanisms were evaluated","Evaluation of failure mechanisms is analysis to determine cause/consequence (INVESTIGATION_START)."),
("D023","Y","during April 2025, MBAG analyzed the sequence of events that could lead to driving impairments resulting from unsuitable screws.","Analysis conducted (INVESTIGATION_START)."),
("D024","X","During 2023, MBAG received isolated reports of complaints in the field regarding different allegations (e.g., warning messages).","Field complaint reports reaching the filer, with its own date 2023: a FILER_AWARENESS event exists."),
]
out=[]
for i,d,q,r in D:
    o={"item_id":i,"decision":d,"quote":q,"reason":r}
    if i=="D008":
        o["corrected"]={"date_text":"April – June 2025","type":"INVESTIGATION_START","quote":"The investigation also included a new assessment of the risk factors that considered recent road hazard safety recalls and continued discussions with NHTSA on road hazard risks.","inherited_date":True,"entry_quote":A,"date_inferred":False}
    out.append(o)
json.dump(out,open("decisions.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
