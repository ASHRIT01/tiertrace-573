# Check: why 39.5% of the dev sample name no supplier vs 27.5% of the audit sample (2015-2022)

AI-checked, not human-verified. Both samples are random draws of vehicle/equipment campaigns, latest 573 version, same parser (block Name = NR, N/A or blank).

| | audit sample | dev sample |
|---|---|---|
| filings 2015-2022 | 200 | 397 |
| no supplier name in block | 55 (27.5%) | 157 (39.5%) |
| 95% CI (resampling filers, 10,000 draws) | [19.3%, 36.5%] | [32.5%, 47.0%] |
| distinct filers | 94 | 152 |

- Difference dev - audit: **+12.0 points, 95% filer-cluster CI [+0.8, +23.0]**. A plain two-proportion z-test gives z = 2.9, which overstates the evidence because filings by one filer are not independent.
- It is not vehicle vs equipment (V: 28% vs 40%; E: 23% vs 29%) and not single vs multiple versions (26% vs 41%; 29% vs 38%).
- **Filer mix explains about half.** Applying each filer's pooled no-name rate to each sample's filer mix predicts 31.7% for audit and 37.4% for dev. The audit sample has BMW (10 filings, 1 no-name), Honda (6, 0) and Kia (6); dev has more Daimler Vans (13, 8 no-name), Mercedes-Benz (13, 8) and Chrysler (14, 5).
- **Naming a supplier is a filer habit.** In filers present in both samples the rates agree: Forest River 10/14 and 16/20 no-name; BMW 1/10 and 0/9; Honda 0/6 and 0/8; Ford 2/14 and 4/22.
- Conclusion: not a parser artifact. The remaining gap (about 6 points) is within what filer clustering and sampling noise allow. The earlier 'about 72% name a supplier' was sample-specific; the larger dev sample suggests about 60% for 2015-2022, and any fill rate must be reported with a filer-cluster interval.
- Implication for splits: the share of no-name filings in a split depends on which filers land in it; the unseen-filers split and Test-A will differ for the same reason.
