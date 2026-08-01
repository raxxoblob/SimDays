# Image declarations
# Ren'Py looks for images relative to the game/ folder.
# game/images is a directory junction -> ../../images (the shared asset folder).

# ── Backgrounds ───────────────────────────────────────────────────────
# All location backgrounds are 16:9 (1672x941 or 1920x1080). We wrap each in
# a Transform that forces 1920x1080 (the game resolution) so they fill the
# screen with no borders. Same ratio -> no distortion.
init python:
    def _bg(name, filename=None):
        path = "images/locations/%s.webp" % (filename or name)
        renpy.image(name, Transform(path, size=(1920, 1080)))

    for _n in [
        "cheaphouse_day", "cheaphouse_night",
        "goodhomeday", "goodhomenight", "richhomeday", "richhomenight",
        "cafeday", "cafenight", "bar", "restaurantday", "restaurantnight",
        "gymdaypeople", "gymdaynopeople",
        "libraryday", "librarynight",
        "mallday", "mallnight", "clothesshop", "electronicsshop", "giftshop",
        "parkday", "parknight", "beachday", "beachnight",
        "goodoffice1", "mediumoffice1", "pooroffice1", "officelobby1",
        "warehouse", "carworkshop", "hospital1", "schoolhall",
        "centerstreet_day", "centerstreet_night",
    ]:
        _bg(_n)

    _bg("classroom", "class")   # 'class' is a Python keyword - rename the image
    # apartment stairwell (doors 12 = you, 14 = Marcus) + Marcus's place - all PNGs.
    renpy.image("hallway",           Transform("images/locations/hallway.png",           size=(1920, 1080)))
    renpy.image("marcus_home_day",   Transform("images/locations/marcus_home_day.png",   size=(1920, 1080)))
    renpy.image("marcus_home_night", Transform("images/locations/marcus_home_night.png", size=(1920, 1080)))
    # New career venues + nightlife/hi-status (per to_generate/locations.md).
    for _pn in ["hub_day", "hub_night", "college_day", "hospital_exam", "hospital_night",
                "bank_day", "bank_night", "nightclub", "bar_rooftop_night", "vip_lounge_airport",
                "cardealer_day", "basketball_court_day"]:
        renpy.image(_pn, Transform("images/locations/%s.png" % _pn, size=(1920, 1080)))
    # kitchen has no windows -> one image for day and night
    renpy.image("kitchen", Transform("images/locations/kitchen_dayandnight.png", size=(1920, 1080)))
    # POV "on the job" full-screen frames (shown during a shift / activity)
    renpy.image("pov_barista",      Transform("images/locations/pov_barista.png",             size=(1920, 1080)))
    renpy.image("hub_pov",          Transform("images/locations/hub_pov.png",                 size=(1920, 1080)))
    renpy.image("pov_warehouse",    Transform("images/locations/warehouse_pov.png",            size=(1920, 1080)))
    renpy.image("pov_doctor",       Transform("images/locations/doctor_pov.png",               size=(1920, 1080)))
    renpy.image("pov_chef",         Transform("images/locations/kitchen_pov.png",              size=(1920, 1080)))
    renpy.image("pov_trainer",      Transform("images/locations/pov_gym_work_trainer.png",     size=(1920, 1080)))
    renpy.image("pov_gym_weights",  Transform("images/locations/pov_gym_weights.png",          size=(1920, 1080)))
    renpy.image("gym_cardio",       Transform("images/locations/gym_cardio.png",               size=(1920, 1080)))

    # Nadbrzeze zone + new venues + activity CG backgrounds
    for _pn2 in ["cheap_home_sleep", "cheap_home_cook", "cheap_home_shower",
                 "casino_night", "lombard_day",
                 "sandbeach_day", "sandbeach_night",
                 "sandbeach_swim_day", "sandbeach_sunbath_day",
                 "gym_reception",
                 "college_study",
                 "park_readbook_day", "park_readbook_night",
                 "park_jog_day", "park_jog_night",
                 "library_study_day", "library_study_night"]:
        renpy.image(_pn2, Transform("images/locations/%s.png" % _pn2, size=(1920, 1080)))
    renpy.image("nadbrzeze_day",   Transform("images/locations/quayside_day.png",   size=(1920, 1080)))
    renpy.image("nadbrzeze_night", Transform("images/locations/quayside_night.png", size=(1920, 1080)))
    renpy.image("diner_night",     Transform("images/locations/diner_night.png",     size=(1920, 1080)))

    # hospital rooftop (Lena scene bg)
    renpy.image("hospital_rooftop_night", Transform("images/locations/hospital_rooftop_night.png", size=(1920, 1080)))

    # Nexus Tower extras
    renpy.image("nexus_meeting_room", Transform("images/locations/nexus_meeting_room.png",  size=(1920, 1080)))
    renpy.image("nexus_office_night", Transform("images/locations/nexus_office_night.png",  size=(1920, 1080)))
    renpy.image("nexus_cafeteria_day", Transform("images/scenes/career_nexus/nexus_cafeteria_day.png", size=(1920, 1080)))

    # hospital break room (career arc bg)
    renpy.image("hospital_break_room", Transform("images/locations/hospital_break_room.png", size=(1920, 1080)))

    # Hospital arc CGs (scenes/career_hospital/)
    for _hn, _hf in [
        ("cg_hosp_first_day", "hosp_first_day_ward_walk"),
        ("cg_hosp_task_1",    "hosp_task_1_intake_desk"),
        ("cg_hosp_npc1",      "hosp_npc1_rounds_lena"),
        ("cg_hosp_npc2",      "hosp_npc2_break_room"),
    ]:
        renpy.image(_hn, Transform("images/scenes/career_hospital/%s.png" % _hf, size=(1920, 1080)))

    # Corporate arc CGs (scenes/career_nexus/)
    for _cn, _cf in [
        ("cg_corp_first_day",       "corporate_caroline_over_desk"),
        ("cg_corp_task_arrive",     "corporate_archive_arrival"),
        ("cg_corp_task_files",      "corporate_archive_files"),
        ("cg_corp_task_convo",      "corporate_archive_worker_conversation"),
        ("cg_corp_review_report",   "corporate_caroline_marked_report"),
        ("cg_corp_review_approval", "corporate_caroline_small_approval"),
        ("cg_corp_client_call",     "corporate_client_call_meeting_room"),
        ("cg_corp_client_handoff",  "corporate_client_call_martha_handoff"),
        ("cg_corp_client_after",    "corporate_client_call_after"),
        ("cg_corp_credit_lobby",    "corporate_credit_lobby_encounter"),
        ("cg_corp_credit_martha",   "corporate_credit_martha_close"),
        ("cg_corp_lunch_wide",      "corporate_lunch_table_wide"),
        ("cg_corp_lunch_martha",    "corporate_lunch_martha_reaction"),
        ("cg_corp_overtime_empty",  "corporate_overtime_empty_office"),
        ("cg_corp_overtime_coffee", "corporate_overtime_coffee"),
        ("cg_corp_overtime_martha", "corporate_overtime_martha_seen"),
        ("cg_corp_martha1_desk",    "corporate_missing_number_martha_desk"),
        ("cg_corp_close_screen",    "corporate_missing_number_close_screen"),
    ]:
        renpy.image(_cn, Transform("images/scenes/career_nexus/%s.png" % _cf, size=(1920, 1080)))

    # Culinary crisis CGs (scenes/rena_crisis/) — all 1672x941, scaled to 1920x1080.
    # cg_cul_crisis_problem: declared but not placed in the sequence —
    # visually too similar to pressure; reserved as fallback or montage asset.
    for _rn in [
        # Common sequence
        "cg_cul_crisis_rush", "cg_cul_crisis_pressure", "cg_cul_crisis_problem",
        "cg_cul_crisis_sauce_closeup", "cg_cul_crisis_table_waiting",
        "cg_cul_crisis_rena_notices",
        # Branch A — tell Rena
        "cg_cul_crisis_admit", "cg_cul_crisis_guided_recovery",
        "cg_cul_crisis_clean_send",
        # Branch B — solo attempt
        "cg_cul_crisis_solo_attempt", "cg_cul_crisis_solo_success",
        "cg_cul_crisis_solo_failure",
        # Branch C — stop the dishes
        "cg_cul_crisis_stop_pass", "cg_cul_crisis_resequence",
        "cg_cul_crisis_delayed_send",
        # Branch D — send anyway
        "cg_cul_crisis_send_anyway", "cg_cul_crisis_dining_consequence",
        "cg_cul_crisis_returned_plate",
        # Ending
        "cg_cul_crisis_last_ticket",
        "cg_cul_crisis_after_good", "cg_cul_crisis_after_mixed",
        "cg_cul_crisis_after_bad",
    ]:
        renpy.image(_rn, Transform("images/scenes/rena_crisis/%s.png" % _rn, size=(1920, 1080)))

    # Trainer arc CGs (scenes/career_gym/)
    for _tn, _tf in [
        ("cg_tr_first_day", "tr_first_day_shadow"),
        ("cg_tr_task_1",    "tr_task_1_solo_session"),
        ("cg_tr_npc1",      "tr_npc1_planning_session"),
        ("cg_tr_npc2",      "tr_npc2_after_last_session"),
    ]:
        renpy.image(_tn, Transform("images/scenes/career_gym/%s.png" % _tf, size=(1920, 1080)))

    # Nora rent sequence (scenes/nora_rent/) — branching 4a/4b and 5a/5b
    for _nrf in ["nora_rent_1","nora_rent_2","nora_rent_3",
                 "nora_rent_4a","nora_rent_4b","nora_rent_5a","nora_rent_5b"]:
        renpy.image(_nrf, Transform("images/scenes/nora_rent/%s.png" % _nrf, size=(1920, 1080)))

    # Sam gym sequence (scenes/sam_gym/) — branching 5a/5b and 6a
    for _sgf in ["sam_gym_1","sam_gym_2","sam_gym_3","sam_gym_4",
                 "sam_gym_5a","sam_gym_5b","sam_gym_6a"]:
        renpy.image(_sgf, Transform("images/scenes/sam_gym/%s.png" % _sgf, size=(1920, 1080)))

    # Zoe beach night sequence (scenes/zoe_beach_night/) — branching 2a/2b
    for _zbnf in ["zoe_beach_night_1","zoe_beach_night_2a","zoe_beach_night_2b","zoe_beach_night_3"]:
        renpy.image(_zbnf, Transform("images/scenes/zoe_beach_night/%s.png" % _zbnf, size=(1920, 1080)))

    # eli_find sequence + martha_rooftop sequence
    for _i in range(1, 6):
        renpy.image("eli_find_%d" % _i,
            Transform("images/scenes/eli_find/eli_find_%d.png" % _i, size=(1920, 1080)))
    renpy.image("eli_find_ring_bonus",
        Transform("images/scenes/eli_find/eli_find_ring_bonus.png", size=(1920, 1080)))
    for _i in range(1, 7):
        renpy.image("martha_rooftop_%d" % _i,
            Transform("images/scenes/martha_rooftop/martha_rooftop_%d.png" % _i, size=(1920, 1080)))

    # IT arc CGs (scenes/career_hub/)
    for _in, _if in [
        ("cg_it_first_day", "it_first_day_eli_intro"),
        ("cg_it_task_1",    "it_task_1_bug_terminal"),
        ("cg_it_npc1",      "it_npc1_pr_comments"),
        ("cg_it_npc2",      "it_npc2_late_deploy"),
    ]:
        renpy.image(_in, Transform("images/scenes/career_hub/%s.png" % _if, size=(1920, 1080)))

    # Elle pier CGs (scenes/elle_pier/)
    for _i in range(1, 7):
        renpy.image("elle_pier_%d" % _i,
            Transform("images/scenes/elle_pier/elle_pier_%d.png" % _i, size=(1920, 1080)))

    # Lena rooftop CGs (scenes/lena_rooftop/)
    for _i in range(1, 6):
        renpy.image("lena_rooftop_%d" % _i,
            Transform("images/scenes/lena_rooftop/lena_rooftop_%d.png" % _i, size=(1920, 1080)))

    # Zoe beach meeting CGs (7-frame sequence, scenes/zoe_beach/)
    for _i in range(1, 8):
        renpy.image("zoe_beach_%d" % _i,
            Transform("images/scenes/zoe_beach/zoe_beach_%d.png" % _i, size=(1920, 1080)))

    # Nora closing-time CGs (scenes/nora_closing/)
    for _i in range(1, 8):
        renpy.image("nora_closing_%d" % _i,
            Transform("images/scenes/nora_closing/cg_nora_closing%d.png" % _i, size=(1920, 1080)))

    # Marcus "Shoot hoops" court CGs (scenes/marcus_court/)
    for _nm, _fn in [
        ("cg_court_trash_talk",  "cg_marcus_court_trash_talk"),
        ("cg_court_jump_shot",   "cg_marcus_court_jump_shot"),
        ("cg_court_bench",       "cg_marcus_court_bench_after_game"),
        ("cg_court_hoop",        "cg_marcus_court_ball_in_hoop"),
        ("cg_court_hoop_insert", "cg_court_success_hoop_insert"),
        ("cg_court_miss",        "cg_player_court_shot_miss"),
        ("cg_court_success",     "cg_player_court_shot_success"),
    ]:
        renpy.image(_nm, Transform("images/scenes/marcus_court/%s.png" % _fn, size=(1920, 1080)))

    # Home-visit scene CGs — per-apartment-tier variants (apartment_tier 1/2/3)
    for _hn, _hpath in [
        # eli_dinner
        ("cg_eli_home_dinner_cheap",  "home/eli_dinner/cg_eli_home_dinner_cheap.png"),
        ("cg_eli_home_dinner_good",   "home/eli_dinner/cg_eli_home_dinner_good.png"),
        ("cg_eli_home_dinner_rich",   "home/eli_dinner/cg_eli_home_dinner_rich.png"),
        # eli_side_project
        ("cg_eli_side_project_cheap", "home/eli_side_project/cheaphome_eli_side_project_desk.png"),
        ("cg_eli_side_project_good",  "home/eli_side_project/goodhome_eli_side_project_desk.png"),
        ("cg_eli_side_project_rich",  "home/eli_side_project/richhome_eli_side_project_desk.png"),
        # nora_coffee
        ("cg_nora_coffee_cheap",      "home/nora_coffee/cheaphome_nora_coffee_machine.png"),
        ("cg_nora_coffee_good",       "home/nora_coffee/goodhome_nora_coffee_machine.png"),
        ("cg_nora_coffee_rich",       "home/nora_coffee/richhome_nora_coffee_machine.png"),
        # zoe_guitar
        ("cg_zoe_guitar_cheap",       "home/zoe_guitar/cheaphome_zoe_guitar_session.png"),
        ("cg_zoe_guitar_good",        "home/zoe_guitar/goodhome_zoe_guitar_session.png"),
        ("cg_zoe_guitar_rich",        "home/zoe_guitar/richhome_zoe_guitar_session.png"),
        # nora_cooking (cheap-home only — no other tiers were generated)
        ("cg_nora_cooking_cheap",     "home/nora_cooking/cheaphome_nora_cook.png"),
    ]:
        renpy.image(_hn, Transform("images/scenes/%s" % _hpath, size=(1920, 1080)))

    # Intro cinematic frames (pre-rendered POV, full-screen). 1672x941 -> 1920x1080.
    for _i, _f in enumerate(["intro_scene_1", "intro_scene2", "intro_scene3",
                             "intro_scene4", "intro_scene5", "intro_scene6", "intro_scene7"], 1):
        renpy.image("intro%d" % _i, Transform("images/scenes/intro_scene/%s.png" % _f, size=(1920, 1080)))

    # Map: resized to 1920x1080 (was 5068x2764, ~56MB VRAM). 0.78MB on disk.
    _bg("map_city")

    # Map district zones: idle = dim icon, hover = bright icon + highlight + name
    for _z in ["bogate_domki", "warehouse", "park", "domki", "bloki", "centrum", "szpital", "mall", "plaza", "nadbrzeze"]:
        renpy.image("z_%s_idle" % _z, "images/ui/z_%s_idle.png" % _z)
        renpy.image("z_%s_hi" % _z, "images/ui/z_%s_hi.png" % _z)

# ── Sprite positioning transforms ─────────────────────────────────────
# Sprites are tall portraits (~1086x1448 / 1024x1535). 'fit contain' scales
# each into a box preserving aspect; yalign 1.0 anchors feet to the bottom.
# yoffset 96 pushes the head clear of the topbar HUD (crops a little at the
# shoes, which is fine for standing full-body sprites).
transform sprite_c:
    fit "contain"
    xysize (660, 900)
    xalign 0.5
    yalign 1.0
    yoffset 96

# Feet-anchored (bottom-centre) sprite placement so everyone rises from the bottom
# edge — a thigh-cropped sprite's crop sits at the bottom (legs off-screen), never
# floating mid-screen. sc is only the light male size nudge now (see
# sprite_display_scale in interact.rpy); with sc=1.0 this equals sprite_c.
# xp = screen x of the standing spot (xalign * 1920).
transform sprite_crop(sc, xp=960):
    fit "contain"
    xysize (660, 900)
    transform_anchor True
    xanchor 0.5 yanchor 1.0
    xpos xp ypos 1176          # box bottom at 1080 + 96 yoffset (crops shoes, like sprite_c)
    zoom sc

transform sprite_r:
    fit "contain"
    xysize (660, 900)
    xalign 0.82
    yalign 1.0
    yoffset 96

transform sprite_l:
    fit "contain"
    xysize (660, 900)
    xalign 0.18
    yalign 1.0
    yoffset 96

transform sprite_solo:
    fit "contain"
    xysize (660, 900)
    xalign 0.60
    yalign 1.0
    yoffset 96

transform sprite_duo_r:
    fit "contain"
    xysize (660, 900)
    xalign 0.75
    yalign 1.0
    yoffset 96

transform sprite_duo_l:
    fit "contain"
    xysize (660, 900)
    xalign 0.40
    yalign 1.0
    yoffset 96

transform sprite_tri_r:
    fit "contain"
    xysize (680, 930)
    xalign 0.82
    yalign 1.0
    yoffset 96

transform sprite_tri_c:
    fit "contain"
    xysize (680, 930)
    xalign 0.60
    yalign 1.0
    yoffset 96

transform sprite_tri_l:
    fit "contain"
    xysize (680, 930)
    xalign 0.38
    yalign 1.0
    yoffset 96

transform sprite_quad_d:
    fit "contain"
    xysize (600, 820)
    xalign 0.84
    yalign 1.0
    yoffset 96

transform sprite_quad_c:
    fit "contain"
    xysize (600, 820)
    xalign 0.67
    yalign 1.0
    yoffset 96

transform sprite_quad_b:
    fit "contain"
    xysize (600, 820)
    xalign 0.50
    yalign 1.0
    yoffset 96

transform sprite_quad_a:
    fit "contain"
    xysize (600, 820)
    xalign 0.35
    yalign 1.0
    yoffset 96

# ── Sprite micro-animation transforms ────────────────────────────────────
# Compose with a position transform: show sprite at sprite_r, react_bounce
# Each animation starts and ends at the base yoffset (96) or xoffset (0) so
# no permanent offset accumulates across repeated show statements or rollback.
# Only yoffset/xoffset are touched — xalign/yalign/xysize/fit come from
# the position transform (sprite_r/l/c) and are never overridden here.
#
# ponytail: yoffset-based transforms hard-code the base value (96) that
# sprite_r/l/c all share. If that base ever changes, every transform below
# needs updating or the sprite will jump one frame on entry. Upgrade path:
# define a named constant and reference it, or switch to OffsetMatrix.

transform react_bounce:
    # Quick upward pop and settle — cheerful reactions, surprise, emphasis
    yoffset 96
    ease 0.09 yoffset 84
    ease 0.14 yoffset 96

transform react_shake:
    # Small horizontal rattle — irritation, disbelief, awkward refusal
    xoffset 0
    linear 0.06 xoffset 7
    linear 0.06 xoffset -6
    linear 0.07 xoffset 4
    linear 0.07 xoffset 0

transform react_step_back:
    # Brief downward sink and return — surprise, discomfort, boundary rejection
    yoffset 96
    ease 0.10 yoffset 106
    ease 0.16 yoffset 96

transform react_lean_in:
    # Small upward rise and return — warm attention, teasing, romantic tension
    yoffset 96
    ease 0.12 yoffset 87
    ease 0.16 yoffset 96

transform react_nod:
    # Tiny downward dip and return — controlled acknowledgement (Martha, Lena)
    yoffset 96
    ease 0.08 yoffset 103
    ease 0.10 yoffset 96

transform react_sigh:
    # Slow downward settle and return — tiredness, resignation, release
    yoffset 96
    ease 0.16 yoffset 105
    ease 0.22 yoffset 96

# ── Zoe sprites (plain files; positioned via the transforms above) ─────
# Zoe refreshed to neutral/talk/laugh/angry (PNG; old .webp moved to zoe/old_zoe/)
image zoe_street_neutral   = "images/characters/zoe/zoe_street_neutral.png"
image zoe_street_talk      = "images/characters/zoe/zoe_street_talk.png"
image zoe_street_laugh     = "images/characters/zoe/zoe_street_laugh.png"
image zoe_street_angry     = "images/characters/zoe/zoe_street_angry.png"
# legacy aliases — older scenes still `show zoe_street_smile` / reference the punk sprite
image zoe_street_smile     = "images/characters/zoe/zoe_street_laugh.png"
image zoe_punk_smile       = "images/characters/zoe/zoe_street_neutral.png"

# ── Nora sprites ───────────────────────────────────────────────────────
# Work outfit (behind the counter)
image nora_cafe_normal = "images/characters/nora/nora_cafe_normal.png"
image nora_cafe_talk   = "images/characters/nora/nora_cafe_talk.png"
image nora_cafe_laugh  = "images/characters/nora/nora_cafe_laugh.png"
image nora_cafe_sad    = "images/characters/nora/nora_cafe_sad.png"
image nora_cafe_angry  = "images/characters/nora/nora_cafe_angry.png"
# Casual / off-duty (closing time, high-aff visits)
# Tag nora_casual_normal kept (many call sites) but points at the renamed neutral file.
image nora_casual_normal = "images/characters/nora/nora_casual_neutral.png"
image nora_casual_neutral = "images/characters/nora/nora_casual_neutral.png"
image nora_casual_talk   = "images/characters/nora/nora_casual_talk.png"
image nora_casual_laugh  = "images/characters/nora/nora_casual_laugh.png"
image nora_casual_angry  = "images/characters/nora/nora_casual_angry.png"

# ── Caroline (corporate / HR) ──────────────────────────────────────────
image caroline_normal = "images/characters/caroline/caroline_normal.png"
image caroline_talk   = "images/characters/caroline/caroline_talk.png"
image caroline_laugh  = "images/characters/caroline/caroline_laugh.png"
image caroline_angry  = "images/characters/caroline/caroline_angry.png"

# ── Dr. Lena (hospital) ────────────────────────────────────────────────
image drlena_normal = "images/characters/dr_lena/drlena_normal.png"
image drlena_talk   = "images/characters/dr_lena/drlena_talk.png"
image drlena_laugh  = "images/characters/dr_lena/drlena_laugh.png"
image drlena_angry  = "images/characters/dr_lena/drlena_angry.png"

# ── Natalie (warehouse manager) ────────────────────────────────────────
image natalie_normal = "images/characters/natalie/natalie_normal.png"
image natalie_talk   = "images/characters/natalie/natalie_talk.png"
image natalie_laugh  = "images/characters/natalie/natalie_laugh.png"
image natalie_angry  = "images/characters/natalie/natalie_angry.png"

# ── Elle (beach / summer; portraits + full body) ───────────────────────
image elle_normal          = "images/characters/elle/elle_normal.png"
image elle_talk            = "images/characters/elle/elle_talk.png"
image elle_laugh           = "images/characters/elle/elle_laugh.png"
image elle_angry           = "images/characters/elle/elle_angry.png"
image elle_surprised       = "images/characters/elle/elle_surprised.png"
image elle_sundress_normal = "images/characters/elle/elle_sundress_normal.png"

# ── Marcus sprites (transparent PNGs; outfit_expression) - reworked look ──
image marcus_casual_normal  = "images/characters/marcus/marcus_casual_normal.png"
image marcus_casual_talk    = "images/characters/marcus/marcus_casual_talk.png"
image marcus_casual_laugh   = "images/characters/marcus/marcus_casual_laugh.png"
image marcus_casual_worried = "images/characters/marcus/marcus_casual_worried.png"
image marcus_bar_normal     = "images/characters/marcus/marcus_bar_normal.png"
image marcus_bar_talk       = "images/characters/marcus/marcus_bar_talk.png"
image marcus_park_neutral   = "images/characters/marcus/marcus_park_neutral.png"
image marcus_park_talk      = "images/characters/marcus/marcus_park_talk.png"
image marcus_park_laugh     = "images/characters/marcus/marcus_park_laugh.png"
image marcus_park_sad       = "images/characters/marcus/marcus_park_sad.png"

# ── Rena sprites (kitchen; charcoal jacket) ────────────────────────────
# angry = controlled assessing/displeased; happy = restrained approval.
image rena_normal = "images/characters/rena/rena_normal.png"
image rena_talk   = "images/characters/rena/rena_talk.png"
image rena_happy  = "images/characters/rena/rena_happy.png"
image rena_angry  = "images/characters/rena/rena_angry.png"
image rena_sad    = "images/characters/rena/rena_sad.png"

# ── Rena sprites (casual; off-duty) ────────────────────────────────────
image rena_casual_normal = "images/characters/rena/rena_casual_normal.png"
image rena_casual_talk   = "images/characters/rena/rena_casual_talk.png"
image rena_casual_happy  = "images/characters/rena/rena_casual_happy.png"
image rena_casual_angry  = "images/characters/rena/rena_casual_angry.png"
image rena_casual_sad    = "images/characters/rena/rena_casual_sad.png"

# ── Sam (park, world) + Eli (library, world) ───────────────────────────
image sam_normal     = "images/characters/sam/sam_normal.png"
image sam_talk       = "images/characters/sam/sam_talk.png"
image sam_laugh      = "images/characters/sam/sam_laugh.png"
image sam_determined = "images/characters/sam/sam_determined.png"
# Eli refreshed to the neutral/talk/laugh/angry convention (files renamed).
# Tag eli_normal kept (many `show eli_normal` call sites) but points at the new file.
image eli_normal     = "images/characters/eli/eli_neutral.png"
image eli_neutral    = "images/characters/eli/eli_neutral.png"
image eli_talk       = "images/characters/eli/eli_talk.png"
image eli_laugh      = "images/characters/eli/eli_laugh.png"
image eli_angry      = "images/characters/eli/eli_angry.png"

# ── Martha sprites (transparent PNGs) ──────────────────────────────────
image martha_neutral = "images/characters/martha/martha_neutral.png"
image martha_talk    = "images/characters/martha/martha_talk.png"
image martha_smile   = "images/characters/martha/martha_smile.png"
image martha_cold    = "images/characters/martha/martha_cold.png"
image martha_worried = "images/characters/martha/martha_worried.png"
# Martha evening / off-duty dress outfit (rooftop bar, social scenes)
image martha_dress_normal = "images/characters/martha/martha_dress_normal.png"
image martha_dress_talk   = "images/characters/martha/martha_dress_talk.png"
image martha_dress_laugh  = "images/characters/martha/martha_dress_laugh.png"
image martha_dress_angry  = "images/characters/martha/martha_dress_angry.png"

# ── Kai (beach / weekends) ─────────────────────────────────────────────
# Refreshed to neutral/talk/laugh/angry; kai_normal kept as alias (scene call sites).
image kai_normal  = "images/characters/kai/kai_neutral.png"
image kai_neutral = "images/characters/kai/kai_neutral.png"
image kai_talk    = "images/characters/kai/kai_talk.png"
image kai_laugh   = "images/characters/kai/kai_laugh.png"
image kai_angry   = "images/characters/kai/kai_angry.png"
# Kai gym outfit (trainer arc scenes)
image kai_gym_normal = "images/characters/kai/kai_gym_normal.png"

# ── Gameplay expansion scenes ──────────────────────────────────────────────────
image cg_nora_feels_ignored        = "images/scenes/nora_feels_ignored/cg_nora_feels_ignored.png"
image cg_marcus_missed             = "images/scenes/marcus_missed_commitment/cg_marcus_missed.png"
image cg_wardrobe_martha           = "images/scenes/wardrobe_martha/cg_wardrobe_martha.png"
image cg_zoe_guitar                = "images/scenes/guitar_zoe_busking/cg_zoe_guitar.png"
image nexus_coffee_machine         = "images/locations/nexus_coffee_machine.png"
image nora_bad_day_cheap           = "images/scenes/nora_bad_day/nora_bad_day_cheap.png"
image nora_bad_day_good            = "images/scenes/nora_bad_day/nora_bad_day_good.png"
image nora_bad_day_rich            = "images/scenes/nora_bad_day/nora_bad_day_rich.png"
image cg_martha_gesture            = "images/scenes/martha_corridor_gesture/cg_martha_gesture.png"
image cg_nora_hug_school           = "images/scenes/nora_hug_school/cg_nora_hug.png"
image cg_eli_deploy_hug            = "images/scenes/eli_deploy_hug/cg_eli_hug.png"
image cg_eli_hardware              = "images/scenes/programming_kit_eli/cg_eli_hardware.png"
image cg_eli_zoe_collab            = "images/scenes/eli_meets_zoe/cg_eli_zoe.png"
image cg_lena_shoulder             = "images/scenes/lena_shoulder_gesture/cg_lena_shoulder.png"
image cg_nora_kai                  = "images/scenes/nora_kai_crossover/cg_nora_kai.png"
image lena_dinner_good             = "images/scenes/kitchen_lena_extended/lena_dinner_good.png"
image lena_dinner_rich             = "images/scenes/kitchen_lena_extended/lena_dinner_rich.png"
image cg_martha_gift               = "images/scenes/martha_gift_accusation/cg_martha_gift.png"
image car_interior_night           = "images/locations/car_interior_night.png"
image car_marcus_night             = "images/scenes/car_marcus_drive/car_marcus_night.png"
image car_interior_pov             = "images/scenes/car_marcus_drive/car_interior_pov.png"
image cg_zoe_almost                = "images/scenes/zoe_spontaneous/cg_zoe_almost.png"
image hospital_break_room_day      = "images/locations/hospital_break_room_day.png"
image parkday_rain                 = "images/locations/parkday_rain.png"

# ── Interaction CGs (kiss / hug per character) ────────────────────────────────
image cg_nora_kiss      = "images/characters/nora/nora_kiss.png"
image cg_nora_hug       = "images/characters/nora/nora_hug.png"
image cg_caroline_kiss  = "images/characters/caroline/caroline_kiss.png"
image cg_caroline_hug   = "images/characters/caroline/caroline_hug.png"
image cg_lena_kiss      = "images/characters/dr_lena/drlena_kiss.png"
image cg_lena_hug       = "images/characters/dr_lena/drlena_hug.png"
image cg_elle_kiss      = "images/characters/elle/elle_kiss.png"
image cg_elle_hug       = "images/characters/elle/elle_hug.png"
image cg_zoe_kiss       = "images/characters/zoe/zoe_kiss.png"
image cg_zoe_hug        = "images/characters/zoe/zoe_hug.png"
image cg_martha_kiss    = "images/characters/martha/martha_kiss.png"
image cg_martha_hug     = "images/characters/martha/martha_hug.png"
image cg_sam_hug        = "images/characters/sam/sam_hug.png"
image cg_eli_hug        = "images/characters/eli/eli_hug.png"

# ── Content Pack 2 CGs ─────────────────────────────────────────────────────────
init python:
    renpy.image("cg_elle_portugal_turn",
        Transform("images/scenes/elle_portugal_payoff/cg_elle_portugal_turn.png", size=(1920, 1080)))
    renpy.image("cg_sam_marcus_court",
        Transform("images/scenes/sam_marcus_crossover/cg_sam_marcus_court.png", size=(1920, 1080)))
