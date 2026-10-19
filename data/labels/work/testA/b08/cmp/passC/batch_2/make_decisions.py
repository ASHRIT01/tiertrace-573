import json
V="RCLRPT-25V818-2172"
D=[
("D018","Y","This assessment was completed on November 19, 2025, and concluded that the issue posed an increased risk to motor vehicle safety.","Y's sentence has its own date and records the conclusion that a safety risk exists (DECISION). X's FSA decision belongs to table row B, which is dated 2025-11-26 and not 2025-11-19, and a recall decision is DECISION, not OTHER."),
("D019","Y","B. Field Service Action decision confirmed by Volvo Car Corporation 2025-11-26","Row B gives the date 2025-11-26 for the confirmed decision to run a field service action (recall), so the type is DECISION. X's quote '2025-11-26 C.' does not report an action."),
("D020","Y","In October 2025, the supplier informed Volvo Cars’ Torslanda factory about a potential issue involving improperly torqued bolts in seat assemblies.","The supplier tells the filer about the problem, which is SUPPLIER_NOTICE. X's quote also runs in table text from another row."),
("D021","Y","On November 12, 2025, the concern was escalated to the Critical Concern Management Team (CCMT), which ordered a formal investigation including to conduct a risk assessment.","A formal investigation was ordered, which is INVESTIGATION_START."),
("D022","Y","C. Condition detected by? (Market VR**, internal, inspection, testing)","This is a form-field question, not a reported action or occurrence, so there is no event."),
("D023","Y","(Market VR**, internal, inspection, testing) Supplier production","This is a form-field answer that describes the detection source. It reports no dated action, so there is no event."),
("D024","X","D. Number of VR with the condition, reported to Volvo Cars from NSC? 0","This is a form-field count (a status statement, with value 0), not an event."),
("D025","Y","Number of VR with the condition, reported to Volvo Cars from NSC? 0","A bare count value is a status, not an event."),
("D026","Y","E. Total number of cars included in VRs concerning the condition? 0","This is a form-field count (a status statement), not an event."),
("D027","Y","Total number of cars included in VRs concerning the condition? 0","A bare count value is a status, not an event."),
("D028","X","F. Implementation date of Field Service Action 2025-11-27","2025-11-27 is the date the remedy is implemented, which is remedy logistics and not an event. The supplier notice in the quote is dated October 2025, not 2025-11-27."),
("D029","NEITHER","This assessment was completed on November 19, 2025, and concluded that the issue posed an increased risk to motor vehicle safety.","The sentence is an event with its own date, so X (null) is wrong. Its conclusion that the issue is a safety risk makes it DECISION, not OTHER (consistent with D018)."),
("D030","X","7) Once the determination of the root cause, emails went out to all dealers with affected units on August 19th inform them of the defect.","Dealer notification emails are remedy logistics, which are excluded from events."),
("D031","Y","8) A resolution email was sent August 22nd with details regarding the resolution of the defect to all dealers with affected units.","A resolution email to dealers is remedy logistics, which is excluded."),
("D032","X","9) Replacement parts were shipped out August 25th.","Shipping replacement parts is remedy logistics (repair), which is excluded."),
("D033","X","10) Follow up emails were sent out to all dealers with defective trailers on October 9th.","Follow-up dealer emails are remedy logistics, which are excluded."),
("D034","Y","11) Confirmation of last open recalled trailer was completed as of October 28th, 2025.","Confirming that the recalled trailers were re-worked is repair of affected vehicles (remedy logistics, plus an 'as of' status), so there is no event."),
("D035","Y","October 7–9, 2025: Zero engineering staff met onsite with Dana in Italy to evaluate potential causes.","Y correctly types the entry's dated sentence (a meeting to evaluate causes) as INVESTIGATION_START. Note: X's sentence is a separate inherited-date event (a finding, OTHER) and is valid in its own right. The two were mismatched as one pair."),
("D036","NEITHER","Late September 2025: Zero proactively reviewed all 'quits while running' cases and identified a pattern of controller failures consistent with overvoltage events.","The event exists: Zero's internal review found the failure pattern (FILER_AWARENESS), so X (null) is wrong. Y drops 'Late', but the rules say to keep words like 'late' in date_text."),
("D037","X","No related injuries or crashes were reported.","A no-reports status statement is not an event."),
("D038","X","Zero and Dana are in full alignment on the root cause as being the use of non phosphate coated fasteners in the controller, and are jointly progressing the corrective action plan.","This is a status statement ('are in full alignment', 'are jointly progressing'), not an action, and it follows a blank line outside the Oct 28 entry. There is no event."),
]
corr={
"D029":{"date_text":"November 19, 2025","type":"DECISION","quote":"This assessment was completed on November 19, 2025, and concluded that the issue posed an increased risk to motor vehicle safety.","inherited_date":False,"date_inferred":False},
"D036":{"date_text":"Late September 2025","type":"FILER_AWARENESS","quote":"Late September 2025: Zero proactively reviewed all 'quits while running' cases and identified a pattern of controller failures consistent with overvoltage events.","inherited_date":False,"date_inferred":False},
}
out=[]
for i,d,q,r in D:
    o={"item_id":i,"decision":d,"quote":q,"reason":r}
    if i in corr:o["corrected"]=corr[i]
    out.append(o)
json.dump(out,open("decisions.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
