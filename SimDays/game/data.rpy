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

default mc_name = "Alex"   # player's name; set during the intro, personalizable

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
default warned_today    = False   # low-need heads-up fires at most once a day
default gift_count      = 0       # generic gifts on hand (give to NPCs for affection)
default apartment_tier = 1    # 1=cheap, 2=mid, 3=rich

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

# Job / career. job_id = career key in CAREERS (None = unemployed); the rest is
# derived from CAREERS[job_id]["ranks"][job_rank] via _sync_job() in careers.rpy.
default job_id          = None
default job_rank        = 0
default job_performance = 0      # 0-100 Performance bar for the current rank
default job_title       = None   # display, e.g. "Junior Dev - The Hub"
default job_next        = ""     # promotion requirement hint
default job_schedule    = ""     # e.g. "Mon-Fri 09-17"

# Time helpers called from script
init python:
    # Gentle per-hour decay so a normal day needs ~1-2 meals, sleep, and a shower
    # every day or two - present but not nagging.
    DECAY = {"need_energy": 3.0, "need_hunger": 2.5, "need_hygiene": 1.5}

    def spend_time(hours):
        store.hour += hours
        for need, rate in DECAY.items():
            setattr(store, need, max(0, getattr(store, need) - int(round(hours * rate))))
        # Grimy -> your looks tank fast, no matter how groomed you were (floor 5).
        if store.need_hygiene < 40:
            drop = hours * (4 if store.need_hygiene < 20 else 2)
            store.stat_app = max(5, store.stat_app - int(round(drop)))

    def new_day():
        store.day  += 1
        store.hour  = DAY_START + 1.0   # wake up 8 AM
        # sleeping refills energy; you wake a little hungry / rumpled
        store.need_energy  = 100 if store.own_bed else 95   # better bed = fuller rest
        store.need_hunger  = max(0, store.need_hunger  - 15)
        store.need_hygiene = max(0, store.need_hygiene - 10)
        store.warned_today = False
        stocks_step()   # each stock moves independently overnight (see stocks.rpy)

    def worn_out():
        # too tired or too hungry to perform well (used by jobs/activities)
        return store.need_energy < 25 or store.need_hunger < 25

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

    def affection_cap():
        # how far ANY relationship can climb, gated by your status. Raise status
        # to lift the ceiling, then keep courting.
        s = status_score()
        if s >= 60: return 100
        if s >= 40: return 75
        if s >= 20: return 50
        return 25

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
