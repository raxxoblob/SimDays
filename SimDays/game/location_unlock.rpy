# Location unlock system — tracks which locations the player has access to.
# All default locations start unlocked. Future locations require specific gates.

init python:

    LOCATION_DEFS = {
        "location_home":     {"display_name": "Home",              "unlocked_by_default": True},
        "location_bar":      {"display_name": "Static (Bar)",      "unlocked_by_default": True},
        "location_cafe":     {"display_name": "Café",              "unlocked_by_default": True},
        "location_park":     {"display_name": "Park",              "unlocked_by_default": True},
        "location_gym":      {"display_name": "Iron Gate Gym",     "unlocked_by_default": True},
        "location_hub":      {"display_name": "The Hub",           "unlocked_by_default": True},
        "location_library":  {"display_name": "Library",           "unlocked_by_default": True},
        "location_hospital": {"display_name": "City Hospital",     "unlocked_by_default": True},
        "location_office":   {"display_name": "Nexus Tower",       "unlocked_by_default": True},
        "location_kitchen":  {"display_name": "Eleven (Kitchen)",  "unlocked_by_default": True},
        "location_sandbeach": {"display_name": "Sandy Beach",      "unlocked_by_default": True},
        "location_nightclub": {"display_name": "Neon",             "unlocked_by_default": True},
        "location_warehouse": {"display_name": "Warehouse",        "unlocked_by_default": True},
        "location_diner":     {"display_name": "Late-Night Diner", "unlocked_by_default": True},
        "location_college":   {"display_name": "College",          "unlocked_by_default": True},
        "future_gallery":    {"display_name": "Gallery",           "unlocked_by_default": False,
                              "unlock_hint": "Build a name in the local art scene."},
        # Private NPC home locations — not travelable by default
        "loc_nora_apt":      {"display_name": "Nora's Apartment",    "unlocked_by_default": False, "private": True},
        "loc_marcus_apt":    {"display_name": "Marcus's Apartment",  "unlocked_by_default": False, "private": True},
        "loc_zoe_studio":    {"display_name": "Zoe's Studio",        "unlocked_by_default": False, "private": True},
        "loc_eli_dorm":      {"display_name": "Eli's Dorm",          "unlocked_by_default": False, "private": True},
        "loc_sam_house":     {"display_name": "Sam's House",         "unlocked_by_default": False, "private": True},
        "loc_lena_apt":      {"display_name": "Lena's Apartment",    "unlocked_by_default": False, "private": True},
        "loc_natalie_house": {"display_name": "Natalie's House",     "unlocked_by_default": False, "private": True},
        "loc_kai_apt":       {"display_name": "Kai's Apartment",     "unlocked_by_default": False, "private": True},
        "loc_martha_apt":    {"display_name": "Martha's Apartment",  "unlocked_by_default": False, "private": True},
        "loc_caroline_apt":  {"display_name": "Caroline's Apartment","unlocked_by_default": False, "private": True},
        "loc_rena_place":    {"display_name": "Rena's Place",        "unlocked_by_default": False, "private": True},
        "loc_elle_apt":      {"display_name": "Elle's Apartment",    "unlocked_by_default": False, "private": True},
        "loc_julia_apt":     {"display_name": "Julia's Apartment",   "unlocked_by_default": False, "private": True},
    }

    def ensure_default_locations_unlocked():
        changed = False
        current = list(store.unlocked_locations)
        for lid, d in LOCATION_DEFS.items():
            if d.get("unlocked_by_default") and lid not in current:
                current.append(lid)
                changed = True
        if changed:
            store.unlocked_locations = current

    def is_location_unlocked(lid):
        ensure_default_locations_unlocked()
        return lid in store.unlocked_locations

    def unlock_location(lid, source_id=""):
        if lid not in store.unlocked_locations:
            store.unlocked_locations = list(store.unlocked_locations) + [lid]
            d = LOCATION_DEFS.get(lid, {})
            record_game_event("unlock_" + lid, "journal",
                "Discovered: " + d.get("display_name", lid),
                journal=True, summary=True,
                metadata={"location": lid, "source": source_id})
            renpy.notify("New location: " + d.get("display_name", lid))
