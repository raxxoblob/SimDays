# LivingTheDream — Project Index

## What This Is

**LivingTheDream / SimDays** is a Ren'Py life-sim visual novel (1920×1080).
The MC moves to a new city and builds a life — relationships, career, money, skills — over open-ended simulated days.

**Ren'Py game root:** this directory (`game/`).

All `.rpy` files, `images/`, and `audio/` live here.
`images/` is accessed via a directory junction — do not move it.

---

## Canonical Documentation

All docs are relative to this directory (`game/`).

| Task | Read First |
|---|---|
| Writing or editing an NPC (personality, voice, events) | `docs/CHARACTERS.md` |
| Adding a story scene, major event, or narrative arc | `docs/STORY_AND_EVENTS.md` |
| Gym / skills / money / activity mechanics | `docs/GAMEPLAY_SYSTEMS.md` |
| Finding helpers, files, call flows, system contracts | `docs/TECHNICAL_ARCHITECTURE.md` |
| Coding or directing constraints for AI/Qwen | `docs/DEVELOPMENT_RULES.md` |
| Current Zoe beach/gym implementation work | `QWEN_WORKMAP.md` |
| Active director handoff targets | `DIRECTOR_TODO.md` |

**Do NOT read every documentation file for every task.** Use this index.

Historical and superseded documents are in `docs/archive/`. They are preserved but not canonical.

---

## File Structure

```
game/                          ← Ren'Py root (you are here)
├── PROJECT_INDEX.md           ← this file
├── QWEN_WORKMAP.md            ← current implementation work
├── DIRECTOR_TODO.md           ← active director handoff list
├── docs/
│   ├── CHARACTERS.md
│   ├── GAMEPLAY_SYSTEMS.md
│   ├── STORY_AND_EVENTS.md
│   ├── TECHNICAL_ARCHITECTURE.md
│   ├── DEVELOPMENT_RULES.md
│   └── archive/               ← 55 historical docs, not canonical
└── *.rpy                      ← game source
```

---

## Current Project Priority

The current active work is:

1. **Zoe Beach Dating Breakpoint (M2)** — engine implemented; director CG subscene pending.
   - Parent scene: `zoe_beach_dating_scene` in `zoe_romance_milestones.rpy`
   - Director file needed: `game/director_romance/romantic_subscene_zoe_beach_dating.rpy`
   - Transition: `interested → dating`, canonical first kiss

2. **Zoe Replayable Gym Training** — design ready; implementation next.
   - Shared workout activity after dating/committed
   - Director CG file needed: `game/director_romance/romantic_subscene_zoe_gym_training.rpy`

3. **Phase 65 — Hobbies** — capability system, painting vertical slice; next after Zoe gym.

4. **Director-owned CG subscenes** — `game/director_romance/` directory does not yet exist; all listed files are PLANNED.

For implementation detail on items 1–2, read `QWEN_WORKMAP.md`.
For the director handoff list, read `DIRECTOR_TODO.md`.
