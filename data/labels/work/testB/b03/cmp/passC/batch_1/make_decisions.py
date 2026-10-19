import json
Q_NOV = "On November 26, 2024, an issue pertaining to incomplete software recall remedies was brought to Ford’s Critical Concern Group (CCRG) for review."
Q_DEC = "In December 2024, a cross-functional team was formed to audit all software FSAs that used the FDRS service tool, with its first focus being on safety and compliance FSAs."
Q_MAR = "In March 2025, during a comprehensive audit of software-related FSAs dating back to 2017, discrepancies were identified during the transition between the legacy field service tool, known as IDS, and the new FDRS service tool."
Q_NOVH = "In November 2025, a harvest program was approved to assess the success of remedies applied using the IDS tool for programs administered during this transition period."
Q_APR = "On April 16, 2026, the matter was presented to the Critical Concern Review Group (CCRG)."
R_U = "Ford is the filer (and the block's OEM); the filer's own committees are not supply-chain parties, and no supplier is mentioned, so NONE_MENTIONED."
R_MIS = "The two versions are different sentences (December 2024 team formation vs December 19, 2024 NHTSA contact) paired by alignment; each is a separate valid event with a defensible type (team formed to audit = INVESTIGATION_START; informing NHTSA of a concern, not a 573 filing = OTHER), so neither side is wrong for one shared event."
R_MAR = "Discrepancies identified in an internal audit = internal audit finding reaching the filer -> FILER_AWARENESS."
R_NOVH = "Approval of a harvest program to assess remedy success = analysis/testing opened to determine scope -> INVESTIGATION_START."
R_APR = "Presenting the matter to an internal committee is a meeting, not a new report reaching the filer -> OTHER."
d = []
def add(i, dec, q, r, corr=None):
    o = {"item_id": i, "decision": dec, "quote": q, "reason": r}
    if corr is not None: o["corrected"] = corr
    d.append(o)
add("D001","X",Q_NOV,R_U)
add("D002","CONTESTED",Q_DEC,R_MIS)
add("D003","Y",Q_MAR,R_MAR)
add("D004","Y",Q_NOVH,R_NOVH)
add("D005","X",Q_APR,R_APR)
add("D006","Y","On July 7, 2026, Ford’s Field Review Committee reviewed the concern and approved an amendment to the population of the field action.","Approving an amendment to the recall population is the decision to recall the added (territory) vehicles covered by this filing -> DECISION.")
add("D007","Y",Q_NOV,R_U)
add("D008","CONTESTED",Q_DEC,R_MIS)
add("D009","X",Q_MAR,R_MAR)
add("D010","X",Q_NOVH,R_NOVH)
add("D011","Y",Q_APR,R_APR)
add("D012","Y","The power window system configuration may exceed the regulatory requirement for remote actuation closing force, increasing the risk of injury.","The cause field only restates that a regulatory requirement may not be met, without a mechanism -> INSUFFICIENT.")
add("D013","X",Q_NOV,R_U)
add("D014","CONTESTED",Q_DEC,R_MIS)
add("D015","Y",Q_MAR,R_MAR)
add("D016","Y",Q_NOVH,R_NOVH)
add("D017","Y",Q_APR,R_APR)
add("D018","Y","Not disclosed by the manufacturer.","The field is not NR/empty but states no cause; the cause is withheld/unsettled, so INSUFFICIENT, not SUPPORTED.")
add("D019","Y","On May 18, 2026, in an audit for information documentation, IMC found a discrepancy on the VIN Label for Indian Chief Vintage models.","Both are SUPPORTED (IMC is the acronym of the block company); Y follows the output format with a name field giving the name as it appears in the narrative, X has a non-schema label key and no name.")
add("D020","Y","On May 18, 2026, in an audit for information documentation, IMC found a discrepancy on the VIN Label for Indian Chief Vintage models.","IMC is the filer itself (Indian Motorcycle Company); the filer is not a supply-chain party, and no other supplier is mentioned -> NONE_MENTIONED.")
add("D021","Y","On May 18, 2026, in an audit for information documentation, IMC found a discrepancy on the VIN Label for Indian Chief Vintage models.","Discrepancy found in an internal audit = internal audit finding -> FILER_AWARENESS.")
add("D022","Y","Vehicles built on or after May 20, 2026 were produced with corrected VIN labels and in conjunction, IMC started an investigation.","May 20, 2026 only bounds a production window ('built on or after') and is not an event date; the sentence has no own date, so no May 20 event exists (it inherits May 19 instead, see D023).")
add("D023","Y","May 19, 2026 an update was made to the manufacturing documentation system updating the VIN Labels.","Entry begins with a bare date, so the following undated sentence (May 20 is a production-window bound) inherits May 19, 2026; its action 'IMC started an investigation' -> INVESTIGATION_START.")
json.dump(d, open("decisions.json","w"), indent=1, ensure_ascii=False)
