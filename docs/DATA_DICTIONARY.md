# Data Dictionary

Every column in every data file, explained.


## `data/tartans.csv`

The main dataset — 5,417 verified tartans on the locked 1,096-colour palette.

**5417 rows.** Columns:

| Column | Example | Meaning |
|---|---|---|
| `name` | A J Gallacher | Tartan name as recorded |
| `slug` | a-j-gallacher | URL-safe identifier |
| `threadcount` | BG/4 RAB2 K2 RAB2 K6 DR1 | The sett — colour codes + thread counts (see README) |
| `palette` | R#FF0000 DR#B22222 K#101 | CODE#HEX for every code used in the threadcount |
| `colors_hex` | #2E8B57|#0000FF|#101010| | Distinct hex values, pipe-separated |
| `symmetric` | yes | yes = reflective sett (mirror at pivots); no = full sett as written |
| `thread_total` | 282 | Total threads in the full sett (checksum for parsers) |
| `verification` | C_dual_register_scrape | Verification tier (A/B/C — how many sources confirm the sett) |
| `confirmed_by` | nan | Which archives confirmed this sett |

## `data/tartans_cross_verified.csv`

3,330 tartans whose sett is confirmed by 2+ independent archives, with the confirming sources listed.

**3330 rows.** Columns:

| Column | Example | Meaning |
|---|---|---|
| `name` | Baird Dress | Tartan name as recorded |
| `slug` | baird-dress | URL-safe identifier |
| `threadcount` | B/8 K8 B46 K24 G20 K2 W4 | The sett — colour codes + thread counts (see README) |
| `palette` | P#780078 PURPLE; W#E0E0E | CODE#HEX for every code used in the threadcount |
| `symmetric` | yes | yes = reflective sett (mirror at pivots); no = full sett as written |
| `thread_total` | 324 | Total threads in the full sett (checksum for parsers) |
| `sources_verifying` | 4 | Count of independent archives that agree on the sett |
| `verified_by` | Scottish Register of Tar | — |
| `colour_agreement` | 4/4 | How many confirming sources also agree on colour |
| `primary_source` | Scottish Register of Tar | — |
| `dissenting_sources` | nan | — |
| `origin_url` | https://www.tartanregist | — |
| `stwr_ref` | 233 | Scottish Tartans World Register reference number |
| `sta_ref` | 233 | — |
| `designer` | nan | Recorded designer/source of the tartan |
| `tartan_date` | 01/01/2002 | Recorded date |
| `register_category` | Clan; Family | — |
| `restrictions` | nan | — |
| `seo_search_volume` | nan | — |

## `data/expansion_candidates.csv`

692 additional verified, renderable tartans not yet in the main set (scored by a demand proxy).

**692 rows.** Columns:

| Column | Example | Meaning |
|---|---|---|
| `priority_rank` | 1 | Rank by demand_score |
| `name` | Ruthven (V.S.) | Tartan name as recorded |
| `slug` | ruthven-v-s | URL-safe identifier |
| `threadcount` | R/8 G4 R60 B36 G30 W/12 | The sett — colour codes + thread counts (see README) |
| `palette` | R#C80000 RED; B#2C2C80 B | CODE#HEX for every code used in the threadcount |
| `symmetric` | yes | yes = reflective sett (mirror at pivots); no = full sett as written |
| `thread_total` | 280 | Total threads in the full sett (checksum for parsers) |
| `demand_score` | 120 | Heuristic demand ranking (higher = more likely to sell) |
| `category` | Clan; Family | Register category |
| `sources_verifying` | 2 | Count of independent archives that agree on the sett |
| `verified_by` | Scottish Register of Tar | — |
| `colour_agreement` | 2/2 | How many confirming sources also agree on colour |
| `listed_house_of_tartan` | yes | — |
| `listed_weddslist` | yes | — |
| `primary_source` | Scottish Register of Tar | — |
| `designer` | Sobieski Stewarts, The | Recorded designer/source of the tartan |
| `tartan_date` | 01/01/1842 | Recorded date |
| `stwr_ref` | 1521.0 | Scottish Tartans World Register reference number |
| `restriction_status` | none | — |
| `restrictions` | nan | — |
| `origin_url` | https://www.tartanregist | — |

## `palette/palette.csv`

The 1,096-colour master palette with per-colour usage across the catalog.

**1096 rows.** Columns:

| Column | Example | Meaning |
|---|---|---|
| `yarn_hex` | #101010 | The colour |
| `family` | Black | Colour family (Blue, Green, Red…) |
| `tartans_using` | 2977 | How many of the 5,417 tartans use this colour |
| `pct_of_catalog` | 54.96 | That as a percentage of the catalog |
| `widest_block_threads` | 240 | Widest solid run of this colour anywhere (in threads) |
| `widest_block_mm` | 138.5 | That width in mm at 44 threads/inch |

## `palette/palette_sorted.csv`

The palette sorted by family→hue→lightness, with nearest-neighbour merge signals.

**1096 rows.** Columns:

| Column | Example | Meaning |
|---|---|---|
| `row` | 1 | Sort position |
| `hex` | #000000 | The colour |
| `R` | 0 | Red channel 0–255 |
| `G` | 0 | Green channel 0–255 |
| `B` | 0 | Blue channel 0–255 |
| `family` | Black | Colour family (Blue, Green, Red…) |
| `hue` | 0.0 | Hue 0–360° |
| `lightness` | 0.0 | Lightness 0–100 |
| `saturation` | 0.0 | Saturation 0–100 |
| `tartans_using` | 367 | How many of the 5,417 tartans use this colour |
| `pct_of_catalog` | 6.77 | That as a percentage of the catalog |
| `widest_block_mm` | 108.5 | That width in mm at 44 threads/inch |
| `nearest_hex` | #101010 | Closest other colour in the palette |
| `nearest_deltaE` | 2.73 | Perceptual distance to that nearest colour (ΔE 2000; <2 ≈ hard to tell apart) |
| `nearest_tartans` | 2977 | How many tartans use that nearest colour |

## `palette/hex_mapping.csv`

Every raw source hex value mapped to the locked palette colour it became.

**1578 rows.** Columns:

| Column | Example | Meaning |
|---|---|---|
| `source_hex` | #000000 | The raw hex as originally recorded in an archive |
| `locked_hex` | #000000 | The palette colour it was consolidated into |
