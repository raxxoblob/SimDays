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

# Needs (0-100, decay each day)
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
default apartment_tier = 1    # 1=cheap, 2=mid, 3=rich

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
    def spend_time(hours):
        store.hour += hours
        # energy drains with activity
        store.need_energy = max(0, store.need_energy - int(hours * 5))

    def new_day():
        store.day  += 1
        store.hour  = DAY_START + 1.0   # wake up 8 AM
        # need decay
        store.need_hunger  = max(0, store.need_hunger  - 25)
        store.need_hygiene = max(0, store.need_hygiene - 15)
        store.need_energy  = 90   # slept → restored

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
