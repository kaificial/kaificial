"""The space background above the page. The camera pans up to it in act 7."""
from engine.camera import FAR_PARALLAX
from engine.config import W, H
from engine.svg import num, rnd

SKY_HEIGHT = H + 60                  # how far the camera moves up
MOON = (430.0, 70.0, 24.0)           # x, y, radius


def sky_gradient(theme):
    stops = ([("0", "#03040c"), ("0.75", "#0a1030"), ("1", "#1c2c66")] if theme == "light"
             else [("0", "#010208"), ("0.75", "#070c26"), ("1", "#16245a")])
    return ('<linearGradient id="skyg" x1="0" y1="0" x2="0" y2="1">'
            + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + "</linearGradient>")


def far_stars():
    """Faint stars that move slower than the rest, for depth."""
    out = []
    for i in range(40):
        x = rnd(i + 400) * W
        y = -FAR_PARALLAX * SKY_HEIGHT + rnd(i + 500) * (H - 50)
        out.append(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(0.4 + 0.5 * rnd(i + 600))}" fill="#ffffff" opacity="{num(0.3 + 0.3 * rnd(i + 700))}"/>')
    return "".join(out)


def moon_defs(p):
    """Mask for the crescent shape. Add it to <defs> once."""
    r = MOON[2]
    return (f'<mask id="moonmask"><circle r="{num(r)}" fill="#ffffff"/>'
            f'<circle cx="{num(r * 0.45)}" cy="{num(-r * 0.2)}" r="{num(r * 0.95)}" fill="#000000"/></mask>')


def moon_body(p):
    """The moon at (0, 0). It's solid so a cat can hide behind it."""
    r = MOON[2]
    return (f'<circle r="{num(r)}" fill="{p["moon_dark"]}"/>'
            f'<circle r="{num(r)}" fill="{p["moon"]}" mask="url(#moonmask)"/>'
            f'<circle cx="{num(-r * 0.45)}" cy="{num(r * 0.3)}" r="{num(r * 0.16)}" fill="{p["moon_dark"]}" opacity="0.25"/>'
            f'<circle cx="{num(-r * 0.6)}" cy="{num(-r * 0.25)}" r="{num(r * 0.1)}" fill="{p["moon_dark"]}" opacity="0.25"/>')


def _planet_limb(p):
    """The curve of the planet below."""
    arc = f"M-40,-12 Q{W / 2},-80 {W + 40},-12"
    return (f'<path d="{arc} L{W + 40},0 L-40,0 Z" fill="{p["limb"]}"/>'
            f'<path d="{arc}" fill="none" stroke="{p["limb_glow"]}" stroke-width="2" opacity="0.7"/>')


def sky(p):
    """Sky, stars and planet. Act 7 draws the moon."""
    top = -(SKY_HEIGHT + H)
    stars = "".join(f'<circle cx="{num(rnd(i + 800) * W)}" cy="{num(top + 10 + rnd(i + 900) * (SKY_HEIGHT + H - 150))}" r="{num(0.7 + 0.8 * rnd(i + 950))}" fill="#ffffff" opacity="{num(0.5 + 0.5 * rnd(i + 990))}"/>'
                    for i in range(40))
    return (f'<rect x="-40" y="{num(top)}" width="{W + 80}" height="{num(-top)}" fill="url(#skyg)"/>'
            + stars + _planet_limb(p))
