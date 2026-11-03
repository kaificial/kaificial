"""Act 8 (23.5 - 31 s): Sesame wins, spider style.

Mochi goes for one last flying kick. Sesame's spider-sense goes off and she backflips over it,
webs Mochi's feet and paws, yanks her off the ground and hangs her from the rule in a cocoon.
She perches above her catch, web-yanks every word back into place, salutes and swings away.
Then the strand snaps, the cocoon drops back into the tunnel, and the loop starts over.
"""
import math

from engine.camera import jolt
from engine.config import EPS, FLOOR, RULE_Y
from engine.effects import fixed, flash, paw, spark, speed_lines, strand, tingle, web_splat
from engine.props import Prop
from engine.svg import num
from engine.timeline import sample

from . import tunnel
from .cast import mochi, mochi_digging, sesame
from .page import all_words

COCOON_HANG = (232.0, 136.0)               # where the cocoon hangs, under the rule
COCOON_ANCHOR = (COCOON_HANG[0], float(RULE_Y))
STRAND_SNAPS = tunnel.DIG_BACK_IN - 0.35


def play(landed):
    t_kick = _flying_kick(landed + 0.35)
    t_wrapped = _web_up(t_kick)
    cocoon, t_hung = _hang_cocoon(t_wrapped)
    t_perched = _perch(t_hung + 0.22)
    t_bye = _tidy_up(t_perched)
    _swing_away(t_bye)
    _drop_cocoon(cocoon)


def _flying_kick(t0):
    """Mochi goes for one last flying kick, and Sesame backflips clean over it. Returns the kick time."""
    mochi.katana(t0, False)
    mochi.pose(t0 - 0.1, "crouch", 0.12)
    mochi.pose(t0 + 0.12, "stand", 0.14)
    mochi.face(t0, 1)
    sesame.pose(t0 + 0.1, "crouch", 0.14)
    sesame.pose(t0 + 0.3, "stand", 0.12)
    sesame.face(t0 + 0.3, -1)

    mochi.pose(t0 + 0.42, "crouch", 0.08)
    mochi.run(t0 + 0.5, t0 + 0.8, 540, frame=0.06)
    t_kick = t0 + 0.8
    mochi.takeoff(t_kick)
    mochi.pose(t_kick + 0.06, "fkick", 0.05, "snap")
    mochi.jump(t_kick, t_kick + 0.38, 660, FLOOR, 26)
    speed_lines(620, t_kick, t_kick + 0.3, FLOOR, 0, horizontal=True)

    tingle(*sesame.world(t_kick - 0.12, "H"), t_kick - 0.12)
    sesame.pose(t_kick, "crouch", 0.05)
    sesame.takeoff(t_kick + 0.04)
    sesame.jump(t_kick + 0.04, t_kick + 0.46, 500, FLOOR, 48)
    sesame.spin(t_kick + 0.06, t_kick + 0.44, -360)
    sesame.pose(t_kick + 0.1, "tuck", 0.05)
    sesame.pose(t_kick + 0.4, "fall", 0.05)
    sesame.land(t_kick + 0.46, 0.22)
    sesame.face(t_kick + 0.48, 1)
    mochi.pose(t_kick + 0.34, "fall", 0.05)
    mochi.land(t_kick + 0.38, 0.24)
    mochi.face(t_kick + 0.52, -1)
    return t_kick


def _web_up(t_kick):
    """Thwip: Mochi's feet are stuck to the floor. Thwip: her paws. Thwip: she's yanked off the ground.
    Returns the moment she disappears into the cocoon."""
    t_feet = t_kick + 0.62
    t_paws = t_feet + 0.22
    t_yank = t_paws + 0.25
    t_wrapped = t_yank + 0.15

    sesame.pose(t_feet, "punch", 0.04, "snap")
    strand(paw(sesame), fixed((662.0, FLOOR - 2.0)), t_feet, t_feet + 0.16, "web", 1.0, shoot=0.07)
    web_splat(662, FLOOR - 2, t_feet + 0.07, t_wrapped - t_feet - 0.07, 1.3)
    mochi.pose(t_feet + 0.08, "hit", 0.04)
    mochi.jitter(t_feet + 0.1, t_yank + 0.1, 0.6)

    sesame.pose(t_paws, "push", 0.04, "snap")
    mochi_paw = mochi.world(t_paws + 0.07, "RH")
    strand(paw(sesame, "LH"), fixed(mochi_paw), t_paws, t_paws + 0.16, "web", 1.0, shoot=0.07)
    web_splat(mochi_paw[0], mochi_paw[1], t_paws + 0.07, t_wrapped - t_paws - 0.07, 1.0)

    sesame.pose(t_yank, "punch", 0.04, "snap")
    sesame.pose(t_yank + 0.12, "tug2", 0.05, "snap")
    jolt(t_yank + 0.12, 1.5)
    mochi.hide(t_wrapped)
    return t_wrapped


def _cocoon_drawing(p):
    """Mochi wrapped up head to toe, only her ears and eyes poking out."""
    body = p["cat_w"]
    line = p["cat_w_line"]
    wraps = "".join(f'<path d="M-9,{num(-16 + 6 * i)} Q0,{num(-12 + 6 * i)} 9,{num(-18 + 6 * i)}" fill="none" stroke="{p["web"]}" stroke-width="0.9"/>' for i in range(6))
    return (f'<path d="M-6.5,-30 L-5.5,-38 L-2,-31 Z" fill="{body}" stroke="{line}" stroke-width="0.9" stroke-linejoin="round"/>'
            f'<path d="M2,-31 L5.5,-38 L6.5,-30 Z" fill="{body}" stroke="{line}" stroke-width="0.9" stroke-linejoin="round"/>'
            f'<ellipse cx="0" cy="-15" rx="10" ry="17" fill="{p["bg"]}" stroke="{p["web"]}" stroke-width="1.4"/>'
            + wraps
            + f'<ellipse cx="0" cy="-26" rx="6" ry="3.4" fill="{body}" stroke="{line}" stroke-width="0.6"/>'
            f'<circle cx="-2.2" cy="-26.3" r="1" fill="{p["cat_w_eye"]}"/><circle cx="2.2" cy="-26.3" r="1" fill="{p["cat_w_eye"]}"/>')


def _hang_cocoon(t_wrapped):
    """The cocoon gets yanked over Sesame's head in a big arc and stuck to the rule, where it sways.
    Returns the cocoon and the time it's hung."""
    t_yank = t_wrapped - 0.15
    cocoon = Prop(_cocoon_drawing, 660, FLOOR - 4)
    cocoon.opacity.set(t_wrapped, 1)
    hang_x, hang_y = COCOON_HANG
    cocoon.pos.hold(t_wrapped)
    for i in range(1, 9):
        s = i / 8
        cocoon.pos.add(t_wrapped + 0.6 * s, (660 + (hang_x - 660) * s, FLOOR - 4 + (hang_y - FLOOR + 4) * s - 150 * math.sin(math.pi * s)))
    t_hung = t_wrapped + 0.6

    def cocoon_top(t):
        x, y = sample(cocoon.pos, t)
        return x, y - 36

    strand(paw(sesame), cocoon_top, t_yank, t_hung, "web", 1.0, shoot=0.08)
    spark(*COCOON_HANG, t_hung, 6, kind="white")
    sesame.pose(t_wrapped + 0.1, "windup", 0.1)
    sesame.pose(t_hung - 0.05, "mega", 0.05, "snap")

    strand(fixed(COCOON_ANCHOR), cocoon_top, t_hung, STRAND_SNAPS, "web", 1.0, shoot=0.01, knot=False)
    web_splat(COCOON_ANCHOR[0], COCOON_ANCHOR[1], t_hung, STRAND_SNAPS - t_hung, 0.8)
    amp, t = 26.0, t_hung
    while t < tunnel.DIG_BACK_IN - 0.5:          # each swing a little smaller than the last
        t += 0.32
        amp *= 0.72
        side = 1 if int((t - t_hung) / 0.32) % 2 else -1
        dx = side * amp
        cocoon.pos.add(t, (hang_x + dx, hang_y - abs(dx) * 0.12), "inout")
    cocoon.pos.hold(STRAND_SNAPS)
    return cocoon, t_hung


def _perch(t0):
    """She zips up onto the rule beside her catch and crouches there. Returns when she's settled."""
    sesame.pose(t0, "point", 0.05, "snap")
    strand(paw(sesame), fixed((300.0, -2.0)), t0, t0 + 0.32, "web", 1.0, shoot=0.06)
    sesame.pose(t0 + 0.06, "fly", 0.05)
    sesame.stay(t0 + 0.06)
    sesame.at(t0 + 0.32, 300, RULE_Y, "in")
    sesame.land(t0 + 0.32, 0.22)
    sesame.face(t0 + 0.34, -1)
    sesame.pose(t0 + 0.45, "crouch", 0.1)
    return t0 + 0.45


def _tidy_up(t0):
    """A few quick web-yanks, and every word that moved flies back home. Returns when she's done."""
    moved = [w for w in all_words() if w.animated]
    for k, w in enumerate(moved[::max(1, len(moved) // 5)][:5]):
        t = t0 + 0.1 * k
        sesame.pose(t, "punch" if k % 2 == 0 else "point", 0.04, "snap")
        strand(paw(sesame), w.pos, t, t + 0.14, "web", 0.9, shoot=0.05)
    sesame.pose(t0 + 0.6, "crouch", 0.1)
    for i, w in enumerate(moved):
        t = t0 + 0.012 * i
        if w.halves:                                   # the two halves fade out as the whole word comes back
            for half in w.halves:
                half.opacity.hold(t)
                half.opacity.add(t + 0.15, 0, "in")
        w.opacity.hold(t)
        if sample(w.opacity, t) < 0.99 or w.halves:
            w.opacity.add(t + 0.2, 1, "out")
        if w.scale.end_value != 1.0:
            w.scale.hold(t)
            w.scale.add(t + 0.6, 1.0, "inout")
        w.restore(t, t + 0.6)
        spark(w.cx, w.cy, t + 0.6, 3, kind="white", dur=0.2)
    return t0 + 0.7


def _swing_away(t0):
    """A two-finger salute, and she swings off the top of the page."""
    sesame.pose(t0, "wave1", 0.1)
    sesame.pose(t0 + 0.16, "wave2", 0.08)
    sesame.pose(t0 + 0.34, "fly", 0.06, "snap")
    exit_x = 420.0
    strand(paw(sesame), fixed((exit_x, -4.0)), t0 + 0.34, t0 + 0.72, "web", 1.0, shoot=0.06)
    sesame.stay(t0 + 0.4)
    sesame.at(t0 + 0.72, exit_x, -60, "in")
    sesame.hide(t0 + 0.74)
    assert t0 + 0.8 < STRAND_SNAPS, "Sesame has to be gone before the strand snaps"


def _drop_cocoon(cocoon):
    """The strand gives way. The cocoon drops onto the page and smashes through the blocks into the tunnel."""
    reopen = tunnel.DIG_BACK_IN
    spark(COCOON_ANCHOR[0], COCOON_ANCHOR[1] + 2, STRAND_SNAPS, 4, kind="white")
    cocoon.pos.add(reopen, (172.0, tunnel.FLOOR_Y - 6.0), "in")
    jolt(reopen, 3)
    flash(reopen, 0.05, 0.25)
    cocoon.pos.add(reopen + 0.35, (170.0, tunnel.FLOOR_Y + 10.0), "in")
    cocoon.scale.hold(reopen)
    cocoon.scale.add(reopen + 0.35, 0.6, "in")
    cocoon.opacity.hold(reopen + 0.2)
    cocoon.opacity.add(reopen + 0.35, 0, "in")
    # Off screen, Mochi wriggles free in the dark and gets ready to dig her way out again.
    # This lines everything up with the first frame, so the loop is seamless.
    mochi.put(reopen + 0.7, 170, tunnel.FLOOR_Y)
    mochi.squash.set(reopen + 0.7, (0.72, 0.72))
    mochi.pose(reopen + 0.7, "dig_hold", EPS)
    mochi.face(reopen + 0.7, -1)
    mochi_digging.pose(reopen + 0.7, "dig_hold", EPS)
