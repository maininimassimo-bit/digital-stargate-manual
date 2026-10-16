"""Original live 180-second budget. No IO, grants, process starts or recovery."""
import datetime as dt
import math
import time

from tools.pixinsight.local_pilot.broker import require


def _monotonic(value):
    require(type(value) in {int,float} and math.isfinite(value) and 0 <= value <= 2**40,
            'NATIVE_BUDGET_MONOTONIC')
    return value


def _wall(value):
    require(type(value) is dt.datetime and value.tzinfo is not None
            and value.utcoffset() == dt.timedelta(0), 'NATIVE_BUDGET_WALL')
    return value


class LiveNativeBudget:
    """Create before first preparation IO; retain this same object for the attempt.

    No timeout argument, renew/reset operation or constructor from persisted data.
    Clocks are trusted callbacks; they cannot authenticate consent or loaded code.
    """
    def __init__(self, *, monotonic=time.monotonic, wall=lambda:dt.datetime.now(dt.timezone.utc)):
        require(callable(monotonic) and callable(wall), 'NATIVE_BUDGET_CLOCKS')
        self._clock, self._wall_clock = monotonic, wall
        self._uncertain = False; self._mono_expired = False; self._wall_expired = False
        self._origin = _monotonic(monotonic())
        self._deadline = self._origin + 180
        require(self._deadline-self._origin == 180, 'NATIVE_BUDGET_PRECISION')
        self._origin_wall = _wall(wall())
        # Canonical native timestamps have whole seconds. Flooring is conservative.
        self._wall_deadline = (self._origin_wall+dt.timedelta(seconds=180)).replace(microsecond=0)
        self._last_mono, self._last_wall = self._origin, self._origin_wall
        self.check()

    @property
    def origin_monotonic(self): return self._origin

    @property
    def deadline_monotonic(self): return self._deadline

    @property
    def deadline_utc(self): return self._wall_deadline.strftime('%Y-%m-%dT%H:%M:%SZ')

    def check(self):
        """Observe both clocks without rejecting a known overrun needed for cleanup."""
        require(not self._uncertain, 'NATIVE_BUDGET_CLOCK_UNCERTAIN')
        try:
            first = _monotonic(self._clock())
            wall = _wall(self._wall_clock())
            last = _monotonic(self._clock())
            require(self._last_mono <= first <= last and self._last_wall <= wall,
                    'NATIVE_BUDGET_CLOCK_REVERSED')
            self._last_mono, self._last_wall = last, wall
            self._mono_expired |= last >= self._deadline
            self._wall_expired |= wall >= self._wall_deadline
        except BaseException:
            self._uncertain = True
            raise
        return self.diagnostic()

    def require_running(self):
        self.check()
        require(not self._mono_expired and not self._wall_expired, 'NATIVE_BUDGET_EXPIRED')

    def publication_clock(self):
        """Trusted clock for byte retention, paired with deadline_monotonic; no new origin."""
        self.check()
        return self._last_mono

    def diagnostic(self):
        """Cached facts only; never a fresh observation or process-stop receipt."""
        return {'parentMonotonicDeadlineExceeded': self._mono_expired,
                'parentWallDeadlineExceeded': self._wall_expired,
                'clockUncertain': self._uncertain, 'parentDeadlineUTC': self.deadline_utc,
                'budgetSeconds': 180, 'newNativeStartAllowed': False,
                'processClosureAuthorized': False}
