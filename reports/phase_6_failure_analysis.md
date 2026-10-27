# Phase 6 failure analysis: **POST HOC, EXPLORATORY, silver labels, not human-verified, not a result**

Nothing here was preregistered. It uses the existing run outputs and the frozen scorer machinery (amendment-1 wrapper, primary settings) only; no model run, no rerun, no change to prompt, verifiers, thresholds, scorer or labels. Events only. 'Accepted' = no verifier fired and run 2 agrees (the H1 accepted set); 'wrong' = the frozen scorer's `event_class` is not `right` (so the same claims as H1/H5; the strict view below reproduces the committed H1 delta, CI and counts exactly on all three splits). Silver labels are AI-made and not independent of the pipeline; no label-error figure is claimed. Scripts: `scripts/phase6_failure_analysis.py`, `scripts/phase6_failure_analysis_md.py`.

## (a) Accepted event claims scored wrong, classified by code
Classes are assigned in this order: (iv) an earlier accepted claim in the same filing has the same type and the same normalised quote (dates and digits removed); otherwise (i) the claim's date overlaps a scored gold event of that filing but the type differs; (ii) a scored gold event of that type exists but none has a matching date; (iii) neither; (v) the claim's own date text cannot be parsed (frozen class `wrong:date_unparsed`, not in the requested list but needed so the classes add up). Class (iii-u) is the part of (iii) where the filing has an unscored (undated) gold event of the same type. Mutually exclusive.

| class | Test-A (primary) | Test-B | unseen-filer |
|---|---|---|---|
| accepted event claims / of which scored wrong | 536 / 143 (26.7%) | 263 / 93 (35.4%) | 231 / 76 (32.9%) |
| (i) date matches a gold event, type differs | 122 (85.3%) | 80 (86.0%) | 57 (75.0%) |
| (ii) type matches a gold event, date differs | 11 (7.7%) | 10 (10.8%) | 8 (10.5%) |
| (iii) neither matches | 3 (2.1%) | 1 (1.1%) | 4 (5.3%) |
| (iii-u) neither matches, but an undated gold event of that type exists | 6 (4.2%) | 2 (2.2%) | 2 (2.6%) |
| (v) own date unparseable | 1 (0.7%) | 0 (0.0%) | 3 (3.9%) |
| (iv) duplicate of an earlier accepted claim | 0 (0.0%) | 0 (0.0%) | 2 (2.6%) |
| date matches a gold event (i) vs date does not match (ii + iii + iii-u + v) | 122 vs 21 | 80 vs 13 | 57 vs 17 |

Duplicates (iv): underlying class of the repeated claims: Test-A (primary): none; Test-B: none; unseen-filer: {'ii': 1, 'i': 1}.

### By manufacturer (filer): the 5 filers with the most accepted-wrong claims in each split, plus other

**Test-A (primary)**

| filer | accepted wrong | (i) | (ii) | (iii) | (iii-u) | (v) | (iv) |
|---|---|---|---|---|---|---|---|
| paccar incorporated | 13 | 12 | 1 | 0 | 0 | 0 | 0 |
| chrysler (fca us, llc) | 9 | 8 | 0 | 1 | 0 | 0 | 0 |
| daimler trucks north america, llc | 8 | 7 | 1 | 0 | 0 | 0 | 0 |
| bmw of north america, llc | 8 | 6 | 1 | 0 | 0 | 1 | 0 |
| forest river, inc. | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| other | 97 | 81 | 8 | 2 | 6 | 0 | 0 |

**Test-B**

| filer | accepted wrong | (i) | (ii) | (iii) | (iii-u) | (v) | (iv) |
|---|---|---|---|---|---|---|---|
| ford motor company | 23 | 20 | 2 | 0 | 1 | 0 | 0 |
| jayco, inc. | 13 | 12 | 0 | 1 | 0 | 0 | 0 |
| chrysler (fca us, llc) | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| lippert | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| general motors, llc | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| other | 44 | 35 | 8 | 0 | 1 | 0 | 0 |

**unseen-filer**

| filer | accepted wrong | (i) | (ii) | (iii) | (iii-u) | (v) | (iv) |
|---|---|---|---|---|---|---|---|
| nova bus (us) inc. | 8 | 7 | 0 | 0 | 0 | 0 | 1 |
| zoox, inc. | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| lucid usa, inc. | 5 | 0 | 1 | 1 | 0 | 3 | 0 |
| electra meccanica vehicles corp | 4 | 3 | 1 | 0 | 0 | 0 | 0 |
| zeekr technology us, llc | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| other | 48 | 36 | 6 | 3 | 2 | 0 | 1 |

## (b) Date-only view (event type ignored): NOT PREREGISTERED
A claim counts as right if its date overlaps ANY scored gold event of the filing, whatever the type. Same claims, same accepted set, same filer-cluster bootstrap (2000 resamples, seed 0). Strict = the committed definition (date and type).

| split | view | B2 error (all claims) | agent accepted error | delta = B2 - accepted | coverage |
|---|---|---|---|---|---|
| Test-A (primary) | strict (date + type) | 0.402 [0.347, 0.466] | 0.267 [0.217, 0.321] | 0.135 [0.086, 0.192] | 0.533 (536/1005) |
| Test-A (primary) | date only | 0.142 [0.087, 0.214] | 0.039 [0.022, 0.061] | 0.103 [0.051, 0.172] | 0.533 (536/1005) |
| Test-B | strict (date + type) | 0.386 [0.306, 0.456] | 0.354 [0.244, 0.461] | 0.033 [-0.024, 0.098] | 0.516 (263/510) |
| Test-B | date only | 0.100 [0.063, 0.146] | 0.049 [0.022, 0.079] | 0.051 [0.022, 0.090] | 0.516 (263/510) |
| unseen-filer | strict (date + type) | 0.417 [0.345, 0.503] | 0.329 [0.258, 0.412] | 0.088 [0.022, 0.159] | 0.520 (231/444) |
| unseen-filer | date only | 0.153 [0.091, 0.238] | 0.078 [0.035, 0.137] | 0.075 [0.032, 0.135] | 0.520 (231/444) |

## (c) Repetition: near-duplicate chronology entries vs agent accepted error
Per filing, the chronology is split into sentences with the labelling sentence splitter; sentences of at least 4 words are normalised (dates, digits and punctuation removed, lower case); the repeat share = entries whose normalised text already occurred earlier in the same filing / all such entries. Pooled over the three splits (the split of each filing is not shown); manufacturers with at least 15 accepted event claims, sorted by accepted claims. Accepted error = accepted-wrong / accepted; B2 error = wrong / all event claims of that manufacturer's filings.

| manufacturer | filings | chronology entries | repeat share within a filing | repeat share across other filings of the same manufacturer (extra column) | accepted claims | accepted error | B2 error |
|---|---|---|---|---|---|---|---|
| chrysler (fca us, llc) | 22 | 117 | 0.000 | 0.256 | 76 | 0.197 | 0.284 |
| ford motor company | 30 | 367 | 0.000 | 0.327 | 49 | 0.571 | 0.476 |
| forest river, inc. | 12 | 58 | 0.000 | 0.138 | 35 | 0.257 | 0.267 |
| mercedes-benz usa, llc | 11 | 127 | 0.000 | 0.047 | 31 | 0.258 | 0.469 |
| nova bus (us) inc. | 5 | 57 | 0.018 | 0.228 | 28 | 0.286 | 0.293 |
| tesla, inc. | 5 | 36 | 0.000 | 0.000 | 24 | 0.083 | 0.138 |
| wabash national corporation | 4 | 33 | 0.000 | 0.000 | 23 | 0.174 | 0.143 |
| volkswagen group of america, inc. | 5 | 63 | 0.063 | 0.000 | 23 | 0.130 | 0.184 |
| jayco, inc. | 5 | 36 | 0.000 | 0.111 | 22 | 0.682 | 0.708 |
| honda (american honda motor co.) | 6 | 55 | 0.055 | 0.091 | 22 | 0.045 | 0.217 |
| terex south dakota, inc. | 4 | 27 | 0.000 | 0.074 | 22 | 0.227 | 0.217 |
| altec industries, inc. | 10 | 82 | 0.000 | 0.134 | 22 | 0.136 | 0.304 |
| daimler trucks north america, llc | 5 | 50 | 0.000 | 0.000 | 21 | 0.429 | 0.516 |
| paccar incorporated | 2 | 37 | 0.027 | 0.000 | 21 | 0.619 | 0.640 |
| lucid usa, inc. | 5 | 56 | 0.000 | 0.000 | 21 | 0.571 | 0.667 |
| bmw of north america, llc | 8 | 79 | 0.000 | 0.139 | 20 | 0.400 | 0.531 |
| international motors, llc | 5 | 55 | 0.000 | 0.182 | 18 | 0.444 | 0.405 |
| prevost car (us) inc. | 4 | 57 | 0.035 | 0.456 | 18 | 0.222 | 0.233 |
| rev recreation group | 3 | 50 | 0.000 | 0.000 | 17 | 0.412 | 0.472 |
| navistar, inc. | 3 | 28 | 0.000 | 0.071 | 15 | 0.400 | 0.348 |

Filing-level association (Spearman rank correlation between a filing's repeat share and its accepted error; filings with at least 3 accepted claims; descriptive, no p-value):

| split | filings | filings with any repeated entry | Spearman rho | mean accepted error: repeat share > 0.2 / <= 0.2 |
|---|---|---|---|---|
| Test-A (primary) | 96 | 7 | -0.12 | nan (n=0) / 0.262 (n=96) |
| Test-B | 51 | 1 | -0.20 | nan (n=0) / 0.366 (n=51) |
| unseen-filer | 39 | 3 | 0.09 | nan (n=0) / 0.320 (n=39) |

## (d) Conclusion (two sentences)

Mostly type disagreement: in Test-B 80 of the 93 accepted-wrong event claims (86%) have a date that matches a gold event of the same filing but a different type, only 13 (14%) have a date that matches no gold event or cannot be parsed, and ignoring type the Test-B delta is 0.051 [0.022, 0.090] with accepted error 0.049, so wrong or invented dates do not drive the Test-B shortfall. The data cannot say whether those type disagreements are the agent mistyping events or silver labelling conventions (both are AI judgements, none human-verified), and the date-only view is lenient (a date can coincide with an unrelated gold event), so it understates date errors somewhat.

Notes: (1) The pattern is the same on Test-A (85% type-only) and unseen-filer (75%); Test-B's smaller delta comes with a higher strict accepted error, not with more date errors. (2) Within a filing, near-duplicate entries are almost absent (repeat share about 0 for Ford, Jayco and most manufacturers; only 2 accepted-wrong claims are duplicates, both in unseen-filer), and the filing-level correlation between repeat share and accepted error is about 0. (3) **Correction to `reports/phase_6_secondary_splits.md` section 3**, which described Ford and Jayco as having 'repeated' chronologies: that is supported only across filings of the same manufacturer for Ford (about 33% of its entries recur in another Ford filing, e.g. the shared software-recall text of 26V369/370/374; FCA also shows about 26% with a low accepted error of 0.197, and Jayco about 11%), not within filings, and the data do not show that repetition causes the errors. (4) The class counts, date-only view and repetition shares are descriptive; nothing here was tuned, rerun or changed.

## (e) Type-ambiguity ceiling: labeller vs labeller, next to the agent (POST HOC, EXPLORATORY)
Existing label files only (`data/labels/<split>_passA.json`, `_passB.json`, final silver); no model call. Same matching rule as the frozen scorer: an event is date-matched if its date span coarsely overlaps a non-fuzzy event of the other side in the same filing, and its type agrees if any overlapping event has the same type (lenient for both sides). Dates of both passes are parsed with the same guarded parser and the filing's chronology-year context; undated, inferred or unparseable events take no part. Labellers: every Pass A event that is date-matched to Pass B (A->B; B->A shown too). Agent: every accepted run-1 event claim (the H1 accepted set) that is date-matched to the final scoring labels, so agent agreement = 1 - share of class (i) among date-matched accepted claims (duplicates included). Wilson 95% intervals; manufacturers by the filer name in the header.

**Test-A (primary)**

| manufacturer | Pass A vs Pass B type agreement (A->B) | (B->A) | agent vs final label, date-matched accepted claims |
|---|---|---|---|
| Ford | 0.685 [0.571, 0.780] (50/73) | 0.750 [0.632, 0.840] (48/64) | 0.769 [0.497, 0.918] (10/13) |
| Jayco | 0.750 [0.301, 0.954] (3/4) | 0.750 [0.301, 0.954] (3/4) | 0.333 [0.061, 0.792] (1/3) |
| PACCAR | 0.825 [0.680, 0.913] (33/40) | 0.757 [0.599, 0.866] (28/37) | 0.400 [0.219, 0.613] (8/20) |
| FCA | 0.750 [0.623, 0.845] (42/56) | 0.745 [0.617, 0.842] (41/55) | 0.818 [0.680, 0.905] (36/44) |
| other | 0.798 [0.769, 0.824] (653/818) | 0.787 [0.757, 0.814] (602/765) | 0.777 [0.736, 0.814] (338/435) |
| **all** | 0.788 [0.762, 0.812] (781/991) | 0.781 [0.753, 0.806] (722/925) | 0.763 [0.725, 0.798] (393/515) |

**Test-B**

| manufacturer | Pass A vs Pass B type agreement (A->B) | (B->A) | agent vs final label, date-matched accepted claims |
|---|---|---|---|
| Ford | 0.671 [0.561, 0.764] (53/79) | 0.645 [0.533, 0.743] (49/76) | 0.355 [0.211, 0.531] (11/31) |
| Jayco | 0.897 [0.736, 0.964] (26/29) | 0.897 [0.736, 0.964] (26/29) | 0.333 [0.163, 0.563] (6/18) |
| PACCAR | n/a (0) | n/a (0) | n/a (0) |
| FCA | 0.595 [0.445, 0.730] (25/42) | 0.756 [0.607, 0.862] (31/41) | 0.815 [0.633, 0.918] (22/27) |
| other | 0.825 [0.782, 0.861] (293/355) | 0.781 [0.735, 0.822] (268/343) | 0.753 [0.684, 0.811] (131/174) |
| **all** | 0.786 [0.748, 0.820] (397/505) | 0.765 [0.725, 0.800] (374/489) | 0.680 [0.620, 0.735] (170/250) |

**unseen-filer**

| manufacturer | Pass A vs Pass B type agreement (A->B) | (B->A) | agent vs final label, date-matched accepted claims |
|---|---|---|---|
| Ford | n/a (0) | n/a (0) | n/a (0) |
| Jayco | n/a (0) | n/a (0) | n/a (0) |
| PACCAR | n/a (0) | n/a (0) | n/a (0) |
| FCA | 0.667 [0.208, 0.939] (2/3) | 1.000 [0.438, 1.000] (3/3) | 1.000 [0.438, 1.000] (3/3) |
| other | 0.828 [0.789, 0.862] (338/408) | 0.822 [0.782, 0.857] (324/394) | 0.724 [0.660, 0.780] (152/210) |
| **all** | 0.827 [0.788, 0.861] (340/411) | 0.824 [0.783, 0.858] (327/397) | 0.728 [0.664, 0.783] (155/213) |

Most frequent type disagreements (unordered pairs; a disagreeing event is paired with the most frequent type among the events it overlaps), pooled over the three splits, with the per-split counts:

(a) Pass A vs Pass B: 389 disagreements

| type pair | count | share of disagreements | Test-A | Test-B | unseen |
|---|---|---|---|---|---|
| INVESTIGATION_START / OTHER | 128 | 32.9% | 68 | 34 | 26 |
| FILER_AWARENESS / OTHER | 126 | 32.4% | 67 | 42 | 17 |
| DECISION / OTHER | 59 | 15.2% | 28 | 15 | 16 |
| FILER_AWARENESS / INVESTIGATION_START | 25 | 6.4% | 16 | 7 | 2 |
| NHTSA_FILING / OTHER | 19 | 4.9% | 9 | 6 | 4 |
| OTHER / SUPPLIER_NOTICE | 12 | 3.1% | 7 | 2 | 3 |

(b) agent (accepted claims) vs final label: 260 disagreements

| type pair | count | share of disagreements | Test-A | Test-B | unseen |
|---|---|---|---|---|---|
| INVESTIGATION_START / OTHER | 102 | 39.2% | 47 | 34 | 21 |
| FILER_AWARENESS / INVESTIGATION_START | 54 | 20.8% | 26 | 20 | 8 |
| FILER_AWARENESS / OTHER | 33 | 12.7% | 13 | 7 | 13 |
| DECISION / FILER_AWARENESS | 15 | 5.8% | 8 | 5 | 2 |
| FILER_AWARENESS / SUPPLIER_NOTICE | 14 | 5.4% | 6 | 5 | 3 |
| DECISION / OTHER | 11 | 4.2% | 5 | 1 | 5 |

**Plain reading.** The agent's type agreement with the final labels, on date-matched accepted claims, compared with Pass A's type agreement with Pass B on date-matched events: Test-A (primary): agent 76.3% vs labellers 78.8%, i.e. similar to (the intervals overlap); Test-B: agent 68.0% vs labellers 78.6%, i.e. below; unseen-filer: agent 72.8% vs labellers 82.7%, i.e. below. 4 of the agent's 6 most frequent confusions are also among the labellers' 6 most frequent (INVESTIGATION_START / OTHER, FILER_AWARENESS / INVESTIGATION_START, FILER_AWARENESS / OTHER, DECISION / OTHER), so the two disagree over largely the same type boundaries. On Test-A the agent's type disagreement is at about the level two AI labellers already have with each other on the same dates; on Test-B and unseen-filer it is larger. The labeller rate indicates how ambiguous these type boundaries are, but it is not a hard ceiling (an extractor could agree with the adjudicated labels more often than two raw passes agree with each other). Two differences stand out. FILER_AWARENESS / INVESTIGATION_START is a much larger share of the agent's confusions (21%) than of the labellers' (6%), which matches the logged rule gap for sentences that report both awareness and the start of an investigation. And on Test-B the gap is concentrated where the labellers did not find the types ambiguous: for Jayco the two passes agree 26/29 but the agent only 6/18; for Ford the passes agree 53/79 and the agent 11/31 (small numbers, wide intervals). That part of the Test-B shortfall is therefore not explained by label ambiguity as measured here; it points more to the agent's typing (or to how the adjudicated labels typed these filers), though the data cannot separate those two.

**Caveats.** The labels are not independent: Pass C sided with Pass B in 72-78% of its items (Test-A 73.5%, Test-B 72.2%, unseen 77.6%), the final labels are Pass A plus Pass C's corrections, and Pass B and Pass C are both Opus; the agent's event-type definitions were copied from the labelling rules (a disclosed bias in the agent's favour). The labeller rate compares two raw passes before adjudication, the agent rate compares with the adjudicated labels, so the two are not measured against the same reference. Matching is lenient on both sides (any overlapping event of the same type counts). Nothing here is a label-error figure; none of it is human-verified.
