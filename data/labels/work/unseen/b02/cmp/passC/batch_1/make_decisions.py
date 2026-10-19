import json
D = [
("D001","X","June 2023: KML inspected the vehicle which reported this 2nd incident of starting problems and found that the alternator rotor and the alternator rotor bolt were loose.","Inspection conducted to find the cause of the starting problem; fits INVESTIGATION_START (testing/inspection conducted to find cause)."),
("D002","Y","KML Quality Assurance Division started an investigation of the cause.","Undated sentence inside the April 2023 bullet entry reporting an action; event with inherited date, INVESTIGATION_START."),
("D003","X","Loosening of the wiper arm nuts may cause the wiper arm actuator to spin within the wiper arm attachment, preventing proper wiper arm operation.","Cause field states a mechanism (nut loosening); rules make that SUPPORTED even though deeper root cause is still investigated."),
("D004","Y","Chinook received an important safety recall from Cummins about the Onan QG 2800i being recalled.","The block names the filer itself; the narrative names Cummins as maker of the recalled Onan generator, i.e. the supplier of the defective component. Chinook is the filer, not the supplier."),
("D005","X","Chinook received an important safety recall from Cummins about the Onan QG 2800i being recalled.","Cummins, a component maker/supplier of the filer, is named in the chronology, so U is NAMED."),
("D006","Y","Then notified by Cummins that they will be performing the recall.","Supplier telling the filer about its own recall is SUPPLIER_NOTICE; date inherited from the entry, using the entry's first date as in a per-date reading of the range."),
("D007","Y","05/12/2023 - Cummins came to Chinook and checked fuel hose lines and correct any if needed.","Checking and correcting fuel hoses on affected units is repair of affected vehicles (remedy logistics), not an event."),
("D008","X","04/18/2023 - 05/22/2023 - Chinook reviewed its records and identified affected Bayside models","Record review to identify affected models is analysis of scope, an event (INVESTIGATION_START) dated at the entry's first date."),
("D009","X","Chronology uploaded separately.","Chronology is only a pointer and the cause names no supply-chain company, so U is NOT_REPORTED."),
("D010","X","A design change was made to this trailer.","The field states no cause or mechanism (the design change is the remedy released per chronology); closest status is INSUFFICIENT."),
("D011","Y","September 21, 2023 through filtering Work Orders in our ERP system Pelsue determined there were 117 Pelsue Tradesman Fiberlite POD trailers & 47 Pelsue Tradesman Fiberlite XL trailers potentially affected","Analysis of work orders to determine the affected population is analysis to find scope: INVESTIGATION_START."),
("D012","Y","March 21, 2023 the first batch of Corner Caps for the field fix on affected trailers were sent to customer Lumen.","Shipping field-fix parts to a customer is remedy logistics, not an event."),
("D013","X","October 2023 - Chinook Motor Coach received Safety Recall Notice 22S48/NHTSA Recall 23V598 from Ford Motor Company.","Block is NR but the narrative names Ford, maker of the recalled base vehicle/component; SUPPORTED."),
("D014","Y","October 2023 - Chinook Motor Coach received Safety Recall Notice 22S48/NHTSA Recall 23V598 from Ford Motor Company.","Ford (base-vehicle maker) is named in the chronology and Valeo in the cause; U is NAMED."),
("D015","Y","Chinook reviewed its records to determine which Ford Transit Vans are affected by this recall.","Record review to determine affected population is scope analysis: INVESTIGATION_START."),
("D016","Y","Alexis Fire Equipment was notified by Spartan Fire LLC of the possible safety defect along with the list of chassis/vehicles sold to Alexis Fire Equipment","Spartan Fire LLC is the chassis maker supplying the filer; a named supply-chain company, so NAMED."),
("D017","Y","October 10, 2023: Nova Bus performs and inspection in the field to further understand the fault frequency.","Field inspection conducted to understand fault frequency/scope is INVESTIGATION_START."),
("D018","Y","December 5, 2023: Nova Bus corrected errors in the model and production dates in vehicle information.","Correcting vehicle information on the filing date is an amendment of the Part 573 report: NHTSA_FILING."),
("D019","Y","September 14, 2023: Nova Bus opens a formal potential safety related issue investigation.","Near-exact repeat of the September 07 sentence; repeats are not events."),
("D020","Y","Warranty experience with one customer shows a failure rate of 9 percent.","Status statement, not an action or occurrence; not an event."),
("D021","Y","There are three claims associated with this defect.","Status statement of claim count; not an event."),
("D022","Y","for more information.","Chronology is only a truncated pointer to more information; cause names no supply-chain company, so NOT_REPORTED."),
("D023","Y","REV Ambulance Gorup Orlando, Inc. (REVO) warranty department received a Technical Service Bulletin (TSB), regarding Equipment recall 23E-084. REVO was notified on December 13th, 2023.","The notice concerns the component maker's equipment recall 23E-084 (Weldon's instructions); a supplier recall notice is SUPPLIER_NOTICE."),
("D024","X","REVO conducted an inventory inspection on December 14th and determined that 235 units were affected.","Inventory inspection to determine affected units is scope analysis: INVESTIGATION_START."),
]
out=[{"item_id":a,"decision":b,"quote":c,"reason":d} for a,b,c,d in D]
json.dump(out,open("decisions.json","w"),indent=1,ensure_ascii=False)
