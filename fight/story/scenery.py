"""The sky above the page: a starfield, a glowing horizon and a range of snowy mountains.

It sits right above the page, out of frame, until the camera pans up in act 7.
"""
from engine.camera import FAR_PARALLAX
from engine.config import W, H
from engine.svg import num, rnd, path_d

SKY_HEIGHT = H + 60                  # how far the camera pans up
MOUNTAIN_HIT = (700.0, 214.0)        # where Mochi smashes into the mountainside (on screen, camera up)


def main_mountain():
    """Outline of the big mountain Mochi gets punched into (y=0 is the top of the page)."""
    peak_x, peak_y = MOUNTAIN_HIT[0] + 22, -SKY_HEIGHT + 128
    return [(500, 0), (540, -34), (570, -60), (596, -78), (612, -104), (636, -122), (652, -148), (676, -168), (694, -186),
            (708, -198), (peak_x, peak_y), (736, -198), (752, -186), (770, -176), (790, -156), (812, -140), (840, -112), (870, -96), (870, 0)]


def sky_gradient(theme):
    stops = ([("0", "#02030a"), ("0.55", "#070b24"), ("0.84", "#1c2f7a"), ("0.94", "#8fb3ff"), ("1", "#ffffff")] if theme == "light"
             else [("0", "#010208"), ("0.55", "#060a20"), ("0.84", "#18286a"), ("0.94", "#3b5cb8"), ("1", "#0d1117")])
    return ('<linearGradient id="skyg" x1="0" y1="0" x2="0" y2="1">'
            + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + "</linearGradient>")


def far_stars():
    """Faint stars far away. They pan slower than everything else, which gives the sky depth."""
    out = []
    for i in range(60):
        x = rnd(i + 400) * W
        y = -FAR_PARALLAX * SKY_HEIGHT + rnd(i + 500) * (H - 50)
        out.append(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(0.4 + 0.6 * rnd(i + 600))}" fill="#ffffff" opacity="{num(0.3 + 0.4 * rnd(i + 700))}"/>')
    return "".join(out)


def _closed(pts):
    return path_d(pts) + " Z"


def sky(p):
    """Dark space at the top fading to a glowing horizon, stars, and the mountains."""
    top = -(SKY_HEIGHT + H)
    stars = "".join(f'<circle cx="{num(rnd(i + 800) * W)}" cy="{num(top + 10 + rnd(i + 900) * (SKY_HEIGHT + H - 150))}" r="{num(0.7 + 0.9 * rnd(i + 950))}" fill="#ffffff" opacity="{num(0.5 + 0.5 * rnd(i + 990))}"/>'
                    for i in range(45))
    twinkle = "".join(f'<circle cx="{num(rnd(i + 1100) * W)}" cy="{num(-SKY_HEIGHT + 20 + rnd(i + 1200) * (H - 120))}" r="1.3" fill="#ffffff">'
                      f'<animate attributeName="opacity" values="0.2;1;0.2" dur="{num(0.8 + rnd(i) * 0.9)}s" repeatCount="indefinite"/></circle>' for i in range(12))
    # the far range: hazy and pale, with small snowy tips
    far = [(-40, 0), (-40, -80), (20, -96), (70, -122), (110, -104), (165, -138), (220, -112), (270, -150), (320, -118),
           (380, -132), (430, -102), (480, -116), (540, -70), (580, 0)]
    far_snow = "".join(f'<path d="M{x - 9},{y + 9} L{x},{y} L{x + 10},{y + 10} L{x + 4},{y + 7} L{x - 2},{y + 11} Z" fill="{p["snow_shade"]}" opacity="0.6"/>'
                       for x, y in ((70, -122), (165, -138), (270, -150), (380, -132)))
    mid = [(-40, 0), (-40, -40), (40, -62), (100, -50), (170, -84), (240, -58), (300, -76), (360, -52), (430, -70), (500, -40), (540, 0)]
    # the main mountain is lit from the left; a ridge splits the light side from the shadow side
    main = main_mountain()
    peak = main[10]
    ridge = [peak, (728, -184), (724, -160), (734, -136), (730, -110), (744, -80), (752, -40), (760, 0)]
    shadow = ridge + [(870, 0), (870, -96), (840, -112), (812, -140), (790, -156), (770, -176), (752, -186), (736, -198)]
    strata = "".join(f'<path d="M{num(x0)},{num(y0)} Q{num((x0 + x1) / 2)},{num(y0 + dy)} {num(x1)},{num(y1)}" fill="none" stroke="{p["mtn_hi"]}" stroke-width="0.7" opacity="0.35"/>'
                     for x0, y0, x1, y1, dy in ((600, -88, 700, -80, -8), (585, -64, 712, -52, -10), (620, -116, 700, -112, -6),
                                                (560, -36, 720, -24, -12), (655, -140, 708, -150, -4)))
    crevices = "".join(f'<path d="M{num(x)},{num(y)} l{num(dx)},{num(dy)} l{num(dx * 0.6)},{num(dy * 1.2)}" fill="none" stroke="{p["mtn_shadow"]}" stroke-width="1.2" opacity="0.7"/>'
                       for x, y, dx, dy in ((680, -160, 6, 18), (650, -128, -4, 20), (700, -130, 4, 16), (620, -96, 6, 22), (590, -60, -5, 18)))
    snow_lit = [(682, -166), (690, -176), peak, (728, -184), (724, -166), (716, -158), (712, -168), (704, -152), (698, -162),
                (690, -150), (686, -160)]
    snow_shade = [peak, (736, -198), (752, -186), (760, -170), (750, -174), (744, -160), (738, -170), (730, -158), (724, -166), (728, -184)]
    pines = ""
    for i in range(26):
        x = 500 + i * 14 + 6 * rnd(i + 1500)
        h = 10 + 8 * rnd(i + 1600)
        pines += f'<path d="M{num(x)},{num(-2)} L{num(x + 3.5)},{num(-2 - h)} L{num(x + 7)},{num(-2)} Z" fill="{p["pine"]}"/>'
    for i in range(30):
        x = -30 + i * 18 + 6 * rnd(i + 1700)
        h = 7 + 6 * rnd(i + 1800)
        pines += f'<path d="M{num(x)},{num(-1)} L{num(x + 3)},{num(-1 - h)} L{num(x + 6)},{num(-1)} Z" fill="{p["pine"]}" opacity="0.85"/>'
    haze = (f'<defs><linearGradient id="mhaze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["haze"]}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{p["haze"]}" stop-opacity="0.45"/></linearGradient></defs>'
            f'<rect x="-40" y="-46" width="{W + 80}" height="46" fill="url(#mhaze)"/>')
    mountains = (f'<path d="{_closed(far)}" fill="{p["mtn_far"]}" opacity="0.85"/>' + far_snow
                 + f'<path d="{_closed(mid)}" fill="{p["mtn_mid"]}"/>'
                 + f'<path d="{_closed(main)}" fill="{p["mtn_lit"]}" stroke="{p["mtn_hi"]}" stroke-width="0.8" stroke-opacity="0.6" stroke-linejoin="round"/>'
                 + f'<path d="{_closed(shadow)}" fill="{p["mtn_shadow"]}"/>'
                 + f'<path d="{path_d(ridge)}" fill="none" stroke="{p["mtn_hi"]}" stroke-width="0.8" opacity="0.5"/>'
                 + strata + crevices
                 + f'<path d="{_closed(snow_lit)}" fill="{p["snow"]}"/>' + f'<path d="{_closed(snow_shade)}" fill="{p["snow_shade"]}"/>'
                 + haze + pines)
    return f'<rect x="-40" y="{num(top)}" width="{W + 80}" height="{num(-top)}" fill="url(#skyg)"/>' + stars + twinkle + mountains
