# Session photo runtime — authorized deployment, Owner login gate pending

The Owner explicitly approved the concrete new paid-resource/cost proposal on
02/10/2026, after source/portal PR #474 was verified. This authorizes the exact
`deployment-plan.json` resources, separate from the previous single-JPEG grant.
No automatic spending cap or storage deletion is implied.

## Deployed source and resources

- Reviewed source: `c656869b3b403cc637b02067efadb118195034c5`.
- Cloud Build: `eb198b21-2dbf-44ce-ace4-df11bb89ea1a`, SUCCESS.
- Registry digest: `sha256:870c16b5b39b95a1b6fb2d76467f3f262ae620631a7a5bac7a2d0f10eeb5a17d`.
- Dedicated service/identity and two private buckets match the deployment plan.
- Both buckets: europe-west1, UBLA, public-access prevention enforced, versioning
  enabled, no automatic lifecycle deletion. Existing project administrators remain
  trusted; the runtime has only the reviewed bucket permissions.
- Primary objectCreator/objectViewer plus objectUser conditional on the exact
  `control/state.json` object; backup objectCreator/objectViewer only.
- Cloud Run: 8 GiB, 2 CPU, concurrency 1, min 0, max 1, timeout 900 seconds,
  request-based billing, no CPU boost; deployment pinned to the registry digest.
- HTTPS origin: `https://dsg-scientific-photo-ingestion-183451329061.europe-west1.run.app`.

## Real cloud evidence and limits

The production container ran real ClamAV and GCS tests using clearly labelled
synthetic inputs. Clean data passed; the standard EICAR antivirus test was
rejected. No mocked scanner/storage was used for these checks. GCS tests used
the dedicated runtime identity through temporary, scoped build impersonation;
that impersonation grant was removed immediately after the successful build.
The default build identity's pre-existing project roles were not expanded.

Full byte read-back, multi-chunk resume after process reconstruction, private
save, exact public field omission, metadata sanitation, immutable versions,
withdrawal, stale-generation rejection and denied immutable/backup overwrite
and backup deletion passed. Anonymous raw-object reads were denied. Sixteen
verified current objects were read from the separate backup and restored into
a non-active primary verification namespace, with exact byte/hash read-back.
No older publication head was restored. The current public collection is empty.
Synthetic test entries and original/recovery bytes remain private; they are
labelled as technical tests and do not represent scientific acceptance.

This establishes container antivirus/GCS behavior, not actual Owner Google
login or acceptance of a real scientific file. Cloud Run startup/HTTP checks are
separate from the build-side core tests. Live Owner/browser upload and real-file
OAT remain explicit gates. Security freshness is unrelated to gallery expiry.

## Staged portal and remaining gate

`OWNER_LOGIN_OAT_PENDING` permits Google login and readonly archive retrieval
only through the UI. Upload, review, publication and withdrawal controls remain
disabled, including keyboard form submission. The browser regression verifies
successful synthetic login cannot enable these controls or create requests.
This UI staging is not a replacement for the service's Owner-only authorization.
All private service routes still require a valid Owner token and exact origin.

Actual Owner login cannot be inferred from a synthetic token or a service-account
token. Acceptance records retain only the outcome, never Google credentials or
tokens. After actual Owner login succeeds, a separately reviewed configuration
change enables the complete procedure; Owner real-file OAT then follows.

Rollback sets the portal service URL to null and disables new requests while
preserving private originals/recovery objects. No bucket deletion, science-file
migration, AP-014 admission, quality promotion, BKL-043 mutation or device action
is part of this grant. CI, ARB/RQ and exact merge-SHA/Pages verification apply to
the staged portal release; their status must be retained in PR evidence.
