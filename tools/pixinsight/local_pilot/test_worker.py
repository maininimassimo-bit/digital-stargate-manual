"""Synthetic coordinator tests; no PixInsight or scientific pixels exercised."""
from pathlib import Path
import json
import tempfile
import unittest
import struct

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

    def test_second_job_rejected_while_reserved(self):
        worker.prepare(self.root, self.request)
        other = {**self.request, "jobId": "Synthetic_02"}
        with self.assertRaises(FileExistsError):
            worker.prepare(self.root, other)
        self.assertFalse((self.root / "Synthetic_02").exists())

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


if __name__ == "__main__":
    unittest.main()
