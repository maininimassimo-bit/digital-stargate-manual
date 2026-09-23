# BKL-042 F6 — portal OAuth ingress gate

Status: **IMPLEMENTED — OAUTH CLIENT ID REQUIRED**

The gateway under `infrastructure/bkl042-portal-gateway/` is prepared for a
Google Identity Services web client. It validates the Google ID token audience,
verified email and exact GitHub Pages origin, then forwards only the bounded
read-only request to the private BKL-042 relay using Cloud Run identity.

Required owner-controlled input before deployment:

1. create a Google OAuth web client for the GitHub Pages origin;
2. configure the OAuth consent/authorized origin for
   `https://maininimassimo-bit.github.io`;
3. provide the resulting **Client ID only** as `GOOGLE_CLIENT_ID`.

No OAuth client secret is required by the browser-token validation path and no
OpenAI credential belongs in this gateway or in GitHub Pages. Until the Client
ID is configured, the gateway remains fail-closed and no public endpoint is
deployed.
