# BKL-031 F3-A1-M2 — Site Authority Materialization Validation Evidence

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-M2-VAL-001 |
| Stato | **INTEGRATED / EXACT-HEAD 8/8 AND POST-MERGE 10/10 SUCCESS** |
| Data | 15/09/2026 |
| Baseline | `main@d5750ce160c5f80d20a72bc35dee321200647d03` |
| Protected values | Omitted by policy |
| Runtime / OAT | Not Applicable |

## 1. Validated scope

The candidate package contains a versioned protected registry, schema contracts, a canonical JSON/SHA-256 implementation, fail-closed lifecycle and resolver validation, public allowlist enforcement, protected-literal scanning and a dedicated GitHub Actions gate.

The owner source decision and protected DRAFT were integrated through PR #203. At that milestone the decision was explicitly not an exact-digest lifecycle approval and the candidate remained ineligible. The owner has since supplied the separate exact-digest decision used only by F3-A1-M4.

## 2. Commands and local evidence

| Command | Result |
|---|---|
| `node --test governance/site-authority/tools/test-site-authority.mjs` | PASS — 51 tests, 0 failures |
| `node governance/site-authority/tools/site-authority-validator.mjs` | PASS after execution against the complete repository tree; exact-head CI authoritative |

The test command was executed against synthetic fixtures and the protected candidate validator was locally checked for payload integrity. The full `docs/` leak scan is authoritative only in GitHub CI because the local staging tree does not mirror the complete repository.

## 3. Accepted-plan execution matrix

| Range | Count | Local result | Exact-head gate |
|---|---:|---|---|
| A1-P01–P10 | 10 | PASS | PASS |
| A1-N01–N12 | 12 | PASS | PASS |
| A1-N13–N27 | 15 | PASS | PASS |
| A1-N28–N37 | 10 | PASS | PASS |
| A1-N38–N41 | 4 | PASS | PASS |
| Total | 51 | **PASS** | PASS |

## 4. Finding disposition

| Finding | Candidate disposition |
|---|---|
| `ARB-193-MI01` | orthometric metres relative to mean sea level; bounded `[-500, 9000]`; reject non-finite/out-of-range |
| `ARB-193-MI02` | one protected canonical observatory identity, explicit authorized mapping, single-authority candidate scope, ambiguous/cross-scope fail closed |
| `ARB-191-MI01` | repository-level public allowlist, independent public identity/digest rules and protected-literal leak scan implemented; future adapters remain gated |
| `ARB-191-MI02` | half-open, adjacency, gap, overlap and unbounded cases executed |

Only the ARB can close architecture findings. This evidence does not self-approve them.

## 5. Privacy evidence

- exact site facts exist only outside `docs/` in the protected registry;
- public documents do not contain the protected site record identifier, observatory identity, source locator or internal digest;
- the validator derives protected literals in memory and scans the full Pages input tree;
- validator success output contains no protected value;
- public-payload tests reject coordinates, elevation, locator, internal identifiers, internal digest and conflict evidence;
- unauthorized exact resolution returns deny plus audit without protected payload.

## 6. Not executed or not claimed

- independent geodetic survey or accuracy certification;
- at the M2 milestone, approved lifecycle receipt or resolver availability;
- runtime adapter, persistence service, caching or public consumer;
- CurrentSetupAssignment;
- EAGLE or observatory execution;
- readiness, ranking, command or Safety Authority;
- independent human ARB review.

## 7. Acceptance gates

F3-A1-M2 integration evidence:

1. dedicated workflow and all applicable repository workflows passed on the exact head;
2. ARB and Release Quality reviewed the exact head without Blocker/Major;
3. merge used DSG-AEM-001 expected-head controls;
4. post-merge verification completed 10/10 SUCCESS on `main@d5750ce160c5f80d20a72bc35dee321200647d03`.

For `APPROVED` promotion:

1. exact digest presentation and explicit validity-bound owner decision are complete;
2. F3-A1-M4 adds the separate immutable approval receipt;
3. payload and digest remain unchanged while the lifecycle envelope is promoted;
4. ARB, Release Quality, exact-head CI and post-merge verification remain mandatory.
