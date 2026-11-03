"""Small helpers for writing SVG: number formatting and SMIL <animate> tags."""
import math

from .config import LOOP, EPS, LEAD_TRIM
from .timeline import SPLINES


def num(v):
    """A number with one decimal, trimmed: 3.0 -> "3", -0.04 -> "0"."""
    s = f"{v:.1f}"
    s = s[:-2] if s.endswith(".0") else s
    return "0" if s == "-0" else s


def fnum(v):
    return num(float(v))


def rnd(i):
    """A repeatable pseudo-random number in [0, 1). The same i always gives the same number."""
    x = math.sin(i * 12.9898 + 78.233) * 43758.5453
    return x - math.floor(x)


def fmt_xy(v):
    return f"{num(v[0])} {num(v[1])}"


def fmt_rotate(v):
    return f"{num(v[0])} {num(v[1])} {num(v[2])}"


def fmt_scale(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


def fmt_uniform_scale(s):
    return f"{fmt_scale(s)} {fmt_scale(s)}"


def fmt_xy_scale(v):
    return f"{fmt_scale(v[0])} {fmt_scale(v[1])}"


def points_str(pts):
    return " ".join(f"{num(x)},{num(y)}" for x, y in pts)


def path_d(pts):
    """An open path through the points."""
    return "M" + " L".join(f"{num(x)},{num(y)}" for x, y in pts)


def animate(attr, track, fmt):
    """An <animate> tag that plays the track on the given attribute, looping forever."""
    keys = track.finished()
    # Shift everything earlier by LEAD_TRIM. The loop still ends at LOOP; the last hold just gets longer.
    keys = [[0.0, keys[0][1], "lin"]] + [[max(EPS, t - LEAD_TRIM), v, e] for t, v, e in keys[1:]]
    for i in range(1, len(keys)):
        if keys[i][0] <= keys[i - 1][0]:
            keys[i][0] = keys[i - 1][0] + EPS / 2
    keys[-1][0] = LOOP
    values = ";".join(fmt(v) for _, v, _ in keys)
    times = ";".join(f"{t / LOOP:.6f}" for t, _, _ in keys)
    if any(e != "lin" for _, _, e in keys[1:]):
        splines = ";".join(SPLINES[e] for _, _, e in keys[1:])
        return (f'<animate attributeName="{attr}" values="{values}" keyTimes="{times}" keySplines="{splines}" '
                f'calcMode="spline" dur="{LOOP}s" repeatCount="indefinite"/>')
    return f'<animate attributeName="{attr}" values="{values}" keyTimes="{times}" dur="{LOOP}s" repeatCount="indefinite"/>'


def animate_transform(kind, track, fmt):
    """Like animate(), but for a transform (translate, rotate or scale)."""
    return animate("transform", track, fmt).replace("<animate ", f'<animateTransform type="{kind}" ')


def fade_group(track):
    """Opens a <g> whose opacity follows the track. Close it with </g>."""
    return f'<g opacity="{fnum(track.keys[0][1])}">' + animate("opacity", track, fnum)


def transform_group(kind, track, fmt):
    """Opens a <g> whose transform follows the track. Close it with </g>."""
    return "<g>" + animate_transform(kind, track, fmt)
