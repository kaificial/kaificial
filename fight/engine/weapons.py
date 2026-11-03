"""Mochi's katana and pickaxe. Both are built from the right paw (RH) and the weapon tip (WT) of a pose."""
import math

from .poses import POSES, joint
from .svg import animate, points_str


def _weapon_frame(pose):
    """The paw, the tip, a unit vector along the weapon, one across it, and the weapon's length."""
    rh, wt = pose["RH"], joint(pose, "WT")
    dx, dy = wt[0] - rh[0], wt[1] - rh[1]
    length = math.hypot(dx, dy) or 1
    ux, uy = dx / length, dy / length
    return rh, wt, (ux, uy), (-uy, ux), length


def katana_parts(pose):
    """A curved single-edged blade with a temper line, an oval guard, a wrapped handle and an end cap."""
    rh, wt, (ux, uy), (px, py), length = _weapon_frame(pose)
    # the cutting edge is on the -perp side, and the blade bows the other way, toward the spine
    bx, by = rh[0] + ux * 2.6, rh[1] + uy * 2.6
    lb = length - 2.6
    bend = lb * 0.075

    def spine(s):
        c = 4 * bend * s * (1 - s)
        return bx + ux * lb * s + px * c, by + uy * lb * s + py * c

    def off(pt, side, w):
        return pt[0] + px * side * w, pt[1] + py * side * w

    back = [off(spine(s), 1, 1.25 - 0.3 * s) for s in (0, 0.3, 0.6, 0.86)]
    edge = [off(spine(s), -1, 1.9 - 0.4 * s) for s in (0.86, 0.6, 0.3, 0)]
    blade = back + [wt] + edge
    hamon = [off(spine(s), -1, 0.55) for s in (0.06, 0.3, 0.6, 0.86)]
    cx, cy = rh[0] + ux * 1.2, rh[1] + uy * 1.2
    tsuba = [(cx + px * 3.4 * math.cos(a) + ux * 1.7 * math.sin(a), cy + py * 3.4 * math.cos(a) + uy * 1.7 * math.sin(a))
             for a in [i * math.pi / 4 for i in range(8)]]
    h0x, h0y = rh[0] - ux * 0.6, rh[1] - uy * 0.6
    h1x, h1y = rh[0] - ux * 10.5, rh[1] - uy * 10.5
    tsuka = [(h0x + px * 1.4, h0y + py * 1.4), (h1x + px * 1.4, h1y + py * 1.4), (h1x - px * 1.4, h1y - py * 1.4), (h0x - px * 1.4, h0y - py * 1.4)]
    diamonds = []
    for s in (0.22, 0.52, 0.82):
        dx, dy = h0x + (h1x - h0x) * s, h0y + (h1y - h0y) * s
        diamonds.append([(dx + ux * 1.3, dy + uy * 1.3), (dx + px * 1.2, dy + py * 1.2), (dx - ux * 1.3, dy - uy * 1.3), (dx - px * 1.2, dy - py * 1.2)])
    kx, ky = rh[0] - ux * 11.3, rh[1] - uy * 11.3
    kashira = [(kx + ux * 0.9 + px * 1.6, ky + uy * 0.9 + py * 1.6), (kx - ux * 0.9 + px * 1.6, ky - uy * 0.9 + py * 1.6),
               (kx - ux * 0.9 - px * 1.6, ky - uy * 0.9 - py * 1.6), (kx + ux * 0.9 - px * 1.6, ky + uy * 0.9 - py * 1.6)]
    return dict(blade=blade, hamon=hamon, tsuba=tsuba, tsuka=tsuka, d0=diamonds[0], d1=diamonds[1], d2=diamonds[2], kashira=kashira)


# (part, fill, stroke, stroke width), drawn back to front
_KATANA_STYLE = [
    ("tsuka", "wrap", None, 0),
    ("d0", "red", None, 0), ("d1", "red", None, 0), ("d2", "red", None, 0),
    ("kashira", "tsuba", "fg", 0.5),
    ("blade", "blade", "blade_edge", 0.7),
    ("hamon", None, "hamon", 0.9),
    ("tsuba", "tsuba", "fg", 0.6),
]


def katana_svg(p, pose_track):
    """The katana, following the paw through every pose in pose_track."""
    parts = katana_parts(POSES[pose_track.keys[0][1]])
    out = []
    for key, fill, stroke, width in _KATANA_STYLE:
        tag = "polyline" if key == "hamon" else "polygon"
        attrs = f'fill="{p[fill]}"' if fill else 'fill="none"'
        if stroke:
            attrs += f' stroke="{p[stroke]}" stroke-width="{width}" stroke-linejoin="round"'
        if key == "hamon":
            attrs += ' stroke-linecap="round" opacity="0.75"'
        anim = animate("points", pose_track, lambda name, key=key: points_str(katana_parts(POSES[name])[key]))
        out.append(f'<{tag} points="{points_str(parts[key])}" {attrs}>{anim}</{tag}>')
    return "".join(out)


def pick_parts(pose):
    rh, wt, (ux, uy), (px, py), _ = _weapon_frame(pose)
    h0x, h0y = rh[0] - ux * 4, rh[1] - uy * 4
    handle = [(h0x + px * 1.1, h0y + py * 1.1), (wt[0] + px * 1.1, wt[1] + py * 1.1), (wt[0] - px * 1.1, wt[1] - py * 1.1), (h0x - px * 1.1, h0y - py * 1.1)]
    head = [(wt[0] + px * 11 - ux * 2.2, wt[1] + py * 11 - uy * 2.2), (wt[0] + px * 6 + ux * 2.2, wt[1] + py * 6 + uy * 2.2),
            (wt[0] + ux * 2.8, wt[1] + uy * 2.8), (wt[0] - px * 6 + ux * 2.2, wt[1] - py * 6 + uy * 2.2),
            (wt[0] - px * 11 - ux * 2.2, wt[1] - py * 11 - uy * 2.2), (wt[0] - px * 6 - ux * 1.2, wt[1] - py * 6 - uy * 1.2),
            (wt[0] - ux * 1.4, wt[1] - uy * 1.4), (wt[0] + px * 6 - ux * 1.2, wt[1] + py * 6 - uy * 1.2)]
    return dict(handle=handle, head=head)


def pick_svg(p, pose_track):
    """The pickaxe, following the paw through every pose in pose_track."""
    out = []
    for key, fill, stroke in (("handle", "wood", "fg"), ("head", "blade", "fg")):
        pts = pick_parts(POSES[pose_track.keys[0][1]])[key]
        out.append(f'<polygon points="{points_str(pts)}" fill="{p[fill]}" stroke="{p[stroke]}" stroke-width="0.7" stroke-linejoin="round">'
                   + animate("points", pose_track, lambda name, key=key: points_str(pick_parts(POSES[name])[key])) + "</polygon>")
    return "".join(out)
