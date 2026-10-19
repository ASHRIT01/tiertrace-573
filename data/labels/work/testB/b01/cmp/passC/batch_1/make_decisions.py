import json
D = [
 ("D001","CONTESTED","An inquiry to the supplier Samsung SDI Co. Ltd. revealed that affected cells have also been delivered to Webasto Roof & Components SE.","The two versions label different sentences (X: supplier inquiry reply, plausibly SUPPLIER_NOTICE; Y: alignment meetings, correctly OTHER). Each is defensible for its own sentence; also X's entry date is separated from the sentence by a blank line in the text, so inheritance is unclear."),
 ("D002","Y","A final meeting to assess product safety relevance and U.S. market exposure was performed and concluded with the decision to notify NHTSA.","The sentence reports the decision to notify NHTSA (i.e. to file/recall), which is DECISION rather than a mere meeting."),
 ("D003","Y","Reports for remedy completion rates will be provided by the individual manufacturers.","Future remedy logistics statement, not an action or occurrence; not an event."),
 ("D004","Y","Multiple alignment meetings with Samsung SDI Co., Ltd. to determine potential risks. Internal analyses were conducted.","'Internal analyses were conducted' reports analysis conducted to assess the issue (INVESTIGATION_START) inside the dated 'From March 2025 to December 2025' entry; the event exists."),
 ("D005","Y","Subsequent validation testing shows post-paint hardness readings averaging approximately 90-95 HB and no impact-test cracking in these post-correction wheels.","Reports a test result (OTHER) within the January 13, 2026 dated entry; it is an occurrence, so the event exists."),
 ("D006","Y","This date constitutes the manufacturer’s defect determination for purposes of 49 C.F.R. Part 573.","Explanatory statement restating the earlier determination (near-repeat/description), not a new action; X also splits the sentence at 'C.F.R.'."),
 ("D007","Y","This date constitutes the manufacturer’s defect determination for purposes of 49 C.F.R. Part 573.","'Part 573.' is a fragment of a non-event explanatory sentence, not an event."),
 ("D008","Y","February 11, 2026: The Accelera by Cummins Product Safety Leader was notified of the incident.","A notice of the problem reaching the filer (a later one counts) is FILER_AWARENESS."),
 ("D009","X","February 20, 2026: A Product Safety Hazard Analysis was initiated to evaluate this software behavior.","An analysis is opened to evaluate the issue: INVESTIGATION_START."),
 ("D010","CONTESTED","3/6/2026 – Investigation opened. Axles bill of materials reviewed and orders put on hold with affected seals.","Versions label different sentences: X (report of incorrect seals, FILER_AWARENESS) and Y (BOM review/orders on hold, OTHER containment) are each correct for their own sentence; the pairing cannot be settled as one being wrong."),
 ("D011","Y","Investigation called for determining affected component range.","An investigation to determine the scope is INVESTIGATION_START."),
 ("D012","Y","Root cause is being researched.","The cause field says the root cause is still being researched with only preliminary indications; per rules this is INSUFFICIENT, and X's quote does not state a cause."),
 ("D013","CONTESTED","The screens were returned to Weldon for futher assessment but no faults were found.","Versions label different sentences: X (field failure report, FILER_AWARENESS) and Y (screens returned, no faults found, OTHER inherited) are each defensible for their own sentence."),
 ("D014","X","By March 17, 2026, the supplier was able to recreate the failure.","The sentence reports a supplier test result, not the supplier telling the filer; test results are OTHER."),
 ("D015","Y","A new screen out of the box indicated the same issue as the unit installed in the vehicle.","Occurrence/test result inside the March 5 2026 dated entry; event exists as OTHER with inherited date."),
 ("D016","Y","Weldon contacted the supplier of the device (Enovation Controls- ENC) for technical support and began to investigate further, including development of a test fixture.","Reports that Weldon began investigating: INVESTIGATION_START, inside the March 5 2026 entry."),
 ("D017","Y","Testing data and additional failed units were provided to the supplier.","An action (providing data/units to supplier) inside the March 5 2026 entry: OTHER event."),
 ("D018","Y","It was also determined by that end of line testing at Enovation controls would not reliably indicate the presence of the issue.","A finding/determination reported as an occurrence inside the March 5 2026 entry: OTHER event."),
 ("D019","Y","On March 24, 2026, NHTSA supplied GM with the final test reports from this supplemental testing, which indicated that the subject brake fluid failed S5.1.7 due to the presence of visible sediment.","A notice from NHTSA reaching the filer is FILER_AWARENESS."),
 ("D020","NEITHER","GM responded to NHTSA’s August 7, 2025 information requests on September 3, 2025 and November 3, 2025","The sentence has distinct dates, so an August 7, 2025 event exists (NHTSA information requests to GM); a notice/request from NHTSA is FILER_AWARENESS, not OTHER."),
 ("D021","CONTESTED","On 4/20/2026, following the event described above, Waymo implemented additional operational restrictions at times and in locations where there is an elevated risk of encountering a flooded, higher-speed roadway.","Versions label different sentences: X (operational restrictions, OTHER) is correct for its sentence; Y labels the flooding incident itself, whose typing (occurrence vs awareness) the rules do not clearly settle."),
 ("D022","Y","May 15, 2026: Keystone notifies Lippert of their decision to release as a recall.","A customer notice about the issue reaching the filer is FILER_AWARENESS (a later report counts)."),
 ("D023","CONTESTED","March 10, 2026: Potential issue initially identified through theoretical FEA stress analysis.","Versions label different sentences: Y (issue identified, FILER_AWARENESS) and X (stop-ship, OTHER inherited) are each correct for their own sentence."),
 ("D024","X","March - June 2026: Cross-functional team conducted an extended review, including root cause analysis, to confirm the FEA stress analysis and to evaluate potential safety implications.","A review including root cause analysis was conducted: INVESTIGATION_START event exists."),
 ("D025","NEITHER","On June 25, 2026, Ford's Critical Concern Review Group (CCRG) completed its investigation, which considered Ford’s 26C10 recall and Federal Motor Vehicle Safety Standard (FMVSS) No. 108, Section 6.2.1.","Completing an investigation is not a notice reaching the filer (X wrong type), and Y merges two distinct dates into one date_text; the June 25 CCRG sentence is an OTHER event."),
]
corr = {
 "D020": {"date_text":"August 7, 2025","type":"FILER_AWARENESS","quote":"GM responded to NHTSA’s August 7, 2025 information requests on September 3, 2025 and November 3, 2025 (together, the “Responses”), and GM incorporates the Responses by reference.","inherited_date":False,"date_inferred":False},
 "D025": {"date_text":"June 25, 2026","type":"OTHER","quote":"On June 25, 2026, Ford's Critical Concern Review Group (CCRG) completed its investigation, which considered Ford’s 26C10 recall and Federal Motor Vehicle Safety Standard (FMVSS) No. 108, Section 6.2.1.","inherited_date":False,"date_inferred":False},
}
out=[]
for i,d,q,r in D:
    o={"item_id":i,"decision":d,"quote":q,"reason":r}
    if d=="NEITHER": o["corrected"]=corr[i]
    out.append(o)
json.dump(out,open("decisions.json","w"),ensure_ascii=False,indent=1)
