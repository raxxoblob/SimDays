# Unexpected Metro Ride with Marcus

## Metadata
- **Scene ID:** marcus_metro_unexpected
- **NPCs:** Marcus
- **Scene category:** A
- **Relationship stage:** Affection 15-40, any trust
- **Trigger conditions:** MC is traveling via take_metro, day % 7 in {0,1,2,3,4} (weekday), hour between 17-20, marcus_affection >= 15
- **Required flags:** none (marcus is a world character — always known)
- **Blocking conditions:** marcus_metro_done = True (fires once per week maximum, not once-ever); or marcus_affection == 0
- **Location:** Metro carriage (in transit — uses take_metro label as hook point)
- **Time of day:** Evening commute, 17:00-20:00
- **Repeatable:** Yes (weekly cooldown — uses a day-based flag `_marcus_metro_last` to allow once per 7 days)
- **Estimated duration:** 0.25h (time already consumed by take_metro)
- **Commitment required:** no
- **Item required:** none (only fires when car_tier == 0 — player is using the metro)
- **Priority:** medium

## Why this scene exists
Marcus has no casual "bumping into" scene during daily transit. His current content is concentrated at the park (morning jogs), the bar (evenings), and at home (dinner). There's no scene that captures what he's actually like when he's not hosting or being hosted — when he's just a person on the way somewhere. This fills the gap between "acquaintance at the bar" and "close friend," giving the relationship a sense of daily life rather than event-based progression.

Additionally: this scene is only reachable when the player doesn't own a car. It subtly frames car ownership as a social fork — different NPCs, different rhythms.

## Narrative purpose
Show Marcus as grounded, observational, and low-pressure. He doesn't need the conversation to go anywhere. He's comfortable with quiet. This scene builds trust by letting him simply be present without an agenda — which is rare in a game where NPCs usually want something from you.

## Full scene summary
The player is taking the metro (take_metro label, no car). The carriage is crowded enough that they almost miss Marcus — he's standing near the doors, headphones around his neck (not on), watching the city slide past. He clocks them immediately.

He doesn't make a big deal of it. Moves over to make room. The ride is 15-20 minutes of easy back-and-forth — where they're each coming from, why they're both still on the metro at this hour. Marcus mentions something happening on his end (varies by relationship stage). The player has 2-3 beat choices. Scene ends when one of them gets off, or if they're going the same way, they walk a block together before splitting.

No affection is guaranteed. The scene can end neutral or even slightly negative depending on choices. Its primary value is trust-building through mundane shared time.

## Emotional progression
- **Initial state:** Both tired after a weekday. Low-stakes encounter.
- **Tension:** None structural — the "tension" is in what each says or doesn't say about their day. Marcus notices when something's off. Player can deflect or open up.
- **Opening:** Marcus spots the player first. A brief nod — he's not the type to shout across a carriage.
- **Player choice:** How much to share about their day. Whether to ask about his.
- **Result:** Depending on choices, ends with +1-3 trust, neutral, or a slight warmth that's hard to name.
- **Relationship trace:** Scene sets a flag `marcus_metro_last = day` for cooldown tracking. If the player shared something honest, unlocks the `marcus_metro_opened` flag which unlocks deeper greeting dialogue.

## Player choices

**Choice 1** — Marcus: "Coming from work? You've got the look."
- Option A: "Yeah. Long one." → Marcus nods. "Those hit different on the metro. You get to sit with it." +1 trust. He stays quiet for a beat before offering something small in return.
- Option B: "I'm fine. Where are you coming from?" → Redirecting. Marcus doesn't push. He says he's been at the park (or the bar, depending on hour). Neutral. No trust change.
- Option C: "Is it that obvious?" → Marcus laughs quietly. "You're still doing the stare-at-the-middle-distance thing." +1 affection. Light. He seems pleased he read it right.

**Choice 2** (only if Option A or C chosen) — A small, genuine exchange:
- Marcus mentions something on his end. If marcus_trust >= 20: he mentions his dad briefly — a good day visiting, or a difficult one. No elaboration. Player can acknowledge or let it land.
  - Acknowledge: "That sounds hard." / "Glad it was a good day." → +2 trust.
  - Let it land (say nothing, just look at him): → +1 trust. He seems to prefer this.
- If marcus_trust < 20: he just mentions the park run, someone he raced who pushed him harder than expected. Lighter.

**Choice 3** — The parting:
- Same stop: they walk a block. Marcus says "Same time tomorrow, maybe." Doesn't mean it literally — just the kind of thing said to someone you don't mind running into.
- Different stop: one of them gets off. Short wave. Marcus: "Don't work yourself flat, yeah?"

## Physical interaction
No physical contact in this scene. They're standing in a crowded metro carriage. Proximity is incidental — they might be holding the same overhead rail, shoulders close but not touching. This is intentional: the emotional closeness of the scene comes from words and presence, not gesture.

## Follow-up opportunities
- Next time MC encounters Marcus at the park or bar, his greeting upgrades slightly: "Still taking the metro?" or a reference to what the player shared.
- If `marcus_metro_opened` is set, unlocks a new topic arc for food or sports that references the commute conversation.
- If the player got a car after this scene and Marcus finds out, he teases them once: "Look at you. No more metro mornings."

## Existing assets to reuse
- Background: `centerstreet_night` or `centerstreet_day` — neither is actually a metro interior. See new assets below.
- Sprites: `marcus_casual_normal`, `marcus_casual_talk`
- Expressions: normal, laugh (available)
- CGs: none

## New assets required
- **Background:** `metro_interior_evening` — metro carriage, standing passengers implied but not shown, warm artificial lighting, large window showing city blurring past at dusk. One new BG.

## CG count
**None.** This is a small, everyday scene. The metro interior background + sprite is sufficient. A CG here would inflate the emotional weight past what the scene earns.

## Sprite requirements
Existing `marcus_casual_normal` and `marcus_casual_talk` are sufficient. Marcus should appear at `sprite_c` (center) since it's a contained space — or `sprite_l` if implying he's by the doors.

## Background requirements
New background needed: `metro_interior_evening`. Requirements:
- Interior of a metro carriage, evening light, slightly crowded feel (suggest passengers without explicitly drawing NPCs)
- Window on one side showing blurred city/night sky
- Warm yellow artificial carriage lighting
- Handrails visible
- Filename: `metro_interior_evening.png`
- Prompt: *Interior of a modern metro carriage at evening rush hour. Warm yellow overhead lighting. Large windows on the right showing city lights blurring past in motion. Handrail bars visible. A sense of mild crowding — implied passengers, slight crowd noise. Clean, realistic visual novel background style. 1920x1080.*

## Ren'Py implementation notes
- Hook into `take_metro` label — add a conditional check before the "fifteen minutes" narration line
- Condition: `car_tier == 0 and marcus_affection >= 15 and day % 7 < 5 and 17 <= hour < 20 and day - _marcus_metro_last > 6`
- `_marcus_metro_last` defaults to -99 in data.rpy
- Scene triggers, plays, then resumes normal take_metro flow
- Does NOT add spend_time — the 0.25h is already consumed by take_metro
- Uses `scene metro_interior_evening` for the scene background
- Flag needed: `default _marcus_metro_last = -99` in data.rpy

## Risks and continuity checks
- Verify take_metro can support injected conditionals without breaking its jump-to-map flow
- Scene must not fire when player is in a commitment (check `player_commitments` or skip by checking if current hour is past a commitment threshold)
- Marcus's schedule has him at the park 6-10 and bar 17-24 — so this fires during his bar window, which is slightly inconsistent (he'd be heading TO the bar, not coming from work). Handle via his dialogue: "Heading to the bar. You heading home?" This keeps it natural.
- Weekly cooldown prevents overuse; the scene is designed to feel spontaneous, not routine
