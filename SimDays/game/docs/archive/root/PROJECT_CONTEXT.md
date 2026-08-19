# LivingTheDream — Project Context for AI Assistants

**Engine:** Ren'Py (Python-based visual novel engine)  
**Genre:** Sandbox dating-sim / life sim VN set in a fictional American city  
**Project path:** `C:/Users/oskar.bazydlo/Documents/LivingTheDream/SimDays/SimDays/game/`  
**Game design doc:** `game_design.md` at repo root

---

## Concept

The player is a young adult who just moved to the city — blank slate, knows nobody. The game blends stat management, career progression, and relationship building. Every job and location has its own social circle; there is no universal NPC pool from day one.

---

## File Structure

```
SimDays/SimDays/game/
  data.rpy                 — default vars, new_day(), spend_time(), time helpers
  characters.rpy           — Character() definitions (mc, z, n, m, etc.)
  images.rpy               — all `image` declarations, micro-animation transforms
  hud.rpy                  — always-on top-bar screen
  map.rpy                  — city map screen, district imagebuttons
  locations.rpy            — one label per location, action menus, NPC meet/talk
  script.rpy               — label start → intro → jump map
  interact.rpy             — NPC_DATA, ROMANCE_PROFILES, NPC_SOCIAL_PROFILES,
                             npc_sprite(), npc_here(), npc_date v2, do_kiss,
                             do_hug, check_jealousy, try_spend, _apply_aff/_trust
  phone.rpy                — phone UI, chat screen, circular avatars, Active Plan card,
                             _INVITATION_META, phone_active_invitation()
  phone_actionable.rpy     — NPC-initiated texting system (initiative), all
                             response dicts, _INITIATIVE_MSGS, variant selection,
                             _check_npc_initiative(), reply labels
  phone_messages.rpy       — queued NPC message delivery system
  world_events.rpy         — WED_REGISTRY, wed_fire(), scene labels for world events
  work_events.rpy          — _wev_relbar_open/close, work event helpers
  gains.rpy                — try_spend(), gain_money(), skill/stat gain helpers
  careers.rpy              — job listing, hiring, promotion logic
  corporate_work.rpy       — Nexus Tower daily work actions
  corporate_arc.rpy        — Martha/Caroline story arcs
  corporate_atlas.rpy      — Atlas presentation arc
  hospital_arc.rpy         — Hospital/Lena story arcs
  it_arc.rpy               — IT/Eli story arcs
  culinary_arc.rpy         — Culinary/Rena arcs
  trainer_arc.rpy          — Gym/Kai arcs
  arcs.rpy                 — generic topic-arc dialogue engine
  gameplay_expansion_scenes.rpy — romance open/reopen scenes
  home_scenes.rpy          — apartment actions
  group_scenes.rpy         — multi-NPC scenes
  onboarding.rpy           — tutorial / first steps
  activity_menu.rpy        — screen activity(items) — left-panel pill-button menu
  screens.rpy              — Ren'Py UI screens overrides
  quests.rpy               — quest/objective tracking
  stocks.rpy               — stock market mini-game
  casino.rpy               — casino mini-game
  profile.rpy              — player profile screen
  test_*.rpy               — self-check test suites (test_gameplay_polish, etc.)

images/                    — assets at repo root, bridged via Windows junction
  locations/               — background WebP files (lossy q88)
  characters/<name>/       — sprite WebP files (lossless) + raw/ originals
  ui/                      — hud_topbar.png, activity_panel.png, activity_item.png,
                             activity_dot.png, icons/, zone masks
  scenes/<scene_name>/     — CG frame PNGs
```

**Asset bridge:** `SimDays/SimDays/game/images` is a Windows directory junction → `../../images`. If assets 404, recreate with `cmd /c mklink /J`.

---

## Stats & Needs

**Core stats (0–100):** STR, INT, CHR, APP  
**Needs (decay daily):** hunger, hygiene, energy  
**Resources:** money (float), day (int), hour (float 7.0–27.0)

Key thresholds from design doc:
- STR ≥ 30 → warehouse/garage jobs
- INT ≥ 35 → IT track
- CHR ≥ 25 → strike up conversation at bar with strangers
- APP+CHR gate → closed party, upscale locations

---

## Time System

Day runs 7 AM – 3 AM (hour 7.0 → 27.0). `spend_time(h)` advances hour; `new_day()` fires at sleep.  
`day % 7` gives weekday (0=Mon … 6=Sun).  
Hard cutoff at hour 27 → auto-sleep with energy penalty.

---

## NPC Roster

All NPCs are in `NPC_DATA` (defined in `interact.rpy`).

| ID | Name | Where met | Romanceable | Notes |
|---|---|---|---|---|
| `nora` | Nora | Café "Grounds" (barista) | Yes | world NPC; likes food/ambition/movies |
| `marcus` | Marcus | Park / Bar | Yes | world NPC; likes sports/food/nightlife |
| `zoe` | Zoe | Beach / Park / Café | Yes | world NPC; likes art/music/nightlife |
| `eli` | Eli | Library / Bar | Yes | world NPC; likes work/movies/music |
| `caroline` | Caroline | Nexus Tower (office) | Yes | career NPC |
| `lena` | Dr. Lena | Hospital | Yes | career NPC |
| `martha` | Martha | Nexus Tower (senior) | Yes | career NPC; gated by caroline_met |
| `natalie` | Natalie | Warehouse | No | career NPC |
| `sam` | Sam | Park / Gym | No | world NPC; likes sports/work/food |
| `kai` | Kai | Gym / Café / Beach | No | world NPC; likes sports/music/nightlife |
| `elle` | Elle | Café / Beach | Yes | world NPC; likes travel/music/art |
| `rena` | Chef Rena | Diner (Mon+Wed nights) | No | career mentor; no_decay=True |

**`NPC_DATA` keys per NPC:**
```python
"nora": {
    "name": "Nora", "portrait": "portrait_nora", "sprite": "nora_cafe_normal",
    "say": "n",        # Ren'Py Character shortcut
    "aff": "nora_affection", "trust": "nora_trust", "greet": "nora_greet",
    "met": "nora_met", # optional — some world NPCs don't have it
    "world": True,     # included in world-NPC interaction pool
    "sprites": {"work": "nora_cafe_normal", "casual": "nora_casual_normal"},
    "sched": [(days_set, (hour_start, hour_end), "location_id"), ...],
    "likes": [...], "dislikes": [...],
    "topic_arcs": { "topic": [ {"id":, "label":, "req":{}} ] }
}
```

**Accessing stats at runtime:**
```python
npc_aff("nora")         # → store.nora_affection
npc_trust("nora")       # → store.nora_trust
npc_sprite("nora", "casual")   # context-appropriate sprite name
npc_here("nora")        # True if NPC is at current_loc and time matches sched
```

**Affection/trust mutation — always use these, never raw setattr:**
```python
_apply_aff("nora", +3)
_apply_trust("nora", +1)
```

---

## Romance System

**`ROMANCE_PROFILES`** (interact.rpy) — romanceable NPCs only.  
**`romance_states`** dict — valid states: `"unopened"`, `"friends"`, `"interested"`, `"dating"`, `"committed"`, `"paused"`, `"closed"`  
**`romance_permanent_closed`** dict — permanently closed routes.  
**`romance_is_open(npc_id)`** — returns True only for `"interested"/"dating"/"committed"`.

Kiss flow: `do_kiss(npc_id)` → if first kiss: `"friends"→"interested"`, fires `scene_first_kiss_{npc}`.  
Jealousy: `check_jealousy` gates on `romance_is_open()`, NOT raw affection.

---

## Economy

**`try_spend(amount, category=None, toast=None)`** (gains.rpy)  
- Returns True and deducts on success.  
- Returns False if insufficient funds or in debt.  
- **Never use `store.money -= cost` directly** (bypasses debt protection). Exception: rent in `new_day()`.

**`gain_money(amount)`** — positive or negative; negative routes through `try_spend`.

---

## NPC-Initiated Texting System (Phases 30–41)

All code in `phone_actionable.rpy` (plus one `default` per variable in `data.rpy`).

### How it works

Once per day, `_check_npc_initiative()` runs:
1. Global roll blocked if `npc_initiative_last_global_day >= day`.
2. Builds `eligible` list: NPCs who are contacts, off cooldown, have available variants.
3. Tier-based global probability (`_TIER_GLOBAL_PROB`) — higher tier = higher chance.
4. Weighted NPC selection: `initiative_weight × tier_weight_mult`; soft 0.5 penalty if same NPC sent yesterday (`npc_initiative_last_sender`).
5. Picks variant via `_pick_weighted_initiative_variant`.
6. Delivers via `_queue_initiative_message` + `deliver_message_now`.
7. Sets `npc_initiative_last_day[npc_id]`, `npc_initiative_pending[npc_id]`, `npc_initiative_last_global_day`, `npc_initiative_last_sender`.

### Texting tiers (`_texting_tier(npc_id)`)

| Value | Name | Description |
|---|---|---|
| 0 | ACQUAINTANCE | in contacts, basic |
| 1 | FAMILIAR | closer friend |
| 2 | CLOSE | trusted friend |
| 3 | VERY_CLOSE | intimate friend |
| None | not a contact | excluded |

### Key dicts in `phone_actionable.rpy` (all `init python`)

```python
_INITIATIVE_MSGS        # variant_id → {"text": str, "responses": list}
_INITIATIVE_VARIANTS    # npc_id → [variant_id, ...]
_INITIATIVE_COOLDOWNS   # npc_id → base cooldown days
_INITIATIVE_NPCS        # ["marcus","nora","zoe","eli","martha","lena","sam","natalie"]
_INITIATIVE_WEIGHT      # {"high":3, "medium":2, "low":1}
_VARIANT_WEIGHTS        # variant_id → weight (atmospheric=4 default, familiar=3, close=2, very_close=2, invitation=2, date=1)
_VARIANT_MIN_TIER       # variant_id → minimum tier (default 0)
_INV_VARIANTS           # set — variants that create invitations (excluded while one is active)
_DATE_VARIANTS          # set — date invite variants (require CLOSE tier + romance eligibility)
_DATE_INVITE_COOLDOWNS  # npc_id → days between date offers
```

### Per-NPC variant inventory (Phases 36–41)

Each NPC has:
- 2–4 **atmospheric** variants (tier 0, weight 4)
- 0–1 **invitation** variant (tier 1, weight 2, in `_INV_VARIANTS`)
- 0–1 **date** variant (tier 2, weight 1, in `_DATE_VARIANTS`) — Nora + Zoe only
- 1 **familiar** variant (tier 1, weight 3)
- 1 **close** variant (tier 2, weight 2)
- 1 **very_close** variant (tier 3, weight 2)

### Date eligibility helpers

```python
_date_route_eligible(npc_id)   # route check only: not permanently closed + romance_is_open()
_date_offer_eligible(npc_id)   # route + 12/14-day offer cooldown (used in variant filtering)
```

Acceptance labels and WED scene guards use `_date_route_eligible` (no cooldown).  
`_avail_initiative_variants` uses `_date_offer_eligible`.

### Active invitation flow

When player accepts a date/park invite:
- `npc_invitation_pending` = `{"npc_id", "invitation_id", "target_location", "accepted_day", "expiry_day"}`
- WED entry fires the scene when player visits the right location within expiry.
- On completion: `store.npc_invitation_pending = None`.

`_INVITATION_META` (phone.rpy) maps invitation_id → `{"npc_id", "location_text", "display_text"}` for the Active Plan card.

---

## World Event Dispatch (WED)

`WED_REGISTRY` in `world_events.rpy` — dict of event defs:
```python
"event_key": {
    "type": "personal",          # or "ambient"
    "label": "wevent_...",       # Ren'Py label to call
    "locations": ["location_bar"],
    "min_day": 1, "once": False, # once=False allows repeat triggers
    "priority": 2, "cooldown": 0,
    "conflict_npc": None,
    "condition": lambda: ...,    # evaluated on location entry
}
```

`wed_fire("event_key")` — marks fired (for `once=True`) and calls the label.  
`_wev_relbar_open(npc_id)` / `_wev_relbar_close()` — show/hide relationship panel during scene.

---

## CG & Scene Conventions

**A-E beat structure:**
- A. Establishing — bg + sprite, 2–5 short lines
- B. Build-up — expression change, important choice
- C. Peak — `scene cg_X with dissolve`, 1–3 lines max
- D. Aftermath — back to bg+sprite
- E. Trace — flags set, optional follow-up text

**CG placement rule:** one CG per breakthrough scene, at emotional/physical peak only. Return to bg+sprite immediately after (not whole scene on CG).

**Sprite micro-animations** (images.rpy transforms):  
`react_bounce`, `react_shake`, `react_step_back`, `react_lean_in`, `react_nod`, `react_sigh`  
Usage: `show nora_cafe_smile at sprite_r, react_bounce`  
Per-character dominant sets — Martha: nod/step_back (0–2 max); Zoe: bounce/shake/lean_in (3–5).

---

## Key Engine Helpers — Always Use These

| Task | Use | File | Never do |
|---|---|---|---|
| Spend money | `try_spend(amount)` | gains.rpy | `store.money -= cost` |
| NPC outfit | `npc_sprite(npc_id, context)` | interact.rpy | hardcode sprite names |
| Dates | `npc_date` v2 + `record_date_outing` | interact.rpy | hand-roll date logic |
| Jealousy | `check_jealousy` (gates on `romance_is_open`) | interact.rpy | gate on raw affection |
| Scripted hugs | `record_forced_hug(npc_id)` | interact.rpy | skip consent gate inline |
| Worn-out check | `store.last_day_worn_out` | data.rpy | `worn_out()` after sleep |
| Relationship changes | `_apply_aff(npc, delta)` / `_apply_trust(npc, delta)` | interact.rpy | `setattr` directly |
| Social counter | `fs_record_social(npc_id, type)` | — | — |
| Jealousy counter | `record_social_attention(npc_id, type)` | — | — |

---

## Ren'Py Syntax Gotchas

- `menu:` must have a colon; items indent one level; labels after `"text":` not `"text":`+label.
- `use=` only valid on `screen` statements, not on `menu`.
- `frame` padding is a 4-tuple `(left, top, right, bottom)`; `vbox`/`hbox` use `spacing`.
- Text properties go on `_text` style child, not the label itself.
- Variable backgrounds: `scene expression cafe_bg() with dissolve` (not `scene cafe_bg()`).
- `init python` runs once at startup — don't put save-state logic there; use `default` vars.
- All `default` vars must be in `data.rpy` for save compatibility. Never add `default` inside a label.

---

## Implemented Phases Summary

| Phase | What was built |
|---|---|
| 1–29 | Core engine, careers (corporate/IT/hospital/culinary/trainer), NPC arcs, CG sequences, romance system, phone UI |
| 30–32 | NPC-initiated texting foundation: `_check_npc_initiative`, cooldowns, variant/tier filtering |
| 33–34 | Topic arcs, post-scene follow-up texts |
| 35 | Standard talk accounting fix |
| 36 | Relationship-aware texting: tier thresholds, circular chat avatars, weighted variant selection |
| 37 | Romance-aware NPC-initiated date pilot: Nora (Static bar) + Zoe (beach); WED scenes; Active Plan card |
| 38 | Wave 2 texting rollout: Martha, Lena, Sam, Natalie — 2 atmospheric variants each |
| 39 | Tier-specific content pilot: FAMILIAR + CLOSE variants for Marcus, Nora, Zoe, Eli |
| 40 | Tier-specific content wave 2: FAMILIAR + CLOSE variants for Martha, Lena, Sam, Natalie |
| 41 | VERY_CLOSE variants (tier 3, weight 2) for all 8 NPCs; soft consecutive-sender 0.5 weight penalty |

---

## Implemented CG Scenes

| Label | Folder | Trigger |
|---|---|---|
| `eli_find` | scenes/eli_find/ | own_metal_detector + eli_met at beach |
| `martha_rooftop_scene` | scenes/martha_rooftop/ | martha_aff≥40, trust≥35, hour≥19, end of corp_work_martha |
| `nora_rent` | scenes/nora_rent/ | nora_trust≥30, nora_aff≥30, nora_closing_done |
| `sam_gym_scene` | scenes/sam_gym/ | sam_aff≥35, sam_trust≥25, hour≥18 |
| `zoe_beach_night_scene` | scenes/zoe_beach_night/ | zoe_aff≥40, hour≥20 |
| `lena_rooftop_scene` | scenes/lena_rooftop/ | job_rank≥1, lena_trust≥25, hour≥22 |
| `nora_closing_scene` | scenes/nora_closing/ | nora_aff≥40, hour≥19 |
| `zoe_beach` | scenes/zoe_beach/ | — |
| `elle_pier` | scenes/elle_pier/ | — |
| `marcus_court` | scenes/marcus_court/ | — |

Interaction CGs (kiss/hug): `images/characters/{name}/{name}_kiss.png` / `{name}_hug.png`  
Declared as `cg_{name}_kiss` / `cg_{name}_hug` in images.rpy.

---

## Item Design Rules

- No item unless it unlocks at least one activity, scene, location, or unique dialogue.
- +stat alone is not a valid reason to add an item.
- Wardrobe tiers → location access (not APP bonuses).
- Jewelry tier 3: some NPCs react negatively (Nora: inauthentic; Martha: trying too hard).
- Cars: upkeep cost + new locations/dates; luxury car alienates some NPCs.

---

## Hard Constraints (do not violate)

- Do not make travel consume time.
- No romance/flirting/physical affection for non-romanceable NPCs.
- Do not terminate careers or permanently lock romance routes in code changes.
- Do not add new NPCs, assets, CGs, or romance routes unless explicitly specified.
- Do not change Zoe's Phase 6C conversation.
- Do not modify onboarding, economy, map or event frequency without a spec.
- Do not hardcode one shared cooldown for every NPC.
- All `default` state vars go in `data.rpy`.
- Never use `store.money -= cost` outside of rent.
- Never skip `_apply_aff`/`_apply_trust` in favour of direct attribute writes.
- Without running Ren'Py, say "no obvious issues during static inspection" — not "no syntax errors".
