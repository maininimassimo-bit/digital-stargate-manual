from pathlib import Path
import subprocess
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[2]
# BaseLoader preserves GitHub's `on` key and literal input strings.
BASE=yaml.load(subprocess.check_output(['git','show','597963f63f974607eb6c10723487dc3bc4f43097:.github/workflows/analyze-session-automatic.yml'],cwd=ROOT,text=True),Loader=yaml.BaseLoader)
NEW=yaml.load((ROOT/'.github/workflows/analyze-session-automatic.yml').read_text(),Loader=yaml.BaseLoader)

class Tests(unittest.TestCase):
    def test_scientific_job_unchanged_except_guard(self):
        job=dict(NEW['jobs']['analyze']);guard=job.pop('if')
        steps=[]
        for step in job['steps']:
            if step.get('id')=='acquisition': continue
            step=dict(step)
            if 'if' in step: step['if']=step['if'].replace(" && steps.acquisition.outputs.skip != 'true'",'')
            steps.append(step)
        job['steps']=steps
        self.assertEqual(job,BASE['jobs']['analyze'])
        self.assertEqual(guard,"github.ref == 'refs/heads/main' && (github.event_name != 'workflow_dispatch' || inputs.telemetry_probe == 'off' || inputs.telemetry_probe == '')")
    def test_no_acquisition_guard_only_narrows_scientific_publication(self):
        steps=NEW['jobs']['analyze']['steps']
        guard=next(step for step in steps if step.get('id')=='acquisition')
        self.assertIn('python .github/scripts/check-session-acquisition.py --session',guard['run'])
        self.assertEqual(guard['if'],"steps.resolve.outputs.skip != 'true'")
        for step in steps[steps.index(guard)+1:]:
            self.assertIn("steps.acquisition.outputs.skip != 'true'",step['if'])

    def test_trigger_and_session_input_preserved(self):
        self.assertEqual(NEW['name'],BASE['name'])
        # Scientific work starts only after the package is promoted to main.
        self.assertEqual(NEW['on']['push']['branches'],['main'])
        self.assertEqual(NEW['on']['push']['paths'],BASE['on']['push']['paths'])
        self.assertEqual(NEW['on']['workflow_dispatch']['inputs']['session_id'],BASE['on']['workflow_dispatch']['inputs']['session_id'])
    def test_probe_cannot_checkout_or_request_permissions(self):
        job=NEW['jobs']['telemetry_probe']
        self.assertEqual(job['permissions'],{})
        self.assertEqual(job['timeout-minutes'],'6')
        self.assertEqual(len(job['steps']),1)
        self.assertNotIn('uses',job['steps'][0])
        text=job['steps'][0]['run']
        for forbidden in ('git ', 'gh ', 'curl ', 'python ', 'node ', 'secrets.', 'GITHUB_TOKEN'):
            self.assertNotIn(forbidden,text)
    def test_confirmation_main_and_modes(self):
        step=NEW['jobs']['telemetry_probe']['steps'][0]
        self.assertIn('test "$PROBE_CONFIRMED" = \'true\'',step['run'])
        self.assertIn('test "$PROBE_REF" = \'refs/heads/main\'',step['run'])
        self.assertIn('sleep 300',step['run'])
        self.assertIn('F4_CANCELLATION_NOT_OBSERVED',step['run'])
        self.assertEqual(NEW['on']['workflow_dispatch']['inputs']['telemetry_probe']['default'],'off')
    def test_concurrency_does_not_cancel_science(self):
        c=NEW['concurrency']
        self.assertEqual(c['cancel-in-progress'],'false')
        self.assertIn("format('f4-telemetry-probe-{0}', github.run_id)",c['group'])
        self.assertIn("'scientific-analytics-projection-main'",c['group'])
    def test_skipped_is_all_jobs_skipped_only_when_confirmed_on_main(self):
        guard=NEW['jobs']['telemetry_probe']['if']
        self.assertIn("inputs.telemetry_probe != 'skipped' || !inputs.confirm_telemetry_probe || github.ref != 'refs/heads/main'",guard)
        # GitHub runtime conclusion/event emission remains to be tested live.
        self.assertNotIn('needs',NEW['jobs']['telemetry_probe'])

if __name__=='__main__':unittest.main(verbosity=2)
