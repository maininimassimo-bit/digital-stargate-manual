# Release Management

## Release flow

```text
Scope Freeze
  -> Validation
  -> Release Candidate
  -> Approval
  -> Tag and Package
  -> Deploy or Publish
  -> Verify
  -> Close and Record
```

## Release record

Each release record must contain:

- version and source commit;
- included changes and resolved defects;
- known limitations;
- required configuration or migration steps;
- validation evidence;
- deployment and rollback procedure;
- approver and release date.

## Rollback

Rollback is a planned release capability, not an improvised incident action. Irreversible migrations require a separately approved recovery strategy.
