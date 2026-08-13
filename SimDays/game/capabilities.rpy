# Phase 65 — Capability layer + NPC interest registry.
#
# Two small, phase-agnostic registries that future hobby phases build on.
#
# 1. has_home_capability(cap_id)
#    The ONLY question a home menu should ask before offering a hobby action.
#    "Can I paint here?" — not "do I own basic_easel or studio_easel or ...".
#    Capabilities live on ITEM_CATALOG entries (see the `caps` argument to
#    _item() in home_items.rpy). Adding a third easel tier later needs no
#    change here and no change in locations.rpy.
#
# 2. NPC_INTERESTS
#    How much each NPC cares about each hobby domain, 0-3. Phase 65 only reads
#    the "art" column (gifting, home-visit comments). The other columns are
#    populated now — from the same dialogue audit — so Phase 66+ does not have
#    to re-derive them.
#
# init priority 1: ITEM_CATALOG is built at init -1 in home_items.rpy, and the
# lifestyle-ownership path calls owns_item() from its init python block.

init 1 python:

    def has_home_capability(cap_id):
        """True if the player currently has equipment/upgrades that enable this
        capability at home.

        Any catalog item listing `cap_id` in its capabilities grants it, provided
        the item is ACTIVE: slotted items must be equipped in their slot,
        lifestyle items (no slot) only need to be owned.

        Capabilities overlap freely — studio_easel grants both "painting" and
        "professional_painting"."""
        for item_id in _CAPABILITY_ITEMS.get(cap_id, ()):
            d = ITEM_CATALOG.get(item_id)
            if not d:
                continue
            if d["slot"] is None:
                if owns_item(item_id):
                    return True
            elif is_equipped(item_id):
                return True
        return False

    def home_capabilities():
        """Every capability currently active. Debug/inspection only."""
        return sorted(c for c in _CAPABILITY_ITEMS if has_home_capability(c))

    def capability_sources(cap_id):
        """Every item that could grant this capability. Debug/shop hints."""
        return list(_CAPABILITY_ITEMS.get(cap_id, ()))

    # Reverse index cap_id -> [item_id, ...], built once from the catalog.
    # ponytail: built at init, so a mod adding items at runtime would need to
    # rebuild it. Nothing does that today; rebuild in grant_item() if it ever does.
    _CAPABILITY_ITEMS = {}
    for _iid, _d in ITEM_CATALOG.items():
        for _cap in _d.get("capabilities", ()):
            _CAPABILITY_ITEMS.setdefault(_cap, []).append(_iid)


    # ── NPC interests ────────────────────────────────────────────────────────
    # Derived from an audit of existing dialogue, scene labels, schedules and
    # the NPC_DATA likes/dislikes table. NOT invented. Provenance per entry.
    #
    #  0 = no interest / no evidence      2 = likes it, has dialogue about it
    #  1 = casual, listed affinity only   3 = passion, it is part of who they are
    # -1 = explicit dislike in NPC_DATA["dislikes"] (Marcus/art is the only one
    #      relevant to Phase 65). Kept distinct from 0 so gifting a painting to
    #      someone who has stated they dislike art reads differently from
    #      gifting to someone who simply has no opinion.
    NPC_INTERESTS = {
        # Barista -> culinary programme. Food is her whole arc. Eligible for the
        # play_music home visit but has no music dialogue, so music is casual.
        "nora":   {"art": 0, "music": 1, "fitness": 0, "programming": 0, "cooking": 3, "mechanics": 0},
        # Runs the park loop daily, semi-pro basketball offer at 18. Cooks one
        # thing properly (chili, mom's recipe). Fixes the Static speaker (mech).
        # NPC_DATA lists "art" under dislikes.
        "marcus": {"art": -1, "music": 1, "fitness": 3, "programming": 0, "cooking": 2, "mechanics": 2},
        # Art student, 4-stage gallery arc. Used to play bass "for years".
        # Her laptop defeats her — programming is a weakness, not an interest.
        "zoe":    {"art": 3, "music": 2, "fitness": 0, "programming": 0, "cooking": 0, "mechanics": 0},
        # Senior developer + side projects on breadboards. Dislikes sports.
        # Music is a listed like with no supporting dialogue.
        "eli":    {"art": 0, "music": 1, "fitness": 0, "programming": 3, "cooking": 0, "mechanics": 1},
        # Gym staff. Consistency is her entire character note. "food" is a listed
        # like with no cooking dialogue anywhere, so it stays casual.
        "sam":    {"art": 0, "music": 0, "fitness": 3, "programming": 0, "cooking": 1, "mechanics": 0},
        # Marine researcher. art/music/travel are listed likes with ZERO
        # supporting dialogue — casual, not passion. Deliberately not a 2.
        "elle":   {"art": 1, "music": 1, "fitness": 0, "programming": 0, "cooking": 0, "mechanics": 0},
        # Hospital doctor. "food" listed; two scenes happen to be set in a
        # kitchen but state no culinary interest.
        "lena":   {"art": 0, "music": 0, "fitness": 0, "programming": 0, "cooking": 1, "mechanics": 0},
        # Head chef, culinary mentor. Walked out of an investment-firm job after
        # one real service — actively anti-desk-work.
        "rena":   {"art": 0, "music": 0, "fitness": 0, "programming": 0, "cooking": 3, "mechanics": 0},
        # Corporate mentor. No lines touching any of the six domains.
        # Dislikes sports. Genuinely domain-empty — 0 across the board is the
        # honest reading, not a gap to be filled in later.
        "martha": {"art": 0, "music": 0, "fitness": 0, "programming": 0, "cooking": 0, "mechanics": 0},
    }

    def npc_interest(npc_id, domain):
        """-1..3. Unknown NPC or domain reads as 0 (no interest)."""
        return NPC_INTERESTS.get(npc_id, {}).get(domain, 0)

    def npcs_interested_in(domain, minimum=2):
        return [n for n in NPC_INTERESTS if npc_interest(n, domain) >= minimum]
