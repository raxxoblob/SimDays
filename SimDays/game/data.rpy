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
default own_computer = True   # coding practice, stock trading
default own_guitar   = False  # music practice
default own_bed      = False  # better bed: full rest + a quick Nap option
# stock market state lives in stocks.rpy

# Finance
default loan    = 0     # outstanding debt; blocks all spending until repaid
default savings = 0     # savings account; earns 2%/week interest

# World events (refreshed each new_day)
default daily_events = []   # list of event dicts from DAILY_EVENT_POOL

# Contacts (NPC phone numbers; only added when the player asks)
default npc_contacts = []
default degrees    = []        # earned degree ids: "med_bach", "med_mast", "prog_bach", etc.
default npc_anger        = {}   # npc_id -> anger level; decays 1/day

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

    def new_day():
        store.day  += 1
        store.hour  = DAY_START + 1.0   # wake up 8 AM
        base_energy = 100 if store.own_bed else 95
        if store.skill_fit >= 4:   # Metabolic Engine perk: sleep recovery +15%
            base_energy = min(100, int(base_energy * 1.15))
        store.need_energy  = base_energy
        store.need_hunger  = max(0, store.need_hunger  - 15)
        store.need_hygiene = max(0, store.need_hygiene - 10)
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
        stocks_step()
        roll_daily_events()
        # Monday: rent + car (direct debit, bypasses debt block) + interest
        if store.day % 7 == 0:
            RENT = {1: 100, 2: 250, 3: 600}
            store.money -= RENT.get(store.apartment_tier, 100)
            if store.car_tier > 0:
                store.money -= store.car_tier * 40
            # auto-loan if balance went negative
            if store.money < 0:
                store.loan += -store.money
                store.money = 0
            # 10%/week interest on outstanding loan
            if store.loan > 0:
                store.loan += max(1, int(store.loan * 0.10))
            # 2%/week interest on savings
            if store.savings > 0:
                store.savings += max(1, int(store.savings * 0.02))
            # Ignore decay: -2 affection for each NPC not seen in the last 7 days
            # (NPC_DATA defined in interact.rpy, accessible at runtime)
            for _nid, _d in NPC_DATA.items():
                _aff_var = _d["aff"]
                _aff = getattr(store, _aff_var, 0)
                _last = store.npc_last_seen.get(_nid, store.day)
                if _aff > 0 and (store.day - _last) > 7:
                    setattr(store, _aff_var, max(0, _aff - 2))

    def eff_app():
        """Effective Appearance: stat_app minus a temporary hygiene debuff."""
        h = store.need_hygiene
        if h >= 60: debuff = 0
        elif h >= 40: debuff = 5
        elif h >= 20: debuff = 12
        else: debuff = 22
        return max(0, store.stat_app - debuff)

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

    def cafe_bg():
        is_night = store.hour >= 19
        return "cafenight" if is_night else "cafeday"
