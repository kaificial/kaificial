"""The README text the fight happens on. Edit H1_TEXT and PARAS to change what it says.

The fight looks words up by name with word(line, text), so if you change the copy, keep these
words on the same lines (or update the lookups in the acts): "University.", "solutions,",
"based", "designing", "new", "technologies", "@", "skills" and "forward!".
"""
from engine.config import FONT, P_Y
from engine.words import Word, layout

H1_TEXT = "Hi, I'm Kai!"
PARAS = [
    "I enjoy designing and building reliable software.",
    "Currently based in Toronto, ON studying CS @ **Queen's** **University.**",
    "From algorithms to full stack solutions, I love exploring new technologies",
    "that push my skills forward!",
]

LINES = [layout(text, P_Y[i]) for i, text in enumerate(PARAS)]


def word(line, text):
    """The word on line `line` (0-based) whose text is exactly `text`."""
    for w in LINES[line]:
        if w.text == text:
            return w
    raise KeyError(text)


def _split_into_letters(w):
    letters, x = [], w.x
    for ch in w.text:
        width = FONT.getlength(ch)
        letters.append(Word(ch, x, w.y, width, centred=False))
        x += width
    return letters


# "skills" shakes letter by letter while Mochi digs right under it.
_skills = word(3, "skills")
SKILLS_LETTERS = _split_into_letters(_skills)
LINES[3].remove(_skills)

# "forward!" sits on top of the tunnel. It's drawn after the tunnel so it can pop off the page.
FORWARD = word(3, "forward!")
LINES[3].remove(FORWARD)


def all_words():
    """Every word that can move, in drawing order."""
    return [w for line in LINES for w in line] + SKILLS_LETTERS + [FORWARD]


def on_top(line):
    """The y a cat's feet are at when she stands on top of a line of text."""
    return P_Y[line] - 12
