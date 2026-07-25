# verified-tartans

A verified, consolidated dataset of **5,417 Scottish tartans** — each with a
machine-readable threadcount (sett) and colour palette — plus a **locked
1,096-colour master palette** and a renderer that produces true-scale woven
images.

Every tartan's construction is **cross-checked against 2 or more independent
historical archives**, so you can render or weave any of them with confidence.

---

## Why this exists

Public tartan data is messy. The same tartan is recorded differently across
archives, colours are stored under dozens of near-duplicate hex values, and
threadcounts are increasingly locked behind logins. This repo is one clean,
verified, self-describing dataset built from that mess — given back openly.

What makes it different from a raw scrape:

- **Cross-verified.** Setts confirmed across the Scottish Register of Tartans,
  the Scottish Tartans Authority, Weddslist, and House of Tartan.
- **Consolidated palette.** ~1,600 raw hex values reduced to **1,096
  perceptually distinct colours** with no visible change to any tartan (CIEDE2000).
- **Renderable.** A documented 2/2-twill renderer turns any row into a
  true-to-size 12"×12" image.

---

## Repository layout

```
verified-tartans/
├── data/
│   ├── tartans.csv                  5,417 verified tartans (the main dataset)
│   ├── tartans_cross_verified.csv   3,330 tartans confirmed by 2+ archives, with source list
│   └── expansion_candidates.csv     692 additional verified tartans not yet in the main set
├── palette/
│   ├── palette.csv                  the 1,096-colour master palette + usage stats
│   ├── palette_sorted.csv           same, sorted by family/hue/lightness with merge signals
│   ├── hex_mapping.csv              every raw source hex → its locked palette colour
│   └── palette_viewer.html          open in a browser to see all 1,096 colours as swatches
├── scripts/
│   └── render_tartan.py             standalone 2/2-twill renderer (numpy + Pillow)
├── docs/
│   ├── DATA_DICTIONARY.md           every column in every file, explained
│   ├── RENDERING.md                 how the images are produced
│   └── DECISIONS.md                 the project decision log (why things are the way they are)
└── README.md                        this file
```

Rendered images (≈360 MB across two sets) are **not** in the main repo — they
are published as a GitHub **Release** to keep the repo lightweight. See
[docs/RENDERING.md](docs/RENDERING.md).

---

## Quick start

**Look at the data:** open `data/tartans.csv` in any spreadsheet.
Each row is one tartan: `name, threadcount, palette, colors_hex, symmetric,
thread_total, verification`.

**See the colours:** open `palette/palette_viewer.html` in a browser.

**Render a tartan:**
```python
from scripts.render_tartan import palette, weave, full_sett
from PIL import Image
pal = palette("K#101010 OG#5C6428 B#345064")
arr = weave("B/28 K6 B6 K6 B6 K32 OG32 K6 OG32 K32 B32 K6 B/6", "yes", pal)
Image.fromarray(arr).save("campbell.png")
```

---

## Reading a threadcount

A threadcount is a sequence of `CODE + COUNT` tokens, e.g.
`B/28 K6 B6 K6 B6 K32 OG32 K6 OG32 K32 B32 K6 B/6`.

- Each `CODE` (B, K, OG…) is a colour, resolved via the row's `palette`
  (`B#345064` = code B is hex #345064).
- Each number is a thread count for that colour.
- A `/` marks a **pivot** — the reflection point of a symmetric sett.

To expand a symmetric sett (`symmetric = yes`) into the full weavable repeat:
take the tokens, then append the interior reversed (`tokens + reversed(tokens[1:-1])`).
The result's total equals `thread_total`. For `symmetric = no`, the threadcount
is already the full sett.

Warp and weft use the same sequence (tartan is woven square), in a 2/2 twill.

Full details in [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).

---

## Provenance & honesty

- All threadcounts and colours originate from the **Scottish Register of
  Tartans** and are cross-checked against the **Scottish Tartans Authority**,
  **Weddslist**, and **House of Tartan**.
- Only tartans whose sett is confirmed by **2+ independent archives** are in the
  verified set — except where the Register, as the authoritative record, is the
  sole holder.
- Colours are **consolidated for perceptual consistency** (see
  [docs/DECISIONS.md](docs/DECISIONS.md)); they are not the raw archive hexes.
  For the exact original recorded hexes, `palette/hex_mapping.csv` maps every one.
- A handful of tartans use mixture colour codes no archive fully defines; these
  are excluded rather than guessed.

## Licence

Built from public data. Check the terms of the upstream source archives before
commercial use — each carries its own. This consolidation is shared for research
and reference.
