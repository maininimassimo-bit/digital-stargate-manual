# Power Continuity

## Objective

Power continuity controls protect the observatory from uncontrolled shutdown, device corruption and unsafe dome states.

## Protected loads

Priority must be assigned to:

1. safety sensors and control logic;
2. dome or roof control;
3. networking and remote access;
4. primary compute;
5. mount parking and camera shutdown;
6. non-critical accessories.

## Power event behavior

When a sustained power anomaly is detected, the platform should:

1. stop new exposures;
2. complete or abort the active exposure according to policy;
3. park the mount;
4. close the dome or roof;
5. stop device services;
6. shut down compute nodes in a controlled manner.

## Validation

UPS autonomy and shutdown behavior must be tested periodically and recorded in the maintenance log.
