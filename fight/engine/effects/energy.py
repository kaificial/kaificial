"""Energy effects: lightning, power-up auras, glowing orbs and spark portals."""
import math

from ..config import EPS
from ..layers import layer
from ..svg import num, rnd, animate_transform, fmt_xy, fmt_uniform_scale, fade_group, transform_group, path_d
from ..timeline import Track, sample


def bolt(x0, y0, x1, y1, t, dur=0.16, col="thunder", core="bolt_core", w=2.2, seed=1, jag=7, k=9, branch=True):
    """A jagged lightning bolt from (x0, y0) to (x1, y1) that flickers once and fades."""
    length = math.hypot(x1 - x0, y1 - y0) or 1
    nx, ny = -(y1 - y0) / length, (x1 - x0) / length
    pts = [(x0, y0)]
    for i in range(1, k):
        s = i / k
        d = (rnd(seed * 31 + i) - 0.5) * 2 * jag
        pts.append((x0 + (x1 - x0) * s + nx * d, y0 + (y1 - y0) * s + ny * d))
    pts.append((x1, y1))
    d_main = path_d(pts)
    d_branches = ""
    if branch:
        for b in range(2):
            i = 2 + int(rnd(seed * 7 + b) * (k - 4))
            bx, by = pts[i]
            ang = math.atan2(y1 - y0, x1 - x0) + (0.7 if b else -0.7)
            fork = [(bx, by)] + [(bx + math.cos(ang) * 7 * j + (rnd(seed + b * 5 + j) - 0.5) * 5,
                                  by + math.sin(ang) * 7 * j + (rnd(seed * 3 + b + j) - 0.5) * 5) for j in range(1, 4)]
            d_branches += " " + path_d(fork)

    def svg(p):
        op = Track(0)
        op.set(t, 1)
        op.add(t + dur * 0.3, 0.35)
        op.add(t + dur * 0.45, 1)
        op.add(t + dur, 0, "in")
        c, kk = p[col], p[core]
        return (fade_group(op) + f'<path d="{d_main}{d_branches}" fill="none" stroke="{c}" stroke-width="{num(w * 2.6)}" stroke-linejoin="round" stroke-linecap="round" opacity="0.3"/>'
                + f'<path d="{d_main}{d_branches}" fill="none" stroke="{c}" stroke-width="{num(w)}" stroke-linejoin="round" stroke-linecap="round"/>'
                + f'<path d="{d_main}" fill="none" stroke="{kk}" stroke-width="{num(w * 0.4)}" stroke-linejoin="round" stroke-linecap="round"/></g>')
    layer("front", svg)


def aura(c, t0, t1, col, hi, fade=0.3, dt=0.04, size=1.0, peak=1.0):
    """A spiky flame aura that follows character c from t0 to t1."""
    def svg(p):
        pos, op = Track(sample(c.pos, t0)), Track(0)
        op.hold(t0)
        op.add(t0 + fade, peak, "out")
        op.hold(t1)
        op.add(t1 + 0.2, 0, "in")
        pos.hold(t0 - EPS)
        t = t0
        while t < t1 + 0.2 - 1e-6:
            t = min(t1 + 0.2, t + dt)
            pos.add(t, sample(c.pos, t))
        pts = []
        for i in range(28):
            a = -math.pi / 2 + i * 2 * math.pi / 28
            r = (24 if i % 2 == 0 else 15) * size
            stretch = 1.0 + 0.55 * max(0.0, -math.sin(a))      # the flames lick upward
            pts.append((r * 0.62 * math.cos(a), -16 * size + r * math.sin(a) * stretch))
        outer = " ".join(f"{num(x)},{num(y)}" for x, y in pts)
        inner = " ".join(f"{num(x * 0.7)},{num(-16 * size + (y + 16 * size) * 0.7)}" for x, y in pts)
        flicker = ('<animateTransform attributeName="transform" type="scale" values="1 1;1.07 1.1;0.97 0.95;1 1" '
                   'dur="0.16s" repeatCount="indefinite" additive="sum"/>')
        return (fade_group(c.opacity) + fade_group(op) + transform_group("translate", pos, fmt_xy) + f'<g>{flicker}<polygon points="{outer}" fill="{p[col]}" opacity="0.32"/>'
                + f'<polygon points="{inner}" fill="{p[hi]}" opacity="0.3"/></g></g></g></g>')
    layer("behind", svg)


def orb_draw(col, hi, r=5.0):
    """A glowing ball of energy with a spinning dashed ring (use it as a Prop drawing)."""
    def draw(p):
        spin = (f'<g><animateTransform attributeName="transform" type="rotate" values="0;360" dur="0.5s" repeatCount="indefinite"/>'
                f'<circle r="{num(r * 1.75)}" fill="none" stroke="{p[hi]}" stroke-width="1" stroke-dasharray="5 4"/></g>')
        return (f'<circle r="{num(r * 2.1)}" fill="{p[col]}" opacity="0.22"/><circle r="{num(r * 1.45)}" fill="{p[col]}" opacity="0.4"/>'
                f'<circle r="{num(r)}" fill="{p[col]}"/><circle cx="{num(-r * 0.3)}" cy="{num(-r * 0.3)}" r="{num(r * 0.42)}" fill="{p[hi]}"/>' + spin)
    return draw


def portal(x, y, t_open, t_close, ry=22.0):
    """A ring of orange sparks that opens on the page, like a sorcerer's portal."""
    def svg(p):
        sc = Track(0.0)
        sc.hold(t_open)
        sc.add(t_open + 0.18, 1.0, "out")
        sc.hold(t_close)
        sc.add(t_close + 0.16, 0.0, "in")
        sparks = "".join(f'<circle cx="{num(14 * math.cos(2 * math.pi * i / 16))}" cy="{num(ry * math.sin(2 * math.pi * i / 16))}" r="{num(0.9 + 0.8 * rnd(i))}" fill="#ffb347"/>' for i in range(16))
        spin = '<animateTransform attributeName="transform" type="rotate" values="0;360" dur="0.6s" repeatCount="indefinite"/>'
        return (f'<g transform="translate({num(x)},{num(y)})"><g>' + animate_transform("scale", sc, fmt_uniform_scale)
                + f'<ellipse rx="13" ry="{num(ry)}" fill="{p["tunnel"]}" opacity="0.85"/>'
                + f'<ellipse rx="14" ry="{num(ry)}" fill="none" stroke="#ff8c1a" stroke-width="2.2"/>'
                + f'<ellipse rx="15.5" ry="{num(ry + 1.5)}" fill="none" stroke="#ffd27a" stroke-width="0.8" stroke-dasharray="3 4">'
                + '<animate attributeName="stroke-dashoffset" values="0;14" dur="0.4s" repeatCount="indefinite"/></ellipse>'
                + f'<g transform="scale(1 1)"><g>{spin}{sparks}</g></g></g></g>')
    layer("behind", svg)
