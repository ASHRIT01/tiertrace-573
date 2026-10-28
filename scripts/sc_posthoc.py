"""SC-1 POST HOC diagnostics (added after seeing results; no protocol change, no new metric definition):
  (1) population filings whose declared name is a short form of the filer's own name (token containment with a filer name), and how many
      agent/silver matches fall in them;
  (2) silver S1 quotes located outside the block by the first-match rule, and whether an occurrence inside the block exists.
  python scripts/sc_posthoc.py -> reports/sc/phase_8_posthoc.json (aggregates only)"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sc_check import attach_claims  # noqa: E402
from sc_inventory import load_all  # noqa: E402
from sc_lib import inside, locate_quote, match_contain, match_exact  # noqa: E402

POP = ("NAMED_SUPPLIER", "MULTIPLE")


def main():
    F = load_all()
    attach_claims(F)
    P = [f for f in F if f["stratum"] in POP]
    short = [f for f in P if any(match_contain(d, fn) for d in f["declared"] for fn in f["filer_names"] if fn)]
    hit = lambda c, f: any(match_exact(c["name"], d) for d in f["declared"])
    R = {"note": "POST HOC diagnostics added after seeing results; reference = filer-declared supplier (non-AI, not ground truth)",
         "population_filings": len(P),
         "declared_name_is_short_form_of_filer": {"filings": len(short),
                                                  "agent_all_matching_claims_in_them": sum(hit(c, f) for f in short for c in f["agent"]),
                                                  "agent_all_matching_claims_total": sum(hit(c, f) for f in P for c in f["agent"]),
                                                  "agent_accepted_matching_claims_in_them": sum(hit(c, f) for f in short for c in f["agent"] if c["accepted"]),
                                                  "agent_accepted_matching_claims_total": sum(hit(c, f) for f in P for c in f["agent"] if c["accepted"]),
                                                  "agent_filings_recalled_in_them": sum(any(hit(c, f) for c in f["agent"]) for f in short),
                                                  "agent_filings_recalled_total": sum(any(hit(c, f) for c in f["agent"]) for f in P)}}
    s1 = []
    for f in P:
        spans = [(b["start"], b["end"]) for b in f["blocks"]]
        silver = {x["file"]: x for x in json.load(open(f"data/labels/{f['split']}_silver.json"))}[f["file"]]
        for c in silver["claims"]:
            if c["id"] == "S1" and c["status"] == "SUPPORTED":
                sp = locate_quote(c["quote"], f["text"])
                if sp is not None and not inside(sp, spans):
                    occ = [m.span() for m in re.finditer(r"\s+".join(re.escape(t) for t in c["quote"].split()), f["text"])]
                    s1.append({"first_match_in_page_header": bool(re.search(r"(?i)manufacturer\s+$", f["text"][max(0, sp[0] - 20):sp[0]])),
                               "an_occurrence_inside_block": any(inside(o, spans) for o in occ)})
    R["silver_S1_located_outside_block"] = {"n": len(s1), "first_match_is_header_manufacturer_name": sum(x["first_match_in_page_header"] for x in s1),
                                            "with_an_occurrence_inside_block": sum(x["an_occurrence_inside_block"] for x in s1)}
    json.dump(R, open("reports/sc/phase_8_posthoc.json", "w"), indent=1)
    print(json.dumps(R, indent=1))


if __name__ == "__main__":
    main()
