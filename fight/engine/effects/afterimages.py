"""Afterimages: fading copies of a cat left behind by very fast movement"""
import math

from ..config import BODY_Y
from ..layers import layer
from ..poses import LIMBS, limb_points
from ..svg import num, animate, animate_transform, fmt_xy
from ..timeline import Track, sample, sample_step


def _still_figure(pose, colour, width=2.6):
    """A plain, unanimated stick cat (ears, head and limbs) in one colour."""
    hx, hy = pose["H"]
    a = math.degrees(math.atan2(pose["H"][0] - pose["N"][0], -(pose["H"][1] - pose["N"][1])))
    out = [f'<g transform="translate({num(hx)} {num(hy)}) rotate({num(a)})"><path d="M-4.6,-2.4 L-5.4,-10.2 L-0.8,-4.9 Z '
           f'M0.4,-5 L4.2,-10.4 L4.9,-2.2 Z" fill="{colour}"/></g>',
           f'<circle r="5" fill="{colour}" cx="{num(pose["H"][0])}" cy="{num(pose["H"][1])}"/>']
    for limb in LIMBS:
        out.append(f'<polyline fill="none" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" '
                   f'stroke-linejoin="round" points="{limb_points(pose, limb)}"/>')
    return "".join(out)


def ghost(pose, x, y, facing, t, colour_key, dur=0.18, drift=(0, 0), alpha=0.45, rot=0.0):
    """One faded copy of a pose at (x, y) that drifts a little and disappears."""
    def svg(p):
        op = Track(0)
        op.set(t, alpha)
        op.add(t + dur, 0, "in")
        tr = Track((0.0, 0.0))
        tr.set(t, (0.0, 0.0))
        tr.add(t + dur, drift, "out")
        return (f'<g transform="translate({num(x)},{num(y)})"><g opacity="0">' + animate("opacity", op, str)
                + animate_transform("translate", tr, fmt_xy) + f'<g transform="rotate({num(rot)} 0 {BODY_Y}) scale({facing},1)">'
                + _still_figure(pose, p[colour_key]) + "</g></g></g>")
    layer("behind", svg)


def trail(c, t0, t1, colour_key, k=4):
    """k afterimages left behind by character c as she moves between t0 and t1."""
    for i in range(k):
        t = t0 + (t1 - t0) * (i + 1) / (k + 1)
        x, y = sample(c.pos, t)
        ghost(c.pose_at(t), x, y, sample_step(c.facing, t), t, colour_key, dur=0.2, alpha=0.35, rot=sample(c.rot, t)[0])
