# Phase 3 report: baselines and harness (dev, 100 filings)

Scores are **vs silver labels** (AI-made, cross-checked by independent AI passes and code checks; not human-verified). Dev only; Test-A not opened.
Code: `tt/eval/riskcov.py` (risk-coverage curves, AURC, filer-cluster bootstrap: 2,000 resamples, seed 0), `tt/eval/phase3.py`, `tt/baselines/rules.py`.
Raw numbers: `reports/phase_3_results.json`. Tests: `tests/test_riskcov.py`.

## Systems
- **B0**: most common value per claim type (cause_reported = True; no companies, no events).
- **B1**: rules/regex only, on the same masked text (`tt/baselines/rules.py`; written once before first dev run, never tuned; see `reports/phase_2_diagnosis.md`).
- **B2**: one LLM pass, no verifier, no abstention: 4B v1, 2B v1 (original prompt) and 4B v2 (prompt revised after seeing dev results; dev-optimistic, see `docs/PROMPT_LOG.md`).
Speed numbers for B2 are in `reports/phase_2_diagnosis.md` (measured with Claude Code and other apps open).

## Method
Claim = what the system asserts. Supplier claims: each SUPPORTED supplier-role company; correct if it matches a silver S1/S2/upstream name; companies named in the text that silver has no claim on are *unlabelled* and excluded (counts in the JSON). Event claims: each predicted event; correct if a silver event has an overlapping date and the same type (any of six types; unparseable date = wrong). Cause: per filing, `cause_reported` equals (silver cause SUPPORTED).
Error = share of accepted claims that are wrong. **No baseline ranks its claims, so every coverage level has the same expected error (ties are included fractionally); the risk at 50/70/90% equals the error at 100% and AURC equals it.** The harness is tested and ready for a ranking score (Phase 4). The intervals resample filers, not claims.

### Supplier claims (S2-type: SUPPORTED supplier/sub-supplier/distributor companies)
| system | claims | error among accepted at 100% coverage (95% filer-cluster CI) | risk at 90 / 70 / 50% coverage | AURC |
|---|---|---|---|---|
| B0 | 0 | n/a (makes no such claims) | n/a | n/a |
| B1 | 10 | 0.700 (0.333-1.000) | 0.700 / 0.700 / 0.700 | 0.700 |
| B2_4b_v1 | 151 | 0.834 (0.769-0.892) | 0.834 / 0.834 / 0.834 | 0.834 |
| B2_2b_v1 | 187 | 0.856 (0.793-0.907) | 0.856 / 0.856 / 0.856 | 0.856 |
| B2_4b_v2 | 27 | 0.370 (0.200-0.560) | 0.370 / 0.370 / 0.370 | 0.370 |

### Event claims (all six types)
| system | claims | error among accepted at 100% coverage (95% filer-cluster CI) | risk at 90 / 70 / 50% coverage | AURC |
|---|---|---|---|---|
| B0 | 0 | n/a (makes no such claims) | n/a | n/a |
| B1 | 246 | 0.476 (0.391-0.564) | 0.476 / 0.476 / 0.476 | 0.476 |
| B2_4b_v1 | 341 | 0.777 (0.716-0.832) | 0.777 / 0.777 / 0.777 | 0.777 |
| B2_2b_v1 | 401 | 0.733 (0.629-0.823) | 0.733 / 0.733 / 0.733 | 0.733 |
| B2_4b_v2 | 434 | 0.380 (0.302-0.465) | 0.380 / 0.380 / 0.380 | 0.380 |

### Cause-reported claim (per filing)
| system | claims | error among accepted at 100% coverage (95% filer-cluster CI) | risk at 90 / 70 / 50% coverage | AURC |
|---|---|---|---|---|
| B0 | 100 | 0.300 (0.210-0.390) | 0.300 / 0.300 / 0.300 | 0.300 |
| B1 | 100 | 0.050 (0.010-0.100) | 0.050 / 0.050 / 0.050 | 0.050 |
| B2_4b_v1 | 100 | 0.020 (0.000-0.051) | 0.020 / 0.020 / 0.020 | 0.020 |
| B2_2b_v1 | 100 | 0.060 (0.020-0.110) | 0.060 / 0.060 / 0.060 | 0.060 |
| B2_4b_v2 | 100 | 0.050 (0.010-0.099) | 0.050 / 0.050 / 0.050 | 0.050 |

## Reading (plain)
- **B1 beats the original LLM runs on events** (error 0.476 vs 0.777 for 4B v1 and 0.733 for 2B v1, intervals do not overlap), and has far fewer supplier claims that are wrong (0.70 on only 10 claims vs 0.83-0.86 on 151-187).
- **B1 matches the LLM on cause**: 0.050 vs 0.020 (4B v1) and 0.060 (2B v1); all intervals overlap.
- **4B v2 beats B1 on events point-wise (0.380 vs 0.476) but the intervals overlap** (0.302-0.465 vs 0.391-0.564), so a win is not shown. Its supplier claims drop to 27 with error 0.37 (0.20-0.56).
- Recall is not in these error numbers: of the 447 silver events, date+type matched 113 (B1), 60 (4B v1), 65 (2B v1), 233 (4B v2); supplier names recovered with a verbatim quote: B1 1/24, 4B 11/24, 2B 11/24, 4B v2 11/24.
- B0 has no supplier or event claims, so its only error is cause (0.300).

## UNVERIFIED
Whether these results hold on Test-A (not opened); correctness of the silver labels themselves; any speed on clean hardware.
