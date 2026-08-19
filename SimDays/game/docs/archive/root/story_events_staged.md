# Story Events — Staging / Shot Breakdown

Production view of the 30 events in [story_events.md](story_events.md): for each event — **when + lighting**, **backgrounds**, **sprites/poses**, and a **beat-by-beat staging** (what's on screen, who, where, camera framing, ambient touches). Dialogue lines live in story_events.md; here we direct the visuals. New assets to make are marked 🆕 and collected at the bottom.

**Conventions**
- Positions: `L / C / R` (left/center/right third). Dialogue rule we set: speaking NPC on **R** so left-side activity/choice UI never covers them.
- "POV / no MC" = first-person framing, MC not drawn. **Open decision:** do we ever draw the male MC? If yes we need an MC sprite set; if no, all "cut to MC" beats become POV reaction text + maybe a bg shift. I've written both options where relevant.
- Lighting tags: `dawn / day-bright / golden / dusk / night`. Park/beach/outdoor events specify sun + soft ambient elements.
- bg names in `code` already exist (webp); 🆕 = needs generating.

---

# MARCUS — staging

## M-1 · The Tour — *Sat, day-bright*
- **BG:** `map_city` (or a 🆕 `street_downtown_day` for a grounded street feel), then `parkday`, pass `bar` exterior. Bright midday, light breeze, a few pedestrians as ambient.
- **Sprites:** `marcus_neutral` 🆕, `marcus_point` 🆕 (arm raised, pointing).
- **Staging:**
  1. [bg street/map] Marcus C, `marcus_point`, gesturing off-screen — "That's the park…". Sunny, warm grade.
  2. Quick bg swap to `parkday` as he name-drops the park (no sprite move, just locale flash).
  3. Back to street; Marcus R, `marcus_neutral` — café/job nudge.
  4. End beat: small street-food stall ambient; both off to eat (fade). 

## M-2 · Twenty Bucks — *anytime, matches current locale*
- **BG:** wherever it triggers (home `cheaphouse_day/night` or `bar`). Keep current lighting.
- **Sprites:** `marcus_smile` 🆕, prop: he holds out a folded bill (bake into a `marcus_offer` pose 🆕 or just dialogue).
- **Staging:** Marcus R, `marcus_smile`; close, low-key. No bg change. Intimate framing (he's doing you a quiet favor).

## M-3 · Ball — *Sat afternoon, day-bright* ⭐ your example
- **BG:** 🆕 `park_court_day` — outdoor basketball court inside the park: chain-link, sunny, long soft shadows, trees behind, a water bottle on the ground, faint city skyline. Bright, light lens flare, leaves.
- **Sprites:** 🆕 `marcus_ball` (athletic wear, basketball under arm, grinning), 🆕 `marcus_dribble` (optional action pose).
- **Staging:**
  1. [bg park_court_day] Establishing — empty court, Marcus C-R with `marcus_ball`, bouncing it. "You hoop?" Bright daylight, ambient: distant kids, birds.
  2. Choice appears (left panel) — Marcus stays R so panel doesn't cover him.
  3. **"Cut to MC" beat** (the reverse you mentioned): if we draw MC → show MC L/POV catching a pass; if no MC → keep bg, narration "He fires a pass; you barely catch it," Marcus reacts.
  4. Win/lose flavor: `marcus_ball` → swap to a laughing `marcus_smile`. Sun lower if it ran long (optional `park_court_golden` 🆕).

## M-4 · Movie Night — *evening, night (indoor, dim warm)*
- **BG:** 🆕 `marcus_apt_night` — his studio, TV glow, couch, soda cans, dim warm light + flickering blue TV cast. (Or reuse `cheaphouse_night` dressed differently — but his place should differ.)
- **Sprites:** `marcus_neutral`, 🆕 `marcus_laugh`, 🆕 `marcus_soft` (quiet/serious for the dad beat).
- **Staging:**
  1. [bg marcus_apt_night] Marcus R on couch, `marcus_laugh`, quoting the movie. TV-glow rim light.
  2. Choice beat — left panel, Marcus R.
  3. End quiet beat: lights lower, `marcus_soft`, the dad line. Warmer, slower. Trust beat.

## M-5 · Bad Shift — *evening, night (bar interior)*
- **BG:** `bar` (existing) — amber + neon, moody. Maybe a 🆕 `bar_empty_night` (no patrons, closing) for the off-the-clock version.
- **Sprites:** 🆕 `marcus_tired` (jaw tight, towel over shoulder), `marcus_neutral`.
- **Staging:**
  1. [bg bar] Marcus behind counter R, `marcus_tired`. Low amber, red/blue neon glow.
  2. Vent choice → if "buy him a drink", swap to `bar_empty_night`, the two of you at the counter, softer.

## M-6 · Hangover Run — *early morning, day-bright (harsh)*
- **BG:** `cheaphouse_day` (your door) then his `marcus_apt_day` 🆕 (or reuse). Over-bright morning, slightly washed (hangover gag).
- **Sprites:** 🆕 `marcus_hungover` (sunglasses indoors, slumped), `marcus_smile`.
- **Staging:** Marcus R at your doorway, `marcus_hungover`, sunglasses. Comedic over-bright grade. Cut to breakfast (his apt) — `marcus_smile`.

## M-7 · The Dream — *late night, night (bar, near-empty)*
- **BG:** 🆕 `bar_empty_night` (closing, chairs up, single light over counter). Intimate, low.
- **Sprites:** `marcus_soft`, `marcus_neutral`.
- **Staging:** Marcus R wiping counter slow, `marcus_soft`. Single warm key light, rest in shadow — confessional mood. Choice = left panel.

## M-8 · The Lease — *day, neutral (his apt or a café table)*
- **BG:** `marcus_apt_day` 🆕 or `cafeday`. Daylight, businesslike but hopeful.
- **Sprites:** `marcus_neutral`, 🆕 `marcus_hopeful`. Prop: lease papers (bake a "holding papers" variant or narrate).
- **Staging:** Marcus R with papers, `marcus_hopeful`. If "read the lease" (INT) — insert a close-up bg 🆕 `lease_paper_closeup` (optional) for the clause-catch beat.

## M-9 · Rough Patch — *dusk/evening, low warm*
- **BG:** `parkday`→ 🆕 `park_dusk` (golden-to-blue, benches, quiet) OR `bar_empty_night`. Subdued.
- **Sprites:** `marcus_soft`, 🆕 `marcus_down` (slumped, looking away).
- **Staging:** Marcus R on a bench, `marcus_down`, not looking at you. Cool dusk grade. "Just sit with him" choice = lingering hold, minimal motion. Trust beat.

## M-10 · Opening Night / Last Call — *night, celebratory OR bittersweet*
- **BG (good):** 🆕 `marcus_bar_night` — his own warm, characterful bar (string lights, his style). Lively, glowy.
- **BG (down):** `bar` or `park_dusk` — quieter.
- **Sprites:** 🆕 `marcus_proud` (grin, arms open), `marcus_soft`.
- **Staging:** Good path: [bg marcus_bar_night] Marcus C-R, `marcus_proud`, toast raised; warm crowd ambient, string-light bokeh. Down path: quieter, `marcus_soft`, two of you, soft light.

---

# ZOE — staging

## Z-1 · Refill — *day, café (day-bright through windows)*
- **BG:** `cafeday`. Warm window light.
- **Sprites:** `zoe_punk_smile` (have), `zoe_neutral` (have).
- **Staging:** Zoe R behind counter, `zoe_punk_smile`. Light banter. Choice = left panel (she stays R).

## Z-2 · The Sketchbook — *day, café*
- **BG:** `cafeday`. Cozy.
- **Sprites:** `zoe_neutral`, 🆕 `zoe_shy` (looking away, guarded), 🆕 `zoe_hopeful`. Prop: sketchbook — optional 🆕 `cg_zoe_sketch` (a close-up CG of her rooftop drawing) shown full-screen when she shares it.
- **Staging:** Zoe R, `zoe_shy` sliding the book over. Insert `cg_zoe_sketch` full-screen on "wanna see?" → back to Zoe `zoe_hopeful` for your reaction.

## Z-3 · Closing Time — *evening→night, café* ⭐ romance opener
- **BG:** `cafenight` (have). Low warm, empty café, chairs maybe up. Then 🆕 `street_night` for the walk.
- **Sprites:** `zoe_punk_smile`, 🆕 `zoe_soft` (gentle, honest). 
- **Staging:**
  1. [bg cafenight] Zoe C (no counter between you — intimate), `zoe_soft`. Music low, warm pools of light.
  2. "Walk you home" → [bg street_night] Zoe R strolling; cool night, streetlamp pools, distant signs. She points at a mural — insert 🆕 `cg_mural` (her unsigned street art) for a beat.

## Z-4 · City at Night — *night, street/rooftop*
- **BG:** 🆕 `rooftop_night` (city lights below, string of skyline) or reuse `street_night`. Cool, romantic, bokeh city.
- **Sprites:** `zoe_soft`, 🆕 `zoe_laugh`.
- **Staging:** Zoe R, `zoe_soft`; on the flirt success → `zoe_laugh`, shoulder bump (narrate). Night grade, city glow rim light.

## Z-5 · Henry — *day, café*
- **BG:** `cafeday`, slightly emptier/quieter framing.
- **Sprites:** `zoe_neutral`, `zoe_shy`, `zoe_soft`.
- **Staging:** Zoe R behind counter, `zoe_shy` → `zoe_soft` as she opens up about the café maybe closing. Daylight but a touch muted.

## Z-6 · The Wall — *night, venue* (her art shown)
- **BG:** 🆕 `art_venue_night` — a bar/gallery wall with her pieces hung, small crowd, warm spotlights on the art. Lively but nervy.
- **Sprites:** 🆕 `zoe_nervous`, `zoe_soft`, 🆕 `zoe_proud`. Optional `cg_zoe_wall` (her work on the wall) full-screen reveal.
- **Staging:**
  1. [bg art_venue_night] Zoe R, `zoe_nervous`, fidgeting before the doors.
  2. Hype-up (CHR) → `zoe_soft`.
  3. Reveal: insert `cg_zoe_wall`; crowd ambient murmur→warm reaction. Zoe finds you in the crowd → `zoe_proud`, the look. Near-confession framing (hold).

## Z-7 · First Date — *venue depends on choice*
- **BG:** by choice → `beachday`/🆕 `beach_sunset`, OR `mallday`/🆕 `gallery_day`, OR `bar`. 
- **Sprites:** `zoe_punk_smile`, `zoe_soft`, `zoe_laugh`.
- **Staging:** Zoe R, expression shifts with the date's mood; beach = golden sunset grade (`beach_sunset` 🆕), gallery = bright clean, bar = amber. End on the "read the moment" (CHR) hold.

## Z-8 · Guard Down — *night, quiet (rooftop/cafe/your place)*
- **BG:** `rooftop_night` 🆕 or `cafenight`. Intimate, low.
- **Sprites:** `zoe_soft`, 🆕 `zoe_vulnerable` (eyes down, armor off).
- **Staging:** Zoe R/C, `zoe_vulnerable`. Minimal light, close framing. Big trust beat — almost no movement, let dialogue carry.

## Z-9 · The Offer — *day, the empty future space*
- **BG:** 🆕 `empty_shop_day` — a bare retail space, dust in sunbeams, potential. Hopeful daylight.
- **Sprites:** `zoe_hopeful`, `zoe_nervous`.
- **Staging:** Zoe C in the empty space, `zoe_hopeful`, gesturing at bare walls. Sunbeams, motes. Choice = partner / back her / caution.

## Z-10 · Opening / Confession — *night, finale*
- **BG (romance/space):** 🆕 `zoe_gallery_night` — her finished gallery-café, warm, her art on the walls, fairy lights. OR `rooftop_night` if space didn't happen.
- **Sprites:** `zoe_soft`, `zoe_proud`, 🆕 `zoe_blush`. Optional `cg_zoe_kiss` if we do CGs.
- **Staging:** Zoe R→C, `zoe_blush`/`zoe_soft`; confession. Kiss option → CG or fade. Warm key light, her art glowing behind.

---

# BECCA — staging (needs full sprite set 🆕)

## B-0 · Spotter — *gym, day-bright* (meeting)
- **BG:** `gymdaypeople` (have). Bright, big windows, mirrors.
- **Sprites:** 🆕 `becca_smirk` (re-racking, confident), 🆕 `becca_neutral`.
- **Staging:** Becca C-R at the rack, `becca_smirk`, sizing you up. Bright gym light, mirror reflections ambient. Choice = left panel, she stays R.

## B-1 · Form Check — *gym, day*
- **BG:** `gymdaypeople`.
- **Sprites:** `becca_neutral`, 🆕 `becca_coach` (hands-on-hips, instructive).
- **Staging:** Becca R, `becca_coach`, correcting your stance (narrate the adjust). Bright.

## B-2 · The Bet — *gym, day*
- **BG:** `gymdaynopeople` (quieter, treadmills) or `gymdaypeople`.
- **Sprites:** 🆕 `becca_competitive` (fired up), `becca_smirk`.
- **Staging:** Becca R on a treadmill, `becca_competitive`. Race = narration + STR check; win/lose → `becca_smirk`.

## B-3 · Smoothie Talk — *gym lobby / juice bar, day*
- **BG:** 🆕 `gym_lobby_day` (juice bar, benches) or reuse `gymdaypeople` corner. Calmer.
- **Sprites:** 🆕 `becca_soft` (still, guard slipping), `becca_neutral`. Prop: smoothie cup (optional pose).
- **Staging:** Becca R seated, `becca_soft` for the "gym quiets my head" line, then deflect to `becca_smirk`. First soft beat — warmer light.

## B-4 · Her Goal — *gym, day*
- **BG:** `gymdaypeople`.
- **Sprites:** `becca_competitive`, `becca_soft`.
- **Staging:** Becca R, `becca_competitive` ("second is first loser") → `becca_soft` when she admits why it matters. 

## B-5 · Setback — *gym, day (iced shoulder)*
- **BG:** `gymdaynopeople` (quieter, she's benched).
- **Sprites:** 🆕 `becca_hurt` (ice pack, frustrated), `becca_soft`.
- **Staging:** Becca R, `becca_hurt`, arms crossed/iced. Tense. "rest" choice risk. Vulnerability — cooler, quieter framing.

## B-6 · Training Montage — *gym, day (recurring block)*
- **BG:** `gymdaypeople` (busy energy) + an evening 🆕 `gym_night` for the shoulder-lean beat.
- **Sprites:** `becca_competitive`, `becca_coach`, `becca_soft`.
- **Staging:** Series of short sessions, Becca R, `becca_competitive`/`becca_coach`. Closing quiet beat: [bg gym_night] she falls asleep on your shoulder post-session — `becca_soft`, low light, tender.

## B-7 · Competition Day — *arena, day (event)*
- **BG:** 🆕 `fitness_arena_day` — comp stage/floor, banners, crowd, bright stage light.
- **Sprites:** 🆕 `becca_nervous`, `becca_competitive`, 🆕 `becca_focused`.
- **Staging:** Becca R backstage, `becca_nervous`, grabbing your sleeve. Pump-up (CHR). Comp = montage beats (bg arena), result branch. She finds you after.

## B-8 · After the Medal — *arena/outside, golden*
- **BG:** `fitness_arena_day` → 🆕 `arena_exterior_dusk` (golden, calming down).
- **Sprites:** 🆕 `becca_emotional` (win: shining; loss: deflated), `becca_soft`.
- **Staging:** Becca R/C, `becca_emotional`. Golden hour grade, softer. Armor cracks → opens romance.

## B-9 · Off the Clock — *diner or dog park, day* (un-gym)
- **BG:** 🆕 `diner_day` (greasy booth, fries) or 🆕 `dog_park_day`. Casual, sunny, un-gym.
- **Sprites:** `becca_soft`, `becca_laugh` 🆕.
- **Staging:** Becca R in a booth, `becca_laugh` (fries gag) → `becca_soft` ("the version not trying to win"). Warm, relaxed.

## B-10 · Confession / Finale — *gym at close, night*
- **BG:** 🆕 `gym_night` (empty, lights half-down, just the two of you).
- **Sprites:** `becca_soft`, `becca_emotional`, 🆕 `becca_blush`.
- **Staging:** Becca R→C, `becca_blush`, the blunt-but-earnest ask. Low gym light, quiet. Kiss/“let me win a race” option.

---

# 🆕 NEW ASSETS TO GENERATE (consolidated)

### Backgrounds (with time/lighting)
- `street_downtown_day` · `street_night`
- `park_court_day` (+ optional `park_court_golden`) · `park_dusk`
- `marcus_apt_day` · `marcus_apt_night`
- `bar_empty_night` · `marcus_bar_night` (his own bar, warm)
- `rooftop_night`
- `art_venue_night` · `empty_shop_day` · `zoe_gallery_night` · `gallery_day`
- `beach_sunset`
- `gym_lobby_day` · `gym_night` · `fitness_arena_day` · `arena_exterior_dusk`
- `diner_day` · `dog_park_day`
- (optional close-ups) `lease_paper_closeup`

### Character sprites / expressions
- **MARCUS (full set 🆕):** neutral, smile, laugh, soft, tired, hungover, hopeful, down, proud, point, ball/dribble.
- **BECCA (full set 🆕):** neutral, smirk, coach, competitive, soft, hurt, nervous, focused, emotional, laugh, blush.
- **ZOE (add to existing):** shy, hopeful, soft, laugh, nervous, proud, vulnerable, blush.

### Optional CGs (full-screen story moments)
- `cg_zoe_sketch` · `cg_mural` · `cg_zoe_wall` · `cg_zoe_kiss`

### Decision needed
- **Draw the male MC or keep POV?** If drawn, add an MC sprite set (a few outfits/expressions) for the "cut to MC" beats; if not, those beats stay first-person.

---

## How to read this when generating
For each event: make the **background** at the stated time-of-day (lighting tag), then the **sprites/poses** listed. Sprites always framed to sit **right** (R) so the left activity panel never covers them. Reuse existing `code` bgs where listed; only the 🆕 are new. Tell me which to prioritize and I'll prep prompts + cut/clean them like the others.
