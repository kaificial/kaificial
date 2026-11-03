"""Keyframe tracks. Everything that moves in the film is a Track of [time, value, ease] keys."""
from .config import LOOP, EPS

# Easing curves, written the way SVG's keySplines wants them.
SPLINES = {"lin": "0 0 1 1", "in": "0.55 0 1 1", "out": "0 0 0.45 1", "inout": "0.45 0 0.55 1", "snap": "0 0 0.15 1"}


class Track:
    """One animated value over time.

    Keys only ever move forward. If you add a key at or before the last one, it gets nudged
    a hair later, so the order you write the choreography in is the order it plays in.
    """

    def __init__(self, start_value):
        self.keys = [[0.0, start_value, "lin"]]

    @property
    def end_time(self):
        return self.keys[-1][0]

    @property
    def end_value(self):
        return self.keys[-1][1]

    def add(self, t, v, ease="lin"):
        """Tween to v, arriving at time t."""
        if t <= self.end_time:
            t = self.end_time + EPS
        self.keys.append([round(t, 5), v, ease])

    def hold(self, t):
        """Stay at the current value until time t."""
        if t > self.end_time + 1e-9:
            self.keys.append([round(t, 5), self.end_value, "lin"])

    def set(self, t, v):
        """Jump straight to v at time t."""
        self.hold(t - EPS)
        self.add(t, v)

    def finished(self):
        """The keys, padded out so the last value holds until the loop ends."""
        keys = [list(k) for k in self.keys]
        assert keys[-1][0] <= LOOP, f"key past loop end {keys[-1]}"
        if keys[-1][0] < LOOP:
            keys.append([LOOP, keys[-1][1], "lin"])
        return keys


def _find_key(keys, t):
    """Index of the last key at or before t."""
    lo, hi = 0, len(keys) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if keys[mid][0] <= t:
            lo = mid
        else:
            hi = mid - 1
    return lo


def eased(s, ease):
    """Apply an easing curve to s (0..1), the same way the browser does.

    We need this so we can ask "where is she right now?" in the middle of a tween and get the
    same answer the animation shows on screen.
    """
    if ease == "lin" or s <= 0 or s >= 1:
        return s
    x1, y1, x2, y2 = (float(v) for v in SPLINES[ease].split())
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        x = 3 * (1 - mid) ** 2 * mid * x1 + 3 * (1 - mid) * mid ** 2 * x2 + mid ** 3
        if x < s:
            lo = mid
        else:
            hi = mid
    u = (lo + hi) / 2
    return 3 * (1 - u) ** 2 * u * y1 + 3 * (1 - u) * u ** 2 * y2 + u ** 3


def segment(keys, t):
    """The two keys around time t, and how far (eased) we are between them."""
    i = _find_key(keys, t)
    if i >= len(keys) - 1:
        return keys[-1], keys[-1], 0.0
    t0 = keys[i][0]
    t1, _, ease = keys[i + 1]
    s = 0 if t1 == t0 else (t - t0) / (t1 - t0)
    return keys[i], keys[i + 1], eased(s, ease)


def sample(track, t):
    """The value of a number (or tuple of numbers) track at time t."""
    k0, k1, s = segment(track.keys, t)
    v0, v1 = k0[1], k1[1]
    if isinstance(v0, (int, float)):
        return v0 + (v1 - v0) * s
    return tuple(a + (b - a) * s for a, b in zip(v0, v1))


def sample_step(track, t):
    """The value of a track at time t, without tweening (for things like facing direction)."""
    return track.keys[_find_key(track.keys, t)][1]


def window(track, t0, t1):
    """A copy of the track that only keeps the keys between t0 and t1.

    Handy for props that are hidden outside that window: their animation stays small.
    """
    w = Track(sample_step(track, t0))
    w.hold(t0 - EPS)
    for t, v, ease in track.keys:
        if t0 <= t <= t1:
            w.add(t, v, ease)
    w.hold(t1)
    return w
