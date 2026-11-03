"""Act 4 (9.2 - 13.4 s): grapple wires, portals and the giant.

Mochi wires into the heading and spins through "designing". Sesame steps through a portal to
the right side of the page, turns into a giant and sweeps words off the page. Mochi wires over
her head and cuts the back of her neck, and the giant shrinks back down in a cloud of steam.
"""
from engine.camera import jolt, rumble
from engine.config import EPS, FLOOR, RULE_Y
from engine.effects import (bolt, crescent, dust, fixed, floor_crack, paw, poof, portal, ring, spark,
                            speed_lines, steam, strand, tint, trail)
from engine.moves import heavy_slash, hit

from .cast import mochi, sesame
from .page import on_top, word

GIANT_X = 640.0       # where Sesame stands while she's a giant
GIANT_SCALE = 4.4


def play():
    _grapple_and_portal()
    _transform()
    _sweep()
    _nape_cut()


def _grapple_and_portal():
    # Mochi fires two wires into the heading and reels in, spinning, blade out
    designing = word(0, "designing")
    mochi.pose(9.22, "ww_cast", 0.06, "snap")
    strand(paw(mochi, "LH"), fixed((86.0, 10.0)), 9.24, 9.66, "wire", 0.9, shoot=0.06)
    strand(paw(mochi, "RH"), fixed((124.0, 12.0)), 9.26, 9.66, "wire", 0.9, shoot=0.06)
    mochi.pose(9.34, "sw_idle", 0.05)
    mochi.stay(9.34)
    mochi.at(9.62, 70, 48, "in")
    mochi.spin(9.34, 9.62, -1080, "in")
    speed_lines(116, 9.34, 9.62, 104, 0, horizontal=True)
    designing.slice(9.48, -15, through=(designing.cx, designing.cy))
    spark(designing.cx, designing.cy, 9.48, 7)
    crescent(84, 70, 22, 0, 330, 9.46, dur=0.14)

    # but Sesame was never there: she steps into a ring of sparks and out of another one
    # on the empty right side of the page
    portal(70, 32, 9.28, 9.6)
    portal(640, FLOOR - 22, 9.4, 9.86)
    sesame.face(9.3, 1)
    sesame.stay(9.36)
    sesame.at(9.5, 66, RULE_Y, "in")
    sesame.hide(9.52)
    sesame.put(9.56, 656, FLOOR)
    sesame.face(9.56, -1)
    sesame.pose(9.56, "stand", EPS)
    sesame.show(9.58)
    sesame.at(9.76, 640, FLOOR, "out")
    mochi.jump(9.66, 9.98, 46, on_top(0), 10)
    mochi.land(9.98, 0.18, pose=None)
    mochi.pose(10.08, "sw_idle", 0.1)
    mochi.face(10.1, 1)


def _transform():
    """She bites her paw: lightning, steam, and she rises as a giant."""
    sesame.pose(9.82, "stand", 0.1)
    sesame.pose(9.98, "scratch", 0.08)
    t_shift = 10.18
    bolt(GIANT_X + 18, -20, GIANT_X, FLOOR - 24, t_shift, dur=0.32, col="thunder", core="bolt_core", w=4, jag=12, k=12, seed=41)
    tint(t_shift, "thunder", 0.5, 0.1)
    jolt(t_shift, 5)
    ring(GIANT_X, FLOOR - 16, t_shift, 90, col="thunder", w=2.5)
    poof(GIANT_X, FLOOR - 30, t_shift + 0.04, 3.0)
    sesame.pose(t_shift + 0.02, "crouch", 0.02)
    sesame.squash.hold(t_shift + 0.02)
    sesame.squash.add(10.6, (GIANT_SCALE, GIANT_SCALE), "out")
    sesame.pose(10.6, "stand", 0.2)
    steam(lambda t: (GIANT_X + 20, FLOOR - 70), 10.3, 13.3, every=0.15, size=1.7, spread=90)
    sesame.pose(10.82, "hit", 0.12)
    rumble(10.86, 11.3, 2.6, 0.4)


def _sweep():
    """One giant paw sweeps "new technologies" off the page."""
    sesame.pose(11.38, "windup", 0.22, "inout")
    sesame.pose(11.6, "mega2", 0.06, "snap")
    crescent(GIANT_X - 70, FLOOR - 104, 64, 160, 230, 11.6, dur=0.14)
    jolt(11.6, 4)
    for k, w in enumerate((word(2, "technologies"), word(2, "new"))):
        w.fly(11.62 + 0.03 * k, 12.2 + 0.05 * k, 330 - 60 * k, FLOOR - 6, -300 + 120 * k, 60)
        spark(w.cx, w.cy, 11.62 + 0.03 * k, 6)


def _nape_cut():
    """Mochi wires over the giant's head, drops in behind her and cuts the back of her neck."""
    mochi.pose(11.76, "ww_cast", 0.06, "snap")
    strand(paw(mochi, "LH"), fixed((760.0, float(RULE_Y))), 11.78, 12.3, "wire", 0.9, shoot=0.07)
    strand(paw(mochi, "RH"), fixed((800.0, float(RULE_Y))), 11.8, 12.3, "wire", 0.9, shoot=0.07)
    mochi.pose(11.88, "fly", 0.05)
    mochi.stay(11.88)
    mochi.at(12.28, 720, 72, "in")
    mochi.spin(11.9, 12.28, 720, "in")
    speed_lines(430, 11.95, 12.28, 100, 0, horizontal=True)
    trail(mochi, 11.95, 12.28, "ghost_w", 4)
    nape = (GIANT_X + 14, FLOOR - 25 * GIANT_SCALE)
    mochi.face(12.3, -1)
    mochi.jump(12.3, 12.5, nape[0] + 18, nape[1] + 22, 10)
    heavy_slash(mochi, 12.5)
    crescent(nape[0] + 8, nape[1] - 4, 30, 200, 330, 12.5, dur=0.12)
    hit(12.5, nape[0], nape[1], 14, mochi, sesame, big=True, shake=5)
    poof(nape[0], nape[1], 12.56, 2.0)
    mochi.jump(12.62, 13.02, 520, FLOOR, 30)
    mochi.spin(12.64, 12.98, -360)
    mochi.pose(12.68, "tuck", 0.05)
    mochi.land(13.02, 0.3)
    dust(520, FLOOR, 13.02, big=True)
    floor_crack(520, 13.02)

    # the giant topples and shrinks back down in a cloud of steam
    sesame.pose(12.6, "hit", 0.04)
    sesame.rot_to(12.62, 12.92, 22, "inout", pivot=(0.0, 0.0))
    sesame.squash.hold(12.92)
    sesame.squash.add(13.3, (1.0, 1.0), "in")
    sesame.rot_to(12.92, 13.3, 0, "inout")
    sesame.rot_pivot(13.31)
    sesame.pose(13.3, "lying", 0.06)
    poof(GIANT_X, FLOOR - 50, 12.95, 3.0)
    poof(GIANT_X, FLOOR - 16, 13.25, 2.0)
