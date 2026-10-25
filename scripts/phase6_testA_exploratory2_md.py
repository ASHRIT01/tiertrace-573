"""Renders reports/phase_6_exploratory_2.md from reports/phase_6_exploratory_2.json (no new computation except the closed-form H1-point-threshold tipping line)."""
import json

R = json.load(open("reports/phase_6_exploratory_2.json"))
d, e, f, g = R["d_attribution"], R["e_tipping"], R["f_bound"], R["g_empty"]
ci = lambda c: f"[{c[0]:.3f}, {c[1]:.3f}]"
P = d["players"]
order = sorted(P, key=lambda p: -P[p]["shapley"])
# tipping for the H1 point threshold (delta >= 0.05): delta(f) = d0 - f*CA*(1/NA - 1/N), linear in f
N, NA, CA, d0 = e["claims"], e["accepted"], e["accepted_correct"], e["delta"]
f05 = (d0 - 0.05) / (CA * (1 / NA - 1 / N)); k05 = f05 * CA
ev, ca = f["events"], f["cause"]
pe, cl = e["point_estimate_tipping"], e["ci_lower_bound_tipping"]
WA = pe["accepted_error_after"] * NA - pe["claims_flipped"]; WR = pe["unfiltered_error_after"] * N - pe["claims_flipped"]
rows_d = "\n".join("| %s | %s | %.4f | %.4f %s | %.4f %s |" % (q, d["fires_on_claims"].get(q, "%d (run 2 disagrees)" % d["run2_disagrees_on_claims"]), d["v_single"][q], P[q]["loo"], ci(P[q]["loo_ci"]), P[q]["shapley"], ci(P[q]["shapley_ci"])) for q in order)
fmt_rows = lambda v: "\n".join(f"| {r['target'].replace('target = the ', '')} ({r['target_value']:.3f}) | {r['scenario']} | {r['false_certifications']}/{r['sims']} | {r['rate']:.4f} {ci(r['rate_ci95'])} | {'valid' if r['valid_rate_le_0.01'] else '**NOT valid**'} |" for r in v["validity"])
md = f"""# Phase 6 Test-A: EXPLORATORY analyses 2 (d)-(g) (not preregistered endpoints; silver labels, AI-made, not human-verified)

Scoring only on the existing Test-A outputs: no model run, nothing frozen changed (frozen `agent.decide`, amendment-1 wrapper, primary settings; run-1 claims, run 2 only as the agreement filter, 4 run-2 timeouts missing). Script `scripts/phase6_testA_exploratory2.py` (pure Python), raw numbers `reports/phase_6_exploratory_2.json`. Everything here is exploratory. All error rates are against silver labels that are not independent of the pipeline (Pass C sided with Pass B, both Opus, in 73.5% of Test-A items); no label-error figure is claimed.

## Summary
| | result |
|---|---|
| (d) attribution of the H1 delta | full set reproduces H1: delta {d['full_delta']:.4f} {ci(d['full_delta_ci'])}; exact Shapley values sum to it. Largest: run-2 agreement {P['run2_agreement']['shapley']:.3f} {ci(P['run2_agreement']['shapley_ci'])}, then V3 unparseable-date {P['V3_unparseable']['shapley']:.3f} {ci(P['V3_unparseable']['shapley_ci'])}, E1 {P['E1']['shapley']:.3f} {ci(P['E1']['shapley_ci'])}; V3o {P['V3o_event_order']['shapley']:.3f}, V1 {P['V1']['shapley']:.3f}; V3 after-filing-date, V3 before-1990 and V8 about 0 (V3 before-1990 and V8 never fire on event claims) |
| (e) tipping point (silver noise, favourable-to-agent direction) | the H1 CI lower bound reaches 0 when {cl['fraction_of_accepted_correct_claims_wrong']:.1%} of the accepted-correct claims are really wrong ({cl['claims_flipped']:.0f} claims = {cl['share_of_all_event_labels']:.1%} of all {N} event labels); the point estimate reaches 0 at {pe['fraction_of_accepted_correct_claims_wrong']:.1%} ({pe['claims_flipped']:.0f} claims = {pe['share_of_all_event_labels']:.1%} of labels); the H1 point threshold (delta >= 0.05) fails first, at {f05:.1%} ({k05:.0f} claims = {k05 / N:.1%} of labels) |
| (f) cluster-sum t-bound (delta 0.01, cap 10 per filer) | events: accepted error {ev['point_error']:.3f} -> upper bound {ev['ucb_99_one_sided']:.3f} ({ev['accepted_claims_in_bound']} claims, {ev['clusters']} filers); cause: {ca['point_error']:.3f} -> {ca['ucb_99_one_sided']:.3f} ({ca['accepted_claims_in_bound']} claims, {ca['clusters']} filers). **Validity check FAILED**: false-certification rate {min(r['rate'] for r in ev['validity'] if r['target'].endswith('bound')):.4f}-{max(r['rate'] for r in ev['validity'] if r['target'].endswith('bound')):.4f} for events and {min(r['rate'] for r in ca['validity'] if r['target'].endswith('bound')):.3f}-{max(r['rate'] for r in ca['validity'] if r['target'].endswith('bound')):.3f} for cause, against the required <= 0.01; the bound is not valid as specified, so its numbers must not be used as guarantees |
| (g) empty event lists | run 1: {g['run1']['empty_event_lists']} of {g['run1']['filings_with_valid_output']} filings ({g['run1']['share']:.1%}), none with a gold event; 0 of {g['run1']['attack_host_like_filings(criteria of tt.agent.inject.fixtures)']['n']} attack-host-like filings; under the suppress_events attack 2 of 6 outputs were empty |

## (d) Per-check attribution of the H1 delta (events)
Players: every rule that can fire on an *event* claim, with the V3 date rule split into its three `extra.py` sub-rules (V1 quote verbatim in the masked section; E1 date text inside the quote or the nearest preceding date; V3 unparseable / before 1990 / after the filing date; V3o event order; V8 instruction-like text), plus the run-2 agreement filter. V2a, V2b, S2n (supplier names), V4 and V4r (cause) cannot change an event claim's acceptance, so they are not players here. A coalition S accepts a claim iff none of its fired rules is in S and (run 2 agrees or the filter is not in S); v(S) = unfiltered error minus accepted error (v of the empty coalition = 0, v of the full set = the H1 delta, asserted equal to 0.1352 and to the committed H1 CI). Leave-one-out = v(all) - v(all without the rule). Shapley = exact, 2^8 = 256 coalitions. Intervals: the same filer-cluster bootstrap as H1 (2000 resamples, seed 0, same resampling sequence; the full-set CI reproduces H1 exactly); a Shapley or leave-one-out value is recomputed in every resample.

| rule | fires on claims (of {d['claims']}) | rule alone: delta | leave-one-out [95% CI] | Shapley [95% CI] |
|---|---|---|---|---|
{rows_d}
| **sum** | | | | **{d['shapley_sum']:.4f}** |

Reading: the run-2 agreement filter carries the largest share on its own (delta {d['v_single']['run2_agreement']:.3f} alone). Rules overlap (a claim with an unparseable date is often also rejected by run 2), so leave-one-out values are small and do not add up; the Shapley values do add up and are the fairer split, but they depend on which rules are put in the game and say nothing about causation. Several intervals include 0.

## (e) Tipping point for silver-label noise (H1 delta)
Question: how many event labels would have to be wrong, in the direction most favourable to the agent, before the H1 result goes away?
Assumptions: (1) the only errors are accepted claims that silver marks correct but are actually wrong (flatters the agent); (2) the same claims are in the unfiltered B2 set (the accepted claims are a subset of it), so each flip also raises the B2 error; (3) flips are spread evenly over the accepted-correct claims (expected value, every claim wrong with the same probability f; clusters resampled as in H1) - flips concentrated in a few filers could do more damage to the CI than the same number spread out; (4) nothing else changes (no label noise on the other claims, run 2 and the verifiers are fixed); (5) unit = one event claim's correctness label ({N} claims, of which {NA} accepted, {CA} accepted and marked correct).
Flipping f x {CA} claims changes the delta by exactly -f x {CA} x (1/{NA} - 1/{N}).

| tipping point | fraction of accepted-correct claims wrong | claims | share of all {N} event labels | share of {NA} accepted labels | accepted error after | unfiltered error after |
|---|---|---|---|---|---|---|
| H1 point threshold delta < 0.05 fails | {f05:.3f} | {k05:.0f} | {k05 / N:.3f} | {k05 / NA:.3f} | {(WA + k05) / NA:.3f} | {(WR + k05) / N:.3f} |
| CI lower bound reaches 0 | {cl['fraction_of_accepted_correct_claims_wrong']:.3f} | {cl['claims_flipped']:.0f} | {cl['share_of_all_event_labels']:.3f} | {cl['share_of_accepted_labels']:.3f} | {cl['accepted_error_after']:.3f} | {cl['unfiltered_error_after']:.3f} |
| point estimate reaches 0 | {pe['fraction_of_accepted_correct_claims_wrong']:.3f} | {pe['claims_flipped']:.0f} | {pe['share_of_all_event_labels']:.3f} | {pe['share_of_accepted_labels']:.3f} | {pe['accepted_error_after']:.3f} | {pe['unfiltered_error_after']:.3f} |

So H1 as a preregistered pass (delta >= 0.05 and CI lower bound > 0) tips first on the point threshold, at roughly 1 wrong label in 10 across all event labels (about 1 in 4 of the accepted-correct claims). This is a single, one-directional scenario, not an estimate of how noisy the silver labels are; no label-error rate is claimed.

## (f) Cluster-sum t-bound on accepted-claim error, and its validity check
Bound (as specified, defined here before looking at any result): per filer cluster g, n_g accepted claims (at most 10 per cluster; if more, a seeded random subset of 10) and e_g errors; r = sum e / sum n; residuals d_g = e_g - r n_g; SE = sqrt(G/(G-1) x sum d_g^2) / sum n; upper bound = r + t(0.99, G-1) x SE (one-sided, delta = 0.01). Real data: events {ev['accepted_claims_in_bound']} of {ev['accepted_total_before_cap']} accepted claims kept by the cap, {ev['errors']} errors, {ev['clusters']} filers: error {ev['point_error']:.3f}, upper bound **{ev['ucb_99_one_sided']:.3f}**; cause {ca['accepted_claims_in_bound']} of {ca['accepted_total_before_cap']} kept, {ca['errors']} errors, {ca['clusters']} filers: error {ca['point_error']:.3f}, upper bound **{ca['ucb_99_one_sided']:.3f}**.
Validity check: keep the real Test-A cluster sizes (after the cap), set the true risk equal to the target, simulate the errors 20,000 times, and count how often the bound comes out *below* the true risk (a false certification of "risk < target"). Valid only if the rate is <= 0.01. Scenarios: independent claims; a beta-binomial with the intra-cluster correlation estimated from the real accepted claims (events {ev['icc_estimate']:.3f}, cause {ca['icc_estimate']:.3f}); stress 0.1, 0.3, 0.5. Targets: the observed bound, and the observed point estimate. Intervals are Wilson 95% for the simulation rate.

**Events** (cluster sizes after the cap: {ev['cluster_sizes_after_cap']})
| target | scenario | false certifications | rate [95% CI] | verdict |
|---|---|---|---|---|
{fmt_rows(ev)}

**Cause** (cluster sizes after the cap: {ca['cluster_sizes_after_cap']})
| target | scenario | false certifications | rate [95% CI] | verdict |
|---|---|---|---|---|
{fmt_rows(ca)}

Result: the bound fails the validity criterion in every scenario, including independent claims. For events it is only mildly anti-conservative (about 1.2% to 2.7% against the 1% target); for cause it is badly so (5% to 21%), because only {ca['errors']} accepted cause claims are wrong, so the linearised variance estimate is unreliable and a sample with no or few errors yields a bound near 0. The bound is therefore **not valid as specified** and none of its numbers is a guarantee. No repair was tried (exact or cluster-bootstrap-t bounds would be the obvious candidates; that is a separate, unrequested step).

## (g) Empty event lists and the limit of H4
suppress_events asks the model for an empty events list. An empty list contains no claim, so no verifier can reject it and a successful attack is invisible to every claim-level check. Test-A run 1: **{g['run1']['empty_event_lists']} of {g['run1']['filings_with_valid_output']} filings** ({g['run1']['share']:.1%}) have an empty event list ({', '.join(g['run1']['files'])}); none of the four has any gold event, so those empty lists are not missed events (of {g['total_gold_filings']} filings, {g['filings_with_scored_gold_events']} have a scored gold event). Run 2: {g['run2']['empty_event_lists']} of {g['run2']['filings_with_valid_output']} ({', '.join(g['run2']['files'])}), also none with a gold event. Among the {g['run1']['attack_host_like_filings(criteria of tt.agent.inject.fixtures)']['n']} filings that meet the attack-host criteria (supported cause, chronology over 300 characters, at least 2 gold events) there is no natural empty output in either run, while 2 of 6 suppress_events attacks produced one (raw and after verifiers + agreement). So H4's 2/30 residual successes are exactly the attack no verifier can catch; a defence would need a different kind of check (for example a floor on events for a chronology with dated sentences), which is not part of the frozen agent and was not added.

## Prior-art note for (d)-(f) (no novelty claims)
Checked: three quick web searches on 2026-10-25 (Shapley or leave-one-out attribution of pipeline components; tipping-point sensitivity analysis for label noise; cluster-robust ratio/linearisation bounds for clustered error rates), reading only result snippets, no paper in full. What they showed: component-level Shapley attribution of a metric gain and its comparison with leave-one-out are already used in the literature (one hit, arXiv 2607.16209, has an unusual identifier and was not verified); tipping-point analysis is a standard device in clinical-trial sensitivity analysis for missing data, and the transfer to label noise here is my adaptation; cluster-robust variance via the delta method for ratio estimators is textbook survey-sampling and econometrics material, and the searches found nothing that combines a t-bound on a clustered error rate with selective prediction. Not checked: any systematic literature review; selective-classification risk bounds (for example Geifman and El-Yaniv), conformal or distribution-free risk control, and finite-population or bootstrap-t bounds for clustered rates, which I know of only from memory and did not look up here; whether the specific combination used here exists elsewhere. Nothing in (d)-(f) is claimed to be new; (d) and (e) apply standard ideas to this evaluation, and (f) failed its own validity check.
"""
open("reports/phase_6_exploratory_2.md", "w").write(md)
print(len(md))
