# Runbook — Storage Capacity

## Trigger

Available storage falls below the configured warning or critical threshold.

## Procedure

1. stop scheduling new acquisition blocks when the critical threshold is reached;
2. identify the affected storage tier;
3. verify whether data transfer or archival jobs are blocked;
4. remove only approved temporary files and rotated logs;
5. never delete unverified scientific data;
6. confirm restored free capacity;
7. record corrective action.
