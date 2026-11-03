"""Act 7 (18.2 - 23.5 s): the explosion throws them into space.

The camera follows them up: the page slides down out of frame and the night sky comes in.
Sesame blinks in behind Mochi and punches her into the side of a mountain, follows her down
and pounds her deeper into the crater. Then a quiet beat: black bars slide in and she lifts
the limp white cat out of the rubble by the scruff and holds her up. She lets go, and the
camera pans back down as they both fall back onto the page.
"""
import math
from dataclasses import dataclass

from engine import camera
from engine.camera import jolt
from engine.config import EPS, FLOOR, W, H
from engine.effects import aura, dust, flash, floor_crack, poof, ring, smear_line, spark, trail
from engine.layers import layer
from engine.moves import carry, hit
from engine.svg import num, rnd, animate_transform, fmt_xy, fmt_uniform_scale, fade_group, transform_group, path_d
from engine.timeline import Track

from .cast import mochi, sesame
from .scenery import MOUNTAIN_HIT, SKY_HEIGHT, main_mountain

# Sesame's combo while she pounds Mochi into the mountain
_COMBO = ("punch", "push", "punch", "fkick", "punch", "push", "punch")


@dataclass
class SpaceTimes:
    pan_up: float       # the camera starts panning up
    pan_down: float     # the camera starts panning back down
    landed: float       # they're both back on the page


def play(clash):
    _explosion(clash)
    pan_up, pan_up_done = clash.t_boom + 0.1, clash.t_boom + 1.0
    camera.pan(pan_up, pan_up_done, SKY_HEIGHT)
    for c, (x, y), turns in ((mochi, (250.0, 176.0), -720), (sesame, (610.0, 128.0), 720)):
        c.pose(clash.t_boom + 0.02, "tuck", 0.03)
        c.stay(clash.t_boom + 0.02)
        c.at(pan_up_done - 0.05, x, y, "out")
        c.spin(clash.t_boom + 0.04, pan_up_done - 0.1, turns, "out")
        c.pose(pan_up_done - 0.1, "fly", 0.15, "inout")
    mochi.katana(clash.t_boom + 0.3, False)

    t_crash = _punch_into_mountain(pan_up_done + 0.12)
    hits = _pound(t_crash)
    t_hold = hits[-1] + 0.32
    t_drop = t_hold + 1.0
    pan_down = t_drop + 0.3
    landed = pan_down + 0.8

    layer("behind", lambda p: _crater(p, t_crash, hits, pan_down))
    layer("front", lambda p: _flying_rocks(p, [t_crash, hits[-1]]))
    _hold_up(t_hold, t_drop)
    layer("overlay", lambda p: _letterbox(t_hold, t_drop))
    camera.pan(pan_down, landed, 0)
    aura(sesame, 13.9, t_drop, "thunder", "flash", fade=0.9, size=1.0, peak=1.0)    # her power-up aura, lit since act 5
    _fall_back_down(t_drop, pan_down, landed)
    return SpaceTimes(pan_up, pan_down, landed)


def _explosion(clash):
    flash(clash.t_boom, 0.12, 0.85)
    ring(clash.x, clash.y, clash.t_boom, 140, col="thunder", w=3, dur=0.45)
    ring(clash.x, clash.y, clash.t_boom + 0.04, 220, col="blue", w=1.5, dur=0.6)
    spark(clash.x, clash.y, clash.t_boom, 18)
    jolt(clash.t_boom, 7)


def _punch_into_mountain(t0):
    """Her aura flares, she blinks in behind Mochi and punches her into the mountainside.
    Returns the moment Mochi hits the mountain."""
    ring(*sesame.world(t0, "N"), t0, 40, col="thunder", w=2.4, dur=0.3)
    jolt(t0, 2)
    sesame.pose(t0, "crouch", 0.05)
    sesame.stay(t0 + 0.04)
    trail(sesame, t0 + 0.04, t0 + 0.2, "ghost_b", 3)
    sesame.at(t0 + 0.2, 224, 172, "in")
    sesame.face(t0 + 0.12, 1)
    mochi.pose(t0 + 0.1, "guard", 0.06)

    t_punch = t0 + 0.24
    sesame.pose(t_punch, "mega", 0.04, "snap")
    hit(t_punch, 240, 150, 12, sesame, mochi, big=True, dur=0.08, shake=6)
    ring(240, 150, t_punch, 60, col="thunder", w=2.5, dur=0.3)

    t_crash = t_punch + 0.3
    hx, hy = MOUNTAIN_HIT
    mochi.pose(t_punch + 0.08, "hit", 0.03)
    mochi.stay(t_punch + 0.08)
    mochi.at(t_crash, hx - 6, hy + 8, "in")
    mochi.spin(t_punch + 0.08, t_crash, 720, "in")
    smear_line(250, 160, hx - 14, hy - 10, t_punch + 0.12, width=5, dur=0.18, colour="flash")
    trail(mochi, t_punch + 0.1, t_crash - 0.02, "ghost_w", 3)

    flash(t_crash, 0.1, 0.75)
    jolt(t_crash, 8)
    spark(hx, hy - 10, t_crash, 18)
    ring(hx, hy - 6, t_crash, 70, col="flash", w=2.5, dur=0.4)
    poof(hx, hy - 10, t_crash + 0.02, 2.6)
    mochi.put(t_crash + 0.01, hx - 4, hy + 8)
    mochi.pose(t_crash + 0.015, "lying", EPS)
    return t_crash


def _pound(t_crash):
    """She follows her down and pounds her deeper into the crater, then lands one last heavy punch.
    Returns the time of every hit."""
    hx, hy = MOUNTAIN_HIT
    sesame.pose(t_crash - 0.1, "fly", 0.06)
    sesame.stay(t_crash - 0.1)
    sesame.at(t_crash + 0.18, hx - 30, hy - 4, "in")
    sesame.face(t_crash, 1)
    hits = []
    t = t_crash + 0.26
    for k, move in enumerate(_COMBO):
        sesame.pose(t, move, 0.035, "snap")
        sesame.pose(t + 0.06, "guard", 0.04)
        spark(hx + (rnd(k + 40) - 0.5) * 12, hy - 8 + (rnd(k + 41) - 0.5) * 8, t + 0.01, 7)
        jolt(t, 2.4)
        mochi.jitter(t, t + 0.06, 1.2)
        hits.append(t)
        t += 0.11
    t_final = t + 0.12
    sesame.pose(t_final - 0.14, "windup2", 0.1)
    sesame.pose(t_final, "mega", 0.03, "snap")
    hit(t_final, hx - 4, hy - 6, 14, sesame, mochi, big=True, dur=0.1, shake=7)
    ring(hx, hy - 6, t_final, 80, col="thunder", w=2.5, dur=0.35)
    poof(hx, hy - 8, t_final + 0.02, 2.0)
    hits.append(t_final)
    return hits


def _hold_up(t_hold, t_drop):
    """The quiet beat: she lifts the limp white cat out of the rubble and holds her up at eye level."""
    sesame.pose(t_hold + 0.05, "punch", 0.08)
    sesame.stay(t_hold + 0.1)
    sesame.at(t_hold + 0.55, 604.0, 150.0, "inout")
    sesame.wobble(t_hold + 0.6, t_hold + 0.95, 3, 0.35)
    carry(mochi, sesame, "RH", t_hold + 0.12, t_drop, 3)
    mochi.pose(t_hold + 0.2, "stand", 0.12)
    mochi.rot_to(t_hold + 0.2, t_hold + 0.4, 14, "inout")       # head tilted, out cold
    mochi.rot_to(t_drop - 0.12, t_drop, 0, "inout")
    for k in range(3):                                           # dizzy sparkles around her head
        t = t_hold + 0.6 + 0.16 * k
        hx, hy = mochi.world(t, "H")
        spark(hx + 8 * math.cos(k * 2.1), hy - 10 + 4 * math.sin(k * 2.1), t, 3, kind="white", dur=0.25)


def _fall_back_down(t_drop, pan_down, landed):
    """She lets go. Mochi tumbles back down to the page; Sesame comes down in control."""
    mochi.pose(t_drop + 0.02, "hit", 0.03)
    mochi.stay(t_drop + 0.02)
    mochi.at(landed + 0.08, 360, FLOOR, "in")
    mochi.spin(t_drop + 0.05, landed, 720, "in")
    mochi.land(landed + 0.08, 0.35)
    mochi.pose(landed + 0.14, "lying", 0.06)
    dust(360, FLOOR, landed + 0.08, big=True)
    floor_crack(360, landed + 0.08)
    sesame.pose(pan_down, "fall", 0.12)
    sesame.stay(pan_down)
    sesame.at(landed, 620, FLOOR, "in")
    sesame.land(landed, 0.32)
    dust(620, FLOOR, landed, big=True)
    floor_crack(620, landed)
    jolt(landed + 0.08, 5)


# ---------------------------------------------------------------- drawings
def _crack_tree(cx, cy, a, length, seed, depth=2):
    """A jagged crack that forks. Returns a list of path strings."""
    pts, x, y = [(cx, cy)], cx, cy
    for j in range(4):
        a += (rnd(seed * 7 + j) - 0.5) * 0.6
        x += math.cos(a) * length / 4
        y += math.sin(a) * length / 4 * 0.75
        pts.append((x, y))
    out = [path_d(pts)]
    if depth:
        bx, by = pts[2]
        out += _crack_tree(bx, by, a + (0.7 if seed % 2 else -0.7), length * 0.5, seed + 13, depth - 1)
    return out


def _crater(p, t_crash, hits, t_gone):
    """A deep crater in the mountainside: a dark pit, a jagged lit rim, rubble, and cracks that
    spread a little further with every hit."""
    cx, cy = MOUNTAIN_HIT[0], MOUNTAIN_HIT[1] - 6
    op = Track(0)
    op.set(t_crash, 1)
    op.hold(t_gone)
    op.add(t_gone + 0.15, 0, "in")
    sc = Track(0.6)
    sc.hold(t_crash)
    sc.add(t_crash + 0.08, 1.0, "out")
    for k, t in enumerate(hits):
        sc.hold(t)
        sc.add(t + 0.05, 1.0 + 0.035 * (k + 1), "out")
    rim = []
    for i in range(22):
        a = i * 2 * math.pi / 22
        r = 1.0 + 0.22 * (rnd(i + 70) - 0.5)
        rim.append((26 * r * math.cos(a), 17 * r * math.sin(a)))
    rim_d = path_d(rim) + " Z"
    inner = " ".join(f"{num(x * 0.62)},{num(y * 0.62 + 2)}" for x, y in rim)
    pit = (f'<defs><radialGradient id="cratg" cx="0.5" cy="0.6" r="0.6"><stop offset="0" stop-color="#000000"/>'
           f'<stop offset="0.65" stop-color="#07080f"/><stop offset="1" stop-color="{p["mtn_shadow"]}"/></radialGradient></defs>'
           f'<path d="{rim_d}" fill="url(#cratg)" stroke="{p["mtn_hi"]}" stroke-width="1.4" stroke-linejoin="round"/>'
           f'<polygon points="{inner}" fill="#000000" opacity="0.55"/>'
           + "".join(f'<path d="M{num(x)},{num(y)} L{num(x * 1.12)},{num(y * 1.12 - 2)}" stroke="{p["snow"]}" stroke-width="1" opacity="0.55"/>'
                     for i, (x, y) in enumerate(rim) if y < 0 and i % 2 == 0))
    rubble = "".join(f'<polygon points="{" ".join(f"{num(x * 1.25 + r * math.cos(j * 2.1))},{num(y * 1.25 + r * math.sin(j * 2.1))}" for j in range(3))}" '
                     f'fill="{p["mtn_lit"]}" stroke="{p["mtn_hi"]}" stroke-width="0.5"/>'
                     for i, (x, y) in enumerate(rim) if i % 3 == 0 for r in (2.2 + 1.8 * rnd(i + 90),))
    base_cracks = "".join(f'<path d="{d}" fill="none" stroke="{p["mtn_hi"]}" stroke-width="1" stroke-linecap="round"/>'
                          for i in range(8) for d in _crack_tree(0, 0, i * 2 * math.pi / 8 + 0.2, 34, i + 5))
    new_cracks = ""
    for k, t in enumerate(hits):
        shown = Track(0)
        shown.set(t, 1)
        d = " ".join(_crack_tree(0, 0, rnd(k + 120) * 2 * math.pi, 40 + 4 * k, k * 3 + 50))
        new_cracks += fade_group(shown) + f'<path d="{d}" fill="none" stroke="{p["mtn_hi"]}" stroke-width="1.1" stroke-linecap="round"/></g>'
    dust_op = Track(0)
    dust_op.set(t_crash, 0.5)
    dust_op.add(t_crash + 1.2, 0, "out")
    haze = fade_group(dust_op) + f'<ellipse cx="0" cy="-6" rx="46" ry="22" fill="{p["smoke"]}" opacity="0.5"/></g>'
    clip_pts = " ".join(f"{num(x)},{num(y + SKY_HEIGHT)}" for x, y in main_mountain())
    clip = f'<clipPath id="mtnclip"><polygon points="{clip_pts}"/></clipPath>'
    return (f'<defs>{clip}</defs><g clip-path="url(#mtnclip)"><g transform="translate({num(cx)},{num(cy)})">' + fade_group(op)
            + "<g>" + animate_transform("scale", sc, fmt_uniform_scale)
            + base_cracks + new_cracks + pit + rubble + "</g>" + haze + "</g></g></g>")


def _flying_rocks(p, bursts):
    """Chunks of rock thrown out of the crater on the first and the last hit."""
    out = []
    for burst_i, tb in enumerate(bursts):
        for i in range(14):
            k = i + 31 * burst_i
            a = -math.pi * (0.05 + 0.9 * rnd(k + 300))
            v = 60 + 80 * rnd(k + 310)
            tr, op, rt = Track((0.0, 0.0)), Track(0), Track(0.0)
            op.set(tb, 1)
            op.hold(tb + 0.45)
            op.add(tb + 0.7, 0, "in")
            tr.hold(tb)
            for q in range(1, 8):
                s = 0.7 * q / 7
                tr.add(tb + s, (v * math.cos(a) * s * (1 if i % 2 else -1), v * math.sin(a) * s + 260 * s * s))
            rt.hold(tb)
            rt.add(tb + 0.7, (rnd(k) - 0.5) * 500)
            r = 1.8 + 3.2 * rnd(k + 320)
            pts = " ".join(f"{num(r * math.cos(j * 1.6 + rnd(k + j)))},{num(r * math.sin(j * 1.6 + rnd(k + j)))}" for j in range(4))
            out.append(f'<g transform="translate({num(MOUNTAIN_HIT[0])},{num(MOUNTAIN_HIT[1] - 8)})">' + fade_group(op) + transform_group("translate", tr, fmt_xy)
                       + transform_group("rotate", rt, lambda angle: f"{num(angle)} 0 0") + f'<polygon points="{pts}" fill="{p["mtn_lit"]}" stroke="{p["mtn_hi"]}" stroke-width="0.5"/></g></g></g></g>')
    return "".join(out)


def _letterbox(t_in, t_out):
    """Black bars slide in from the top and bottom for the quiet beat, then slide away."""
    amount = Track(0.0)
    amount.hold(t_in)
    amount.add(t_in + 0.25, 1.0, "out")
    amount.hold(t_out - 0.1)
    amount.add(t_out + 0.15, 0.0, "in")
    top = Track((0.0, -28.0))
    bottom = Track((0.0, 28.0))
    for t, v, ease in amount.keys[1:]:
        top.add(t, (0.0, -28.0 * (1 - v)), ease)
        bottom.add(t, (0.0, 28.0 * (1 - v)), ease)
    return (transform_group("translate", top, fmt_xy) + f'<rect x="-30" y="-30" width="{W + 60}" height="56" fill="#000000"/></g>'
            + transform_group("translate", bottom, fmt_xy) + f'<rect x="-30" y="{H - 26}" width="{W + 60}" height="56" fill="#000000"/></g>')
