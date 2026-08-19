# Sam × Marcus — Early Morning Court

## Metadata
- **Scene ID:** scene_sam_marcus_park
- **NPCs:** Sam (female), Marcus
- **Scene category:** Crossover / Major
- **Relationship stage:** sam_affection >= 25, marcus_affection >= 25
- **Required flags:** sam_met, marcus_met, sam_marcus_scene_pending
- **Location:** location_park (basketball court)
- **Time of day:** 06:00–10:00 (Mon–Fri)
- **Repeatable:** No (MAJOR scene)
- **Estimated duration:** 1.5h

## Why this scene exists
Sam and Marcus are both at the park every morning. NPC_RELATIONS marks them as gym_friends but they only produce generic group chat. This scene converts that systemic overlap into a scripted moment: the player arrives to find them already mid-argument about training methodology, and has to pick a side.

## New assets required

### CG 1: The Three of Them at the Court

**Filename:** `cg_sam_marcus_court.png`

**When it appears:** After the player chooses a side. The argument winds down and they actually play. The CG is the moment right after the player takes a shot — mid-motion, unremarkable, familiar.

**Camera:** Medium-wide, court level. Slightly low angle — the ground is visible, the basket implied above frame.

**Framing:** Three figures in natural positions on a basketball court. Ball in the air (mid-arc, just released). Marcus watching the ball. Sam watching the player / the shot. Player implied off-left or as a near-frame presence.

**Characters:** Sam (left or center), Marcus (right). Player implied.

**Sam:** Female. Athletic build. Casual gym clothes — fitted t-shirt or tank, shorts. Natural, relaxed energy — she's at ease here. Expression: watching the shot, slight competitive attention. Not performing anything.

**Marcus:** Taller, broader. Sportswear. Arms relaxed — watching the ball, not Sam. Similar comfort level — this is their place.

**Positioning:** Both of them in natural "waiting for the outcome" posture. Not posed. The kind of stance you fall into when you've done this a hundred times.

**Environment:** Outdoor basketball court in a city park. Early morning. Concrete court, standard markings. Trees or park greenery in soft background. Low morning light — not harsh, slightly golden.

**Lighting:** Early morning — directional but soft. Long shadows on the court. Not dramatic.

**Tone:** Mundane and comfortable. This is an unremarkable morning for them. The player is included in the mundanity — that's the point.

**What must NOT appear:** Confrontation framing. Not a face-off. Not athletic drama. These are two people who come here every day and the player has joined that. The image should look like a moment between friends, not a competition.

**Generation prompt:** *Two people on an outdoor urban basketball court in the early morning — a woman (athletic, casual sportswear, relaxed expression watching a shot) and a taller man (sportswear, arms loose, watching the ball in the air). Basketball mid-arc above them. Low morning golden light, long soft shadows on the concrete. Trees in soft background. The mood is casual, familiar — this is their regular spot. Visual novel CG style, semi-realistic, 1920x1080.*

## Existing assets to reuse
- **Backgrounds:** `basketball_court_day` (used before and after CG), `parkday` fallback
- **Sprites:** `sam_normal` (Sam), `marcus_park_neutral` (Marcus) — used at sprite_r and sprite_l

## Background requirements
None new. `basketball_court_day` is already declared and used in this scene.
