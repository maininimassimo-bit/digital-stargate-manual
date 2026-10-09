"""Preparation guards; optional Google SDKs are never imported by these tests."""
import unittest
from tools.scientific_transients.lab_runtime import validate_config


def fixture():
    return {"activation": "FRESH_OWNER_AUTHORIZED", "sessionRef": "d" * 32,
        "sourceRevision": "e" * 40, "project": "digital-stargate-telemetry",
        "primaryBucket": "dsg-s4-lab-dddddddddddd-primary",
        "backupBucket": "dsg-s4-lab-dddddddddddd-backup",
        "runtimeServiceAccount": "dsg-s4-lab-dddddddddddd@digital-stargate-telemetry.iam.gserviceaccount.com",
        "googleClientId": "183451329061-8iedbjrn60u6iau42u1tlsonn6bi6hjd.apps.googleusercontent.com", "ownerEmail": "owner@example.invalid",
        "portalOrigin": "https://maininimassimo-bit.github.io", "workerId": "a" * 32,
        "workerSha256": "b" * 64, "deadline": 1100, "maximumEuro": 10}


class RuntimeGuards(unittest.TestCase):
    def test_valid_future_configuration_is_only_a_configuration_check(self):
        self.assertEqual(validate_config(fixture(), "e" * 40, now=1000), fixture())

    def test_missing_fresh_approval_source_or_budget_is_rejected(self):
        for field, value in (("activation", "OWNER_AUTHORIZED"), ("sourceRevision", "f" * 40),
                ("maximumEuro", 11), ("deadline", 1000), ("deadline", 2801),
                ("portalOrigin", "https://evil.invalid"), ("primaryBucket", "old-p6-bucket"),
                ("runtimeServiceAccount", "old@digital-stargate-telemetry.iam.gserviceaccount.com")):
            with self.subTest(field=field):
                config = fixture();config[field] = value
                with self.assertRaises(ValueError):validate_config(config, "e" * 40, now=1000)

    def test_unknown_fields_cannot_open_extra_routes_or_relax_limits(self):
        config = fixture();config["allowNativeWorker"] = True
        with self.assertRaises(ValueError):validate_config(config, "e" * 40, now=1000)


if __name__ == "__main__":unittest.main()
