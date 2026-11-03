"""Draw layers. Effects register a draw function here, and the renderer calls them in order.

Each draw function takes a palette and returns an SVG string, so one choreography can be drawn
in both the light and the dark theme.

  tunnel   the blocks Mochi mines through, drawn on the page
  page     on the page itself; it scrolls away with the page when the camera pans up
  behind   behind the cats, fixed to the screen
  front    in front of the cats
  overlay  over everything: full-screen flashes, the black letterbox bars
"""
LAYERS = {name: [] for name in ("tunnel", "page", "behind", "front", "overlay")}


def layer(name, draw):
    LAYERS[name].append(draw)


def draw_layer(name, palette):
    return [draw(palette) for draw in LAYERS[name]]
