# Icons — status

## ✅ DONE (all on disk, wired)

**Stats:** `stat_app`, `stat_work`, `stat_int`, `stat_str`, `stat_social`,
`stat_money`, `stat_energy`, `stat_hunger`, `stat_hygiene`, `stat_mood`,
`stat_thirst`, `stat_time`

**Skills:** `skill_art`, `skill_biz`, `skill_cook`, `skill_fit`, `skill_mech`,
`skill_med`, `skill_prog`

**Venue/location:** `icon_apartment_block`, `icon_apartment_ext`, `icon_bar`,
`icon_beach`, `icon_clinic`, `icon_coffee_shop`, `icon_college`, `icon_door_12`,
`icon_door_14`, `icon_elevator`, `icon_garage`, `icon_gym`, `icon_hospital`,
`icon_house_suburb`, `icon_house_uptown`, `icon_hub`, `icon_library`,
`icon_lobby_luxury`, `icon_mall`, `icon_metro`, `icon_nightclub`,
`icon_office_budget`, `icon_office_exec`, `icon_office_ext`, `icon_office_mid`,
`icon_park`, `icon_reception`, `icon_restaurant`, `icon_restaurant_eleven`,
`icon_rooftop`, `icon_shop_clothing`, `icon_shop_electronics`,
`icon_shop_lifestyle`, `icon_szpital`, `icon_terrace`, `icon_university`

**Portrait icons (all 11):** `portrait_nora`, `portrait_marcus`, `portrait_caroline`,
`portrait_lena`, `portrait_natalie`, `portrait_martha`, `portrait_elle`,
`portrait_zoe`, `portrait_sam`, `portrait_eli`, `portrait_kai`

**Conversation topic icons (all 9):** `topic_ambition`, `topic_art`, `topic_food`,
`topic_movies`, `topic_music`, `topic_nightlife`, `topic_sports`, `topic_travel`,
`topic_work`

**NPC action icons (all 7):** `act_talk`, `act_gift`, `act_hug`, `act_kiss`, `act_invite`,
`act_phone`, `act_leave`


**Phone app icons (all 8):** `app_messages`, `app_contacts`, `app_map`, `app_jobs`,
`app_bank`, `app_stocks`, `app_tips`, `app_settings`

---

## ❌ STILL TO GENERATE

### 1. Skill icon (1)
| Cut name | Skill | Glyph | Style |
|---|---|---|---|
| `skill_music` | Music | guitar / note | circular navy-badge (same as other skills) |

Drop into `images/ui/icons/skill_music.png`. Low priority — falls back to no-icon.

---

### 2. Nadbrzeże venue icons (2)
Used in `nadbrzeze_hub` bottom bar. `icon_bar` already exists (reused for The Anchor).

| Cut name | Venue | Glyph | Style |
|---|---|---|---|
| `icon_casino` | Casino | roulette wheel or playing card + chip | circular navy-badge |
| `icon_lombard` | Lombard / Pawn Shop | magnifying glass over a tag, or scales | circular navy-badge |

Drop into `images/ui/icons/icon_casino.png` and `icon_lombard.png`.

---

### 3. Weekend venue icon (1)
Used in `nadbrzeze_hub` and `centrum_hub` as the flea market tile.
Currently falls back to `icon_mall`.

| Cut name | Venue | Glyph | Style |
|---|---|---|---|
| `icon_flea_market` | Flea Market | vendor stall / tent canopy | circular navy-badge |

Drop into `images/ui/icons/icon_flea_market.png`.

---

### 3. New zone map icons (3 PNG sets)
Each map zone needs `z_<key>_idle.png`, `z_<key>_hi.png`, `z_<key>_mask.png`
in `images/ui/`. The new Quayside zone is wired in code but missing art.

| Zone key | Location | Notes |
|---|---|---|
| `nadbrzeze` | Quayside / Nadbrzeże | **Temporary placeholder blob PNGs now on disk** (plain ellipse at 870,820) so the zone is clickable — replace with real art. Adjust centre coords (870, 820) in `map.rpy` if you move it |

**Style:** same as existing zone PNGs — irregular blob/district shape, not a rectangle.
- `_idle`: muted dark blue-grey fill, subtle outline, no glow
- `_hi`: same shape, bright cyan/blue fill + soft outer glow (hover state)
- `_mask`: pure black silhouette on white, exact same shape (used for click detection)

**What the zone looks like on the map:** waterfront district — narrow strip along the river above plaza. Shape should suggest a quayside: slightly elongated horizontally, irregular edge on the river side.
