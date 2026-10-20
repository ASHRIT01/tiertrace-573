import json
def inf(q, t="OTHER"):
    return {"date_text": "", "type": t, "quote": q, "inherited_date": False, "date_inferred": True}
bm = "Battle Motors was notified by one of its customers"
why_bm = "Event exists, but the chronology starts 'On or around May 19, 2025' (prose, not a dated entry), so this undated sentence gets date_inferred:true and date_text '' rather than an inherited date."
D = [
 ("D001","X","related to the performance of certain brake chambers produced by Knorr-Bremse","Narrative names Knorr-Bremse, the component maker (block supplier) of the filer's part, so U is NAMED.",None),
 ("D002","Y","Bosch notified ZF of a concern with iTCU weld integrity on its E-Modules","'Bosch' is a short form of block name Robert Bosch GmbH and is named in the narrative, so S2 is SUPPORTED.",None),
 ("D003","Y","Bosch notified ZF of a concern with iTCU weld integrity on its E-Modules","Narrative names Bosch, the Tier 2 supplier, so U is NAMED.",None),
 ("D004","Y","ZF jointly investigated the potential issue with Bosch, including engineering analysis and inspection / analysis of affected parts.","An investigation/analysis is conducted -> INVESTIGATION_START.",None),
 ("D005","X","ZF jointly investigated the issue with BMW, including further testing and analysis of parts","Investigation and testing conducted -> INVESTIGATION_START.",None),
 ("D006","Y","September 2023: Bosch reported concerns with additional E-Modules","The supplier (Bosch) tells the filer about the problem -> SUPPLIER_NOTICE.",None),
 ("D007","Y","September 2023 - November 2023: ZF worked with both customers (BMW and Stellantis) to investigate the issue.","Entry sentence reports an investigation -> INVESTIGATION_START; X's typing of the follow-on 'Collaborative investigation and analyses were conducted' sentence as OTHER is also wrong (it is an investigation).",None),
 ("D008","CONTESTED","November 29, 2023: BMW initiated a recall of 552 vehicles","The two versions are different sentences: X (collaborative investigation sentence, INVESTIGATION_START) and Y (BMW recall, OTHER) are each correctly typed events, so the pairing is not settled by the rules.",None),
 ("D009","CONTESTED","November 2023 - May 2024: Further collaborative investigation and analyses were conducted with Stellantis.","Different sentences were paired: X's investigation entry as INVESTIGATION_START and Y's Stellantis recall as OTHER are each correct events.",None),
 ("D010","CONTESTED","NHTSA contacted ZF and asked whether ZF supplied the subject components to additional U.S.-based vehicle manufacturers.","Different sentences were paired: X's NHTSA contact (notice from NHTSA, FILER_AWARENESS) and Y's 'ZF advised NHTSA' (OTHER, inherited Aug 2024) are both defensible separate events.",None),
 ("D011","CONTESTED","September 4-9, 2025: ZF received a follow-up inquiry form NHTSA's Recall Management Division","Different entries were paired: X's records review (OTHER) and Y's NHTSA inquiry (FILER_AWARENESS) are each defensible separate events.",None),
 ("D012","Y","ZF is providing this defect information report under 49 CFR 573.3(f).","The filer submits its Part 573 report -> NHTSA_FILING.",None),
 ("D013","X","9/10/2025 sample parts from customers received at manufacturing plant","Dated bullet reports an action (parts received, return requested) -> an event exists.",None),
 ("D014","Y","9/11/2025 discovered during investigation at gear manufacturing plant that some samples of part number Q47170 (gear) have oversize teeth","Dated bullet reports a finding -> an event exists.",None),
 ("D015","Y","Total population of 98 gears was shipped to differential assembly plant on 5/22/2025","A second distinct date in the bullet marks a shipment occurrence (not a production window) -> separate event.",None),
 ("D016","Y","10/9/2025 to present– additional engineering testing and analysis to confirm issue and reconfirm total scope","Dated bullet reports testing/analysis to confirm issue and scope -> INVESTIGATION_START event exists.",None),
 ("D017","Y","the global management team was informed at the Critical Concerns Management Team (CCMT) meeting on February 4, 2025.","This is internal escalation at a meeting after the filer had already found the noncompliance, not a new report reaching the filer -> OTHER (meetings).",None),
 ("D018","Y","Similar configurations are screened through to identify other potential affected vehicles.","Screening to identify the affected scope is analysis to find scope -> INVESTIGATION_START.",None),
 ("D019","Y","KZ's safety committee met on May 1st and agreed to issue a recall.","Decision to recall -> DECISION.",None),
 ("D020","Y","On April 26th, units in the yard were repaired.","Repair of affected units is remedy logistics, not an event.",None),
 ("D021","NEITHER","During the repair process, the techician noted that no torque seal was present",why_bm,inf("During the repair process, the techician noted that no torque seal was present, indicating that the nut was not properly torqued to specification and was indeed found to be loose.")),
 ("D022","NEITHER","The fleet manager had the remaining units of the same vintage inspected",why_bm,inf("The fleet manager had the remaining units of the same vintage inspected and found one other unit with a loose retaining nut and no torque seal.")),
 ("D023","NEITHER","All other units were found to be within specification with torque seal indicating proper torque.",why_bm,inf("All other units were found to be within specification with torque seal indicating proper torque.")),
 ("D024","NEITHER","Battle Motors reviewed the issue and determined that during the manufacturing process",why_bm,inf("Battle Motors reviewed the issue and determined that during the manufacturing process of the units in question a part shortage existed for the turn signal switch resulting in a deviation from standard manufactung practices, to continue production.")),
 ("D025","NEITHER","Units at the factory were inspected and no defects were found",why_bm,inf("Units at the factory were inspected and no defects were found, as well as a coursey units produced before and after the suspected time period with no issues found.")),
]
out=[]
for i,d,q,r,c in D:
    o={"item_id":i,"decision":d,"quote":q,"reason":r}
    if c: o["corrected"]=c
    out.append(o)
json.dump(out,open("decisions.json","w"),indent=1,ensure_ascii=False)
