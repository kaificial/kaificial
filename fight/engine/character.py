"""A character: a stick figure in a cat costume, moved around by keyframe tracks."""
import math

from .config import LOOP, EPS, BODY_Y
from .poses import POSES, LIMBS, RUN_CYCLE, RUN_BOB, joint, sample_pose, limb_points
from .svg import (num, rnd, animate, animate_transform, fmt_xy, fmt_rotate, fmt_scale)
from .costumes import bone_angle
from .timeline import Track, eased, sample, sample_step, window
from .weapons import katana_svg, pick_svg


class Character:
    def __init__(self, costume, pose0="stand", pos0=(0, 0), face0=1):
        self.costume = costume
        self.pos = Track(tuple(map(float, pos0)))          # where her feet are
        self.rot = Track((0.0, 0.0, float(BODY_Y)))        # (angle, pivot x, pivot y)
        self.facing = Track(face0)                          # 1 faces right, -1 faces left
        self.squash = Track((1.0, 1.0))                     # squash and stretch (x, y)
        self.opacity = Track(0)
        self.pose_track = Track(pose0)
        self.katana_opacity = Track(0)
        self.pick_opacity = Track(0)

    # ---------------------------------------------------------------- moving around
    def at(self, t, x, y, ease="lin"):
        """Move to (x, y), arriving at time t."""
        self.pos.add(t, (float(x), float(y)), ease)

    def stay(self, t):
        """Stay where she is until time t."""
        self.pos.hold(t)

    def put(self, t, x, y):
        """Appear at (x, y) at time t, with no travel in between."""
        self.pos.set(t, (float(x), float(y)))

    def x(self, t=None):
        return self.pos.end_value[0] if t is None else sample(self.pos, t)[0]

    def jump(self, t0, t1, x1, y1, h, step=0.04):
        """An arc from where she is to (x1, y1), peaking h pixels up."""
        self.pos.hold(t0)
        x0, y0 = self.pos.end_value
        k = max(4, int(round((t1 - t0) / step)))
        for i in range(1, k + 1):
            s = i / k
            self.pos.add(t0 + (t1 - t0) * s, (x0 + (x1 - x0) * s, y0 + (y1 - y0) * s - 4 * h * s * (1 - s)))

    def run(self, t0, t1, x1, frame=0.06, ease="lin"):
        """Run to x1 using the run cycle, one frame every `frame` seconds."""
        self.pos.hold(t0)
        x0, y = self.pos.end_value
        t, i = t0, 0
        while t < t1 - 1e-6:
            self.pose(t, RUN_CYCLE[i % 6], tween=frame * 0.95, ease="inout")
            t += frame
            i += 1
            tt = min(t, t1)
            sx = eased((tt - t0) / (t1 - t0), ease)
            self.pos.add(tt, (x0 + (float(x1) - x0) * sx, y + RUN_BOB[i % 6]))
        self.pos.add(t1 + EPS, (float(x1), y))

    def jitter(self, t0, t1, amp, hz=24, amp1=None):
        """Shake in place. Pass amp1 to make the shake grow (or shrink) over time."""
        self.pos.hold(t0)
        x, y = self.pos.end_value
        t, i = t0, 0
        while t < t1 - 1 / hz:
            t += 1 / hz
            i += 1
            a = amp if amp1 is None else amp + (amp1 - amp) * (t - t0) / (t1 - t0)
            self.pos.add(t, (x + a * (rnd(i * 3.1) - 0.5) * 2, y + a * 0.5 * (rnd(i * 7.7) - 0.5) * 2))
        self.pos.add(t1, (x, y))

    # ---------------------------------------------------------------- body language
    def pose(self, t, name, tween=0.08, ease="out"):
        """Blend into pose `name` over `tween` seconds, landing on it at time t."""
        assert name in POSES, name
        self.pose_track.hold(t - tween)
        self.pose_track.add(t, name, ease)

    def idle(self, t0, t1, base="stand", period=0.5):
        """Breathe gently in a pose."""
        t, i = t0, 0
        while t < t1 - 1e-6:
            self.pose(t, base if i % 2 == 0 else base + "_b", tween=period * 0.9, ease="inout")
            t += period
            i += 1

    def face(self, t, direction):
        self.facing.set(t, direction)

    def spin(self, t0, t1, deg, ease="lin"):
        """Spin by `deg` degrees, then snap the angle back into -180..180."""
        self.rot.hold(t0)
        a, px, py = self.rot.end_value
        end = a + deg
        self.rot.add(t1, (end, px, py), ease)
        self.rot.add(t1 + EPS, (((end + 180) % 360) - 180, px, py))

    def rot_to(self, t0, t1, angle, ease="out", pivot=None):
        """Turn to an angle, optionally around a new pivot."""
        self.rot.hold(t0)
        _, px, py = self.rot.end_value
        if pivot is not None:
            px, py = pivot
            self.rot.add(t0 + EPS, (self.rot.end_value[0], float(px), float(py)))
        self.rot.add(t1, (float(angle), px, py), ease)

    def rot_pivot(self, t, px=0.0, py=float(BODY_Y)):
        """Move the rotation pivot without turning."""
        self.rot.hold(t)
        self.rot.add(t + EPS, (self.rot.end_value[0], float(px), float(py)))

    def wobble(self, t0, t1, deg, period=0.16, base=None):
        """Rock back and forth around her current angle (or `base`)."""
        self.rot.hold(t0)
        a0, px, py = self.rot.end_value
        if base is not None:
            a0 = base
        t, i = t0, 0
        while t < t1 - period / 2:
            t += period / 2
            i += 1
            self.rot.add(t, (a0 + (deg if i % 2 else -deg), px, py), "inout")
        self.rot.add(t1, (a0, px, py), "inout")

    def land(self, t, amount=0.26, pose="crouch"):
        """Squash on landing, then spring back."""
        self.squash.set(t, (1 + amount, 1 - amount))
        self.squash.add(t + 0.09, (0.95, 1.05), "out")
        self.squash.add(t + 0.17, (1.0, 1.0), "out")
        if pose:
            self.pose(t, pose, tween=0.03)

    def takeoff(self, t, amount=0.12):
        """Stretch up as she leaves the ground."""
        self.squash.hold(t - 0.05)
        self.squash.add(t, (1 - amount, 1 + amount), "out")
        self.squash.add(t + 0.1, (1.0, 1.0), "out")

    def hitstop(self, t, dur):
        """Freeze for a moment on impact, so the hit feels heavy."""
        for track in (self.pos, self.rot, self.pose_track, self.squash):
            track.hold(t)
            track.hold(t + dur)

    def show(self, t):
        self.opacity.set(t, 1)

    def hide(self, t):
        self.opacity.set(t, 0)

    def katana(self, t, on):
        self.katana_opacity.set(t, 1 if on else 0)

    def pickaxe(self, t, on):
        self.pick_opacity.set(t, 1 if on else 0)

    # ---------------------------------------------------------------- where things are
    def world(self, t, key):
        """Where one of her joints is on the page at time t."""
        x, y = joint(sample_pose(self.pose_track, t), key)
        facing = sample_step(self.facing, t)
        sqx, sqy = sample(self.squash, t)
        x, y = x * facing * sqx, y * sqy
        a, px, py = sample(self.rot, t)
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        dx, dy = x - px, y - py
        x, y = px + dx * ca - dy * sa, py + dx * sa + dy * ca
        fx, fy = sample(self.pos, t)
        return fx + x, fy + y

    def pose_at(self, t):
        return sample_pose(self.pose_track, t)

    # ---------------------------------------------------------------- drawing
    def svg(self, pal, opacity=None, armed=False, katana_window=(0, LOOP), pick_window=(0, LOOP)):
        """Draw her for one palette.

        opacity: use a different visibility track than her own (for the outline copy in space).
        armed: draw the katana and pickaxe too, each only animated inside its time window.
        """
        opacity = opacity or self.opacity
        costume = self.costume
        colour = pal[costume["body"]]

        # facing and squash both scale her, so fold them into one scale track
        scale = Track((float(self.facing.keys[0][1]), 1.0))
        for t in sorted({k[0] for k in self.facing.keys} | {k[0] for k in self.squash.keys}):
            if t == 0:
                continue
            qx, qy = sample(self.squash, t)
            scale.add(t, (sample_step(self.facing, t) * qx, qy))

        pose0 = POSES[self.pose_track.keys[0][1]]
        head_anim = (animate("cx", self.pose_track, lambda name: num(POSES[name]["H"][0]))
                     + animate("cy", self.pose_track, lambda name: num(POSES[name]["H"][1])))

        def stick_figure(col, width, head_r):
            parts = [f'<circle r="{head_r}" fill="{col}" cx="{num(pose0["H"][0])}" cy="{num(pose0["H"][1])}">' + head_anim + "</circle>"]
            for limb in LIMBS:
                parts.append(f'<polyline fill="none" stroke="{col}" stroke-width="{width}" stroke-linecap="round" '
                             f'stroke-linejoin="round" points="{limb_points(pose0, limb)}">'
                             + animate("points", self.pose_track, lambda name, limb=limb: limb_points(POSES[name], limb)) + "</polyline>")
            return "".join(parts)

        def pinned(joint_key, a, b, inner):
            """A group stuck to a joint that tilts with the bone a -> b."""
            if not inner:
                return ""
            return ('<g>' + animate_transform("translate", self.pose_track, lambda name: fmt_xy(POSES[name][joint_key]))
                    + '<g>' + animate_transform("rotate", self.pose_track, lambda name: num(bone_angle(POSES[name], a, b))) + inner + '</g></g>')

        out = [f'<g opacity="{opacity.keys[0][1]}">', animate("opacity", opacity, str), animate_transform("translate", self.pos, fmt_xy),
               "<g>", animate_transform("rotate", self.rot, fmt_rotate),
               "<g>", animate_transform("scale", scale, lambda v: f"{fmt_scale(v[0])} {fmt_scale(v[1])}")]
        out.append(pinned("P", "P", "N", costume["hips"](pal)))
        out.append(pinned("H", "N", "H", costume["head_back"](pal)))
        out.append(stick_figure(pal[costume["line"]], 4.3, 5.85))     # dark outline, so she reads on both themes
        out.append(stick_figure(colour, 2.6, 5))
        if costume["white_paws"]:
            paw = f'<circle r="1.55" fill="{pal["cat_paw"]}" stroke="{pal[costume["line"]]}" stroke-width="0.5"/>'
            for j in ("LH", "RH", "LF", "RF"):
                out.append(pinned(j, "N", "H", paw))
        out.append(pinned("N", "P", "N", costume["neck"](pal)))
        out.append(pinned("H", "N", "H", costume["head_front"](pal)))
        if armed:
            out.append('<g opacity="0">' + animate("opacity", self.katana_opacity, str)
                       + katana_svg(pal, window(self.pose_track, *katana_window)) + "</g>")
            out.append('<g opacity="0">' + animate("opacity", self.pick_opacity, str)
                       + pick_svg(pal, window(self.pose_track, *pick_window)) + "</g>")
        out.append("</g></g></g>")
        return "".join(out)
