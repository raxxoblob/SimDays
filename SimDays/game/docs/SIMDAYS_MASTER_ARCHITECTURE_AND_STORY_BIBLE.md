# LivingTheDream / SimDays — Master Architecture, World, Characters & Story Bible

> **Purpose:** one large architectural reference for understanding the entire game at a glance: what the player does, how the world is structured, who the characters are, where they live/work/spend time, how relationships progress, what major scenes exist, how careers and locations connect to story, and how AI-authored parent scenes hand off to director-owned CG subscenes.
>
> **Audience:** director/writer, Qwen/Aider, Claude, future coding agents.
>
> **Important:** this document is a **master overview**, not a replacement for current source code. Exact helper names, active line numbers and current task-specific file pointers belong in `QWEN_WORKMAP.md` / technical documentation. Current source always wins if code has changed after this document was written.
>
> **Status vocabulary**
>
> - **CURRENT** — established project/canon behavior.
> - **IMPLEMENTED** — known to exist in the project or in the current content architecture.
> - **PLANNED** — approved direction but not necessarily implemented yet.
> - **DIRECTOR-OWNED** — final CG-driven section implemented manually by the user/director.
> - **LEGACY / VERIFY** — appears in older source/docs and must not be treated as current without checking live source.

---

# 1. High-Level Game Identity

## 1.1 What SimDays is

SimDays is a contemporary urban life-simulation visual novel.

It is not intended to behave like a traditional route-based dating sim where the player selects a character, advances through a fixed sequence of scenes, reaches a confession, and effectively finishes that character's content.

The intended structure is a **persistent sandbox city** in which:

- the player has daily time, needs, money and skills;
- the player can work multiple careers;
- NPCs have locations, schedules and their own lives;
- relationships grow through repeated ordinary contact as well as authored scenes;
- major world events temporarily bring otherwise separate systems and characters together;
- skills and careers create alternate routes into content instead of replacing social progression;
- missing an early scene does not invalidate a save;
- different saves can reach the same later event through different histories.

The game fantasy is not "complete quests."

It is:

> build a life, become competent at things, meet people, develop routines, create a social circle, form relationships, and gradually accumulate a personal history in the city.

---

# 2. Core Design Philosophy

## 2.1 Sandbox over quest chain

The player should not constantly be told what to do next.

Avoid:

```text
QUEST: Meet Zoe
QUEST: Increase Zoe Relationship
QUEST: Go to Gallery
QUEST: Kiss Zoe
```

Prefer:

```text
player visits beach
→ meets Zoe naturally

player continues seeing Zoe
→ relationship context develops

shared memories / attraction / trust become sufficient
→ Zoe initiates a meaningful scene

authored breakpoint changes relationship state
```

HUD/UI should primarily show **state**, not orders.

---

## 2.2 Progression categories mean different things

### Skill

Skill represents actual ability.

Examples:

- Programming
- Music
- Art
- Cooking
- Mechanics
- professional career-specific skills

Skill should improve through repeated practice.

### Reputation

Reputation represents external standing and the quality of opportunities the world is willing to offer.

Reputation is not a substitute for skill.

### Portfolio / accomplishments

Portfolio represents things the player has actually achieved.

It should answer:

> What has this version of MC done?

### Money

Money increases options, convenience and speed.

Money must not directly purchase mastery.

A rich player should still have to learn.

---

## 2.3 RNG philosophy

Preferred structure:

```text
GUARANTEED PROGRESS
+
VARIABLE RESULT
+
RARE OUTCOME
```

Randomness should make the world less predictable without making long-term investment feel pointless.

Do not use RNG to:

- erase major progress;
- destroy a relationship arbitrarily;
- delete a career;
- invalidate hours of training;
- create giant save-scumming incentives.

Rare outcomes should usually unlock:

- a special opportunity;
- alternate future content;
- a memorable accomplishment;
- a contact;
- a cosmetic/keepsake;
- a stronger version of a normal reward.

No global Luck stat.

Where possible, important rolls should be stable per event/attempt so reloading the same moment does not trivially reroll the world.

---

# 3. Player Loop

A normal player day can contain any mixture of:

```text
wake / needs / home
        ↓
work or career shift
        ↓
skill activity
        ↓
city travel
        ↓
NPC encounter
        ↓
phone message / invitation
        ↓
shared activity or authored scene
        ↓
shopping / home / computer
        ↓
nightlife / group event
        ↓
sleep
```

Quiet days are valid.

Not every day should contain a major narrative beat.

The contrast between ordinary days and meaningful events is important.

---

# 4. Time, Needs and Daily Rhythm

## 4.1 Time

The world advances through explicit time costs.

Canonical time advancement is handled through the existing time system; historically `spend_time(hours)` is the central helper.

A day supports morning, workday, evening and late-night activities.

Time matters because:

- careers occupy chunks of the day;
- NPC schedules determine who is where;
- some scenes require specific time bands;
- nightlife belongs to night;
- commitments can conflict with other activity;
- the player cannot realistically do everything every day.

---

## 4.2 Needs

Core recurring needs include:

- Energy
- Hunger
- Hygiene

Activities may alter needs as well as skills/money/time.

The player should see predictable costs where useful.

A repeatable activity selection should ideally communicate:

```text
time
expected skill progress
energy cost
hunger cost
hygiene cost
money/material cost
```

before the player commits.

---

# 5. Stats and Skills

The older core-stat architecture includes:

- STR
- INT
- CHR
- APP

The project also has trainable professional/activity skills.

The important design distinction is:

```text
core stats = broad personal capability
skills     = learned domain ability
```

Current upcoming Zoe gym work uses **Strength** as a competency gate.

Approved direction:

- approximately Strength 3 is enough to credibly invite/help Zoe in a shared workout;
- Strength 5 may unlock a more competent coaching/spotting variation;
- Strength must not become "romance probability";
- competence changes what MC can reasonably do, not whether Zoe likes MC.

---

# 6. Relationship Architecture

## 6.1 Axes

The relationship model contains several separate dimensions.

Primary relationship-reading concepts:

- Familiarity
- Affection
- Chemistry / Attraction

Secondary but important dimensions:

- Trust
- Respect

They answer different questions.

### Familiarity

How much shared history and normal comfort exists?

### Affection

How much does this character like having MC in their life?

### Trust

How safe is personal honesty, vulnerability and reliance?

### Respect

How much does the character believe in MC's judgement, competence or integrity?

### Attraction / Chemistry

Romantic or physical charge.

High Attraction must **not** automatically change romance state.

---

## 6.2 Romance state

Romance is a separate state machine.

Current architectural set:

```text
unopened
friends
interested
dating
committed
paused
closed
```

Meaning:

### unopened

No romantic route has meaningfully opened.

### friends

Romantic possibility has been declined or relationship is presently framed as friendship.

### interested

Both sides have acknowledged enough attraction/possibility that romantic escalation is narratively valid.

### dating

A real romantic relationship has begun.

### committed

The relationship has been explicitly chosen as serious/defined.

### paused

Romance is temporarily inactive without being permanently closed.

### closed

Route is deliberately closed.

Raw points do not advance these states by themselves.

**Authored breakpoint scenes do.**

---

## 6.3 Relationship memory

Important shared experiences become relationship memories/facts.

Use memories for things future dialogue genuinely needs to know, such as:

- first kiss;
- major gallery night;
- Marcus learning important news;
- shared festival;
- a conflict and repair;
- first home evening;
- important personal disclosure.

Do not create a permanent fact for every line of dialogue.

---

# 7. Story Architecture

## 7.1 The game is a graph, not separate routes

Preferred structure:

```text
                      CITY / WORLD EVENTS
                              │
               ┌──────────────┼──────────────┐
               │              │              │
              ZOE           MARCUS           ELI
          art / identity   social life     IT / projects
               │              │              │
               └──────┐       │       ┌──────┘
                      │       │
                       GROUP LIFE
                      │       │
               ┌──────┘       └────────┐
               │                       │
             NORA                   CAREERS
          café / personal          skills / work
               │                       │
               └───────────┬───────────┘
                           │
                   MAJOR CONVERGENCE
                         EVENTS
```

Characters have thematic story clusters, but those clusters should overlap.

---

## 7.2 Requirements

Scenes may use:

### HARD requirements

Necessary for logic.

Examples:

- character met;
- specific fact known;
- required item owned;
- relationship state;
- location accessible.

### SOFT requirements

Increase probability/priority or alter dialogue.

Examples:

- high Familiarity;
- recent contact;
- relevant skill;
- strong reputation;
- regular visits to a location.

### ALTERNATIVE requirements

One of several histories can make a scene valid.

Example:

```text
Zoe Trust high
OR
Art skill high
OR
MC knows gallery contact
OR
relevant shared memory exists
```

This is crucial for nonlinearity.

### OBSOLESCENCE

Early scenes disappear when they no longer fit.

A player with a deep relationship should never suddenly receive an awkward "we barely know each other" scene just because they skipped it on day five.

---

# 8. Visual Production Architecture

## Tier A — reusable background + sprites

Use for:

- normal conversations;
- callbacks;
- routine dates;
- café/bar/library interaction;
- exposition;
- cross-NPC dialogue;
- followups.

This should be the majority of authored story.

## Tier B — special reusable event background + sprites

Use when a location/context is narratively important but does not need a bespoke composition every line.

Examples:

- gallery;
- meetup room;
- rooftop;
- event aftermath café;
- tournament setup;
- art workshop.

## Tier C — full CG

Reserve for:

- relationship breakpoints;
- major emotional physical gestures;
- group event highlights;
- performances;
- competitions;
- major reveals;
- festival sequences.

Typical budget philosophy:

- micro/ordinary scene: 0–1 CG;
- strong personal scene: 1–3 CG;
- meaningful group hangout: 2–5 CG;
- relationship CG subscene: usually several targeted CGs;
- major world event: roughly 8–15+ CG.

---

# 9. Director / AI Ownership Split

This is a major production rule.

## Director / ChatGPT

Owns:

- story architecture;
- canon;
- exact scene purpose;
- dialogue;
- pacing;
- choices;
- relationship progression;
- callbacks;
- location choice;
- the moment a scene should hand off;
- CG direction/prompts.

## Coding agent (Claude / Qwen)

Owns:

- implementation of supplied screenplay;
- eligibility;
- invitations;
- schedules;
- state plumbing;
- facts/memories;
- save compatibility;
- parent scene;
- normal backgrounds and sprites;
- everything before the final visual handoff;
- safe call/return;
- aftermath;
- tester/static checks.

## User / Director-owned CG implementation

The user takes over **only at the final CG-driven payoff**, not halfway through the event.

Pattern:

```text
AI PARENT SCENE
    opening
    date / event
    normal dialogue
    choices
    emotional buildup
           │
           ▼
DIRECTOR HANDOFF
           │
           ▼
director-owned .rpy
    CG sequence
    final romantic/physical payoff
    internal visual choices
    required milestone mutation if specified
    return
           │
           ▼
PARENT AFTERMATH / RECONVERGENCE
```

The handoff is the climax.

The AI still implements the complete buildup.

---

# 10. World / Location Bible

The city should feel like a single connected social environment rather than isolated menu screens.

---

## 10.1 Player Apartment / Home

### Function

- sleep;
- needs;
- personal computer;
- home activities;
- items/upgrades;
- private social visits;
- later relationship scenes;
- group movie/apartment nights.

### Story tone

The home becomes more narratively important as relationships deepen.

Early game:

```text
private player utility space
```

Later game:

```text
place other people naturally enter
```

Home scenes must not assume exact furniture unless the current home tier guarantees it.

Use generic home-state compatible backgrounds.

---

## 10.2 Hallway / Building

Function:

- transition from home into city;
- neighbor/early Marcus context;
- lightweight encounter space.

Marcus's early role is tied to the player's arrival/neighborhood.

Avoid turning the hallway into a major social hub.

---

## 10.3 Grounds Café

### Identity

Recurring independent café.

### Core character

**Nora works here.**

This is a major part of Nora's day-to-day identity.

### Other characters

Depending on schedule:

- Zoe may visit;
- Kai is an established regular;
- other known NPCs can overlap naturally.

### Narrative role

Grounds supports:

- first/early meetings;
- routine conversations;
- relationship callbacks;
- quiet personal scenes;
- spontaneous group overlap;
- work/study;
- familiar repeated seating/table motifs.

### Important NPC relationship

Nora and Kai have an established regular/barista dynamic.

The player should sometimes enter a conversation that already existed before MC arrived.

---

## 10.4 Static

### Identity

Local bar / nightlife social anchor.

### Marcus

Marcus is strongly tied to Static.

Current canon treats Marcus as a bartender / person who runs or is deeply responsible for Static.

Static is one of the main places where Marcus naturally becomes a social connector between MC and other people.

### Uses

- Marcus scenes;
- group drinks;
- nightlife;
- Marcus + Zoe group scene;
- regular overlap;
- tournament/challenge potential;
- relationship/world callbacks.

Static should not become "the romance bar."

Its primary role is social convergence.

---

## 10.5 Eleven

### Identity

Serious culinary workplace / restaurant.

### Rena

**Rena works at Eleven.**

Current canon:

- Rena is the head chef;
- she is a career mentor;
- she is not a diner employee;
- she is not intended as a romance route.

This distinction is important.

Eleven is her professional environment.

---

## 10.6 Diner

### Identity

Older / casual late-night food location.

### Rena caveat

Rena may plausibly appear here **off duty**, but she does **not** work here.

Do not place Rena behind the counter, on diner shifts or acting as diner staff.

The diner can function as:

- late-night decompression;
- inexpensive food;
- off-duty crossover;
- quiet post-work conversation.

If the current schedule puts Rena there, interpret it as private/off-duty presence unless live source explicitly says otherwise.

---

## 10.7 Sand Beach / Beach

### Identity

A recurring personal location rather than a one-off romance backdrop.

### Zoe

The beach is particularly important to Zoe.

It should exist in her life independent of MC.

That is what gives later relationship scenes weight.

### Uses

- Zoe introduction route;
- quiet walking;
- beach-night conversations;
- romantic breakpoint architecture;
- Elle-related content;
- possible late event endings.

### Current relationship direction

The beach is intended to own the **canonical Zoe interested → dating breakpoint**.

Important distinction:

There may be multiple beach scenes.

The latest working documentation indicates that the older `zoe_beach_night_scene` should not automatically be assumed to be the canonical first romantic breakpoint; current source/workmap must decide which concrete beach label owns M2.

---

## 10.8 City Park

### Uses

- running;
- sports;
- basketball;
- music/guitar;
- casual encounters;
- weather/rain scenes.

### Marcus

Morning/park activity is part of Marcus's normal life.

### Zoe

Known Zoe park content includes rain shelter and possible guitar/busking crossover.

### Sam

Sports-related content can bring Sam here.

The park is useful because it allows characters to meet outside their occupational identities.

---

## 10.9 Gym

### Identity

Actual mechanical Strength/training location.

### Current implementation note

Current project documentation indicates gym workout logic is largely inline in the gym-floor location rather than isolated in a dedicated workout module.

### Regular gym characters

Sam/Kai have stronger native sports/gym associations.

### Marcus

**Marcus is canonically not a gym NPC.**

Do not place him there simply because he likes sport.

Marcus's sport identity is better represented through park/running/basketball.

### Zoe — planned shared activity

After dating:

- MC can invite Zoe to train;
- Strength ~3 allows the shared activity;
- Strength 5 can unlock a more competent coaching variation;
- Zoe does not gain a permanent gym schedule;
- she attends because the shared activity was explicitly arranged;
- after the first session, the activity can become replayable;
- low-frequency Zoe initiative may later produce "Gym tomorrow?" type invitations.

The workout itself should reuse real workout mechanics.

---

## 10.10 The Hub

### Identity

Functional modern tech workplace.

### Eli

Eli is strongly tied to the Hub through IT/coding work.

### Environment

Not a glossy fake startup.

It should feel like a real working dev floor:

- monitors;
- standing desks;
- cables;
- cups;
- developers;
- real technical work.

### Narrative uses

- IT career;
- Eli introduction;
- PR/code review;
- production problem;
- late deploy;
- open-source/project collaboration;
- Eli + Zoe creative-tech crossover.

---

## 10.11 Library

### Uses

- study;
- skill work;
- Eli late-night scenes;
- quiet relationship development.

Library scenes are valuable because closeness can be expressed through comfortable silence rather than constant exposition.

---

## 10.12 Nightclub

### Uses

- nightlife;
- romantic tension;
- Zoe "Moment That Didn't Happen";
- spontaneous encounters;
- group/social contrast with quieter daytime locations.

The nightclub should not automatically equal kissing/romance.

For Zoe it works well as a place where a moment becomes too obvious to dismiss.

---

## 10.13 Nexus Tower

### Identity

Corporate career environment.

### Key characters

- Caroline
- Martha

### Spaces

- lobby;
- main office floor;
- meeting room;
- cafeteria / coffee area;
- corridor;
- archive floor;
- nighttime office version.

### Narrative role

The corporate story should show multiple layers:

```text
polished public office
vs
older forgotten infrastructure
vs
private after-hours human moments
```

Martha's content especially benefits from small deviations from her controlled professional behavior.

---

## 10.14 Hospital

### Identity

Medical career environment.

### Key character

Dr. Lena.

### Uses

- career shifts;
- break-room scenes;
- exhaustion/competence;
- subtle relationship scenes;
- later home interaction where appropriate.

---

## 10.15 Warehouse / Industrial Work

### Function

Physical/work career loop.

Natalie is associated with the warehouse career.

The world event/work-event system can create small shift texture:

- scanner issues;
- blocked bay;
- label problems;
- deliveries;
- practical problem solving.

---

## 10.16 Quayside / Riverside Terrace / Downtown

These are connective city spaces.

Useful for:

- walking conversations;
- transition out of cafés/events;
- dates that are not locked to a business interior;
- city-night atmosphere;
- later relationship pacing.

A good relationship scene often benefits from moving through multiple spaces:

```text
venue
→ walk
→ quiet edge of city
```

rather than staying at one table for forty lines.

---

## 10.17 Gallery / Art Event Spaces

Gallery space belongs primarily to:

- Zoe's personal-art arc;
- city art events;
- Art & Culture Night;
- player Art skill/opportunity chain.

A gallery must not become a mandatory route gate for every Zoe relationship state.

A player can develop Zoe romance without becoming an artist.

---

# 11. Character Bible

---

# 11.1 MC — Protagonist

MC is a young adult building a life in the city.

The player determines much of MC's competence and lifestyle through:

- career;
- skills;
- money;
- appearance;
- activities;
- relationships.

Visual rule for CGs:

MC should usually remain:

- POV;
- rear three-quarter;
- shoulder foreground;
- face obscured;

unless a specific approved protagonist identity is intentionally used.

The game should avoid making MC's inner monologue excessively prescriptive.

Do not narrate:

> "You think Zoe is fascinating."

when behavior/composition can let the player reach that feeling themselves.

---

# 11.2 Zoe

## Role

Creative/social anchor and one of the most developed relationship routes.

## Core themes

- art;
- personal creative identity;
- gallery/exhibition;
- showing work publicly;
- paid client work vs personal work;
- creative judgement;
- music;
- former bass playing;
- nightlife;
- vulnerability through being observed/judged;
- relationships becoming part of ordinary life.

## Personality

Zoe is:

- dry;
- observant;
- opinionated;
- slightly guarded;
- capable of being direct;
- not interested in performing likability.

Her humor is observational rather than bubbly.

She notices:

- typography;
- bad signs;
- composition;
- visual choices;
- small environmental details;
- things people do repeatedly.

## What Zoe is NOT

Do not turn her into:

- generic cute girlfriend;
- clingy partner;
- constant blushing anime heroine;
- relentlessly sarcastic edgelord;
- manic creative stereotype;
- person who needs MC to solve her career.

## Creative weakness

Zoe finds critique easier than exposure.

Showing her own work means accepting that someone else can judge something she actually cares about.

This is one of her central vulnerabilities.

## Art / work

She has paid client/creative work and a separate personal artistic identity.

The tension is not:

```text
career vs no ambition
```

It is closer to:

```text
commercially useful creative work
vs
work she personally needs to make
```

Her dislike of transactional "ambition" framing should not be interpreted as lack of artistic drive.

## Funding

Funding/rejection material should be revealed in properly authored scenes, not casually dumped by generic Talk before the scene has earned it.

## Bass / music

Zoe used to play bass.

Important reveal material:

- played for years;
- became genuinely competent;
- stopped partly because she was trying to be too many things at once;
- still notices basslines / instruments / reminders.

Generic music talk should hint before the authored scene owns the full history.

## Relationship behavior

Early:

- notices MC;
- argues about small things;
- doesn't try to impress;
- talks because she has something to say.

Comfortable:

- remembers previous conversations;
- references things MC did;
- invents excuses to see MC;
- sends specific messages.

Friend/close:

- initiates without practical reason;
- admits failures before fully processing them;
- can simply want company.

Dating:

- ordinary access becomes normal;
- shared routines matter;
- invites need less justification;
- physical familiarity becomes understated rather than theatrical.

Committed:

- intimacy is visible because she assumes continued presence in MC's life.

## Texting style

Short, specific, dry.

Not:

```text
heyyy ❤️ what are you doinggg
```

More like:

```text
"Grounds?"
"Four days. This is objectively excessive."
"Saw something you'd hate. Saved it."
```

## Important connections

### Marcus

Marcus and Zoe already know each other.

Their relationship should feel like a pre-existing city connection rather than two NPC routes colliding for the first time.

### Elle

Zoe and Elle have an established friendship relation in older/current NPC relation data.

### Eli

Professional/creative respect can develop through digital portfolio, generative art or technical setup work.

Not romantic between Eli and Zoe.

## Zoe story inventory

### Introduction / early presence

- beach introduction routes;
- Marcus-linked route into Zoe;
- early callbacks;
- contextual Talk;
- rain shelter;
- park/music possibility.

### Creative/personal arc

Known authored concepts/scenes include:

- **The Print**
- **Client Wants Beige**
- **Second Opinion**
- **Coffee, Not Advice**
- **Not Ready to Show It**
- **Thing You Noticed**
- **Deadline**
- **After Deadline** / gallery acceptance integration
- gallery/exhibition invitation/opening/aftermath/callback material
- funding application/rejection thread
- personal work vs commercial direction

### Music

- generic bass hint
- **Bass in the Window**
- possible park guitar interaction when MC has Music skill/guitar

### Routine/social

- **Wednesday at Grounds**
- **You Disappeared** phone beat
- Static/group overlap
- Marcus + Zoe scene
- small disagreement
- repair
- **Just Stay**

### Romance awareness

- **The Moment That Didn't Happen**
- typically nightclub / late-night context
- romantic awareness can move into `interested`
- no automatic kiss required at this stage

### Current Zoe relationship milestone direction

#### M2 — canonical dating breakpoint

**Current approved direction: beach.**

Function:

```text
interested
→ Zoe initiates meaningful beach meeting
→ full AI-implemented buildup
→ DIRECTOR HANDOFF
→ possible canonical first kiss
→ dating
```

The final CG-driven payoff is user-owned.

The parent must reuse the canonical first-kiss state contract rather than inventing a second one.

#### M3 — post-dating ordinary closeness

The latest documentation indicates the old beach-night content may now sit after the first-kiss breakpoint rather than before it.

Exact current label ordering should be checked in live source before editing.

The narrative function of M3 should be:

> dating changes normal life, not just unlocks more romantic cutscenes.

#### Replayable Zoe gym activity — PLANNED

After dating/committed:

```text
Strength gate
→ invite Zoe
→ gym arrival/buildup
→ DIRECTOR HANDOFF
→ CG workout/flirt sequence
→ parent post-workout scene
→ replayable shared activity
```

This is not a new romance-state milestone.

#### Commitment

Current consolidated documentation says the **current source commitment scene is on a terrace**, not the older planned beach-commitment version.

Therefore:

- treat terrace as current source truth unless live source changes;
- older beach commitment documents are legacy design;
- do not blindly restore beach because an archived MD says so.

#### First spoken "love you"

Late committed payoff at MC's home.

Key tone:

- ordinary;
- unceremonious;
- not a candlelit confession;
- Zoe says something significant almost as part of normal life.

---

# 11.3 Marcus

## Role

MC's first real social friend and primary social anchor.

## Personality

Marcus is:

- proactive;
- socially easy;
- comfortable initiating;
- quick to treat MC as part of his world;
- good at superficial/everyday conversation;
- more evasive around deep personal material.

He should feel like someone who calls because something is happening, not because the game needs to deliver a relationship scene.

## Texting

Short, direct, action-oriented.

Examples of rhythm:

```text
"Static tonight?"
"You coming?"
"Wednesday?"
```

Do not punish the player emotionally for not answering every casual invitation.

## Work / Static

Current canon:

- bartender / runs or substantially operates Static.

Static is therefore personal to him, not just a random bar spawn.

## Sport

Marcus:

- wakes very early;
- runs;
- has meaningful basketball history;
- received a serious basketball opportunity around age eighteen;
- did not follow that path;
- part of the deeper reason involves his father being ill.

Important:

**Marcus is not a gym NPC.**

Do not use gym attendance as shorthand for "sporty."

His sports identity should be park/running/basketball.

## Food

Marcus is not a broadly skilled chef.

Chili is the important exception.

The family-recipe/notepad thread is emotionally valuable because it is one specific thing he preserves carefully.

## Known/target scenes

- opening/neighborhood introduction
- Bowl Return
- Morning Person
- You Coming or What?
- One Game
- The One Thing I Cook
- Could've Left
- family-recipe hint
- **Notepad** authored reveal
- basketball offer
- **Why I Stayed**
- Random Errand
- Good News
- arm-around-shoulder celebration
- Haven't Seen You
- Nothing Important / Nothing, Really
- missed commitment consequence + repair
- Late Night Drive
- Marcus + Sam court/post-game crossover
- Marcus + Zoe at Static
- group invitations
- tournament/challenge lead-in

## Relationship function

Marcus's route must not exist only to feed player exposition.

He should:

- ask about MC's work;
- remember prior answers;
- follow up;
- share his own current life;
- introduce MC to social spaces;
- know people independently of MC.

---

# 11.4 Eli

## Role

Technical/professional anchor around IT, projects and focused work.

## Presentation

Established as:

- late 20s / early 30s;
- gender-neutral / androgynous presentation;
- practical dark tech clothing;
- economical posture;
- dry/direct expression.

Use current source for pronouns and exact dialogue representation; do not guess from old notes.

## Core themes

- programming;
- real technical work;
- competence;
- architecture;
- projects;
- overworking;
- difficulty switching off;
- professional standards;
- relying on other people;
- quiet forms of closeness.

## Personality

Eli should not become suddenly expressive because relationship points increased.

Closeness is visible through:

- staying;
- asking for another pair of eyes;
- sharing work that matters;
- comfortable silence;
- letting MC remain present;
- small physical breakthroughs only after sufficient context.

## Hub content

Known content includes:

- first-day introduction;
- production bug;
- PR review/comments;
- late deploy;
- junior/promotion review;
- programming kit / open-source project;
- late-night library;
- accidental physical-contact/deploy scene.

## Nonlinear story cluster

### Still Working?

Player finds Eli continuing to work.

Programming skill can change technical understanding, but non-technical MC can still experience the personal scene.

### Second Pair of Eyes

Eli needs feedback/help.

Potential entry through:

- Programming;
- Trust;
- prior project knowledge;
- professional context.

Technical competence should primarily create Respect/opportunity quality.

### Demo Night

Professional/social convergence.

Can be reached through:

- Eli;
- Programming;
- career contact;
- social/world event.

## Cross-links

### Marcus

Existing friendship / banter / contrasting approaches.

### Zoe

Creative-tech crossover.

Possible context:

- website;
- digital portfolio;
- generative visuals;
- exhibition setup.

The scene should allow Eli and Zoe to discover they can collaborate without MC remaining the center of every interaction.

---

# 11.5 Nora

## Role

Grounds café anchor; relationship route built around repeated everyday familiarity, food, noticing people and small acts of care.

## Work

Nora works at **Grounds Café**.

Use café uniform/sprites while working and casual/off-duty presentation elsewhere.

## Character direction

Nora is warm and observant without becoming sugary.

She notices changes.

Her care is often practical:

- remembers an order;
- brings food;
- checks in;
- makes space;
- asks a more precise second question.

She should not become passive-aggressive melodrama.

If hurt, she can be direct and quieter rather than theatrical.

## Known scenes / concepts

- café introduction / recurring interaction
- Quiet Hour
- Rough Shift
- After Closing
- Bad Day text → apartment visit
- bread/food gesture
- optional brief arm touch
- Nora Feels Ignored / Stops Waiting
- later repair
- Nora/Kai café crossover
- hug/personal-school-related scene in older implementation
- group hangouts
- late-work food/drink crossover potential

## Kai connection

Kai is an established café regular.

Nora knows his order and they can already be in a familiar low-stakes argument when MC enters.

This is a useful model for NPCs having relationships that predate the player.

---

# 11.6 Rena

## Role

Culinary career mentor.

## Current canon

- adult woman, around mid-30s in current working canon;
- authoritative;
- career mentor;
- head chef at **Eleven**;
- non-romanceable.

## Critical location rule

**Rena does not work in the diner.**

The diner may be an off-duty place she visits.

Her professional chef identity belongs to Eleven / culinary career scenes.

## Culinary content

Known career architecture includes:

- culinary first day;
- culinary tasks;
- Rena mentor scenes;
- review/commis progression.

Rena should feel authoritative because she knows the work, not because she is written as a hostile "TV chef."

---

# 11.7 Elle

## Core associations

- travel;
- outdoors;
- beach;
- music/art adjacent interests;
- social spontaneity.

## Connections

- established friendship relation with Zoe;
- café/beach world presence.

## Known story thread

Portugal / going-abroad decision thread.

Known visual payoff concept:

- Elle turns back toward MC on the beach at the emotional peak.

This is one of the arcs that historically needed a proper payoff.

Do not accidentally leave the Portugal decision permanently unresolved.

---

# 11.8 Martha

## Role

Senior corporate relationship route associated with Nexus Tower.

## Presentation

- early 30s;
- long dark hair;
- professional;
- controlled;
- economical body language;
- very restrained emotional display.

## Relationship tone

With Martha, small changes matter.

Examples:

- a minimal smile;
- waiting near an elevator;
- remaining late;
- brief touch below the elbow;
- sharing credit;
- unexpectedly mundane coffee-machine conversation.

Do not make her emotionally expansive too early.

## Known scenes

- corporate first/work interactions
- client call
- coffee machine
- after everyone leaves / overtime
- archive floor
- credit in hallway
- wardrobe notice
- gift accusation
- corridor first gesture
- later relationship escalation where current source supports it

Corporate scenes should preserve the sense that professional choices and personal attention overlap but are not identical.

---

# 11.9 Dr. Lena

## Role

Hospital/medical career NPC and relationship route.

## Tone

- capable;
- tired;
- dry;
- off-shift humanity matters;
- intimacy grows through trust and repeated stressful context rather than constant flirting.

## Known scenes

- hospital work encounters;
- break-room scene;
- shoulder gesture;
- home dinner / kitchen-related extended scene in older implementation;
- phone/off-shift possibilities.

Do not make medical scenes into implausible crisis heroics just to create drama.

---

# 11.10 Caroline

## Role

Corporate career NPC.

Associated with Nexus Tower and professional progression.

Current director-photo philosophy describes Caroline as controlled and likely to share personal material later and intentionally.

Do not merge Caroline and Martha into the same narrative function.

Martha's route is especially about precise observation/control; Caroline should retain her own current source characterization.

---

# 11.11 Sam

## Role

World/sports NPC.

## Romance

Non-romanceable in older/current roster architecture.

## Associations

- park;
- gym;
- sports;
- Marcus.

## Marcus connection

Marcus and Sam have an established sports friendship.

Known crossover:

- court / post-game bench.

Their comfort should feel older than MC's inclusion.

---

# 11.12 Kai

## Role

Sports/trainer world NPC.

## Romance

Non-romanceable in older/current roster architecture.

## Associations

- gym;
- café;
- beach;
- training.

## Nora connection

Regular at Grounds.

Their familiar cortado argument/café dynamic is an example of pre-existing NPC-to-NPC life.

## Sam connection

Training-regular relationship exists in expanded NPC relation data.

---

# 11.13 Natalie

## Role

Warehouse/career NPC.

## Romance

Non-romanceable in the established roster.

Her purpose is primarily career/world texture.

Do not force every career contact into a romance arc.

---

# 12. NPC-to-NPC World

The world should not be built as:

```text
NPC ←→ MC
NPC ←→ MC
NPC ←→ MC
```

It should also contain:

```text
NPC ←→ NPC
```

Known relationship examples from project data/materials include:

- Marcus ↔ Sam — sports friends;
- Nora ↔ Kai — café regular/barista familiarity;
- Zoe ↔ Elle — friends;
- Nora ↔ Elle — café familiarity;
- Lena ↔ Marcus — bar acquaintances;
- Sam ↔ Kai — training regulars;
- Caroline ↔ Marcus — Thursday/regular social overlap.

Not every pair needs simulated relationship axes.

Use lightweight facts and authored crossovers.

---

# 13. Group Life

The full cast should not instantly become a fixed party.

Group comfort emerges.

## Static Tonight?

Core:

- MC
- Marcus
- Eli

Possible:

- Zoe
- Nora

depending on:

- whether met;
- schedule;
- relationship context.

## Everyone Somehow Ended Up Here

Spontaneous city convergence.

Purpose:

- character chemistry;
- cross-NPC dialogue;
- world feeling alive.

No major plot required.

## Movie / Apartment Evening

Requires more group comfort.

It should not unlock merely because MC has met four people once.

Possible gating:

```text
shared memories
OR
several comfortable relationships
OR
specific invitation history
```

---

# 14. Major Events

---

## 14.1 Summer Festival — IMPLEMENTED major convergence

Major multi-CG city event.

Known design:

- downtown summer night festival;
- string lights;
- stalls;
- stage;
- group movement;
- weather/rain component;
- shelter section;
- late-night ending.

The event uses a large CG sequence and functions as a convergence memory.

It should not act as "Chapter 1 complete."

Different later content may use attendance as:

- a callback;
- alternate requirement;
- group-memory source;

but individual arcs must still work if the festival was skipped.

### Zoe romantic interlude

Approved architecture supports an optional director-owned romantic branch inside the shared event.

Rules:

- event remains primarily shared;
- private romance is a short interlude;
- branch returns to festival;
- interested can potentially use it as alternate first-kiss route if current canon keeps that option;
- dating/committed variants can show established intimacy;
- skipping it has no relationship punishment.

---

## 14.2 Art & Culture Night — PLANNED major event

Recommended next large world event.

Target structure:

```text
arrival
→ gallery/downtown environment
→ Zoe/public art context
→ group begins to gather
→ installation/activity
→ live performance/music
→ player-specific opportunity if relevant
→ Zoe-focused beat
→ social group section
→ complication/pressure
→ quiet conversation
→ result/reveal
→ after-event gathering
→ late-night ending
```

Art-skilled player:

- may understand more;
- may submit work;
- may receive stronger professional opportunity.

Non-art player:

- can still attend;
- support Zoe;
- socialize;
- discover contacts;
- experience the full event.

Possible entry routes:

- Zoe;
- gallery/world discovery;
- Art skill;
- social announcement;
- professional contact.

No single path mandatory.

---

## 14.3 City Sports / Community Challenge Day — PLANNED

Mechanically different from another night festival.

Possible content:

- fitness challenge;
- casual games;
- food stalls;
- spectators;
- Marcus;
- sports NPCs;
- Mechanics/community booth;
- competition;
- social/group payoff.

Useful for:

- Strength;
- Marcus;
- Sam;
- Kai;
- player reputation;
- community life.

---

## 14.4 Static Tournament / Local Challenge — PLANNED/cluster

A local competitive event can exist even if MC does not enter.

Reasons to care may include:

- Marcus rivalry;
- regular at Static;
- activity mastery;
- group invitation;
- world discovery.

This is preferable to hiding the entire event behind one minigame threshold.

---

## 14.5 Eli Demo Night — PLANNED/cluster

Professional/social convergence connecting:

- Eli;
- Programming;
- contacts;
- freelance;
- city event system.

---

# 15. Career Architecture

The game supports multiple career domains.

Current/known tracks include:

- Corporate
- IT
- Hospital
- Culinary
- Trainer / fitness
- Warehouse / physical work

The player can have multiple active careers under the multi-career architecture.

Career should create:

- money;
- time pressure;
- skill development;
- professional relationships;
- opportunities;
- contextual dialogue.

Career should not replace the rest of the game.

---

## 15.1 Corporate

Location:

- Nexus Tower.

Important NPCs:

- Caroline;
- Martha.

Scene style:

- client calls;
- project pressure;
- credit;
- professional judgement;
- overtime;
- archive/system discoveries.

---

## 15.2 IT

Location:

- The Hub.

Important NPC:

- Eli.

Scene style:

- real coding problems;
- PR reviews;
- deploys;
- architecture;
- pair/problem solving;
- work relationships.

Programming competence changes technical branches and Respect.

---

## 15.3 Hospital

Important NPC:

- Dr. Lena.

Scene style:

- practical medical work;
- fatigue;
- professional competence;
- human moments around stressful work.

---

## 15.4 Culinary

Location:

- Eleven.

Important NPC:

- Rena.

Scene style:

- kitchen discipline;
- technique;
- timing;
- career mentorship;
- progression.

Again:

**Rena is Eleven staff, not diner staff.**

---

## 15.5 Trainer / Fitness

Connects to:

- gym;
- Strength;
- Sam/Kai;
- sports events.

---

## 15.6 Warehouse

Connects to:

- physical work;
- Natalie;
- small logistical work events.

---

# 16. Phone Architecture

The phone is part of the living-world simulation.

Channels/features include concepts such as:

- Messages;
- Mail;
- Social;
- Calendar;
- Gigs.

NPC messages should feel like real contact, not quest notifications.

Relationship progression should alter what people naturally send.

## Photo-message philosophy

### Early

NPC sends:

- object;
- place;
- food;
- work thing;
- observation.

### Familiar

They send pieces of their actual day.

### Interested

Content becomes more personally targeted.

### Dating

Selfies/opinion asks can become natural.

### Committed

Ordinary unpolished fragments can become intimate because the recipient matters.

Character-specific direction:

- Zoe — observations, dry visual details, later occasional selfie/opinion ask;
- Nora — food/café/cooking/warm practical content;
- Elle — locations/travel/outdoors;
- Martha — rare and deliberate;
- Lena — tired/off-shift/hospital-day fragments;
- Caroline — controlled and later personal;
- Marcus — friendship photos: court, Static, chili, neighborhood; not gym.

---

# 17. Invitations and Commitments

NPC initiative should be low-pressure.

Pattern:

```text
eligibility
→ NPC message/invitation
→ accept / decline / reschedule
→ commitment/calendar
→ temporary schedule override
→ scene at location/time
→ completion / cleanup
```

Declining a normal invitation should usually not damage relationships.

Missed accepted commitments can matter because the player promised something.

Important distinction:

```text
decline honestly
≠
agree and fail to appear
```

---

# 18. Repeatable Shared Activities

Repeatable activities make relationships feel like ongoing life rather than a finite scene list.

Examples:

- café;
- walk;
- group drinks;
- home movie;
- gym training;
- game/sport;
- study/work session.

A repeatable relationship activity should:

- reuse existing mechanical activity systems;
- have a cooldown;
- use a small intro/outro pool;
- allow occasional NPC initiation;
- provide moderate relationship texture rather than massive point farming.

---

# 19. Zoe Gym Activity — Detailed Approved Direction

## Unlock

After Zoe is dating/committed.

Approximate requirement:

```text
Strength >= 3
```

No permanent Zoe gym schedule.

## First invitation

MC can propose training together.

The comedy should come from Zoe being suspicious of MC's confidence with machines/settings, not from her being physically incompetent.

## Parent scene

AI implements:

- invitation;
- commitment;
- arrival;
- warm-up conversation;
- normal sprites/background;
- pre-workout buildup.

## Director handoff

Planned director-owned file:

```text
game/director_romance/romantic_subscene_zoe_gym_training.rpy
```

Planned label:

```renpy
label romantic_subscene_zoe_gym_training:
```

Director owns:

- exercise CG sequence;
- physical coaching;
- light flirt;
- workout choices;
- CG-specific relationship texture.

## CG concept pool

Six useful modular images:

1. warm-up together;
2. basic form correction;
3. real training shot;
4. stronger spotting/coaching moment;
5. rest between sets;
6. post-workout/stretch ending.

Do not show all six on every replay.

Use subsets/rotation.

## Mechanics

The session must still count as real training.

Reuse:

- normal time cost;
- normal needs impact;
- normal Strength progression.

Do not create `zoe_strength_training_system`.

---

# 20. Zoe Dating Breakpoint — Detailed Approved Direction

The beach should carry the real emotional weight of moving from acknowledged interest into actual dating.

## Before the scene

Required history should establish:

- Zoe and MC know each other well enough;
- romantic possibility is explicit;
- state is `interested`;
- no first kiss has already happened in the normal route;
- enough time has passed to avoid immediate threshold cutscene behavior.

## Parent buildup

AI implements:

- invitation;
- night beach arrival;
- walking;
- callbacks;
- Zoe admitting the situation has become obvious;
- the point where she stops pretending she does not know what she is doing.

## Handoff

The user/director owns the visual romantic resolution.

Planned file:

```text
game/director_romance/romantic_subscene_zoe_beach_dating.rpy
```

Planned label:

```renpy
label romantic_subscene_zoe_beach_dating:
```

The director subscene may own:

- physical approach;
- final player choice;
- kiss/no-kiss;
- canonical first-kiss mutation;
- successful transition to dating;
- retry state if player is not ready.

## Important

Generic Kiss must not steal the canonical first kiss while this authored first-kiss route is pending.

The project already has a canonical first-kiss contract reported in current documentation as:

```text
_commit_first_kiss("zoe")
```

Do not duplicate its internal mutations.

---

# 21. Scene Inventory — Cross-Project Known Content

This section is a **narrative inventory**, not a promise that every label is still named exactly this way.

For coding, search current source.

---

## Zoe

### Everyday / location

- first beach introduction
- Marcus-linked beach introduction variant
- rain shelter
- Wednesday at Grounds
- park guitar/listening crossover
- normal contextual Talk
- group Static scene
- delayed group callbacks

### Art / personal

- The Print
- Client Wants Beige
- Second Opinion
- Coffee, Not Advice
- Not Ready to Show It
- Thing You Noticed
- Deadline
- After Deadline / gallery acceptance integration
- exhibition invitation
- exhibition opening
- exhibition aftermath
- final gallery callback
- gallery talk
- funding application
- funding rejection
- commercial-vs-personal creative tension
- small disagreement
- repair
- Just Stay

### Music

- bass hint
- Bass in the Window
- music callbacks

### Phone

- poster/visual observations
- bad-email/funding thread
- You Disappeared
- routine messages
- later dating initiative

### Romance

- The Moment That Didn't Happen
- beach dating breakpoint — current approved target
- post-dating ordinary scenes
- replayable gym date — planned
- commitment — current source location should be checked; consolidated docs say terrace
- first spoken Love You — home
- Summer Festival optional romantic interlude

---

## Marcus

- arrival/neighbour introduction
- Bowl Return
- Morning Person
- You Coming or What?
- One Game
- The One Thing I Cook
- family recipe hint
- Notepad
- Could've Left
- basketball offer
- Why I Stayed
- Random Errand
- Good News
- arm-around-shoulder celebration
- Haven't Seen You
- Nothing Important / Nothing Really
- missed commitment
- commitment repair/reschedule
- Late Night Drive
- Sam court crossover
- Sam post-game bench
- Marcus + Zoe at Static
- group invitation
- tournament/challenge lead-in

---

## Eli

- Hub first day
- production bug
- PR review
- late deploy
- promotion/review
- Still Working?
- Second Pair of Eyes
- programming kit
- open-source/project scene
- late-night library
- accidental touch/deploy
- brief deploy hug / physical breakthrough
- Zoe creative-tech collaboration
- Demo Night lead-in
- group Static content

---

## Nora

- Grounds introduction/routine
- Quiet Hour
- Rough Shift
- After Closing
- bad-day message
- apartment bread visit
- optional departure arm touch
- Feels Ignored / Stops Waiting
- later repair
- Kai café crossover
- personal/hug-school-related beat from older implementation
- group Static / spontaneous overlap
- late-work food/drink crossover concept

---

## Martha

- office introduction/progression
- client call
- office coffee machine
- overtime after everyone leaves
- archive floor
- credit hallway
- wardrobe upgrade notice
- gift accusation
- corridor gesture
- after-hours personal/corporate escalation

---

## Lena

- hospital career scenes
- break room
- shoulder gesture
- home dinner / kitchen extended material
- off-shift phone/relationship content

---

## Rena

- culinary first day
- kitchen task progression
- mentor scenes
- review / commis progression
- off-duty city appearance possible
- Eleven is professional home

---

## Elle

- café/beach presence
- Zoe friendship crossover
- Portugal / abroad reveal
- pier/beach payoff
- travel/outdoor content

---

## Sam

- sports/gym/park presence
- Marcus court scene
- post-game bench
- sports-world crossover

---

## Kai

- gym/trainer presence
- Grounds regular
- Nora café crossover
- Sam training familiarity
- beach/casual world presence

---

## Caroline

- corporate career content
- Nexus Tower relationship/professional scenes
- controlled later personal content

---

## Natalie

- warehouse career/world interaction
- physical-work texture

---

# 22. Location-to-Character Matrix

| Location | Strongest character links | Typical narrative use |
|---|---|---|
| Home | MC, later close NPCs | needs, private visits, intimacy, computer |
| Hallway | Marcus / early city | arrival, neighbour texture |
| Grounds Café | Nora, Zoe, Kai | routine, work/study, personal talk |
| Static | Marcus, Eli, Zoe/group | nightlife, group convergence |
| Eleven | Rena | culinary career |
| Diner | off-duty/crossovers | late-night decompression |
| Beach | Zoe, Elle | introspection, romance, walking |
| Park | Marcus, Sam, Zoe | sports, running, rain, guitar |
| Gym | Sam, Kai, planned Zoe | Strength, training, shared workout |
| Hub | Eli | IT, projects, deploys |
| Library | Eli / MC | study, quiet closeness |
| Nightclub | Zoe/group | tension, nightlife |
| Nexus Tower | Martha, Caroline | corporate career |
| Hospital | Lena | medical career |
| Warehouse | Natalie | physical career |
| Quayside/Riverside | social/romance | walking transitions, dates |
| Gallery/art space | Zoe | art arc, world events |

---

# 23. Technical File Map — High-Level

Exact live paths should be verified before edits, but current working architecture references these files heavily:

```text
game/interact.rpy
    NPC interaction
    generic Talk/actions
    canonical first-kiss contract

game/npc_relationships.rpy
    multi-axis relationships
    relationship changes/stages/memories

game/data.rpy
    defaults
    time
    day transitions
    shared state

game/npc_schedules.rpy
    canonical NPC schedule resolution

game/locations.rpy
    location labels
    location actions
    gym-floor workout logic
    scene staging hooks

game/phone_messages.rpy
    normal NPC messages

game/phone_actionable.rpy
    actionable messages / invitation responses

game/zoe_arc.rpy
    Zoe-specific authored arc/content

game/zoe_romance_milestones.rpy
    Zoe relationship milestone parent scenes

game/marcus_friendship.rpy
    Marcus authored friendship structure

game/story_direct_pass.rpy
    director-authored Zoe/Marcus story corrections/additions

game/arcs.rpy
    topic/story arc material

game/gameplay_expansion_scenes.rpy
    many authored one-off scenes/crossovers

game/summer_festival.rpy
    major festival event

game/debug_scene_tester.rpy
    developer scene testing
```

Current task-specific paths should be taken from `QWEN_WORKMAP.md`.

---

# 24. Canonical System Rules for Coding Agents

A coding agent must not create a parallel version of:

- relationship axes;
- romance states;
- first kiss;
- NPC schedule;
- phone;
- invitations;
- commitments;
- skill progression;
- time;
- RNG;
- event recording;
- scene tester;
- save migration.

Search current source and reuse the shipping helper.

---

# 25. Save Compatibility

This project evolves continuously.

New scenes must consider old saves.

Typical migration questions:

- did the old save already hear this reveal?
- did an older generic Talk reveal the fact first?
- does the save already contain a first-kiss memory?
- is romance state inconsistent with an old memory?
- would a new "first" scene replay absurdly?
- does a removed/merged arc leave an old flag behind?

Rule:

```text
new flag + default
```

is not sufficient by itself.

Narrative firsts require migration/backfill logic.

---

# 26. Ren'Py Engineering Gotchas

- `call` targets labels, not `.rpy` files.
- Screen-language `for` and raw script-level Python control flow are not interchangeable.
- Do not "fix" valid multiline `$ (...)` expressions simply because they span lines.
- Return values and caller unpacking must match.
- Stable sprite tags should be reused.
- Do not create fake image registrations for missing assets.
- Do not claim Ren'Py lint/runtime success unless the SDK was actually available and executed.

---

# 27. Scene Priority Philosophy

A location can have multiple possible events.

Priority should generally favor:

```text
major commitment / scheduled event
>
major authored relationship scene
>
high-priority personal scene
>
contextual followup
>
Tier A ordinary beat
>
ambient encounter
>
generic menu
```

Do not allow five unrelated story scenes to trigger on the same visit.

Major-scene/day budgeting helps preserve pacing.

---

# 28. Character Presence and Continuity

Characters should remember:

- what MC told them;
- what happened yesterday;
- what they themselves are doing;
- previous shared events;
- missed commitments;
- jokes/routines;
- group relationships.

Dynamic greeting/farewell is useful.

Example:

Bad:

```text
"Hey."
```

every time.

Better:

```text
"There you are."
"You survived."
"I was starting to think I'd have to text you."
```

only when context supports it.

Do not overuse relationship-specific greeting variants.

Ordinary greetings remain important.

---

# 29. Conflict / Friction Philosophy

Relationships need imperfection without artificial drama.

Good friction:

- disagreement over a poster/art judgement;
- missed commitment;
- feeling ignored after prolonged absence;
- professional disagreement;
- misunderstanding that can be repaired.

Bad friction:

- random betrayal roll;
- huge argument only because relationship level reached a threshold;
- NPC becoming irrational to manufacture drama.

A repaired disagreement can become a later commitment qualifier because it proves the relationship can absorb something imperfect.

---

# 30. Current Major Story Priorities

## Priority A — Zoe consolidation / relationship spine

- beach dating breakpoint;
- director CG handoff;
- first-kiss contract protection;
- post-dating ordinary life;
- replayable gym activity.

## Priority B — Zoe should stop expanding after the core is solid

Once Zoe v1 has:

- coherent reveals;
- art arc;
- music history;
- relationship breakpoints;
- ordinary dating life;
- group integration;

development should move outward rather than adding infinite Zoe scenes.

## Priority C — Eli and Nora depth

Bring them to the same level of personhood.

Eli:

- Still Working?
- Second Pair of Eyes
- Demo Night

Nora:

- Quiet Hour
- Rough Shift
- After Closing

## Priority D — group dynamics

More scenes where the player sees NPCs knowing one another.

## Priority E — Art & Culture Night

Next major convergence event.

---

# 31. Known Canon Traps / Do Not Reintroduce

1. **Rena working in diner** — wrong. Rena works at Eleven; diner only off duty.
2. **Marcus at gym** — wrong. Sport does not imply gym schedule.
3. **Generic Talk revealing Zoe's strongest facts before authored scenes** — avoid.
4. **Duplicate Zoe gallery arcs** — use one coherent exhibition path.
5. **Generic first kiss stealing an authored Zoe dating breakpoint** — protect the milestone.
6. **Large relationship state changes from raw points alone** — authored scene owns state change.
7. **Every character waiting for MC to create their social life** — NPCs need pre-existing links.
8. **Major event becomes mandatory chapter gate** — shared event is convergence, not chapter completion.
9. **CG generation before scene architecture is decided** — define event/roster/branching first.
10. **AI inventing CG filenames/director content** — director owns final visual subscene.
11. **Permanent schedule modification for one date** — use temporary invitation/commitment override.
12. **Career skill automatically equals romance success** — competence primarily affects respect/opportunity/context.
13. **Quiet day treated as failure** — quiet life is part of the simulation.

---

# 32. AI Working Rule

Before modifying the project:

1. identify the exact task;
2. read `QWEN_WORKMAP.md`;
3. read only relevant canonical docs;
4. inspect current source;
5. find canonical helpers;
6. change the minimum complete file set;
7. preserve authored dialogue unless explicitly asked to rewrite;
8. preserve save compatibility;
9. inspect diff;
10. run available checks;
11. report exactly what changed.

For current local Qwen work, the master bible is context; `QWEN_WORKMAP.md` is the operational pointer.

---

# 33. Short Project Summary

SimDays should ultimately feel like a city in which the player gradually becomes embedded.

The important long-term transition is:

```text
new apartment
↓
strangers and practical routines
↓
recognizable regulars
↓
friends
↓
shared social group
↓
professional identity
↓
private routines with specific people
↓
relationships with history
↓
a city that feels personally inhabited
```

The story does not end because a bar reaches 100.

A bar makes a moment plausible.

The authored moment gives the number meaning.

The strongest relationship scenes should therefore be remembered by:

- where they happened;
- what was said;
- what the characters did;
- what changed afterward;

not by the threshold that unlocked them.

---

# 34. Maintenance Rule for This Document

This file should change only when one of these changes:

- major character canon;
- location ownership/workplace;
- relationship milestone architecture;
- major event structure;
- career/world architecture;
- director handoff convention;
- large story cluster;
- canonical system ownership.

Do **not** update this master file after every small dialogue edit.

For day-to-day development use:

```text
QWEN_WORKMAP.md
```

For exact source truth:

```text
current .rpy / .py files
```

For historical detail:

```text
docs/archive/
```

This document is the map of the game, not the commit log.
