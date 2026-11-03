"""The two cats."""
from engine.character import Character
from engine.costumes import cat_costume

# Sesame, the black tuxedo cat. She wins.
sesame = Character(cat_costume("b"), "fall", (440, -40))

# Mochi, the white cat with the katana.
mochi = Character(cat_costume("w"), "stand", (170, 214))

# Mochi again, while she's still inside the page digging out. This copy is only visible
# through the blocks that are already broken.
mochi_digging = Character(cat_costume("w"), "dig_hold", (170, 214))
