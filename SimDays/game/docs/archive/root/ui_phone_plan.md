# UI progression + Phone — plan (draft for review)

Decision locked: **advanced stats live in a slide-in Profile panel now; the phone
is a separate system built later** (SMS, events, contacts). Topbar stays lean
(time / money / needs) for at-a-glance info.

---

## 1. Graphics to generate next

### A. UI icons (needed for the Profile panel)
| Asset | Why |
|---|---|
| `stat_app` | Appearance skill — used in code, no icon yet |
| `stat_work` / `stat_performance` | Job Performance bar — the core Sims-like meter |
| (optional) `stat_chr` proper | we reuse `stat_social` as CHR; fine, but a dedicated one is cleaner |

→ One small sheet (2–3 icons), same circular style as the others.

### B. Location backgrounds — real gaps
| Asset | Note |
|---|---|
| **The Hub — IT office interior** | corporate (`goodoffice1`) currently doubles as everything; IT career from jobs_system needs its own room (desks, monitors, startup vibe) |
| **Hospital — usable interior** | `hospital1` exists but the location is a stub; if we build a health/job hook we want a reception-with-NPC shot |
| (low priority) night variants | `bar`, `gym`, `warehouse` have no night version — reuse day for now |

### C. Character sprites still missing (from sprite_briefs.md)
- **Sam** (park runner) and **Anna** (café regular) — briefed, not generated
- **Becca** (gym) — no sprites at all
- Marcus/Martha/Zoe are covered

### D. Phone assets (for later — section 3)
- App icons (6–8 small tiles)
- Phone frame OR a frameless rounded panel (see build options)

> Likely placeholder you saw: **Hospital** ("Nothing you need here right now") — a
> deliberate stub, or the generic **office** standing in for Nexus Tower.

---

## 2. Advanced stats UI — the Profile panel

A slide-in panel (from the right) that reuses the glass-bar aesthetic already in
the activity menu. Opened by a small button on the topbar (a portrait/☰ icon) or
a hotkey. Pauses nothing — it's an overlay you dismiss.

### Layout (top → bottom)
```
┌───────────────────────────┐
│  [name]        Day 3 · 14:00 │   header: name + date/time
├───────────────────────────┤
│  SKILLS                     │
│  💪 Strength    ▓▓▓▓░░ 42    │   4 bars, stat icon + label + value
│  🧠 Intellect   ▓▓░░░░ 23    │
│  💬 Charisma    ▓▓▓░░░ 31    │
│  ✨ Appearance  ▓░░░░░ 14    │
├───────────────────────────┤
│  WORK                       │
│  Junior Dev @ The Hub       │   current job + rank
│  Performance  ▓▓▓▓▓░ 78 / 100│   THE key Sims-like meter
│  Next rank: INT 50 (you 23) │   promotion gate, live check
│  Shift: Mon–Fri 09–17       │   schedule reminder
├───────────────────────────┤
│  (no job → "Unemployed —    │
│   find work in the city")   │
└───────────────────────────┘
```

- **Skills**: horizontal bars, same rounded style, colour-coded (STR red, INT
  blue, CHR gold, APP violet). Value shown as number.
- **Work block**: only shows if employed. Rank title, Performance bar (accent
  colour), promotion requirement with your current stat inline so you see the
  gap. If no job: a prompt line.
- Reuses `act_bar_idle.png` framing + Quicksand SemiBold → zero new UI style work.

### Build steps
1. Data: `job_career`, `job_rank`, `job_performance` in data.rpy (from jobs_system).
2. `screen profile()` — the panel above, `zorder 20`, dismiss on click-outside/Esc.
3. Topbar: add a small button that does `ShowMenu`/`Show("profile")`.
4. Bind a key (e.g. `C`) as a shortcut.

This is self-contained and doesn't touch the phone. Ship it as the next UI step.

---

## 3. The phone — concept + how to build it

A separate overlay, built after the Profile panel. It's the "living" layer:
messages, contacts, apps. Think a smartphone that slides up from the bottom.

### App set (start small, grow)
| App | Content | Phase |
|---|---|---|
| **Messages** | texts from Marcus etc.; drives events ("Free Saturday? Park.") | 1 (first) |
| **Contacts** | met NPCs, their Affection/Trust, where/when to find them | 1 |
| **Map** | fast-travel (replaces opening the big map) | 2 |
| **Jobs** | gig board + job applications (career apply, gig work) | 2 |
| **Bank** | balance, rent countdown, Marcus loan | 2 |
| **Calendar** | shifts, appointments, event reminders | 3 |

> Note: the phone **won't** duplicate the Profile panel skills — those stay in
> Profile. The phone is comms + world-interaction. (If it feels redundant later
> we can fold Profile into a phone "Me" app, but not now.)

### Build options (pick when we get there)
- **Frameless panel** (lazy, recommended start): a rounded dark panel on the
  right ~32% of screen, a status bar (time/battery flavour), a grid of app
  icons. No phone-frame art needed — pure Ren'Py frames + our glass style.
- **Framed phone** (prettier, more art): a phone-frame PNG; app screens render
  inside its "screen" area. Needs a phone frame asset + more careful positioning.

Recommended: **frameless first**, one app (Messages) as vertical slice, then add
Contacts. Messages doubles as the event-delivery system (Marcus texts unlock
hangouts) — high gameplay value for low art cost.

### Mechanics hook
- Messages arrive on `new_day()` or on triggers (affection thresholds). A small
  notification dot on the phone button.
- Tapping a message → can jump to a scene/label (this is how events fire).

---

## Suggested order
1. Generate **`stat_app` + `stat_work`** icons (tiny sheet).
2. Build **Profile panel** (skills + Performance) — needs the jobs data model.
3. Implement **jobs_system** data + one career (IT via The Hub) end-to-end.
4. Generate **The Hub** background.
5. Build **phone** frameless with **Messages** app → wire Marcus's first text.
