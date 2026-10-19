import json
D=[
("D025","Y","From August 10, 2026 – August 21, 2026, Tesla reviewed production torque records and video footage as well as vehicle test and repair records to further assess vehicle production","Review of records to assess affected production is analysis conducted to find scope: INVESTIGATION_START, not OTHER. Date difference (range vs start) not the disputed point."),
("D026","Y","to further assess vehicle production between July 26, 2026, and August 7, 2026.","August 7 here only bounds a production data window; not an event date, so no event."),
("D027","CONTESTED","From March 2026 through May 2026, FCA US TSRC met with FCA US Engineering to understand potential root cause, customer consequence and vehicle scope.","Rules list meetings under OTHER, but the meetings are held to find root cause and scope (INVESTIGATION_START); rules do not settle which governs."),
("D028","Y","On August 5, 2026, FCA US TSRC organization recognized that a vehicle build issue existed on certain vehicles related to the brake pedal position sensor","Dated action (internal finding/recognition of the issue) is an event; FILER_AWARENESS fits."),
("D029","X","From June 2026 through August 2026, FCA US TSRC conducted analysis of additional field records and customer assistance records to verify affected components and vehicle scope.","Dated sentence reporting analysis conducted to find scope is an event (INVESTIGATION_START)."),
("D030","X","On August 24, 2026, Forest River's Corporate Standards Manager went to the plant to look into the concern and inspect units on hand.","Going to look into the concern and inspect units is an investigation conducted: INVESTIGATION_START."),
("D031","Y","28-APR-2026: Hiab received a report of a second field failure. The issue was escalated for further investigation.","Y correctly labels the undated sentence inside the 28-APR-2026 entry as an inherited INVESTIGATION_START. X has wrong date_text (APR-2026 instead of 28-APR-2026) and SUPPLIER_NOTICE does not fit a field report received by Hiab."),
("D032","NEITHER","5-May-2026: The issue was elevated to","Elevation to leadership is a dated action (OTHER), so the event exists, but date_text must be written exactly as '5-May-2026', not 'May-2026'."),
("D033","X","28-APR-2026 through 5-May-2026: The investigation observed broken deck pins in the field failures.","Dated entry reporting a finding is an event (OTHER) dated from its entry start."),
("D034","Y","Hiab reviewed warranty claims involving deck pins and inspected additional units in the field.","Undated sentence inside the 28-APR-2026 dated entry reporting review/inspection: inherited INVESTIGATION_START event."),
("D035","Y","Based on the investigation's review, Hiab found evidence of liftgates with hydraulic cylinders that appeared to operate asymmetrically","Finding (action: found evidence) inside the dated entry is an inherited event (OTHER)."),
("D036","X","the error- proofing data for the relevant torque station was in bypass mode from December 27, 2025, until January 23, 2026.","The dates bound the period of bypass (a data/production window), not when an action happened; the conclusion itself is undated prose. No event with this date."),
("D037","X","the error- proofing data for the relevant torque station was in bypass mode from December 27, 2025, until January 23, 2026.","January 23, 2026 only bounds the bypass window; not an event date."),
("D038","CONTESTED","In August to September 2026, Toyota investigated the impact of the below-specification material on the steering knuckle’s performance.","Versions label different sentences of the same entry: X (own-dated investigation, INVESTIGATION_START) and Y (test results, inherited OTHER) are each correct for their own sentence; the pairing cannot be settled by the rules."),
("D039","Y","Toyota conducted CAE on models of the part with the below- specification material.","Y's sentence is testing conducted (INVESTIGATION_START), clearly correct; X's sentence (assessed impact and determined) is an ambiguous analysis/result."),
("D040","Y","As a result of the investigation, Toyota confirmed that only one batch did not go through the aging furnace step.","Finding inside the 'June 2026 – July 2026' dated entry is an inherited event (OTHER)."),
("D041","Y","In some operating conditions this could lead to a loss of vehicle control, which may increase the risk of a crash.","Description of possible consequence with no action or occurrence: not an event."),
("D042","Y","On July 13, 2026, and July 30, 2026, Altec received reports from vehicle owners regarding improper operation of the boom stow auto-neutral functionality.","Owner reports reaching the filer are FILER_AWARENESS."),
("D043","Y","This recall expands upon the vehicle population subject to Recall No. 25V116, filed on February 24, 2025.","The filer's earlier Part 573 report was filed on that date: NHTSA_FILING."),
("D044","CONTESTED","During September and October 2025, MBAG reviewed the additional reports and available vehicle and production information to determine the appropriate means of obtaining and analyzing representative field parts.","Review of reports is analysis, but its stated aim is planning parts collection rather than finding cause/scope; INVESTIGATION_START vs OTHER not settled by the rules."),
("D045","Y","From November 2025 through February 2026, MBAG identified candidate vehicles and markets, developed the collection protocol, and coordinated the retrieval and shipment of the requested components.","Y's sentence (collection logistics) is correctly OTHER; X labels a different sentence (beginning coordination) whose INVESTIGATION_START type is doubtful for preparatory coordination."),
("D046","Y","The Field Engineering Activity was formally launched in March 2026.","Formal launch of the field engineering activity to obtain parts for analysis opens an investigation activity: INVESTIGATION_START."),
("D047","NEITHER","Late Aug-2026, a USA based customer noticed the hazard lamp indicators did not operate with the MRS (Master Run Switch) in the off position","Customer report of the problem is an event (FILER_AWARENESS), but date_text must keep 'Late': 'Late Aug-2026'."),
("D048","X","From July 2026, through September 2026, FCA US TSRC conducted an analysis of field records and customer assistance records to understand potential customer consequences.","Analysis conducted is INVESTIGATION_START."),
("D049","Y","On September 2, 2026, the FCA US TSRC organization recognized a vehicle build issue existed on certain vehicles","Internal recognition/finding of the issue reaching the filer is FILER_AWARENESS."),
]
corr={
"D032":{"date_text":"5-May-2026","type":"OTHER","quote":"5-May-2026: The issue was elevated to Hiab’s liftgate leadership.","inherited_date":False,"date_inferred":False},
"D047":{"date_text":"Late Aug-2026","type":"FILER_AWARENESS","quote":"Late Aug-2026, a USA based customer noticed the hazard lamp indicators did not operate with the MRS (Master Run Switch) in the off position, which varied from their previous buses.","inherited_date":False,"date_inferred":False},
}
out=[]
for i,d,q,r in D:
    o={"item_id":i,"decision":d,"quote":q,"reason":r}
    if d=="NEITHER": o["corrected"]=corr[i]
    out.append(o)
json.dump(out,open("decisions.json","w"),ensure_ascii=False,indent=1)
