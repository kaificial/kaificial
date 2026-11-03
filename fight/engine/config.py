"""Canvas size, loop length and fonts shared by the whole animation."""
from PIL import ImageFont

LOOP = 31.0          # length of one full loop, in seconds
EPS = 0.002          # a tiny time step, used to make instant jumps between keyframes
LEAD_TRIM = 0.25     # the whole film plays this much earlier, so the quiet opening is shorter

W, H = 830, 277      # canvas size
FLOOR = 272          # the ground the cats stand on
H1_Y, RULE_Y = 32, 50
P_Y = [84, 124, 164, 204]    # baselines of the four paragraph lines
BODY_Y = -17         # a cat spins around this point by default (roughly the middle of her body)

FONT_SIZE = 16
FONT_STACK = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

# Words are measured with Liberation Sans or Arial. Both have the same letter widths,
# so the layout comes out the same on Linux, macOS and Windows.
_REGULAR_FONTS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/liberation-sans/LiberationSans-Regular.ttf",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
]
_BOLD_FONTS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def _load_font(paths):
    for path in paths:
        try:
            return ImageFont.truetype(path, FONT_SIZE)
        except OSError:
            continue
    raise SystemExit("Couldn't find Liberation Sans or Arial. Install one of them (e.g. fonts-liberation) and try again.")


FONT = _load_font(_REGULAR_FONTS)
FONT_BOLD = _load_font(_BOLD_FONTS)
