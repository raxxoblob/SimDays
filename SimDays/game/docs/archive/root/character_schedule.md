# Character schedule (where + when)

Single reference for **when each character is available to talk**, and any
**unlock gate** beyond the clock. Discovery-driven: you meet people by being in
their place at the right time.

**In-game source of truth:** `game/interact.rpy` -> `NPC_DATA[...]["sched"]` and
`["gate"]`, read by `npc_here(id)`. Keep this doc and that table in sync.

## Two kinds of discovery
- **World characters** (`"world": True`) - beach, park, café regulars. You meet
  them by **showing up in their window**; the first talk is the meeting. Their
  schedule alone decides if you can talk.
- **Career characters** (`"met": "<flag>"`) - doctors, corporate, warehouse boss.
  **Invisible until introduced through the career** - no "Talk" option, no hint,
  nothing, until their `met` flag is set by a career touchpoint (first shift,
  promotion). After that, their schedule decides repeat visits.

Code: `npc_here` = present now (schedule); `npc_known` = world OR met;
`npc_talkable` = here AND known. Venues use `npc_talkable` for the Talk option.

## How to read it
- **Days**: Mon Tue Wed Thu Fri Sat Sun. Weekday index in code: Mon=0 ... Sun=6.
- **Hours**: 24h, game clock runs ~07:00-03:00 (27 = 3 AM next day).
- **Type**: World (open) or Career (hidden until met).
- **Introduced by**: what sets a career NPC's `met` flag.
- `sched` format in code: `[(days_set_or_None, (h_start, h_end)), ...]`
  (None = any day). Example Elle: `[({2}, (16, 19))]` = Wed 16:00-19:00.

---

## Live now (wired)

| Character | Location | Days | Hours | Type | Introduced by |
|---|---|---|---|---|---|
| **Nora** | Grounds (café) | every day | 08-18 | World | first café visit (scripted) |
| **Marcus** | Apartment 14 | every day | 06-11, 17-03 | World | Day 1 intro |
| **Elle** | Beach | **Wed only** | 16-19 | World | just show up (Wed) |
| **Caroline** | Nexus Tower (HR) | Mon-Fri | 09-18 | **Career** | first corporate shift |
| **Natalie** | LogiCity Warehouse | Mon-Sat | 07-15 | **Career** | first warehouse shift |
| **Dr. Lena** | City Hospital | any | 08-20 | **Career** | promotion to Resident |

---

## Planned (have sprites/templates or roster; schedule proposed)

Fill these into `NPC_DATA` as each gets wired. Proposed times below.

| Character | Location | Days | Hours | Gate |
|---|---|---|---|---|
| Zoe | Park / street-art spot | Sat-Sun | 12-18 | - (met via a gig/park, not café) |
| Henry | Grounds (café, owner) | Mon-Sat | 07-16 | - |
| Anna | Grounds (café regular) | Tue Thu | 14-18 | - (slow-burn) |
| Martha | Nexus Tower | Mon-Fri | 09-19 | work there (`job_id=="corporate"`) |
| Bradley | Nexus Tower (boss) | Mon-Fri | 10-20 | corporate rank ≥ 2 |
| Vera | Nexus Tower (reception) | Mon-Fri | 08-18 | - (gatekeeper to exec floor) |
| Prof. Adeyemi | City College | Mon-Fri | 09-15 | - (runs the courses) |
| Dr. Grant | City Hospital (chief) | any | 08-18 | hospital rank ≥ 1 |
| Dave | The Hub (IT mentor) | Mon-Fri | 09-18 | work there (`job_id=="it"`) |
| Jake | The Hub | Mon-Fri | 10-22 | IT rank ≥ 2 |
| Ray | Warehouse / Gym | Mon-Sat | 07-15 / eve | work warehouse OR gym regular |
| Becca | Iron Gate Gym | Mon Wed Fri | 17-21 | - |
| Tommy | Iron Gate Gym | daily | 15-22 | - (rival trainer) |
| Victor | Iron Gate Gym (owner) | daily | 09-20 | gym Trainer tier |
| Sam | Park | Mon-Fri | 07-10 | - (morning runner) |
| Kai | Beach | Sat-Sun | 10-18 | - (lifeguard) |
| Theo | Grounds (coworker) | days Nora is off | 08-18 | café job |

---

## Design guidelines for schedules
- **Spread people across the week** so the player plans around them (the Sims-y
  loop). Don't stack everyone at the same hours.
- **Gated NPCs** (Lena, Natalie, Bradley...) reward progression - you literally
  can't chat until you've earned access. Keeps early game from being a free menu.
- **Rare windows** (Elle: Wed only) make a character feel special / worth chasing.
- **Roommates / café leads** (Marcus, Nora) stay broadly available - they're the
  friendly onboarding characters.
- Weekend-only or evening-only NPCs give nightlife/leisure venues a reason to exist.
