"""Act 1 (0.6 - 3.8 s): Mochi mines her way out of the page from behind."""
from engine.config import EPS, FLOOR
from engine.effects import dust, flash, poof
from engine.moves import hop

from . import tunnel
from .cast import mochi, mochi_digging
from .page import FORWARD, SKILLS_LETTERS


def play():
    tunnel.build()

    # She swings the pickaxe once for every crack stage of the first block, then once per block.
    mochi_digging.squash.set(0, (0.72, 0.72))     # she's further back, inside the page, so she looks smaller
    mochi_digging.face(0, -1)
    mochi_digging.pickaxe(0, True)
    mochi_digging.show(0.7)
    swings = tunnel.BLOCKS[0]["stages"] + [block["stages"][0] for block in tunnel.BLOCKS[1:]]
    for t in swings:
        mochi_digging.pose(t - 0.05, "dig_up", 0.06, "out")
        mochi_digging.pose(t, "dig_down", 0.04, "snap")
    mochi_digging.pose(2.45, "dig_hold", 0.12)

    # "forward!" rattles, then pops off the page when the first block breaks
    FORWARD.shake(0.8, 1.32, 0.9)
    FORWARD.fly(1.38, 2.05, 640, FLOOR - 6, 165, 70, bounce=(16, 0.2, 8))
    for letter in SKILLS_LETTERS:
        letter.shake(1.1, 1.36, 0.6)
    flash(1.38, 0.06, 0.35)

    # Swap to the real Mochi: she steps out of the dark toward us, growing to full size.
    mochi_digging.hide(2.6)
    mochi.squash.set(0, (0.72, 0.72))
    mochi.face(0, -1)
    mochi.pose(0, "dig_hold", EPS)
    mochi.pickaxe(0, True)
    mochi.show(2.6)
    mochi.stay(2.6)
    mochi.squash.add(2.85, (1.0, 1.0), "out")
    mochi.at(2.85, 162, tunnel.FLOOR_Y, "out")
    mochi.pose(2.85, "stand", 0.2)
    mochi.face(2.98, 1)
    mochi.face(3.08, -1)
    hop(mochi, 3.12, 3.42, 110, FLOOR, 18)
    dust(110, FLOOR, 3.42)

    # puts the pickaxe away and dusts herself off
    mochi.pose(3.56, "dig_hold", 0.1)
    mochi.pickaxe(3.62, False)
    poof(*mochi.world(3.6, "WT"), 3.62, 0.6)
    mochi.pose(3.66, "dust", 0.08)
    mochi.pose(3.76, "dust2", 0.06)
    mochi.pose(3.86, "hips", 0.1)
