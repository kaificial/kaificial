"""Colours for the light and dark themes. They match GitHub's own light and dark page colours."""

# Space colours, the same in both themes.
_SKY = dict(moon="#f2efe4", moon_dark="#252c52", limb="#0e1a44", limb_glow="#8fd0ff")

PALETTES = {
    "light": dict(
        _SKY,
        bg="#ffffff", fg="#1f2328", rule="#d1d9e0", red="#cf222e",
        blade="#d6dbe0", blade_edge="#6b7580", hamon="#ffffff", tsuba="#8a6d2f", wrap="#2b2b2b",
        void_fg="#f0f0ff", smoke="#8c959f", flash="#ffffff", crack="#9ea5ad", wood="#7a5230",
        cat_w="#ffffff", cat_w_line="#1f2328", cat_w_eye="#1f2328", cat_w_whisk="#57606a",
        cat_b="#1f2328", cat_b_line="#1f2328", cat_b_eye="#e3b341", cat_b_whisk="#8c959f",
        cat_paw="#ffffff", cat_nose="#f08aa6", ghost_w="#8c959f", ghost_b="#1f2328",
        web="#8c959f", wire="#57606a", bolt_core="#cae8ff", thunder="#d4a72c",
        blue="#2f81f7", blue_hi="#9ecbff", tunnel="#0b0d12", tunnel_hi="#262a33",
    ),
    "dark": dict(
        _SKY,
        bg="#0d1117", fg="#e6edf3", rule="#3d444d", red="#f85149",
        blade="#dfe5ec", blade_edge="#6b7580", hamon="#ffffff", tsuba="#c9a24a", wrap="#2b2b2b",
        void_fg="#f0f0ff", smoke="#8b949e", flash="#f0f0ff", crack="#8b949e", wood="#9a6b3f",
        cat_w="#f6f8fa", cat_w_line="#0d1117", cat_w_eye="#0d1117", cat_w_whisk="#6e7681",
        cat_b="#010409", cat_b_line="#c9d1d9", cat_b_eye="#f2cc60", cat_b_whisk="#c9d1d9",
        cat_paw="#f6f8fa", cat_nose="#f08aa6", ghost_w="#f6f8fa", ghost_b="#6e7681",
        web="#c9d1d9", wire="#8b949e", bolt_core="#ffffff", thunder="#e3b341",
        blue="#58a6ff", blue_hi="#cae8ff", tunnel="#010409", tunnel_hi="#21262d",
    ),
}
