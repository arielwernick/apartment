# Apartment

Interactive 3D tools for planning and building out my apartment closets.

## Closet Sim — Left Bay

`closet-sim.html` is a self-contained Three.js app for practicing the cleat-and-shelf
build for the left pantry bay before touching a real wall. Open it in any browser —
no server, no install.

**The bay:** 46" W × 65" H × 29.5" D, four graduated plywood shelves below the
existing divider shelf.

**What you can do:**
- Orbit / zoom / pan around the empty bay
- Step through the 7-stage build: tape lines → studs → pre-paint → back cleats →
  side cleats → drop shelves
- Watch each part animate into place

Build plan source: `left_bay_final_build_plan.svg` (graduated shelf heights
9 / 10 / 11 / 13 / 22", cleat geometry with 1" setback and 45° front clip).

**Live:** https://arielwernick.github.io/apartment/closet-sim.html

### Run it locally

It uses ES module import maps (Three.js from a CDN), so it must be served over
http — a `file://` double-click won't load the module in every browser.

```bash
python3 -m http.server 8731
open http://localhost:8731/closet-sim.html
```

### Deploy

It's a single static HTML file, so any static host works. This repo is published
via **GitHub Pages** (Settings → Pages → deploy from `main`, root) — every push to
`main` auto-redeploys.
