import json
D=[]
def a(i,d,q,r,c=None):
    o={"item_id":i,"decision":d,"quote":q,"reason":r}
    if c: o["corrected"]=c
    D.append(o)
q1="From September 2022, through January 2023, FCA US TSRC reviewed vehicle records and met with FCA US engineering to review supplier data to understand the condition."
a("D001","NEITHER",q1,"Reviewing records/supplier data to understand the condition is analysis conducted to find the cause -> INVESTIGATION_START (X's type). But a range gives one event per distinct date, so this event's date_text is 'September 2022' (Y's date), not the whole range.",
  {"date_text":"September 2022","type":"INVESTIGATION_START","quote":q1,"inherited_date":False,"date_inferred":False})
a("D002","X","On January 18, 2023, FCA US TSRC recognized that the TRSCM may fail internally resulting in the rearview camera image not displaying during a backing event","The filer recognizing (becoming aware of) the potential noncompliance is FILER_AWARENESS, not OTHER.")
a("D003","Y","No known warranty claims, field or service reports, or any vehicle crashes/injuries. Only two internal failures at the manufacturing facility in Lyons Station, PA","Status statement summarising failures, not an action/occurrence; not an event.")
a("D004","Y","On February 6, 2023, Outfitter Manufacturing contacted all 78 consumers affected by the Suburban Manufacturing recall notice.","Contacting affected owners is remedy logistics (owner notification), excluded from events.")
a("D005","X","On March 15, 2023, Autocar obtained new information from the operator-customer regarding a January 2019 incident","A customer report reaching the filer is FILER_AWARENESS.")
a("D006","Y","This new information led Autocar to believe the January 2019 incident may have been related to the recalled condition.","Belief statement; rules exclude beliefs and assumptions from events.")
a("D007","Y","January 31, 2020, Autocar was contacted by NHTSA regarding potential plumbing attached to the exhaust port of any PP1 park brake valves and inquired as to any reported roll-away events. Autocar researched the potential condition on its vehicles","The entry begins with a date (no 'On'), so the following undated research sentence inherits January 31, 2020; researching the condition is INVESTIGATION_START.")
a("D008","X","In or about August 2022, investigation reviews installation records from Winnebago assembly technicians and found no concern;","Reviewing records as part of the investigation is investigation/analysis conducted -> INVESTIGATION_START; Y's quote also spans another entry.")
a("D009","X","October 2022, Winnebago identified a social media post where a consumer had identified a propane gas leak on a Suburban SDS2 cook top","The dated October 2022 sentence is a consumer report reaching the filer -> FILER_AWARENESS. Y's version is a different sentence (attempted part return), which is a separate OTHER event, not this one.")
a("D010","X","In or about January 2023, Winnebago continued to search for and analyzed any claim or complaint concerning SDS2 cooktops;","Analysis of claims conducted to determine scope -> INVESTIGATION_START; Y's quote merges two entries.")
a("D011","Y","January 26, 2023 Suburban sent Winnebago notice that Winnebago was impacted by 22E-035","The sentence's dated occurrence is the supplier telling the filer about its recall -> SUPPLIER_NOTICE (the decision follows from it); X's quote also spills into the next entry ('February 2, 2023'), so it is not a clean one-sentence quote.")
a("D012","Y","February 2, 2023, after working with Suburban Manufacturing Company to determine scope of impacted units, Winnebago filed a notice of defect with NHTSA.","Filing the defect notice with NHTSA is NHTSA_FILING; X's quote is the wrong sentence.")
a("D013","X","April 28, 2022, Suburban Manufacturing Co. issued recall 22E-035 specifically for Escape RV;","A supplier issuing its own recall is an occurrence (OTHER: a supplier's own filing); it is an event.")
a("D014","Y","A machine that is not forming the roof bow supports correctly is currently under investigation for root cause.","The cause field states a mechanism (machine not forming roof bow supports correctly); only the deeper root cause of the machine fault is open, so SUPPORTED.")
a("D015","Y","01/19/2023 and 01/20/2023 – Navistar Manufacturing audits the processes from bow former through topping sheet installation.","Auditing the processes to find the cause is investigation/analysis conducted -> INVESTIGATION_START.")
a("D016","Y","01/19/2023 and 01/20/2023 – Navistar Manufacturing audits the processes from bow former through topping sheet installation.","Same as D015: process audit is INVESTIGATION_START.")
a("D017","X","In January 2023, the review indicated that the supplier of the hand brake lever involved in the subject recall was provided with specifications which were insufficient.","The narrative refers to the lever supplier only generically; 'BMW' in the narrative is the filer acting, not a naming of the supplier -> INSUFFICIENT.")
a("D018","Y","In January 2023, the review indicated that the supplier of the hand brake lever involved in the subject recall was provided with specifications which were insufficient.","This is a finding of BMW's own review, not the supplier telling the filer; a review result is OTHER, not SUPPLIER_NOTICE.")
a("D019","X","On February 14, 2023, an issue pertaining to 2023 model year Ford Maverick trailer tow taillamp function was brought to Ford’s Critical Concern Review Group for review.","A report of the issue reaching the filer's review group is FILER_AWARENESS.")
a("D020","Y","In March 2023, Ford notified Jayco that remedy parts are available.","Notice of remedy part availability is not a notice about the problem/finding/recall; it is an OTHER occurrence.")
a("D021","Y","on June 23, 2023, DTNA updated the description of the remedy section of its Defect Information Report.","Updating the Defect Information Report is amending the Part 573 report -> NHTSA_FILING.")
q22="Mid-February 2023, DTNA received a report on an incident involving failed tie rod assembly and opened a preliminary investigation."
a("D022","NEITHER",q22,"The event exists (Y's null is wrong), but date_text must keep 'Mid' as written: 'Mid-February 2023', not 'February 2023'.",
  {"date_text":"Mid-February 2023","type":"INVESTIGATION_START","quote":q22,"inherited_date":False,"date_inferred":False})
a("D023","Y","On May 26, 2023, DTNA amended the Defect Information Report to clarify and consolidate the model listing","Amending the Part 573 report is an NHTSA_FILING event.")
a("D024","CONTESTED","An engineering review was initiated and, on March 21st, the seat supplier was contacted.","One sentence holds both an investigation start (undated) and a dated supplier contact (OTHER); rules give one event per sentence but do not settle which action sets the type.")
json.dump(D,open("decisions.json","w"),indent=1,ensure_ascii=False)
