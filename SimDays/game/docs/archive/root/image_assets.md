# Living the Dream — Image Asset Tracker

Tracking list for all generated images. Companion to [game_design.md](game_design.md).

## Conventions

- **Style:** location backgrounds are **eye-level**, realistic/anime VN style. Characters are pasted on top (transparent PNG). The **city map is the only isometric low-poly asset.**
- **Interiors only (Phase 1):** one interior background per location — the map serves as the "exterior". Establishing exteriors are Phase 3 (optional).
- **Day / Night:** every location background gets a **day** and a **night** variant (lighting, window light, lamps on). No seasons.
- **Resolution:** target 1920×1080 (16:9), backgrounds full-bleed. Characters: tall portrait PNG, transparent, ~1080px tall, feet near bottom.
- **Consistency:** same camera height, same lens feel, same color grading family across all backgrounds so characters sit naturally in any scene.
- **Naming:** `bg_<location>_<day|night>.png` for backgrounds, `char_<name>_<pose|expr>.png` for characters, `map_city_<day|night>.png`.

Status legend: ⬜ todo · 🟨 in progress · ✅ done

---

## PHASE 1 — MVP start (the minimum to have a playable loop)

The core loop: live at home → go to map → work a job → train a skill → socialize. These cover that.

### Home
| # | Asset | Day | Night | File / Notes |
|---|---|---|---|---|
| 1 | Apartment — Tier 1 (cheap) | ✅ | ✅ | `cheaphouse_day` / `cheaphouse_night` — starter |
| 2 | Apartment — Tier 2 (mid) | ✅ | ✅ | `goodhomeday` / `goodhomenight` |
| 3 | Apartment — Tier 3 (rich) | ✅ | ✅ | `richhomeday` / `richhomenight` |

### Core job interiors
| # | Asset | Day | Night | File / Job |
|---|---|---|---|---|
| 4 | Corporate office ("biuro 1") | ✅ | ⬜ | `goodoffice1` — A. Corporate (INT). Lobby: `officelobby1` |
| 5 | Coworking / IT ("biuro 2") | 🟨 | ⬜ | `mediumoffice1` as stand-in — D. IT/Freelance (dedicated coworking look optional) |
| 5b | Low-tier / gritty office | ✅ | ⬜ | `pooroffice1` — spare: startup grind / temp job |
| 6 | Coffee Shop "Grounds" | ✅ | ✅ | `cafeday/cafenight` — B. Food & Bev |
| 7 | Iron Gate Gym | ✅ | ⬜ | `gymdaypeople` + `gymdaynopeople` (no night) — E. Trainer / STR |

### Core skill / social interiors
| # | Asset | Day | Night | File / Purpose |
|---|---|---|---|---|
| 8 | City Library | ✅ | ✅ | `libraryday/librarynight` — study INT |
| 9 | Bar "Static" | — | ✅ | `bar.png` (evening; day variant optional) — nightlife/CHR/security |

### City
| # | Asset | Day | Night | Notes |
|---|---|---|---|---|
| 10 | City map | ✅ | ⬜ | isometric; night variant still needed |

**Phase 1 status:** strong base, but 3 must-haves missing before the loop is whole → **starter apartment, corporate office, coworking/IT office.**

---

## PHASE 2 — Full location set (rounds out jobs, skills, leisure)

### Remaining job interiors
| # | Asset | Day | Night | File / Career |
|---|---|---|---|---|
| 11 | Restaurant "Eleven" | ✅ | ✅ | `restaurantday/restaurantnight` — B. Food & Bev |
| 12 | LogiCity Warehouse | ✅ | ⬜ | `warehouse.png` (no night) — C. Physical (STR) |
| 13 | Krawczyk's Garage | ✅ | ⬜ | `carworkshop.png` (no night) — C. mechanic |
| 14 | Hospital — lobby / ward | ✅ | ⬜ | `hospital1` (no night) — "szpital" |

### Skills / leisure / utility
| # | Asset | Day | Night | File / Purpose |
|---|---|---|---|---|
| 15 | Community College — classroom | ✅ | ⬜ | `class.png` + `schoolhall.png` (no night) — "szkoła" |
| 16 | The Mall — concourse | ✅ | ✅ | `mallday/mallnight` |
| 16a | Mall — Clothes shop | ✅ | ⬜ | `clothesshop.png` — buy APP |
| 16b | Mall — Electronics shop | ✅ | ⬜ | `electronicsshop.png` |
| 16c | Mall — Gift shop | ✅ | ⬜ | `giftshop.png` — gifts for NPCs |
| 17 | Grocery Store | ⬜ | ⬜ | **MISSING** — buy food (hunger/cooking) |
| 18 | City Park | ✅ | ✅ | `parkday/parknight` |
| 19 | Beach / Boardwalk | ✅ | ✅ | `beachday` / `beachnight` |

**Phase 2 status:** only **Grocery Store** still missing. Remaining: night variants for warehouse/garage/school/mall-shops/offices/gym/hospital.

---

## PHASE 3 — Polish (optional, later)

- Establishing **exterior** shots for key locations (instead of relying on map zoom).
- Apartment **sub-rooms** if needed: bathroom, separate bedroom view (Tiers 2–3 only).
- Map landmarks seen on the city image but not yet jobs: **Stadium**, **Marina/Port**, **Airport**, **Botanical domes**, **Amusement/Water park**, **Cathedral**. Reserve as future event/date venues — generate only when a feature needs them.

---

## Characters (transparent PNG, separate track)

You're already generating these. Roster from [game_design.md](game_design.md). Each character needs at minimum a **neutral full-body** pose; expressions (smile / sad / surprised / angry) added per character as their content is written.

| Name | Gender | Met at | Base pose | Expressions |
|---|---|---|---|---|
| Protagonist | ? | — | ⬜ | — |
| Martha | F | Corporate | ⬜ | ⬜ |
| Zoe | F | Coffee Shop | ✅ | 🟨 (see below) |

**Zoe wardrobe roles:** `punk` = her **default** look · `street` = **gym** outfit · plus `hoodie`, `coat`, `beach` (beach still in raw/). All sprites background-cleaned (rembg u2net+isnet combine; backups in `backup_pre_rembg/`).
| Ray | M | Warehouse | ⬜ | ⬜ |
| Jake | M | Coworking | ⬜ | ⬜ |
| Natalie | F | Warehouse | ⬜ | ⬜ |
| Anna | F | Coffee Shop | ⬜ | ⬜ |
| Becca | F | Gym | ⬜ | ⬜ |
| Mia | F | Coworking | ⬜ | ⬜ |
| Tommy | M | Gym | ⬜ | ⬜ |

> Generation order suggestion: do characters for the **Phase 1 job locations first** (Martha, Zoe, Becca/Tommy, Jake/Mia) so the MVP loop has people in it.

### Zoe — wardrobe & sprites (`images/characters/zoe/`)
Consistent design: long wavy red hair, green eyes, gold star hairclip, star pendant, red hair-ribbon. **5 outfits.** Clean transparent cut-outs live in the folder root; raw originals needing background cleanup are in `zoe/raw/`.

| Outfit | Clean sprites (root) | Raw extras (`raw/`, need cleanup) |
|---|---|---|
| **street** (bomber + crop top + track pants) | neutral, smile, talk, surprised, full | — |
| **punk** (biker jacket + skirt + thigh-highs) | smile, full_back, full_sit, full_wave | neutral, talk |
| **hoodie** (cream hoodie + shorts + bag) | smile, full | neutral, talk |
| **coat** (red coat + black turtleneck) | smile, full | surprised |
| **beach** (bikini + open shirt + shorts) | — | neutral, smile, full *(+ `surprised_BROKEN` — checkerboard baked in, re-cut needed)* |

**Cleanup TODO for `raw/`:** faint colored halo around the silhouette on most → re-key the background before use; `zoe_beach_surprised_BROKEN.png` has a checkerboard baked into the pixels and must be regenerated/re-cut.

---

## Open decisions

1. **Protagonist on-screen?** Most dating sims keep the MC off-screen (first-person). If MC is shown, needs a sprite + outfit variants (APP changes wardrobe).
2. **Outfit variants** — does APP stat visibly change the MC / NPC clothes, or is it stat-only? Affects character image count a lot.
3. **Day/night for low-difference interiors** (warehouse, garage) — do we really need night, or skip to save work? Currently planned for all.
