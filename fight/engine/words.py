"""Words on the page. Each word is its own <text>, so the fight can grab, throw and slice it."""
import html
import itertools
import math

from .config import FLOOR, FONT, FONT_BOLD, FONT_SIZE
from .svg import num, animate, animate_transform, fmt_xy, fmt_uniform_scale, points_str
from .timeline import Track, sample

_clip_ids = itertools.count()


class Word:
    def __init__(self, text, x, y, w, size=FONT_SIZE, centred=True, bold=False):
        self.text, self.x, self.y, self.w, self.size = text, x, y, w, size
        self.centred, self.bold = centred, bold
        self.cx, self.cy = x + w / 2, y - size * 0.33      # the word's centre
        self.offset = Track((0.0, 0.0))                   # how far it has moved from its home spot
        self.rot = Track(0.0)
        self.scale = Track(1.0)
        self.opacity = Track(1)
        self.animated = False
        self.halves = None                                # the two pieces, once it's been cut
        self.clip = None                                  # set on a half: which side of the cut it keeps
        self.clip_id = None

    def pos(self, t):
        """Where the word's centre is at time t."""
        dx, dy = sample(self.offset, t)
        return self.cx + dx, self.cy + dy

    def move_through(self, keys):
        """Move the word's centre through (t, (x, y)) or (t, (x, y), angle) keys."""
        self.animated = True
        for item in keys:
            t, (x, y) = item[0], item[1]
            self.offset.add(t, (x - self.cx, y - self.cy))
            if len(item) > 2:
                self.rot.add(t, item[2])

    def shake(self, t0, t1, amp, hz=28):
        """Shiver in place, wherever the word is right now."""
        self.animated = True
        self.offset.hold(t0)
        bx, by = self.offset.end_value
        t, i = t0, 0
        while t < t1 - 1 / hz:
            t += 1 / hz
            i += 1
            self.offset.add(t, (bx + amp * (1 if i % 2 else -1), by + amp * 0.4 * (1 if (i // 2) % 2 else -1)))
        self.offset.add(t1, (bx, by))

    def fly(self, t0, t1, lx, ly, rot, h, bounce=None):
        """Fly in an arc to (lx, ly), spinning by `rot` degrees. bounce = (dx, duration, height)."""
        self.animated = True
        self.offset.hold(t0)
        self.rot.hold(t0)
        dx, dy = self.offset.end_value
        x0, y0, r0 = self.cx + dx, self.cy + dy, self.rot.end_value
        k = max(5, int(round((t1 - t0) / 0.04)))
        for i in range(1, k + 1):
            s = i / k
            x, y = x0 + (lx - x0) * s, y0 + (ly - y0) * s - 4 * h * s * (1 - s)
            self.offset.add(t0 + (t1 - t0) * s, (x - self.cx, y - self.cy))
            self.rot.add(t0 + (t1 - t0) * s, r0 + rot * s)
        if bounce:
            bx, bt, bh = bounce
            r0 = self.rot.end_value
            for i in range(1, 6):
                s = i / 5
                self.offset.add(t1 + bt * s, (lx + bx * s - self.cx, ly - 4 * bh * s * (1 - s) - self.cy))
                self.rot.add(t1 + bt * s, r0 + 12 * s)

    def restore(self, t0, t1):
        """Glide back home and straighten up."""
        self.offset.hold(t0)
        self.rot.hold(t0)
        self.offset.add(t1, (0.0, 0.0), "inout")
        self.rot.add(t1, 0.0, "inout")

    def slice(self, t, angle, fall=((-26, 70), (24, -120)), through=None):
        """Cut the word in two along a line at `angle` degrees, wherever it is (even mid-air).

        through: a point on the page the cut passes through (where the blade actually crossed);
        defaults to the word's centre. fall: (sideways drift, spin) for each half as it drops.
        """
        self.animated = True
        bx, by = sample(self.offset, t)
        r0 = sample(self.rot, t)
        self.opacity.set(t, 0)
        a = math.radians(angle - r0)
        d, nn = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
        self.halves = []
        c = (through[0] - bx, through[1] - by) if through else (self.cx, self.cy)     # back into the word's own frame
        for sgn, (ddx, drot) in zip((1, -1), fall):
            half = Word(self.text, self.x, self.y, self.w, self.size, self.centred, bold=self.bold)
            half.opacity = Track(0)
            half.opacity.set(t, 1)
            L = 120
            half.clip = [(c[0] + d[0] * L, c[1] + d[1] * L), (c[0] - d[0] * L, c[1] - d[1] * L),
                         (c[0] - d[0] * L + sgn * nn[0] * L, c[1] - d[1] * L + sgn * nn[1] * L),
                         (c[0] + d[0] * L + sgn * nn[0] * L, c[1] + d[1] * L + sgn * nn[1] * L)]
            half.clip_id = f"cut{next(_clip_ids)}"
            half.animated = True
            half.offset.set(t, (bx, by))
            half.rot.set(t, r0)
            half.offset.add(t + 0.1, (bx + sgn * nn[0] * 5, by + sgn * nn[1] * 5), "out")
            x0, y0 = self.cx + bx + sgn * nn[0] * 5, self.cy + by + sgn * nn[1] * 5
            lx, ly = x0 + ddx, FLOOR - 7
            dur = 0.42 + 0.18 * max(0.0, 1 - y0 / 300)
            for i in range(1, 11):
                s = i / 10
                half.offset.add(t + 0.1 + dur * s, (x0 + (lx - x0) * s - self.cx, y0 + (ly - y0) * (s * s) - self.cy))
                half.rot.add(t + 0.1 + dur * s, r0 + drot * s)
            self.halves.append(half)

    # ---------------------------------------------------------------- drawing
    def text_svg(self, fg):
        """The word, sitting still in its home spot."""
        # The viewer's font may be a little narrower or wider than the one we measured with, so the
        # word sits centred in its slot at its natural size. Forcing an exact width would either
        # open gaps between letters or stretch them.
        anchor = f'x="{num(self.cx)}" text-anchor="middle"' if self.centred else f'x="{num(self.x)}"'
        weight = ' font-weight="700"' if self.bold else ""
        return (f'<text {anchor} y="{num(self.y)}" font-size="{self.size}" fill="{fg}"{weight}>'
                f'{html.escape(self.text)}</text>')

    def svg(self, fg):
        text = self.text_svg(fg)
        if not self.animated:
            return text
        if any(k[1] != 1.0 for k in self.scale.keys):
            text = (f'<g transform="translate({num(self.cx)} {num(self.cy)})"><g>' + animate_transform("scale", self.scale, fmt_uniform_scale)
                    + f'<g transform="translate({num(-self.cx)} {num(-self.cy)})">{text}</g></g></g>')
        clip = ""
        if self.clip:
            clip = f'<clipPath id="{self.clip_id}"><polygon points="{points_str(self.clip)}"/></clipPath>'
            text = f'<g clip-path="url(#{self.clip_id})">{text}</g>'
        return (f'{clip}<g opacity="{self.opacity.keys[0][1]}">' + animate("opacity", self.opacity, str)
                + animate_transform("translate", self.offset, fmt_xy) + "<g>"
                + animate_transform("rotate", self.rot, lambda a: f"{num(a)} {num(self.cx)} {num(self.cy)}")
                + text + "</g></g>")

    def svg_with_halves(self, fg):
        return self.svg(fg) + ("".join(h.svg(fg) for h in self.halves) if self.halves else "")


def layout(text, y):
    """Lay out a line of text as separate words. **word** makes a word bold."""
    words, x, space = [], 0.0, FONT.getlength(" ")
    for token in text.split(" "):
        bold = token.startswith("**") and token.endswith("**")
        token = token.strip("*")
        w = (FONT_BOLD if bold else FONT).getlength(token)
        words.append(Word(token, x, y, w, bold=bold))
        x += w + space
    return words
