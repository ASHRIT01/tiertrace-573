# TierTrace-573 project rules
- Public data only. No employer or internal company data.
- Fetch at most one page per second and always identify yourself (user agent in tt/fetch/nhtsa.py).
- Never pretend to be a browser or get around bot blocks. If blocked, stop and ask the user.
- Say suppliers are "named in the filing", never "responsible" or "caused".
- Never touch the test data (Test-A, Test-B, unseen-filer, injection splits) before the labels and splits are frozen and hashed in PREREGISTRATION.md.
- Do not edit tt/verify/verifier.py unless the user asks.
- Save progress after every task (git commit).
- Do not run model benchmarks while the user is measuring memory; they run bench scripts themselves.
