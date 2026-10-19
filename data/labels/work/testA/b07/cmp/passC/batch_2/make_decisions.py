import json
D=[
("D025","Y","From January to April 2024, MMC continued investigating the returned tailgate gas spring, confirming that the cylinder of the tailgate gas spring was severely corroded.","Investigation conducted to find the cause; rules count analysis 'opened, started or conducted' as INVESTIGATION_START."),
("D026","Y","From February to April 2025, MMC continued to analyze the second tailgate gas spring failure, including a replication test to attempt to identify the root cause of water penetration into the tailgate gas spring.","Analysis/testing conducted to identify root cause = INVESTIGATION_START."),
("D027","CONTESTED","July 3, 2025 a concern related to vehicle oversteer guidance is brought to the Product Safety organization and an investigation is opened.","One sentence carries both a first report reaching the filer (FILER_AWARENESS) and an investigation opening (INVESTIGATION_START); rules give no priority."),
("D028","X","July 21, 2025 Product Safety Evaluation Committee is informed of early results of the investigation and that additional testing is requested.","Internal committee briefing on results is a meeting/test-results occurrence (OTHER), not a new report of the problem reaching the filer."),
("D029","X","MBAG is currently aware of one warranty claim received on August 26, 2024 in the USA.","Status statement ('is currently aware of' N claims); rules exclude status statements as events."),
("D030","X","The root cause of rear brake hose leaks has not been fully determined to date.","Cause field says root cause not determined -> INSUFFICIENT."),
("D031","Y","On October 3, 2024, NHTSA opened a Preliminary Evaluation (PE24-027) to","A notice from NHTSA reaching the filer is listed under FILER_AWARENESS; the investigation is NHTSA's, not the filer's cause investigation."),
("D032","X","alleging rear brake jounce hose leaks in 2015 – 2017 Edge vehicles.","'2015' is a model-year range bounding the affected population, not an event date."),
("D033","X","On July 11, 2025, a non-conforming crimp was found during production.","Filer discovered the problem (internal finding) -> FILER_AWARENESS."),
("D034","Y","July 31- The harness manufacture (APC Manufacturing in Mexico) supplier of the harness had provided a generic brand 35-amp fuse, rather than the Bussman fuse specified on the harness drawing.","Sentence reports the filer's finding about the supplied fuse; it does not say the supplier informed the filer (the supplier's confirmation is the Aug 1 entry). FILER_AWARENESS."),
("D035","Y","a REV RV battery control center review of the macerator fuse of earlier built model year units revealed that the installation orientation of the fuse blocks by RRG employees may not match the fuse block diagram key.","Internal review finding a new problem = internal audit finding -> FILER_AWARENESS."),
("D036","X","This could cause confusion and possibly cause a fuse of a certain rating to be installed that maybe over or under rated for the designated circuit or component.","Consequence description with no action; not an event."),
("D037","NEITHER","August 14 – Update to the investigation: The generic 35-amp fuse provided by APC Manufacturing, installed to protect the macerator circuit can create a subpar connection and create heat, allowing the plastic housing to melt.","Dated entry reporting the filer's investigation finding (a result) -> event of type OTHER; APC is only the subject, it did not notify the filer, so not SUPPLIER_NOTICE.",
 {"date_text":"August 14","type":"OTHER","quote":"August 14 – Update to the investigation: The generic 35-amp fuse provided by APC Manufacturing, installed to protect the macerator circuit can create a subpar connection and create heat, allowing the plastic housing to melt.","inherited_date":False,"date_inferred":False}),
("D038","X","This may cause confusion and a fuse installed in the wrong location based upon the diagram key with risk of over or under protection of a circuit.","Consequence description with no action; not an event."),
("D039","CONTESTED","Inspection of field motor home to be performed.","Planned future action, not yet done; rules neither include nor exclude planned actions explicitly."),
("D040","X","August 18 – All units in inventory with 8/14/2025 manufacture date or newer were remedied.","8/14/2025 bounds a production window ('manufacture date or newer'), so it is not an event date."),
("D041","Y","August 1 – APC Manufacturing confirmed this fuse was substituted in their harness, but no reports of similar issues.","Supplier confirms a finding to the filer -> SUPPLIER_NOTICE event."),
("D042","Y","On August 28, 2025, FCA US determined, through the Vehicle Regulations Committee, a noncompliance with FVMSS No. 114 exists on all affected vehicles.","Block company is FCA US LLC; narrative names it by short form 'FCA US' -> SUPPORTED."),
("D043","Y","During July 2025, FCA US TSRC met with FCA US engineering and manufacturing to review the issue, understand the failure mode, review customer records and determine the suspect population.","Analysis conducted to find failure mode and scope (suspect population) -> INVESTIGATION_START."),
]
out=[]
for d in D:
    o={"item_id":d[0],"decision":d[1],"quote":d[2],"reason":d[3]}
    if len(d)>4: o["corrected"]=d[4]
    out.append(o)
json.dump(out,open("decisions.json","w"),ensure_ascii=False,indent=1)
