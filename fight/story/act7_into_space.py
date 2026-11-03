"""Act 7 (18.2 - 23.5 s): the fight in space.

1. Binary star: they lock paws and spin around each other, trading blows.
2. The moon: Sesame webs the moon and throws it. Mochi cuts it in half.
3. The ambush: Sesame was hiding behind the moon and kicks Mochi's sword away.
4. Hammer throw: Sesame swings Mochi on a web and throws her back down to the page.
"""
import math
from dataclasses import dataclass

from engine import camera
from engine.camera import PAN, jolt
from engine.config import EPS, FLOOR
from engine.effects import aura, dust, flash, floor_crack, paw, ring, smear_line, spark, strand, trail
from engine.layers import layer
from engine.moves import hit
from engine.svg import num, fnum, fmt_xy, fade_group, transform_group, points_str
from engine.timeline import Track, sample

from .cast import mochi, sesame
from .scenery import MOON, SKY_HEIGHT, moon_body, moon_defs


@dataclass
class SpaceTimes:
    pan_up: float       # camera starts moving up
    pan_down: float     # camera starts moving down
    landed: float       # both cats are back on the page


# Tracks that move the moon, relative to its spot in the sky.
_MOON_MOVE = Track((0.0, 0.0))     # position
_MOON_SPIN = Track(0.0)            # rotation
_MOON_FADE = Track(1)
_HALF_MOVE = [Track((0.0, 0.0)), Track((0.0, 0.0))]      # each half after the cut
_HALF_TURN = [Track(0.0), Track(0.0)]


def moon_centre(t):
    dx, dy = sample(_MOON_MOVE, t)
    return (MOON[0] + dx, MOON[1] + dy)


def play(clash):
    _explosion(clash)
    pan_up, pan_up_done = clash.t_boom + 0.1, clash.t_boom + 1.0
    camera.pan(pan_up, pan_up_done, SKY_HEIGHT)
    for c, (x, y), turns in ((mochi, (200.0, 160.0), -720), (sesame, (640.0, 140.0), 720)):
        c.pose(clash.t_boom + 0.02, "tuck", 0.03)
        c.stay(clash.t_boom + 0.02)
        c.arc(clash.t_boom + 0.02, pan_up_done - 0.2, x, y, bend=-30 if c is mochi else 30, ease="out")
        c.spin(clash.t_boom + 0.04, pan_up_done - 0.25, turns, "out")
        c.pose(pan_up_done - 0.25, "fly", 0.2, "inout")
    mochi.katana(clash.t_boom + 0.3, False)

    t0 = pan_up_done - 0.2
    mochi.face(t0, 1)
    sesame.face(t0, -1)
    t_break = _binary_star(t0)
    t_kick = _moon_toss(t_break)
    t_release = _hammer_throw(t_kick)
    pan_down = t_release + 0.05
    landed = pan_down + 0.85
    camera.pan(pan_down, landed, 0)
    aura(sesame, 13.9, pan_down, "thunder", "flash", fade=0.9, size=1.0, peak=1.0)    # aura from act 5
    _burn_back_down(t_release, pan_down, landed)
    return SpaceTimes(pan_up, pan_down, landed)


def _explosion(clash):
    flash(clash.t_boom, 0.12, 0.85)
    ring(clash.x, clash.y, clash.t_boom, 140, col="thunder", w=3, dur=0.45)
    ring(clash.x, clash.y, clash.t_boom + 0.04, 220, col="blue", w=1.5, dur=0.6)
    spark(clash.x, clash.y, clash.t_boom, 18)
    jolt(clash.t_boom, 7)


# ---------------------------------------------------------------- 1. binary star
def _binary_star(t0):
    """They lock paws and spin, trading a blow every half turn. Returns when Mochi is thrown."""
    cx, cy, r, ry = 420.0, 150.0, 24.0, 12.0
    t_lock = t0 + 0.22
    for c, side in ((mochi, -1), (sesame, 1)):
        c.pose(t0 + 0.12, "windup", 0.12, "inout")
        c.arc(t0, t_lock, cx + side * r, cy, bend=14, ease="in")
        trail(c, t0 + 0.08, t_lock - 0.02, "ghost_w" if c is mochi else "ghost_b", 3)
        c.pose(t_lock, "push", 0.04, "snap")
    hit(t_lock, cx, cy - 20, 9, mochi, sesame, dur=0.06, shake=3)
    ring(cx, cy - 20, t_lock, 50, col="flash", w=1.5, dur=0.3, squash=0.35)

    t, a, face = t_lock + 0.06, math.pi, 1          # a: Mochi's angle
    blows = ((mochi, sesame, "tuck", "fkick", 0.28), (sesame, mochi, "windup", "punch", 0.24),
             (sesame, mochi, "windup2", "mega", 0.2))
    for k, (att, dfd, wind, move, dur) in enumerate(blows):
        last = k == len(blows) - 1
        att.strike(t + dur, move, windup=wind, lead=dur * 0.75, recover=None)
        dfd.pose(t + dur * 0.5, "guard", dur * 0.4, "inout")
        n = 10
        for i in range(1, n + 1):
            aa, tt = a + math.pi * i / n, t + dur * i / n
            mochi.pos.add(tt, (cx + r * math.cos(aa), cy + ry * math.sin(aa)))
            sesame.pos.add(tt, (cx - r * math.cos(aa), cy - ry * math.sin(aa)))
            f = 1 if math.cos(aa) < 0 else -1          # face each other
            if f != face:
                mochi.face(tt, f)
                sesame.face(tt, -f)
                face = f
        trail(mochi, t + 0.04, t + dur - 0.02, "ghost_w", 2)
        trail(sesame, t + 0.04, t + dur - 0.02, "ghost_b", 2)
        a += math.pi
        t += dur
        dfd.pose(t + 0.03, "hit", 0.03)
        t = hit(t, cx, cy - 20, 14 if last else 9, att, dfd, big=last, dur=None if last else 0.06, shake=7 if last else 3)
        if not last:
            dfd.pose(t + 0.08, "guard", 0.08)

    # Mochi flies off, Sesame drifts back
    ring(cx, cy - 20, t, 90, col="thunder", w=2.5, dur=0.4)
    mochi.pose(t + 0.02, "hit", 0.03)
    mochi.arc(t, t + 0.45, 650, 176, bend=-24, ease="out")
    mochi.spin(t, t + 0.45, 360, "out")
    trail(mochi, t + 0.02, t + 0.3, "ghost_w", 4)
    mochi.pose(t + 0.45, "fly", 0.2, "inout")
    sesame.arc(t, t + 0.45, 236, 128, bend=14, ease="out")
    sesame.pose(t + 0.35, "fly", 0.2, "inout")
    return t


# ---------------------------------------------------------------- 2 and 3. moon and ambush
def _moon_toss(t_break):
    """Sesame throws the moon, Mochi cuts it, Sesame kicks from behind it. Returns the kick."""
    mx0, my0, _ = MOON
    t_web = t_break + 0.38
    sesame.face(t_web - 0.1, 1)
    sesame.pose(t_web, "point", 0.08, "snap")
    t_yank = t_web + 0.14
    sesame.strike(t_yank, "tug2", windup="point", lead=0.08, recover=None)
    sesame.stay(t_yank)
    sx, sy = sesame.world(t_yank, "N")

    # pull the moon in
    R = 62.0
    a0 = math.atan2(my0 - sy, mx0 - sx)
    t_in = t_yank + 0.18
    _MOON_MOVE.hold(t_yank)
    _MOON_MOVE.add(t_yank + 0.05, (-4.0, 3.0), "out")
    _MOON_MOVE.add(t_in, (sx + R * math.cos(a0) - mx0, sy + R * math.sin(a0) - my0), "in")
    ring(mx0, my0, t_yank + 0.03, 36, col="flash", w=1.2, dur=0.3)

    # swing it around, let go at the top
    a_end = -math.pi / 2
    while a_end < a0 + 1.5 * math.pi:
        a_end += 2 * math.pi
    t_hurl = t_in + 0.42
    for i in range(1, 17):
        s = (i / 16) ** 1.5
        a = a0 + (a_end - a0) * s
        _MOON_MOVE.add(t_in + 0.42 * i / 16, (sx + R * math.cos(a) - mx0, sy + R * math.sin(a) - my0))
    sesame.pose(t_in, "point", 0.1, "inout")
    sesame.spin(t_in, t_hurl, 360, "in")
    strand(paw(sesame), moon_centre, t_web, t_hurl, "web", 1.0, shoot=0.08)
    sesame.strike(t_hurl, "push", windup="point", lead=0.06, recover=None)

    # Mochi draws her sword
    mochi.drift(t_break + 0.45, t_hurl - 0.1, amp=2, period=0.7, sway=2)
    mochi.face(t_break + 0.38, -1)
    mochi.katana(t_hurl - 0.42, True)
    mochi.pose(t_hurl - 0.3, "sw_draw", 0.12)
    mochi.pose(t_hurl - 0.02, "sw_low", 0.24, "inout")
    spark(*mochi.world(t_hurl - 0.3, "RH"), t_hurl - 0.3, 3, kind="white", dur=0.2)

    # the moon flies at the blade
    t_cut = t_hurl + 0.26
    mochi.strike(t_cut, "sw_upcut", windup="sw_low", lead=0.1, recover=None)
    mochi.pose(t_cut + 0.1, "sw_upthru", 0.1, "out")
    (tx, ty), (hx, hy) = mochi.world(t_cut, "WT"), mochi.world(t_cut, "RH")
    px, py = (tx + hx) / 2, (ty + hy) / 2
    qx, qy = moon_centre(t_hurl)
    _MOON_MOVE.add(t_cut, (px - mx0, py - my0))
    _MOON_SPIN.hold(t_yank)
    _MOON_SPIN.add(t_cut, -900.0, "in")

    # Sesame hides behind the moon
    sesame.stay(t_hurl)
    t = t_hurl + 0.08
    sesame.pose(t, "tuck", 0.06)
    sesame.pos.add(t, (moon_centre(t)[0], moon_centre(t)[1] + 15), "in")
    while t < t_cut - 1e-6:
        t = min(t_cut, t + 0.03)
        cx, cy = moon_centre(t)
        sesame.pos.add(t, (cx, cy + 15))

    # cut the moon in half
    cut_deg = math.degrees(math.atan2(ty - hy, tx - hx))
    vx, vy = px - qx, py - qy
    vlen = math.hypot(vx, vy)
    vx, vy = vx / vlen, vy / vlen
    nx, ny = -math.sin(math.radians(cut_deg)), math.cos(math.radians(cut_deg))
    for i, side in enumerate((1, -1)):
        m, rt = _HALF_MOVE[i], _HALF_TURN[i]
        m.hold(t_cut)
        m.add(t_cut + 1.1, (vx * 110 + side * nx * 46, vy * 110 + side * ny * 46), "out")
        rt.hold(t_cut)
        rt.add(t_cut + 1.1, side * 80.0, "out")
    _MOON_FADE.hold(t_cut + 0.7)
    _MOON_FADE.add(t_cut + 1.1, 0, "in")
    smear_line(tx - (hx - tx) * 0.8, ty - (hy - ty) * 0.8, hx + (hx - tx) * 0.6, hy + (hy - ty) * 0.6, t_cut, width=3, dur=0.14, colour="flash")
    spark(px, py, t_cut, 4, kind="white", dur=0.3)
    jolt(t_cut, 3)
    mochi.hitstop(t_cut + 0.01, 0.05)
    layer("front", lambda p: _moon_svg(p, t_cut, cut_deg, sample(_MOON_SPIN, t_cut)))

    # Sesame kicks
    t_kick = t_cut + 0.17
    sesame.face(t_cut, 1)
    sesame.arc(t_cut, t_kick, sample(sesame.pos, t_cut)[0] + 6, sample(sesame.pos, t_cut)[1] - 2, bend=-4, ease="out")
    sesame.strike(t_kick, "fkick", windup="tuck", lead=0.12, recover=None)
    kx, ky = sesame.world(t_kick, "RF")
    mochi.pose(t_kick + 0.02, "hit", 0.03)
    hit(t_kick, kx, ky, 14, sesame, mochi, big=True, shake=8)
    mochi.katana(t_kick + 0.03, False)
    spark(*mochi.world(t_kick + 0.03, "RH"), t_kick + 0.13, 8, kind="white")
    return t_kick


def _moon_svg(p, t_cut, cut_deg, spin_at_cut):
    """The moon as two halves that move together until the cut. It moves with the camera."""
    mx0, my0, r = MOON
    local = math.radians(cut_deg - spin_at_cut)          # cut angle inside the spinning moon
    dx, dy = math.cos(local) * 2 * r, math.sin(local) * 2 * r
    nx, ny = -dy, dx
    halves = [[(dx, dy), (dx + nx, dy + ny), (-dx + nx, -dy + ny), (-dx, -dy)],
              [(dx, dy), (dx - nx, dy - ny), (-dx - nx, -dy - ny), (-dx, -dy)]]
    clips = "".join(f'<clipPath id="moonhalf{i}"><polygon points="{points_str(pts)}"/></clipPath>' for i, pts in enumerate(halves))

    def spin_fmt(a):
        return f"{num(a)} 0 0"

    parts = []
    for i in range(2):
        parts.append(transform_group("translate", _HALF_MOVE[i], fmt_xy) + transform_group("rotate", _HALF_TURN[i], spin_fmt)
                     + transform_group("rotate", _MOON_SPIN, spin_fmt) + f'<g clip-path="url(#moonhalf{i})">' + moon_body(p) + "</g></g></g></g>")
    # glow along the cut
    glow = Track(0)
    glow.set(t_cut, 1)
    glow.add(t_cut + 0.35, 0, "in")
    a = math.radians(cut_deg)
    edge = (fade_group(glow) + f'<path d="M{num(-math.cos(a) * r)},{num(-math.sin(a) * r)} L{num(math.cos(a) * r)},{num(math.sin(a) * r)}" '
            f'stroke="{p["flash"]}" stroke-width="2" stroke-linecap="round"/></g>')
    return (f"<defs>{moon_defs(p)}{clips}</defs>" + transform_group("translate", PAN, fmt_xy)
            + f'<g transform="translate({fnum(mx0)},{fnum(my0 - SKY_HEIGHT)})">' + transform_group("translate", _MOON_MOVE, fmt_xy)
            + fade_group(_MOON_FADE) + "".join(parts) + edge + "</g></g></g></g>")


# ---------------------------------------------------------------- 4. the hammer throw
def _hammer_throw(t_kick):
    """Sesame swings Mochi on a web and lets go. Returns the release time."""
    t1 = t_kick + 0.12
    mochi.arc(t1, t1 + 0.32, 712, 120, bend=14, ease="out")
    mochi.rot_to(t1, t1 + 0.32, 40, "out")
    sesame.pose(t1 + 0.12, "guard", 0.12, "inout")

    t_web = t1 + 0.1
    sesame.face(t_web - 0.06, 1)
    sesame.pose(t_web, "point", 0.06, "snap")
    t_pull = t_web + 0.1
    sesame.strike(t_pull, "tug2", windup="point", lead=0.08, recover=None)
    sesame.stay(t_pull)
    cx, cy = sesame.world(t_pull, "N")

    # swing her around, faster each turn
    R = 50.0
    mx, my = sample(mochi.pos, t_pull)
    b0 = math.atan2(my - 17 - cy, mx - cx)
    b_end = math.pi / 4                                   # let go toward the bottom left
    while b_end < b0 + 2.2 * math.pi:
        b_end += 2 * math.pi
    t_release = t_pull + 0.5
    mochi.stay(t_pull)
    mochi.pose(t_pull + 0.04, "fall", 0.06)
    for i in range(1, 21):
        s = (i / 20) ** 1.6
        b = b0 + (b_end - b0) * s
        mochi.pos.add(t_pull + 0.5 * i / 20, (cx + R * math.cos(b), cy + R * math.sin(b) + 17))
    turn = math.degrees(b_end - b0)
    mochi.rot_to(t_pull, t_release, sample(mochi.rot, t_pull)[0] + turn + 90, "in")
    sesame.pose(t_pull + 0.1, "point", 0.1, "inout")
    sesame.spin(t_pull + 0.04, t_release, turn, "in")
    sesame.rot_to(t_release + 0.05, t_release + 0.3, 0, "inout")
    strand(paw(sesame), paw(mochi, "N"), t_web, t_release, "web", 1.0, shoot=0.07)
    trail(mochi, t_pull + 0.3, t_release, "ghost_w", 4)
    ring(*mochi.world(t_release, "N"), t_release, 30, col="flash", w=1.2, dur=0.25)
    jolt(t_release, 3)
    return t_release


def _burn_back_down(t_release, pan_down, landed):
    """Both fall back to the page. Mochi is on fire."""
    mochi.pose(t_release + 0.04, "hit", 0.04)
    mochi.stay(t_release)
    mochi.at(landed + 0.08, 360, FLOOR)
    a, px, py = mochi.rot.end_value
    mochi.rot_to(t_release, landed, round(a / 360) * 360 - 1080, "lin")
    mochi.rot.add(landed + EPS, (0.0, px, py))
    aura(mochi, t_release + 0.1, landed - 0.1, "red", "thunder", fade=0.2, size=0.9)
    trail(mochi, t_release + 0.04, pan_down + 0.3, "ghost_w", 4)
    mochi.land(landed + 0.08, 0.35)
    mochi.pose(landed + 0.14, "lying", 0.06)
    dust(360, FLOOR, landed + 0.08, big=True)
    floor_crack(360, landed + 0.08)
    sesame.pose(pan_down, "fall", 0.15, "inout")
    sesame.stay(pan_down)
    sesame.arc(pan_down, landed, 620, FLOOR, bend=-20, ease="in")
    sesame.land(landed, 0.32)
    dust(620, FLOOR, landed, big=True)
    floor_crack(620, landed)
    jolt(landed + 0.08, 5)
