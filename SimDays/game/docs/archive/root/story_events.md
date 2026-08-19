# Story Events — Marcus, Zoe, Becca (10 each)

Draft scripts. **Read & mark changes — not implemented yet.** Protagonist = male ("You"); choices come in the standard 3 voices (earnest / sarcastic / reserved). Meeting/intro scenes for Marcus & Zoe live in [story_marcus_zoe.md](story_marcus_zoe.md); Becca's meeting is below. Companion to [characters.md](characters.md).

Notation: `You:` / `MARCUS:` etc · *(narration)* · `▸ "choice" → effect` (Aff = Affection, Tr = Trust, flags in `code`).

Arc shape per character: **early (meet→friend) → mid (their storyline) → late (commitment/finale)**, gated by Affection/Trust + stats/money/time.

---

# MARCUS REYES — friendship / bro arc (10 events)

Found: mornings home/park, evenings at Static. Interests: basketball, cooking, old action movies. Helps you settle, then chases his own bar.

## M-1 · "The Tour" (first weekend after meeting)
*Trigger: first Sat/Sun after `marcus_met`. Text: "Free? Showing you the good spots. Bring shoes."*

*[bg: map_city / street] [show: marcus]*
MARCUS: Okay, crash course. That's the park — free, and the one place in this city that won't take your money. Mall's that way, overpriced. And that —*(points)*— is Static, where I pour drinks and lose my hearing.
You: *(taking it in)*
MARCUS: Café "Grounds" is around the corner. Told you — they're hiring. Go charm 'em.
▸ "Thanks for doing this." → Aff +4, Tr +2. MARCUS: "Eh. Nobody did it for me. Pay it forward someday."
▸ "You give this tour to everyone?" → Aff +2. MARCUS: "Only the ones who catch trays— wait, that's the other guy. Only the ones I like."
*Ends: he buys cheap street food. +Aff. Reveals a couple map districts. Sets `marcus_tour_done`.*

## M-2 · "Twenty Bucks" (triggers if Money < $20)
MARCUS: Hey — you look like a guy who's counting coins. Don't. *(slides you a twenty)* Pay me back when payday hits. No interest, I'm not a monster.
▸ "I'll pay you back this week." → `marcus_loan = 20`. If repaid on time later → Tr +6. MARCUS: "See? Trustworthy. Rare."
▸ "I can't take this." → MARCUS: "You can and you will. Eat something." → still gives it, Aff +2.
*If never repaid (after 2 weeks): small Tr −4, he never mentions it but the warmth dims a notch.*

## M-3 · "Ball" (Affection 20+, weekend, park)
*[bg: parkday] [show: marcus]*
MARCUS: You hoop? Don't lie, I'll know in the first possession.
▸ "I can hold my own." (STR check) → win: Aff +5, "Okay okay, the new guy's got game." / lose: Aff +3, comedic, "We'll get you there."
▸ "Absolutely not." → MARCUS laughs, teaches you anyway. Aff +3, small STR +1.
*Sets weekend-park hangout as a recurring low-key +Aff option. Flag `marcus_ball`.*

## M-4 · "Movie Night" (Affection 30+, evening, home)
MARCUS: Got a six-pack of soda and the worst action movie ever made. You in? It's tradition. The tradition started tonight but still.
*You watch. He quotes every line before it happens.*
▸ "This is genuinely terrible." → MARCUS: "Terrible is the point! Lean in!" Aff +3.
▸ "I'm kind of into it." → Aff +4, Tr +2, `marcus_movie_buddy`. Unlocks occasional movie-night invites.
*Quiet beat at the end — he talks about his dad, who loved these movies. First crack in the easygoing shell. Tr +3.*

## M-5 · "Bad Shift" (Trust 30+, evening, Static)
*Marcus is behind the bar, jaw tight.*
MARCUS: Owner stiffed me on hours again. Says the register was short. It wasn't me, but guess who eats it.
▸ "That's theft. Push back." → MARCUS: "Yeah? With what leverage? I need this job." → Aff +2, plants seed for his independence arc.
▸ "Let me buy you a drink — off the clock." → Tr +5. He vents, you listen. `marcus_vented`.
▸ "Want me to talk to him?" (CHR 30+) → if you do, mixed result; Tr +6 for having his back regardless.
*This is the wound that powers M-7/M-8 (his own bar).*

## M-6 · "Hangover Run" (Affection 40+, morning after a bar night)
*Knock at your door, painfully early. Marcus, sunglasses indoors.*
MARCUS: Two things. One: never let me do tequila. Two: I made too much breakfast and I will cry if it's wasted.
▸ "Say less." → comedic morning, Aff +3. He's grateful for the company.
▸ "It's 7 AM, Marc." → MARCUS: "And yet here we both are. Eggs?" Aff +2.
*Light palate-cleanser event. Tiny Energy cost, restores some Hunger (free meal).*

## M-7 · "The Dream" (Affection 50+, evening, Static)
*Late, bar empty. Marcus wiping the counter slow.*
MARCUS: Can I tell you something stupid? I keep sketching this place in my head. Mine. Small. Good music, no register games, regulars who actually like each other.
▸ "That's not stupid. Do it." → `marcus_dream_known`, Aff +5, Tr +4. MARCUS: "Easy to say. Hard to fund."
▸ "Bars fail all the time, you know that." → reserved/realist. Tr +3 (he respects honesty). "Yeah. I know. Doesn't kill the want, though."
*Opens the back half of his arc.*

## M-8 · "The Lease" (after `marcus_dream_known`, mid-late)
MARCUS: There's a spot. Old place on 5th, owner wants out cheap. Catch is I'd need a partner, or a loan, or a miracle.
▸ "I'll back you." (Money ≥ threshold) → `marcus_partner = True`. Big Tr. Locks toward "Opening Night" good path.
▸ "Let's read that lease first." (INT 30+) → you spot a bad clause; saves him from a trap. Tr +8, even if you don't invest. MARCUS: "You just saved my whole life, you nerd."
▸ "It's too risky, Marc." → he's deflated but hears you; path bends toward "give up / regroup."

## M-9 · "Rough Patch" (Trust 50+, mid-late)
*Marcus is quiet, off his game. The deal's wobbling, money's thin, maybe a breakup he never mentioned.*
MARCUS: I'm fine. *(beat)* I'm not fine. I don't really… do this. Asking.
▸ "You don't have to do it alone." → Tr +6. He leans on you; friendship deepens past banter.
▸ *(just sit with him, say nothing)* → reserved. Tr +5. Sometimes presence beats words.
▸ "Snap out of it, we've got work." (tough love) → risky; if Trust high enough it lands (+Tr), else stings (−Tr).
*Determines his resilience going into the finale.*

## M-10 · "Opening Night / Last Call" (finale)
**Good path** (`marcus_partner` or you saved the lease + supported him):
*[bg: bar / Static-but-warmer] [show: marcus, grinning]*
MARCUS: We did it. Well — I did it, but you're the reason I didn't chicken out. First drink's on the house. Forever, for you.
*Toast scene. Becomes your hangout hub. Best-friend ending locked.*
**Down path** (you discouraged / never supported):
MARCUS: Didn't happen. Maybe that's okay. Maybe I needed someone to tell me to slow down. *(small smile)* Still got a friend out of it, right?
▸ "Always." → bittersweet but solid friendship.
*Either way: Marcus remains a loyal fixture. (Optional future: romance flag if you opened it.)*

---

# ZOE — romance / artist arc (10 events)

Found: café daytimes. Interests: drawing/street art, indie music, late-night walks. Guarded wit; warms with Trust. Arc: her own creative space.

## Z-1 · "Refill" (Affection 10+, café)
*First easy re-meet after the spill.*
ZOE: The tray-catcher returns. Henry still talks about that plate like it's his firstborn.
▸ "I'm a hero. It's a burden." → Aff +3, banter. ZOE: "A humble one, clearly."
▸ "Just here for caffeine." → Aff +1. ZOE: "Respect. Romance the bean, not the barista."
*Establishes the easy rapport + the running "Henry/the plate" bit.*

## Z-2 · "The Sketchbook" (Affection 35+, `zoe_art_known`)
ZOE: *(hesitates, then slides a battered sketchbook across the counter)* Don't make it weird. It's just… rooftops. The city when it forgets to perform.
▸ "These are genuinely good, Zoe." → Aff +6, Tr +4, `zoe_showed_art`. ZOE: *(quiet)* "…Yeah?"
▸ "Why aren't these on a wall somewhere?" → ZOE: "Because walls cost money and so does failing in public." (seeds her dream)
▸ "Huh. Interesting." (lukewarm) → Aff +0, she closes the book. "Right. Forget it." (recoverable later)

## Z-3 · "Closing Time" (Affection 40+, café in the evening)
*[bg: cafenight] [show: zoe_punk_smile]*
*Empty café, Henry gone, low music. No counter between you for once.*
ZOE: Officially we're closed. Unofficially… last cup's yours if you want to actually talk. Not customer-talk.
*You talk. Real, not banter.*
▸ "Walk you home? You always say you love the city at night." → `zoe_walk = True`, Aff +7, Tr +5 → **opens romance track**.
▸ "I should let you close up." → Aff +2, polite; romance track stays slower.
*If walk: short street scene, she points out her favorite alley mural — turns out it's hers, unsigned.*

## Z-4 · "City at Night" (after `zoe_walk`, evening)
*A proper late walk. She's lighter out here than behind the counter.*
ZOE: Daytime me is all sharp edges. Night me… I don't know. Tells the truth more.
▸ "I like night you." → (CHR) success: Aff +6, she bumps your shoulder. fail: she deflects, "Smooth. Try again sometime," no penalty.
▸ "Both of you are alright." → Tr +4, earnest. "…That's annoyingly nice."
*Romance temperature rises. `zoe_night_truth`.*

## Z-5 · "Henry" (Trust 35+, café)
ZOE: Henry's thinking of selling. Lease, his knees, all of it. If Grounds goes, I'm just… a barista with no counter.
▸ "What do you want to happen?" → she admits she's scared, but also that it might be a push she needs. Tr +5.
▸ "I'll help however I can." → Aff +4. `zoe_helping`. Threads into her dream arc.
▸ "Maybe it's time for your own place, then." → plants `zoe_dream_known` if not set; she goes quiet, then: "…Don't say things like that. I'll start believing them."

## Z-6 · "The Wall" (Affection 55+, `zoe_dream_known`)
*A bar/venue offers her a wall for one night. She's terrified.*
ZOE: I said yes before I could chicken out. Now there's a wall, a date, and a very real chance of public humiliation.
▸ "I'll be there. Front row." → Aff +6, Tr +5. 
▸ "Let me help you set up." → practical support, Tr +6, you spend time/Energy.
▸ "You hype me up?" (CHR check) → success steadies her nerves, the night goes great, Aff +8.
*Payoff scene: people actually love it. She finds you in the crowd. A look. (Near-confession energy.)*

## Z-7 · "First Date" (Affection 60+, romance track)
*You ask her out properly — not café, not work.*
ZOE: Like… a date date? With a destination and everything? Look at you, planning.
*Destination choice (ties to systems):*
▸ **Beach at sunset** (chill) → Aff +6.
▸ **Gallery / mall art store** (her interest) → Aff +8 (interest match), Tr +4.
▸ **Bar with Marcus DJing** (social) → Aff +5, fun crossover with Marcus.
*Date scene branches a little by venue; ends on whether you read the moment (CHR).*

## Z-8 · "Guard Down" (Trust 55+)
*She tells you the why — an art-school dream that fell apart, a person who made her feel small, the cynicism as armor.*
ZOE: I don't do the soft stuff. But you… make it hard to stay armored. That's terrifying, for the record.
▸ "I'm not going anywhere." → Tr +8, big romance beat.
▸ "Armor's fine. I'll just sit next to it." → reserved, oddly perfect for her. Tr +7. "…God, that's exactly the right thing to say and I hate it."

## Z-9 · "The Offer" (late, `zoe_dream_known` + `zoe_helping`)
*A real shot at her own gallery-café — but it needs money, or a co-signer, or quitting her safety net.*
ZOE: This is the part where I find out if I'm brave or just loud. I could use a… co-conspirator.
▸ "Partner up." (Money/CHR) → `zoe_partner = True`. Locks her best ending + ties your fates.
▸ "It's your dream — I'll back you, not own it." → she does it solo-ish with your support; Tr +8, healthier framing.
▸ "Are you sure you're ready?" → caution; she has to convince herself, slower path.

## Z-10 · "Opening / Confession" (finale, Trust 70+ & CHR check OR friendship ending)
**Romance ending:** opening night of her space (or a quiet rooftop if the space didn't happen but the relationship did).
ZOE: I spent years expecting the floor to drop. With you it… didn't. *(beat)* I'm not good at this. So I'll just say it. I'm in. Are you?
▸ "I'm in. All the way." → couple ending.
▸ *(kiss her instead of answering)* (CHR) → couple ending, her favorite version.
**Friendship ending** (Trust high, romance not pursued): she names you the first regular of her new place; warm, no romance, door left open.
**Drift** (low Trust): polite distance; "Thanks for the coffees." Quietly sad.

---

# BECCA — gym / competitive romance arc (10 events)

🆕 Found: Iron Gate Gym, mornings/evenings. Interests: competing, smoothies/nutrition, terrible pump-up music, dogs. Driven, blunt, secretly soft. Arc: a fitness competition + learning she's more than her PRs. **Needs sprites (athletic, gym wear, F ~25).**

## B-0 · "Spotter" (meeting, gym)
*[bg: gymdaypeople] [show: becca (todo)]*
*A woman re-racks a heavy bar like it owes her money, then clocks you eyeing the weight.*
BECCA: You're gonna stand there or you gonna spot me? I don't bite. I might judge your form.
▸ "I've got you." → Aff +4. BECCA: "Hands ready, mouth shut. Good spotter."
▸ "That's more than I weigh." → Aff +3, she smirks. "Then today you learn something."
▸ "Maybe later." → neutral; she shrugs, "Suit yourself, civilian."
*Sets `becca_met`. Unlocks "Talk to Becca" + train-together option.*

## B-1 · "Form Check" (Affection 15+, gym)
BECCA: Your squat depth is a war crime. Here— *(adjusts your stance)* —there. Now it counts.
▸ "Thanks, coach." → Aff +4, small STR +1. BECCA: "Coach. Ha. I like that."
▸ "My form's fine." (STR low) → she proves you wrong, comedic, Aff +2.

## B-2 · "The Bet" (Affection 25+, gym)
BECCA: Race. Treadmill, two miles. Loser buys smoothies. I should warn you I'm petty about winning.
▸ Accept (STR check) → win: Aff +6, she's delighted/annoyed. lose: Aff +4, "Cute. Train harder." +motivation.
▸ "I don't gamble with a pro." → Aff +3, she likes the respect. "Smart. Still buying smoothies though."
*Sets `becca_bet`, recurring competitive banter.*

## B-3 · "Smoothie Talk" (Affection 35+, post-workout)
*Cooling down, smoothies in hand. First time she's still instead of moving.*
BECCA: People think this is all ego. It's not. The gym's the one place the noise in my head shuts up. *(beat)* …Forget I said that.
▸ "I get that. The quiet." → Tr +5, real connection. 
▸ "Deep, for a smoothie." → she laughs, deflects, Aff +3.
*First glimpse past the bravado. `becca_softside`.*

## B-4 · "Her Goal" (Affection 40+, gym)
BECCA: Regional fitness comp. Eight weeks out. I've placed second twice. Second is just first loser with a nicer view.
▸ "You'll win it." → Aff +5. "Don't jinx me. …But yeah. I will."
▸ "Why does it matter so much?" → Tr +6; ties to proving something to someone from her past. `becca_goal_known`.

## B-5 · "Setback" (Trust 35+, gym)
*Becca's iced up, furious. A tweaked shoulder, weeks before the comp.*
BECCA: Don't. Don't say "rest." If one more person says rest I'm going to bench them.
▸ "Okay. Then let's train smart, not stupid." → Tr +7, you become her training partner properly. `becca_partner_training`.
▸ "Rest." *(say it anyway)* → risky; if Trust high she deflates and listens (+Tr), else she snaps (−Aff, recoverable).
*Vulnerability beat — the fear under the drive.*

## B-6 · "Training Montage" (after `becca_partner_training`, recurring block)
*A stretch of weeks: you train together, she pushes you, you keep her honest about recovery.*
BECCA: Again. Two more. I said two— okay one. Fine. *(grinning)* You're not totally useless, you know.
▸ "High praise." → Aff +4 each session, your STR climbs too.
*Multi-session: each visit small Aff + STR; builds toward comp. A quiet evening mid-block where she falls asleep on your shoulder post-session — `becca_close`.*

## B-7 · "Competition Day" (Affection 55+, `becca_goal_known`, event)
*[bg: gym/arena] [show: becca, nervous for once]*
BECCA: I throw up before every one of these. Glamorous, right? *(grabs your sleeve)* …Stay where I can see you.
▸ "You've already won the hard part — showing up scared." → Aff +6, steadies her.
▸ "Go destroy them." (CHR pump-up) → check: success boosts her run.
*Result branches (win/podium/off-day) by her training + your support. Either way, she finds you first after.*

## B-8 · "After the Medal" (post-B-7)
**If she placed well:** BECCA: I did it. I actually— *(then, smaller)* and the first person I wanted to tell was you. What do I do with that?
**If she didn't:** BECCA: Second again. Or worse. *(long pause)* You're still here, though. Huh.
▸ "I'm proud of you. Medal or not." → Tr +8, the armor fully cracks. → opens romance.
▸ "There's always next one." (competitor-to-competitor) → Aff +5, she respects it.

## B-9 · "Off the Clock" (Trust 60+, non-gym)
*She drags you somewhere un-gym: a dog park, a greasy diner, anything off-brand.*
BECCA: Nobody sees me eat fries. This is classified. *(beat)* I wanted you to see the version that isn't trying to win something.
▸ "I like this version." → Aff +7, romance deepening.
▸ "Fries are a competition too. Eat faster." → she howls laughing, Aff +6. "God, you get it."

## B-10 · "Confession / Finale" (Trust 70+ & CHR, or friendship)
**Romance:** *(post-workout, gym closing, just the two of you)*
BECCA: I'm bad at losing and worse at this. But not having you around feels like losing. So— *(frustrated, earnest)* be with me. That's the ask.
▸ "Took you long enough." → couple ending.
▸ "Only if you finally let me win a race." → she laughs, kisses you, couple ending.
**Friendship:** lifelong gym-buddy/best-friend ending; she keeps you as the one person who saw her scared.
**Drift:** stays a respectful gym acquaintance; "See you around, civilian."

---

## Cross-character & system notes

- **Meters:** most ▸ choices nudge Aff/Tr; finales gate on Trust + a stat (CHR mostly, STR for Becca's comp).
- **Time/needs tie-in:** dates/events cost time blocks; some restore needs (Marcus meals, smoothies). Comp/wall events are calendar-triggered.
- **Crossovers:** Marcus DJs Zoe's wall night / your date; Becca and Marcus could rib each other at the bar — cheap, fun reactivity.
- **Assets still needed:** Marcus sprites; Becca sprites; Zoe extra expressions (laugh, blush, serious). Logged for [image_assets.md](image_assets.md).

## Open questions
1. Becca as the third — keep, or swap for Martha (corporate slow-burn) / Anna (mystery)?
2. Romance finales: lock to Trust 70 + CHR check, or vary per character?
3. How many events make the **first build** — all 10 each, or 4–5 each to start and expand?
4. Friendship-vs-romance fork point: should declining romance keep a strong friendship ending for everyone (as written), yes?
