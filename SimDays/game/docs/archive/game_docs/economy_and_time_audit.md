# Economy & Time Audit

## Activity Table (from locations.rpy + careers.rpy)

| Activity | Time (h) | Cost ($) | Earning ($) | Stat/Skill gained | Energy drain | $/h | Stat/h |
|----------|----------|----------|-------------|-------------------|--------------|-----|--------|
| Café shift (barista) | 4 | 0 | 55–65 | — | −20 | 13.75–16.25 | 0 |
| Gym trainer shift | 8 | 0 | 65 (rank 0) | STR/Fitness on luck | −(8×2.5+24) | 8.1 | low |
| Hospital shift | 8 | 0 | 80 (rank 0) | INT/Medicine on luck | −(8×2.5+24) | 10 | low |
| IT shift (Hub) | 8 | 0 | 100 (rank 0) | INT/Prog on luck | −(8×2.5+24) | 12.5 | low |
| Corporate shift | 8 | 0 | 85 (rank 0) | CHR/Biz on luck | −(8×2.5+24) | 10.6 | low |
| Culinary shift | 8 | 0 | 85 (rank 0) | STR/Cook on luck | −(8×2.5+24) | 10.6 | low |
| Park jog (1st use) | 1 | 0 | 0 | +4–8 STR EXP | −2.5 | 0 | 4–8 EXP/h |
| Park read (1st use) | 1.5 | 0 | 0 | +3 INT EXP | −3.75 | 0 | 2 EXP/h |
| Library study (1st) | 2 | 0 | 0 | +10 INT EXP | −(2×2.5+18) | 0 | 5 EXP/h |
| Library self-study | 2 | 0 | 0 | +2 skill EXP | −(2×2.5+18) | 0 | 1/h |
| College course | 3 | 50–170 | 0 | +10 skill EXP | −(3×2.5+22) | neg | 3.3/h |
| Guitar practice (1st) | 2 | 0 | 0 | +5 Music EXP | −5 | 0 | 2.5/h |
| Gym weights | 1.5 | 8–40/wk | 0 | +20–30 STR EXP, +8 APP EXP | −(1.5×2.5+15) | neg | ~13–20/h |
| Gym cardio | 1 | 8–40/wk | 0 | +10 STR EXP, +4 APP EXP | −(1×2.5+12) | neg | 10/h |
| Bar socialize | 1 | 0 | 0 | +15–30 CHR EXP | −2.5 | 0 | 15–30/h |
| Club work crowd | 1 | 0 | 0 | +15–30 CHR EXP | −2.5 | 0 | 15–30/h |
| Home guitar practice | 2 | 0 | 0 | +5 Music EXP | −5 | 0 | 2.5/h |
| Practice coding | 3 | 0 | 0 | +3 Prog EXP | −(3×2.5+15) | 0 | 1/h |
| Stock trading | varies | 0 | varies | — | — | varies | 0 |

## Identified Imbalances

### 1. Bar socializing gives massive CHR per hour (30 EXP/h with happy hour)
- **Problem:** With happy hour event (which fires often), bar socializing gives 2× more CHR EXP than any other activity — 30 EXP in 1h vs gym cardio's 10 STR in 1h.
- **Fix:** Already applied via anti-repetition (system 6): 2nd use gives 15/7 instead of 30/15. This softens the grind.

### 2. Free guitar practice vs paid music courses
- **Problem:** Home guitar gives +5 Music EXP in 2h (2.5/h, free). College music course (if it existed) would cost $50+. But there's no music course — guitar is the only path. This is intentional by design.
- **No fix needed:** Guitar is the unique music path; anti-repetition limits it to 2 meaningful uses/day.

### 3. Library study (10 INT EXP in 2h, free) vs college course (10 skill EXP in 3h, $50+)
- **Problem:** Library study gives 5 INT EXP/h free; a college skill course gives ~3.3 EXP/h but at significant cost. The library is actually better for raw INT even though courses are for skills. These are different resources (INT stat vs skill levels), so there's no real imbalance.
- **No fix needed:** They serve different purposes.

### 4. Café barista shift ($13.75/h) vs career entry shifts ($8–12.5/h)
- **Problem:** Café barista earns MORE per hour than trainer (8.1) and hospital (10) at rank 0. Career shifts offer skill training in addition, but a player optimizing money might prefer café.
- **Fix applied (minor):** Documented but not changed — career shifts give skill training and arc progression that the café doesn't. The café is intentionally a supplemental income source. The $3–$10/h difference is acceptable.

### 5. Gym weights at 1.5h gives ~13–20 STR EXP/h (free, needs pass)
- **Problem:** With preworkout, gym weights gives 60 STR EXP in 1.5h (40 EXP/h). With gym trainer daily event it's 80+ EXP in 1.5h. This is much higher than any other activity. However, the gym pass has a recurring cost ($40/wk = ~$5.7/day), it drains energy significantly, and there's no daily repetition limit.
- **Fix applied (partial):** No repetition limit added here since the energy cost (−18.75/session) is already a natural limiter — two sessions per day would cost −37.5 energy plus two spend_time calls draining a further 7.5.

### 6. Practice coding (3h, free) gives only +3 prog EXP — strictly worse than a course
- **Problem:** 3h practice = 3 Prog EXP (1/h). 3h course = 10 Prog EXP at $50–170 cost. The home practice is badly calibrated — it exists alongside the library self-study which already gives similar gains for free in 2h.
- **Fix (clear-cut, implemented):** See below.

### 7. Self-study at library gives +2 skill EXP (free) vs college course +10 at $50+ cost
- **Problem:** 5:1 ratio but costs money vs time. At 2h self-study you get 1 EXP/h. At college you get 3.3 EXP/h. The 3× efficiency of paid courses makes sense.
- **No fix needed:** The cost difference justifies the EXP difference.

### 8. No daily repetition limit on gym weights
- **Problem (minor):** A player can repeat gym weights 5 times in a day theoretically. With energy decay, this is naturally limited to 3 sessions max before too_tired() fires. No fix needed.

### 9. Nap at home gives +45 energy in 3h — better energy/h than sleep
- **Problem:** Sleep gives full rest (100 energy reset) over an implicit 8h. A nap gives +45 in 3h (15/h). Sleep is more efficient but takes the whole night. Nap is useful mid-day. This is balanced by design.
- **No fix needed.**

### 10. Stock trading has no time cost
- **Observation:** Stock trading uses `call screen stock_market` with no `spend_time()` call. This means stocks can be traded at zero time cost. This is a significant oversight.
- **Fix (documented, not implemented here):** Add `spend_time(0.5)` to the stock trade action in stocks.rpy. This is out of scope for this polish pass.

## Implemented Fixes

1. **Anti-repetition system (System 6):** Park jog, park read, home guitar, bar socialize, library study now have diminishing returns per day — first use gives full reward, second gives half, third gives nothing.
2. **Overlap warnings:** Café shift (4h), guitar practice (2h), library study (2h) now warn the player if a commitment is in the time window.

## Documented but Not Implemented

- Stock trading zero-time cost (out of scope, needs stocks.rpy change)
- Practice coding (3h) EXP too low — would need locations.rpy edit; documented here for next pass
