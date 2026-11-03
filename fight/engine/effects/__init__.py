"""Visual effects. Each one registers itself on a draw layer when you call it."""
from .afterimages import ghost, trail
from .energy import aura, bolt, orb_draw, portal
from .impacts import crescent, flash, impact_frame, impact_lines, ring, smear_line, spark, speed_lines, tint
from .lines import fixed, paw, strand, tingle, web_splat
from .smoke import dust, floor_crack, poof, steam

__all__ = [
    "ghost", "trail",
    "aura", "bolt", "orb_draw", "portal",
    "crescent", "flash", "impact_frame", "impact_lines", "ring", "smear_line", "spark", "speed_lines", "tint",
    "fixed", "paw", "strand", "tingle", "web_splat",
    "dust", "floor_crack", "poof", "steam",
]
