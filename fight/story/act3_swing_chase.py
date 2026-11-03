"""Act 3 (6.9 - 9.2 s): Sesame web-swings across the page. Mochi chases her up through the lines,
cutting words on the way, and Sesame zips up onto the rule under the heading."""
import math

from engine.config import RULE_Y
from engine.effects import crescent, fixed, paw, spark, strand
from engine.moves import blade_cut_point, heavy_slash, heavy_upswing

from .cast import mochi, sesame
from .page import on_top, word


def play():
    _swing()
    _chase()
    _zip_away()


def _swing():
    anchor = (330.0, float(RULE_Y))
    sesame.pose(6.92, "point", 0.06, "snap")
    sesame.stay(7.0)
    for i in range(1, 17):
        s = i / 16
        angle = math.radians(63 + 87 * (s * s * (3 - 2 * s)))
        radius = 248 - 98 * s
        x, y = anchor[0] + radius * math.cos(angle), anchor[1] + radius * math.sin(angle)
        sesame.at(7.0 + 0.62 * s, x, y + 26)       # her paw is on the strand, her feet hang below it
    sesame.pose(7.02, "fly", 0.06)
    strand(paw(sesame), fixed(anchor), 6.95, 7.62, "web", 1.0)
    # lets go, flips, and lands on the second line
    sesame.pose(7.62, "tuck", 0.05)
    sesame.jump(7.62, 7.95, 92, on_top(1), 26)
    sesame.spin(7.64, 7.92, 360)
    sesame.land(7.95, 0.2)
    sesame.face(7.96, 1)
    sesame.pose(8.08, "hips", 0.1)


def _chase():
    """Mochi runs and jumps up after her, cutting "solutions," on the way up."""
    solutions = word(2, "solutions,")
    mochi.pose(7.06, "sw_idle", 0.12)
    mochi.run(7.1, 7.42, 205, frame=0.07)
    mochi.pose(7.44, "crouch", 0.04)
    mochi.takeoff(7.48)
    mochi.jump(7.48, 7.86, 262, on_top(2), 40)
    heavy_upswing(mochi, 7.74)
    solutions.slice(7.74, 35, through=blade_cut_point(mochi, 7.74, solutions))
    spark(solutions.cx, solutions.cy, 7.74, 7)
    mochi.land(7.86, 0.2, pose=None)
    mochi.pose(7.95, "sw_idle", 0.1)
    mochi.face(7.98, -1)
    mochi.pose(8.06, "crouch", 0.05)
    mochi.takeoff(8.1)
    mochi.jump(8.1, 8.42, 140, on_top(1), 34)
    mochi.pose(8.16, "tuck", 0.05)
    mochi.land(8.42, 0.18, pose=None)
    heavy_slash(mochi, 8.72)


def _zip_away():
    """Sesame zips out of the way at the last moment, and the cut hits "based" instead."""
    based = word(1, "based")
    sesame.pose(8.5, "point", 0.05, "snap")
    strand(paw(sesame), fixed((44.0, 8.0)), 8.5, 8.74, "web", 1.0, shoot=0.05)
    sesame.pose(8.56, "fly", 0.05)
    sesame.at(8.74, 40, RULE_Y, "in")
    sesame.land(8.76, 0.2)
    based.slice(8.72, -28, through=(based.cx - 4, based.cy))
    crescent(mochi.x() - 14, on_top(1) - 18, 24, 120, 250, 8.72)
    sesame.pose(8.95, "hips", 0.1)
    sesame.idle(8.95, 9.35, "hips", 0.2)
