# Data access notes (OUR INTERPRETATION; NOT confirmed by NHTSA)

Observed 2026-10-18:
- `https://api.nhtsa.gov/robots.txt` -> HTTP 403, body `{"message":"Missing Authentication Token"}`.
- `https://static.nhtsa.gov/robots.txt` -> HTTP 404 (NoSuchKey): no robots.txt, nothing disallowed.
- `https://api.nhtsa.gov/recalls/campaignNumber?...` answered 200 JSON with our identifying user agent.

Interpretation (unconfirmed): that 403 body is the standard AWS API Gateway reply for a path with no route,
so it most likely means api.nhtsa.gov has no robots.txt, not that bots are blocked. NHTSA publishes this API
for public use and a browser reaches it with no login. We have NOT read NHTSA's API terms in full.

Conditions (set by the project owner): identifying user agent; at most 1 request/s; cache every response;
stop immediately on any 401/403/429 from a data call; about 300 campaigns for the audit, no full crawl yet.
