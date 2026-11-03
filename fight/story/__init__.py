"""The fight, act by act. Times are in seconds (the finished film plays LEAD_TRIM earlier).

 0.6  Mining. A 3x3 patch of the page under "forward!" cracks open: Mochi is mining it from
      behind. "forward!" pops off, she steps out, and the blocks click back into place.
 3.8  Web drop. Sesame lowers in upside down on a web from the top of the page and waves.
 5.6  Web yank. She snags "University." on a strand, whirls it around and throws it. Mochi draws
      her katana and cuts it in half in mid-air.
 6.9  Swing chase. Sesame swings across the page, Mochi chases her up through the lines, cutting
      "solutions," and "based", and Sesame zips up onto the rule under the heading.
 9.2  Grapple wires and portals. Mochi wires into the heading and spins through "designing".
      Sesame steps through a ring of sparks and out of another one on the right of the page.
 9.8  The giant. Lightning, steam, and a giant Sesame sweeps "new technologies" off the page.
      Mochi wires over her head and cuts the back of her neck; the giant shrinks back down.
13.7  Power-up. A golden aura; the words on the floor float up, hover, then blast away.
15.0  The @ shield. Mochi grapples the @ off the page and it grows into a shield. It ricochets
      around the page and comes back, then a barrage of energy blasts knocks it away.
17.2  Beam clash. Sesame's blue beam against Mochi's golden one. It explodes.
18.3  Into space. The camera follows them up; the page slides out of frame under a starry sky.
19.3  The mountain. Sesame punches Mochi into a mountainside and pounds her deeper into the
      crater. Black bars slide in as she holds her up by the scruff. Then she lets go.
23.3  Back on the page. Mochi tries one last flying kick; Sesame backflips over it, webs her up
      and hangs her from the rule in a cocoon.
25.7  Sesame web-yanks every word back into place, salutes and swings away.
28.2  The strand snaps, the cocoon drops back into the tunnel, and the loop starts over.

The fight scenes are homages to fight tropes, drawn with two original cats. No characters,
logos or designs from any franchise are used.
"""
from dataclasses import dataclass

from . import (act1_mining, act2_web_drop, act3_swing_chase, act4_giant, act5_power_up,
               act6_beam_clash, act7_into_space, act8_finale)


@dataclass
class Timings:
    beam: float
    boom: float
    pan_up: float
    pan_down: float
    landed: float


def build():
    """Run the whole choreography, in order. Returns the key moments the renderer needs."""
    act1_mining.play()
    act2_web_drop.play()
    act3_swing_chase.play()
    act4_giant.play()
    clash_start = act5_power_up.play()
    clash = act6_beam_clash.play(clash_start)
    space = act7_into_space.play(clash)
    act8_finale.play(space.landed)
    return Timings(clash.t_beam, clash.t_boom, space.pan_up, space.pan_down, space.landed)
