# BKL-042 F6 — portal OAuth ingress gate

Status: **CLOSED — AUTHENTICATED LIVE OAT PASSED — BOUNDED READ-ONLY**

The gateway under `infrastructure/bkl042-portal-gateway/` is prepared for a
Google Identity Services web client. It validates the Google ID token audience,
verified email and exact GitHub Pages origin, then forwards only the bounded
read-only request to the private BKL-042 relay using Cloud Run identity.

Deployment evidence:

- Google OAuth web client created for the GitHub Pages origin;
- client ID configured as non-secret runtime configuration;
- gateway service: `dsg-bkl042-portal-gateway`;
- gateway revision: `dsg-bkl042-portal-gateway-00002-m7c`;
- gateway health: `READY`;
- relay invocation: service-account mediated;
- allowed owner identity: `maininimassimo@gmail.com`.
- GitHub Pages consumer publication verified;
- owner-witnessed authenticated live OAT passed;
- final OAT evidence: `docs/architecture/validation/BKL-042-F6-PORTAL-OAUTH-OAT-EVIDENCE-2026-09-23.md`.

No OAuth client secret is required by the browser-token validation path and no
OpenAI credential belongs in this gateway or in GitHub Pages. The public
consumer remains bounded read-only and forwards only the governed five-field
request shape.
