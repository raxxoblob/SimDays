# Scenes — Marcus & Zoe (draft for review)

Full scripts for the first two characters. **Draft only — read, mark changes, then I implement in Ren'Py.** Protagonist = male ("You"), eventually everyone datable, focus on women. Companion to [characters.md](characters.md).

Notation:
- `You:` player line · `MARCUS:` / `ZOE:` NPC · *(italics)* = stage/narration.
- `▸ "choice"` = player option → `→ effect` (Affection/Trust deltas, flags).
- `[bg: …]` background · `[show: …]` sprite.

---

MARCUS REYES — the roommate
Met Day 1. Friendship/bro arc. Found: mornings home/park, evenings at Static (bar). Interests: basketball, cooking, old action movies. Helps you settle in; later his own arc (wants to open a bar).

SCENE M0 — Move-in day (intro, scripted, Day 1)
[bg: apartment_staircase]

The hallway is quiet. Old wooden stairs creak beneath your feet, and the faint smell of fresh paint mixes with someone's dinner cooking nearby. You stop in front of Apartment 12. It's not much... Just a small studio apartment. But for now, it's home. As you reach for your keys, you hear footsteps behind you.

A guy about your age with an easy grin turns the corner of the stairs, a dish towel over one shoulder.

MARCUS: Oh! You must be the new neighbor. I don't think we've met before. I'm Marcus.

▸ "Nice to meet you. Yeah... I just moved in today." (Earnest)
→ MARCUS +3 Affection.
▸ "Is it that obvious? I thought the heavy sighing gave it away." (Sarcastic)
→ MARCUS +2 Affection (he laughs).
▸ "Yeah. Just trying to figure out the lock." (Reserved)
→ neutral.

MARCUS: Welcome to the building! Apartment 12, huh? Small place... but it's surprisingly cozy. We've all started somewhere.

▸ "I hope so. Everything still feels a little overwhelming." (Earnest)
→ MARCUS +2 Trust.
▸ "Cozy is a nice word for it. 'Glorified closet' also works, but I'll take it." (Sarcastic)
→ MARCUS +3 Affection.
▸ "It'll do for now. It's a roof over my head." (Reserved)
→ neutral.

MARCUS: Trust me, you'll settle in faster than you think. The people around here are friendly. If you ever need anything, just knock on my door. Apartment 14.

You: Thanks, Marcus. I really appreciate it.

MARCUS: No problem. Oh, and one more thing... If you're looking for a job, check out the cafés downtown. They're almost always hiring.

(This is the soft nudge toward Zoe's café / first job.)

MARCUS: Anyway... Welcome to the neighborhood. See you around!

[hide marcus] → Sets marcus_met = True. Return to apartment action menu.

---

## TALKING TO MARCUS (repeatable)

Where/when: knock on 4B (home, morning/afternoon) or find him at **Static** in the evening. Costs ~1h. Each talk: small +Affection (diminishing), can raise a topic.

**Greeting varies by Affection tier:**
- 0–25 (Acquaintance): "Hey, neighbor. Surviving?"
- 25–50 (Friend): "There he is. Grab a seat."
- 50+ (Close): "Was just about to text you. What's up, man?"

**Topics (pick one per visit):**

▸ **"How's the bar?"**
  - MARCUS: "Static? Busy. Loud. Tips are decent if you can fake liking the music." → small INT/CHR flavor, hints you can pick up nightlife work later.
  - At Affection 40+: "I keep thinking… I could run a place better than this. Smaller. Mine." → unlocks his dream thread `marcus_dream_known = True`.

▸ **"Got any work leads?"** (if `marcus_jobtips`)
  - Rotates a tip: café hiring (CHR), warehouse needs backs (STR), the Hub takes freelancers if you're sharp (INT). Flavor + soft direction. No hard reward, just guidance.

▸ **"Just hanging out."**
  - Light banter, basketball/movies. +Affection. Occasionally: "We should ball sometime. Park, Saturday." → sets a weekend hangout availability.

▸ **"You good?"** (Trust 30+)
  - He opens up a little — money's tight, the bar owner's a pain, he's stuck. Raises Trust. Foreshadows M-event "Marc needs a hand."

## MARCUS EVENTS (early)

**M-EVENT 1 — "The tour" (first weekend after meeting).**
Marcus texts: *"Free? Showing you the good spots. Bring shoes."* If you go (costs a block of time): he walks you past the park, the mall, points out Static and the café. Mechanically: reveals/【highlights】a couple map districts + gives a one-time small CHR bump from socializing. Ends with him buying you a cheap street-food dinner. +Affection, +Trust.

**M-EVENT 2 — "Twenty bucks" (triggers if Money < $20).**
Marcus notices (or you ask). One-time loan, no interest, "pay me back when you can." Builds Trust if you repay; small Trust hit if you never do.

**M-EVENT 3 — "His dream" (Affection 50+, after `marcus_dream_known`).**
Late-game thread: Marcus wants to open his own bar and asks if you're in — as a friend, an investor, or to talk him out of a bad lease. Branches based on your money/CHR. (Detail later.)

> **Asset note:** Marcus needs sprites (M, ~27, casual, dish-towel/bartender looks). Not generated yet — add to [image_assets.md](image_assets.md).

---

# ZOE — the barista / artist

Met at the café. Romance/friendship, focus character. Found: **Grounds**, daytimes (works there). Interests: drawing/street art, indie music, late-night city walks. Guarded wit, warms up once she trusts you. Her arc: wants to open her own creative space.

## SCENE Z0 — First meeting ("the spill", café, first visit)

*[bg: cafeday] [show: zoe_punk_smile at right]*

*The café is warm, smells of espresso and cinnamon. Behind the counter, a girl with red hair and a star clip is balancing a tray stacked too high — mugs, a cake stand, a little glass of pens that does not belong there.*

*She turns, the tray tips —*

ZOE: — no no no —

*You catch the cake stand a half-second before it becomes art on the floor. One mug isn't so lucky; it bounces, miraculously unbroken, and rolls to your feet.*

ZOE: *(exhales)* Okay. Nice hands. You just saved me a very bad morning and Henry's favorite cake plate.

▸ "Couldn't let the cake die." → ZOE +4 Affection. ZOE: *(snorts)* "A man with priorities."
▸ "You always carry that much at once?" → ZOE +2 Affection, +1 Trust. ZOE: "Only when I'm showing off. Clearly going great."
▸ "Careful." *(hand her the mug, say little)* → neutral +1. ZOE: "…Thanks. Strong silent type. Got it."

ZOE: I'm Zoe. I make the coffee and, apparently, the messes.

You: *(introduce yourself)*

ZOE: Well, [you], you've got free refills for life. Or, you know, one. Henry watches the register like a hawk.

*She notices the glass of pens you're still holding.*

ZOE: Oh — those are mine, not the café's. I sketch on breaks. Don't tell anyone the latte art's just practice.

▸ "You're an artist?" → ZOE +3 Affection, sets `zoe_art_known = True`. ZOE: "Trying to be. There's a difference, and rent reminds me daily."
▸ "Your secret's safe." → ZOE +2 Trust. ZOE: "A man who can keep his mouth shut. Rare."

ZOE: Anyway — first coffee's on me, for the save. After that you're a paying customer like everyone else.

→ Sets `zoe_met = True`. Unlocks café actions incl. "Talk to Zoe." Return to café menu.

## TALKING TO ZOE (repeatable, café, ~1h)

**Greeting by Affection tier:**
- 0–25: "Back already? The coffee's that good, or…?"
- 25–50: "Hey, you. Usual?"
- 50–75: "I was hoping you'd come in today."
- 75+ (romance track): "There's my favorite distraction."

**Topics / branches (one per visit; lines vary by tier):**

▸ **Small talk** (always)
  - Low tier: weather, the regulars, Henry's moods. ZOE: "See the guy in the corner? Orders the same thing for three years. I respect the commitment, I just don't get it."
  - Mid tier: she asks about *you* — where you're from, what you're chasing. Listens. +Affection if answers are honest.

▸ **Ask about her art** (if `zoe_art_known`)
  - First time: she's cagey. ZOE: "It's nothing. Rooftops, alleys, the city when it's not trying so hard."
  - Affection 35+: "Wanna see?" → shows a sketch. ▸ "It's really good." (genuine) → +5 Affection, +3 Trust. ▸ "It's… interesting." → +0, she deflects. ▸ "Why don't you sell these?" → ZOE: "And ruin them with money? …Maybe. I don't know." (foreshadows her dream)
  - Affection 50+: `zoe_dream_known = True` — she admits she wants her own little gallery-café, somewhere art doesn't have to apologize for existing.

▸ **Flirt** (CHR ≥ 20, Affection 30+)
  - Light, deniable. ZOE volleys back harder than you serve. Success (CHR check) → +Affection; fail → she teases you, small whiff, no penalty. "Smooth. Did that line work on anyone, ever?"

▸ **"How's the job?"**
  - Banter about Henry, tips, the dream of quitting. Occasionally seeds her storyline.

## ZOE — café actions (non-conversation)

- **Buy a coffee** ($3): small Hunger bump; if Zoe's working, a one-liner from her (varies by tier).
- **Work a shift (barista)**: if you also work here, shifts with Zoe raise Affection passively + a short two-line exchange each shift. Builds the "coworkers → more" track.

## ZOE EVENTS (early)

**Z-EVENT 1 — "Closing time" (Affection 40+, visit café in the evening).**
The café's empty, Henry's gone home. Zoe's wiping tables, music low. She offers you the last cup and they actually *talk* — no counter between them. A quieter, more honest scene. Choice to walk her partway home (a late-night city walk — her favorite thing). Big Affection/Trust beat; opens romance track if you take it.

**Z-EVENT 2 — "Open mic / wall" (Affection 55+, `zoe_dream_known`).**
Zoe gets a chance to show her art — a wall, a night, a small crowd. She's terrified. You can hype her up (CHR), help set up, or just be there. Payoff scene for her arc; your support shifts whether she chases the dream.

**Z-EVENT 3 — "The offer" (late).**
A real shot at her own space comes with strings (money/partner/risk). Mirrors Marcus's bar dream — you may be juggling both. Branches later.

> **Asset note:** Zoe sprites exist (punk = default, plus expressions). Could use a "holding sketchbook" pose later. Expressions to add: laughing, embarrassed/blushing, serious.

---

## Notes / open questions

1. **Marcus → Zoe pipeline:** Marcus literally points you to the café for work — nice organic intro to Zoe. Keep?
2. **Tone of "You":** I wrote 3 stances per choice (earnest / sarcastic / reserved). Lock this 3-way voice as the standard?
3. **Romance gating:** Zoe romance via Affection + Trust + one honest "Closing time" choice. Marcus friend-only for now (you said maybe all datable later — flag it for a future pass?).
4. **First playable slice:** implement M0 (move-in intro) + Z0 (the spill) + basic repeatable talks first — that's a real vertical slice. Then events.
5. Need **Marcus sprites** before M-scenes can show him on screen.
