# Phase 61 — Equipment progression.
# There was no "equipped item" concept before this phase. Equipment is introduced
# here as a thin, additive layer on top of the existing own_* ownership flags:
#   * Each domain (guitar / computer / kitchen / tools) has tiered items.
#   * The player "has" the highest tier they own; that item is the equipped one.
#   * Equipment gives SMALL modifiers (capped 5-15%). Skill stays dominant.
# Baseline tier-1 items are synthesised from the legacy own_* flags so nothing
# breaks and a player who owns nothing extra gets a +0 (neutral) modifier.

default owned_equipment      = []   # list of upgrade item ids bought (marketplace/shops)
default equipment_condition  = {}   # item_id -> "Poor"/"Used"/"Good"/"Excellent"

init python:

    # effect keys:
    #   busk_perf     (+points to busking/open-mic roll)
    #   music_energy  (fractional guitar-practice energy discount)
    #   project_energy(fractional programming energy discount)
    #   prog_xp       (fractional programming practice XP bonus)
    #   cook_quality  (+points to cooking roll)
    #   cook_time     (fractional cooking prep-time discount)
    #   repair_chance (+points to mechanics repair roll)
    #   diagnosis     (+points added by a successful diagnosis; see mechanics)
    EQUIPMENT_DEFS = {
        # ── guitar ────────────────────────────────────────────────
        "basic_guitar":     {"cat": "guitar",   "tier": 1, "name": "Starter Guitar",
                             "effects": {}},
        "used_acoustic":    {"cat": "guitar",   "tier": 2, "name": "Used Acoustic Guitar",
                             "effects": {"busk_perf": 6, "music_energy": 0.03}},
        "quality_acoustic": {"cat": "guitar",   "tier": 3, "name": "Quality Acoustic",
                             "effects": {"busk_perf": 10, "music_energy": 0.05}},
        # ── computer ──────────────────────────────────────────────
        "basic_pc":         {"cat": "computer", "tier": 1, "name": "Old Laptop",
                             "effects": {}},
        "used_desktop":     {"cat": "computer", "tier": 2, "name": "Refurb Desktop",
                             "effects": {"project_energy": 0.06, "prog_xp": 0.05}},
        "dev_workstation":  {"cat": "computer", "tier": 3, "name": "Dev Workstation",
                             "effects": {"project_energy": 0.12, "prog_xp": 0.10}},
        # ── kitchen ───────────────────────────────────────────────
        "basic_kitchen":    {"cat": "kitchen",  "tier": 1, "name": "Basic Cookware",
                             "effects": {}},
        "used_cookware":    {"cat": "kitchen",  "tier": 2, "name": "Cast-Iron Cookware",
                             "effects": {"cook_quality": 5}},
        "chef_kit":         {"cat": "kitchen",  "tier": 3, "name": "Chef Knife & Pan Set",
                             "effects": {"cook_quality": 9, "cook_time": 0.10}},
        # ── tools (mechanics) ─────────────────────────────────────
        "basic_tools":      {"cat": "tools",    "tier": 1, "name": "Basic Hand Tools",
                             "effects": {}},
        "used_toolkit":     {"cat": "tools",    "tier": 2, "name": "Used Tool Kit",
                             "effects": {"repair_chance": 6, "diagnosis": 3}},
        "pro_toolkit":      {"cat": "tools",    "tier": 3, "name": "Pro Tool Kit",
                             "effects": {"repair_chance": 10, "diagnosis": 6}},
    }

    # Per-effect hard caps so a single item can never dominate a domain.
    _EQUIP_POINT_CAP = 15    # additive roll-point effects
    _EQUIP_FRAC_CAP  = 0.15  # fractional (energy/xp/time) effects

    _EQUIP_CONDITION_FACTOR = {"Poor": 0.5, "Used": 0.75, "Good": 0.9, "Excellent": 1.0}
    CONDITION_ORDER = ["Poor", "Used", "Good", "Excellent"]

    # Legacy own_* flags -> the tier-1 baseline item they grant.
    _EQUIP_BASELINE = {
        "own_guitar":      "basic_guitar",
        "own_computer":    "basic_pc",
        "own_kitchen_set": "basic_kitchen",
    }

    def _all_owned_equipment_ids():
        """Owned upgrade items + baseline items synthesised from legacy flags."""
        ids = list(store.owned_equipment)
        for flag, item_id in _EQUIP_BASELINE.items():
            if getattr(store, flag, False) and item_id not in ids:
                ids.append(item_id)
        # basic hand tools are always available (everyone has a screwdriver)
        if "basic_tools" not in ids:
            ids.append("basic_tools")
        return ids

    def owns_equipment(item_id):
        return item_id in _all_owned_equipment_ids()

    def equipment_condition_of(item_id):
        return store.equipment_condition.get(item_id, "Good")

    def equipped_item(category):
        """Highest-tier owned item in a category, or None."""
        best = None
        best_tier = -1
        for item_id in _all_owned_equipment_ids():
            d = EQUIPMENT_DEFS.get(item_id)
            if d and d["cat"] == category and d["tier"] > best_tier:
                best, best_tier = item_id, d["tier"]
        return best

    def _legacy_equipment_raw(category, effect_type):
        """Condition-scaled contribution of the legacy tier item only."""
        item_id = equipped_item(category)
        if not item_id:
            return 0.0
        raw = EQUIPMENT_DEFS[item_id]["effects"].get(effect_type, 0)
        if raw == 0:
            return 0.0
        return raw * _EQUIP_CONDITION_FACTOR.get(equipment_condition_of(item_id), 0.9)

    def equipment_modifier(category, effect_type):
        """Capped modifier for a category, scaled by condition. Returns an int
        for point effects, float for fractional ones.

        Phase 62: folds in the equipped home-room items that feed this category
        (see ROOM_TO_EQUIP_CAT in home_items.rpy) so there is ONE modifier
        pipeline, not two. The room's PRIMARY slot replaces the legacy tier item
        instead of stacking with it — otherwise a player holding both an old
        legacy guitar and a new catalog guitar would double-dip toward the cap.
        Accessory slots (amp, monitors, workbench, ...) stack additively.
        The Phase 61 caps still apply to the combined total."""
        legacy = _legacy_equipment_raw(category, effect_type)
        home_primary, home_extra = 0.0, 0.0
        for room, (cat, primary_slot) in ROOM_TO_EQUIP_CAT.items():
            if cat != category:
                continue
            for slot in HOME_ROOM_SLOTS.get(room, []):
                iid = equipped_in(room, slot)
                if not iid:
                    continue
                val = _raw_home_effect(iid, effect_type)
                if not val:
                    continue
                if slot == primary_slot:
                    home_primary += val
                else:
                    home_extra += val
        total = max(legacy, home_primary) + home_extra
        if total == 0:
            return 0
        # A key is fractional if either source declares it as a float.
        is_frac = effect_type in _HOME_FRAC_KEYS
        if is_frac:
            return min(_EQUIP_FRAC_CAP, total)
        return int(min(_EQUIP_POINT_CAP, round(total)))

    def grant_equipment(item_id, condition="Good"):
        """Add an equipment item to the player's inventory (idempotent)."""
        if item_id not in store.owned_equipment:
            store.owned_equipment = list(store.owned_equipment) + [item_id]
        c = dict(store.equipment_condition)
        c[item_id] = condition
        store.equipment_condition = c

    def improve_equipment_condition(item_id):
        """Bump condition one step (used by mechanics restoration). Returns new
        condition or None if already Excellent / unknown item."""
        cur = equipment_condition_of(item_id)
        if cur not in CONDITION_ORDER:
            return None
        idx = CONDITION_ORDER.index(cur)
        if idx >= len(CONDITION_ORDER) - 1:
            return None
        new = CONDITION_ORDER[idx + 1]
        c = dict(store.equipment_condition)
        c[item_id] = new
        store.equipment_condition = c
        return new

    def p62_primary_item_for(category):
        """The catalog item occupying this category's PRIMARY home slot, or None.
        Lets the Gear screen name the real item a Phase 62 player is using."""
        for room, (cat, primary_slot) in ROOM_TO_EQUIP_CAT.items():
            if cat == category:
                iid = equipped_in(room, primary_slot)
                if iid and ITEM_CATALOG[iid]["price_new"] > 0:
                    return iid
        return None

    def _category_effect_keys(category):
        """Every effect key this category can currently produce (legacy + home)."""
        keys = set()
        item_id = equipped_item(category)
        if item_id:
            keys |= set(EQUIPMENT_DEFS[item_id]["effects"])
        for room, (cat, _primary) in ROOM_TO_EQUIP_CAT.items():
            if cat != category:
                continue
            for slot in HOME_ROOM_SLOTS.get(room, []):
                iid = equipped_in(room, slot)
                if iid:
                    keys |= set(ITEM_CATALOG[iid]["modifiers"])
        # Phase 62-only keys are reported by the Home screen, not the Gear screen.
        return [k for k in keys if k in EFFECT_LABELS]

    def equipment_effect_summary(category):
        """Human-readable list of (label, value_str) for the live category total
        (legacy tier item + equipped home-room items)."""
        out = []
        for eff in sorted(_category_effect_keys(category)):
            val = equipment_modifier(category, eff)
            if not val:
                continue
            if eff in _HOME_FRAC_KEYS:
                sign = "-" if eff.endswith(("energy", "time")) else "+"
                out.append((EFFECT_LABELS.get(eff, eff), "%s%d%%" % (sign, int(round(abs(val) * 100)))))
            else:
                out.append((EFFECT_LABELS.get(eff, eff), "+%d" % val))
        return out

    EFFECT_LABELS = {
        "busk_perf":      "Busking performance",
        "music_energy":   "Guitar practice energy",
        "project_energy": "Project energy cost",
        "prog_xp":        "Programming practice XP",
        "cook_quality":   "Cooking quality",
        "cook_time":      "Cooking prep time",
        "repair_chance":  "Repair chance",
        "diagnosis":      "Diagnosis bonus",
    }

    _EQUIP_CATEGORIES = [
        ("guitar",   "Guitar"),
        ("computer", "Computer"),
        ("kitchen",  "Kitchen"),
        ("tools",    "Tools"),
    ]


# ── Equipment inspection screen (phone app) ─────────────────────────────────────
screen equipment_scr():
    modal True
    use phone_shell:
        vbox:
            xsize (PHONE_SCR_W - 24)
            xalign 0.5
            spacing 0
            null height 8
            text "Equipment" font PROFILE_FONT size 22 color "#ffffff" xalign 0.5
            null height 6
            viewport:
                xfill True
                ysize 610
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 10
                    xfill True
                    for _cat, _clabel in _EQUIP_CATEGORIES:
                        $ _eq = equipped_item(_cat)
                        # Phase 62: a player may own only catalog items in this
                        # category, in which case there is no legacy item to name
                        # but there ARE live bonuses. Fall back to the home item.
                        $ _hq = p62_primary_item_for(_cat)
                        $ _summ = equipment_effect_summary(_cat)
                        frame:
                            xfill True
                            background Frame("images/ui/act_bar_idle.png", 16, 16, 16, 16)
                            padding (10, 8, 10, 8)
                            vbox:
                                spacing 3
                                text _clabel font PROFILE_FONT size 13 color "#5bcafa"
                                if _hq:
                                    hbox:
                                        xfill True
                                        text ITEM_CATALOG[_hq]["label"] font ACT_FONT size 13 color "#cfe0f5" yalign 0.5
                                        text equipment_condition_of(_hq) font ACT_FONT size 12 color "#7fd06a" yalign 0.5 xalign 1.0
                                elif _eq:
                                    hbox:
                                        xfill True
                                        text EQUIPMENT_DEFS[_eq]["name"] font ACT_FONT size 13 color "#cfe0f5" yalign 0.5
                                        text equipment_condition_of(_eq) font ACT_FONT size 12 color "#7fd06a" yalign 0.5 xalign 1.0
                                else:
                                    text "Nothing owned in this category." font ACT_FONT size 12 color "#4a6080"
                                if _summ:
                                    for _lbl, _vs in _summ:
                                        hbox:
                                            xfill True
                                            text _lbl font ACT_FONT size 11 color "#7a9ab8" yalign 0.5
                                            text _vs font ACT_FONT size 11 color "#ffd66a" yalign 0.5 xalign 1.0
                                elif _eq or _hq:
                                    text "No mechanical bonus (baseline gear)." font ACT_FONT size 11 color "#4a6080"
            null height 6
            textbutton "Back" action [Hide("equipment_scr"), Show("phone_home")] xalign 0.5 text_font ACT_FONT text_size 20 text_color "#9fb6d6" text_hover_color "#ffffff"
