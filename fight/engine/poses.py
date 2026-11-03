"""Stick-figure poses for the cats.

Each pose is a set of joints in the cat's own space: feet at (0, 0), up is -y, facing +x.
  H head, N neck, P hips, LE/RE elbows, LH/RH paws, LK/RK knees, LF/RF feet
  WT weapon tip (the katana's point, or the head of the pickaxe), only in weapon poses
"""
from .svg import num
from .timeline import segment

POSES = {
    "stand":  dict(H=(0, -30), N=(0, -25), P=(0, -13), LE=(-3, -18), LH=(-4, -11), RE=(3, -18), RH=(4, -11), LK=(-2, -6), LF=(-3, 0), RK=(2, -6), RF=(3, 0)),
    "guard":  dict(H=(1, -30), N=(0, -25), P=(0, -13), LE=(3, -19), LH=(6, -25), RE=(6, -21), RH=(9, -27), LK=(-4, -7), LF=(-6, 0), RK=(4, -7), RF=(6, 0)),
    # run cycle, leaning into it: contact, down (absorbing the landing), passing, up (pushing off)
    "runA":   dict(H=(5, -29), N=(4, -24), P=(0, -13), LE=(-5, -20), LH=(-10, -16), RE=(8, -21), RH=(13, -26), LK=(-6, -8), LF=(-12, -2), RK=(8, -8), RF=(12, 0)),
    "runD":   dict(H=(5, -27), N=(4, -22), P=(0, -12), LE=(-4, -18), LH=(-8, -13), RE=(7, -20), RH=(11, -24), LK=(-8, -7), LF=(-13, -5), RK=(4, -6), RF=(3, 0)),
    "runB":   dict(H=(5, -31), N=(4, -26), P=(0, -15), LE=(1, -21), LH=(2, -15), RE=(4, -22), RH=(6, -17), LK=(5, -10), LF=(2, -5), RK=(-2, -9), RF=(-4, -1)),
    "punch":  dict(H=(4, -29), N=(3, -24), P=(0, -13), LE=(-3, -20), LH=(1, -24), RE=(10, -25), RH=(18, -26), LK=(-6, -7), LF=(-9, 0), RK=(5, -6), RF=(8, 0)),
    "fkick":  dict(H=(-14, -24), N=(-9, -23), P=(0, -20), LE=(-13, -18), LH=(-18, -14), RE=(-10, -28), RH=(-16, -31), LK=(-4, -13), LF=(-8, -10), RK=(7, -20), RF=(16, -19)),
    "crouch": dict(H=(2, -20), N=(1, -16), P=(0, -8), LE=(-4, -11), LH=(-3, -5), RE=(5, -11), RH=(7, -6), LK=(-6, -6), LF=(-7, 0), RK=(6, -6), RF=(7, 0)),
    "hit":    dict(H=(-5, -28), N=(-3, -24), P=(0, -13), LE=(-8, -30), LH=(-10, -36), RE=(2, -31), RH=(0, -37), LK=(2, -8), LF=(5, -2), RK=(-4, -7), RF=(-7, 0)),
    "tuck":   dict(H=(4, -24), N=(2, -20), P=(0, -12), LE=(6, -16), LH=(5, -10), RE=(7, -15), RH=(6, -9), LK=(7, -10), LF=(2, -6), RK=(8, -11), RF=(3, -7)),
    "lying":  dict(H=(-16, -5), N=(-11, -4), P=(0, -3), LE=(-7, -9), LH=(-3, -7), RE=(-10, -1), RH=(-6, 0), LK=(6, -6), LF=(12, -7), RK=(7, -1), RF=(14, 0)),
    "fall":   dict(H=(0, -30), N=(0, -25), P=(0, -13), LE=(-6, -30), LH=(-8, -37), RE=(6, -30), RH=(8, -37), LK=(-3, -7), LF=(-5, -1), RK=(3, -7), RF=(5, -1)),
    "hips":   dict(H=(0, -30), N=(0, -25), P=(0, -13), LE=(-6, -19), LH=(-2, -14), RE=(6, -19), RH=(2, -14), LK=(-2, -6), LF=(-3, 0), RK=(2, -6), RF=(3, 0)),
    "point":  dict(H=(1, -30), N=(0, -25), P=(0, -13), LE=(-4, -19), LH=(-5, -12), RE=(8, -23), RH=(16, -24), LK=(-2, -6), LF=(-3, 0), RK=(2, -6), RF=(3, 0)),
    "dust":   dict(H=(0, -30), N=(0, -25), P=(0, -13), LE=(4, -20), LH=(7, -18), RE=(5, -19), RH=(8, -20), LK=(-2, -6), LF=(-3, 0), RK=(2, -6), RF=(3, 0)),
    "dust2":  dict(H=(0, -30), N=(0, -25), P=(0, -13), LE=(5, -19), LH=(8, -21), RE=(4, -21), RH=(7, -17), LK=(-2, -6), LF=(-3, 0), RK=(2, -6), RF=(3, 0)),
    "wave1":  dict(H=(0, -30), N=(0, -25), P=(0, -13), LE=(-3, -18), LH=(-4, -11), RE=(7, -30), RH=(9, -38), LK=(-2, -6), LF=(-3, 0), RK=(2, -6), RF=(3, 0)),
    "wave2":  dict(H=(0, -30), N=(0, -25), P=(0, -13), LE=(-3, -18), LH=(-4, -11), RE=(7, -30), RH=(13, -36), LK=(-2, -6), LF=(-3, 0), RK=(2, -6), RF=(3, 0)),
    "scratch": dict(H=(1, -30), N=(0, -25), P=(0, -13), LE=(-3, -18), LH=(-4, -11), RE=(6, -30), RH=(3, -36), LK=(-2, -6), LF=(-3, 0), RK=(2, -6), RF=(3, 0)),
    "windup": dict(H=(-4, -28), N=(-3, -23), P=(0, -13), LE=(3, -20), LH=(7, -23), RE=(-10, -26), RH=(-16, -24), LK=(-6, -7), LF=(-9, 0), RK=(5, -7), RF=(8, 0)),
    "windup2": dict(H=(-7, -27), N=(-6, -22), P=(-1, -13), LE=(4, -20), LH=(9, -24), RE=(-14, -25), RH=(-21, -21), LK=(-8, -6), LF=(-12, 0), RK=(6, -7), RF=(9, 0)),
    "mega":   dict(H=(8, -27), N=(6, -22), P=(0, -13), LE=(-6, -19), LH=(-10, -14), RE=(16, -24), RH=(26, -25), LK=(-8, -6), LF=(-13, 0), RK=(7, -6), RF=(10, 0)),
    "mega2":  dict(H=(10, -26), N=(8, -21), P=(1, -13), LE=(-6, -19), LH=(-10, -14), RE=(18, -23), RH=(28, -23), LK=(-8, -6), LF=(-13, 0), RK=(7, -6), RF=(10, 0)),
    "push":   dict(H=(6, -27), N=(5, -22), P=(0, -13), LE=(10, -20), LH=(16, -19), RE=(10, -23), RH=(16, -22), LK=(-6, -7), LF=(-10, 0), RK=(5, -7), RF=(8, 0)),
    "fly":    dict(H=(0, -31), N=(0, -26), P=(0, -14), LE=(-7, -27), LH=(-12, -31), RE=(7, -27), RH=(12, -31), LK=(-3, -8), LF=(-6, -2), RK=(2, -7), RF=(4, 0)),
    "tug2":   dict(H=(-10, -27), N=(-8, -23), P=(-1, -13), LE=(6, -20), LH=(14, -21), RE=(7, -23), RH=(14, -21), LK=(-7, -7), LF=(-10, 0), RK=(5, -7), RF=(8, 0)),
    # katana
    "sw_draw": dict(H=(0, -30), N=(0, -25), P=(0, -13), LE=(-3, -19), LH=(-4, -12), RE=(-4, -28), RH=(-6, -33), LK=(-2, -6), LF=(-3, 0), RK=(2, -6), RF=(3, 0), WT=(-16, -19)),
    "sw_idle": dict(H=(1, -30), N=(0, -25), P=(0, -13), LE=(-4, -20), LH=(-6, -14), RE=(6, -21), RH=(10, -19), LK=(-4, -7), LF=(-6, 0), RK=(4, -7), RF=(6, 0), WT=(26, -36)),
    "sw_wind": dict(H=(-6, -29), N=(-5, -24), P=(-2, -13), LE=(-2, -19), LH=(2, -15), RE=(-12, -27), RH=(-16, -34), LK=(-8, -7), LF=(-11, 0), RK=(3, -7), RF=(6, 0), WT=(-40, -30)),
    "sw_up":   dict(H=(-1, -30), N=(-1, -25), P=(0, -13), LE=(-5, -20), LH=(-3, -14), RE=(2, -31), RH=(4, -39), LK=(-4, -7), LF=(-6, 0), RK=(4, -7), RF=(6, 0), WT=(-13, -58)),
    "sw_down": dict(H=(6, -27), N=(5, -22), P=(1, -13), LE=(-4, -19), LH=(-7, -14), RE=(12, -20), RH=(18, -14), LK=(-7, -7), LF=(-10, 0), RK=(7, -7), RF=(10, 0), WT=(34, 2)),
    "sw_thru": dict(H=(10, -25), N=(8, -20), P=(2, -12), LE=(-2, -18), LH=(-5, -13), RE=(10, -15), RH=(12, -8), LK=(-8, -6), LF=(-12, 0), RK=(9, -6), RF=(13, 0), WT=(4, 12)),
    "sw_rec":  dict(H=(6, -27), N=(5, -22), P=(1, -13), LE=(-3, -19), LH=(-6, -13), RE=(8, -18), RH=(11, -12), LK=(-6, -7), LF=(-9, 0), RK=(6, -7), RF=(9, 0), WT=(20, 8)),
    # rising cut: the blade starts low and behind, sweeps up through the target and ends overhead
    "sw_low":    dict(H=(-3, -29), N=(-2, -24), P=(0, -13), LE=(-5, -20), LH=(-6, -15), RE=(2, -17), RH=(-2, -11), LK=(-5, -7), LF=(-8, 0), RK=(5, -7), RF=(8, 0), WT=(-20, 6)),
    "sw_upcut":  dict(H=(4, -29), N=(3, -24), P=(0, -13), LE=(-4, -20), LH=(-7, -15), RE=(10, -24), RH=(16, -22), LK=(-6, -7), LF=(-9, 0), RK=(6, -7), RF=(9, 0), WT=(40, -38)),
    "sw_upthru": dict(H=(1, -30), N=(0, -25), P=(0, -13), LE=(-4, -20), LH=(-6, -14), RE=(4, -33), RH=(2, -40), LK=(-4, -7), LF=(-6, 0), RK=(4, -7), RF=(6, 0), WT=(-18, -62)),
    # arm thrust straight out in front (firing a wire, a beam, or holding the blade out flat)
    "ww_cast":   dict(H=(3, -30), N=(2, -25), P=(0, -13), LE=(5, -20), LH=(11, -22), RE=(9, -22), RH=(16, -21), LK=(-5, -7), LF=(-8, 0), RK=(5, -7), RF=(8, 0), WT=(46, -20)),
    # pickaxe (WT is the head of the pick)
    "dig_hold": dict(H=(0, -30), N=(0, -25), P=(0, -13), LE=(-3, -18), LH=(-4, -11), RE=(5, -21), RH=(8, -27), LK=(-2, -6), LF=(-3, 0), RK=(2, -6), RF=(3, 0), WT=(-8, -44)),
    "dig_up":   dict(H=(-2, -30), N=(-1, -25), P=(0, -13), LE=(-4, -31), LH=(-6, -38), RE=(-3, -31), RH=(-5, -38), LK=(-3, -7), LF=(-5, 0), RK=(3, -7), RF=(5, 0), WT=(-16, -50)),
    "dig_down": dict(H=(4, -28), N=(3, -23), P=(0, -13), LE=(6, -20), LH=(12, -12), RE=(7, -21), RH=(13, -13), LK=(-5, -7), LF=(-8, 0), RK=(5, -7), RF=(8, 0), WT=(29, -1)),
}


def _mirror_limbs(pose):
    """Swap left and right limbs (the second half of the run cycle)."""
    q = dict(pose)
    for a, b in (("LE", "RE"), ("LH", "RH"), ("LK", "RK"), ("LF", "RF")):
        q[a], q[b] = pose[b], pose[a]
    return q


def _breathe_in(pose):
    """The same pose with the head and arms lifted a little, for idle breathing."""
    q = dict(pose)
    for k in ("H", "N"):
        q[k] = (pose[k][0], pose[k][1] - 1)
    for k in ("LE", "RE", "LH", "RH"):
        q[k] = (pose[k][0], pose[k][1] - 0.6)
    return q


for _name in ("runA", "runD", "runB"):
    POSES[_name + "2"] = _mirror_limbs(POSES[_name])
for _name in ("stand", "hips", "guard", "sw_idle", "point", "dig_hold", "fly", "ww_cast"):
    POSES[_name + "_b"] = _breathe_in(POSES[_name])

LIMBS = [("N", "P"), ("N", "LE", "LH"), ("N", "RE", "RH"), ("P", "LK", "LF"), ("P", "RK", "RF")]
RUN_CYCLE = ["runA", "runD", "runB", "runA2", "runD2", "runB2"]
RUN_BOB = [0, 1.2, -1.2, 0, 1.2, -1.2]       # how far she bobs on each run frame (down on contact, up on passing)


def joint(pose, key):
    """A joint's position. Poses without a weapon get a default tip above the right paw."""
    if key == "WT":
        return pose.get("WT", (pose["RH"][0] + 4, pose["RH"][1] - 22))
    return pose[key]


def blend(a, b, s):
    """A pose part way (s = 0..1) from pose a to pose b."""
    return {k: (joint(a, k)[0] + (joint(b, k)[0] - joint(a, k)[0]) * s,
                joint(a, k)[1] + (joint(b, k)[1] - joint(a, k)[1]) * s)
            for k in set(a) | set(b) | {"WT"}}


def sample_pose(track, t):
    """The exact (blended) pose a pose track shows at time t."""
    k0, k1, s = segment(track.keys, t)
    return blend(POSES[k0[1]], POSES[k1[1]], s)


def limb_points(pose, limb):
    return " ".join(f"{num(joint(pose, k)[0])},{num(joint(pose, k)[1])}" for k in limb)
