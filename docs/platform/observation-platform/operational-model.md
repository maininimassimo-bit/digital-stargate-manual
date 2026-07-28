# Operational Model

## 1. Operating modes

| Mode | Description |
|---|---|
| Manual Supervised | Operator explicitly controls each major step |
| Assisted | Platform validates safety and coordinates selected procedures |
| Automated | Platform executes an approved observation plan end to end |
| Recovery | Platform is restoring a safe and known state |
| Maintenance | Automation is inhibited while equipment is serviced |

## 2. Readiness gates

Before starting a session, the platform verifies:

- safety authority available;
- weather state current and acceptable;
- enclosure controller reachable;
- mount, camera and required equipment reachable;
- valid equipment profile selected;
- sufficient storage available;
- active plan valid for the time window;
- no maintenance lock present.

## 3. Operational responsibilities

### Operator

- approves plans and maintenance windows;
- responds to escalated alerts;
- reviews failed recovery cases;
- authorizes return to service.

### Platform

- evaluates readiness;
- coordinates execution;
- records evidence;
- initiates recovery;
- inhibits unsafe actions.

### Safety authority

- determines whether operation is permitted;
- revokes permission when conditions become unsafe;
- remains independent from imaging success.

## 4. Failure classes

- transient integration failure;
- device unavailable;
- stale telemetry;
- guiding degradation;
- sequence failure;
- enclosure control failure;
- power or host degradation;
- connectivity loss;
- unsafe environmental condition.

## 5. Recovery priorities

1. protect people and equipment;
2. stop unsafe motion or exposure;
3. park the mount when possible;
4. close the enclosure;
5. isolate or power down affected equipment;
6. preserve logs and evidence;
7. notify the operator.

## 6. Operational evidence

Every session must produce:

- session identifier;
- selected plan and equipment profile;
- safety decisions;
- command and response timeline;
- state transitions;
- warnings and failures;
- recovery actions;
- final outcome and closure state.
