# ARB-012-C04 — VM-R05 / ENV-005 Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R05 |
| Work item | C04-W06 |
| Control | VM-R05 / ENV-005 |
| Host | `dsg-arb012-c04-val` |
| DSOC repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Validated commit | `c8c09f1962222f064e653864de8eee4196ffbbfe` |
| Date | 2026-08-22 |
| Result | **PASS — technical authorization policy validation** |

## 1. Scope

Validate the minimum non-production two-person authorization policy required by the approved ARB-012-C04 target model. This evidence does not authorize production use or physical-device control.

## 2. Implemented mapping

- `dsgmassimo`: Requester, Operator, Maintainer.
- `dsgleonardo`: C3 Approver, Safety Authority, Security Authority, Return-to-Service Approver.
- self-approval: denied.
- own return-to-service approval: denied.
- Security Authority self-access approval: denied.
- positive C4: denied by design.
- break-glass: denied by design.
- suspended principal: denied before role evaluation.
- unknown/unmapped principal: deny by default.

## 3. VM execution evidence

The VM clone was updated from the immutable ENV-011 baseline to the authorization validation commit and tested with .NET SDK `8.0.129`.

Domain regression suite:

```text
DigitalStarGate.Control.Domain.Tests
Failed: 0
Passed: 4
Skipped: 0
Total: 4
```

Application authorization suite after correcting the missing xUnit namespace import:

```text
DigitalStarGate.Control.Application.Tests
Failed: 0
Passed: 10
Skipped: 0
Total: 10
Duration: 65 ms
```

The application test build produced:

```text
DigitalStarGate.Control.Application.dll
DigitalStarGate.Control.Application.Tests.dll
```

## 4. Defect retained in evidence history

The first execution of the Application test project failed to compile because `ValidationAuthorizationPolicyTests.cs` omitted `using Xunit;`. The defect was corrected in commit `c8c09f1962222f064e653864de8eee4196ffbbfe` and the suite was rerun successfully. The failed first run remains part of the evidence history and is not overwritten.

## 5. Disposition

**VM-R05 / ENV-005: PASS for the technical two-person authorization policy on the non-production validation baseline.**

This PASS proves the policy and deterministic allow/deny rules in the Application layer. It does not yet prove runtime audit persistence, correlation export or an external identity provider; those remain governed by VM-R06 through VM-R10 as applicable.