# Link Validation Checklist

## Internal links

- [ ] Run the MkDocs strict build.
- [ ] Review all unresolved-anchor messages.
- [ ] Confirm all newly introduced links resolve.
- [ ] Verify navigation links in the generated site.
- [ ] Record legacy unresolved anchors in `known-issues.md`.

## External links

- [ ] Confirm referenced vendor and standards links are still valid.
- [ ] Avoid links to transient download locations.
- [ ] Prefer authoritative sources.
- [ ] Record externally unavailable references.

## Release decision

The release may proceed with legacy informational link messages only when they are documented, accepted and do not prevent successful site generation.
