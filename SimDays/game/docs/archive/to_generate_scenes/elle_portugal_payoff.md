# Elle — Portugal Payoff (Beach Decision)

## Metadata
- **Scene ID:** scene_elle_portugal_payoff
- **NPC:** Elle
- **Scene category:** Breakthrough / Resolution
- **Relationship stage:** Affection 35+, Trust 30+
- **Required flags:** elle_abroad_revealed, elle_pier_done
- **Location:** Beach (location_beach / location_sandbeach)
- **Time of day:** Late afternoon or evening (hour >= 17 preferred)
- **Repeatable:** No
- **Estimated duration:** 1h

## Why this scene exists
Elle revealed she had been offered a marine research position in Portugal (arc_elle_travel_2). The player heard about it — and the arc ended without a payoff. This scene is that payoff: she tells the player what she decided. The player's earlier response to her dilemma branches the outcome.

## New assets required

### CG 1: Elle at the Water's Edge

**Filename:** `cg_elle_portugal_turn.png`

**When it appears:** At the emotional peak — Elle has just said something that requires a moment to land. She turns toward the player. This is the CG.

**Camera:** Medium shot, slight elevation — the player's POV, standing a few steps behind and slightly above Elle who is at the waterline.

**Framing:** Elle in center-left, face in three-quarter turn toward viewer. Water behind her. Late afternoon light. Open sky.

**Characters:** Elle only. Player implied from POV.

**Positioning:** Elle is at the waterline, shoes off (implied by posture and wet sand). She has turned her head — not dramatically, the way you turn when you hear your name. Natural, half-expecting the player.

**Pose:** Relaxed but alert. Weight on one foot. Arms loose. She's not performing anything — she was standing here thinking, and now the player arrived.

**Expression:** Quiet. Something decided behind the eyes. Not sad, not happy — the specific stillness of a person who has made a real choice and is done weighing it.

**Environment:** Sandy beach, late afternoon. Water in background — could be sea or large lake. Golden-hour or pre-sunset light. No crowds. Bare feet implied (shoes not visible or seen at the edge of frame).

**Lighting:** Warm late-afternoon directional light from low angle. Catches her face and shoulder. Water behind her is softer, slightly overexposed.

**Continuity requirements:** Elle's standard sundress outfit (`elle_sundress_normal`). Hair as standard. Bare feet optional but preferred.

**What must NOT appear:** Drama. No wind-blown hair, no tears, no cinematic pose. Elle is someone for whom this moment is significant but contained. The image should feel like a candid catch — she happened to turn.

**Generation prompt:** *A young woman in a sundress standing at the water's edge on a sandy beach, turning her head three-quarters toward the viewer. Late afternoon golden light. Barefoot, weight on one foot, relaxed posture. Expression: composed, something quietly decided in it — not sad, not dramatic. Water behind her catches the light. The shot is from slightly behind and above, as if the viewer has just walked up to her. Visual novel CG, semi-realistic style, 1920x1080.*

## Existing assets to reuse
- **Backgrounds:** `beachday`, `beachnight` (day/night expression switch based on hour)
- **Sprite:** `elle_sundress_normal` — used before and after CG

## Background requirements
None new. `beachday` / `beachnight` expression covers the time-of-day variation.
