"""Act 2 (3.8 - 6.9 s): Sesame drops in on a web, yanks a word off the page and throws it.
Mochi draws her katana and cuts it in half in mid-air."""
import math

from engine.config import EPS, FLOOR, BODY_Y
from engine.camera import jolt
from engine.effects import crescent, dust, fixed, paw, spark, strand
from engine.moves import heavy_slash, hit
from engine.timeline import sample

from .cast import mochi, sesame
from .page import word


def play():
    _spider_drop()
    _web_yank()


def _spider_drop():
    """She lowers in upside down from the top of the page, waves, and flips the right way up."""
    anchor = (440.0, -2.0)
    sesame.rot.keys[0][1] = (180.0, 0.0, 0.0)     # she starts hanging by her feet
    sesame.face(0, -1)
    sesame.show(3.8)
    sesame.stay(3.8)
    sesame.at(4.2, 440, 136, "out")
    sesame.at(4.32, 440, 124, "inout")
    sesame.at(4.44, 440, 133, "inout")
    sesame.at(4.56, 440, 130, "inout")
    strand(fixed(anchor), lambda t: sample(sesame.pos, t), 3.8, 5.0, "web", 1.0, shoot=0.01, knot=False)
    mochi.face(4.3, 1)
    mochi.pose(4.36, "guard", 0.1)
    sesame.pose(4.6, "wave1", 0.1)
    sesame.pose(4.72, "wave2", 0.08)
    sesame.pose(4.84, "wave1", 0.08)

    # lets go and flips over on the way down
    sesame.pose(5.0, "tuck", 0.06)
    sesame.jump(5.0, 5.34, 452, FLOOR, 4)
    sesame.rot.hold(5.0)
    sesame.rot.add(5.3, (360.0, 0.0, 0.0), "out")
    sesame.rot.add(5.3 + EPS, (0.0, 0.0, float(BODY_Y)))
    sesame.pose(5.28, "fall", 0.05)
    sesame.land(5.34, 0.26)
    dust(452, FLOOR, 5.34)
    sesame.pose(5.5, "stand", 0.1)


def _web_yank():
    """She snags "University." with a web, whirls it around and hurls it at Mochi."""
    uni = word(1, "University.")
    sesame.pose(5.62, "punch", 0.05, "snap")
    strand(paw(sesame), uni.pos, 5.62, 6.42, "web", 1.0)
    spark(*uni.pos(5.7), 5.7, 6)
    sesame.pose(5.76, "tug2", 0.06, "snap")
    jolt(5.76, 1)

    centre = (452.0, 196.0)          # the middle of the whirl
    uni.offset.hold(5.7)
    uni.rot.hold(5.7)
    path = [(5.76, (uni.cx, uni.cy - 2), 0.0)]
    for i in range(1, 6):            # pulled in toward her
        s = i / 5
        path.append((5.76 + 0.16 * s, (uni.cx + (centre[0] + 48 - uni.cx) * s, uni.cy + (centre[1] - uni.cy) * s), 40 * s))
    for i in range(1, 15):           # one and a half turns around her
        a = 2 * math.pi * 1.5 * i / 14
        path.append((5.92 + 0.46 * i / 14, (centre[0] + 48 * math.cos(a), centre[1] - 34 * math.sin(a)), 40 + 540 * i / 14))
    uni.move_through(path)
    sesame.pose(6.0, "windup", 0.1)
    sesame.pose(6.2, "windup2", 0.1)
    sesame.pose(6.4, "mega", 0.05, "snap")

    # Mochi draws and cuts it out of the air
    mochi.pose(5.98, "sw_draw", 0.08)
    mochi.katana(6.02, True)
    spark(mochi.x() - 6, 236, 6.08, 5, kind="white")
    mochi.pose(6.16, "sw_idle", 0.1)
    x0, y0 = uni.pos(6.38)
    t_cut = 6.66
    cut_x, cut_y = mochi.x() + 20, FLOOR - 28
    uni.move_through([(6.38 + 0.28 * i / 6, (x0 + (cut_x - x0) * i / 6, y0 + (cut_y - y0) * i / 6 - 18 * math.sin(math.pi * i / 6)), 580 + 120 * i / 6)
                      for i in range(1, 7)])
    heavy_slash(mochi, t_cut)
    uni.slice(t_cut, -30, fall=((-40, 160), (30, -140)), through=(cut_x, cut_y))
    crescent(mochi.x() + 6, FLOOR - 22, 26, -80, 60, t_cut)
    hit(t_cut, cut_x, cut_y, 10, mochi, big=True)
