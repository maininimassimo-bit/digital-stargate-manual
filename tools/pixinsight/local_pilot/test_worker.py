"""Synthetic coordinator tests; no PixInsight or scientific pixels exercised."""
from pathlib import Path
import json
import tempfile
import unittest
import struct
import os

from tools.pixinsight.local_pilot import worker


class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.sources = self.base / "sources"
        self.sources.mkdir()
        self.root = self.base / "worker"
        self.root.mkdir()
        self.inputs = []
        for role in worker.ROLES:
            path = self.sources / (role + ".xisf")
            path.write_bytes(("synthetic-" + role).encode())
            self.inputs.append(dict(role=role, path=str(path), sha256=worker.digest(path), imageIndex=0, width=10, height=12))
        self.request = dict(schemaVersion="1.0", jobId="Synthetic_01", recipe=worker.RECIPE,
                            inputs=self.inputs, background=dict(polyDegree=1, boxSize=12, boxSeparation=16))

    def tearDown(self):
        self.tmp.cleanup()

    def terminal(self, job, status="CANCELLED"):
        manifest = json.loads((job / "manifest.json").read_text())
        worker.write_new(job / "terminal.json", dict(jobId=manifest["jobId"], token=manifest["token"], runtimeSha256=manifest["runtimeSha256"], status=status, outputs=[], processCount=0))

    def test_prepare_copies_original_bytes_and_trusted_launcher(self):
        job = worker.prepare(self.root, self.request)
        for i in self.inputs:
            self.assertEqual(worker.digest(Path(i["path"])), worker.digest(job / "inputs" / (i["role"] + ".xisf")))
        script = (job / "run.js").read_text()
        self.assertIn("executor.jsh", script)
        self.assertIn((job / "executor.jsh").as_posix(), script)
        self.assertEqual((job / "executor.jsh").read_bytes(), Path(worker.__file__).with_name("executor.jsh").read_bytes())
        self.assertNotIn("eval(", script)
        self.assertNotIn("new Function", script)
        raw_launcher = (job / 'run.js').read_bytes()
        self.assertTrue(raw_launcher.startswith(b'#engine v8\r\n#include '))
        self.assertNotIn(b'\n', raw_launcher.replace(b'\r\n', b''))

    def test_second_job_rejected_while_reserved(self):
        worker.prepare(self.root, self.request)
        other = {**self.request, "jobId": "Synthetic_02"}
        with self.assertRaises(FileExistsError):
            worker.prepare(self.root, other)
        self.assertFalse((self.root / "Synthetic_02").exists())

    def test_reviewed_tuning_is_bound_into_digest_and_native_manifest(self):
        from .scientific_delivery import registry_digest
        from .broker import encode
        import hashlib
        baseline = {**self.request, "recipe": worker.NONLINEAR_RECIPE}
        baseline["inputs"] = [{**row, "width":4634,"height":2808} for row in self.inputs]
        legacy_projection = {"recipe":baseline["recipe"], "background":baseline["background"],
                             "inputs":[{k:v for k,v in row.items() if k != "path"} for row in baseline["inputs"]]}
        self.assertEqual(registry_digest(baseline), hashlib.sha256(encode(legacy_projection)).hexdigest())
        tuned = {**baseline, "processing": {**worker.PROCESSING_DEFAULTS, "sharpenL":0.58}}
        self.assertNotEqual(registry_digest(baseline), registry_digest(tuned))
        changed = {**tuned, "processing": {**tuned["processing"], "sharpenL":0.57}}
        self.assertNotEqual(registry_digest(tuned), registry_digest(changed))
        job = worker.prepare(self.root, tuned)
        manifest = json.loads((job / "manifest.json").read_text())
        self.assertEqual(manifest["processing"], tuned["processing"])

    def test_replay_rejected(self):
        job = worker.prepare(self.root, self.request)
        self.terminal(job)
        worker.collect(self.root, self.request["jobId"])
        with self.assertRaisesRegex(ValueError, "Existing job"):
            worker.prepare(self.root, self.request)

    def test_cancel_collect_and_idempotent_verification(self):
        job = worker.prepare(self.root, self.request)
        worker.cancel(self.root, self.request["jobId"])
        self.assertTrue((job / "cancel.json").exists())
        self.terminal(job)
        first = worker.collect(self.root, self.request["jobId"])
        self.assertEqual(first, worker.collect(self.root, self.request["jobId"]))
        self.assertFalse((self.root / "active-job.json").exists())
        self.assertTrue((job / "reservation-closed.json").exists())

    def test_running_job_not_released(self):
        job = worker.prepare(self.root, self.request)
        self.terminal(job, "RUNNING")
        with self.assertRaisesRegex(ValueError, "Terminal status"):
            worker.collect(self.root, self.request["jobId"])
        self.assertTrue((self.root / "active-job.json").exists())

    def test_incomplete_success_not_released(self):
        job = worker.prepare(self.root, self.request)
        self.terminal(job, "COMPLETED")
        with self.assertRaisesRegex(ValueError, "Incomplete recipe"):
            worker.collect(self.root, self.request["jobId"])

    def test_source_mutation_prevents_release(self):
        job = worker.prepare(self.root, self.request)
        self.terminal(job)
        Path(self.inputs[0]["path"]).write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "Original/copy changed"):
            worker.collect(self.root, self.request["jobId"])
        self.assertTrue((self.root / "active-job.json").exists())

    def test_output_escape_rejected(self):
        job = worker.prepare(self.root, self.request)
        manifest = json.loads((job / "manifest.json").read_text())
        worker.write_new(job / "terminal.json", dict(jobId=manifest["jobId"], token=manifest["token"], runtimeSha256=manifest["runtimeSha256"], status="FAILED",
            outputs=[dict(name="../outside.xisf", sha256="a"*64)], processCount=0))
        with self.assertRaisesRegex(ValueError, "Unexpected output name"):
            worker.collect(self.root, self.request["jobId"])

    def test_tampered_copy_rejected(self):
        job = worker.prepare(self.root, self.request)
        self.terminal(job)
        (job / "inputs/R.xisf").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "Original/copy changed"):
            worker.collect(self.root, self.request["jobId"])

    def test_requests_fail_before_reservation(self):
        for change in ({"recipe":"EVAL_SCRIPT"}, {"jobId":"../escape"}, {"background":{"polyDegree":5,"boxSize":12,"boxSeparation":16}},
                       {"background":{"polyDegree":True,"boxSize":12,"boxSeparation":16}}, {"script":"alert(1)"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                worker.prepare(self.root, {**self.request, **change})
            self.assertFalse((self.root / "active-job.json").exists())

    def test_changed_source_rejected_before_reservation(self):
        Path(self.inputs[0]["path"]).write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "Source digest mismatch"):
            worker.prepare(self.root, self.request)
        self.assertFalse((self.root / "active-job.json").exists())

    def test_worker_root_in_sources_rejected(self):
        with self.assertRaisesRegex(ValueError, "directories must be separate"):
            worker.prepare(self.sources, self.request)

    def test_runtime_tamper_retains_reservation(self):
        job = worker.prepare(self.root, self.request)
        self.terminal(job)
        (job / "executor.jsh").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "Runtime identity mismatch"):
            worker.collect(self.root, self.request["jobId"])
        self.assertTrue((self.root / "active-job.json").exists())

    def test_bounded_output_header(self):
        path = self.base / "output.xisf"
        raw = b'<xisf><Image geometry="10:12:3" sampleFormat="Float32" colorSpace="RGB"/></xisf>'
        path.write_bytes(b"XISF0100" + struct.pack("<II", len(raw), 0) + raw)
        self.assertEqual(worker.xisf_header(path), dict(width=10, height=12, channels=3, sampleFormat="Float32", colorSpace="RGB"))
        path.write_bytes(b"XISF0100" + struct.pack("<II", 1024*1024+1, 0))
        with self.assertRaisesRegex(ValueError, "header limit"):
            worker.xisf_header(path)
        raw = b'<!DOCTYPE xisf [<!ENTITY unsafe "data">]><xisf/>'
        path.write_bytes(b"XISF0100" + struct.pack("<II", len(raw), 0) + raw)
        with self.assertRaisesRegex(ValueError, "Unsupported output header"):
            worker.xisf_header(path)

    def test_export_renames_identifiers_preserving_literals(self):
        job = worker.prepare(self.root, self.request)
        source = 'var P = new AutomaticBackgroundExtractor;\nP.someText = "P";\n'
        worker.write_new(job / "events/0000-start.json", dict(event="process-started", data=dict(label="background-R", nativeSource=source, target="Synthetic_R", dependencies=["synthetic"])))
        worker.write_new(job / "events/0001-completed.json", dict(event="process-completed", data=dict(label="background-R", target="Synthetic_R")))
        exported = worker.export_runtime_instances(job, dict(jobId=self.request["jobId"], processCount=1))
        self.assertEqual(exported["instanceCount"], 1)
        self.assertIn('DSGPilotProcess001.someText = "P";', (job / "workflow.js").read_text())

    def test_wrong_native_process_rejected(self):
        job = worker.prepare(self.root, self.request)
        worker.write_new(job / "events/0000-start.json", dict(event="process-started", data=dict(label="background-R", nativeSource="var P = new ChannelCombination;", dependencies=[])))
        worker.write_new(job / "events/0001-completed.json", dict(event="process-completed", data=dict(label="background-R", target="Synthetic_R")))
        with self.assertRaisesRegex(ValueError, "native process mismatch"):
            worker.export_runtime_instances(job, dict(jobId=self.request["jobId"], processCount=1))

    def test_completion_target_is_preserved_for_global_process(self):
        job = worker.prepare(self.root, self.request)
        labels = ["background-R", "background-G", "background-B", "background-L", "RGB-composition"]
        for ordinal, label in enumerate(labels):
            process = "ChannelCombination" if ordinal == 4 else "AutomaticBackgroundExtractor"
            worker.write_new(job / f"events/{ordinal*2:04}-start.json", dict(event="process-started", data=dict(label=label, nativeSource=f"var P = new {process};", dependencies=[])))
            worker.write_new(job / f"events/{ordinal*2+1:04}-completed.json", dict(event="process-completed", data=dict(label=label, target=f"Synthetic_{ordinal}")))
        worker.export_runtime_instances(job, dict(jobId=self.request["jobId"], processCount=5))
        correlations = json.loads((job / "runtime-correlations.json").read_text())
        self.assertEqual(correlations["instances"][-1]["target"], "Synthetic_4")

    def test_cancel_refuses_terminal_job_and_wrong_identity(self):
        job = worker.prepare(self.root, self.request)
        identity = json.loads((job / "reservation.json").read_text())
        (job / "reservation.json").write_text(json.dumps({**identity, "token": "wrong"}))
        with self.assertRaisesRegex(ValueError, "Cancellation identity mismatch"):
            worker.cancel(self.root, self.request["jobId"])
        self.assertFalse((job / "cancel.json").exists())
        (job / "reservation.json").write_text(json.dumps(identity))
        self.terminal(job)
        with self.assertRaisesRegex(ValueError, "already terminal"):
            worker.cancel(self.root, self.request["jobId"])

    def test_cancel_publishes_complete_identity_once(self):
        job = worker.prepare(self.root, self.request)
        worker.cancel(self.root, self.request["jobId"])
        marker = json.loads((job / "cancel.json").read_text())
        identity = json.loads((job / "reservation.json").read_text())
        self.assertEqual(marker, {**{k:identity[k] for k in ("jobId", "token")}, "requested": True})
        with self.assertRaises(FileExistsError):
            worker.cancel(self.root, self.request["jobId"])
        self.assertEqual(json.loads((job / "cancel.json").read_text()), marker)

    def p3_job(self):
        request = {**self.request, "recipe": worker.NONLINEAR_RECIPE,
                   "inputs": [{**i, "width": 1000, "height": 800} for i in self.inputs]}
        return worker.prepare(self.root, request)

    def p3_events(self, job, mask_evidence=True):
        ordinal = 0
        masked = {"background-color", "contrast-large", "contrast-small", "contrast-curve", "nebula-color"}
        for label, process in worker.NONLINEAR_ACTIONS:
            if label in masked and mask_evidence:
                worker.write_new(job / f"events/{ordinal:04}-mask.json", dict(event="mask-attached", data=dict(target="Synthetic_target", mask="Synthetic_mask", inverted=label == "background-color")))
                ordinal += 1
            worker.write_new(job / f"events/{ordinal:04}-start.json", dict(event="process-started", data=dict(label=label, target="Synthetic_target", nativeSource=f"var P = new {process};", dependencies=["Synthetic_mask"])))
            ordinal += 1
            worker.write_new(job / f"events/{ordinal:04}-completed.json", dict(event="process-completed", data=dict(label=label, target="Synthetic_target")))
            ordinal += 1
            if label in masked and mask_evidence:
                worker.write_new(job / f"events/{ordinal:04}-unmask.json", dict(event="mask-detached", data=dict(target="Synthetic_target")))
                ordinal += 1

    def test_p3_exports_all_actions_with_mask_context(self):
        job = self.p3_job()
        self.p3_events(job)
        result = worker.export_runtime_instances(job, dict(jobId=self.request["jobId"], recipe=worker.NONLINEAR_RECIPE, processCount=29))
        self.assertEqual(result["instanceCount"], 29)
        report = json.loads((job / "runtime-correlations.json").read_text())
        self.assertEqual(sum("mask" in p for p in report["instances"]), 5)
        self.assertEqual(report["upstreamHistoryCompleteness"], "NOT_ESTABLISHED")

    def test_p3_missing_masks_cannot_export_complete_workflow(self):
        job = self.p3_job()
        self.p3_events(job, False)
        with self.assertRaisesRegex(ValueError, "mask evidence"):
            worker.export_runtime_instances(job, dict(jobId=self.request["jobId"], recipe=worker.NONLINEAR_RECIPE, processCount=29))
        self.assertFalse((job / "workflow.js").exists())

    def test_p3_recipe_downgrade_receipt_retains_reservation(self):
        job = self.p3_job()
        self.terminal(job)
        with self.assertRaisesRegex(ValueError, "recipe mismatch"):
            worker.collect(self.root, self.request["jobId"])
        self.assertTrue((self.root / "active-job.json").exists())

    def p3_completed(self):
        job = self.p3_job()
        manifest = json.loads((job / "manifest.json").read_text())
        self.p3_events(job)
        outputs = {r + "-linear.xisf": (1, False) for r in worker.ROLES} | {"RGB-linear.xisf": (3, False)} | worker.NONLINEAR_OUTPUTS
        receipt_outputs = []
        for name, (channels, nonlinear) in outputs.items():
            path = job / "outputs" / name
            extra = 'location="attachment:4096:9600000"' if name == "LRGB-nonlinear.xisf" else ''
            header = f'<xisf><Image geometry="1000:800:{channels}" sampleFormat="Float32" colorSpace="{"RGB" if channels == 3 else "Gray"}" {extra}/></xisf>'.encode()
            with path.open("wb") as stream:
                stream.write(b"XISF0100" + struct.pack("<II", len(header), 0) + header)
                if name == "LRGB-nonlinear.xisf":
                    stream.truncate(4096 + 9600000)
                    for channel in range(3):
                        stream.seek(4096 + channel * 3200000)
                        stream.write(struct.pack("<f", 0.5))
            receipt_outputs.append(dict(name=name, sha256=worker.digest(path), nonLinear=nonlinear))
        worker.write_new(job / "terminal.json", dict(jobId=manifest["jobId"], token=manifest["token"], recipe=worker.NONLINEAR_RECIPE,
                         runtimeSha256=manifest["runtimeSha256"], status="COMPLETED", outputs=receipt_outputs, processCount=29,
                         exclusiveLeaseVerified=True, originalViewsUnmodified=True))
        return job

    def test_p3_collect_validates_pixels_and_remains_owner_review_required(self):
        self.p3_completed()
        result = worker.collect(self.root, self.request["jobId"])
        self.assertEqual(result["outputCount"], 15)
        self.assertEqual(result["workflowInstanceCount"], 29)
        self.assertTrue(result["pixelVerification"]["allFinite"])
        self.assertEqual(result["scientificAcceptance"], "OWNER_REVIEW_REQUIRED")
        self.assertEqual(worker.collect(self.root, self.request["jobId"]), result)

    def test_p3_invalid_pixel_retains_reservation_despite_matching_output_hash(self):
        job = self.p3_completed()
        path = job / "outputs/LRGB-nonlinear.xisf"
        with path.open("r+b") as stream:
            stream.seek(4096)
            stream.write(struct.pack("<f", float("nan")))
        receipt_path = job / "terminal.json"
        receipt = json.loads(receipt_path.read_text())
        next(o for o in receipt["outputs"] if o["name"] == path.name)["sha256"] = worker.digest(path)
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValueError, "Nonfinite"):
            worker.collect(self.root, self.request["jobId"])
        self.assertTrue((self.root / "active-job.json").exists())
        self.assertFalse((job / "verification.json").exists())

    @unittest.skipUnless(os.name == "nt", "Actual Windows sharing-mode proof")
    def test_cancel_while_windows_exclusive_handle_is_held(self):
        import ctypes
        from ctypes import wintypes
        job = worker.prepare(self.root, self.request)
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        kernel.CreateFileW.restype = wintypes.HANDLE
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle.restype = wintypes.BOOL
        handle = kernel.CreateFileW(str(self.root / "active-job.json"), 0xC0000000, 0, None, 3, 0x80, None)
        self.assertNotEqual(handle, ctypes.c_void_p(-1).value)
        try:
            with self.assertRaises(PermissionError):
                (self.root / "active-job.json").read_text()
            worker.cancel(self.root, self.request["jobId"])
            self.assertTrue((job / "cancel.json").exists())
        finally:
            self.assertTrue(kernel.CloseHandle(handle))


if __name__ == "__main__":
    unittest.main()
