"""Hit effects: sparks, shockwave rings, slash arcs, speed lines and full-screen flashes."""
import math

from ..config import W, H
from ..layers import layer
from ..svg import num, fnum, rnd, animate, animate_transform, fmt_uniform_scale, fade_group, transform_group
from ..timeline import Track


def spark(x, y, t, size, kind="spark", dur=0.26, layer_name="front"):
    """An impact: a thin ring that expands and fades, with a few sharp lines shooting outward.

    kind="white" is a small glint instead (a blade catching the light, a block clicking into place).
    """
    def svg(p):
        col = p["fg"]
        op = Track(0)
        op.set(t, 1)
        op.hold(t + dur * 0.35)
        op.add(t + dur, 0, "in")
        out = [f'<g transform="translate({num(x)},{num(y)})"><g opacity="0">', animate("opacity", op, str)]
        if kind == "white":
            sc = Track(0.2)
            sc.hold(t)
            sc.add(t + dur * 0.35, 1.0, "out")
            sc.add(t + dur, 0.5, "in")
            rot = Track(0.0)
            rot.hold(t)
            rot.add(t + dur, 40.0, "out")
            L = size * 1.6
            out.append("<g>" + animate_transform("rotate", rot, lambda a: f"{num(a)} 0 0") + "<g>" + animate_transform("scale", sc, fmt_uniform_scale)
                       + f'<path d="M{num(-L)},0 H{num(L)} M0,{num(-L)} V{num(L)} M{num(-L * .45)},{num(-L * .45)} L{num(L * .45)},{num(L * .45)} M{num(-L * .45)},{num(L * .45)} L{num(L * .45)},{num(-L * .45)}" '
                       f'stroke="{col}" stroke-width="1.3" stroke-linecap="round"/></g></g>')
        else:
            radius = Track(size * 0.3)
            radius.hold(t)
            radius.add(t + dur, size * 2.6, "out")
            width = Track(2.4)
            width.hold(t)
            width.add(t + dur, 0.3, "out")
            out.append(f'<circle r="{num(size * .3)}" fill="none" stroke="{col}" stroke-width="2.4">'
                       + animate("r", radius, num) + animate("stroke-width", width, num) + "</circle>")
            count = 7
            for i in range(count):
                a = i * 2 * math.pi / count + rnd(i * 3 + size) * 0.5
                r0, L = size * 0.6, size * (1.0 + 0.9 * rnd(i + size))
                push = size * (2.2 + 1.2 * rnd(i * 7 + size))
                ux, uy = math.cos(a), math.sin(a)
                ends = Track((r0, r0 + L))
                ends.hold(t)
                ends.add(t + dur * 0.9, (r0 + push, r0 + push + L * 0.15), "out")
                out.append(f'<polyline fill="none" stroke="{col}" stroke-width="{num(1.0 + 0.8 * rnd(i + 2))}" stroke-linecap="round" points="{num(r0 * ux)},{num(r0 * uy)} {num((r0 + L) * ux)},{num((r0 + L) * uy)}">'
                           + animate("points", ends, lambda v, ux=ux, uy=uy: f"{num(v[0] * ux)},{num(v[0] * uy)} {num(v[1] * ux)},{num(v[1] * uy)}") + "</polyline>")
        out.append("</g></g>")
        return "".join(out)
    layer(layer_name, svg)


def impact_lines(x, y, t, colour="fg"):
    """The anime impact frame: thin lines bursting from the hit point to the edges, for two frames."""
    def svg(p):
        op = Track(0)
        op.set(t, 0.75)
        op.hold(t + 0.04)
        op.add(t + 0.1, 0, "in")
        lines = []
        for i in range(22):
            a = i * 2 * math.pi / 22 + rnd(i + t) * 0.22
            r0 = 34 + 26 * rnd(i * 2 + t)
            r1 = r0 + 90 + 160 * rnd(i * 3 + t)
            lines.append(f'<path d="M{num(x + r0 * math.cos(a))},{num(y + r0 * math.sin(a))} L{num(x + r1 * math.cos(a))},{num(y + r1 * math.sin(a))}" stroke-width="{num(0.6 + 1.0 * rnd(i + 9))}"/>')
        return f'<g opacity="0" stroke="{p[colour]}" stroke-linecap="round">' + animate("opacity", op, str) + "".join(lines) + "</g>"
    layer("front", svg)


def impact_frame(t, x, y, chars, dur=0.12):
    """Anime impact frame: a black frame, then a white frame, with the cats as silhouettes.
    Use only for big hits, at most one per second."""
    from .afterimages import _still_figure
    from ..timeline import sample, sample_step

    def figure(c, tt, ink):
        x0, y0 = sample(c.pos, tt)
        a, px, py = sample(c.rot, tt)
        sx, sy = sample(c.squash, tt)
        f = sample_step(c.facing, tt)
        return (f'<g transform="translate({num(x0)},{num(y0)}) rotate({num(a)} {num(px)} {num(py)}) scale({num(f * sx)},{num(sy)})">'
                + _still_figure(c.pose_at(tt), ink, width=3.4) + "</g>")

    def svg(p):
        mid = t + dur * 0.55
        out = []
        for b0, b1, bg, ink, seed in ((t, mid, "#05060a", "#ffffff", 0), (mid, t + dur, "#f7f5ee", "#05060a", 7)):
            op = Track(0)
            op.set(b0, 1)
            op.set(b1, 0)
            spikes = []
            for i in range(30):
                a = i * 2 * math.pi / 30 + (rnd(i + seed + t) - 0.5) * 0.18
                w = 0.012 + 0.03 * rnd(i * 3 + seed)
                r0 = 22 + 30 * rnd(i * 5 + seed + t)
                r1 = 900
                spikes.append(f"M{num(x + r0 * math.cos(a))},{num(y + r0 * math.sin(a))} "
                              f"L{num(x + r1 * math.cos(a - w))},{num(y + r1 * math.sin(a - w))} "
                              f"L{num(x + r1 * math.cos(a + w))},{num(y + r1 * math.sin(a + w))} Z")
            visible = [c for c in chars if sample_step(c.opacity, b0)]
            out.append(fade_group(op) + f'<rect x="-40" y="-40" width="{W + 80}" height="{H + 80}" fill="{bg}"/>'
                       + f'<path d="{" ".join(spikes)}" fill="{ink}"/>'
                       + f'<circle cx="{num(x)}" cy="{num(y)}" r="14" fill="{bg}" stroke="{ink}" stroke-width="2.5"/>'
                       + "".join(figure(c, b0, ink) for c in visible) + "</g>")
        return "".join(out)
    layer("overlay", svg)


def flash(t, dur=0.06, amount=0.7, colour="flash"):
    """The whole frame flashes bright for a moment."""
    def svg(p):
        op = Track(0)
        op.set(t, amount)
        op.hold(t + dur * 0.5)
        op.add(t + dur, 0, "in")
        return f'<rect width="{W}" height="{H}" fill="{p[colour]}" opacity="0">' + animate("opacity", op, str) + "</rect>"
    layer("overlay", svg)


def tint(t, colour, amount=0.5, dur=0.08):
    """The whole frame flashes a colour (a palette key or a plain colour)."""
    def svg(p):
        op = Track(0)
        op.set(t, amount)
        op.hold(t + dur * 0.5)
        op.add(t + dur, 0, "in")
        return f'<rect x="-30" y="-30" width="{W + 60}" height="{H + 60}" fill="{p.get(colour, colour)}" opacity="0">' + animate("opacity", op, fnum) + "</rect>"
    layer("overlay", svg)


def ring(x, y, t, r=40, col="fg", dur=0.35, w=2.0, squash=1.0):
    """A shockwave ring that grows out from (x, y) and fades."""
    def svg(p):
        op, sc = Track(0), Track(0.1)
        op.set(t, 0.9)
        op.add(t + dur, 0, "in")
        sc.hold(t)
        sc.add(t + dur, 1.0, "out")
        return (f'<g transform="translate({num(x)},{num(y)}) scale(1 {num(squash)})">' + fade_group(op) + transform_group("scale", sc, fmt_uniform_scale)
                + f'<circle r="{num(r)}" fill="none" stroke="{p[col]}" stroke-width="{num(w)}" vector-effect="non-scaling-stroke"/></g></g></g>')
    layer("front", svg)


def crescent(cx, cy, r_out, a0, a1, t, dur=0.1):
    """The swoosh a sword cut leaves behind: a crescent from angle a0 to a1."""
    r_in = r_out * 0.55

    def svg(p):
        op = Track(0)
        op.set(t, 0.45)
        op.add(t + dur, 0, "in")
        sc = Track(0.8)
        sc.hold(t)
        sc.add(t + dur, 1.1, "out")
        A0, A1 = math.radians(a0), math.radians(a1)
        big = 1 if abs(A1 - A0) > math.pi else 0
        sweep = 1 if A1 > A0 else 0
        d = (f"M{num(r_out * math.cos(A0))},{num(r_out * math.sin(A0))} A{num(r_out)},{num(r_out)} 0 {big} {sweep} "
             f"{num(r_out * math.cos(A1))},{num(r_out * math.sin(A1))} L{num(r_in * math.cos(A1))},{num(r_in * math.sin(A1))} "
             f"A{num(r_in)},{num(r_in)} 0 {big} {1 - sweep} {num(r_in * math.cos(A0))},{num(r_in * math.sin(A0))} Z")
        return (f'<g transform="translate({num(cx)},{num(cy)})"><g opacity="0">' + animate("opacity", op, str)
                + animate_transform("scale", sc, fmt_uniform_scale) + f'<path d="{d}" fill="{p["fg"]}"/></g></g>')
    layer("front", svg)


def smear_line(x0, y0, x1, y1, t, width=5, dur=0.07, colour="fg"):
    """A motion smear: one thick line that's gone almost as soon as it appears."""
    def svg(p):
        op = Track(0)
        op.set(t, 0.5)
        op.add(t + dur, 0, "in")
        return (f'<path d="M{num(x0)},{num(y0)} L{num(x1)},{num(y1)}" stroke="{p[colour]}" stroke-width="{width}" stroke-linecap="round" opacity="0">'
                + animate("opacity", op, str) + "</path>")
    layer("front", svg)


def speed_lines(x, t0, t1, y0=-6, y1=36, horizontal=False):
    """A few streaks trailing behind something fast."""
    def svg(p):
        op = Track(0)
        op.set(t0, 0.55)
        op.hold(t0 + (t1 - t0) * 0.5)
        op.add(t1, 0, "in")
        if horizontal:
            lines = "".join(f'<path d="M{num(x + dx)},{num(y0 + dy)} h{num(ln)}"/>' for dx, dy, ln in [(0, -24, -40), (-8, -16, -60), (2, -8, -46)])
        else:
            lines = "".join(f'<path d="M{num(x + dx)},{num(a)} V{num(b)}"/>' for dx, a, b in [(-8, y0 + 4, y1 - 10), (0, y0, y1), (8, y0 + 6, y1 - 12)])
        return f'<g opacity="0" stroke="{p["fg"]}" stroke-width="2" stroke-linecap="round">' + animate("opacity", op, str) + lines + "</g>"
    layer("page", svg)
