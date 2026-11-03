"""Reusable fight moves built from character tracks and effects."""
from .camera import jolt
from .config import W
from .effects import flash, impact_lines, spark
from .svg import rnd
from .timeline import sample


def hit(t, x, y, size, *chars, big=False, dur=None, shake=None):
    """A landed hit at (x, y): a spark, a short freeze on everyone involved, and a camera knock.

    Big hits also get an impact frame and a flash. Returns the time the freeze ends.
    """
    dur = dur or (0.09 if big else 0.06)
    spark(x, y, t, size)
    for c in chars:
        c.hitstop(t, dur)
    if big:
        impact_lines(x, y, t)
        flash(t, 0.07, 0.75)
    jolt(t, shake if shake is not None else (3 if big else 1.5))
    return t + dur


def heavy_slash(c, t_contact, big=True):
    """A committed overhead cut: slow wind-up, raise, snap down, follow through, slow recovery.

    The caller adds the slash arc and the cut itself at t_contact.
    """
    c.pose(t_contact - 0.30, "sw_wind", 0.16, "inout")
    c.pose(t_contact - 0.09, "sw_up", 0.13, "in")
    c.pose(t_contact, "sw_down", 0.045, "snap")
    c.pose(t_contact + 0.07, "sw_thru", 0.07, "out")
    c.squash.hold(t_contact - 0.001)
    c.squash.add(t_contact + 0.05, (1.08, 0.94), "out")      # her weight drops into the cut
    c.squash.add(t_contact + 0.22, (1.0, 1.0), "inout")
    c.pose(t_contact + 0.3, "sw_rec", 0.2, "inout")
    c.pose(t_contact + 0.55, "sw_idle", 0.22, "inout")
    if big:
        jolt(t_contact, 1.2)


def heavy_upswing(c, t_contact):
    """A rising cut. The blade starts low and behind, sweeps up through the target and ends
    overhead, which is exactly where the next overhead cut starts."""
    c.pose(t_contact - 0.28, "sw_low", 0.16, "inout")
    c.pose(t_contact + 0.04, "sw_upcut", 0.1, "snap")
    c.pose(t_contact + 0.14, "sw_upthru", 0.1, "out")
    c.squash.hold(t_contact - 0.001)
    c.squash.add(t_contact + 0.05, (0.94, 1.08), "out")      # she rises into it
    c.squash.add(t_contact + 0.22, (1.0, 1.0), "inout")
    jolt(t_contact, 1.2)


def blade_cut_point(c, t, word):
    """Where the blade (paw to tip) crosses the word's middle at time t."""
    (hx, hy), (tx, ty) = c.world(t, "RH"), c.world(t, "WT")
    if abs(ty - hy) < 1e-6:
        return (tx, word.cy)
    k = (word.cy - hy) / (ty - hy)
    return (hx + (tx - hx) * k, word.cy)


def hop(c, t0, t1, x, y, h=14, land_amount=0.22):
    """A small jump from where she is to (x, y): crouch, take off, tuck, land."""
    c.pose(t0 - 0.06, "crouch", 0.06)
    c.takeoff(t0)
    c.jump(t0, t1, x, y, h)
    c.pose(t0 + 0.05, "tuck", 0.05)
    c.pose(t1 - 0.06, "fall", 0.06)
    c.land(t1, land_amount)


def carry(c, holder, paw_key, t0, t1, dx):
    """c dangles from holder's paw by the scruff, following every move the holder makes."""
    c.stay(t0)
    t = t0
    while t < t1 - 1e-6:
        t = min(t1, t + 0.03)
        hx, hy = holder.world(t, paw_key)
        c.pos.add(t, (hx + dx, hy + 26))


def float_debris(words, t0, t_up, t_blast, cx):
    """Words lying on the floor lift off and hover during a power-up, then get blasted away from cx."""
    for i, word in enumerate(words):
        bx, by = sample(word.offset, t0)
        r0 = sample(word.rot, t0)
        lift = 22 + 26 * rnd(i + 70)
        word.offset.hold(t0 + 0.04 * i)
        word.offset.add(t_up + 0.03 * i, (bx, by - lift), "out")
        word.rot.hold(t0 + 0.04 * i)
        word.rot.add(t_up + 0.03 * i, r0 + (rnd(i + 9) - 0.5) * 40, "out")
        for k in range(3):
            word.offset.add(t_up + 0.03 * i + 0.12 * (k + 1), (bx + (rnd(i * 3 + k) - 0.5) * 3, by - lift + (2 if k % 2 else -2)), "inout")
        word.offset.hold(t_blast)
        side = 1 if word.cx + bx > cx else -1
        dist = 70 + 60 * rnd(i + 31)
        ex = max(10.0, min(W - 10.0, word.cx + bx + side * dist)) - word.cx
        steps = 6
        for j in range(1, steps + 1):
            s = j / steps
            word.offset.add(t_blast + 0.4 * s, (bx + (ex - bx) * s, (by - lift) + (by - (by - lift)) * s - 30 * 4 * s * (1 - s)))
        word.rot.hold(t_blast)
        word.rot.add(t_blast + 0.4, r0 + side * (120 + 90 * rnd(i)))
