"""Act 5 (13.4 - 16.95 s): the power-up, the @ shield and the barrage.

Sesame powers up in a golden aura and the fallen words float up around her. Mochi grapples the
@ off the page and it grows into a shield that ricochets around the page. Sesame hammers it
with energy blasts until it's knocked away.
"""
import math

from engine.camera import jolt, rumble
from engine.config import FLOOR
from engine.effects import bolt, orb_draw, paw, ring, spark, strand, tint
from engine.moves import float_debris
from engine.props import Prop
from engine.svg import rnd
from engine.timeline import sample

from .act4_giant import GIANT_X
from .cast import mochi, sesame
from .page import FORWARD, word


def play():
    """Returns the time the beam clash (act 6) starts."""
    _power_up()
    shield = word(1, "@")
    _grab_shield(shield)
    return _barrage(shield)


def _power_up():
    mochi.katana(13.5, False)
    spark(mochi.x() + 6, FLOOR - 20, 13.5, 4, kind="white")
    mochi.face(13.5, 1)
    mochi.pose(13.52, "guard", 0.1)
    sesame.pose(13.7, "crouch", 0.14)
    sesame.jitter(13.9, 14.85, 0.2, amp1=1.4)
    t_burst = 14.85
    rumble(13.9, t_burst, 0.4, 2.6)
    for k, t in enumerate((14.1, 14.32, 14.52, 14.7)):     # little sparks of lightning crackle around her
        a = rnd(k + 3) * 2 * math.pi
        bolt(GIANT_X + 18 * math.cos(a), FLOOR - 20 + 14 * math.sin(a), GIANT_X + 30 * math.cos(a + 1), FLOOR - 26 + 22 * math.sin(a + 1),
             t, dur=0.12, col="thunder", core="bolt_core", w=1.2, jag=4, k=5, seed=60 + k, branch=False)

    # everything lying on the floor lifts off, hovers, and gets blasted away
    cut_words = (word(1, "University."), word(2, "solutions,"), word(1, "based"), word(0, "designing"))
    debris = [half for w in cut_words for half in (w.halves or [])] + [word(2, "technologies"), word(2, "new"), FORWARD]
    float_debris(debris, 13.95, 14.6, t_burst, GIANT_X)
    sesame.pose(t_burst, "fly", 0.06, "snap")
    tint(t_burst, "thunder", 0.4, 0.1)
    ring(GIANT_X, FLOOR - 18, t_burst, 110, col="thunder", w=3)
    ring(GIANT_X, FLOOR - 18, t_burst + 0.05, 160, col="thunder", w=1.2, dur=0.5)
    spark(GIANT_X, FLOOR - 20, t_burst, 14)
    jolt(t_burst, 5)
    sesame.pose(t_burst + 0.3, "guard", 0.12)


def _grab_shield(shield):
    """Mochi grapples the @ off the page and it grows into a shield. She throws it, and it bounces
    off Sesame's aura, the right wall and the heading before coming back to her."""
    mochi.pose(15.0, "ww_cast", 0.06, "snap")
    strand(paw(mochi, "RH"), shield.pos, 15.0, 15.24, "wire", 0.9, shoot=0.07)
    mochi.pose(15.14, "tug2", 0.05, "snap")
    shield.animated = True
    held_at = (mochi.x() + 16, FLOOR - 26)
    shield.offset.hold(15.14)
    shield.rot.hold(15.14)
    x0, y0 = shield.pos(15.14)
    shield.move_through([(15.14 + 0.2 * i / 6, (x0 + (held_at[0] - x0) * i / 6, y0 + (held_at[1] - y0) * i / 6 - 50 * math.sin(math.pi * i / 6)), 360 * i / 6)
                         for i in range(1, 7)])
    shield.scale.hold(15.14)
    shield.scale.add(15.34, 2.6, "out")
    mochi.pose(15.36, "guard", 0.06)

    mochi.pose(15.5, "punch", 0.04, "snap")
    bounces = [(15.64, (GIANT_X - 12, FLOOR - 30)), (15.84, (824.0, 118.0)), (16.06, (560.0, 22.0)), (16.3, held_at)]
    shield.move_through([(t, pt, 360 + 1440 * (t - 15.5) / 0.8) for t, pt in bounces])
    for t, (x, y) in bounces[:-1]:
        spark(x, y, t, 7)
        jolt(t, 1.2)
    ring(GIANT_X - 12, FLOOR - 30, 15.64, 26, col="thunder", w=2)
    sesame.wobble(15.64, 15.8, 3, 0.08)
    mochi.pose(16.3, "guard", 0.03, "snap")
    mochi.jitter(16.3, 16.36, 0.6)


def _barrage(shield):
    """Six quick energy blasts, each one caught on the shield and pushing Mochi back, until the
    last one knocks the shield away. Returns when the beam clash starts."""
    sesame.pose(16.42, "punch", 0.04, "snap")
    t, shield_x = 16.42, mochi.x()
    for k in range(6):
        paw_key = "RH" if k % 2 == 0 else "LH"
        sesame.pose(t, "punch" if k % 2 == 0 else "push", 0.03, "snap")
        hx, hy = sesame.world(t, paw_key)
        blast = Prop(orb_draw("thunder", "bolt_core", 3.0))
        blast.pos.set(t, (hx, hy))
        blast.opacity.set(t, 1)
        blast.pos.add(t + 0.13, (shield_x + 18, FLOOR - 26 + (rnd(k) - 0.5) * 8))
        blast.opacity.set(t + 0.13, 0)
        spark(shield_x + 18, FLOOR - 26, t + 0.13, 6)
        jolt(t + 0.13, 1)
        shield_x -= 5
        mochi.at(t + 0.18, shield_x, FLOOR, "out")
        shield.move_through([(t + 0.18, (shield_x + 16, FLOOR - 26), sample(shield.rot, t) + 6)])
        t += 0.09 if k < 5 else 0.0
    mochi.pose(t + 0.15, "hit", 0.03)
    shield.fly(t + 0.15, t + 0.65, shield_x - 70, FLOOR - 9, 300, 40)
    shield.scale.hold(t + 0.6)
    shield.scale.add(t + 0.65, 1.6, "in")
    return t + 0.3
