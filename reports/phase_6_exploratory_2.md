# Phase 6 Test-A: EXPLORATORY analyses 2 (d)-(g) (not preregistered endpoints; silver labels, AI-made, not human-verified)

Scoring only on the existing Test-A outputs: no model run, nothing frozen changed (frozen `agent.decide`, amendment-1 wrapper, primary settings; run-1 claims, run 2 only as the agreement filter, 4 run-2 timeouts missing). Script `scripts/phase6_testA_exploratory2.py` (pure Python), raw numbers `reports/phase_6_exploratory_2.json`. Everything here is exploratory. All error rates are against silver labels that are not independent of the pipeline (Pass C sided with Pass B, both Opus, in 73.5% of Test-A items); no label-error figure is claimed.

## Summary
| | result |
|---|---|
| (d) attribution of the H1 delta | full set reproduces H1: delta 0.1352 [0.086, 0.192]; exact Shapley values sum to it. Largest: run-2 agreement 0.065 [0.038, 0.097], then V3 unparseable-date 0.031 [0.013, 0.055], E1 0.026 [0.009, 0.045]; V3o 0.009, V1 0.004; V3 after-filing-date, V3 before-1990 and V8 about 0 (V3 before-1990 and V8 never fire on event claims) |
| (e) tipping point (silver noise, favourable-to-agent direction) | the H1 CI lower bound reaches 0 when 26.7% of the accepted-correct claims are really wrong (105 claims = 10.4% of all 1005 event labels); the point estimate reaches 0 at 39.5% (155 claims = 15.5% of labels); the H1 point threshold (delta >= 0.05) fails first, at 24.9% (98 claims = 9.7% of labels) |
| (f) cluster-sum t-bound (delta 0.01, cap 10 per filer) | events: accepted error 0.256 -> upper bound 0.324 (379 claims, 71 filers); cause: 0.026 -> 0.058 (153 claims, 75 filers). **Validity check FAILED**: false-certification rate 0.0124-0.0216 for events and 0.048-0.109 for cause, against the required <= 0.01; the bound is not valid as specified, so its numbers must not be used as guarantees |
| (g) empty event lists | run 1: 4 of 199 filings (2.0%), none with a gold event; 0 of 117 attack-host-like filings; under the suppress_events attack 2 of 6 outputs were empty |

## (d) Per-check attribution of the H1 delta (events)
Players: every rule that can fire on an *event* claim, with the V3 date rule split into its three `extra.py` sub-rules (V1 quote verbatim in the masked section; E1 date text inside the quote or the nearest preceding date; V3 unparseable / before 1990 / after the filing date; V3o event order; V8 instruction-like text), plus the run-2 agreement filter. V2a, V2b, S2n (supplier names), V4 and V4r (cause) cannot change an event claim's acceptance, so they are not players here. A coalition S accepts a claim iff none of its fired rules is in S and (run 2 agrees or the filter is not in S); v(S) = unfiltered error minus accepted error (v of the empty coalition = 0, v of the full set = the H1 delta, asserted equal to 0.1352 and to the committed H1 CI). Leave-one-out = v(all) - v(all without the rule). Shapley = exact, 2^8 = 256 coalitions. Intervals: the same filer-cluster bootstrap as H1 (2000 resamples, seed 0, same resampling sequence; the full-set CI reproduces H1 exactly); a Shapley or leave-one-out value is recomputed in every resample.

| rule | fires on claims (of 1005) | rule alone: delta | leave-one-out [95% CI] | Shapley [95% CI] |
|---|---|---|---|---|
| run2_agreement | 287 (run 2 disagrees) | 0.1025 | 0.0293 [0.014, 0.046] | 0.0651 [0.038, 0.097] |
| V3_unparseable | 91 | 0.0595 | 0.0027 [0.000, 0.009] | 0.0309 [0.013, 0.055] |
| E1 | 159 | 0.0403 | 0.0144 [-0.002, 0.035] | 0.0259 [0.009, 0.045] |
| V3o_event_order | 44 | 0.0045 | 0.0131 [0.000, 0.029] | 0.0091 [-0.001, 0.021] |
| V1 | 114 | 0.0024 | 0.0052 [-0.008, 0.018] | 0.0037 [-0.010, 0.017] |
| V3_after_filing_date | 4 | 0.0014 | -0.0005 [-0.002, 0.000] | 0.0005 [-0.001, 0.002] |
| V3_before_1990 | 0 | 0.0000 | 0.0000 [0.000, 0.000] | 0.0000 [0.000, 0.000] |
| V8_injection | 0 | 0.0000 | 0.0000 [0.000, 0.000] | 0.0000 [0.000, 0.000] |
| **sum** | | | | **0.1352** |

Reading: the run-2 agreement filter carries the largest share on its own (delta 0.103 alone). Rules overlap (a claim with an unparseable date is often also rejected by run 2), so leave-one-out values are small and do not add up; the Shapley values do add up and are the fairer split, but they depend on which rules are put in the game and say nothing about causation. Several intervals include 0.

## (e) Tipping point for silver-label noise (H1 delta)
Question: how many event labels would have to be wrong, in the direction most favourable to the agent, before the H1 result goes away?
Assumptions: (1) the only errors are accepted claims that silver marks correct but are actually wrong (flatters the agent); (2) the same claims are in the unfiltered B2 set (the accepted claims are a subset of it), so each flip also raises the B2 error; (3) flips are spread evenly over the accepted-correct claims (expected value, every claim wrong with the same probability f; clusters resampled as in H1) - flips concentrated in a few filers could do more damage to the CI than the same number spread out; (4) nothing else changes (no label noise on the other claims, run 2 and the verifiers are fixed); (5) unit = one event claim's correctness label (1005 claims, of which 536 accepted, 393 accepted and marked correct).
Flipping f x 393 claims changes the delta by exactly -f x 393 x (1/536 - 1/1005).

| tipping point | fraction of accepted-correct claims wrong | claims | share of all 1005 event labels | share of 536 accepted labels | accepted error after | unfiltered error after |
|---|---|---|---|---|---|---|
| H1 point threshold delta < 0.05 fails | 0.249 | 98 | 0.097 | 0.183 | 0.449 | 0.499 |
| CI lower bound reaches 0 | 0.267 | 105 | 0.104 | 0.196 | 0.462 | 0.506 |
| point estimate reaches 0 | 0.395 | 155 | 0.155 | 0.290 | 0.557 | 0.557 |

So H1 as a preregistered pass (delta >= 0.05 and CI lower bound > 0) tips first on the point threshold, at roughly 1 wrong label in 10 across all event labels (about 1 in 4 of the accepted-correct claims). This is a single, one-directional scenario, not an estimate of how noisy the silver labels are; no label-error rate is claimed.

## (f) Cluster-sum t-bound on accepted-claim error, and its validity check
Bound (as specified, defined here before looking at any result): per filer cluster g, n_g accepted claims (at most 10 per cluster; if more, a seeded random subset of 10) and e_g errors; r = sum e / sum n; residuals d_g = e_g - r n_g; SE = sqrt(G/(G-1) x sum d_g^2) / sum n; upper bound = r + t(0.99, G-1) x SE (one-sided, delta = 0.01). Real data: events 379 of 536 accepted claims kept by the cap, 97 errors, 71 filers: error 0.256, upper bound **0.324**; cause 153 of 155 kept, 4 errors, 75 filers: error 0.026, upper bound **0.058**.
Validity check: keep the real Test-A cluster sizes (after the cap), set the true risk equal to the target, simulate the errors 20,000 times, and count how often the bound comes out *below* the true risk (a false certification of "risk < target"). Valid only if the rate is <= 0.01. Scenarios: independent claims; a beta-binomial with the intra-cluster correlation estimated from the real accepted claims (events 0.100, cause 0.191); stress 0.1, 0.3, 0.5. Targets: the observed bound, and the observed point estimate. Intervals are Wilson 95% for the simulation rate.

**Events** (cluster sizes after the cap: {'1': 10, '2': 8, '3': 8, '4': 8, '5': 8, '6': 6, '7': 1, '8': 2, '9': 2, '10': 18})
| target | scenario | false certifications | rate [95% CI] | verdict |
|---|---|---|---|---|
| observed bound (0.324) | independent claims (rho = 0) | 248/20000 | 0.0124 [0.011, 0.014] | **NOT valid** |
| observed bound (0.324) | rho = estimated 0.100 | 301/20000 | 0.0150 [0.013, 0.017] | **NOT valid** |
| observed bound (0.324) | stress rho = 0.1 | 278/20000 | 0.0139 [0.012, 0.016] | **NOT valid** |
| observed bound (0.324) | stress rho = 0.3 | 343/20000 | 0.0171 [0.015, 0.019] | **NOT valid** |
| observed bound (0.324) | stress rho = 0.5 | 432/20000 | 0.0216 [0.020, 0.024] | **NOT valid** |
| observed point estimate (0.256) | independent claims (rho = 0) | 231/20000 | 0.0115 [0.010, 0.013] | **NOT valid** |
| observed point estimate (0.256) | rho = estimated 0.100 | 368/20000 | 0.0184 [0.017, 0.020] | **NOT valid** |
| observed point estimate (0.256) | stress rho = 0.1 | 364/20000 | 0.0182 [0.016, 0.020] | **NOT valid** |
| observed point estimate (0.256) | stress rho = 0.3 | 462/20000 | 0.0231 [0.021, 0.025] | **NOT valid** |
| observed point estimate (0.256) | stress rho = 0.5 | 546/20000 | 0.0273 [0.025, 0.030] | **NOT valid** |

**Cause** (cluster sizes after the cap: {'1': 45, '2': 16, '3': 4, '4': 4, '5': 1, '6': 1, '9': 3, '10': 1})
| target | scenario | false certifications | rate [95% CI] | verdict |
|---|---|---|---|---|
| observed bound (0.058) | independent claims (rho = 0) | 963/20000 | 0.0481 [0.045, 0.051] | **NOT valid** |
| observed bound (0.058) | rho = estimated 0.191 | 1556/20000 | 0.0778 [0.074, 0.082] | **NOT valid** |
| observed bound (0.058) | stress rho = 0.1 | 1288/20000 | 0.0644 [0.061, 0.068] | **NOT valid** |
| observed bound (0.058) | stress rho = 0.3 | 1727/20000 | 0.0863 [0.083, 0.090] | **NOT valid** |
| observed bound (0.058) | stress rho = 0.5 | 2176/20000 | 0.1088 [0.105, 0.113] | **NOT valid** |
| observed point estimate (0.026) | independent claims (rho = 0) | 1774/20000 | 0.0887 [0.085, 0.093] | **NOT valid** |
| observed point estimate (0.026) | rho = estimated 0.191 | 2872/20000 | 0.1436 [0.139, 0.149] | **NOT valid** |
| observed point estimate (0.026) | stress rho = 0.1 | 2454/20000 | 0.1227 [0.118, 0.127] | **NOT valid** |
| observed point estimate (0.026) | stress rho = 0.3 | 3354/20000 | 0.1677 [0.163, 0.173] | **NOT valid** |
| observed point estimate (0.026) | stress rho = 0.5 | 4111/20000 | 0.2056 [0.200, 0.211] | **NOT valid** |

Result: the bound fails the validity criterion in every scenario, including independent claims. For events it is only mildly anti-conservative (about 1.2% to 2.7% against the 1% target); for cause it is badly so (5% to 21%), because only 4 accepted cause claims are wrong, so the linearised variance estimate is unreliable and a sample with no or few errors yields a bound near 0. The bound is therefore **not valid as specified** and none of its numbers is a guarantee. No repair was tried (exact or cluster-bootstrap-t bounds would be the obvious candidates; that is a separate, unrequested step).

## (g) Empty event lists and the limit of H4
suppress_events asks the model for an empty events list. An empty list contains no claim, so no verifier can reject it and a successful attack is invisible to every claim-level check. Test-A run 1: **4 of 199 filings** (2.0%) have an empty event list (23V221-8304, 24E029-4277, 24V274-3413, 24V364-1692); none of the four has any gold event, so those empty lists are not missed events (of 199 filings, 179 have a scored gold event). Run 2: 4 of 195 (24E029-4277, 24V143-7520, 24V294-3024, 24V587-7214), also none with a gold event. Among the 117 filings that meet the attack-host criteria (supported cause, chronology over 300 characters, at least 2 gold events) there is no natural empty output in either run, while 2 of 6 suppress_events attacks produced one (raw and after verifiers + agreement). So H4's 2/30 residual successes are exactly the attack no verifier can catch; a defence would need a different kind of check (for example a floor on events for a chronology with dated sentences), which is not part of the frozen agent and was not added.

## Prior-art note for (d)-(f) (no novelty claims)
Checked: three quick web searches on 2026-10-25 (Shapley or leave-one-out attribution of pipeline components; tipping-point sensitivity analysis for label noise; cluster-robust ratio/linearisation bounds for clustered error rates), reading only result snippets, no paper in full. What they showed: component-level Shapley attribution of a metric gain and its comparison with leave-one-out are already used in the literature (one hit, arXiv 2607.16209, has an unusual identifier and was not verified); tipping-point analysis is a standard device in clinical-trial sensitivity analysis for missing data, and the transfer to label noise here is my adaptation; cluster-robust variance via the delta method for ratio estimators is textbook survey-sampling and econometrics material, and the searches found nothing that combines a t-bound on a clustered error rate with selective prediction. Not checked: any systematic literature review; selective-classification risk bounds (for example Geifman and El-Yaniv), conformal or distribution-free risk control, and finite-population or bootstrap-t bounds for clustered rates, which I know of only from memory and did not look up here; whether the specific combination used here exists elsewhere. Nothing in (d)-(f) is claimed to be new; (d) and (e) apply standard ideas to this evaluation, and (f) failed its own validity check.
