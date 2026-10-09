"""Owned-service stop protocol with injected, separately authorized command runner.

No gcloud process, credential discovery, scheduler or background task on import.
The runner contract reports sanitized identity only, never raw service env/credentials.
"""
import time
from tools.pixinsight.local_pilot.broker import require
from tools.scientific_transients.lab_build_plan import deployment_commands


class OwnedServiceStop:
    def __init__(self, session_ref, revision, image_digest, runner):
        self.plan = deployment_commands(session_ref, revision, image_digest)
        self.runner = runner
        self.used = False

    def identity(self, reply):
        expected = self.plan["resourcePlan"]
        require(type(reply) is dict and reply.get("present") is True, "LAB_SERVICE_PRESENCE_UNCONFIRMED")
        require(reply.get("project") == expected["project"] and reply.get("region") == expected["region"]
            and reply.get("service") == expected["service"] and reply.get("sessionRef") == expected["sessionRef"]
            and reply.get("sourceRevision") == expected["sourceRevision"] and reply.get("image") == self.plan["image"],
            "LAB_STOP_IDENTITY_MISMATCH")

    def stop(self):
        require(not self.used, "LAB_STOP_ALREADY_ATTEMPTED")
        self.used = True
        before = self.runner(self.plan["verifyService"], 60)
        if before == {"present": False}:
            return self.receipt("OBSERVED_ABSENT_BEFORE_STOP", False)
        self.identity(before)
        uncertain = False
        try:
            reply = self.runner(self.plan["stopNewServiceOnly"], 120)
            require(reply == {"stopConfirmed": True}, "LAB_STOP_UNCERTAIN")
        except Exception:uncertain = True
        # Read-only reconciliation after an uncertain stop; never replay deletion.
        after = self.runner(self.plan["verifyService"], 60)
        require(after == {"present": False}, "LAB_SERVICE_STOP_NOT_OBSERVED")
        return self.receipt("OBSERVED_ABSENT_AFTER_STOP", uncertain)

    def receipt(self, outcome, uncertain):
        resources = self.plan["resourcePlan"]
        return {"protocol": "DSG_S4_OWNED_STOP_V1", "sessionRef": resources["sessionRef"],
            "sourceRevision": resources["sourceRevision"], "service": resources["service"],
            "outcome": outcome, "stopResponseWasUncertain": uncertain,
            "dataDeleted": False, "scientificValidation": "NOT_VALIDATED", "milestoneClosed": False}

    def wait_until(self, stop_deadline, *, clock=time.time, sleep=time.sleep):
        require(type(stop_deadline) in (int, float) and clock() <= stop_deadline <= clock() + 2400,
                "LAB_STOP_DEADLINE")
        while clock() < stop_deadline:sleep(max(0, min(1, stop_deadline - clock())))
        return self.stop()
