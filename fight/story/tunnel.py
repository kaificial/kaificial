"""The 3x3 block of the page under "forward!" that Mochi mines through from behind.

Each block cracks through a few stages, breaks open, and later clicks back into place. The
blocks open twice: once at the start, and again at the end when Mochi digs back in for the loop.
"""
import math

from engine.camera import jolt
from engine.effects import spark
from engine.layers import layer
from engine.svg import num, fnum, rnd, animate, fmt_xy, fade_group, transform_group, path_d
from engine.timeline import Track

CELL = 16
LEFT, TOP = 146, 166                  # top-left corner of the 3x3 block
FLOOR_Y = TOP + 3 * CELL              # the tunnel floor, where Mochi stands while digging
DIG_BACK_IN = 29.2                    # when the blocks open again at the end of the loop

# the order the blocks break in: the middle one first, then outward
_BREAK_ORDER = [(1, 1), (2, 1), (1, 0), (1, 2), (0, 1), (2, 0), (2, 2), (0, 0), (0, 2)]


def _make_blocks():
    blocks = []
    for i, (row, col) in enumerate(_BREAK_ORDER):
        if i == 0:
            stages, t_break = [0.8, 0.95, 1.1, 1.25], 1.38
        else:
            t0 = 1.32 + 0.11 * i
            stages, t_break = [t0, t0 + 0.025, t0 + 0.05, t0 + 0.075], t0 + 0.09
        blocks.append(dict(x=LEFT + col * CELL, y=TOP + row * CELL, stages=stages, seed=i * 7 + 3,
                           open=[(t_break, 3.42 + 0.035 * (8 - i)), (DIG_BACK_IN, DIG_BACK_IN + 0.75 + 0.035 * (8 - i))]))
        for t in stages:
            jolt(t, 0.6 if i == 0 else 0.25)
        jolt(t_break, 1.0 if i == 0 else 0.4)
    return blocks


def _crack_branches(seed):
    """Four wiggly crack lines growing out from near the middle of a block."""
    out = []
    for b in range(4):
        x, y = 8 + (rnd(seed + b) - 0.5) * 4, 8 + (rnd(seed + b + 9) - 0.5) * 4
        a = b * math.pi / 2 + rnd(seed * 3 + b) * 1.2
        pts = [(x, y)]
        for j in range(4):
            a += (rnd(seed * 5 + b * 4 + j) - 0.5) * 1.1
            x = min(15.2, max(0.8, x + 2.4 * math.cos(a)))
            y = min(15.2, max(0.8, y + 2.4 * math.sin(a)))
            pts.append((round(x * 2) / 2, round(y * 2) / 2))
        out.append(pts)
    return out


def _open_track(block, value_when_open=1.0):
    track = Track(0.0)
    for t_open, t_close in block["open"]:
        track.set(t_open, value_when_open)
        track.set(t_close, 0.0)
    return track


def _draw_blocks(p):
    out = []
    for block in BLOCKS:
        x, y = block["x"], block["y"]
        # the dark hole behind the block, with a bit of texture
        texture = "".join(f'<rect x="{2 * int(rnd(block["seed"] * 13 + j) * 7)}" y="{2 * int(rnd(block["seed"] * 17 + j) * 7)}" width="2" height="2" fill="{p["tunnel_hi"]}"/>' for j in range(7))
        out.append(f'<g transform="translate({x},{y})">' + fade_group(_open_track(block)) + f'<rect width="16" height="16" fill="{p["tunnel"]}"/>' + texture
                   + f'<rect x="0.3" y="0.3" width="15.4" height="15.4" fill="none" stroke="{p["smoke"]}" stroke-width="0.6" opacity="0.5"/></g></g>')
        # the outline and the cracks while it's being mined
        t_break = block["open"][0][0]
        outline = Track(0)
        outline.set(block["stages"][0] - 0.02, 1)
        outline.set(t_break, 0)
        out.append(f'<g transform="translate({x},{y})">' + fade_group(outline) + f'<rect x="0.3" y="0.3" width="15.4" height="15.4" fill="none" stroke="{p["fg"]}" stroke-width="0.7" opacity="0.6"/></g></g>')
        branches = _crack_branches(block["seed"])
        for k, t_stage in enumerate(block["stages"]):
            stage = Track(0)
            stage.set(t_stage, 1)
            stage.set(t_break, 0)
            d = " ".join(path_d(branch[:k + 2]) for branch in branches)
            out.append(f'<g transform="translate({x},{y})">' + fade_group(stage) + f'<path d="{d}" fill="none" stroke="{p["fg"]}" stroke-width="{num(0.8 + 0.15 * k)}" stroke-linecap="square" opacity="0.75"/></g></g>')
        # crumbs fly out every time it breaks
        for t_open, t_close in block["open"]:
            for j in range(5):
                a = -math.pi / 2 + (rnd(block["seed"] * 11 + j + t_open) - 0.5) * 2.6
                v = 30 + 30 * rnd(block["seed"] + j * 5)
                tr, op = Track((0.0, 0.0)), Track(0)
                op.set(t_open, 1)
                op.hold(t_open + 0.3)
                op.add(t_open + 0.55, 0, "in")
                tr.hold(t_open)
                for q in range(1, 7):
                    s = 0.55 * q / 6
                    tr.add(t_open + s, (v * math.cos(a) * s, v * math.sin(a) * s + 160 * s * s))
                colour = (p["fg"], p["smoke"], p["rule"])[j % 3]
                out.append(f'<g transform="translate({x + 8},{y + 8})">' + fade_group(op) + transform_group("translate", tr, fmt_xy)
                           + f'<rect x="-1.2" y="-1.2" width="2.4" height="2.4" fill="{colour}"/></g></g></g>')
    return "".join(out)


def tunnel_clip():
    """A clip path of the blocks that are open right now. Mochi, while digging, only shows through it."""
    rects = []
    for block in BLOCKS:
        width = _open_track(block, 16.0)
        rects.append(f'<rect x="{block["x"]}" y="{block["y"]}" width="0" height="16">' + animate("width", width, fnum) + "</rect>")
    return '<clipPath id="tunnel">' + "".join(rects) + "</clipPath>"


BLOCKS = []


def build():
    """Set up the blocks (this also shakes the camera on every pickaxe hit)."""
    BLOCKS.extend(_make_blocks())
    layer("tunnel", _draw_blocks)
    for block in BLOCKS:
        for _, t_close in block["open"]:
            spark(block["x"] + 8, block["y"] + 8, t_close, 4, kind="white", dur=0.2)  # the block clicks back into place
