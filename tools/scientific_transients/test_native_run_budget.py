"""Synthetic clocks only; no sleeping, filesystem, processes or fresh grants."""
import datetime as dt
import unittest

from tools.scientific_transients.native_run_budget import LiveNativeBudget


class LiveNativeBudgetTests(unittest.TestCase):
    def setUp(self):
        self.mono=10.0; self.wall=dt.datetime(2026,10,16,10,0,0,tzinfo=dt.timezone.utc)
        self.budget=LiveNativeBudget(monotonic=lambda:self.mono,wall=lambda:self.wall)

    def test_original_deadline_is_not_reset_by_phases_or_retention(self):
        for elapsed in [20,100,179]:
            self.mono=10+elapsed; self.budget.require_running()
            self.assertEqual(self.budget.deadline_monotonic,190)
        self.mono=190
        with self.assertRaisesRegex(Exception,'NATIVE_BUDGET_EXPIRED'): self.budget.require_running()
        self.assertEqual(self.budget.publication_clock(),190)
        self.assertTrue(self.budget.diagnostic()['parentMonotonicDeadlineExceeded'])

    def test_stalled_utc_does_not_renew_monotonic_budget(self):
        self.mono=191
        self.assertTrue(self.budget.check()['parentMonotonicDeadlineExceeded'])
        self.assertFalse(self.budget.diagnostic()['parentWallDeadlineExceeded'])

    def test_wall_expiry_also_blocks_computation(self):
        self.wall+=dt.timedelta(seconds=180)
        with self.assertRaisesRegex(Exception,'NATIVE_BUDGET_EXPIRED'): self.budget.require_running()
        self.assertTrue(self.budget.diagnostic()['parentWallDeadlineExceeded'])
        self.assertFalse(self.budget.diagnostic()['parentMonotonicDeadlineExceeded'])

    def test_backward_monotonic_is_permanently_uncertain(self):
        self.mono=9
        with self.assertRaisesRegex(Exception,'NATIVE_BUDGET_CLOCK_REVERSED'): self.budget.check()
        self.mono=11
        with self.assertRaisesRegex(Exception,'NATIVE_BUDGET_CLOCK_UNCERTAIN'): self.budget.check()
        self.assertTrue(self.budget.diagnostic()['clockUncertain'])

    def test_backward_wall_is_permanently_uncertain(self):
        self.wall-=dt.timedelta(microseconds=1)
        with self.assertRaisesRegex(Exception,'NATIVE_BUDGET_CLOCK_REVERSED'): self.budget.check()
        self.assertTrue(self.budget.diagnostic()['clockUncertain'])

    def test_invalid_monotonic_values_never_become_elapsed_zero(self):
        for value in [True,float('nan'),float('inf'),-1,'10',2**41]:
            with self.subTest(value=value):
                with self.assertRaises(Exception): LiveNativeBudget(monotonic=lambda:value,wall=lambda:self.wall)

    def test_wall_must_be_utc_aware_datetime(self):
        for value in [self.wall.replace(tzinfo=None),'2026-10-16T10:00:00Z',
                      self.wall.astimezone(dt.timezone(dt.timedelta(hours=1)))]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(Exception,'NATIVE_BUDGET_WALL'):
                    LiveNativeBudget(monotonic=lambda:10,wall=lambda:value)

    def test_fractional_wall_deadline_is_conservative(self):
        self.wall=self.wall.replace(microsecond=900000)
        budget=LiveNativeBudget(monotonic=lambda:self.mono,wall=lambda:self.wall)
        self.assertEqual(budget.deadline_utc,'2026-10-16T10:03:00Z')

    def test_time_spent_inside_wall_callback_is_counted(self):
        def wall():
            self.mono+=91
            return self.wall
        budget=LiveNativeBudget(monotonic=lambda:self.mono,wall=wall)
        self.assertTrue(budget.diagnostic()['parentMonotonicDeadlineExceeded'])
        with self.assertRaisesRegex(Exception,'NATIVE_BUDGET_EXPIRED'): budget.require_running()

    def test_diagnostic_is_copy_and_never_grants_authority(self):
        value=self.budget.diagnostic(); value['clockUncertain']=True
        self.assertFalse(self.budget.diagnostic()['clockUncertain'])
        self.assertFalse(value['newNativeStartAllowed']); self.assertFalse(value['processClosureAuthorized'])


if __name__=='__main__': unittest.main()
