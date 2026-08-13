"""Phase 64 Computer OS shell self-check.

Same approach as phase62_selfcheck: EXTRACTS the real `init python:` blocks out
of equipment.rpy / home_items.rpy / mail.rpy / calendar.rpy / computer_os.rpy and
execs them against a stub `store`, so the assertions run the shipping code.

    python phase64_computer_selfcheck.py

Guards the two things that actually break this feature:
  1. Badge counts must be DERIVED from existing state (no duplicate stores).
  2. Opening an app must clear only its own badge, and must cost no time/energy.
Plus the equipment tier -> 0..3 visual mapping and app visibility gating.
"""
import io, os, re, sys, textwrap

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rpy_python_blocks(path):
    src = io.open(os.path.join(GAME, path), encoding="utf-8").read().split("\n")
    out, i = [], 0
    while i < len(src):
        if re.match(r"^init(\s+-?\d+)?\s+python\s*:\s*$", src[i]) or src[i].strip() == "python:":
            i += 1
            body = []
            while i < len(src):
                ln = src[i]
                if ln.strip() and not ln.startswith((" ", "\t")):
                    break
                body.append(ln)
                i += 1
            out.append(textwrap.dedent("\n".join(body)))
        else:
            i += 1
    return out


class Store(object):
    def __init__(self):
        self.day = 10
        self.hour = 9.0
        self.money = 5000
        self.need_energy = 60
        # equipment
        self.owned_equipment = []
        self.equipment_condition = {}
        self.home_slots = {}
        self.wardrobe_equipped = {}
        self.savings_target = None
        self.guitar_strings_last_refreshed = -999
        self._morning_item_used = None
        self._home_ambient_day = -1
        self._home_ambient_tier = -1
        self._p62_home_flavor = ""
        self.own_guitar = False
        self.own_computer = True
        self.own_coffee_machine = False
        self.own_kitchen_set = False
        self.own_bed = False
        # systems the computer presents
        self.player_mail = []
        self._active_mail_tag = None
        self.calendar_events = []
        self.freelance_offers = []
        self.freelance_active_project = None
        self.freelance_last_refresh_day = 9
        self.market_listings_period = 3
        # computer shell state (mirrors data.rpy defaults)
        self.computer_active_app = None
        self._capp_market_seen_period = -1
        self._capp_freelance_seen_day = -2
        self._capp_market_cat = "all"


G = {}
store = Store()

_restarts = []


class _FakeRenpy(object):
    def restart_interaction(self):
        _restarts.append(1)

    def notify(self, msg):
        return None

    def call_in_new_context(self, *a, **k):
        raise AssertionError("call_in_new_context must not run during a badge/open check")


def boot():
    global G
    G = {
        "store": store,
        "renpy": _FakeRenpy(),
        "try_spend": lambda a, c="discretionary", t=True: True,
        "record_game_event": lambda *a, **k: None,
        "skill_val": lambda s: 5,
        "__builtins__": __builtins__,
    }
    for path in ("equipment.rpy", "home_items.rpy", "mail.rpy",
                 "calendar.rpy", "computer_os.rpy"):
        for blk in rpy_python_blocks(path):
            exec(compile(blk, path, "exec"), G)


failures = []


def check(name, cond, extra=""):
    print(("  OK   " if cond else "  FAIL ") + name + (("  -> " + str(extra)) if extra and not cond else ""))
    if not cond:
        failures.append(name)


def reset():
    store.__init__()
    G["store"] = store
    del _restarts[:]


def mail(tag, read=False, delivered=True):
    return {"sender": "Bank", "subject": "s", "body": "b", "category": "c",
            "send_on_day": 0, "delivered": delivered, "delivered_on": 0,
            "read": read, "tag": tag}


boot()
APPS = G["COMPUTER_APPS"]

# ── Registry ────────────────────────────────────────────────────────────────
print("\n[REGISTRY]")
check("six apps registered", len(APPS) == 6, list(APPS))
check("order preserved (OrderedDict)",
      list(APPS) == ["mail", "freelance", "marketplace", "calendar", "portfolio", "browser"],
      list(APPS))
check("every app names a capp_* screen",
      all(d["screen"].startswith("capp_") for d in APPS.values()))
check("every app has a display name", all(d["name"] for d in APPS.values()))

# ── Visibility gating ───────────────────────────────────────────────────────
print("\n[VISIBILITY]")
reset()
check("all apps visible with a computer owned",
      len(G["computer_visible_apps"]()) == 6)
store.own_computer = False
check("freelance hidden without own_computer",
      not G["computer_app_visible"]("freelance"))
check("mail still visible without own_computer",
      G["computer_app_visible"]("mail"))

# ── Badges derive from existing state ───────────────────────────────────────
print("\n[BADGES]")
reset()
check("a never-visited marketplace badges once",
      G["computer_badge_count"]("marketplace") == 1)
store._capp_market_seen_period = store.market_listings_period
check("no badges on a clean, fully-seen store",
      all(G["computer_badge_count"](a) == 0 for a in APPS),
      {a: G["computer_badge_count"](a) for a in APPS})
store._capp_market_seen_period = -1

store.player_mail = [mail("a"), mail("b"), mail("c", read=True),
                     mail("d", delivered=False)]
check("mail badge = delivered & unread (2)", G["computer_badge_count"]("mail") == 2,
      G["computer_badge_count"]("mail"))
check("mail badge matches unread_mail_count()",
      G["computer_badge_count"]("mail") == G["unread_mail_count"]())

# reading through the SHARED mail function clears the badge
G["mark_mail_read"]("a")
check("marking read via mark_mail_read drops the badge to 1",
      G["computer_badge_count"]("mail") == 1, G["computer_badge_count"]("mail"))

reset()
store.freelance_offers = ["t1", "t2", "t3"]
store.freelance_last_refresh_day = 10
check("freelance badge = offer count when board is unseen",
      G["computer_badge_count"]("freelance") == 3, G["computer_badge_count"]("freelance"))
store.freelance_active_project = {"title": "x"}
check("freelance badge suppressed while a project is active",
      G["computer_badge_count"]("freelance") == 0)

reset()
check("marketplace badge set when period differs from seen",
      G["computer_badge_count"]("marketplace") == 1)
store._capp_market_seen_period = store.market_listings_period
check("marketplace badge clears once period is seen",
      G["computer_badge_count"]("marketplace") == 0)

reset()
G["add_calendar_event"]("Dinner", store.day, 19, commitment=True)
G["add_calendar_event"]("Far off", store.day + 9, 19, commitment=True)
check("calendar badge counts only today/tomorrow commitments",
      G["computer_badge_count"]("calendar") == 1, G["computer_badge_count"]("calendar"))
check("calendar badge matches _calendar_badge_count()",
      G["computer_badge_count"]("calendar") == G["_calendar_badge_count"]())

# ── Window management: open/close clear the right badge and nothing else ────
print("\n[WINDOW MANAGEMENT]")
reset()
store.player_mail = [mail("a")]
store.freelance_offers = ["t1"]
store.freelance_last_refresh_day = 10
before = (store.day, store.hour, store.money, store.need_energy)

G["computer_open_app"]("marketplace")
check("open sets computer_active_app", store.computer_active_app == "marketplace")
check("opening marketplace clears ONLY the marketplace badge",
      G["computer_badge_count"]("marketplace") == 0
      and G["computer_badge_count"]("mail") == 1
      and G["computer_badge_count"]("freelance") == 1)

G["computer_open_app"]("freelance")
check("opening freelance clears the freelance badge",
      G["computer_badge_count"]("freelance") == 0)
check("opening freelance does NOT mark mail read",
      G["computer_badge_count"]("mail") == 1)

G["computer_open_app"]("mail")
check("opening mail does not silently mark everything read",
      G["computer_badge_count"]("mail") == 1)
check("opening mail resets the reading pane selection",
      store._active_mail_tag is None)

G["computer_close_app"]()
check("close returns to the desktop", store.computer_active_app is None)
check("close clears the reading pane", store._active_mail_tag is None)
check("every open/close restarted the interaction", len(_restarts) == 4, len(_restarts))

# THE rule: browsing is free.
check("browsing cost no time, money or energy",
      (store.day, store.hour, store.money, store.need_energy) == before,
      (store.day, store.hour, store.money, store.need_energy))

# ── Equipment visual tier ───────────────────────────────────────────────────
print("\n[VISUAL TIER]")
reset()
check("no computer owned -> tier 0", G["computer_visual_tier"]() == 0)

expected = [("basic_laptop", 0), ("thinkpad_laptop", 1),
            ("gaming_laptop", 2), ("desktop_workstation", 3),
            ("pro_workstation", 3)]
for iid, want in expected:
    reset()
    G["grant_item"](iid, "Good")
    G["equip_item"](iid)
    got = G["computer_visual_tier"]()
    check("%s -> tier %d" % (iid, want), got == want, got)

reset()
for iid, _ in expected:
    G["grant_item"](iid, "Good")
    G["equip_item"](iid)
    t = G["computer_visual_tier"]()
    check("tier stays in 0..3 (%s -> %d)" % (iid, t), 0 <= t <= 3, t)

check("a theme exists for every tier",
      all(t in G["COMPUTER_THEMES"] and len(G["COMPUTER_THEMES"][t]) == 5
          for t in range(4)))

reset()
check("tier 0 has boot flavor", G["computer_boot_flavor"]() != "")
G["grant_item"]("thinkpad_laptop", "Good"); G["equip_item"]("thinkpad_laptop")
check("mid tiers have no boot flavor", G["computer_boot_flavor"]() == "")

# ── No duplicate state ──────────────────────────────────────────────────────
print("\n[NO DUPLICATE STATE]")
src = io.open(os.path.join(GAME, "computer_os.rpy"), encoding="utf-8").read()
own_defaults = re.findall(r"^default\s+(\w+)", src, re.M)
check("computer_os.rpy declares no defaults of its own (they live in data.rpy)",
      not own_defaults, own_defaults)

data_src = io.open(os.path.join(GAME, "data.rpy"), encoding="utf-8").read()
for v in ("computer_active_app", "_capp_market_seen_period",
          "_capp_freelance_seen_day", "_capp_market_cat"):
    check("data.rpy declares default %s" % v,
          re.search(r"^default\s+%s\b" % v, data_src, re.M) is not None)

for banned in ("player_mail =", "freelance_offers =", "market_listings =",
               "calendar_events =", "player_portfolio ="):
    check("computer_os.rpy never reassigns %s" % banned.split()[0],
          banned not in src)

check("computer_desktop_session resets computer_active_app on entry",
      re.search(r"label computer_desktop_session:\s*\n\s*\$ computer_active_app = None", src) is not None)

# every screen referenced by the registry is actually defined
defined = set(re.findall(r"^screen\s+(\w+)", src, re.M))
missing = [d["screen"] for d in APPS.values() if d["screen"] not in defined]
check("every registered app screen is defined", not missing, missing)
check("shell + desktop screens defined",
      {"computer_desktop", "computer_taskbar", "computer_icon_grid",
       "computer_app_shell"} <= defined,
      sorted(defined))

# ── External data contracts CityNet & the apps format ───────────────────────
# Every key below is read by a screen in computer_os.rpy. If a producing file
# renames or retypes one, the screen crashes at render time (Ren'Py cannot
# type-check screen code), so pin the contract here.
print("\n[DATA CONTRACTS]")


def owner_src(path):
    return io.open(os.path.join(GAME, path), encoding="utf-8").read()


contracts = {
    "careers.rpy":     ["title", "req", "pay", "hours", "ranks", "location", "name"],
    "marketplace.rpy": ["name", "cat", "asking", "seller", "expire_day", "fair_low", "fair_high"],
    "freelance.rpy":   ["title", "client", "pay", "difficulty", "hours", "days", "min_skill",
                        "worked_hours", "required_hours", "deadline_day"],
    "city_events.rpy": ["title", "day", "hour", "location", "req", "saved_to_calendar", "status"],
}
for path, keys in contracts.items():
    s = owner_src(path)
    missing = [k for k in keys if ('"%s"' % k) not in s and ("'%s'" % k) not in s]
    check("%s still provides every key the computer reads" % path, not missing, missing)

# The bug this caught once: CAREERS rank "hours" is a schedule STRING, not an
# int, so the CityNet job listing must format it with %s.
# Rank dicts are the one-line `{"title": ..., "req": ..., "pay": ..., "hours": ...}` form.
rank_lines = [ln for ln in owner_src("careers.rpy").split("\n")
              if '"title":' in ln and '"pay":' in ln and '"hours":' in ln]
rank_hours = [re.search(r'"hours":\s*([^,}]+)', ln).group(1) for ln in rank_lines]
check("CAREERS rank 'hours' values are all strings",
      rank_hours and all(h.strip().startswith(('"', "'")) for h in rank_hours),
      [h for h in rank_hours if not h.strip().startswith(('"', "'"))])
job_line = re.search(r'_r0\["pay"\][^\n]*', src)
check("CityNet job listing does not format 'hours' as an integer",
      job_line is not None and "%dh" not in job_line.group(0),
      job_line.group(0) if job_line else "job listing line not found")

print("\n%d failure(s)" % len(failures))
if failures:
    for f in failures:
        print("  - " + f)
sys.exit(1 if failures else 0)
