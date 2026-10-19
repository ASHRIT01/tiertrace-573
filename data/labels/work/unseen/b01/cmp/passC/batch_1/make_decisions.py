import json
D = [
("D001","X","Following reporting of an overheating incident in December, 2021, Orpak undertook to conduct internal and independent testing","A report of an incident reaching the filer side in Dec 2021 is a FILER_AWARENESS event, not OTHER."),
("D002","Y","Orpak undertook to conduct internal and independent testing of the DataPass Plus devices up through May, 2022.","Second distinct date in the sentence attaches to the testing action (not a production data window); testing conducted to find the cause is INVESTIGATION_START."),
("D003","Y","2/6/2023 – Meritor Product Safety and Compliance Committee reviewed engineering technical position conclusion and determined a possible safety related concern has been identified and impacted customers should be notified.","Committee determination that a safety concern exists is a DECISION."),
("D004","X","3/23/2023 – Meritor notified that Spartan Fire filed a 573 Defect Report with NHTSA.","Dated occurrence (Meritor received notice of a customer's filing); not a status, pointer or remedy logistics, so it is an event (OTHER)."),
("D005","Y","As part of its normal quality control procedures, 3M tested a sample of sheeting from the lot in question during December 2022.","Routine QC testing, not an investigation opened to find the cause or scope of a known problem; OTHER fits better than INVESTIGATION_START."),
("D006","Y","Additional investigation continued into early 2024, which resulted in additional raw material lots of the sub- supplier identified as being potentially affected by the subject condition.","Narrative refers to a sub-supplier only generically; Hyundai and Mercedes-Benz are customers, so UNNAMED."),
("D007","Y","Between October 2023 and December of 2023, Hyundam continued to inspect and evaluate fuel pumps recovered by Hyundai and Mercedes-Benz.","Inspection and evaluation of recovered pumps is investigation/analysis conducted to find cause or scope: INVESTIGATION_START."),
("D008","X","Between October 2023 and December of 2023, Hyundam continued to inspect and evaluate fuel pumps","Two distinct dates in one sentence give one event per date; October 2023 bounds the inspection action, not a production data window."),
("D009","X","Precision Circuits traveled to Brinkley RV on September 22, 2023 to review the application and to confirm that the wire in fact was undersized.","Filer conducted a review on site to confirm the defect: analysis conducted to find cause/scope, INVESTIGATION_START."),
("D010","Y","On Thursday, September 21, 2023, during an electrical audit performed at Brinkley RV, it was discovered that the neutral wire for the Power Control System was undersized for a 50 Amp service system.","Dated discovery of the problem in an audit is an event; first awareness of the issue (FILER_AWARENESS)."),
("D011","Y","After a lot of research it was determined that the models that Ford sent us did not have stabilizer bar.","Ford supplied the base vehicles to the filer (base-vehicle maker), a supply-chain company named in the narrative: NAMED."),
("D012","Y","They were all repaired in April of 2023.","Repair of affected vehicles is remedy logistics, not an event."),
("D013","X","On October 23, 2023, Cruise completed its review and immediately initiated an assessment of the safety risk associated with the findings.","An assessment/analysis was initiated: INVESTIGATION_START."),
("D014","Y","On January 4, 2023, Gratimax decided that a non- compliance with FMVSS 108 and 224 existed.","Decision that a noncompliance exists is DECISION."),
("D015","Y","September 2022: Additional complaints were received.","Later customer complaints reaching the filer are FILER_AWARENESS."),
("D016","Y","Engineering team instructed to conduct further investigation.","Investigation opened/ordered: INVESTIGATION_START."),
("D017","X","January 30, 2023: The engineering and quality dedicated team gathered again, and updated data and information related to the propulsion issue.","Dated meeting/action, not a status or repeat; an event (OTHER)."),
("D018","Y","NEWELL IMMEDIATELY CONDUCTED A QUALITY REVIEW AND DETERMINDED THE INSTALLATION OF AN ADDITIONAL BRAKE SWITCH","Quality review conducted to find the cause: INVESTIGATION_START."),
("D019","Y","Mar. 7,2023 - After internal discussions and analysis of the Meritor information, Terex Advance Mixer deemed this condition to be safety related.","Determination that the condition is safety related is DECISION."),
("D020","Y","Therefore, a 573 defect report was initiated.","Filer initiating its Part 573 report is NHTSA_FILING."),
("D021","Y","Defective part.","Only restates that there is a defect; no cause or mechanism is stated, so INSUFFICIENT."),
("D022","Y","June 2023: New cases of in-service vehicles with cracks in the firewall leading to damage to the cables running under the tank were reported.","New field reports reaching the filer are FILER_AWARENESS."),
]
out=[{"item_id":a,"decision":b,"quote":c,"reason":d} for a,b,c,d in D]
json.dump(out,open("decisions.json","w"),indent=1,ensure_ascii=False)
