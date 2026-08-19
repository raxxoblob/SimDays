# Living the Dream — Game Design Document v0.2

## Concept

A modern sandbox dating sim / VN set in a fictional American city. The player is a young adult who just moved there — blank slate, knows nobody, starting from scratch. The game blends stat management, career progression, and relationship building with characters met through different walks of life.

Core principle: every job and every location has its own social circle. There's no universal pool of NPCs available from day one.

---

## City — Map & Navigation

### Presentation
One single city map image with clickable location icons. Clicking a location takes you directly to that location's background screen with its action menu. No district sub-screens — locations are just dots on the map. This keeps navigation fast and avoids extra screens that add little value.

### Locations

**Home**
- **Your Apartment** — sleep, cook, browse phone, shower, manage inventory

**Around Town** *(all on one map)*
- **Coffee Shop "Grounds"** — hang out, work (barista), casual dates
- **City Park** — morning jog (STR/energy), random encounters, reading (INT)
- **The Mall** — buy clothes (APP), electronics, gifts for NPCs
- **Bar "Static"** — networking, night out, events (unlocks via CHR)
- **Nexus Tower** — corporate career path
- **The Hub (Coworking)** — IT / freelance career path
- **Restaurant "Eleven"** — waiter job or date location
- **LogiCity Warehouse** — physical labor career path
- **Krawczyk's Garage** — mechanic work
- **Iron Gate Gym** — train STR, meet athletes
- **City Library** — study INT, meet students
- **Community College** — optional courses (boost INT or unlock job paths)
- **Grocery Store** — buy food (needed for hunger/cooking at home)

---

## Stats System

### Core Stats (built up over time, 0–100)
| Stat | Short | How it grows | What it unlocks |
|---|---|---|---|
| Strength | STR | Gym, physical jobs | Manual labor jobs, certain dialogue options |
| Intelligence | INT | Library, courses, IT work | White-collar jobs, smarter conversation choices |
| Charisma | CHR | Socializing, bar, dating | Persuasion, first impressions, promotions |
| Appearance | APP | Clothes shopping, gym, grooming | First impressions, certain locked scenes |

### Needs (decay daily, must be maintained)
| Need | Decays | How to restore | Penalty if neglected |
|---|---|---|---|
| Hunger | Every few hours | Eat at home, restaurant, grocery | Low energy, mood debuff on dialogue |
| Hygiene | Daily | Shower at home | APP penalty, some NPC interactions blocked |
| Energy | Activity + hours awake | Sleep (required), food | Stat gains halved, can't work effectively |

Needs aren't stats you level — they're a floor to maintain. The game shouldn't feel like a chore, so decay is slow enough that a player focused on social content won't micro-manage them constantly. But neglect for multiple days has real consequences.

### Resources
- **Money** — earned from jobs, spent on food, clothes, rent, dates, courses
- **Time** — the main resource (see below)

### Unlock Examples
- STR ≥ 30 → can apply to warehouse / garage jobs
- INT ≥ 35 → unlocks IT track, advanced dialogue at college
- CHR ≥ 25 → "strike up a conversation" option at bar with new NPCs
- CHR ≥ 40 + APP ≥ 35 → invited to a closed party (new NPCs)
- Money ≥ $5,000 → can upgrade to better apartment (unlocks NPC options)
- Hygiene < 20 → NPC refuses hangout, certain scenes blocked
- Hunger < 15 → energy won't restore fully from sleep

---

## Time System

### Hours-based day
The day runs from **7 AM to 3 AM** (20 hours). Every action has a time cost in hours. The player picks what to do hour by hour — no rigid slots, just a clock ticking forward.

```
7:00 AM  — Wake up (alarm or natural)
           Shower: 0.5h | Breakfast: 0.5h | Check phone: 0.5h
8:00 AM  — Morning block: gym, work, library, park jog
12:00 PM — Midday: lunch, errands, short social meet
2:00 PM  — Afternoon: work continues, coworking, college
6:00 PM  — Evening: dates, hanging out, bar, cooking dinner
10:00 PM — Night: bar events, phone conversations, Netflix at home
3:00 AM  — Hard cutoff. If not in bed, auto-sleep → energy penalty next day
```

### Approximate action durations
| Action | Time cost |
|---|---|
| Work shift (full-time) | 6–8h |
| Work shift (part-time / sidejob) | 3–4h |
| Gym session | 1.5h |
| Library study | 2h |
| Cooking at home | 1h |
| Quick meal (out) | 0.5h |
| Casual hangout with NPC | 2h |
| Planned date | 3h |
| Sleep (recommended) | 8h — less causes energy debt |
| Shower | 0.5h |

### Weekly rhythm
- **Mon–Fri**: jobs fully available, library open, college classes
- **Sat–Sun**: no full-time work, more NPC events, bar is busier
- **Every few weeks**: a seasonal event — sports competition, company outing, city festival — brings multiple NPCs together in one scene

### Long-term progression
- Game runs for **1 in-game year** (52 weeks) → soft ending, reflects on choices
- After year one: sandbox mode, no pressure
- Quarterly milestones unlock new locations / events (e.g., after 3 months at a job a new story arc opens)

---

## Jobs System

### Rules
- Player can hold **one full-time job** + **one part-time / sidejob** simultaneously
- Quitting is always possible but may affect relationships with coworkers
- Promotion requires a stat check at the relevant rank threshold — no auto-leveling
- Each workplace has **unique NPCs** not found elsewhere

---

### Career Paths

#### A. Corporate — Nexus Tower
**Entry requirement:** INT ≥ 20  
**Grows:** INT (passive reading, meetings), Money  
**Hours:** Mon–Fri, 8h shift  
**Ranks:** Intern → Associate → Analyst → Senior → Team Lead → Manager  
**Unique NPCs:** Martha (coworker, sharp and cynical), Bradley (boss, high-pressure), Caroline (HR, knows everyone's secrets)  
**Story arc:** office politics, a coworker being pushed out, loyalty vs. self-interest

#### B. Food & Beverage — Coffee Shop / Restaurant
**Entry requirement:** CHR ≥ 15  
**Grows:** CHR, Money (tips vary)  
**Hours:** flexible, 4–6h shifts  
**Ranks:** Trainee → Barista/Server → Shift Lead → Manager  
**Unique NPCs:** Zoe (coworker, aspiring artist), Henry (owner, old-school), Anna (regular customer, mysterious)  
**Story arc:** Zoe wants to open her own place — player can back her or stay out of it

#### C. Physical — Warehouse / Garage
**Entry requirement:** STR ≥ 25  
**Grows:** STR, Money (solid hourly rate)  
**Hours:** early shifts (6 AM–2 PM or 2 PM–10 PM)  
**Ranks:** Floor Worker → Crew Lead → Shift Supervisor  
**Unique NPCs:** Ray (loyal buddy, rough around the edges), Natalie (warehouse manager, no-nonsense), Chris (mechanic mentor)  
**Story arc:** Ray is in financial trouble — player can help, loan money, or stay out of it

#### D. IT / Freelance — The Hub (Coworking)
**Entry requirement:** INT ≥ 35  
**Grows:** INT, Money (irregular, high ceiling)  
**Hours:** flexible — player chooses hours, income varies  
**Ranks:** Freelancer → Regular Client Base → Senior Dev → Co-founder  
**Unique NPCs:** Jake (potential co-founder), Mia (designer client, creative), Dave (senior mentor)  
**Story arc:** Jake proposes a startup — requires INT + CHR + capital to pursue

#### E. Personal Trainer — Iron Gate Gym
**Entry requirement:** STR ≥ 40, APP ≥ 25  
**Grows:** STR, CHR, APP  
**Hours:** flexible, morning heavy  
**Ranks:** Assistant Trainer → Trainer → Head Trainer  
**Unique NPCs:** Tommy (rival trainer), Becca (ambitious client), Victor (gym owner, ex-athlete)  
**Story arc:** local fitness competition — seasonal event, unlocks new story beats

#### F. Security — Sidejob (bars & events)
**Entry requirement:** STR ≥ 30, APP ≥ 20  
**Type:** Part-time / sidejob only, weekends  
**Grows:** STR, Money  
**Unique NPCs:** met through nightlife — a separate social web  
**Note:** opens access to nightlife characters not reachable any other way

---

## Characters — NPC Overview

### Discovery rule
NPCs are tied to jobs and locations. The player doesn't see a character list — they discover people naturally through activity. Someone you meet at the gym won't be waiting at the coffee shop.

### Roster (to be expanded)

| Name | Gender | Where you meet | Relationship type |
|---|---|---|---|
| Martha | F | Corporate | Romance / rivalry |
| Zoe | F | Coffee Shop | Romance / friendship |
| Ray | M | Warehouse | Friendship / bro-story |
| Jake | M | Coworking | Friendship / business partner |
| Natalie | F | Warehouse | Romance / antagonist arc |
| Anna | F | Coffee Shop (customer) | Slow-burn mystery romance |
| Becca | F | Gym | Romance / competitive |
| Mia | F | Coworking | Romance / creative scene |
| Tommy | M | Gym | Rival → friend |
| ??? | ??? | Bar (CHR ≥ 40 unlock) | Late-game secret character |

Each character has:
- **Affection** (0–100)
- **Trust** (0–100) — separate, because you can like someone you don't trust
- Scene triggers based on stat checks + affection/trust thresholds
- Multiple possible endings: friend, partner, falling out, neutral drift

---

## UI Sketch

```
[ CITY MAP — single image, clickable location icons ]

Clicking a location icon → location background + action menu

[ HUD — always visible ]
Mon, March 14  |  2:30 PM           $1,840
STR: 28  INT: 41  CHR: 33  APP: 30
Hunger: ████░░  Hygiene: ███░░░  Energy: █████░
```

- Phone as a mini-menu (texts from NPCs, event calendar, relationship status)
- Character journal — affection and trust bars visible only after a certain familiarity threshold
- Time clock always visible — player always knows the cost of their next action

---

## Open Questions

1. **Protagonist gender** — fixed male, or player choice at start?
2. **Romance options** — hetero only, or can the player romance NPCs of any gender?
3. **18+ content** — separate patch (standard Ren'Py approach) or built-in?
4. **Art style** — own assets, stock VN sprites, AI-generated, or commissioned?
5. **MVP scope** — how many jobs and NPCs for a first demo build?
