"""The camera: screen shake, and the vertical pan up into the sky and back down."""
from .config import EPS
from .svg import rnd
from .timeline import Track

SHAKE = Track((0.0, 0.0))       # offset of the whole frame
PAN = Track((0.0, 0.0))         # offset of the page and the near sky
PAN_FAR = Track((0.0, 0.0))     # offset of the far stars (they move slower, for depth)
FAR_PARALLAX = 0.55


def jolt(t, amp):
    """One quick knock that settles in about 0.16 s."""
    SHAKE.hold(t - EPS)
    for dt, fx, fy in [(0.03, 1, -0.6), (0.07, -0.7, 0.5), (0.11, 0.4, -0.3), (0.16, 0, 0)]:
        SHAKE.add(t + dt, (amp * fx, amp * fy), "out")


def rumble(t0, t1, amp0, amp1):
    """A steady shake that grows (or fades) from amp0 to amp1."""
    SHAKE.hold(t0)
    t, i = t0, 0
    while t < t1 - 0.04:
        t += 0.04
        i += 1
        a = amp0 + (amp1 - amp0) * (t - t0) / (t1 - t0)
        SHAKE.add(t, (a * (rnd(i * 5.3) - 0.5) * 2, a * (rnd(i * 9.1) - 0.5) * 2))
    SHAKE.add(t1, (0.0, 0.0))


def pan(t0, t1, y):
    """Slide the world down by y between t0 and t1 (so the camera looks up)."""
    PAN.hold(t0)
    PAN.add(t1, (0.0, float(y)), "inout")
    PAN_FAR.hold(t0)
    PAN_FAR.add(t1, (0.0, float(y) * FAR_PARALLAX), "inout")
