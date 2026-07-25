# Core game data - stats, needs, time, money

init python:
    DAY_START = 7      # 7 AM
    DAY_END   = 27     # 3 AM next day (27 = 24+3)
    DAY_NAMES = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    def time_label(hour_float):
        h = int(hour_float) % 24
        m = int((hour_float % 1) * 60)
        suffix = "AM" if h < 12 else "PM"
        h12 = h % 12 or 12
        return "%d:%02d %s" % (h12, m, suffix)

    def day_name(day_int):
        return DAY_NAMES[day_int % 7]

default money    = 500
default day      = 0       # days since game start (0 = Day 1, Monday)
default hour     = 8.0     # current hour (float, 7.0-27.0)

# Core stats (0-100)
default stat_str = 10
default stat_int = 10
default stat_chr = 10
default stat_app = 10

# Needs (0-100, decay over time - see spend_time/new_day)
default need_hunger  = 80
default need_hygiene = 80
default need_energy  = 90

# Professional skills (0-10; learned via courses at the college + on the job).
# These GATE careers alongside core stats (e.g. Doctor needs Medicine 5 + INT 50).
default skill_med  = 0   # Medicine   -> hospital careers
default skill_prog = 0   # Programming-> IT / The Hub
default skill_biz  = 0   # Business   -> corporate / management
default skill_cook = 0   # Cooking    -> restaurant / kitchen
default skill_fit  = 0   # Fitness    -> gym / personal trainer
default skill_mech = 0   # Mechanics  -> garage / warehouse
default skill_art  = 0   # Art        -> creative / gallery (Zoe's world)
default skill_music = 0  # Music      -> guitar practice, busking / gigs later
default skill_exp = {}   # key -> exp banked toward the NEXT level (see gain_skill)

default mc_name = "Alex"   # player's name; set during the intro, personalizable
default current_loc = ""  # which location label the player is currently in

# Relationship (affection 0-100, trust 0-100)
default zoe_affection = 0
default zoe_trust     = 0
default nora_affection = 0
default nora_trust     = 0
default marcus_affection = 0
default marcus_trust     = 0
default martha_affection = 0
default martha_trust     = 0
default caroline_affection = 0
default caroline_trust     = 0
default lena_affection     = 0
default lena_trust         = 0
default natalie_affection  = 0
default natalie_trust      = 0
default elle_affection     = 0
default elle_trust         = 0
default sam_affection      = 0
default sam_trust          = 0
default eli_affection      = 0
default eli_trust          = 0
default kai_affection      = 0
default kai_trust          = 0
default rena_affection     = 0
default rena_trust         = 0

# Progression flags
default zoe_met       = False
default nora_met      = False
default marcus_met    = False
default marcus_chili  = False
default martha_met    = False
# Career NPCs - introduced through the career, not by wandering in.
default caroline_met  = False
default lena_met      = False
default natalie_met   = False
default eli_met       = False
default kai_met       = False
default sam_met       = False
default rena_met           = False
default rena_diner_first_done = False
default cafe_shift_done = False   # so the "first shift" line only plays once
default nora_closing_done = False
default elle_pier_done = False
default lena_rooftop_done = False
default warned_today    = False   # low-need heads-up fires at most once a day
default gifts           = {"book": 0, "sweets": 0, "gadget": 0, "flowers": 0}  # gifts by category
default apartment_tier = 1    # 1=cheap, 2=mid, 3=rich

# Stat XP (mirror of skill_exp — higher level = more EXP to next)
default stat_exp        = {}   # key -> EXP banked toward next level
# Supplements consumed before training: protein=+50% EXP, preworkout=+100% EXP (STR)
default supplements     = {"protein": 0, "preworkout": 0}
# Passive STR boost on next gain_stat("str",...) call; auto-resets to 1.0
default stat_boost_str  = 1.0

# Social status assets (0-3 tiers). Status = how the city reads you; gates some
# people and raises how far relationships can go.
default car_tier      = 0
default wardrobe_tier = 0
default jewelry_tier  = 0

# Owned items (Sims-like). Computer comes with the apartment; the rest are bought.
default own_computer       = True   # coding practice, stock trading
default own_guitar         = False  # music practice
default own_bed            = False  # better bed: full rest + a quick Nap option
default own_book           = False  # readable at home for +INT
default own_sketchbook     = False  # sketch at home for +art skill
default own_metal_detector    = False  # beach searching mechanic
default own_programming_kit      = False  # bonus prog EXP per self-study / course
default own_coffee_machine       = False  # unlocks Nora scene + home coffee activity
default own_kitchen_set          = False  # unlocks dinner invite action
default home_coffee_calibrated   = False  # set after Nora's tasting; home coffee gives +energy bonus
default gym_pass_expires      = -1     # game day when gym pass runs out (-1 = no pass)
default cosmetic_boost_until  = -1     # day when cosmetic temp APP boost expires
# stock market state lives in stocks.rpy

# Finance
default loan    = 0     # outstanding debt; blocks all spending until repaid
default savings = 0     # savings account; earns 2%/week interest

# World events (refreshed each new_day)
default daily_events = []   # list of event dicts from DAILY_EVENT_POOL

# Contacts (NPC phone numbers; only added when the player asks)
default npc_contacts = []
default degrees         = []   # earned degree ids: "med_bach", "med_mast", "prog_bach", etc.
default quests_completed = []  # quest ids stamped on first completion — never un-stamps
default npc_anger           = {}   # npc_id -> anger level; decays 1/day
default npc_gift_week       = {}   # npc_id -> (week_index, gifts_this_week)
default work_events_seen    = {}   # cid -> [event ids already fired]
default _career_event_last  = {}   # cid -> shift count when last event fired
default _career_event_gap   = {}   # cid -> current gap until next event
default npc_messages     = []   # list of {npc_id, text, day}
default npc_texted_today = []   # npc_ids player texted today
default player_commitments = []  # list of {id, npc_id, title, day, hour, location, label, completed, missed}

# Relationship memory + threshold tracking
default relationship_memories = {}         # {npc_id: [{id, title, day}]}
default relationship_thresholds_seen = {}  # {"nora_aff_25": True, ...}
default npc_last_date_day = {}             # {npc_id: day_of_last_date/outing}
default npc_date_venue_count = {}          # {"npc|venue": times_visited} — diminishing returns
default npc_last_hug_day = {}              # {npc_id: day_of_last_hug}
default npc_last_kiss_day = {}             # {npc_id: day_of_last_kiss}
default failed_physical_attempts = {}     # {(npc_id, action): consecutive_fail_count}
default _last_hug_accepted = False         # side channel: was the most recent do_hug() accepted?
default physical_boundary_lockout = {}    # {(npc_id, action): day_lockout_expires}
# Romance progression flags — legacy booleans kept for save compatibility; do not set directly
default nora_romance_unlocked     = False
default elle_romance_unlocked     = False
default zoe_romance_unlocked      = False
default caroline_romance_unlocked = False
default lena_romance_unlocked     = False
# Romance state architecture — reversible, player-driven
# Valid states: unopened | friends | interested | dating | committed | paused | closed
default romance_states           = {}  # {npc_id: state}
default romance_momentum         = {}  # {npc_id: 0–100}
default romance_last_choice_day  = {}  # {npc_id: day}
default romance_previous_choice  = {}  # {npc_id: source_string}
default romance_pause_until_day  = {}  # {npc_id: day_pause_expires}
default romance_permanent_closed = {}  # {npc_id: True} — only after explicit confirmation
default romance_route_memories   = {}  # {npc_id: [{from, to, source, day}]}
default nora_reopen_done         = False
default zoe_reopen_done          = False
default martha_reopen_done       = False

# Activity anti-repetition tracking (FIX 8: single bounded structure)
default activity_daily_uses = {}           # {activity_id: {"day": N, "count": K}}

# Career performance threshold notifications
default career_perf_thresholds_seen = {}   # {(job_id, job_rank, threshold): True, ...}

# Stock trading session flag (FIX 2): cleared before opening market, set on first trade
default _stock_session_charged = False

# Actionable invitation tracking
default martha_coffee_accepted   = False
default martha_coffee_day        = -1
default martha_declined_invites  = []
default eli_debug_joined         = False
default eli_debug_day            = -1
default lena_case_accepted       = False
default lena_case_day            = -1
default nora_closing_accepted    = False
default nora_closing_day         = -1
default natalie_extra_shift_day  = -1
default topic_arc_done   = {}   # arc_id -> True when that stage has been played
default shifts_worked    = {}   # career_id -> total shifts completed

# Corporate arc flags
default corporate_style        = None    # "ambitious" / "reliable" / "people_first"
default corp_task_1_done       = False
default corp_martha_1_done     = False
default corp_martha_2_done     = False
default corp_review_intern_done = False
default corp_shifts            = 0      # total corporate shifts worked (gate for arc pacing)
default corp_review_score      = 0     # accumulated from arc choices; feeds review outcome
default corp_net_credit_hallway_done = False

# Project Atlas — Associate arc
default atlas_started          = False
default atlas_completed        = False
default atlas_stage            = 0
default atlas_score            = 0
default atlas_risk             = 0
default atlas_route            = None   # "ambitious" / "reliable" / "people_first"
default atlas_credit_choice    = None   # "shared" / "self" / "modest"
default atlas_martha_involved  = False
default atlas_caroline_warned  = False
default atlas_intro_done       = False
default atlas_research_done    = False
default atlas_problem_done     = False
default atlas_crunch_done      = False
default atlas_presentation_done = False
default atlas_aftermath_done   = False
default atlas_shifts           = 0     # project-work sessions since intro; gates scenes

# Corporate Associate collab flags
default mco_client_call_done    = False
default _corp_promised_client   = False
default _corp_measured_in_call  = False
default _corp_client_reframe    = False
default martha_rooftop_done     = False
default eli_find_done           = False
default nora_rent_done          = False
default sam_gym_done            = False
default zoe_beach_night_done    = False

# ── Gameplay expansion defaults ────────────────────────────────────────────────
default nora_ignored_done         = False
default nora_ignored_pending      = False
default nora_ignored_response     = ""
default nora_bad_day_done         = False
default nora_bad_day_pending      = False
default last_day_worn_out         = False   # was the player worn out at the end of yesterday?
default nora_touched_arm          = False
default marcus_missed_done        = False
default marcus_missed_pending     = None   # None or {trigger_day, commitment_id, title, location, hour, variant}
default marcus_basketball_invite_done    = False
default marcus_basketball_invite_pending = False
default martha_wardrobe_done      = False
default zoe_park_guitar_done               = False
default zoe_rain_done                      = False
default zoe_moment_deflected_done          = False
default zoe_moment_deflected_pending       = False
default zoe_moment_deflected_pending_day   = -1
default martha_corridor_done         = False
default martha_corridor_pending      = False
default martha_corridor_pending_day  = -1
default martha_corridor_context      = None
default nora_hug_school_done         = False
default nora_hug_school_pending      = False
default nora_hug_school_pending_day  = -1
default eli_deploy_hug_done          = False
default eli_deploy_pending           = False
default eli_deploy_pending_day       = -1
default lena_shoulder_done           = False
default lena_shoulder_pending        = False
default lena_shoulder_pending_day    = -1
default nora_kai_crossover_done      = False
default nora_kai_pending             = False
default eli_meets_zoe_done        = False
default car_marcus_drive_done     = False
default martha_gift_accusation_done = False
default martha_gift_scene_pending = None   # None or {trigger_day, gift_id, gift_name, gift_count, trigger_location, variant}
default programming_kit_eli_done  = False
default nora_last_seen_day        = 0
default nora_kai_pending_day      = -1
default nora_kai_retry_after_day  = 0
default kitchen_lena_extended_done = False
default lena_break_room_done      = False
default hospital_hard_case_pending = False
default martha_coffee_machine_done = False
default gift_log                  = []
default major_scene_last_day      = -1

# ── Content Pack 2: relationship scene flags ──────────────────────────
default caroline_bar_done             = False
default caroline_bar_pending          = False
default caroline_bar_pending_day      = -1
# Romance-opening scenes for the three NPCs that previously had no entry point.
default caroline_romance_open_done    = False
default lena_romance_open_done        = False
default elle_romance_open_done        = False
default nora_cooking_state            = "none"  # "none" | "offered" | "pending" | "done"
default nora_cooking_declined_day     = -1      # day of last decline; -1 = never declined
default natalie_bar_scene_done        = False
default natalie_bar_scene_pending     = False
default natalie_bar_scene_pending_day = -1
default kai_cafe_quiet_done           = False
default kai_cafe_quiet_pending        = False
default kai_cafe_quiet_pending_day    = -1
default elle_decision_done            = False
default elle_decision_pending         = False
default elle_travel_2_response        = None
default elle_abroad_day               = -1
default sam_marcus_scene_done         = False
default sam_marcus_scene_pending      = False
default sam_marcus_scene_pending_day  = -1
default eli_dinner_done               = False

# Corporate work activity system
default office_reputation      = 0    # 0-100; built through networking
default martha_last_collab     = -7   # day of last "work with martha" session
default network_week_count     = 0    # networking sessions this week
default network_week_idx       = -1   # day//7 when network_week_count was last reset

# IT arc (Junior Dev)
default it_first_day_done = False
default it_task_1_done    = False
default it_npc1_done      = False
default it_npc2_done      = False
default it_review_done    = False
default it_shifts         = 0

# Hospital arc (Clinical Assistant)
default hosp_first_day_done = False
default hosp_task_1_done    = False
default hosp_npc1_done      = False
default hosp_npc2_done      = False
default hosp_review_done    = False
default hosp_shifts         = 0

# Culinary arc (Commis Chef)
default cul_first_day_done = False
default cul_task_1_done    = False
default cul_npc1_done      = False
default cul_npc2_done      = False
default cul_review_done    = False
default cul_shifts         = 0
default scene_cul_service_crisis_done = False
default cul_crisis_branch             = ""     # honest / solo_success / solo_fail / stop / send
default cul_crisis_rena_informed      = False
default cul_crisis_bad_plate          = False
default cul_crisis_technical          = ""     # saved / delayed / failed / ruined
default cul_crisis_aftermath          = ""     # good / mixed / bad
default cul_crisis_aftermath_pending  = False

# Trainer arc (Assistant Trainer)
default tr_first_day_done  = False
default tr_task_1_done     = False
default tr_npc1_done       = False
default tr_npc2_done       = False
default tr_review_done     = False
default tr_shifts          = 0

# Story flags set by topic arcs
default zoe_grant_discussed   = False
default zoe_exhibition_invited = False
default nora_school_revealed  = False
default elle_abroad_revealed  = False

# ── World Event Director ──────────────────────────────────────────────
default wed_personal_fired_day    = -1    # day when last personal WED event fired
default wed_ambient_fired         = {}    # {location_id: True} per current day
default wed_ambient_today         = {}    # pre-rolled: {location_id: event_id or None}
default wed_event_last_day        = {}    # {event_id: last day fired}
default wed_resolved              = []    # [event_id] for once=True events that have fired
default wed_callbacks             = []    # [{label, fires_day}] scheduled callbacks
default wed_ready_callbacks       = []    # callbacks whose fires_day has passed

# Marcus loan state machine
default wed_marcus_loan_state         = "none"   # none|offered|pending_repay|pending_practical|pending_solved|resolved_*
default wed_marcus_loan_callback_day  = -1       # day on which to promote callback to ready
default wed_marcus_loan_callback_ready = False   # True when callback should fire at next visit

# Sam off-routine
default sam_off_routine_done          = False
default sam_off_routine_greet_done    = False

# Marcus home access
default marcus_home_state             = "locked"  # locked|invited_once|welcome
default marcus_home_invite_day        = -1
default marcus_chili_last_day         = -1

# Job / career. job_id = career key in CAREERS (None = unemployed); the rest is
# derived from CAREERS[job_id]["ranks"][job_rank] via _sync_job() in careers.rpy.
default job_id          = None
default job_rank        = 0
default job_performance = 0      # 0-100 Performance bar for the current rank
default promotion_trials = {}    # {(job_id, from_rank): True} — trial completed
default job_title       = None   # display, e.g. "Junior Dev - The Hub"
default job_next        = ""     # promotion requirement hint
default job_schedule    = ""     # e.g. "Mon-Fri 09-17"

# Time helpers called from script
init python:
    DAILY_EVENT_POOL = [
        {"key": "gym_trainer",  "from": "Iron Gate",    "body": "Free trainer today — weight sessions give +50%% STR EXP."},
        {"key": "bar_happy",    "from": "The Barrel",   "body": "Happy Hour all day. Drinks $4, Socialize earns 2x CHR EXP."},
        {"key": "cafe_energy",  "from": "Grounds",      "body": "Double Caffeine Day. Coffee gives +20 energy instead of +10."},
        {"key": "college_sale", "from": "City College", "body": "Spring deal — all courses 30%% off today."},
        {"key": "club_night",   "from": "Neon",         "body": "Industry night. Work the Crowd earns 2x CHR EXP."},
        {"key": "park_weather", "from": "City Park",    "body": "Perfect running weather. Morning jog gives 2x STR EXP."},
    ]

    def has_event(key):
        return any(e["key"] == key for e in store.daily_events)

    def roll_daily_events():
        _r = renpy.random   # renpy.random is an RNG instance, not an importable module
        pool = list(DAILY_EVENT_POOL)
        _r.shuffle(pool)
        n = _r.choice([0, 0, 1, 1, 2])
        store.daily_events = pool[:n]

    def in_debt():
        return store.loan > 0

    # Gentle per-hour decay so a normal day needs ~1-2 meals, sleep, and a shower
    # every day or two - present but not nagging.
    DECAY = {"need_energy": 2.5, "need_hunger": 2.5, "need_hygiene": 1.5}

    def spend_time(hours):
        store.hour += hours
        for need, rate in DECAY.items():
            if need == "need_hunger" and store.skill_cook >= 3:
                rate *= 0.8   # Meal Prep perk: hunger drains 20% slower
            old = getattr(store, need)
            new = max(0, old - int(round(hours * rate)))
            setattr(store, need, new)
            _push_drain(need, new - old)
        # hygiene debuff is temporary — see eff_app(); no permanent stat damage
        # Past 3 AM (DAY_END) you can't stay awake — collapse into the next day.
        # Without this, hour climbs past 24 forever: time_label wraps %24 while
        # is_night/venue gates read raw hour, so the clock and day/night desync.
        if store.hour >= DAY_END:
            new_day()
            return   # new_day() already runs its own miss/deliver cycle
        expire_late_commitments()
        notify_available_commitments()

    def new_day():
        # Capture how depleted the player was at the END of the previous day,
        # BEFORE sleep restores energy — scenes that react to a hard day (e.g.
        # nora_bad_day) must read this, not worn_out(), which post-sleep is
        # almost always False on the energy axis.
        store.last_day_worn_out = worn_out()
        store.day  += 1
        store.hour  = DAY_START + 1.0   # wake up 8 AM
        base_energy = 100 if store.own_bed else 95
        if store.skill_fit >= 4:   # Metabolic Engine perk: sleep recovery +15%
            base_energy = min(100, int(base_energy * 1.15))
        store.need_energy  = base_energy
        _tier = store.apartment_tier
        _hunger_loss  = 15 if _tier == 1 else (10 if _tier == 2 else 5)
        _hygiene_loss = 10 if _tier == 1 else (8  if _tier == 2 else 5)
        store.need_hunger  = max(0, store.need_hunger  - _hunger_loss)
        store.need_hygiene = max(0, store.need_hygiene - _hygiene_loss)
        store.warned_today = False
        # topic streak: increment for topics used today, decay unused ones
        for npc_id, used in store._topics_today.items():
            streak = dict(store._topic_streak.get(npc_id, {}))
            for t in used:
                streak[t] = streak.get(t, 0) + 1
            for t in list(streak):
                if t not in used and streak[t] > 0:
                    streak[t] -= 1
            store._topic_streak[npc_id] = streak
        store._topics_today = {}
        # anger decays 1 per day (jealousy or bad interactions)
        store.npc_anger = {k: v - 1 for k, v in store.npc_anger.items() if v > 1}
        store.npc_texted_today = []
        check_missed_commitments()
        deliver_due_messages()
        stocks_step()
        roll_daily_events()
        wed_preroll_day()
        # Monday: rent + car (direct debit, bypasses debt block) + interest
        if store.day % 7 == 0:
            RENT = {1: 220, 2: 550, 3: 1300}
            store.money -= RENT.get(store.apartment_tier, 100)
            if store.car_tier > 0:
                store.money -= store.car_tier * 40
            # auto-loan if balance went negative
            if store.money < 0:
                store.loan += -store.money
                store.money = 0
            # 10%/week interest on outstanding loan
            if store.loan > 0:
                store.loan += max(1, int(store.loan * 0.05))
            # 2%/week interest on savings
            if store.savings > 0:
                store.savings += min(50, max(1, int(store.savings * 0.02)))
            # Ignore decay: -2 affection for each NPC not seen in the last 7 days
            # (NPC_DATA defined in interact.rpy, accessible at runtime)
            for _nid, _d in NPC_DATA.items():
                if _d.get("no_decay"):
                    continue   # mentor NPCs (e.g. Rena) aren't "seen" via the menu
                _aff_var = _d["aff"]
                _aff = getattr(store, _aff_var, 0)
                _last = store.npc_last_seen.get(_nid, store.day)
                if _aff > 0 and (store.day - _last) > 7:
                    setattr(store, _aff_var, max(0, _aff - 2))

        # ── Gameplay expansion: scene triggers ─────────────────────────────
        # martha_gift_scene_pending: promote to "delayed" after 4 days
        if (store.martha_gift_scene_pending
                and store.martha_gift_scene_pending.get("variant") == "immediate"
                and store.day >= store.martha_gift_scene_pending["trigger_day"] + 4):
            _mgp = dict(store.martha_gift_scene_pending)
            _mgp["variant"] = "delayed"
            store.martha_gift_scene_pending = _mgp

        # nora feels ignored
        if (not store.nora_ignored_done and not store.nora_ignored_pending
                and store.nora_affection >= 30 and store.nora_trust >= 20
                and store.nora_closing_done
                and "nora" in store.npc_contacts
                and (store.day - store.nora_last_seen_day) >= 8):
            store.nora_ignored_pending = True
            queue_phone_message("nora",
                "You've been quiet. Is that a thing I should know about, or just a busy week that turned into two?",
                store.day, "nora_ignored_text", responses=_NORA_IGNORED_RESP)

        # nora bad day visit
        if (not store.nora_bad_day_done and not store.nora_bad_day_pending
                and store.nora_affection >= 30 and store.nora_trust >= 20
                and store.nora_closing_done
                and "nora" in store.npc_contacts
                and store.last_day_worn_out):
            store.nora_bad_day_pending = True
            queue_phone_message("nora",
                "You had the look today. I'm off at seven. I'm bringing bread. You don't have to talk, you just have to let me in.",
                store.day, "nora_bad_day_text", responses=_NORA_BAD_DAY_RESP)

        # nora kai crossover — set pending; expires after 14 days if not triggered at café
        if (not store.nora_kai_crossover_done and not store.nora_kai_pending
                and store.nora_affection >= 30 and store.kai_affection >= 20
                and store.nora_met and store.kai_met
                and store.day >= store.nora_kai_retry_after_day):
            store.nora_kai_pending = True
            store.nora_kai_pending_day = store.day
        elif (store.nora_kai_pending
                and store.nora_kai_pending_day > 0
                and store.day > store.nora_kai_pending_day + 14):
            store.nora_kai_pending = False
            store.nora_kai_pending_day = -1
            store.nora_kai_retry_after_day = store.day + 21  # 3-week cooldown before re-triggering

        # Marcus basketball invite — fires once after sports arc + relationship gate.
        # ponytail: arc completion tracked in topic_arc_done dict (not a standalone bool).
        #   Falls back to affection gate only; add arc check here if a dedicated flag is added.
        if (not store.marcus_basketball_invite_done
                and not store.marcus_basketball_invite_pending
                and store.marcus_met
                and store.marcus_affection >= 25
                and store.topic_arc_done.get("marcus_sports_1")
                and not any(c.get("npc_id") == "marcus" for c in store.player_commitments)):
            store.marcus_basketball_invite_pending = True

        # ── Zoe spontaneous moment: pending when thresholds met ─────────────
        if (not store.zoe_moment_deflected_done
                and not store.zoe_moment_deflected_pending
                and store.zoe_affection >= 45
                and store.zoe_trust >= 35
                and store.zoe_beach_night_done):
            store.zoe_moment_deflected_pending = True
            store.zoe_moment_deflected_pending_day = store.day

        # nora hug school (pending after school reveal arc + affection/trust thresholds)
        # ponytail: nora_bad_day_done removed as gate — school reveal + stats are sufficient.
        #   nora_bad_day_done may still gate bonus dialogue inside scene_nora_hug_school.
        if (not store.nora_hug_school_done and not store.nora_hug_school_pending
                and store.nora_school_revealed
                and store.nora_affection >= 40 and store.nora_trust >= 35):
            store.nora_hug_school_pending = True
            store.nora_hug_school_pending_day = store.day

        # eli deploy hug (pending after open-source session done)
        if (not store.eli_deploy_hug_done and not store.eli_deploy_pending
                and store.programming_kit_eli_done):
            store.eli_deploy_pending = True
            store.eli_deploy_pending_day = store.day

        # lena shoulder gesture: pending after break-room + hospital hard case + thresholds.
        # hospital_hard_case_pending is set by hospital shift when job_performance < 70;
        # cleared here when scene is armed so it doesn't re-trigger on next qualifying shift.
        if (not store.lena_shoulder_done and not store.lena_shoulder_pending
                and store.lena_break_room_done
                and store.hospital_hard_case_pending
                and store.lena_affection >= 45 and store.lena_trust >= 45):
            store.lena_shoulder_pending = True
            store.lena_shoulder_pending_day = store.day
            store.hospital_hard_case_pending = False

        # ── Content Pack 2 triggers ────────────────────────────────────

        # Caroline off-work: set pending on any Thursday once gates met.
        # Expires after 14 days if player never visits bar that Thursday window.
        if (store.caroline_met
                and store.caroline_affection >= 30 and store.caroline_trust >= 25
                and not store.caroline_bar_done and not store.caroline_bar_pending):
            if store.day % 7 == 3:  # Thursday
                store.caroline_bar_pending = True
                store.caroline_bar_pending_day = store.day
        elif (store.caroline_bar_pending and store.caroline_bar_pending_day > 0
                and store.day > store.caroline_bar_pending_day + 14):
            store.caroline_bar_pending = False
            store.caroline_bar_pending_day = -1

        # Natalie humanisation: set pending once gates met; expires after 14 days.
        if (store.natalie_met
                and store.natalie_affection >= 25 and store.natalie_trust >= 20
                and not store.natalie_bar_scene_done and not store.natalie_bar_scene_pending):
            store.natalie_bar_scene_pending = True
            store.natalie_bar_scene_pending_day = store.day
        elif (store.natalie_bar_scene_pending and store.natalie_bar_scene_pending_day > 0
                and store.day > store.natalie_bar_scene_pending_day + 14):
            store.natalie_bar_scene_pending = False
            store.natalie_bar_scene_pending_day = -1

        # Kai café quiet: set pending once gates met; expires after 21 days.
        # Guard: not nora_kai_pending (nora_kai takes priority at the café).
        if (store.kai_met
                and store.kai_affection >= 30 and store.kai_trust >= 25
                and not store.kai_cafe_quiet_done and not store.kai_cafe_quiet_pending
                and not store.nora_kai_pending):
            store.kai_cafe_quiet_pending = True
            store.kai_cafe_quiet_pending_day = store.day
        elif (store.kai_cafe_quiet_pending and store.kai_cafe_quiet_pending_day > 0
                and store.day > store.kai_cafe_quiet_pending_day + 21):
            store.kai_cafe_quiet_pending = False
            store.kai_cafe_quiet_pending_day = -1

        # Elle Portugal payoff: phone message 7+ days after abroad_revealed + pier_done.
        if (store.elle_pier_done and store.elle_abroad_revealed
                and not store.elle_decision_done and not store.elle_decision_pending
                and store.elle_affection >= 40 and store.elle_trust >= 25
                and (store.elle_abroad_day < 0 or store.day >= store.elle_abroad_day + 7)
                and not message_already_queued("elle_decision_msg")):
            store.elle_decision_pending = True
            queue_phone_message("elle",
                "I made up my mind about Portugal. Come find me at the beach when you have time.",
                store.day, "elle_decision_msg")

        # Sam × Marcus crossover: set pending when both relationships developed.
        # Individual gates ensure neither is a stranger; combined >= 55 for pacing.
        if (store.sam_met and store.marcus_met
                and store.sam_affection >= 25 and store.marcus_affection >= 25
                and store.sam_affection + store.marcus_affection >= 55
                and not store.sam_marcus_scene_done and not store.sam_marcus_scene_pending):
            store.sam_marcus_scene_pending = True
            store.sam_marcus_scene_pending_day = store.day

        # Marcus home invite: queued once when relationship is established.
        if (store.marcus_home_state == "locked"
                and store.marcus_met
                and store.marcus_affection >= 30
                and store.marcus_trust >= 35
                and store.day >= 15
                and not message_already_queued("marcus_home_invite")):
            store.marcus_home_state = "invited_once"
            queue_phone_message(
                "marcus",
                "You free this week? Stop by whenever. 14 Crane Street, top floor.",
                store.day + 1, "marcus_home_invite")

        # Marcus loan callback: promote to ready when the scheduled day arrives.
        if (store.wed_marcus_loan_state in ("pending_repay", "pending_practical", "pending_solved")
                and store.wed_marcus_loan_callback_day > 0
                and store.day >= store.wed_marcus_loan_callback_day
                and not store.wed_marcus_loan_callback_ready):
            store.wed_marcus_loan_callback_ready = True
            store.wed_marcus_loan_callback_day   = -1

        # Respectful-refusal callback: Marcus mentions he sorted it.
        if (store.wed_marcus_loan_state == "resolved_refused"
                and store.wed_marcus_loan_callback_day > 0
                and store.day >= store.wed_marcus_loan_callback_day
                and not store.wed_marcus_loan_callback_ready):
            store.wed_marcus_loan_state          = "pending_solved"
            store.wed_marcus_loan_callback_ready = True
            store.wed_marcus_loan_callback_day   = -1

    def cosmetic_days_left():
        return max(0, store.cosmetic_boost_until - store.day)

    def eff_app():
        """Effective Appearance: stat_app minus hygiene debuff, plus cosmetic temp bonus."""
        h = store.need_hygiene
        if h >= 60: debuff = 0
        elif h >= 40: debuff = 5
        elif h >= 20: debuff = 12
        else: debuff = 22
        bonus = 10 if store.day < store.cosmetic_boost_until else 0
        return max(0, store.stat_app - debuff + bonus)

    def worn_out():
        # performance penalty zone: shift quality suffers but work still possible
        return store.need_energy < 30 or store.need_hunger < 25

    def too_tired():
        # hard block: below this you can't start demanding activities at all
        return store.need_energy < 20

    def status_score():
        # 0-100, from what you own. Apartment tier 1 gives a small baseline.
        return min(100, store.apartment_tier * 12 + store.car_tier * 14
                        + store.wardrobe_tier * 10 + store.jewelry_tier * 10)

    def status_label():
        s = status_score()
        if s >= 60: return "Elite"
        if s >= 40: return "Established"
        if s >= 20: return "Getting by"
        return "Nobody (yet)"

    def stat_exp_needed(level):
        """EXP to go from level → level+1. Gentle curve: fast early, slow late.
        Level 0→1: 15, L10→11: 25, L30→31: 45, L50→51: 65, L99→100: 114."""
        return 15 + level

    def affection_cap():
        return 100   # no stat gate; story_gate flags on NPC_DATA control access instead

    def home_bg():
        tier = store.apartment_tier
        is_night = store.hour >= 20 or store.hour < 6
        if tier == 1:
            return "cheaphouse_night" if is_night else "cheaphouse_day"
        elif tier == 2:
            return "goodhomenight"    if is_night else "goodhomeday"
        else:
            return "richhomenight"    if is_night else "richhomeday"

    # apartment_tier: 1=cheap, 2=good/mid, 3=rich
    # Returns the declared image name for the current home variant of a home scene CG.
    # Returns None for any unrecognised future tier — caller must fall back to home_bg() + sprite.
    _HOME_SCENE_CG = {
        "eli_dinner":       {1: "cg_eli_home_dinner_cheap",   2: "cg_eli_home_dinner_good",   3: "cg_eli_home_dinner_rich"},
        "eli_side_project": {1: "cg_eli_side_project_cheap",  2: "cg_eli_side_project_good",  3: "cg_eli_side_project_rich"},
        "nora_coffee":      {1: "cg_nora_coffee_cheap",       2: "cg_nora_coffee_good",       3: "cg_nora_coffee_rich"},
        "zoe_guitar":       {1: "cg_zoe_guitar_cheap",        2: "cg_zoe_guitar_good",        3: "cg_zoe_guitar_rich"},
    }
    def get_home_scene_cg(scene_id):
        variants = _HOME_SCENE_CG.get(scene_id)
        if variants is None:
            return None
        return variants.get(store.apartment_tier)   # None for unknown future tiers

    def cafe_bg():
        is_night = store.hour >= 19
        return "cafenight" if is_night else "cafeday"

    # ── Activity anti-repetition helpers ──────────────────────────────────
    # FIX 8: single bounded dict; count resets automatically on a new day.
    # Public interface unchanged: activity_recently_used / activity_use_count_today
    # / mark_activity_used / mark_activity_used_today.

    def activity_recently_used(activity_id, days=1):
        entry = store.activity_daily_uses.get(activity_id)
        if not entry:
            return False
        return store.day - entry["day"] < days

    def mark_activity_used(activity_id):
        d = dict(store.activity_daily_uses)
        entry = d.get(activity_id, {})
        if entry.get("day") != store.day:
            d[activity_id] = {"day": store.day, "count": 1}
        store.activity_daily_uses = d

    def activity_use_count_today(activity_id):
        """How many times this activity has been used today."""
        entry = store.activity_daily_uses.get(activity_id)
        if not entry or entry["day"] != store.day:
            return 0
        return entry["count"]

    def mark_activity_used_today(activity_id):
        d = dict(store.activity_daily_uses)
        entry = d.get(activity_id, {})
        if entry.get("day") != store.day:
            d[activity_id] = {"day": store.day, "count": 1}
        else:
            d[activity_id] = {"day": store.day, "count": entry["count"] + 1}
        store.activity_daily_uses = d

    # ── Commitment overlap warning ─────────────────────────────────────────

    def _overlap_warning_text(duration):
        """Returns a warning string if any active same-day commitment falls within [now, now+duration)."""
        end_hour = store.hour + duration
        for c in store.player_commitments:
            if not _c_active(c):
                continue
            if c["day"] != store.day:
                continue
            if store.hour <= c["hour"] < end_hour:
                hrs = c["hour"] - store.hour
                time_str = "%.0fh" % hrs if hrs >= 1 else "30 min"
                return "You have plans (%s) in %s.\nThis activity takes %dh." % (
                    c["title"], time_str, int(duration)
                )
        return ""
