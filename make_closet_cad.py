"""
Generate a dimensioned CAD drawing of the apartment closet (left-bay shelving).
Units = inches. Outputs closet.dxf (AutoCAD R2010), openable in AutoCAD/Fusion/
LibreCAD/SketchUp and re-saveable as .dwg.
"""
import ezdxf
from ezdxf.enums import TextEntityAlignment

# ── Closet dimensions (inches) ──────────────────────────────────────────────
FW, FH, D = 92.0, 99.0, 29.5            # full closet W × H × depth
DIV_T = 1.5                              # center divider thickness
LOWER_H = 65.0                           # lower section / divider height
CX = FW / 2                              # closet centerline
DIV_L, DIV_R = CX - DIV_T/2, CX + DIV_T/2
BAY_R = DIV_L                            # left bay right edge (divider face)
BAY_W = BAY_R                            # left bay width (left wall at x=0)
OPEN_W = 59.25                           # doorway opening (centered)
OPEN_L, OPEN_R = (FW - OPEN_W)/2, (FW + OPEN_W)/2
HEADER = 96.0                            # door top (≈3" header gap)
PANEL_W = 31.0
FIXED = [65.0, 82.0]                     # existing full-width shelves
SHELVES = [21.0, 34.0, 45.0, 54.0]      # new left-bay shelf tops (AFF)
SHELF_T = 0.75
SHELF_DEPTH = 22.0

doc = ezdxf.new("R2000", setup=True)   # R2000 round-trips cleanly through LibreDWG → .dwg
doc.units = ezdxf.units.IN
msp = doc.modelspace()

# ── Layers ──────────────────────────────────────────────────────────────────
def layer(name, color, lt="CONTINUOUS"):
    doc.layers.add(name, color=color, linetype=lt)
layer("WALLS", 7)
layer("DIVIDER", 8)
layer("FIXED_SHELF", 3)
layer("NEW_SHELF", 4)
layer("DOORS", 5, "DASHED")
layer("CLEATS", 30)
layer("DIM", 1)
layer("TEXT", 2)
layer("TITLE", 7)

# ── Dimension style ─────────────────────────────────────────────────────────
ds = doc.dimstyles.add("CLOSET")
ds.dxf.dimtxt = 2.2      # text height
ds.dxf.dimasz = 1.4      # arrow size
ds.dxf.dimexe = 0.7      # extension beyond dim line
ds.dxf.dimexo = 0.6      # extension offset from object
ds.dxf.dimgap = 0.7
ds.dxf.dimdec = 2

def rect(x1, y1, x2, y2, lay):
    msp.add_lwpolyline([(x1,y1),(x2,y1),(x2,y2),(x1,y2)], close=True, dxfattribs={"layer": lay})
def line(x1, y1, x2, y2, lay):
    msp.add_line((x1,y1), (x2,y2), dxfattribs={"layer": lay})
def text(s, x, y, h=2.2, lay="TEXT", align=TextEntityAlignment.LEFT):
    t = msp.add_text(s, dxfattribs={"layer": lay, "height": h})
    t.set_placement((x, y), align=align)
def _tick(x, y):
    msp.add_line((x-0.9, y-0.9), (x+0.9, y+0.9), dxfattribs={"layer": "DIM"})
# hand-drawn dimensions (lines + ticks + TEXT) — no MTEXT, fully DWG-convertible
def hdim(x1, x2, y, base_y, txt):
    line(x1, y, x1, base_y, "DIM"); line(x2, y, x2, base_y, "DIM")   # extension lines
    line(x1, base_y, x2, base_y, "DIM")                              # dimension line
    _tick(x1, base_y); _tick(x2, base_y)
    text(txt, (x1+x2)/2, base_y+1.0, 2.2, "DIM", TextEntityAlignment.CENTER)
def vdim(y1, y2, x, base_x, txt):
    line(x, y1, base_x, y1, "DIM"); line(x, y2, base_x, y2, "DIM")
    line(base_x, y1, base_x, y2, "DIM")
    _tick(base_x, y1); _tick(base_x, y2)
    text(txt, base_x+1.6, (y1+y2)/2, 2.2, "DIM", TextEntityAlignment.LEFT)

# ════════════════════════════════════════════════════════════════════════════
# VIEW 1 — FRONT ELEVATION  (origin 0,0)
# ════════════════════════════════════════════════════════════════════════════
rect(0, 0, FW, FH, "WALLS")                                   # outer shell
rect(DIV_L, 0, DIV_R, LOWER_H, "DIVIDER")                     # center divider (lower)
for y in FIXED:                                              # existing shelves
    rect(0, y-0.75, FW, y+0.75, "FIXED_SHELF")
for y in SHELVES:                                           # new left-bay shelves
    rect(0, y-SHELF_T, BAY_R, y, "NEW_SHELF")
# doorway opening + header
line(OPEN_L, 0, OPEN_L, HEADER, "WALLS")
line(OPEN_R, 0, OPEN_R, HEADER, "WALLS")
line(OPEN_L, HEADER, OPEN_R, HEADER, "WALLS")
# two sliding panels (representative, meeting at center)
rect(OPEN_L, 0, CX, HEADER, "DOORS")
rect(CX, 0, OPEN_R, HEADER, "DOORS")
text("FRONT ELEVATION", FW/2, FH+14, 3.2, "TITLE", TextEntityAlignment.CENTER)
# shelf-height labels (left bay)
for y in SHELVES + FIXED:
    text(f'{y:.0f}" AFF', BAY_R-1.5, y+1.0, 1.8, "TEXT", TextEntityAlignment.RIGHT)
# dims
hdim(0, FW, 0, -10, "92\"")                                  # overall width
hdim(OPEN_L, OPEN_R, FH, FH+5, "59.25\" doorway")            # doorway
vdim(0, FH, FW, FW+12, "99\"")                               # overall height
vdim(0, LOWER_H, 0, -12, "65\"")                             # lower section
hdim(0, BAY_R, -16, -16, '45.25" left bay')                 # bay width

# ════════════════════════════════════════════════════════════════════════════
# VIEW 2 — SIDE PROFILE  (offset right). Back wall at left, front (door) at right.
# ════════════════════════════════════════════════════════════════════════════
SX = FW + 46
rect(SX, 0, SX+D, FH, "WALLS")
for y in FIXED:
    line(SX, y, SX+D, y, "FIXED_SHELF")
for y in SHELVES:
    rect(SX, y-SHELF_T, SX+SHELF_DEPTH, y, "NEW_SHELF")
    # cleat hint under shelf front
    line(SX+SHELF_DEPTH-1.5, y-SHELF_T, SX+SHELF_DEPTH-1.5, y-SHELF_T-1.5, "CLEATS")
line(SX+D-0.8, 0, SX+D-0.8, HEADER, "DOORS")                 # door plane
text("SIDE PROFILE", SX+D/2, FH+14, 3.2, "TITLE", TextEntityAlignment.CENTER)
text("back", SX+1, FH-4, 1.8, "TEXT")
text("front", SX+D-1, FH-4, 1.8, "TEXT", TextEntityAlignment.RIGHT)
hdim(SX, SX+D, 0, -10, "29.5\" deep")
hdim(SX, SX+SHELF_DEPTH, FH, FH+5, '22" shelf')
vdim(0, FH, SX+D, SX+D+12, "99\"")

# ════════════════════════════════════════════════════════════════════════════
# VIEW 3 — PLAN VIEW  (below elevation). Back wall at top, opening at bottom.
# ════════════════════════════════════════════════════════════════════════════
PY = -64                                                     # plan baseline (back wall y)
back, front = PY, PY - D
rect(0, front, FW, back, "WALLS")
rect(DIV_L, front, DIV_R, back, "DIVIDER")                   # divider footprint
rect(0, back-SHELF_DEPTH, BAY_R, back, "NEW_SHELF")          # left-bay shelf footprint
# front wall returns (solid each side of opening)
rect(0, front, OPEN_L, front+1.0, "WALLS")
rect(OPEN_R, front, FW, front+1.0, "WALLS")
# bypass door panels on two tracks
rect(OPEN_L, front+1.0, OPEN_L+PANEL_W, front+2.0, "DOORS")
rect(OPEN_R-PANEL_W, front+2.2, OPEN_R, front+3.2, "DOORS")
text("PLAN VIEW", FW/2, back+14, 3.2, "TITLE", TextEntityAlignment.CENTER)
hdim(0, FW, front, front-10, "92\"")
vdim(front, back, 0, -12, "29.5\"")
hdim(0, BAY_R, back, back+7, '45.25" bay')

# ── Title + notes ───────────────────────────────────────────────────────────
text("APARTMENT CLOSET — LEFT-BAY SHELVING", 0, FH+52, 4.0, "TITLE")
notes = [
    "All dimensions in inches.  Drawn 1:1 (1 unit = 1 inch).",
    "Closet 92 W x 99 H x 29.5 D.  Sliding-door opening 59.25 (centered).",
    "Left bay 45.25 wide: four 3/4\" plywood shelves at 21 / 34 / 45 / 54 AFF,",
    "22\" deep, on 1-1/2\" wood cleats (back + 2 sides).  Existing shelves at 65 & 82.",
]
for i, n in enumerate(notes):
    text(n, 0, FH+46 - i*3.2, 1.9, "TEXT")

doc.audit()
out = "/Users/arielwernick/ariel_claude/apartment/closet.dxf"
doc.saveas(out)
print("wrote", out)
