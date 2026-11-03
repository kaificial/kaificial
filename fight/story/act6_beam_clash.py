"""Act 6 (16.95 - 18.2 s): the beam clash.

Sesame charges a blue beam between her paws; Mochi answers with a golden beam off her blade.
The point where they meet pushes back and forth, the page rumbles, and it all explodes.
"""
import math
from dataclasses import dataclass

from engine.camera import jolt, rumble
from engine.effects import aura, orb_draw, spark
from engine.layers import layer
from engine.props import Prop
from engine.svg import num, rnd, animate, animate_transform, fmt_xy, fade_group, transform_group
from engine.timeline import Track

from .cast import mochi, sesame


@dataclass
class Clash:
    t_beam: float       # the beams fire
    t_boom: float       # the explosion
    x: float            # where the beams meet
    y: float


def play(t_start):
    mochi.pose(t_start + 0.1, "sw_draw", 0.1)
    mochi.katana(t_start + 0.14, True)
    mochi.pose(t_start + 0.3, "sw_wind", 0.14)
    sesame.pose(t_start, "windup2", 0.14, "inout")
    charge_at = sesame.world(t_start + 0.05, "RH")
    charge = Prop(orb_draw("blue", "blue_hi", 4.0))
    charge.pos.set(t_start, (charge_at[0], charge_at[1]))
    charge.opacity.set(t_start, 1)
    charge.scale.keys[0][1] = 0.2
    charge.scale.hold(t_start)
    charge.scale.add(t_start + 0.45, 1.6, "in")
    _gathering_sparks(charge_at, t_start)
    aura(mochi, t_start + 0.3, t_start + 1.05, "blue_hi", "flash", fade=0.2, size=0.9, peak=0.8)

    t_beam = t_start + 0.5
    t_boom = t_beam + 0.55
    sesame.pose(t_beam, "push", 0.04, "snap")
    mochi.pose(t_beam + 0.04, "ww_cast", 0.05, "snap")      # blade thrust straight out; the beam leaves her paw
    jolt(t_beam + 0.04, 1.2)
    charge.opacity.set(t_beam, 0)

    blue_src = sesame.world(t_beam + 0.01, "RH")
    gold_src = mochi.world(t_beam + 0.05, "RH")
    beam_y = (blue_src[1] + gold_src[1]) / 2
    middle = (blue_src[0] + gold_src[0]) / 2
    # the meeting point slams to the middle, then see-saws back and forth until it blows
    clash = Track((blue_src[0], beam_y))
    clash.hold(t_beam)
    clash.add(t_beam + 0.08, (middle, beam_y), "out")
    for k in range(5):
        clash.add(t_beam + 0.08 + 0.09 * (k + 1), (middle + (12 if k % 2 else -12), beam_y), "inout")
    clash.add(t_boom, (middle, beam_y), "inout")
    _beams(blue_src, gold_src, beam_y, clash, t_beam, t_boom)

    rumble(t_beam + 0.05, t_boom, 1.5, 4)
    for k in range(4):
        spark(middle + (rnd(k) - 0.5) * 30, beam_y + (rnd(k + 4) - 0.5) * 20, t_beam + 0.12 + 0.1 * k, 6)
    sesame.jitter(t_beam + 0.06, t_boom, 0.6)
    mochi.jitter(t_beam + 0.3, t_boom, 0.6)
    return Clash(t_beam, t_boom, middle, beam_y)


def _gathering_sparks(at, t_start):
    """Little specks of energy get sucked into her paws while she charges."""
    def svg(p):
        out = []
        for i in range(10):
            a = 2 * math.pi * i / 10
            t0 = t_start + 0.04 * i
            tr, op = Track((42 * math.cos(a), 42 * math.sin(a))), Track(0)
            op.set(t0, 0.9)
            op.add(t0 + 0.22, 0, "in")
            tr.hold(t0)
            tr.add(t0 + 0.22, (0.0, 0.0), "in")
            out.append(f'<g transform="translate({num(at[0])},{num(at[1])})">' + fade_group(op) + transform_group("translate", tr, fmt_xy)
                       + f'<circle r="1.4" fill="{p["blue_hi"]}"/></g></g></g>')
        return "".join(out)
    layer("front", svg)


def _beams(blue_src, gold_src, beam_y, clash, t_beam, t_boom):
    def svg(p):
        op = Track(0)
        op.set(t_beam, 1)
        op.set(t_boom, 0)
        gold_tip = Track((gold_src[0], beam_y))
        gold_tip.hold(t_beam + 0.04)
        for t, v, ease in clash.keys[1:]:
            if t > t_beam + 0.04:
                gold_tip.add(t, v, ease)

        def fx(v):
            return num(v[0])
        blue = "".join(f'<line x1="{num(blue_src[0])}" y1="{num(blue_src[1])}" x2="{num(blue_src[0])}" y2="{num(beam_y)}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" opacity="{o}">'
                       + animate("x2", clash, fx) + "</line>" for c, w, o in ((p["blue"], 14, 0.3), (p["blue"], 7, 0.9), (p["bolt_core"], 2.5, 1)))
        gold = "".join(f'<line x1="{num(gold_src[0])}" y1="{num(gold_src[1])}" x2="{num(gold_src[0])}" y2="{num(beam_y)}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" opacity="{o}">'
                       + animate("x2", gold_tip, fx) + "</line>" for c, w, o in ((p["thunder"], 12, 0.3), (p["thunder"], 6, 0.9), (p["flash"], 2, 1)))
        ball = ('<g>' + animate_transform("translate", clash, fmt_xy) + '<g><animateTransform attributeName="transform" type="scale" values="1;1.25;0.9;1" dur="0.12s" repeatCount="indefinite"/>'
                f'<circle r="13" fill="{p["flash"]}" opacity="0.5"/><circle r="8" fill="{p["flash"]}" stroke="{p["thunder"]}" stroke-width="1.5"/></g></g>')
        return fade_group(op) + blue + gold + ball + "</g>"
    layer("front", svg)
