import json
K="RCLRPT-25V598-1713"
DAYREASON=("Each KTM chronology line begins with a day number ('20. Jan 2023', '01. Feb 2024'; days rise within a month: 10/11/13 Feb, 02/03/05/11 Sept 2025), "
 "so the date as written is the day-prefixed form and the trailing numbers in the versions' quotes belong to the next line's date.")
def ev(d,t,q,inh=None):
    e={"date_text":d,"type":t,"quote":q,"inherited_date":bool(inh),"date_inferred":False}
    if inh: e["entry_quote"]=inh
    return e
E1="20. Jan 2023: Start of KTM internal investigation."
D=[]
def add(i,dec,q,r,c=None):
    x={"item_id":i,"decision":dec,"quote":q,"reason":r}
    if c is not None: x["corrected"]=c
    D.append(x)
add("D044","NEITHER",E1,"Event exists (investigation started) as Y says, but date_text must be '20. Jan 2023'. "+DAYREASON,ev("20. Jan 2023","INVESTIGATION_START",E1))
q="Coordination, root cause analysis & testing with manufacturer and supplier"
add("D045","NEITHER",q,"Undated sentence inside the 20. Jan 2023 entry: an event. Root cause analysis & testing is INVESTIGATION_START, not OTHER; quote must not include the next line's '01.'; entry date is '20. Jan 2023'.",ev("20. Jan 2023","INVESTIGATION_START",q,E1))
for i,d,t,body,why in [
 ("D046","01. Jan 2024","OTHER","100% camera base inspection to check PCBA after conformal coating","Production/containment action is an OTHER event (X right that it exists)"),
 ("D047","01. Feb 2024","OTHER","Automatic Cleaning of circuit board after PCBA & wire terminal soldering","Production change is an OTHER event (Y right that it exists)"),
 ("D048","18. Sept 2024","FILER_AWARENESS","First contact of Transport Canada regarding consumer report to TC","Regulator contacting KTM about a consumer report is a notice of the problem reaching the filer: FILER_AWARENESS, not OTHER"),
 ("D049","25. Sept 2024","INVESTIGATION_START","Vehicle inspection of reported vehicle","Inspection of the reported vehicle is testing conducted to find the cause: INVESTIGATION_START, not OTHER"),
 ("D050","03. Oct 2024","INVESTIGATION_START","Transport Canada starts investigation","An investigation is opened: INVESTIGATION_START (X right on existence and type)"),
 ("D051","10. Feb 2025","FILER_AWARENESS","Transport Canada informs KTM about two additional reports","Later reports reaching the filer are FILER_AWARENESS, not OTHER"),
 ("D052","11. Feb 2025","OTHER","Transport Canada request warranty claim data.","Regulator request is an OTHER event (Y right that it exists)"),
 ("D054","13. Feb 2025","OTHER","Meeting Transport Canada and KTM NA","Meeting is an OTHER event (X right that it exists)"),
 ("D055","06. Mar 2025","OTHER","Data shared with Transport Canada","Action, OTHER event (Y right that it exists)"),
 ("D056","07. July 2025","OTHER","Meeting request from Transport Canada","Occurrence, OTHER event (X right that it exists)"),
 ("D057","02. Sept 2025","OTHER","Meeting KTM HQ with Transport Canada","Meeting, OTHER event (X right that it exists)"),
 ("D058","03. Sept 2025","DECISION","KTM HQ determination that a recall is needed","Decision to recall: DECISION (Y right on existence and type)"),
 ("D059","05. Sept 2025","OTHER","Notice of Defect filed with Transport Canada","Filing with Transport Canada is not a Part 573 NHTSA filing; OTHER event (Y right that it exists)"),
]:
    qq=f"{d}: {body}"
    add(i,"NEITHER",qq,why+"; but date_text/quote are wrong. "+DAYREASON,ev(d,t,qq))
add("D053","X","13. Feb 2025: Meeting Transport Canada and KTM NA","'13.' is the day of the next line's date (13. Feb 2025), not a sentence; no event.")
D.sort(key=lambda x:x["item_id"])
add("D060","X","On September 4, 2025 DTNA decided to conduct a safety recall to address affected vehicles.","Rules: an acronym of the block company counts ('DTNA' for 'Daimler Trucks North America'); narrative names DTNA, so SUPPORTED.")
add("D061","CONTESTED","09/15/2025      International places a quality hold on all suspect wiper modules at its Parts Distribution Centers","The two versions are different chronology entries (09/15 quality hold = OTHER; 09/05-09/17 inspection finding suspect modules = scope inspection). Each is reasonably typed for its own entry; the paired comparison is not settled by the rules.")
add("D062","Y","03/17/2025      Initial analysis did not indicate a specific trend.","Reports an initial analysis conducted to find the cause/scope: INVESTIGATION_START.")
add("D063","Y","International again reviewed the content of the field service report and conducted further assessment of the issue.","Further assessment conducted to find cause/scope: INVESTIGATION_START.")
add("D064","X","08/26/2025     A review of warranty data finds approximately 20 claims ,16 of which had occurred after the initial field service report.","Warranty claims found by the filer are a later report of the problem reaching it: FILER_AWARENESS.")
add("D065","X","Vehicles referenced in the field service report were repaired.","Repair of affected vehicles is remedy logistics, not an event.")
add("D066","Y","Some claims mentioned audible air leaks.","Description of claim content with no action; not an event.")
add("D067","CONTESTED","Rubbing of an air line was noted on the tire and fender.","'was noted' could be a finding (event) or a description of the warranty claims' content (not an event); rules do not settle it.")
add("D068","X","Production variances due to quality control at supplier including thinner than nominal wiring gauge.","Chronology is a pointer, but the cause (part of the narrative) refers to the supplier generically: UNNAMED.")
json.dump(D,open("decisions.json","w"),indent=1,ensure_ascii=False)
