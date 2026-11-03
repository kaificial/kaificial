# the fight

The top of the profile README looks like plain text, but it isn't. `fight-light.svg` and
`fight-dark.svg` are 31-second animated SVGs (pure SMIL, no JavaScript) that GitHub shows as-is.

Two original cats, Mochi (white, with a katana) and Sesame (a black tuxedo cat), fight their way
through the page with superhero and anime moves: a mining entrance, a web drop, a word yanked off
the page and cut in half, grapple wires and portals, a giant, a golden power-up that lifts the
fallen words, the @ grabbed as a ricochet shield, a beam clash, and an explosion that throws them
up into space. There, Sesame punches Mochi into a mountain, pounds her deeper into the crater and
holds her up out of the rubble in a quiet, letterboxed beat. Sesame wins, spider style. No dialogue.

## Building

```
pip install pillow
python3 make_fight.py
```

This writes `fight-light.svg` and `fight-dark.svg` next to the script. You'll need Liberation Sans
or Arial installed (they have the same letter widths, so the layout comes out the same everywhere).

## How it's organised

```
make_fight.py          entry point: builds the fight and writes both SVGs
engine/                a small keyframe animation engine
  timeline.py          Track: a list of keyframes for one value
  svg.py               number formatting and <animate> tags
  character.py         a cat: position, pose, squash and stretch, drawing
  poses.py             the stick-figure poses
  costumes.py          the cat drawings layered over the poses
  weapons.py           the katana and the pickaxe
  words.py             one word on the page (it can fly, spin and be cut in half)
  effects/             sparks, smoke, lightning, webs, afterimages...
  moves.py             reusable moves: hits, sword swings, hops
  camera.py            screen shake and the pan up into space
  layers.py            draw order for effects
story/                 the fight itself
  page.py              the README text (edit it here)
  cast.py              Mochi and Sesame
  act1_mining.py ...   one file per act, in order
  act8_finale.py
  render.py            puts everything together into one SVG
```

The beat sheet with timings is at the top of `story/__init__.py`.

## Changing the text

Edit `H1_TEXT` and `PARAS` in `story/page.py`. The fight looks some words up by name
(`"University."`, `"solutions,"`, `"based"`, `"designing"`, `"new"`, `"technologies"`, `"@"`,
`"skills"` and `"forward!"`), so keep those on the same lines or update the lookups in the acts.

Every word is its own `<text>`, so the fight can yank, slice, sweep and put back individual words.
Each word is centred in the slot it was measured for, so it keeps its natural shape in whatever
font the viewer has, and the line layout stays the same on every OS.
