"""The two cats, drawn over the stick figures.

Every piece (ears, face, tail, bib) is pinned to a joint and tilts with the bone it hangs off,
so it follows every pose for free. Pieces are drawn facing +x with the head centre at (0, 0),
radius 5; the character's own scale flips them when she turns around.
"""
import math


def bone_angle(pose, a, b):
    """The angle (degrees) of the bone from joint a to joint b, measured from straight up."""
    dx, dy = pose[b][0] - pose[a][0], pose[b][1] - pose[a][1]
    return math.degrees(math.atan2(dx, -dy))


def _sway(deg, dur, inner, pivot=(0, 0), phase=0.0):
    """A gentle endless back-and-forth for tails (it runs on its own clock, not the film's)."""
    px, py = pivot
    vals = f"{-deg} {px} {py};{deg} {px} {py};{-deg} {px} {py}"
    return (f'<g><animateTransform attributeName="transform" type="rotate" values="{vals}" dur="{dur}s" '
            f'begin="{phase}s" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" repeatCount="indefinite"/>{inner}</g>')


def cat_costume(kind):
    """kind "w" is Mochi, the white cat. kind "b" is Sesame, the black tuxedo cat."""
    is_black = kind == "b"
    body, line, eye, whisker = f"cat_{kind}", f"cat_{kind}_line", f"cat_{kind}_eye", f"cat_{kind}_whisk"

    def ears(p):
        st = f'stroke="{p[line]}" stroke-width="0.9" stroke-linejoin="round"'
        return (f'<path d="M-4.6,-2.4 L-5.4,-10.2 L-0.8,-4.9 Z" fill="{p[body]}" {st}/>'
                f'<path d="M0.4,-5 L4.2,-10.4 L4.9,-2.2 Z" fill="{p[body]}" {st}/>'
                f'<path d="M1.6,-5 L3.9,-8.4 L4.2,-4 Z" fill="{p["cat_nose"]}" opacity="0.75"/>')

    def face(p):
        if is_black:   # amber eyes with slit pupils
            eyes = (f'<ellipse cx="1.3" cy="-0.9" rx="1.05" ry="1.35" fill="{p[eye]}"/>'
                    f'<ellipse cx="3.9" cy="-1.1" rx="0.95" ry="1.3" fill="{p[eye]}"/>'
                    f'<path d="M1.3,-2 V0.2 M3.9,-2.2 V0" stroke="#000000" stroke-width="0.45" stroke-linecap="round"/>')
        else:          # round dark eyes with a little shine
            eyes = (f'<ellipse cx="1.3" cy="-0.9" rx="0.95" ry="1.25" fill="{p[eye]}"/>'
                    f'<ellipse cx="3.9" cy="-1.1" rx="0.85" ry="1.2" fill="{p[eye]}"/>'
                    f'<circle cx="1.6" cy="-1.4" r="0.35" fill="#ffffff"/><circle cx="4.15" cy="-1.6" r="0.32" fill="#ffffff"/>')
        mouth = p[whisker] if is_black else p[line]
        return (eyes + f'<path d="M4.6,0.9 L5.8,0.6 L5.3,1.6 Z" fill="{p["cat_nose"]}"/>'
                f'<path d="M5.2,1.7 Q4.6,2.6 3.9,2.2 M5.2,1.7 Q5.6,2.7 6.3,2.3" fill="none" stroke="{mouth}" stroke-width="0.4" stroke-linecap="round"/>'
                f'<path d="M5.4,1.5 L10.4,0.4 M5.4,2 L10.6,2.4 M5.2,2.4 L9.6,4.2" stroke="{p[whisker]}" stroke-width="0.35" stroke-linecap="round"/>')

    def tail(p):
        d = "M-0.8,-1.5 C-6.5,-0.5 -10,-4.5 -9.2,-10 C-8.8,-13.2 -11.2,-15.2 -13.2,-13.4"
        inner = (f'<path d="{d}" fill="none" stroke="{p[line]}" stroke-width="3.8" stroke-linecap="round"/>'
                 f'<path d="{d}" fill="none" stroke="{p[body]}" stroke-width="2.2" stroke-linecap="round"/>')
        if is_black:   # white tip on the tail
            inner += f'<path d="M-9.9,-13.6 C-10.6,-14.6 -12,-14.8 -13.2,-13.4" fill="none" stroke="{p["cat_paw"]}" stroke-width="1.6" stroke-linecap="round"/>'
        return _sway(12, 0.85 if is_black else 0.7, inner, (-0.8, -1.5), 0.4 if is_black else 0.15)

    def bib(p):
        if not is_black:
            return ""
        return f'<ellipse cx="0.6" cy="3.6" rx="1.7" ry="3" fill="{p["cat_paw"]}"/>'

    return dict(body=body, line=line, head_back=ears, head_front=face, neck=bib, hips=tail, white_paws=is_black)
