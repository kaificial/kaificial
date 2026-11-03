"""Web strands, grapple wires, web splats and the spider-sense tingle."""
import math

from ..config import EPS
from ..layers import layer
from ..svg import num, animate, fmt_uniform_scale, fade_group, transform_group, path_d
from ..timeline import Track


def fixed(pt):
    """A point that never moves (one end of a strand stuck to the page)."""
    return lambda t: pt


def paw(c, key="RH"):
    """One of character c's paws, wherever it is at time t."""
    return lambda t: c.world(t, key)


def strand(start, end, t0, t1, col, width=1.0, shoot=0.08, dt=0.03, layer_name="front", knot=True):
    """A web strand or grapple wire between two moving points, from t0 to t1.

    start and end are functions of time. The strand shoots out from `start` over `shoot`
    seconds. They're only called at render time, after all the choreography exists, so the
    strand can follow things that are animated later in the script.
    """
    def svg(p):
        a0 = start(t0)
        A, B, op = Track(a0), Track(a0), Track(0)
        op.set(t0, 1)
        op.set(t1, 0)
        A.hold(t0 - EPS)
        B.hold(t0 - EPS)
        t = t0
        while t < t1 - 1e-6:
            t = min(t1, t + dt)
            pa, pb = start(t), end(t)
            s = min(1.0, (t - t0) / shoot)
            A.add(t, pa)
            B.add(t, (pa[0] + (pb[0] - pa[0]) * s, pa[1] + (pb[1] - pa[1]) * s))

        def fx(v):
            return num(v[0])

        def fy(v):
            return num(v[1])
        out = (fade_group(op) + f'<line stroke="{p[col]}" stroke-width="{width}" stroke-linecap="round">'
               + animate("x1", A, fx) + animate("y1", A, fy) + animate("x2", B, fx) + animate("y2", B, fy) + "</line>")
        if knot:
            out += f'<circle r="1.7" fill="{p[col]}">' + animate("cx", B, fx) + animate("cy", B, fy) + "</circle>"
        return out + "</g>"
    layer(layer_name, svg)


def web_splat(x, y, t, life, size=1.0):
    """A blob of web that sticks where it lands, for `life` seconds."""
    def svg(p):
        op, sc = Track(0), Track(0.2)
        op.set(t, 1)
        op.hold(t + life)
        op.add(t + life + 0.12, 0, "in")
        sc.hold(t)
        sc.add(t + 0.08, 1.0, "out")
        r = 6 * size
        spokes = "".join(f'<path d="M0,0 L{num(r * math.cos(a))},{num(r * math.sin(a) * 0.7)}"/>' for a in (i * math.pi / 4 for i in range(8)))
        rings = "".join(f'<ellipse rx="{num(r * k / 3)}" ry="{num(r * k / 3 * 0.7)}" fill="none"/>' for k in (1, 2, 3))
        return (f'<g transform="translate({num(x)},{num(y)})">' + fade_group(op) + transform_group("scale", sc, fmt_uniform_scale)
                + f'<g stroke="{p["web"]}" stroke-width="0.8" fill="none">{spokes}{rings}</g>'
                + f'<ellipse rx="{num(r * 0.45)}" ry="{num(r * 0.32)}" fill="{p["web"]}" opacity="0.6"/></g></g></g>')
    layer("overlay", svg)


def tingle(x, y, t, dur=0.35):
    """Spider-sense: little zigzag lines flicker around her head."""
    def svg(p):
        op = Track(0)
        op.set(t, 1)
        op.hold(t + dur * 0.6)
        op.add(t + dur, 0, "in")
        out = []
        for a in (-150, -115, -65, -30):
            r0, r1 = 10, 18
            ar = math.radians(a)
            pts = []
            for j in range(5):
                rr = r0 + (r1 - r0) * j / 4
                off = 1.6 if j % 2 else -1.6
                pts.append((x + rr * math.cos(ar) - off * math.sin(ar), y + rr * math.sin(ar) + off * math.cos(ar)))
            out.append(f'<path d="{path_d(pts)}" fill="none" stroke="{p["fg"]}" stroke-width="1.2" stroke-linecap="round"/>')
        return fade_group(op) + "".join(out) + "</g>"
    layer("overlay", svg)
