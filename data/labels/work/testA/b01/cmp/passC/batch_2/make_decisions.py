import json
D = [
 ("D025","NEITHER","Between January 2020 and June 2022, Super Products learned of 4 more incidents of tank strap tie rod weld failures for the affected vehicle population.",
  "'learned of 4 more incidents' is a report reaching the filer -> FILER_AWARENESS (X's OTHER is wrong); Y's date_text joins two dates, which the rules split into one event per date, so the June 2022 event keeps date_text 'June 2022'.",
  {"date_text":"June 2022","type":"FILER_AWARENESS","quote":"Between January 2020 and June 2022, Super Products learned of 4 more incidents of tank strap tie rod weld failures for the affected vehicle population.","inherited_date":False,"date_inferred":False}),
 ("D026","Y","After the May 2022 incident, Super Products conducted metallurgical tests on the tank tie rod and the connected square tabbed washer to confirm the cause as insufficient rod penetration and weld size.",
  "Testing conducted to establish the cause is INVESTIGATION_START by rule.",None),
 ("D027","Y","In October 2022, during the course of the investigation a customer reported another disengaged tank tie rod.",
  "A customer report reaching the filer is FILER_AWARENESS (a later one counts too).",None),
 ("D028","X","On April 3, 2023, the chassis manufacturer added a riser tube.",
  "Block is NR, but the narrative refers generically to the chassis manufacturer (the maker of the chassis/tube assembly), so it is a generic supplier reference: INSUFFICIENT, not NOT_REPORTED.",None),
 ("D029","X","On April 3, 2023, the chassis manufacturer added a riser tube.",
  "A chassis maker is a supply-chain party under the rules, and it is mentioned only generically, so UNNAMED rather than NONE_MENTIONED.",None),
 ("D030","X","On March 21, 2023, Columbus inspected a vehicle of the same model and found that there wasn’t the appropriate clearance",
  "Inspecting another vehicle of the same model to check the condition is testing/analysis conducted to find the scope: INVESTIGATION_START.",None),
 ("D031","Y","April 10, 2023 Mack Manufacturing reports that they have discovered that we have vehicles where the vehicle horns are inoperative and an investigation is opened.",
  "The main action is the first report/discovery of the problem reaching the filer (FILER_AWARENESS); the investigation opening follows from it in the same sentence.",None),
 ("D032","X","On March 15, 2023, E-ONE was contacted and told the inclination sensor stopped working during training on truck SO 144708 in Sarnia, Canada.",
  "A notice of the problem reaching the filer is FILER_AWARENESS.",None),
 ("D033","X","On April 17, 2023, E-ONE was contacted that the Aerial device contacted the cab during training on another truck in Marion, Illinois, truck SO 144814.",
  "A later report of the problem reaching the filer is FILER_AWARENESS.",None),
 ("D034","Y","On April 28, 2023, research was performed to identify the population of the affected trucks",
  "Research to identify the affected population is analysis conducted to find the scope (INVESTIGATION_START); X's quote also runs on into the separate May 8 sentence.",None),
 ("D035","Y","REV Recreation Group would immediately conduct a recall out of an abundance of caution on behalf of the hitch supplier.",
  "The sentence states the filer's decision to recall: DECISION.",None),
 ("D036","X","A review of warranty history revealed no other reported failures of this part as of this time.",
  "A warranty-history review is an analysis conducted to find the scope: INVESTIGATION_START. It sits inside the July 2022 bullet, so the inherited date is right.",None),
 ("D037","X","In November 2022, REV Recreation Group received notice of a second reported failure of this hitch.",
  "X's sentence is a notice of failure reaching the filer (FILER_AWARENESS). Y's version quotes a different sentence (parts returned to Lippert), so it is not this event.",None),
 ("D038","X","April 3, 2023 - A customer with REV Recreation Group gas motor home reported their Lippert hitch welds had a failure.",
  "A customer report reaching the filer is FILER_AWARENESS.",None),
 ("D039","Y","Further evaluations were conducted and remain underway.",
  "X's 'Field data now shows that there are a total of 5 similar reports' is a status statement (count of reports), not an event. Evaluations conducted within the April 3, 2023 bullet are INVESTIGATION_START.",None),
 ("D040","NEITHER","Further evaluations were conducted and remain underway.",
  "The event exists (an action inside the April 3, 2023 bullet), but evaluations conducted are INVESTIGATION_START, not OTHER.",
  {"date_text":"April 3, 2023","type":"INVESTIGATION_START","quote":"Further evaluations were conducted and remain underway.","inherited_date":True,"entry_quote":"April 3, 2023 - A customer with REV Recreation Group gas motor home reported their Lippert hitch welds had a failure.","date_inferred":False}),
 ("D041","Y","On May 18, 2022, during a routine PDI Inspection, it was found that the cooktop may be pulling the cooktop flame down/inverted.",
  "An internal inspection/audit finding of the problem is FILER_AWARENESS.",None),
 ("D042","Y","3/6/23, Noticed weld issue with robotic weld program on first shift.",
  "'Entered concern response to bring awareness to product safety team.' is an undated action inside the dated 3/6/23 entry, so it is an event with an inherited date. It is an internal escalation, so OTHER.",None),
]
out=[]
for iid,dec,q,r,c in D:
    o={"item_id":iid,"decision":dec,"quote":q,"reason":r}
    if c is not None: o["corrected"]=c
    out.append(o)
json.dump(out,open("decisions.json","w"),ensure_ascii=False,indent=1)
