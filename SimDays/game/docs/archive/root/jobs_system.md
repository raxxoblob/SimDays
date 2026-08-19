# Jobs & Work System (Sims-like) — design draft

More **life-sim than VN**: jobs mean *showing up on time and working*, a **Performance bar** that climbs when you attend and **decays when you skip**, and **promotions** that (in the right careers) eventually buy you back your freedom. Draft for review — supersedes the Jobs section in [game_design.md](game_design.md).

---

## Two kinds of work

### A. Career jobs — fixed schedule, ladder, performance
- You must **be at the workplace during shift hours** (e.g., Corporate 09:00–17:00, Mon–Fri).
- Working a shift raises a **Performance bar** for your current rank.
- **Miss scheduled shifts → Performance decays.** Let it fall too far → probation → fired (drop a rank / lose the job).
- Fill Performance **and** meet the rank's stat requirement → **promotion**: more pay, higher requirements, and (near the top) **flexible hours**.
- Higher pay, real progression, but demands discipline + stats.

### B. Gig / casual work ("dorywcza") — freedom, no ladder
- **No schedule** — do it anytime the place is open, for as long as you want.
- **Lower pay per hour**, but instant cash whenever.
- **No promotion, no stat requirements, little/no skill growth.**
- The safety net so nobody feels chained: broke? do a gig. Examples: warehouse day-labor, food delivery, flyering, weekend event security, bar-back shifts.

> Design intent: early game you lean on gigs; mid game you commit to a career and grind the ladder; late game a **manager-tier career gives flexible hours**, so you get freedom *back* — the aspirational payoff.

---

## The Performance bar (career jobs)

Per job, for your **current rank**, a value 0–100.

| Event | Effect |
|---|---|
| Complete a scheduled shift | **+Performance** (base) |
| Shift while needs OK + stat check passed | **+Performance bonus** (do the job *well*) |
| Shift while exhausted/hungry (low needs) | reduced gain (you underperform) |
| **Miss a scheduled work day** | **−Performance** |
| Several misses in a row | Warning → **Probation** → **Fired** (lose rank/job) |
| Performance ≥ promo threshold **and** rank stat met | **Promotion review** event → next rank |

- Promotion resets Performance for the new (harder) rank, raises pay + requirements.
- Decay only counts days the job **expected** you (respects weekends/days off).
- Energy/Hunger/Hygiene feed into how *well* you work (Sims-like: tired worker = slow progress).
- UI: a **Work bar** shown on the job screen (current rank + Performance %), plus a subtle indicator when you're skipping and it's dropping.

---

## Career ladders by workplace

Not every job promotes. Where it does, higher ranks need higher stats; the top tier often unlocks **flexible hours** (no fixed show-up).

### IT / The Hub — full ladder, ends flexible ⭐
| Rank | Needs | Pay | Hours |
|---|---|---|---|
| Junior Dev | INT 35 | low | fixed, must show up |
| Mid Dev | INT 50 | medium | fixed |
| Senior Dev | INT 65, CHR 30 | high | fixed, some leeway |
| Team Lead | INT 75, CHR 45 | higher | mostly flexible |
| **Manager / Co-founder** | INT 85, CHR 55 | top | **flexible — work when you want** |

### Corporate — Nexus Tower — full ladder
Intern → Associate → Analyst → Senior → Team Lead → **Manager** (INT + rising CHR). Similar shape to IT; Manager = flexible hours. More politics (ties to Martha/Bradley/Caroline events).

### Physical — Warehouse / Garage — short ladder, stays scheduled
Floor Worker → Crew Lead → Shift Supervisor (STR-gated). Solid hourly pay, but **schedule-bound even at the top** (blue-collar shifts). Good early STR + money.

### Gym — Personal Trainer — short ladder
Assistant Trainer → Trainer → Head Trainer (STR/APP/CHR). Flexible-ish hours (you book clients), scales with your own stats. Ties to Becca/Tommy/Victor.

### Café "Grounds" — **no promotion (by design)**
Flat role, **low pay**, flexible-ish shifts, but high **CHR gain** + social hub (Zoe, Anna, Henry). It's the "nice, easy, people-y" job — not a career. You stay a barista; the value is money-while-you-socialize + story, not a ladder.

### Restaurant / Bar — light ladder + gig overlap
Server → Shift Lead (CHR). Bar also offers **gig** security/bar-back work (no ladder). Marcus's world.

---

## Casual / gig jobs (no schedule)

| Gig | Where | Pay | Notes |
|---|---|---|---|
| Warehouse day-labor | LogiCity | low-med hourly | STR flavor, no ladder |
| Food delivery | anywhere | low, per-run | do between other stuff |
| Bar-back / security | Static | med, nights | Marcus can hook you up |
| Odd jobs / flyering | Mall, street | low | pure cash filler |

Do any of these anytime the venue's open. No stats needed, no decay, no promotion — just hours-for-cash on your terms.

---

## How it ties into the rest

- **Time system:** shifts consume hour blocks; skipping means you spent those hours elsewhere (and Performance drops).
- **Needs:** show up hungry/exhausted → weaker Performance gains (maybe a bad-day event). Manage needs to climb faster.
- **Stats:** career jobs both *require* and *grow* stats (Corporate/IT → INT, Warehouse → STR, Café → CHR, Trainer → STR/APP/CHR).
- **Freedom curve:** chained early (need money, low rank, fixed hours) → free late (manager flex hours, or coast on gigs). This is the core Sims-y arc.
- **Relationships:** workplaces are where you meet their NPCs; performing/attending naturally puts you near them (Zoe at café, Ray/Natalie at warehouse, etc.).

---

## Open questions
1. **Firing:** hard-fire (lose the job entirely, must re-apply) or soft (demote a rank)? I lean demote-then-fire.
2. **Performance numbers:** starting +gain per shift, −decay per miss — want me to propose concrete values and a sample week?
3. **Multiple jobs:** keep the "1 full-time career + 1 gig/part-time" rule from game_design.md?
4. **Flexible-hours meaning:** at manager tier, do you still *go* to work (just any hours) for the pay, or can it partly auto-earn while you do other things?
5. **Which career to build first** as the vertical slice — IT (cleanest junior→manager ladder) or Warehouse (simple, STR, early-game)?
