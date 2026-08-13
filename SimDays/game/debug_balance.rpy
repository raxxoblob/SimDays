# Developer balance report — static economy audit screen.
# Read-only: pulls from constants, not save state.
# Access: debug_menu → "Balance report" button.

init python:

    def _dbg_balance_report():
        """Quick renpy.notify summary of key economy constants."""
        lines = []
        lines.append("RENT: T1=$220 T2=$550 T3=$1300 /week")
        lines.append("STARTING MONEY: $350")
        lines.append("GIGS: lifeguard $95/6h  guitar $70/3h  catering $80/4h  promo $110/3h  moving $55/3h")
        lines.append("WAREHOUSE: $115/8h weekday  $170/8h sunday  (req STR25)")
        lines.append("CAFE: $55/$60/$65 per 4h shift (by shift count)")
        lines.append("XP to lv10: 2200 total (20-35-55-85-125-180-250-340-460-650)")
        lines.append("PROG gates lv3/5/7/9/10 wired via freelance_submit(); MUSIC gates are placeholders (auto-open)")
        renpy.notify("  |  ".join(lines))


# ── Balance report screen ─────────────────────────────────────────────────────
screen debug_balance_scr():
    modal True
    zorder 260
    add "#000000e0"
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1100
        ysize 940
        background "#12161ef8"
        padding (28, 20, 28, 20)
        vbox:
            spacing 8
            hbox:
                text "ECONOMY & BALANCE REPORT (static constants)" font PROFILE_FONT size 24 color "#ffdd44" yalign 0.5
                textbutton "← Back" action [Hide("debug_balance_scr"), Show("debug_menu")] xalign 1.0 text_size 17 text_color "#9fb6d6"
                textbutton "✕ Close" action Hide("debug_balance_scr") text_size 17 text_color "#9fb6d6"
            null height 4

            viewport:
                scrollbars "vertical"
                mousewheel True
                ysize 840
                xfill True
                vbox:
                    spacing 10
                    xsize 1040

                    # ── STARTING CONDITIONS ───────────────────────────────────
                    text "STARTING CONDITIONS" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "Starting money:  $350" font ACT_FONT size 14 color "#cfe0f5"
                            text "Rent:  Tier 1 = $220/week  |  Tier 2 = $550/week  |  Tier 3 = $1300/week  (auto-deducted every Monday)" font ACT_FONT size 14 color "#cfe0f5"
                            text "Car payment:  car_tier × $40/week (on top of rent)" font ACT_FONT size 14 color "#cfe0f5"
                            text "Loan interest: 5%/week  |  Savings interest: 2%/week (max +$50)" font ACT_FONT size 14 color "#cfe0f5"

                    null height 4

                    # ── SKILL XP TABLE ────────────────────────────────────────
                    text "SKILL XP TABLE  (_SKILL_XP)" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "Level  XP-to-next  Cumulative-to-reach" font ACT_FONT size 14 color "#8fb0d0"
                            text "0→1    20           20" font ACT_FONT size 14 color "#cfe0f5"
                            text "1→2    35           55" font ACT_FONT size 14 color "#cfe0f5"
                            text "2→3    55           110" font ACT_FONT size 14 color "#cfe0f5"
                            text "3→4    85           195    ← PROG+MUSIC GATED (lv3 gate)" font ACT_FONT size 14 color "#e8a24d"
                            text "4→5    125          320" font ACT_FONT size 14 color "#cfe0f5"
                            text "5→6    180          500    ← PROG+MUSIC GATED (lv5 gate)" font ACT_FONT size 14 color "#e8a24d"
                            text "6→7    250          750" font ACT_FONT size 14 color "#cfe0f5"
                            text "7→8    340          1090   ← PROG+MUSIC GATED (lv7 gate)" font ACT_FONT size 14 color "#e8a24d"
                            text "8→9    460          1550" font ACT_FONT size 14 color "#cfe0f5"
                            text "9→10   650          2200   ← PROG+MUSIC GATED (lv9+10 gate)" font ACT_FONT size 14 color "#e8a24d"
                            text "" font ACT_FONT size 14 color "#cfe0f5"
                            text "Phase 63: prog gates ARE wired (freelance_submit). Music gates are placeholders." font ACT_FONT size 14 color "#ff6666"
                            text "         Phase 63B fixed the prog 9/10 circular deadlock (was hard-capped at 8)." font ACT_FONT size 14 color "#ff6666"
                            text "         Med/Biz/Cook/Fit/Mech/Art have placeholder gates (no source_prefix) — auto-open." font ACT_FONT size 14 color "#7fd06a"

                    null height 4

                    # ── GATED LEVELS per skill ────────────────────────────────
                    text "GATE STATUS BY SKILL  (gates at levels 3, 5, 7, 9, 10)" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "prog   lv3=fl_complete (BLOCKING)  lv5=fl_intermediate (BLOCKING)  lv7-10 BLOCKING" font ACT_FONT size 14 color "#ff6666"
                            text "music  lv3=busk_complete (BLOCKING) lv5=open_mic_complete (BLOCKING) lv7-10 BLOCKING" font ACT_FONT size 14 color "#ff6666"
                            text "med    all placeholder gates → auto-open (non-blocking)" font ACT_FONT size 14 color "#7fd06a"
                            text "biz    all placeholder gates → auto-open" font ACT_FONT size 14 color "#7fd06a"
                            text "cook   all placeholder gates → auto-open" font ACT_FONT size 14 color "#7fd06a"
                            text "fit    all placeholder gates → auto-open" font ACT_FONT size 14 color "#7fd06a"
                            text "mech   all placeholder gates → auto-open" font ACT_FONT size 14 color "#7fd06a"
                            text "art    all placeholder gates → auto-open" font ACT_FONT size 14 color "#7fd06a"

                    null height 4

                    # ── COURSES TABLE ─────────────────────────────────────────
                    text "COURSES  (one-time per ID, checked against completed_courses)" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "Tier       Cost   Hours  XP    Min-skill  Max-skill  (same for all 8 skills)" font ACT_FONT size 14 color "#8fb0d0"
                            text "intro       $60     3h    30      0          3" font ACT_FONT size 14 color "#cfe0f5"
                            text "inter      $120     3h    50      2          5" font ACT_FONT size 14 color "#cfe0f5"
                            text "adv        $220     4h    80      4          7" font ACT_FONT size 14 color "#cfe0f5"
                            text "master     $400     5h   110      6          9" font ACT_FONT size 14 color "#cfe0f5"
                            text "─────────────────────────────────────────────────────────────────────" font ACT_FONT size 14 color "#3a4a6a"
                            text "Total/skill: $800  15h  270 XP  (all 4 tiers)" font ACT_FONT size 14 color "#ffd66a"
                            text "Total all 8 skills: $6400  120h  2160 XP" font ACT_FONT size 14 color "#ffd66a"
                            text "Sale event (college_sale): all costs × 0.7" font ACT_FONT size 14 color "#8fb0d0"
                            text "270 XP from courses alone is NOT enough to reach lv10 (needs 2200 XP)" font ACT_FONT size 14 color "#e8a24d"
                            text "Courses cover: lv0→lv2 fully (55 XP) + part of lv2→lv3 for most skills" font ACT_FONT size 14 color "#cfe0f5"

                    null height 4

                    # ── DAILY DIMINISHING RETURNS ─────────────────────────────
                    text "DAILY DIMINISHING RETURNS  (gain_skill_practice only)" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "Hours trained today (cumulative, before session)  →  XP multiplier" font ACT_FONT size 14 color "#8fb0d0"
                            text "0h–2h:   100% of base_xp" font ACT_FONT size 14 color "#7fd06a"
                            text "2h–4h:    70% of base_xp" font ACT_FONT size 14 color "#ffd66a"
                            text "4h–6h:    40% of base_xp" font ACT_FONT size 14 color "#e8a24d"
                            text "6h+:      15% of base_xp  (min 1)" font ACT_FONT size 14 color "#e86060"
                            text "Note: career shifts (do_shift → gain_skill) bypass DR. Courses also bypass DR." font ACT_FONT size 14 color "#8fb0d0"

                    null height 4

                    # ── REPEATABLE SKILL TRAINING ─────────────────────────────
                    text "REPEATABLE SKILL TRAINING ACTIONS" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "Action                       Skill  Base XP  Hours  Energy  Location         DR?" font ACT_FONT size 14 color "#8fb0d0"
                            text "Home computer practice        prog   5 (7*)    3h     -15    Home/computer    YES" font ACT_FONT size 14 color "#cfe0f5"
                            text "Library self-study (prog)     prog   2 (3*)    2h     -18    Library          YES" font ACT_FONT size 14 color "#cfe0f5"
                            text "Home guitar practice 1st      music  5         2h      —     Home             YES" font ACT_FONT size 14 color "#cfe0f5"
                            text "Home guitar practice 2nd      music  2         2h      —     Home             YES" font ACT_FONT size 14 color "#cfe0f5"
                            text "Library self-study (med)      med    2         2h     -18    Library          YES" font ACT_FONT size 14 color "#cfe0f5"
                            text "Library self-study (biz)      biz    2         2h     -18    Library          YES" font ACT_FONT size 14 color "#cfe0f5"
                            text "Library self-study (art)      art    2         2h     -18    Library          YES" font ACT_FONT size 14 color "#cfe0f5"
                            text "Freelance work (per hour)     prog   2         1h     -5     Home/computer    NO" font ACT_FONT size 14 color "#cfe0f5"
                            text "Cook bolognese (lv2 req)      cook   2         0.5h   —      Home             NO" font ACT_FONT size 14 color "#cfe0f5"
                            text "Cook stir-fry (lv4 req)       cook   2         0.75h  —      Home             NO" font ACT_FONT size 14 color "#cfe0f5"
                            text "Cook Sunday roast (lv7 req)   cook   3         1h     —      Home             NO" font ACT_FONT size 14 color "#cfe0f5"
                            text "IT shift (prog chance 55%)    prog   5         8h     —      Hub              NO" font ACT_FONT size 14 color "#cfe0f5"
                            text "Hospital shift (med 45%)      med    5         8h     —      Hospital         NO" font ACT_FONT size 14 color "#cfe0f5"
                            text "Corporate shift (biz 50%)     biz    5         8h     —      Office           NO" font ACT_FONT size 14 color "#cfe0f5"
                            text "Trainer shift (fit 45%)       fit    5         8h     —      Gym              NO" font ACT_FONT size 14 color "#cfe0f5"
                            text "Culinary shift (cook 50%)     cook   5         8h     —      Kitchen          NO" font ACT_FONT size 14 color "#cfe0f5"
                            text "* = with own_programming_kit ($100 purchase)" font ACT_FONT size 13 color "#7a8aa0"

                    null height 4

                    # ── SHIFT PAY TABLE ───────────────────────────────────────
                    text "CAREER SHIFT PAY  (per shift via do_shift — all 8h except IT at prog≥5→6h)" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "Career         R0         R1         R2         R3         R4" font ACT_FONT size 14 color "#8fb0d0"
                            text "Hospital       $80        $140       $240       $350       $480" font ACT_FONT size 14 color "#cfe0f5"
                            text "IT             $100       $155       $230       $310       $400" font ACT_FONT size 14 color "#cfe0f5"
                            text "Corporate      $85        $145       $220       $310       $430" font ACT_FONT size 14 color "#cfe0f5"
                            text "Trainer        $65        $115       $190       —          —" font ACT_FONT size 14 color "#cfe0f5"
                            text "Culinary       $85        $135       $220       $340       —" font ACT_FONT size 14 color "#cfe0f5"
                            text "─────────────────────────────────────────────────────────────────────" font ACT_FONT size 14 color "#3a4a6a"
                            text "Non-career shifts:" font ACT_FONT size 14 color "#8fb0d0"
                            text "Warehouse      $115/8h weekday  |  $170/8h Sunday  (req STR≥25)" font ACT_FONT size 14 color "#cfe0f5"
                            text "Café barista   $55 (shifts 1-4) / $60 (5-14) / $65 (15+) per 4h shift" font ACT_FONT size 14 color "#cfe0f5"
                            text "$/h: Eng.Manager $50/h — Hospital Chief $60/h — Warehouse Sunday $21.25/h" font ACT_FONT size 14 color "#ffd66a"

                    null height 4

                    # ── PROMOTION REQUIREMENTS ────────────────────────────────
                    text "CAREER PROMOTION REQUIREMENTS  (_RANK_SHIFT_REQ = [3, 6, 10, 15, 20])" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "HOSPITAL:" font ACT_FONT size 14 color "#8fb0d0"
                            text "  R0→R1 (Resident):    skill_med≥5, INT≥45, med_bach,  min 3 rank-shifts" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R1→R2 (Doctor):      skill_med≥7, INT≥58, med_mast,  min 6 rank-shifts" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R2→R3 (Attending):   skill_med≥8, INT≥68, CHR≥45,   min 10 rank-shifts" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R3→R4 (Chief):       skill_med≥9, INT≥78, CHR≥60,   min 15 rank-shifts" font ACT_FONT size 14 color "#cfe0f5"
                            text "IT:" font ACT_FONT size 14 color "#8fb0d0"
                            text "  R0→R1 (Mid Dev):     skill_prog≥3, INT≥40,                        min 3" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R1→R2 (Senior Dev):  skill_prog≥5, INT≥55, CHR≥25, prog_bach,     min 6  [trial]" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R2→R3 (Team Lead):   skill_prog≥7, INT≥65, CHR≥40, prog_mast,     min 10" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R3→R4 (Eng.Manager): skill_prog≥8, INT≥75, CHR≥55,               min 15" font ACT_FONT size 14 color "#cfe0f5"
                            text "  WARNING: prog gates blocked — R1+ promotions (prog≥3 req) unreachable without gate fix." font ACT_FONT size 14 color "#ff6666"
                            text "CORPORATE:" font ACT_FONT size 14 color "#8fb0d0"
                            text "  R0→R1 (Associate):  skill_biz≥3, INT≥35, CHR≥35,              min 3  [trial]" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R1→R2 (Analyst):    skill_biz≥5, INT≥50, CHR≥45, biz_bach,    min 6" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R2→R3 (Manager):    skill_biz≥7, INT≥55, CHR≥60, biz_mast,    min 10" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R3→R4 (Director):   skill_biz≥9, INT≥60, CHR≥75,             min 15" font ACT_FONT size 14 color "#cfe0f5"
                            text "TRAINER:" font ACT_FONT size 14 color "#8fb0d0"
                            text "  R0→R1 (Trainer):      skill_fit≥4, STR≥45, APP≥40,  min 3" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R1→R2 (Head Trainer):  skill_fit≥7, STR≥60, CHR≥45, min 6" font ACT_FONT size 14 color "#cfe0f5"
                            text "CULINARY:" font ACT_FONT size 14 color "#8fb0d0"
                            text "  R0→R1 (Line Cook):   skill_cook≥3, STR≥35,            min 3" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R1→R2 (Sous Chef):   skill_cook≥6, STR≥45, CHR≥30,   min 6" font ACT_FONT size 14 color "#cfe0f5"
                            text "  R2→R3 (Head Chef):   skill_cook≥9, STR≥55, CHR≥45,   min 10" font ACT_FONT size 14 color "#cfe0f5"

                    null height 4

                    # ── GIG POOL ──────────────────────────────────────────────
                    text "GIG POOL  (40%/day chance of one new post; each gig one-shot when worked)" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "ID           Title              Pay   Hours  Energy  Req             Window      Post-days" font ACT_FONT size 14 color "#8fb0d0"
                            text "lifeguard    Beach Lifeguard    $95    6h    -30     STR≥30          09-17       1 day" font ACT_FONT size 14 color "#cfe0f5"
                            text "guitar       Fill-in Bar Gig    $70    3h    -12     music≥2         20-03       1 day" font ACT_FONT size 14 color "#cfe0f5"
                            text "catering     Catering Shift     $80    4h    -22     cook≥2          15-22       2 days" font ACT_FONT size 14 color "#cfe0f5"
                            text "promo        Promo/Modelling    $110   3h    -14     APP≥45          10-18       3 days" font ACT_FONT size 14 color "#cfe0f5"
                            text "moving       Moving Day Help    $55    3h    -25     STR≥20          09-18       2 days" font ACT_FONT size 14 color "#cfe0f5"
                            text "$/h: promo $36.7 — lifeguard $15.8 — guitar $23.3 — catering $20 — moving $18.3" font ACT_FONT size 14 color "#ffd66a"

                    null height 4

                    # ── FREELANCE TEMPLATES ───────────────────────────────────
                    text "FREELANCE TEMPLATES  (prog skill required; up to 3 daily offers)" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "ID              Title                         MinSk  MinRep  Hours  Days  Pay    Exp" font ACT_FONT size 14 color "#8fb0d0"
                            text "css_fix_01      Fix CSS layout bug            1      0       2h     3d    $90    5" font ACT_FONT size 14 color "#cfe0f5"
                            text "html_page_01    Simple landing page           1      0       3h     4d    $120   6" font ACT_FONT size 14 color "#cfe0f5"
                            text "form_fix_01     Form validation bug           2      0       3h     3d    $140   7" font ACT_FONT size 14 color "#cfe0f5"
                            text "api_docs_01     Write API docs                2      2       2h     4d    $110   6" font ACT_FONT size 14 color "#cfe0f5"
                            text "script_01       Automation script             3      3       4h     4d    $190   10" font ACT_FONT size 14 color "#cfe0f5"
                            text "wp_plugin_01    WordPress plugin tweak        3      3       4h     5d    $220   12" font ACT_FONT size 14 color "#cfe0f5"
                            text "rest_api_01     Build REST endpoint           4      5       5h     5d    $280   14" font ACT_FONT size 14 color "#cfe0f5"
                            text "db_opt_01       DB query optimisation         4      5       4h     4d    $260   12" font ACT_FONT size 14 color "#cfe0f5"
                            text "spa_01          Single-page app component     5      8       6h     6d    $360   18" font ACT_FONT size 14 color "#cfe0f5"
                            text "auth_01         OAuth integration             5      8       5h     5d    $320   16" font ACT_FONT size 14 color "#cfe0f5"
                            text "mobile_01       Mobile app screen             6      10      7h     6d    $440   20" font ACT_FONT size 14 color "#cfe0f5"
                            text "data_pipe_01    Data pipeline                 6      10      6h     5d    $400   18" font ACT_FONT size 14 color "#cfe0f5"
                            text "arch_01         Architecture refactor         7      14      8h     7d    $580   25" font ACT_FONT size 14 color "#cfe0f5"
                            text "perf_01         Performance audit and fix     8      16      8h     6d    $700   28" font ACT_FONT size 14 color "#cfe0f5"
                            text "ml_api_01       ML API integration            9      18      10h    7d    $950   35" font ACT_FONT size 14 color "#cfe0f5"
                            text "fullstack_01    Full-stack feature            10     20      12h    8d    $1200  45" font ACT_FONT size 14 color "#cfe0f5"
                            text "Note: freelance_work() gives +2 prog XP per hour worked (gain_skill, no DR)" font ACT_FONT size 14 color "#8fb0d0"
                            text "WARNING: prog gate lv3 blocks reaching prog≥3 so most freelance templates are inaccessible." font ACT_FONT size 14 color "#ff6666"

                    null height 4

                    # ── BALANCE PATHS ─────────────────────────────────────────
                    text "EXAMPLE PATHS (deterministic math)" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "PATH A — First 7 days, survival focus:" font ACT_FONT size 14 color "#ffd66a"
                            text "  Café shifts: 5×$55 + 2×$60 = $275 + $120 = $395 income" font ACT_FONT size 14 color "#cfe0f5"
                            text "  Food costs: ~$28 (est. $4/day)" font ACT_FONT size 14 color "#cfe0f5"
                            text "  Balance at rent: $500 + $395 – $28 = $867" font ACT_FONT size 14 color "#cfe0f5"
                            text "  After rent ($220): $647 remaining.  SURVIVES easily." font ACT_FONT size 14 color "#7fd06a"
                            text "" font ACT_FONT size 14 color "#cfe0f5"
                            text "PATH B — Rush Programming to level 5:" font ACT_FONT size 14 color "#ffd66a"
                            text "  XP needed: 320 total" font ACT_FONT size 14 color "#cfe0f5"
                            text "  Courses (prog_intro 30XP $60 + prog_inter 50XP $120) = 80 XP, $180 cost" font ACT_FONT size 14 color "#cfe0f5"
                            text "  Remaining needed: 240 XP via practice (6 XP/day no kit, 9 XP/day with kit)" font ACT_FONT size 14 color "#cfe0f5"
                            text "  BLOCKED: gate at lv3 requires complete_skill_gate(prog,3,...) — never called." font ACT_FONT size 14 color "#ff6666"
                            text "  Without gate fix: prog is permanently capped at lv2." font ACT_FONT size 14 color "#ff6666"
                            text "" font ACT_FONT size 14 color "#cfe0f5"
                            text "PATH C — Rush Guitar/Music to level 5:" font ACT_FONT size 14 color "#ffd66a"
                            text "  Requires: own_guitar ($150), then home practice" font ACT_FONT size 14 color "#cfe0f5"
                            text "  XP needed: 320 total.  Per day (2 sessions): 5+2 = 7 XP/day" font ACT_FONT size 14 color "#cfe0f5"
                            text "  BLOCKED: gate at lv3 requires busk_complete — park busking not implemented." font ACT_FONT size 14 color "#ff6666"
                            text "  Without gate fix: music is permanently capped at lv2." font ACT_FONT size 14 color "#ff6666"
                            text "" font ACT_FONT size 14 color "#cfe0f5"
                            text "PATH D — Rich player ($10,000), buy all courses:" font ACT_FONT size 14 color "#ffd66a"
                            text "  All 32 courses cost $6400 total (8 skills × $800)" font ACT_FONT size 14 color "#cfe0f5"
                            text "  All 32 courses give 270 XP per skill" font ACT_FONT size 14 color "#cfe0f5"
                            text "  After all courses: med/biz/cook/fit/mech/art → XP=270 of 2200 needed = lv4 (195 XP gates lv0→4, 270 > 195 so reach lv4, 75 banked toward lv5)" font ACT_FONT size 14 color "#cfe0f5"
                            text "  prog/music → CAPPED at lv2 (gate at lv3 permanently blocks)" font ACT_FONT size 14 color "#ff6666"
                            text "  NO skill reaches lv10 through courses alone (270 XP of 2200 needed = 12.3%)" font ACT_FONT size 14 color "#cfe0f5"
                            text "  Remaining funds after all courses: $10,000 – $6,400 = $3,600" font ACT_FONT size 14 color "#cfe0f5"

                    null height 4

                    # ── RISKS ─────────────────────────────────────────────────
                    text "IDENTIFIED RISKS" font PROFILE_FONT size 17 color "#5bcafa"
                    frame:
                        xfill True background "#1a2030" padding (12, 8, 12, 8)
                        vbox:
                            spacing 3
                            text "[FIXED 63B] Prog gates wired + 9/10 deadlock resolved. Music gates are non-blocking." font ACT_FONT size 14 color "#ff6666"
                            text "[RISK] Promo gig: $110/3h = $36.7/h — highest $/h in the game at low skill (req APP≥45 easily met via cosmetics)." font ACT_FONT size 14 color "#e8a24d"
                            text "[RISK] Sunday warehouse: $170/8h = $21.25/h — STR passive gains from shifts can quietly unlock this." font ACT_FONT size 14 color "#e8a24d"
                            text "[RISK] Top-tier freelance (fullstack_01 $1200/12h = $100/h) is blocked by prog gate — if gate ever gets fixed, income snowballs fast." font ACT_FONT size 14 color "#e8a24d"
                            text "[RISK] Hospital overtime event ($60/4h, no gate) is a bonus income path via work events." font ACT_FONT size 14 color "#cfe0f5"
                            text "[INFO] No softlock: tier-1 rent $220/week requires only 4 café shifts ($220 / $55 = 4 shifts, 16h)." font ACT_FONT size 14 color "#7fd06a"
                            text "[INFO] Career DR (double skill chance at perf≥100) can accelerate med/biz/cook/fit skills significantly." font ACT_FONT size 14 color "#cfe0f5"
                            text "[INFO] IT shift reduces to 6h at prog≥5 — improves pay rate from $12.5/h to $16.7/h at Junior Dev." font ACT_FONT size 14 color "#cfe0f5"
                            text "[INFO] No busking/open_mic activity implemented — music skill has no working gate progression path." font ACT_FONT size 14 color "#e8a24d"
