# To Generate - asset backlog

What still needs AI-generating, split by type so you know what to make. Driven by
the new skills + careers scaffold in `game/careers.rpy` and `game/data.rpy`.

- **[icons.md](icons.md)** - UI + skill + venue icons (mostly DONE)
- **[locations.md](locations.md)** - background art for venues (mostly DONE)
- **[characters.md](characters.md)** - sprites for NPCs (7 done, rest listed)
- **[events.md](events.md)** - scripted career scenes (bg + who needed)
- **[scenes.md](scenes.md)** - story/relationship scenes to build now that
  we have a full cast (most reuse existing art; flags the few new images needed)
- **[phone.md](phone.md)** - phone home-screen look + app-icon sheet (rounded
  square tiles; the phone already runs frameless, this is the polish pass)

## The skill + career model (context)

**Core stats** (0-100): STR, INT, CHR, APP - trained by generic activities.
**Professional skills** (0-10): Medicine, Programming, Business, Cooking, Fitness,
Mechanics, Art - LEARNED at the college / on the job, and they **gate careers**.

**Careers** are rank ladders gated by stats + a pro skill (see `careers.rpy`):

| Career | Venue | Pro skill | Ladder (bottom -> top) |
|---|---|---|---|
| Medicine | City Hospital | Medicine | Med Student -> Resident -> Doctor -> Attending -> Chief |
| IT | The Hub | Programming | Junior -> Mid -> Senior -> Team Lead -> Eng. Manager |
| Corporate | Nexus Tower | Business | Intern -> Associate -> Analyst -> Manager -> Director |
| Trainer | Iron Gate Gym | Fitness | Assistant -> Trainer -> Head Trainer |
| Culinary | Eleven (restaurant) | Cooking | Commis -> Line Cook -> Sous Chef -> Head Chef |
| Warehouse | LogiCity | Mechanics | Floor -> Crew Lead -> Supervisor (stays scheduled) |
| Café (no ladder) | Grounds | - | Barista (flat, CHR + money + Nora) |

Top tiers unlock **flexible hours** = the freedom payoff.

## Done so far
- ✅ Icon sheets A + B (stats, skills, venues). Only `skill_music` + `icon_flea_market` missing.
- ✅ Backgrounds: hub (day/night), college, hospital (exam/night), bank (day/night),
  nightclub, rooftop bar, airport VIP lounge.
- ✅ Sprites + wired NPCs: Nora, Marcus, Martha, Caroline, Dr. Lena, Natalie, Elle,
  Zoe, Sam, Eli, Kai.
- ✅ Careers live: IT (Hub), Medicine (Hospital), Corporate (Nexus), Warehouse, Café.
- ✅ University degree system (Bach/Mast for Med/CS/Biz) — gating career entry + promotions.
- ✅ Dress code requirement (stat_app) on hospital, IT, corporate entry.
- ✅ Quest/goals system — phone Goals app, 11 state-driven quests.
- ✅ Debt + loan system, bank app.
- ✅ Daily events / SMS system, NPC contacts.
- ✅ NPC anger system — `sprite_angry` key wired, blocked actions, contextual hint.
- ✅ Group interactions — 3-way conversation when two related NPCs are co-present
  (Marcus+Sam at park, Nora+Kai at café, Zoe+Elle at nightclub).
- ✅ Marcus intro with character creation (2 dialogue choices → starting stat spread).
- ✅ Map image optimised: 5068×2764 → 1920×1080 (56 MB VRAM → 8 MB).

## Art gaps (what's still missing)
- **Angry sprites** — Marcus, Zoe, Elle, Sam, Eli (5 sprites; Nora+Kai done).
- **`flea_market_day`** — weekend market uses `mallday` placeholder.
- **`icon_flea_market`** — flea market tile uses `icon_mall` placeholder.
- **`skill_music`** icon — music skill has no icon yet.
- **Quayside backgrounds** — `anchor_night`, `terrace_day`, `terrace_night` (new zone).
- **Zone map PNGs** — `z_nadbrzeze_idle/hi/mask.png` for the new map zone.
- **`hospital_reception`** — needed for medicine promotion scene.
- **`phone_wallpaper`** — polish pass for phone home screen.
- **New NPCs** — Dave, Victor, Head Chef (career), Anna/Priya/Dante (world).
- **Outfit variants** — Marcus sport, Lena casual, Martha cocktail.
- **Martha rooftop scene** — 5 CGs (only story scene still missing).

## Priority order (now)
1. **Angry sprites** (5 NPCs) — anger system is live, just missing the art.
2. **`flea_market_day`** + **Quayside backgrounds** — new zone has no art.
3. **Zone map PNGs** (`z_nadbrzeze_*`) — map zone is wired but invisible.
4. **`icon_flea_market`** + **`skill_music`** icons — small, low-effort.
5. **Martha rooftop CGs** — only story scene left (scenes.md).
6. **Career NPCs** — Dave, Victor, Head Chef (unlock career events).
7. **World NPCs** — Anna, Priya, Dante (populate locations).
8. **Outfit variants** + **`phone_wallpaper`** — polish.
