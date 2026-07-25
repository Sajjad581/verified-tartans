# Decision log

Why the dataset is the way it is. Kept so future work (and future collaborators)
don't re-litigate settled questions.

## Data source

- The base data is a ~2020 snapshot of the **Scottish Register of Tartans**
  (originally via tartanify.com), verified register-accurate against a
  login-gated record byte-for-byte.
- The register today holds 10,000+ tartans, but threadcounts are now behind a
  login, and most post-2020 additions are low-demand "(Personal)" vanity
  tartans. This snapshot's ~5,400 core is the useful, weavable set.

## Verification

- Setts are cross-checked across **4 independent archives**: Scottish Register of
  Tartans, Scottish Tartans Authority, Weddslist, House of Tartan (via the
  open `thetartan/tartan-database` repo).
- Matching is done on **threadcount geometry** (stripe-count sequence, forwards
  or reversed), not colour codes — different archives use different code letters
  for the same yarn, so code matching would wrongly reject genuine agreements.
- **Tiers:** A = 2+ independent archives agree; B = 1 independent archive agrees;
  C = both register scrapes agree (the register is authoritative, so C is sound).
- Name collisions are real (12 different "Anderson" tartans, 7 "Black Watch"),
  which is why matching indexes *all* records per name, not the first.

## The 1,096-colour palette

- Raw archives record the same yarn under ~1,600 near-duplicate hex values
  (decades of different cataloguers). These are consolidated to **1,096
  perceptually distinct colours** so **no tartan changes visibly**.
- Method: two-pass CIEDE2000 (ΔE 2000) merge.
  - Colours ≤ 1.0 ΔE apart (below the human just-noticeable difference) merge.
  - Thin stripes (≤ 8 threads) and single-tartan accent colours are allowed up
    to ΔE 2.0 — a shift that small on a thin or unique stripe is imperceptible.
  - Common colours forming large solid blocks are **never** shifted.
  - Maximum shift anywhere: **ΔE 2.74**, only on thin single-tartan stripes.
- **Why not the register's official 137 shades?** 137 is the register's *yarn
  standard* — correct for weaving, but it collapses distinct recorded colours and
  loses per-tartan fidelity in the *images*. 1,096 keeps the images faithful to
  what each tartan actually records. The two numbers answer different questions
  (screen fidelity vs. yarn stocking); they are not sequential reductions.
- Usage is heavily Pareto: ~10 colours cover 50% of all thread used, ~120 cover
  90%, and ~570 colours each appear in a single tartan. `palette/hex_mapping.csv`
  preserves every original hex if you need the exact recorded value.

## Colourways (Modern / Ancient / Weathered / Muted)

- These are **not separate tartans**. They are the *same threadcount* rendered
  with a different shade card:
  - **Modern** — deep synthetic-dye colours (standard since the 1860s).
  - **Ancient** — lighter, softer, mimicking pre-1860 vegetable dyes.
  - **Weathered / Reproduction** — earthy, greyed, "aged" look (mid-20th century).
  - **Muted** — a later, softened-modern commercial tier.
- The register stores only one sett per tartan (Modern hexes). Ancient/Weathered/
  Muted images must be *generated* by shade substitution — they are not distinct
  records.
- This is why a retail site can list 4× more products than there are setts: the
  right model is **clan → sett → colourway**, three levels, not one.

## Scope

- The verified set is **5,417**, not the full 10,000+. Completeness that can't be
  backed by a verified threadcount + image is worth less than authority that can.
- `data/expansion_candidates.csv` holds 692 further verified tartans that can be
  added, scored by a commercial-demand proxy.
