# Rendering tartans to images

`scripts/render_tartan.py` turns any row of `data/tartans.csv` into a
true-to-size woven-cloth image.

## The spec

| Property | Value |
|---|---|
| Threads | 528 × 528 |
| Physical size | 12" × 12" |
| Threads per inch | 44 |
| Pixels per thread | 3 → 1584 px cloth |
| Weave | 2/2 twill, Z direction |
| Yarn shading | round-yarn (crown bright, edges dark) so the weave shows in solid blocks |
| Output | palette-mode PNG, ~28 KB each |

At 3 px/thread and 44 threads/inch the image is exactly 132 px per inch, so a
528-thread sett renders at 1584 px = 12.0 inches of real cloth.

## The method, in five steps

1. **Expand the threadcount** to the full sett. If `symmetric = yes`, mirror the
   interior at the pivots (`tokens + reversed(tokens[1:-1])`).
2. **Tile** that colour sequence out to 528 threads, for both warp (vertical) and
   weft (horizontal) — tartan uses the same sett on both axes.
3. **Apply the 2/2 twill.** For pixel (x, y) the warp thread shows if
   `(x - y) mod 4 < 2`, otherwise the weft thread shows. This is what makes the
   diagonals run bottom-left to top-right.
4. **Shade each yarn** as a round cylinder — a parabolic brightness profile across
   each thread — so even a solid single-colour block shows woven texture rather
   than flat colour.
5. **Render at an integer number of pixels per thread and do NOT resample.**

## The one critical rule: never downscale the weave

Rendering large then resizing down (e.g. Lanczos) smears the hard thread edges
into thousands of intermediate colours. That destroys two things at once:

- **Fidelity** — clean thread boundaries turn to mush.
- **File size** — the image goes from ~10 distinct colours to tens of thousands,
  which makes even WEBP compression **~12× larger** than a clean palette PNG.

Rendering at an exact integer px/thread keeps the image a clean, periodic lattice
of a handful of colours. A palette-mode PNG then compresses it to ~28 KB.
The whole 5,417-image set is ~150 MB because of this.

## Where the images live

Two full sets (~150 MB plain, ~215 MB watermarked) are published as a GitHub
**Release**, not committed to the repo, to keep clones fast. Regenerate them from
the data any time with `render_tartan.py`.
