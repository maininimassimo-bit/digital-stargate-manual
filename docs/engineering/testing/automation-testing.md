# Automation Testing

## Test modes

Automation workflows should be validated using simulators, recorded telemetry, controlled hardware-in-the-loop tests and supervised production proving.

## Critical scenarios

- startup with one or more unavailable devices;
- stale or contradictory safety signals;
- weather degradation during exposure;
- guiding loss and repeated recovery failure;
- meridian flip interruption;
- storage exhaustion;
- network loss during autonomous operation;
- controlled and emergency shutdown;
- restart after partial completion.

## Acceptance rule

No autonomous workflow is production-ready until its timeout, retry, abort and safe-state behaviour have been observed and documented.
