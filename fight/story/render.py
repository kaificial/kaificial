"""Draws the finished choreography as one SVG, for one theme."""
import html

from engine.camera import SHAKE, PAN, PAN_FAR
from engine.config import EPS, FONT_STACK, H, H1_Y, LOOP, RULE_Y, W
from engine.layers import draw_layer
from engine.palette import PALETTES
from engine.svg import animate_transform, fmt_xy
from engine.timeline import Track, sample_step

from . import scenery, tunnel
from .cast import mochi, mochi_digging, sesame
from .page import FORWARD, H1_TEXT, LINES, SKILLS_LETTERS


def _space_outline(times):
    """Sesame is a black cat, so she'd vanish against the night sky. While the sky is behind her
    we draw a second copy of her with a light outline. This track says when that copy shows."""
    w0, w1 = times.pan_up + 0.35, times.pan_down + 0.55
    switch_times = sorted({k[0] for k in sesame.opacity.keys} | {w0, w0 + EPS, w1, w1 + EPS})
    track = Track(0)
    for t in switch_times:
        if t <= 0:
            continue
        v = sample_step(sesame.opacity, t) if (w0 + EPS <= t <= w1) else 0
        if v != track.end_value:
            track.set(t, v)
    return track


def render(theme, times):
    p = PALETTES[theme]
    in_space = dict(p, cat_b_line=p["void_fg"], cat_b_whisk=p["void_fg"])
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT_STACK}">',
           "<defs>" + tunnel.tunnel_clip() + scenery.sky_gradient(theme) + "</defs>",
           f'<rect width="{W}" height="{H}" fill="{p["bg"]}"/>',
           "<g>", animate_transform("translate", SHAKE, fmt_xy),
           "<g>" + animate_transform("translate", PAN, fmt_xy) + scenery.sky(p) + "</g>",
           "<g>" + animate_transform("translate", PAN_FAR, fmt_xy) + scenery.far_stars() + "</g>",
           # the page itself
           "<g>" + animate_transform("translate", PAN, fmt_xy),
           f'<rect x="-40" y="0" width="{W + 80}" height="{H + 40}" fill="{p["bg"]}"/>',
           f'<text x="0" y="{H1_Y}" font-size="32" font-weight="600" fill="{p["fg"]}">{html.escape(H1_TEXT)}</text>',
           f'<path d="M0,{RULE_Y} H{W}" stroke="{p["rule"]}" stroke-width="1"/>']
    for line in LINES:
        for word in line:
            out.append(word.svg_with_halves(p["fg"]))
    for letter in SKILLS_LETTERS:
        out.append(letter.svg(p["fg"]))
    out.extend(draw_layer("tunnel", p))
    out.append('<g clip-path="url(#tunnel)">' + mochi_digging.svg(p, armed=True) + "</g>")
    out.append(FORWARD.svg(p["fg"]))
    out.extend(draw_layer("page", p))
    out.append("</g>")
    # everything below stays put on screen while the page pans
    out.extend(draw_layer("behind", p))
    out.append(sesame.svg(p))
    out.append(sesame.svg(in_space, opacity=_space_outline(times)))
    out.append(mochi.svg(p, armed=True, katana_window=(5.9, times.boom + 0.4), pick_window=(0.0, LOOP)))
    out.extend(draw_layer("front", p))
    out.extend(draw_layer("overlay", p))
    out.append("</g></svg>")
    return "".join(out)
