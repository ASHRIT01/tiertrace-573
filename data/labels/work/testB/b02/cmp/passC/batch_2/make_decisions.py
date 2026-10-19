import json
D=[]
def a(i,d,q,r,c=None):
    o={"item_id":i,"decision":d,"quote":q,"reason":r}
    if c: o["corrected"]=c
    D.append(o)
a("D026","Y","On March 13, 2026, the CCRG confirmed an increasing number of warranty reports for the monitor period.","Warranty reports reaching the filer are a (later) report of the problem: FILER_AWARENESS.")
a("D027","Y","The reports were received from June 2, 2025 to March 27, 2026.","Continues the 'As of April 10, 2026, Ford is aware of 60 warranty claims' status statement; the dates only bound a data window, not an event.")
a("D028","X","In addition to the field report on 3/25/26, Newmar is aware of one additional service claim for a loose chin spoiler on 12/16/25.","Distinct dated occurrence: a service claim reached the filer on 12/16/25 (second date in sentence; the 3/25/26 part repeats an earlier event). FILER_AWARENESS.")
a("D029","X","a Field Report from Mar-2026 was identified that indicated the dash lamps were not illuminated","Second distinct date in sentence: a field report reaching the filer is FILER_AWARENESS.")
a("D030","NEITHER","20 to 24-Apr-2026 information was gathered to verify the issue and was determined to be an incorrect program.","An event exists, but date_text must be as written ('20 to 24-Apr-2026'), and gathering information to verify the issue/cause is an investigation conducted.",
  {"date_text":"20 to 24-Apr-2026","type":"INVESTIGATION_START","quote":"20 to 24-Apr-2026 information was gathered to verify the issue and was determined to be an incorrect program.","inherited_date":False,"date_inferred":False})
a("D031","Y","The affected buses (4 total) were corrected on 31-Mar-2026.","Repair of affected vehicles is remedy logistics, not an event (X's date_text also not as written).")
a("D032","X","The same day, the manufacturing plant notified OCC of concern; OCC opened a research item.","Inside the May 4, 2026 dated entry; the new action is OCC opening a research item, i.e. an investigation opened.")
a("D033","X","September – Hyundai’s North America Safety Office (“NASO”) received ARC’s response and files","Narrative names ARC, a short form of block company ARC Automotive, Inc.: SUPPORTED.")
a("D034","Y","September – Hyundai’s North America Safety Office (“NASO”) received ARC’s response and files","Narrative names supply-chain company ARC (the inflator supplier): NAMED.")
a("D035","X","An initial meeting to develop and review the full investigation plan was held with NG on October 23, 2023.","Sentence with its own date reporting a meeting: OTHER event.")
a("D036","NEITHER","January through February – NASO began preparation for on-site inspection procedures of recovery parts with its Safety Testing & Investigation Laboratory (“STIL”).","The 'Month(s): January – June 2024' header is not part of the event; the action's own date is 'January through February' (kept as written without year).",
  {"date_text":"January through February","type":"OTHER","quote":"January through February – NASO began preparation for on-site inspection procedures of recovery parts with its Safety Testing & Investigation Laboratory (“STIL”).","inherited_date":False,"date_inferred":False})
a("D037","X","Month(s): July – December 2024","Section header with no action or occurrence; not an event.")
a("D038","X","Month(s): January – March 2025","Section header with no action or occurrence; not an event.")
a("D039","NEITHER","April through August – NG continued its investigation through crush and closed-bomb testing of lower-density propellant wafers.","Header 'Month(s): April – December 2025' is not the event date; the sentence's own date is 'April through August' and it reports testing conducted.",
  {"date_text":"April through August","type":"INVESTIGATION_START","quote":"April through August – NG continued its investigation through crush and closed-bomb testing of lower-density propellant wafers.","inherited_date":False,"date_inferred":False})
a("D040","NEITHER","January through February – NG continued with validation efforts of its analysis findings.","Header 'Month(s): January – May 2026' is not the event date; the sentence's own date is 'January through February' and it reports analysis/validation conducted.",
  {"date_text":"January through February","type":"INVESTIGATION_START","quote":"January through February – NG continued with validation efforts of its analysis findings.","inherited_date":False,"date_inferred":False})
a("D041","Y","Month(s): July 2026","Section header with no action; the July 10 amendment is a separate sentence.")
a("D042","Y","LCI notified Keystone RV that they have identified a potential concern involving shock bolts","Both SUPPORTED with same quote; the supplier named as acting is LCI (acronym of block's Lippert), and Y follows the required output shape with a 'name' field.")
a("D043","Y","05/10/2026 – Warranty claims for shock bolts include 1 claims, claim created start date 4/25/2024 to claim created end date 05/10/2026","Status statement of claim count over a data window; not an event.")
a("D044","X","claim created start date 4/25/2024 to claim created end date 05/10/2026","4/25/2024 only bounds a data window; not an event date.")
a("D045","X","The concern was entered into Wabash’s quality system for review.","Inside the 4/21/2026 entry; entering the concern for review opens an investigation/review.")
a("D046","Y","4/22/2026 - Wabash reviewed photographs from the customer and noted the absence of conspicuity tape across the width of the rear deck.","Reviewing evidence to establish the problem is analysis conducted: INVESTIGATION_START.")
a("D047","X","Wabash determined that the affected populations of trailers may not comply with FMVSS 108 S8.2.","Determination that a noncompliance exists: DECISION.")
a("D048","NEITHER","4/23-5/14/2026 - Wabash investigated warranty, sales, and manufacturing information and escalated the issue","Event exists but date_text must be as written ('4/23-5/14/2026'); it reports an investigation conducted.",
  {"date_text":"4/23-5/14/2026","type":"INVESTIGATION_START","quote":"4/23-5/14/2026 - Wabash investigated warranty, sales, and manufacturing information and escalated the issue to the Product Safety Committee to evaluate compliance with FMVSS 108 and the potential scope of the issue.","inherited_date":False,"date_inferred":False})
a("D049","X","We as the vehicle manufacturer are required to issue a recall for the vehicles involved and started the recall process on 5/20/2026.","Starting the recall process is the decision to recall: DECISION.")
a("D050","Y","On May 18, 2026, research began into finding out which brands used Q'Straints products within their defined dates of recall.","Research to determine scope began: INVESTIGATION_START.")
json.dump(D,open("decisions.json","w"),ensure_ascii=False,indent=1)
