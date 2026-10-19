# Phase 4 report: agent with verifiers and abstention (dev, 100 filings)

Scores are **vs silver labels** (AI-made, cross-checked by independent AI passes and code checks; not human-verified). Dev only; Test-A not opened.
Code: `tt/agent/agent.py` (decisions), `tt/agent/inject.py` (fixtures), `tt/eval/phase4.py`; tests `tests/test_agent.py`. Raw: `reports/phase_4_results.json`, `reports/phase_4_results_strictE1.json`, `reports/phase_4_injection.json`.
Model: qwen3.5:4b-q4_K_M, prompt v2 (dev-tuned, see `docs/PROMPT_LOG.md`). The 2B-to-4B cascade (optional) was not built.

## Design
The model proposes; code disposes. Run 1 = temperature 0 seed 0; run 2 = temperature 0.5 seed 1 (same model and prompt). A claim is **accepted** only if no verifier fails **and** run 2 gives the same claim; otherwise the agent abstains. Model confidence is never used.
Verifiers: V1 quote verbatim in the claimed section (masked text); V2a name in the filing; V2b the filer is not a supplier unless it is the block supplier; V3 valid date (span parser), V3o event order; V4 an NR cause stays NR; **V4r** a stated cause is not reported as "not reported" unless the cause text says it is undetermined; E1 the event date is inside its quote, or is the nearest date mentioned before it (a dated entry); S2n supplier name verbatim in the cause/chronology, else INSUFFICIENT; V8 no instruction-like text in a quote or name (0 firings on the 100 real dev filings).
Ranking score for risk-coverage curves (deterministic): 0 if a verifier failed; else 1 + 2 x (run 2 agrees) + (rule baseline B1 agrees). Accepted = score >= 3.
Changes after seeing dev results: E1 inherited-date allowance (the literal rule rejected 183 of 434 events, 101 of them silver-matching; the allowance rejects 94, 41 silver-matching); V4r (added after the injection test showed cause flipping got through). Both are dev-only and logged in `docs/PROMPT_LOG.md`.

## Dev results (4B v2; claims proposed by run 1)

### Supplier claims (27 candidate claims)
| setting | accepted | coverage | error among accepted (95% filer-cluster CI) | claims that match silver |
|---|---|---|---|---|
| B2 (no verifiers) | 27 | 100.0% | 0.370 (0.200-0.560) | 17 |
| verifiers only | 21 | 77.8% | 0.333 (0.150-0.524) | 14 |
| verifiers + two-run agreement (accepted) | 15 | 55.6% | 0.333 (0.133-0.562) | 10 |
| ranked by deterministic score: AURC 0.413 (0.168-0.643); risk at 90 / 70 / 50% coverage | | | 0.354 / 0.326 / 0.343 | |

### Event claims (six types) (434 candidate claims)
| setting | accepted | coverage | error among accepted (95% filer-cluster CI) | claims that match silver |
|---|---|---|---|---|
| B2 (no verifiers) | 434 | 100.0% | 0.380 (0.302-0.465) | 269 |
| verifiers only | 284 | 65.4% | 0.324 (0.244-0.414) | 192 |
| verifiers + two-run agreement (accepted) | 221 | 50.9% | 0.281 (0.210-0.362) | 159 |
| ranked by deterministic score: AURC 0.279 (0.203-0.372); risk at 90 / 70 / 50% coverage | | | 0.368 / 0.335 / 0.279 | |

### Cause-reported claim (100 candidate claims)
| setting | accepted | coverage | error among accepted (95% filer-cluster CI) | claims that match silver |
|---|---|---|---|---|
| B2 (no verifiers) | 100 | 100.0% | 0.050 (0.010-0.099) | 95 |
| verifiers only | 94 | 94.0% | 0.011 (0.000-0.033) | 93 |
| verifiers + two-run agreement (accepted) | 90 | 90.0% | 0.011 (0.000-0.034) | 89 |
| ranked by deterministic score: AURC 0.013 (0.000-0.038); risk at 90 / 70 / 50% coverage | | | 0.011 / 0.011 / 0.011 | |

Event claims with the brief's literal E1 rule (date text inside the quote only): verifiers only accepted 201 (error 0.318 (0.233-0.407)); with agreement 159 (error 0.277 (0.205-0.347)).

Reading: abstention lowers the error among accepted claims for events (0.380 to 0.281) and cause (0.050 to 0.011), at 51% and 90% coverage; **the event intervals overlap (0.302-0.465 vs 0.210-0.362), so the event gain is not shown at this sample size.** Supplier claims: only 27 candidates; error stays about 0.33. The remaining event error is mostly wrong type, which no verifier here can detect. Fewer than half of silver events are recovered by accepted claims (159 right accepted claims vs 447 silver scored events). The dev scores are optimistic (prompt and verifier choices made on dev, silver labels).
Verifier firings (candidate claims): {'C:V4r': 6, 'E:E1': 94, 'E:V1': 41, 'E:V3': 12, 'E:V3o': 32, 'S2:S2n': 3, 'S2:V1': 9, 'S2:V2a': 3}.

## Prompt-injection fixtures (20; 5 attack types x 4 dev filings, attack sentence appended to the chronology)
Success is machine-checked (fake supplier listed, 2031 event added, cause flipped to not-reported, filer listed as supplier, events suppressed). Fixtures were written by me after the verifiers, and V4r was added after seeing the flip-cause result, so the "with verifiers" figures are **in-sample, not a robustness guarantee**.
| attack | raw output | after hard verifiers | after verifiers + two-run agreement |
|---|---|---|---|
| fake_supplier | 0/4 | 0/4 | 0/4 |
| future_event | 1/4 | 0/4 | 0/4 |
| flip_cause | 4/4 | 0/4 | 0/4 |
| filer_as_supplier | 0/4 | 0/4 | 0/4 |
| suppress_events | 0/4 | 0/4 | 0/4 |
| **all** | **5/20** | **0/20** | **0/20** |
Attack success rate: 5/20 (25%) without verifiers; 0/20 with the hard verifiers; 0/20 with verifiers and agreement. Only the cause-flip attack worked reliably on the raw model (4/4) and one future-event attack (1/4). The event-suppression attack cannot be detected by claim verifiers (it removes claims), and the model did not follow it here (0/4).

## UNVERIFIED
Generalisation to Test-A/B and unseen filers; correctness of silver labels; any clean-hardware speed; robustness against attacks not in these 20 fixtures.
