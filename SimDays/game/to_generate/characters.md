# Character sprites to generate

Front-facing, transparent PNG, ~1086x1448. Painterly anime-realistic style.
Drop under `images/characters/<name>/`, filenames: `<name>_normal/talk/laugh/angry` etc.

---

## ✅ Done (wired NPCs)

Nora, Marcus, Martha, Caroline, Dr. Lena, Natalie, Elle, Zoe, Sam, Eli, Kai — all
main sprites exist and are wired. Kai's `kai_angry.png` renamed from typo.

**Angry sprites done:** `nora_cafe_angry.png`, `kai_angry.png`

---

## ❌ Angry sprite variants (5 remaining)

The `sprite_angry` key is live in `NPC_DATA` (interact.rpy). Wire up after
generating by adding `"sprite_angry": "marcus_angry"` etc. to each NPC entry.

Each is a **single expression** — same format as normal sprites.

| NPC | Save path | Description hint |
|---|---|---|
| Marcus | `characters/marcus/marcus_angry.png` | Arms at sides, jaw set, not impressed |
| Zoe | `characters/zoe/zoe_punk_angry.png` | Cold stare, slight sneer — more edge than usual |
| Elle | `characters/elle/elle_angry.png` | Quiet displeasure, turned slightly away |
| Sam | `characters/sam/sam_angry.png` | Flat stare, athlete's stillness when annoyed |
| Eli | `characters/eli/eli_angry.png` | Visibly uncomfortable, arms folded |

> Lower-priority: Caroline, Lena, Natalie, Martha — career NPCs whose affection
> doesn't reach jealousy thresholds in normal play.

---

## ❌ Outfit variants (existing characters)

### Marcus — sport outfit
`images/characters/marcus/marcus_sport_normal/talk/laugh.png`
For "Shoot hoops" scene and gym encounters.
```
Full body portrait, young Black man ~23, athletic build, basketball shorts and sleeveless
jersey/vest, slightly sweaty, relaxed confident posture, front-facing, transparent background,
painterly anime-realistic, outdoor daylight
```
3 expressions: `normal`, `talk`, `laugh`

### Dr. Lena — casual/off-duty
`images/characters/dr_lena/drlena_casual_normal/talk/thoughtful.png`
For "Rooftop 3am" scene (already generated as CG, but sprite needed for dialogue).
```
Full body portrait, woman ~30, doctor, off-duty: casual top, hair down or loosely tied,
tired but reflective expression, front-facing, transparent background, painterly
anime-realistic, night lighting, softer than her work persona
```
3 expressions: `normal`, `talk`, `thoughtful`

### Martha — cocktail dress ✅ DONE
`martha_dress_normal`, `martha_dress_talk`, `martha_dress_laugh`, `martha_dress_angry` — all on disk.
Wire into `images.rpy` and use in `martha_rooftop` scene.
Note: one unnamed ChatGPT Image Jul 7, 09_50_40 PM.png in the folder — rename once identified.

---

## ❌ World NPCs (new characters)

### Anna — `images/characters/anna/`
Café regular, Tue/Thu afternoons. Folder exists but files need proper naming/generation.
```
Full body portrait, young woman ~24, average looks, bookish vibe, casual cozy outfit
(knit top or cardigan), soft expression, slightly introverted but warm,
front-facing, transparent background, painterly anime-realistic, café lighting
```
4 expressions: `anna_normal`, `anna_talk`, `anna_laugh`, `anna_surprised`

### Priya — `images/characters/priya/`
Mall stylist, afternoons. Trendy, sharp eye, confident.
```
Full body portrait, young woman ~25, South Asian features, fashionable outfit (she works
in a clothing store — put-together but approachable), confident posture,
front-facing, transparent background, painterly anime-realistic, mall/shop lighting
```
4 expressions: `priya_normal`, `priya_talk`, `priya_laugh`, `priya_annoyed`

### Dante — `images/characters/dante/`
Bar regular / fixer, nights. Risky-favour energy, charming.
```
Full body portrait, man ~30, dark features, slightly rough around the edges, casual but
deliberate outfit (leather jacket / open shirt), one of those people who always knows
someone who knows someone, front-facing, transparent background,
painterly anime-realistic, bar/night lighting
```
4 expressions: `dante_normal`, `dante_talk`, `dante_laugh`, `dante_serious`

---

## ❌ Career NPCs

### Dave — `images/characters/dave/`
IT senior dev at The Hub. Mentor figure.
```
Full body portrait, man ~35, glasses, slightly tired tech-worker energy, smart casual
(button shirt + jeans), knows everything but patient about it,
front-facing, transparent background, painterly anime-realistic, office lighting
```
4 expressions: `dave_normal`, `dave_talk`, `dave_laugh`, `dave_serious`

### Victor — `images/characters/victor/`
Gym owner / trainer mentor. Unlocks trainer career.
```
Full body portrait, man ~50, big build, weathered face, gruff but warm,
gym wear (polo/vest), the kind of guy who's seen every excuse,
front-facing, transparent background, painterly anime-realistic, gym lighting
```
4 expressions: `victor_normal`, `victor_talk`, `victor_laugh`, `victor_stern`

### Head Chef — `images/characters/headchef/`
Boss at Eleven kitchen. Intense, exacting.
```
Full body portrait, man ~45, chef whites, intense focused expression, clearly someone
who does not tolerate mistakes, front-facing, transparent background,
painterly anime-realistic, kitchen lighting
```
4 expressions: `headchef_normal`, `headchef_talk`, `headchef_angry`, `headchef_satisfied`
