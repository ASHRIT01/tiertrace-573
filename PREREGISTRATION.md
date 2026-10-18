# Preregistration (provisional; freeze before touching Test-A/Test-B)

Wording rule: results say "named in the filing as component manufacturer", never that a supplier "caused" a recall.

| ID | Hypothesis | Threshold |
|----|-----------|-----------|
| H1 | Masked-block parent-supplier recovery | Top-1 >= 0.80 where name is in chronology; >= +10 pts over B1 on full masked set |
| H2 | Verifier cuts confident-wrong outputs | >= 50% fewer vs. no verifier; <= 15 pts coverage lost |
| H3 | Timeline | Date exact-match F1 >= 0.90; median lag error <= 3 days (200 labelled) |
| H4 | Tier/locus labelling | Krippendorff alpha >= 0.70; agent macro-F1 >= 0.60 and +15 over keyword baseline |
| H5 | 4-bit 4B vs full precision | within 3 pts on H1, H3, H4 |
| H6 | (stretch) forward prediction | exploratory |

Headline metric: error among accepted claims vs. coverage (risk-coverage curve). Abstaining on everything is never success.
Splits and L1 labels: publish SHA-256 hashes here before any test run.
