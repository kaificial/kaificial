"""Dust, smoke and steam, plus the cracks a hard landing leaves in the floor."""
import math

from ..config import FLOOR
from ..layers import layer
from ..svg import num, rnd, animate, animate_transform, fmt_xy, fmt_uniform_scale, fade_group, transform_group
from ..timeline import Track


def dust(x, y, t, big=False):
    """A little puff of dust kicked up from the floor."""
    def svg(p):
        out = []
        if big:
            pts = [(-18, -6), (-10, -13), (-2, -16), (6, -15), (14, -11), (20, -5)]
        else:
            pts = [(-12, -5), (-5, -10), (5, -10), (12, -5)]
        for i, (dx, dy) in enumerate(pts):
            tr = Track((0.0, 0.0))
            tr.set(t, (0.0, 0.0))
            tr.add(t + 0.32, (dx * 1.3, dy * 1.2), "out")
            op = Track(0)
            op.set(t, 0.75)
            op.add(t + 0.32, 0, "in")
            r = 1.8 + 0.6 * rnd(i + t)
            out.append(f'<g transform="translate({num(x)},{num(y)})"><circle r="{num(r)}" fill="{p["smoke"]}" opacity="0">'
                       + animate("opacity", op, str) + animate_transform("translate", tr, fmt_xy) + "</circle></g>")
        return "".join(out)
    layer("page", svg)


def poof(x, y, t, size=1.0):
    """A round burst of smoke."""
    def svg(p):
        out = []
        for i in range(7):
            a = i * 2 * math.pi / 7 + rnd(i + t) * 0.5
            d = (9 + 7 * rnd(i * 3 + t)) * size
            tr = Track((0.0, 0.0))
            tr.set(t, (0.0, 0.0))
            tr.add(t + 0.36, (d * math.cos(a), d * math.sin(a) * 0.7 - 4), "out")
            op = Track(0)
            op.set(t, 0.9)
            op.hold(t + 0.12)
            op.add(t + 0.36, 0, "in")
            sc = Track(0.4)
            sc.hold(t)
            sc.add(t + 0.15, 1.0, "out")
            sc.add(t + 0.36, 1.3)
            r = (4 + 2.5 * rnd(i * 5 + t)) * size
            out.append(f'<g transform="translate({num(x)},{num(y)})"><g opacity="0">' + animate("opacity", op, str)
                       + animate_transform("translate", tr, fmt_xy) + "<g>" + animate_transform("scale", sc, fmt_uniform_scale)
                       + f'<circle r="{num(r)}" fill="{p["smoke"]}"/></g></g></g>')
        return "".join(out)
    layer("behind", svg)


def steam(where, t0, t1, every=0.16, size=1.6, spread=30):
    """Steam puffs rising from where(t), one every `every` seconds."""
    def svg(p):
        out, t, i = [], t0, 0
        while t < t1:
            x, y = where(t)
            x += (rnd(i * 7 + 1) - 0.5) * spread
            tr, op, sc = Track((0.0, 0.0)), Track(0), Track(0.5)
            op.set(t, 0.55)
            op.hold(t + 0.25)
            op.add(t + 0.8, 0, "in")
            tr.hold(t)
            tr.add(t + 0.8, ((rnd(i + 3) - 0.5) * 16, -30 - 20 * rnd(i)), "out")
            sc.hold(t)
            sc.add(t + 0.8, 1.4, "out")
            r = (5 + 4 * rnd(i * 5)) * size
            out.append(f'<g transform="translate({num(x)},{num(y)})">' + fade_group(op) + transform_group("translate", tr, fmt_xy) + transform_group("scale", sc, fmt_uniform_scale)
                       + f'<circle r="{num(r)}" fill="{p["smoke"]}" opacity="0.6"/><circle cx="{num(r * 0.6)}" cy="{num(-r * 0.3)}" r="{num(r * 0.7)}" fill="{p["smoke"]}" opacity="0.45"/></g></g></g></g>')
            t += every
            i += 1
        return "".join(out)
    layer("front", svg)


def floor_crack(x, t, life=2.0):
    """Cracks in the floor under a hard landing. They fade after `life` seconds."""
    def svg(p):
        op = Track(0)
        op.set(t, 1)
        op.hold(t + life - 0.4)
        op.add(t + life, 0, "in")
        out = [fade_group(op)]
        for dx, dy in ((-18, -3), (-10, -6), (-3, -1), (5, -5), (13, -2), (19, -4)):
            out.append(f'<path d="M{num(x)},{FLOOR} L{num(x + dx * 0.5)},{num(FLOOR + dy * 0.4 - 1)} L{num(x + dx)},{num(FLOOR + dy * 0.2)}" fill="none" stroke="{p["crack"]}" stroke-width="1" stroke-linecap="round"/>')
        return "".join(out) + "</g>"
    layer("page", svg)
