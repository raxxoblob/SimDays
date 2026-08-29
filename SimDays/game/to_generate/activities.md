# Activities — plan & balance

## Balance philosophy

| Tier | Cost | Gain/h | Examples |
|---|---|---|---|
| Free, low-effort | $0 | +5–8 stat/h | Park jog, beach relax, read in park |
| Free, focussed | $0 | +8–12 stat/h | Library study, home guitar |
| Paid, consumable | $10–20/session | +15–20 stat/h | Gym supplements |
| Paid, subscription | $40–120/period | full gym access | Gym week/month pass |
| Paid, course | $50–200 | +1 skill level | College courses |

**Rule:** a free park jog should never be as good as a paid gym session.
Going to the gym with a week pass + preworkout should be ~3× more EXP/h than a free jog.

---

## Gym — membership gate (⚠️ implement in code)

Currently gym is **free** — must add a pass system.

```
default gym_pass_expires = -1   # game day when pass runs out (-1 = no pass)
```

At gym entry: if `day >= gym_pass_expires`, show reception only:
- **Week pass ($40)** → `gym_pass_expires = day + 7`
- **Month pass ($120)** → `gym_pass_expires = day + 30`
- "Just looking" → jump back

With pass: full activity menu as now.
Without pass: only reception options.

Icon needed: `icon_gym_pass.png` (or reuse `icon_gym`).

---

## Beach — missing activities (implement in code)

Current: only "Relax (1h) +10 energy"

Add:
| Activity | Time | Cost | Gain | Notes |
|---|---|---|---|---|
| Swim (1h) | 1h | free | +6 STR, +4 APP | daytime only |
| Sunbathe (1.5h) | 1.5h | free | +6 APP | daytime only, -5 energy |
| Beach volleyball (1h) | 1h | free | +6 STR, +5 CHR | needs time of day check |
| Night swim (1h) | 1h | free | +6 STR | night only, slight risk flavour |

---

## Park — missing activities (implement in code)

Current: jog (+8 STR), basketball (+12 STR), read (+8 INT)

Balance fixes:
- Basketball (+12 STR) → reduce to **+8 STR** (same as jog, free)

Add:
| Activity | Time | Cost | Gain | Notes |
|---|---|---|---|---|
| Sit and rest (1h) | 1h | free | +20 energy | no stat — pure recovery |
| Meditate (0.5h) | 0.5h | free | +5 INT | low gain, pure free |
| Evening walk (1h) | 1h | free | +5 CHR | night only |

---

## Library — balance fix (implement in code)

Current: general study gives **+15 INT** free — too high.

Fix: **+10 INT** per 2h session.

Self-study skill (+1 level / 2h free) is fine — slower than college, appropriate.

---

## Home — missing activities (implement in code)

Add:
| Activity | Condition | Time | Gain | Notes |
|---|---|---|---|---|
| Read a book (2h) | `own_book` flag or item in inventory | 2h | +8 INT | Bookshop / flea market purchase |
| Study at desk (2h) | `own_computer` | 2h | +10 INT, -18 energy | Alt to library; slightly less than library |
| Sketch / draw (1.5h) | `own_sketchbook` | 1.5h | +1 art skill | Slower than library self-study |

Item flags needed: `own_book`, `own_sketchbook` (default False, bought at mall/flea).

---

## College — missing courses (implement in code)

Currently no Cooking or Music course.

Add to college menu:
| Course | Cost | Time | Gain | Gate |
|---|---|---|---|---|
| Intro to Cooking | $80 | 2h | +1 `skill_cook` | none |
| Music Theory | $80 | 2h | +1 `skill_music` | none |
| Advanced Cooking | $150 | 3h | +2 `skill_cook` | `skill_cook >= 3` |

---

## Flea market — metal detector / beach search (future)

Lombard sells a metal detector ($200). Once owned (`own_metal_detector`):
- Beach: "Use metal detector (1.5h)" option appears
- Rolls on loot table: 70% junk ($0–5), 20% valuables ($20–50), 9% jewellery (random item), 1% ring (Eli quest item)
- Lombard buys junk at face value; player can sell finds

This connects the Eli ring quest (her affection gate at 60).
