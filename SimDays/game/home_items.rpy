# Phase 62 — Lifestyle, home and item economy.
#
# DESIGN NOTE (read before extending):
#   This phase does NOT create a second inventory. Ownership lives in
#   `owned_equipment` + `equipment_condition` (Phase 61, equipment.rpy) and is
#   written through grant_equipment(). `home_slots` only records WHICH owned
#   item is currently active in each room slot.
#   Modifiers do NOT create a parallel system either: equipment_modifier() in
#   equipment.rpy was extended to fold in home-slot items, so every existing
#   call site (busking, cooking, mechanics, freelance) picks them up for free.
#   Keys that Phase 61 has no concept of (sleep, home social, morning energy)
#   go through home_modifier() and are capped independently.

default home_slots                   = {}     # {room: {slot: item_id}}
default wardrobe_equipped            = {}     # {category: clothing_id}
default savings_target               = None   # item_id the player is saving for
default guitar_strings_last_refreshed = -999  # day number
default _morning_item_used           = None   # day number the morning item was used
default _home_seen_by                = []     # npc ids that have seen the current tier
default _home_ambient_day            = -1
default _home_ambient_tier           = -1
default _p62_home_flavor             = ""
default _p62_drink                   = None
default _p62_drink_name              = ""
default _p62_drink_gain              = 0
default _p62_morning_label           = "Make coffee (0.5h)"
default _p62_strings_cost            = 12
default _p62_has_guitar              = False

init -1 python:

    # ── Rooms and their slots ────────────────────────────────────────────────
    # Order matters: it is the display order in the room overview screen.
    HOME_ROOMS = [
        ("bedroom",      "Bedroom",       ["bed", "lighting", "comfort_extra"]),
        ("workspace",    "Workspace",     ["desk", "computer", "chair", "accessory"]),
        ("kitchen",      "Kitchen",       ["appliance_major", "cookware", "appliance_small"]),
        ("music_corner", "Music Corner",  ["instrument", "amp", "accessory"]),
        ("workshop",     "Workshop",      ["tools", "workbench", "specialized"]),
        ("living_room",  "Living Room",   ["seating", "display", "decor_level"]),
        # Phase 65: the corner of the flat a hobby physically occupies. One slot
        # today (art_station); future hobby phases add their station here rather
        # than bolting slots onto rooms that already mean something else.
        # Weighted 0.75 in home_visual_score like the other working rooms, so an
        # empty corner costs a little look — which is honest, it IS empty.
        ("studio",       "Studio Corner", ["art_station"]),
    ]
    HOME_ROOM_LABELS = {r: lbl for r, lbl, _ in HOME_ROOMS}
    HOME_ROOM_SLOTS  = {r: slots for r, _, slots in HOME_ROOMS}

    SLOT_LABELS = {
        "bed": "Bed", "lighting": "Lighting", "comfort_extra": "Climate",
        "desk": "Desk", "computer": "Computer", "chair": "Chair", "accessory": "Accessory",
        "appliance_major": "Stove", "cookware": "Cookware", "appliance_small": "Small appliance",
        "instrument": "Instrument", "amp": "Amp",
        "tools": "Tools", "workbench": "Workbench", "specialized": "Specialised",
        "seating": "Seating", "display": "Screen", "decor_level": "Decor",
        "art_station": "Art station",
    }

    # Home rooms whose gear feeds a Phase 61 equipment category. The FIRST slot
    # listed is the "primary" one: it REPLACES the legacy equipment item rather
    # than stacking with it, so a player who owns both an old legacy guitar and
    # a new catalog guitar does not double-dip toward the cap.
    ROOM_TO_EQUIP_CAT = {
        "music_corner": ("guitar",   "instrument"),
        "workspace":    ("computer", "computer"),
        "kitchen":      ("kitchen",  "cookware"),
        "workshop":     ("tools",    "tools"),
    }

    # ── Item catalog ─────────────────────────────────────────────────────────
    ITEM_CATALOG = {}

    def _item(iid, label, cat, slot, new, vis, desc,
              mods=None, unlocks=None, used=None, shop=True, used_ok=True,
              caps=None):
        """Compact catalog builder. price_used defaults to ~55% of retail.
        `caps` (Phase 65): capability ids this item enables at home when active.
        Read only through has_home_capability() — never by item id."""
        ITEM_CATALOG[iid] = {
            "label": label, "category": cat, "slot": slot,
            "price_new": new,
            "price_used": int(round((new * 0.55 if used is None else used) / 5.0) * 5),
            "description": desc,
            "modifiers": mods or {},
            "unlocks": unlocks or [],
            "visual_tier": vis,
            "available_used": bool(used_ok and new >= 40),
            "shop_available": shop,
            "capabilities": caps or [],
        }

    # ---- WORKSPACE ----------------------------------------------------------
    _item("basic_laptop", "Old Laptop", "workspace", "computer", 220, 1,
          "Slow, loud fan, but it compiles. Eventually.",
          {"project_energy": 0.02}, caps=["programming", "computer_work"])
    _item("thinkpad_laptop", "Refurbished ThinkPad", "workspace", "computer", 380, 2,
          "Boring, indestructible, and the keyboard is genuinely good.",
          {"project_energy": 0.05, "prog_xp": 0.04}, caps=["programming", "computer_work"])
    _item("gaming_laptop", "Gaming Laptop", "workspace", "computer", 850, 3,
          "Overkill for text files. Wonderful for everything else.",
          {"project_energy": 0.08, "prog_xp": 0.06}, caps=["programming", "computer_work"])
    _item("desktop_workstation", "Custom Desktop", "workspace", "computer", 1400, 4,
          "You picked every part. Builds finish before you finish your coffee.",
          {"project_energy": 0.12, "prog_xp": 0.10}, caps=["programming", "computer_work"])
    _item("pro_workstation", "Dual-CPU Workstation", "workspace", "computer", 3200, 4,
          "Absurd. Silent under load. You do not regret it.",
          {"project_energy": 0.14, "prog_xp": 0.12}, used_ok=False,
          caps=["programming", "computer_work", "professional_programming"])
    _item("basic_desk", "Folding Table", "workspace", "desk", 40, 1,
          "It has four legs and holds a laptop. That is the whole review.")
    _item("student_desk", "Student Desk", "workspace", "desk", 120, 2,
          "Flat-pack, one drawer, slight wobble you have learned to work around.",
          {"project_energy": 0.02})
    _item("large_desk", "Large Writing Desk", "workspace", "desk", 280, 3,
          "Enough surface to spread out a whole problem at once.",
          {"project_energy": 0.04, "prog_xp": 0.02})
    _item("standing_desk", "Standing Desk", "workspace", "desk", 520, 4,
          "Motorised. You use the standing mode more often than you expected.",
          {"project_energy": 0.06, "work_session_minutes": 20})
    _item("kitchen_chair", "Kitchen Chair", "workspace", "chair", 0, 1,
          "You sit on it. Your back files a complaint after two hours.", shop=False)
    _item("office_chair", "Basic Office Chair", "workspace", "chair", 90, 2,
          "Adjustable height. That is the feature list.",
          {"work_session_minutes": 15, "project_energy": 0.02})
    _item("ergonomic_chair", "Ergonomic Chair", "workspace", "chair", 320, 3,
          "Lumbar support you stop noticing, which is the point.",
          {"work_session_minutes": 30, "project_energy": 0.04})
    _item("keyboard_basic", "Membrane Keyboard", "workspace", "accessory", 35, 1,
          "Quiet, cheap, entirely forgettable.")
    _item("keyboard_mech", "Mechanical Keyboard", "workspace", "accessory", 120, 2,
          "Loud enough that the neighbours know when a deadline is close.",
          {"prog_xp": 0.02})
    _item("second_monitor", "Second Monitor", "workspace", "accessory", 210, 3,
          "Docs on one side, code on the other. You will not go back.",
          {"project_energy": 0.03, "prog_xp": 0.02})
    _item("dual_monitors", "Dual Monitor Setup", "workspace", "accessory", 420, 4,
          "Two panels on an arm. Your desk finally looks like it means business.",
          {"project_energy": 0.05, "prog_xp": 0.03})

    # ---- BEDROOM ------------------------------------------------------------
    _item("basic_bed", "Single Mattress", "bedroom", "bed", 0, 1,
          "On the floor. It is a bed in the technical sense.", shop=False)
    _item("double_bed", "Double Bed Frame", "bedroom", "bed", 280, 2,
          "Off the floor at last. It even has a headboard.",
          {"sleep_recovery": 0.06})
    _item("quality_mattress", "Memory Foam Mattress", "bedroom", "bed", 480, 3,
          "The first night on it is genuinely surprising.",
          {"sleep_recovery": 0.15})
    _item("premium_bed", "Platform Bed + Mattress", "bedroom", "bed", 820, 4,
          "Solid frame, proper mattress. Mornings feel different.",
          {"sleep_recovery": 0.20})
    _item("bare_bulb", "Bare Bulb", "bedroom", "lighting", 0, 0,
          "One bulb, one switch, no shade.", shop=False)
    _item("desk_lamp", "Bedside Lamp", "bedroom", "lighting", 35, 1,
          "Warm light instead of interrogation light.",
          {"sleep_recovery": 0.03})
    _item("blackout_curtains", "Blackout Curtains", "bedroom", "lighting", 75, 2,
          "Street light stays outside where it belongs.",
          {"sleep_recovery": 0.08})
    _item("smart_lighting", "Smart Lighting Kit", "bedroom", "lighting", 160, 3,
          "Dims automatically in the evening. Faintly ridiculous, quietly great.",
          {"sleep_recovery": 0.10, "home_social": 1})
    _item("fan_basic", "Box Fan", "bedroom", "comfort_extra", 45, 1,
          "Loud, but the white noise helps more than the airflow.",
          {"sleep_recovery": 0.03})
    _item("tower_fan", "Tower Fan", "bedroom", "comfort_extra", 110, 2,
          "Oscillates. Much quieter than the box fan it replaced.",
          {"sleep_recovery": 0.05, "summer_energy_drain": 0.02})
    _item("ac_unit", "Window AC Unit", "bedroom", "comfort_extra", 380, 3,
          "Heavy to install, worth it by the first hot week.",
          {"sleep_recovery": 0.10, "summer_energy_drain": 0.05})

    # ---- KITCHEN ------------------------------------------------------------
    _item("basic_stove", "Basic Stove", "kitchen", "appliance_major", 0, 1,
          "Two of the four rings work reliably.", shop=False)
    _item("upgraded_oven", "Gas Range + Oven", "kitchen", "appliance_major", 640, 3,
          "Real flame control and an oven that holds its temperature.",
          {"cook_quality": 4, "cook_time": 0.05})
    _item("basic_pots", "Basic Pot Set", "kitchen", "cookware", 0, 1,
          "Thin bases. Everything sticks if you look away.", shop=False)
    _item("quality_cookware", "Quality Cookware Set", "kitchen", "cookware", 180, 2,
          "Heavy bottoms, even heat. Cooking stops being a fight.",
          {"cook_quality": 5, "recipe_difficulty_max": 7}, caps=["quality_cooking"])
    _item("pro_cookware", "Professional Cookware", "kitchen", "cookware", 420, 4,
          "Restaurant-grade. Slightly intimidating in a good way.",
          {"cook_quality": 9, "cook_time": 0.08, "recipe_difficulty_max": 10},
          caps=["quality_cooking", "professional_cooking"])
    _item("coffee_maker", "Drip Coffee Maker", "kitchen", "appliance_small", 55, 1,
          "Fills the flat with the right smell at the right hour.",
          {"morning_energy": 5})
    _item("espresso_machine", "Espresso Machine", "kitchen", "appliance_small", 320, 3,
          "Takes practice. Makes mornings something you look forward to.",
          {"morning_energy": 8, "home_social": 2})
    _item("blender", "Blender", "kitchen", "appliance_small", 80, 2,
          "Loud for nine seconds, useful for years.",
          {"morning_energy": 4}, unlocks=["smoothie_recipe"])

    # ---- MUSIC --------------------------------------------------------------
    _item("old_acoustic", "Old Acoustic Guitar", "music", "instrument", 140, 1,
          "The action is high and the tuners slip. It still sings.",
          {"busk_perf": 3}, caps=["guitar_playing"])
    _item("cedar_acoustic", "Cedar Acoustic", "music", "instrument", 380, 2,
          "Warm cedar top. It rewards a light touch.",
          {"busk_perf": 6, "music_energy": 0.03}, caps=["guitar_playing"])
    _item("stage_electroacoustic", "Stage Electro-Acoustic", "music", "instrument", 780, 3,
          "Built to be plugged in. Cuts through a noisy room.",
          {"busk_perf": 10, "music_energy": 0.05}, unlocks=["paid_gig_option"],
          caps=["guitar_playing", "amplified_performance"])
    _item("vintage_acoustic", "Vintage Dreadnought", "music", "instrument", 2600, 4,
          "Sixty years old. People stop walking when you play it.",
          {"busk_perf": 13, "music_energy": 0.06},
          unlocks=["paid_gig_option"], used_ok=False,
          caps=["guitar_playing", "amplified_performance"])
    _item("practice_amp", "Small Practice Amp", "music", "amp", 130, 1,
          "Fifteen watts. Plenty for a flat with thin walls.",
          {"music_energy": 0.02})
    _item("combo_amp", "Good Combo Amp", "music", "amp", 310, 3,
          "Clean headroom and a reverb you actually like.",
          {"busk_perf": 3, "music_energy": 0.03})
    _item("guitar_stand", "Guitar Stand", "music", "accessory", 25, 1,
          "The guitar is out of its case, so you pick it up more.",
          {"music_energy": 0.02})
    _item("pedal_delay", "Delay Pedal", "music", "accessory", 90, 2,
          "One knob too many, but the sound fills out beautifully.",
          {"busk_perf": 2})
    _item("pedalboard", "Pedalboard + 3 Pedals", "music", "accessory", 280, 3,
          "Everything patched and velcroed down. Setup takes a minute now.",
          {"busk_perf": 4})

    # ---- WORKSHOP -----------------------------------------------------------
    _item("basic_tool_set", "Basic Tool Set", "workshop", "tools", 45, 1,
          "Screwdrivers, pliers, an adjustable spanner. Covers most of it.",
          {"repair_chance": 3}, caps=["basic_repair"])
    _item("mechanics_toolkit", "Mechanic's Toolkit", "workshop", "tools", 190, 2,
          "Proper sockets in a proper case. No more improvising.",
          {"repair_chance": 6, "diagnosis": 3}, caps=["basic_repair", "mechanics_work"])
    _item("precision_kit", "Precision Electronics Kit", "workshop", "tools", 280, 3,
          "Tiny drivers, tweezers, magnifier. For the fiddly work.",
          {"repair_chance": 10, "diagnosis": 6}, unlocks=["electronics_projects"],
          caps=["basic_repair", "mechanics_work", "electronics_work"])
    _item("portable_workbench", "Portable Workbench", "workshop", "workbench", 130, 1,
          "Folds away. Wobbles slightly. Better than the kitchen table.",
          {"repair_chance": 2})
    _item("proper_workbench", "Proper Workbench", "workshop", "workbench", 340, 3,
          "Heavy top, vice bolted on. Nothing moves while you work.",
          {"repair_chance": 4}, unlocks=["advanced_projects"])
    _item("soldering_station", "Soldering Station", "workshop", "specialized", 95, 2,
          "Temperature controlled. Your joints stop looking like chewing gum.",
          {"repair_chance": 3, "diagnosis": 2})
    _item("electronics_bench", "Full Electronics Bench", "workshop", "specialized", 460, 4,
          "Scope, bench supply, hot air. You can see what the circuit is doing.",
          {"repair_chance": 5, "diagnosis": 4}, unlocks=["electronics_projects"])

    # ---- LIVING ROOM --------------------------------------------------------
    _item("basic_sofa", "Second-hand Sofa", "living_room", "seating", 150, 1,
          "One cushion is flatter than the others. It seats three at a push.",
          {"home_social": 2})
    _item("good_sofa", "Good Sofa", "living_room", "seating", 480, 3,
          "Deep enough to sink into, firm enough to get back out of.",
          {"home_social": 4})
    _item("sectional_sofa", "Sectional Sofa", "living_room", "seating", 980, 4,
          "Everyone gets a corner. Nobody wants to leave.",
          {"home_social": 7})
    _item("designer_sofa", "Designer Lounge Sofa", "living_room", "seating", 2400, 4,
          "The kind of thing people photograph without meaning to.",
          {"home_social": 8}, used_ok=False)
    _item("small_tv", "32\" TV", "living_room", "display", 220, 1,
          "Fine from close up. Two people can share it.",
          {"home_social": 2})
    _item("mid_tv", "50\" Smart TV", "living_room", "display", 520, 3,
          "Big enough that people stop looking at their phones.",
          {"home_social": 5})
    _item("large_tv", "65\" TV + Soundbar", "living_room", "display", 1100, 4,
          "Film night at your place became a thing people ask about.",
          {"home_social": 8})
    _item("home_theater", "Projector + 5.1 System", "living_room", "display", 2200, 4,
          "Lights off, wall becomes a cinema. Absurd and wonderful.",
          {"home_social": 9}, used_ok=False)
    _item("basic_decor", "Some Posters", "living_room", "decor_level", 30, 1,
          "Blu-tack and enthusiasm. It is a start.",
          {"home_social": 1})
    _item("nice_decor", "Art Prints + Plants", "living_room", "decor_level", 120, 2,
          "Framed prints, three plants you have not killed yet.",
          {"home_social": 3})
    _item("curated_decor", "Gallery Wall + Setup", "living_room", "decor_level", 280, 4,
          "Considered, hung straight, lit properly. It looks like a choice.",
          {"home_social": 5})

    # ---- LIFESTYLE (no slot — pure ownership) --------------------------------
    _item("coffee_grinder", "Burr Coffee Grinder", "lifestyle", None, 85, 2,
          "Fresh grounds every morning. A small ritual you look forward to.")
    _item("record_player", "Turntable", "lifestyle", None, 240, 3,
          "Deliberately inconvenient. That is most of the appeal.",
          {"home_social": 2})
    _item("bookshelf", "Bookshelf", "lifestyle", None, 90, 2,
          "The books are off the floor. The flat reads differently.",
          {"home_social": 1})
    _item("nice_headphones", "Quality Headphones", "lifestyle", None, 180, 2,
          "You hear parts of songs you have known for years.",
          {"music_energy": 0.02})
    _item("smart_speaker", "Smart Speaker", "lifestyle", None, 120, 2,
          "Music follows you between rooms. Occasionally mishears you.",
          {"home_social": 1})
    _item("plants_set", "Plant Collection", "lifestyle", None, 60, 2,
          "Six pots by the window. Watering them became part of Sunday.")
    _item("art_print", "Framed Art Print", "lifestyle", None, 45, 1,
          "You bought it because you liked it. That was the whole reason.")
    _item("hifi_system", "Hi-Fi Listening System", "lifestyle", None, 1800, 4,
          "Separates, proper speakers, one very good chair.",
          {"home_social": 4}, used_ok=False)

    # ---- ART / CREATIVE (Phase 65) ------------------------------------------
    # The easels are the capability gate for painting. Nothing outside this block
    # names them: the home menu asks has_home_capability("painting").
    _item("basic_easel", "Basic Easel", "studio", "art_station", 145, 1,
          "Pine, three legs, one wing nut that needs retightening. It holds a canvas.",
          {"art_quality_modifier": 0.04}, caps=["painting", "sketching"])
    _item("studio_easel", "Studio Easel", "studio", "art_station", 380, 3,
          "Heavy, adjustable, and it does not move when you lean into a stroke.",
          {"art_quality_modifier": 0.09, "home_social": 1},
          caps=["painting", "sketching", "professional_painting"])
    # Sketching without an easel: cheap, real, and already a marketplace item
    # (own_sketchbook, Phase 45) that until now unlocked nothing at all.
    _item("sketchbook", "Sketchbook", "lifestyle", None, 22, 1,
          "Cartridge paper and a tin of charcoal. Fits in a bag.",
          caps=["sketching"])
    # Not a capability — a quality modifier and the source of material cost.
    # Painting without it means improvising, which is worse but free.
    _item("art_supply_kit", "Art Supply Kit", "lifestyle", None, 55, 1,
          "Decent brushes, real pigment, canvas board by the pack.",
          {"art_quality_modifier": 0.04})

    # ---- WARDROBE -----------------------------------------------------------
    # Wardrobe items use `slot` as the clothing CATEGORY.
    _item("basic_casual", "Basic T-shirt + Jeans", "wardrobe", "casual", 0, 1,
          "Clean, comfortable, invisible. Works nearly everywhere.", shop=False)
    _item("nice_casual", "Quality Casual Outfit", "wardrobe", "casual", 90, 2,
          "Things that fit properly. People notice without knowing why.",
          {"confidence": 2})
    _item("smart_casual", "Smart Casual", "wardrobe", "smart_casual", 160, 3,
          "The outfit that covers eighty percent of situations.",
          {"confidence": 3})
    _item("nice_jacket_smart", "Quality Jacket", "wardrobe", "smart_casual", 160, 3,
          "Good shoulders, honest fabric. Lifts anything underneath it.",
          {"confidence": 3})
    _item("formal_outfit", "Business Formal Outfit", "wardrobe", "formal", 240, 3,
          "For the rooms where being underdressed is the whole story.",
          {"confidence": 4})
    _item("tailored_suit", "Tailored Suit", "wardrobe", "formal", 1200, 4,
          "Measured, adjusted, made for you. It changes how you stand.",
          {"confidence": 6}, used_ok=False)
    _item("performance_jacket", "Stage Jacket", "wardrobe", "music_performance", 180, 3,
          "Reads well under bad lighting. Made to be looked at.",
          {"confidence": 3, "busk_perf": 2})
    _item("sport_kit", "Sport Kit", "wardrobe", "sport", 65, 2,
          "Proper shoes and something that breathes.",
          {"confidence": 2})
    _item("work_uniform", "Work-appropriate Set", "wardrobe", "work_uniform_compatible", 110, 2,
          "Neutral, durable, meets every dress code you have met.",
          {"confidence": 2})
    _item("premium_watch", "Nice Watch", "wardrobe", "accessory", 340, 3,
          "Quiet, mechanical, and it does not need charging.",
          {"confidence": 3})

    WARDROBE_CATEGORIES = [
        ("casual",                   "Casual"),
        ("smart_casual",             "Smart casual"),
        ("formal",                   "Formal"),
        ("sport",                    "Sport"),
        ("music_performance",        "Performance"),
        ("work_uniform_compatible",  "Work"),
        ("accessory",                "Accessory"),
    ]

    # Slot defaults — the $0 item that occupies a slot when nothing is equipped.
    SLOT_DEFAULT_ITEM = {
        ("workspace", "chair"):        "kitchen_chair",
        ("bedroom", "bed"):            "basic_bed",
        ("bedroom", "lighting"):       "bare_bulb",
        ("kitchen", "appliance_major"): "basic_stove",
        ("kitchen", "cookware"):       "basic_pots",
    }
    WARDROBE_DEFAULT_ITEM = {"casual": "basic_casual"}

    # Labels for the Phase 62 modifier keys that Phase 61 does not know about.
    # (Phase 61 keys stay in EFFECT_LABELS in equipment.rpy.)
    HOME_EFFECT_LABELS = {
        "sleep_recovery":        "Sleep recovery",
        "home_social":           "Home social quality",
        "morning_energy":        "Morning energy",
        "summer_energy_drain":   "Hot-day energy loss",
        "work_session_minutes":  "Focus before fatigue",
        "recipe_difficulty_max": "Max recipe difficulty",
        "confidence":            "Confidence",
        "art_quality_modifier":  "Art quality",
    }
    # Fractional keys render as percentages; everything else as points.
    _HOME_FRAC_KEYS = {"sleep_recovery", "summer_energy_drain",
                       "music_energy", "project_energy", "prog_xp", "cook_time",
                       "art_quality_modifier"}
    # Keys where the value is a ceiling/threshold, not something to add up.
    _HOME_MAX_KEYS = {"recipe_difficulty_max"}

    # Independent caps for Phase 62-only keys (Phase 61 keys use its own caps).
    _HOME_CAPS = {
        "sleep_recovery":       0.25,
        "home_social":          30,
        "morning_energy":       10,
        "summer_energy_drain":  0.10,
        "work_session_minutes": 45,
        "confidence":           8,
        # studio easel (0.09) + supply kit (0.04) = 0.13. The cap leaves headroom
        # for one future item without letting gear outweigh skill: painting.rpy
        # converts this to roll points at x100, so 0.15 is +15 max, vs +25 skill.
        "art_quality_modifier": 0.15,
    }


init python:

    # ── Ownership (delegates to Phase 61 inventory) ──────────────────────────
    def owns_item(item_id):
        """True if the player owns this catalog item. Free default items are
        always owned; legacy own_* flags satisfy their catalog equivalents."""
        d = ITEM_CATALOG.get(item_id)
        if not d:
            return False
        if d["price_new"] == 0:
            return True
        if item_id in store.owned_equipment:
            return True
        return item_id in _LEGACY_ITEM_FLAGS and getattr(store, _LEGACY_ITEM_FLAGS[item_id], False)

    # An owned legacy flag also grants the equivalent catalog item, so players
    # mid-save are not silently downgraded by this phase.
    _LEGACY_ITEM_FLAGS = {
        "old_acoustic":    "own_guitar",
        "coffee_maker":    "own_coffee_machine",
        "quality_cookware": "own_kitchen_set",
        "double_bed":      "own_bed",
        "basic_laptop":    "own_computer",
        # Phase 45 marketplace flag item; Phase 65 gives it a use.
        "sketchbook":      "own_sketchbook",
    }

    def owned_home_items():
        """Every catalog item the player owns (excluding free defaults)."""
        return [i for i in ITEM_CATALOG if i not in _FREE_ITEMS and owns_item(i)]

    _FREE_ITEMS = set()

    def grant_item(item_id, condition="Good"):
        """Buy/receive an item. Reuses the Phase 61 inventory + condition map."""
        if item_id not in ITEM_CATALOG:
            return False
        grant_equipment(item_id, condition)
        if store.savings_target == item_id:
            store.savings_target = None
        return True

    def item_condition(item_id):
        return store.equipment_condition.get(item_id, "Good")

    # ── Slots ────────────────────────────────────────────────────────────────
    def equipped_in(room, slot):
        """Item id active in a slot: explicit choice, else the free default."""
        chosen = store.home_slots.get(room, {}).get(slot)
        if chosen and owns_item(chosen):
            return chosen
        return SLOT_DEFAULT_ITEM.get((room, slot))

    def equip_item(item_id):
        """Put an owned item into its slot. Returns True on success."""
        d = ITEM_CATALOG.get(item_id)
        if not d or not d["slot"] or not owns_item(item_id):
            return False
        if d["category"] == "wardrobe":
            w = dict(store.wardrobe_equipped)
            w[d["slot"]] = item_id
            store.wardrobe_equipped = w
            return True
        room = _room_for_item(item_id)
        if not room:
            return False
        hs = dict(store.home_slots)
        rooms = dict(hs.get(room, {}))
        rooms[d["slot"]] = item_id
        hs[room] = rooms
        store.home_slots = hs
        return True

    def _room_for_item(item_id):
        d = ITEM_CATALOG.get(item_id)
        if not d or not d["slot"]:
            return None
        cat = d["category"]
        if cat == "music":
            return "music_corner"
        if cat in HOME_ROOM_SLOTS:
            return cat
        return None

    def item_room_slot(item_id):
        """(room, slot) this item occupies, or (None, None) for lifestyle items."""
        d = ITEM_CATALOG.get(item_id)
        if not d or not d["slot"]:
            return (None, None)
        if d["category"] == "wardrobe":
            return ("wardrobe", d["slot"])
        return (_room_for_item(item_id), d["slot"])

    def is_equipped(item_id):
        room, slot = item_room_slot(item_id)
        if room is None:
            return False
        if room == "wardrobe":
            return store.wardrobe_equipped.get(slot) == item_id
        return equipped_in(room, slot) == item_id

    def all_equipped_items():
        """Every actively-equipped item id (rooms + wardrobe + lifestyle owned)."""
        out = []
        for room, _lbl, slots in HOME_ROOMS:
            for slot in slots:
                iid = equipped_in(room, slot)
                if iid:
                    out.append(iid)
        for cat, _lbl in WARDROBE_CATEGORIES:
            iid = store.wardrobe_equipped.get(cat) or WARDROBE_DEFAULT_ITEM.get(cat)
            if iid:
                out.append(iid)
        # lifestyle items have no slot — owning one is equipping it
        out.extend(i for i, d in ITEM_CATALOG.items()
                   if d["category"] == "lifestyle" and owns_item(i))
        return out

    # ── Modifiers ────────────────────────────────────────────────────────────
    def _cond_factor(item_id):
        return _EQUIP_CONDITION_FACTOR.get(item_condition(item_id), 0.9)

    def _raw_home_effect(item_id, key):
        """One item's contribution to a key, scaled by its condition."""
        d = ITEM_CATALOG.get(item_id)
        if not d:
            return 0
        raw = d["modifiers"].get(key, 0)
        if not raw:
            return 0
        if key in _HOME_MAX_KEYS:
            return raw          # thresholds are not condition-scaled
        return raw * _cond_factor(item_id)

    def home_modifier(key, room=None):
        """Total capped modifier for a Phase 62 key across equipped items.
        `room` restricts the sum to one room. Fractional keys return float,
        point keys return int, _HOME_MAX_KEYS return the best single value."""
        if room is not None:
            items = [equipped_in(room, s) for s in HOME_ROOM_SLOTS.get(room, [])]
            items = [i for i in items if i]
        else:
            items = all_equipped_items()
        if key in _HOME_MAX_KEYS:
            best = 0
            for iid in items:
                best = max(best, _raw_home_effect(iid, key))
            return int(best)
        total = sum(_raw_home_effect(iid, key) for iid in items)
        cap = _HOME_CAPS.get(key, _EQUIP_FRAC_CAP if key in _HOME_FRAC_KEYS else _EQUIP_POINT_CAP)
        total = min(cap, total)
        return float(total) if key in _HOME_FRAC_KEYS else int(round(total))

    # ── Phase 62 gameplay helpers ────────────────────────────────────────────
    def sleep_recovery_modifier():
        """Fractional bonus to morning energy recovery from bedroom gear.
        Capped at +25% (spec §8). Blackout curtains pay off after a late night."""
        val = home_modifier("sleep_recovery", room="bedroom")
        if _slept_late() and equipped_in("bedroom", "lighting") == "blackout_curtains":
            val += 0.04
        return min(_HOME_CAPS["sleep_recovery"], val)

    def _slept_late():
        """True if the player was still up after 2am (hour wraps past 24)."""
        return store.hour >= 26 or store.hour < 6

    def home_social_quality():
        """0-30 score driving the quality of home-based social activities.
        Living room is the core; a few other items contribute politely."""
        return home_modifier("home_social")

    def home_social_tier():
        """0-3 bucket used by home visits. 0 = no bonus."""
        q = home_social_quality()
        if q >= 21: return 3
        if q >= 13: return 2
        if q >= 6:  return 1
        return 0

    def home_social_bonus():
        """Relationship-gain bonus applied to home visits. Small by design."""
        return (0, 1, 2, 3)[home_social_tier()]

    def home_visual_tier():
        """0-4 overall look of the flat. Pure flavour — never gates an action."""
        return max(0, min(4, int(home_visual_score() + 0.35)))

    def home_visual_score():
        """Continuous 0-4 look score behind home_visual_tier(). Bedroom and
        living room dominate; lifestyle items add up to a full tier."""
        weighted, weight = 0.0, 0.0
        for room, _lbl, slots in HOME_ROOMS:
            # Bedroom and living room ARE the look of the flat; the working
            # rooms count, but a bare workshop should not cap a nice home at 2.
            w = 3.0 if room in ("bedroom", "living_room") else 0.75
            for slot in slots:
                iid = equipped_in(room, slot)
                weighted += w * (ITEM_CATALOG[iid]["visual_tier"] if iid else 0)
                weight += w
        avg = weighted / weight if weight else 0.0
        # Lifestyle items are decoration by definition and are the main reason
        # a stat-free purchase is still worth making: a fully decorated flat is
        # worth a whole tier on its own (capped, so furniture still matters).
        lifestyle = sum(1 for i, d in ITEM_CATALOG.items()
                        if d["category"] == "lifestyle" and owns_item(i))
        avg += min(1.0, lifestyle * 0.15)
        # Phase 65: your own work on the walls. Worth more per piece than a
        # bought lifestyle item (0.5 vs 0.15) but capped at one tier total, so
        # hanging twenty paintings is not a substitute for furniture.
        # Read defensively: this file is exec'd standalone by the Phase 62
        # self-check harness, where painting.rpy's defaults do not exist.
        avg += min(1.0, len([a for a in getattr(store, "player_artworks", [])
                             if a.get("displayed")]) * 0.5)
        return max(0.0, min(4.0, avg))

    HOME_VISUAL_FLAVOR = [
        "The apartment is almost empty. Your stuff fits in two bags.",
        "It's functional. Not much else.",
        "It's starting to feel like somewhere you actually live.",
        "Your apartment has a particular feel to it now.",
        "It's a genuinely comfortable place. You notice it when you come home.",
    ]

    def home_visual_text():
        return HOME_VISUAL_FLAVOR[home_visual_tier()]

    def check_home_ambient():
        """Once-per-day ambient line about the flat. Sets _p62_home_flavor and
        returns True when it should be shown. Also re-fires immediately after the
        look of the place changes, so upgrades are acknowledged."""
        tier = home_visual_tier()
        if store._home_ambient_day == store.day and store._home_ambient_tier == tier:
            return False
        store._home_ambient_day = store.day
        store._home_ambient_tier = tier
        store._p62_home_flavor = home_visual_text()
        return True

    def workspace_quality():
        """0-8 desk+computer score used as a small study/focus modifier."""
        total = 0
        for slot in ("desk", "computer"):
            iid = equipped_in("workspace", slot)
            if iid:
                total += ITEM_CATALOG[iid]["visual_tier"]
        return total

    def study_focus_modifier():
        """Small focus bonus for studying at a real workspace (0-4 points)."""
        return min(4, workspace_quality() // 2)

    # ── Morning routine items ────────────────────────────────────────────────
    def morning_item():
        """The best equipped morning drink item, or None."""
        iid = equipped_in("kitchen", "appliance_small")
        if iid and ITEM_CATALOG[iid]["modifiers"].get("morning_energy"):
            return iid
        return None

    def morning_item_available():
        """Usable now? Once per day, before noon, item equipped."""
        return (morning_item() is not None
                and store._morning_item_used != store.day
                and store.hour < 12)

    def use_morning_item():
        """Apply the once-per-day morning energy bonus. Returns (label, gain)."""
        iid = morning_item()
        if not iid or store._morning_item_used == store.day:
            return None
        gain = int(round(ITEM_CATALOG[iid]["modifiers"]["morning_energy"] * _cond_factor(iid)))
        gain = min(_HOME_CAPS["morning_energy"], gain)
        store.need_energy = min(100, store.need_energy + gain)
        store._morning_item_used = store.day
        return (ITEM_CATALOG[iid]["label"], gain)

    # ── Guitar strings consumable ────────────────────────────────────────────
    GUITAR_STRINGS_COST = 12

    def strings_age():
        """Days since the strings were last changed (large if never)."""
        return store.day - store.guitar_strings_last_refreshed

    def strings_modifier():
        """+4 fresh (within 7 days), -3 stale, 0 if the player never engaged."""
        if store.guitar_strings_last_refreshed < 0:
            return 0
        return 4 if strings_age() <= 7 else -3

    def strings_state_text():
        if store.guitar_strings_last_refreshed < 0:
            return "Strings: original set."
        a = strings_age()
        if a <= 7:
            return "Strings: fresh (%d day%s ago). +4 performance." % (a, "" if a == 1 else "s")
        return "Strings: worn (%d days old). -3 performance." % a

    def can_refresh_strings():
        return store.money >= GUITAR_STRINGS_COST and (
            equipped_in("music_corner", "instrument") is not None or store.own_guitar)

    def refresh_strings():
        if not try_spend(GUITAR_STRINGS_COST, "discretionary"):
            return False
        store.guitar_strings_last_refreshed = store.day
        return True

    def _refresh_strings_wrapper():
        """Function() wrapper — returns None."""
        refresh_strings()

    # ── Wardrobe ─────────────────────────────────────────────────────────────
    def wardrobe_equipped_in(category):
        return store.wardrobe_equipped.get(category) or WARDROBE_DEFAULT_ITEM.get(category)

    def dressed_for(context):
        """Soft contextual check. Returns points: +N if appropriately dressed,
        a small penalty if clearly underdressed. Never a hard block."""
        iid = wardrobe_equipped_in(context)
        if iid:
            return int(round(min(_HOME_CAPS["confidence"],
                                 ITEM_CATALOG[iid]["modifiers"].get("confidence", 0))))
        # nothing in the required category — underdressed, small penalty only
        return -3 if context in ("formal", "music_performance") else 0

    def wardrobe_confidence():
        """Passive confidence from the casual/smart everyday outfit + accessory."""
        total = 0
        for cat in ("casual", "smart_casual", "accessory"):
            iid = wardrobe_equipped_in(cat)
            if iid:
                total += ITEM_CATALOG[iid]["modifiers"].get("confidence", 0)
        return int(min(_HOME_CAPS["confidence"], total))

    # ── Purchasing ───────────────────────────────────────────────────────────
    def item_price(item_id, used=False):
        d = ITEM_CATALOG.get(item_id)
        if not d:
            return 0
        return d["price_used"] if used else d["price_new"]

    def can_buy_item(item_id):
        d = ITEM_CATALOG.get(item_id)
        return bool(d and d["shop_available"] and not owns_item(item_id)
                    and store.money >= d["price_new"])

    def buy_item(item_id):
        """Retail purchase. Returns True on success. Always 'Excellent' new."""
        d = ITEM_CATALOG.get(item_id)
        if not d or owns_item(item_id) or not d["shop_available"]:
            return False
        if not try_spend(d["price_new"], "discretionary"):
            return False
        grant_item(item_id, "Excellent")
        record_game_event("item_buy_%s_day%d" % (item_id, store.day), "purchase",
            "Bought: " + d["label"], summary=True, journal=False,
            metadata={"item": item_id, "price": d["price_new"]})
        return True

    def _buy_item_wrapper(item_id, equip_after=False):
        """Function() wrapper — returns None."""
        if buy_item(item_id) and equip_after:
            equip_item(item_id)

    def _equip_item_wrapper(item_id):
        """Function() wrapper — returns None."""
        equip_item(item_id)

    def _set_savings_target(item_id):
        """Function() wrapper — returns None. Toggles the target off if repeated."""
        store.savings_target = None if store.savings_target == item_id else item_id

    def savings_target_text():
        """Cosmetic phone chip. None when no target is set."""
        t = store.savings_target
        if not t or t not in ITEM_CATALOG:
            return None
        d = ITEM_CATALOG[t]
        return "Saving for: %s ($%d) — you have $%d." % (d["label"], d["price_new"], store.money)

    # ── Modifier preview / delta ─────────────────────────────────────────────
    # Keys where a POSITIVE stored value means "costs less" — they must render
    # with a flipped sign, and a negative delta must read as "+N%" (a cost going
    # back up), not "-N%". Getting this wrong makes downgrades look like upgrades.
    _HOME_INVERSE_KEYS = {"project_energy", "music_energy", "cook_time",
                          "summer_energy_drain"}

    def format_modifier(key, value):
        """Human-readable single modifier value. Handles deltas (which may be
        negative) as well as absolute values."""
        label = HOME_EFFECT_LABELS.get(key) or EFFECT_LABELS.get(key, key)
        if key in _HOME_MAX_KEYS:
            return (label, "%d" % value)
        if key in _HOME_FRAC_KEYS:
            pct = int(round(value * 100))
            if key in _HOME_INVERSE_KEYS:
                pct = -pct
            return (label, "%+d%%" % pct)
        return (label, "%+d" % value)

    def item_modifier_lines(item_id):
        """[(label, value_str)] for an item at its stored condition (Good if it
        is not owned yet — the same number a shop-new 'Excellent' would beat)."""
        d = ITEM_CATALOG.get(item_id)
        if not d:
            return []
        return [format_modifier(k, _raw_home_effect(item_id, k)) for k in sorted(d["modifiers"])]

    def equip_delta(item_id):
        """[(label, delta_str)] comparing item_id against the slot's current
        occupant. Uses _raw_home_effect — exactly the numbers the live modifiers
        use — so the preview and the post-equip value cannot disagree."""
        room, slot = item_room_slot(item_id)
        if room is None:
            return []
        cur = wardrobe_equipped_in(slot) if room == "wardrobe" else equipped_in(room, slot)
        if cur == item_id:
            return []
        keys = set(ITEM_CATALOG[item_id]["modifiers"])
        if cur:
            keys |= set(ITEM_CATALOG[cur]["modifiers"])
        out = []
        for k in sorted(keys):
            new_v = _raw_home_effect(item_id, k)
            old_v = _raw_home_effect(cur, k) if cur else 0
            delta = (max(new_v, old_v) - old_v) if k in _HOME_MAX_KEYS else (new_v - old_v)
            if abs(delta) < 0.005:
                continue
            out.append(format_modifier(k, delta))
        return out

    # The marketplace previews an item at a hypothetical condition; same maths.
    equip_delta_at_condition = equip_delta

    def current_slot_occupant_label(item_id):
        room, slot = item_room_slot(item_id)
        if room is None:
            return None
        cur = wardrobe_equipped_in(slot) if room == "wardrobe" else equipped_in(room, slot)
        return ITEM_CATALOG[cur]["label"] if cur else "Nothing"

    # ── Shop browsing helpers ────────────────────────────────────────────────
    SHOP_CATEGORIES = [
        ("bedroom",     "Bedroom"),
        ("workspace",   "Workspace"),
        ("kitchen",     "Kitchen"),
        ("music",       "Music"),
        ("workshop",    "Workshop"),
        ("living_room", "Living Room"),
        ("studio",      "Studio"),
        ("lifestyle",   "Lifestyle"),
        ("wardrobe",    "Wardrobe"),
    ]

    def shop_items(category):
        """Catalog items in a category, cheapest first."""
        return sorted((i for i, d in ITEM_CATALOG.items()
                       if d["category"] == category and d["shop_available"]),
                      key=lambda i: ITEM_CATALOG[i]["price_new"])

    def affordable_item_count():
        """How many unowned shop items the player could buy right now."""
        return sum(1 for i in ITEM_CATALOG if can_buy_item(i))


# Populate the free-item set once the catalog exists.
init 1 python:
    _FREE_ITEMS = {i for i, d in ITEM_CATALOG.items() if d["price_new"] == 0}
