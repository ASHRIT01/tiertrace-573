import json
D = [
 ("D001","X","International begins a limited inspection of other bus chassis to determine if the same issue is present.","Inspection opened to determine whether other chassis have the issue (scope) = INVESTIGATION_START."),
 ("D002","X","Curtiss-Wright completes its inspection of 10 suspect shift actuators returned by International, finding there was unexpected variation in the neutral set point","Completion of supplier inspection with a finding is a test result (OTHER), not the start of an investigation."),
 ("D003","X","Curtiss-Wright continues its investigation into the issue and determines that the actuator’s input shaft was updated from powdered metal to cut steel","Supplier's continuing investigation/result; text does not say the supplier informed the filer, so OTHER (test result) rather than SUPPLIER_NOTICE."),
 ("D004","Y","May 1, 2025 – Spartan Fire Chassis (Spartan) received claim of a cab door latch logic issue.","Narrative names Spartan Fire Chassis, a short form/brand of block company Spartan Fire LLC; rule says this counts as SUPPORTED."),
 ("D005","X","May 1, 2025 – Spartan Fire Chassis (Spartan) received claim of a cab door latch logic issue.","Spartan is the filer's chassis maker/block-listed supplier, a supply-chain company named in the chronology = NAMED."),
 ("D006","Y","May 1, 2025 – Spartan Fire Chassis (Spartan) received claim of a cab door latch logic issue.","The claim reached Spartan (supplier), not the filer Alexis; FILER_AWARENESS is for reports reaching the filer, so OTHER."),
 ("D007","Y","October 14, 2025 - Alexis Fire Equipment was notified by Spartan about the recall and provided with the recall population","Supplier/chassis maker Spartan tells the filer about its recall = SUPPLIER_NOTICE."),
 ("D008","X","December 2024 - October 2025 Toyota conducted vehicle testing to confirm if (1) the interruptions, or (2) the abnormal camera optical alignment data could occur on a vehicle","Dated entry sentence reports testing conducted to find scope = INVESTIGATION_START with own date; Y's paired sentence is a test result (would be OTHER), not FILER_AWARENESS."),
 ("D009","X","As a result, Toyota decided to conduct a recall.","Decision to recall is an event (DECISION). No blank line/new entry follows the 'December 2024 - October 2025' entry ('On October 24' starts with 'On'), so per rules it inherits that entry date."),
 ("D010","X","August 31, 2024: Agility’s engineering team was advised of a report from a customer that the manual cylinder valve on a CNG fuel system experienced a leak.","Filer is The Heil Co.; the report reached Agility (a supplier), not the filer, so OTHER rather than FILER_AWARENESS."),
 ("D011","X","Based upon the results of the investigation to date, Agility’s engineering team recommended that the matter be escalated to Agility’s Safety Committee for consideration.","An action (recommendation to escalate) inside the dated 'September 12 – November 13, 2024:' entry; valid OTHER event with inherited date."),
 ("D012","Y","Arrangements were made to obtain the valves for analysis.","An action inside the 'August 31, 2024:' entry; not remedy logistics or status, so it is an event (OTHER) with inherited date."),
 ("D013","Y","On Friday, October 24, 2025, Micro Bird received a notification letter of a recall (NHTSA #25E063) from its provider (Q’Straint)","Receipt of the supplier's recall notice = SUPPLIER_NOTICE event on its own date; Y has it, X omits it."),
 ("D014","Y","certain wheelchair securement kits shipped between May 7, 2025, and September 10, 2025, may contain a defective retractor.","September 10, 2025 only bounds a shipment data window; not an event date, so no event."),
 ("D015","NEITHER","Internal reviews of our recent orders and stock quickly determined that Micro Bird had been provided with potentially defective parts.","Event exists, but the preceding sentence starts with 'On', so it is not a dated entry: undated prose gets date_inferred true and empty date_text. It is an internal finding (FILER_AWARENESS), not a defect/recall DECISION."),
 ("D016","X","On Monday, October 27, 2025, a meeting was called to advise strategic Micro Bird personnel that a recall notification was received from its provider","A dated meeting is an action/occurrence = OTHER event; Y wrongly omits it."),
 ("D017","Y","The trapped air may create a separation between the components, resulting in a bubble appearance.","Explanatory description with no action; not an event."),
]
out=[]
for i,d,q,r in D:
    o={"item_id":i,"decision":d,"quote":q,"reason":r}
    if i=="D015":
        o["corrected"]={"date_text":"","type":"FILER_AWARENESS","quote":q,"inherited_date":False,"date_inferred":True}
    out.append(o)
json.dump(out,open("decisions.json","w"),ensure_ascii=False,indent=1)
