# Runbook — Emergency Hotfix

## Conditions

An emergency hotfix is permitted only for an active production defect with material safety, availability, security or data-integrity impact.

## Procedure

1. Assign an incident owner and technical reviewer.
2. Branch from the affected production baseline.
3. Apply the smallest safe correction.
4. Run targeted tests plus all mandatory safety and regression checks available in the time window.
5. Record the risk and obtain emergency approval.
6. Tag, deploy and verify the hotfix.
7. Merge the correction into active development branches.
8. Complete a retrospective and any missing validation after stabilization.
