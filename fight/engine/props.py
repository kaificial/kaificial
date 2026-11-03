"""Props: anything thrown, conjured or carried that isn't a cat or a word."""
from .layers import layer
from .svg import fmt_xy, fmt_uniform_scale, fade_group, transform_group
from .timeline import Track


class Prop:
    """A drawing with its own position, scale and opacity tracks. It starts hidden."""

    def __init__(self, draw, x=0.0, y=0.0, layer_name="front"):
        self.pos = Track((float(x), float(y)))
        self.scale = Track(1.0)
        self.opacity = Track(0)
        self.draw = draw
        layer(layer_name, self.svg)

    def svg(self, p):
        return (fade_group(self.opacity) + transform_group("translate", self.pos, fmt_xy)
                + transform_group("scale", self.scale, fmt_uniform_scale) + self.draw(p) + "</g></g></g>")
