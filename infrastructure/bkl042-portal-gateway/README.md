# BKL-042 Google Identity gateway

This gateway is the only public-facing component proposed for the BKL-042
portal. It validates a Google ID token, admits only the configured owner email,
and calls the private AI relay using the Cloud Run service identity.

Required runtime configuration:

- `GOOGLE_CLIENT_ID`: Google Identity Services web client ID;
- `BKL042_ALLOWED_EMAIL=maininimassimo@gmail.com`;
- `BKL042_PRIVATE_RELAY_URL`: private Cloud Run relay URL;
- `BKL042_PORTAL_ORIGIN=https://maininimassimo-bit.github.io`.

The gateway does not hold the OpenAI key, does not accept tools or actions, and
does not grant command, scheduler, remediation or Safety Authority capability.
It remains `NOT_READY` until the OAuth web client ID is configured.
