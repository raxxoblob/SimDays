# Phase 69 — Possessions, personal bests, accomplishments.
#
# DESIGN NOTE (read before extending):
#   This phase does NOT rebuild ownership and it does NOT build a second
#   opportunity/event generator. Three stores already exist and stay canonical:
#
#     owned_equipment / equipment_condition (Phase 61)  — gear you can equip.
#         Read through owns_item() / owned_home_items() / equipment.rpy.
#     player_artworks (Phase 65)                        — paintings you made.
#     player_possessions (THIS PHASE)                   — keepsakes/collectibles:
#         objects that record a moment and have no slot, no condition and no
#         modifier. Nothing else belongs here. The Possessions app READS the
#         other two; it never copies them.
#
#   Likewise, "opportunities" already exist: CITY_CHALLENGE_TEMPLATES (Phase 61)
#   are scheduled by the city-event generator, discovered at locations/Social,
#   previewed with real odds and resolved with the Phase 60 roll engine. A
#   parallel OPPORTUNITY_TEMPLATES table would have duplicated cook-off,
#   fitness, coding, art-exhibition, showcase and networking verbatim. What was
#   actually missing is ANTICIPATION and AFTERMATH, so this file adds:
#     - preparation modifiers (rest / recent practice) folded into the ONE
#       modifier list city challenges already share between preview and roll,
#     - keepsakes, personal bests and accomplishments on the way out,
#     - a takeaway line when you don't place.
#
#   Wiring is done by wrapping the existing functions at init 20 rather than
#   editing eight files. Phase 66/67/68 are being written concurrently in
#   city_challenges.rpy / world_challenges.rpy / data.rpy; wrapping keeps this
#   phase out of their diffs entirely.
#
# ponytail: featured is a data flag only. Home backgrounds are static art, so a
#   featured trophy cannot appear on a shelf. Upgrade path: when per-room
#   composited home art exists, read get_featured_possessions() from there.

default player_possessions    = []   # list of possession instance dicts
default player_personal_bests = {}   # key -> best value seen
default player_accomplishments = []  # list of milestone dicts
default _possession_seq       = 0    # instance id counter
default _p69_last_practice    = {}   # skill key -> day last practised
default _p69_synced_day       = -1   # last day the derived-award sync ran (-1 = never)
default _possessions_tab      = "keepsakes"
default _selected_possession  = None


init python:

    # ── Catalog ──────────────────────────────────────────────────────────────
    # unique=True  -> at most one instance, ever.
    # unique=False -> one instance per distinct `source` (see grant_possession).
    POSSESSION_CATALOG = {
        "pool_trophy": {
            "name": "Downtown Pool Trophy", "category": "keepsake",
            "description": "First place against The Professor at Static.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_trophy", "tags": ["bar", "competition", "first"],
            "hint": "Beat The Professor at pool.",
        },
        "darts_trophy": {
            "name": "Friday Darts Cup", "category": "keepsake",
            "description": "You took the Friday board off the champion.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_trophy", "tags": ["bar", "competition"],
            "hint": "Beat the Friday Champion at darts.",
        },
        "cookoff_medal": {
            "name": "Cook-Off Medal", "category": "keepsake",
            "description": "A placement at the park food fair.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_medal", "tags": ["cooking", "competition"],
            "hint": "Place at the Local Cook-Off.",
        },
        "coding_challenge_plaque": {
            "name": "Coding Challenge Plaque", "category": "keepsake",
            "description": "Handed out at the library contest. Slightly crooked.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_plaque", "tags": ["programming", "competition"],
            "hint": "Place at the Public Coding Challenge.",
        },
        "gallery_ribbon": {
            "name": "Gallery Exhibition Ribbon", "category": "keepsake",
            "description": "Your name on the card by the door.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_ribbon", "tags": ["art", "exhibition"],
            "hint": "Place at the Local Art Exhibition.",
        },
        "gym_challenge_medal": {
            "name": "Fitness Challenge Medal", "category": "keepsake",
            "description": "Cheap metal, heavier than it looks.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_medal", "tags": ["fitness", "competition"],
            "hint": "Place at the Amateur Fitness Challenge.",
        },
        "first_paid_gig_stub": {
            "name": "First Paid Gig Stub", "category": "keepsake",
            "description": "The stub from the night the room actually listened.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_ticket", "tags": ["music", "milestone"],
            "hint": "Land a great open mic performance.",
        },
        "mechanics_restoration_badge": {
            "name": "Restoration Badge", "category": "keepsake",
            "description": "For a repair that came back better than new.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_badge", "tags": ["mechanics", "milestone"],
            "hint": "Finish a repair with a critical success.",
        },
        "freelance_client_card": {
            "name": "Client Thank-You Card", "category": "keepsake",
            "description": "A short handwritten note from a client you did right by.",
            "unique": False, "sellable": False, "giftable": False,
            "icon_key": "keepsake_card", "tags": ["freelance", "professional"],
            "hint": "Deliver a project rated S.",
        },
        "musician_contact_card": {
            "name": "Kaz's Number", "category": "keepsake",
            "description": "Written on the back of a setlist. Another player, "
                           "same corner, most weekends.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_card", "tags": ["music", "opportunity", "rare"],
            "hint": "Busk well enough that another player waits for you to finish.",
        },
        "art_market_vendor_card": {
            "name": "Gallery Contact Card", "category": "keepsake",
            "description": "Someone at the gallery wants to see more.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_card", "tags": ["art", "opportunity"],
            "hint": "Reach art reputation 25.",
        },
        "festival_wristband": {
            "name": "Festival Wristband", "category": "keepsake",
            "description": "You never cut it off. It's fine.",
            "unique": False, "sellable": False, "giftable": False,
            "icon_key": "keepsake_wristband", "tags": ["event", "community"],
            "hint": "Attend a city event.",
        },
        "promotion_certificate": {
            "name": "Promotion Certificate", "category": "keepsake",
            "description": "Printed on paper that is trying very hard to be card.",
            "unique": False, "sellable": False, "giftable": False,
            "icon_key": "keepsake_certificate", "tags": ["career", "milestone"],
            "hint": "Earn a promotion.",
        },
        "networking_lanyard": {
            "name": "Pitch Night Lanyard", "category": "keepsake",
            "description": "Your name, misspelled, in a plastic sleeve.",
            "unique": True, "sellable": False, "giftable": False,
            "icon_key": "keepsake_card", "tags": ["career", "competition"],
            "hint": "Place at the Pitch & Network Evening.",
        },
        "rare_vintage_coin": {
            "name": "Old City Coin", "category": "collectible",
            "description": "Pre-decimal, worn smooth. Someone would pay for this.",
            "unique": True, "sellable": True, "sell_value": 45,
            "icon_key": "collectible_coin", "tags": ["rare", "world"],
            "hint": "Turn up somewhere lucky.",
        },
        "trivia_night_mug": {
            "name": "Quiz Night Mug", "category": "collectible",
            "description": "The prize nobody wants and everybody keeps.",
            "unique": True, "sellable": True, "sell_value": 8,
            "icon_key": "collectible_coin", "tags": ["bar", "competition"],
            "hint": "Place at Pub Trivia Night.",
        },
    }

    # ── Icons ────────────────────────────────────────────────────────────────
    # Design-ready slots. None of these assets ship yet; possession_icon()
    # returns None when nothing is loadable and the UI draws a colour swatch.
    POSSESSION_ICONS = {
        "keepsake_trophy":      "images/ui/items/trophy.png",
        "keepsake_medal":       "images/ui/items/medal.png",
        "keepsake_ribbon":      "images/ui/items/ribbon.png",
        "keepsake_plaque":      "images/ui/items/plaque.png",
        "keepsake_ticket":      "images/ui/items/ticket.png",
        "keepsake_badge":       "images/ui/items/badge.png",
        "keepsake_card":        "images/ui/items/card.png",
        "keepsake_wristband":   "images/ui/items/wristband.png",
        "keepsake_certificate": "images/ui/items/certificate.png",
        "collectible_coin":     "images/ui/items/coin.png",
        "_fallback":            "images/ui/items/generic_keepsake.png",
    }

    POSSESSION_CATEGORY_COLOR = {
        "keepsake":    "#ffd66a",
        "collectible": "#5bcafa",
        "artwork":     "#c07ee6",
        "gear":        "#7fd06a",
        "gift":        "#f2765f",
    }

    def possession_icon(icon_key):
        """Icon path, or None when neither the icon nor the fallback exists.
        Callers must handle None — the art is not in the repo yet."""
        for path in (POSSESSION_ICONS.get(icon_key), POSSESSION_ICONS["_fallback"]):
            if path and renpy.loadable(path):
                return path
        return None

    # ── Core helpers ─────────────────────────────────────────────────────────
    def grant_possession(item_id, source, meta=None, force=False, silent=False):
        """Award a possession. Returns True if a new instance was created.

        unique=True  items are granted at most once, ever.
        unique=False items are granted at most once per distinct `source`, so
        'a card from every S-rated client' works without a per-caller guard."""
        cat = POSSESSION_CATALOG.get(item_id)
        if cat is None:
            if renpy.config.developer:
                renpy.log("grant_possession: unknown item_id %r" % (item_id,))
            return False
        if not force:
            if cat.get("unique", False):
                if has_possession(item_id):
                    return False
            elif any(p["item_id"] == item_id and p.get("acquired_source") == source
                     for p in store.player_possessions):
                return False
        store._possession_seq += 1
        store.player_possessions = list(store.player_possessions) + [{
            "id": "poss_%03d_%s" % (store._possession_seq, item_id),
            "item_id": item_id,
            "acquired_day": store.day,
            "acquired_source": source,
            "category": cat.get("category", "keepsake"),
            "featured": False,
            "meta": dict(meta or {}),
        }]
        if not silent:
            record_game_event("poss_%s_%s" % (item_id, source), "event",
                              "Kept: " + cat.get("name", item_id),
                              summary=True, journal=False,
                              metadata={"item_id": item_id, "source": source})
        return True

    def has_possession(item_id):
        return any(p["item_id"] == item_id for p in store.player_possessions)

    def possession_by_id(instance_id):
        return next((p for p in store.player_possessions if p["id"] == instance_id), None)

    def get_possessions_by_category(category):
        return [p for p in store.player_possessions if p.get("category") == category]

    def possession_name(item_id):
        return POSSESSION_CATALOG.get(item_id, {}).get("name", item_id)

    def _write_possessions(items):
        """Possessions live in a plain list of dicts. Rewrite the whole list so
        Ren'Py's rollback/save machinery sees the change (same rule as
        update_artwork in painting.rpy)."""
        store.player_possessions = [dict(p) for p in items]

    def feature_possession(instance_id, featured=True):
        items = [dict(p) for p in store.player_possessions]
        hit = False
        for p in items:
            if p["id"] == instance_id:
                p["featured"] = bool(featured)
                hit = True
        if hit:
            _write_possessions(items)
        return hit

    def get_featured_possessions():
        return [p for p in store.player_possessions if p.get("featured")]

    def sell_possession(instance_id):
        """Sell a sellable, unfeatured possession. Returns cash received, or 0."""
        p = possession_by_id(instance_id)
        if p is None:
            return 0
        cat = POSSESSION_CATALOG.get(p["item_id"], {})
        if not cat.get("sellable") or p.get("featured"):
            return 0
        value = int(cat.get("sell_value", 0))
        store.player_possessions = [q for q in store.player_possessions
                                    if q["id"] != instance_id]
        if value > 0:
            gain_money(value, "discretionary")
        return value

    def unearned_possessions():
        """Catalog entries the player has never earned — the 'anticipation'
        half of the app: what is out there and how you get it."""
        return [(iid, d) for iid, d in sorted(POSSESSION_CATALOG.items())
                if not has_possession(iid)]

    # ── Personal bests ───────────────────────────────────────────────────────
    _PB_TIER_ORDER = ["critical_failure", "weak", "success", "great", "critical"]
    _PB_RATING_ORDER = ["D", "C", "B", "A", "S"]

    PERSONAL_BEST_LABELS = {
        "best_open_mic_tier":            "Best open mic",
        "best_busking_tier":             "Best busking set",
        "highest_busking_tips":          "Highest busking tips",
        "best_artwork_quality":          "Best artwork",
        "best_artwork_estimated_value":  "Most valuable piece",
        "best_freelance_rating":         "Best project rating",
        "highest_pool_opponent_defeated":"Toughest pool opponent",
        "best_cooking_challenge_finish": "Best cook-off finish",
        "best_catering_tier":            "Best catering job",
        "best_repair_tier":              "Best repair",
        "highest_career_rank":           "Highest career rank",
        "best_city_challenge_finish":    "Best competition finish",
        "best_fitness_pb_tier":          "Best gym personal best",
    }

    def _pb_better(value, current, comparison):
        if comparison == "higher":
            return value > current
        if comparison == "lower":
            return value < current
        if comparison == "tier":
            order = _PB_TIER_ORDER
        elif comparison == "rating":
            order = _PB_RATING_ORDER
        else:
            return False
        if value not in order or current not in order:
            return value in order          # unknown current: any known value wins
        return order.index(value) > order.index(current)

    def record_personal_best(key, value, comparison="higher"):
        """Update a personal best if `value` beats the stored one. Returns True
        on a new best. Unknown tier/rating strings are ignored, not crashed on."""
        if value is None:
            return False
        d = dict(store.player_personal_bests)
        current = d.get(key)
        if current is not None and not _pb_better(value, current, comparison):
            return False
        if current is None and comparison in ("tier", "rating"):
            order = _PB_TIER_ORDER if comparison == "tier" else _PB_RATING_ORDER
            if value not in order:
                return False
        d[key] = value
        store.player_personal_bests = d
        return True

    def personal_best_display(key):
        """(label, printable value) or None."""
        if key not in store.player_personal_bests:
            return None
        v = store.player_personal_bests[key]
        if isinstance(v, str) and v in _PB_TIER_ORDER:
            v = tier_label(v)
        elif isinstance(v, int) and key.startswith("highest_") and "tips" in key:
            v = "$%d" % v
        return (PERSONAL_BEST_LABELS.get(key, key.replace("_", " ").title()), str(v))

    # ── Accomplishments ──────────────────────────────────────────────────────
    def record_accomplishment(acc_id, title, description, category, value=None):
        """Structured milestone. Deduplicated on acc_id. Not a Journal entry —
        the Journal is chronological prose, this is a queryable record."""
        if any(a["id"] == acc_id for a in store.player_accomplishments):
            return False
        store.player_accomplishments = list(store.player_accomplishments) + [{
            "id": acc_id, "title": title, "description": description,
            "day": store.day, "category": category, "value": dict(value or {}),
        }]
        return True

    def accomplishments_by_category(category=None):
        if category is None:
            return list(reversed(store.player_accomplishments))
        return [a for a in reversed(store.player_accomplishments)
                if a.get("category") == category]

    # ── Preparation (anticipation layer) ──────────────────────────────────────
    # These fold into _city_chal_mods, which city_challenges.rpy already uses for
    # BOTH the odds preview and the roll. The number shown is the number rolled.
    PREPARATION_BONUSES = {
        "rest_well":       4,   # need_energy >= 70 when you turn up
        "recent_practice": 4,   # practised the event's skill in the last 2 days
    }
    PREP_PRACTICE_WINDOW = 2

    # Cap on repeatable, purely commemorative keepsakes.
    FESTIVAL_WRISTBAND_CAP = 6

    def prep_practiced_recently(skill_key):
        if not skill_key:
            return False
        last = store._p69_last_practice.get(skill_key, -999)
        return 0 <= (store.day - last) <= PREP_PRACTICE_WINDOW

    def preparation_mods(skill_key):
        """Modifier list contributed by preparation. Pure — no side effects."""
        mods = []
        if store.need_energy >= 70:
            mods.append(("Rested", PREPARATION_BONUSES["rest_well"]))
        if prep_practiced_recently(skill_key):
            mods.append(("Recent practice", PREPARATION_BONUSES["recent_practice"]))
        return mods

    def preparation_hints(skill_key):
        """What the player could still do before the event. Used by the app."""
        out = []
        if store.need_energy < 70:
            out.append("Turn up rested (energy 70+) — +%d"
                       % PREPARATION_BONUSES["rest_well"])
        if not prep_practiced_recently(skill_key):
            out.append("Practise in the %d days before — +%d"
                       % (PREP_PRACTICE_WINDOW, PREPARATION_BONUSES["recent_practice"]))
        return out

    # ── Reward tables: which existing result earns which keepsake ─────────────
    # City challenge template id -> keepsake awarded on first placement.
    CITY_CHALLENGE_KEEPSAKES = {
        "cook_off":         "cookoff_medal",
        "fitness_challenge":"gym_challenge_medal",
        "coding_workshop":  "coding_challenge_plaque",
        "art_exhibition":   "gallery_ribbon",
        "music_showcase":   "first_paid_gig_stub",
        "networking_pitch": "networking_lanyard",
        "trivia_night":     "trivia_night_mug",
    }
    # World challenge id -> keepsake awarded on first win.
    WORLD_CHALLENGE_KEEPSAKES = {
        "beat_professor_pool":      "pool_trophy",
        "restore_showpiece":        "mechanics_restoration_badge",
        "first_exhibition_win":     "gallery_ribbon",
        "hard_technical_challenge": "coding_challenge_plaque",
        "signature_dish_master":    "cookoff_medal",
    }
    # Bar-game first-win token -> keepsake (derived, works on old saves too).
    BAR_FIRST_WIN_KEEPSAKES = {
        "professor_pool":  "pool_trophy",
        "darts_champion":  "darts_trophy",
    }
    _POOL_OPPONENT_TIER = {
        "pool_reg_easy": "weak", "pool_marcus": "success",
        "pool_reg_hard": "great", "pool_professor": "critical",
    }

    # Placement tiers that count as "you placed".
    _PLACED_TIERS = ("success", "great", "critical")

    # ── Loss takeaways ───────────────────────────────────────────────────────
    # A tone beat on the existing result screen rather than a set of dialogue
    # labels nothing calls. Keyed by challenge category.
    P69_LOSS_TAKEAWAYS = {
        "culinary": "The judges had notes. Watching the winning dish taught you something.",
        "fitness":  "You finish anyway. Your legs will remember this on Thursday.",
        "art":      "Someone photographs the winning piece. You look at it for a long time.",
        "skill":    "You get the answer walking home, which is the worst time to get it.",
        "music":    "It didn't land the way you hoped. A musician near the bar nods anyway.",
        "career":   "Your pitch was fine. Fine is not what wins a room.",
        "bar":      "You rack the balls again out of habit.",
    }

    def p69_loss_takeaway(category):
        return P69_LOSS_TAKEAWAYS.get(category,
                                      "It didn't go your way. You know more than you did.")


# ── Wiring ────────────────────────────────────────────────────────────────────
# init 20: every function wrapped below is defined at a lower priority.
# Wrapping (rather than editing eight files) keeps Phase 69 out of the diffs of
# the phases being written concurrently, and means one place to read when this
# behaviour surprises someone later.
init 20 python:

    # ---- preparation folds into the shared city-challenge modifier list ------
    _p69_orig_city_chal_mods = _city_chal_mods

    def _city_chal_mods(event=None):
        mods = _p69_orig_city_chal_mods(event)
        spec = city_challenge_spec(event) if event is not None else None
        mods.extend(preparation_mods(spec.get("skill") if spec else None))
        return mods

    # ---- city challenge results --------------------------------------------
    _p69_orig_resolve_city_challenge = resolve_city_challenge

    def resolve_city_challenge(event_id):
        cres = _p69_orig_resolve_city_challenge(event_id)
        if cres is None:
            return None
        tmpl_id = next((e.get("template_id") for e in store.city_event_schedule
                        if e["id"] == event_id), "")
        cres["template_id"] = tmpl_id      # read back by _city_challenge_lines
        tier = cres["tier"]
        record_personal_best("best_city_challenge_finish", tier, "tier")
        if tmpl_id == "cook_off":
            record_personal_best("best_cooking_challenge_finish", tier, "tier")
        if tier in _PLACED_TIERS:
            ks = CITY_CHALLENGE_KEEPSAKES.get(tmpl_id)
            if ks:
                cres["keepsake"] = ks if grant_possession(ks, "citychal_" + event_id) else None
            record_accomplishment(
                "citychal_%s_first_place" % tmpl_id if tier == "critical"
                else "citychal_%s_placed" % tmpl_id,
                cres["title"], "%s at %s." % (cres["outcome"]["label"], cres["title"]),
                city_event_template(tmpl_id).get("category", "general"),
                {"template_id": tmpl_id, "tier": tier})
        return cres

    _p69_orig_city_challenge_lines = _city_challenge_lines

    def _city_challenge_lines(cres):
        lines = _p69_orig_city_challenge_lines(cres)
        if cres.get("keepsake"):
            lines.append("Keepsake: " + possession_name(cres["keepsake"]))
        if cres["tier"] not in _PLACED_TIERS:
            cat = city_event_template(cres.get("template_id", "")).get("category", "")
            lines.append(p69_loss_takeaway(cat))
        if cres.get("rare"):
            lines.append(cres["rare"])
        return lines

    # ---- world challenge first wins ----------------------------------------
    _p69_orig_attempt_world_challenge = attempt_world_challenge

    def attempt_world_challenge(challenge_id):
        before = store.world_challenge_history.get(challenge_id, {}).get("wins", 0)
        result, won = _p69_orig_attempt_world_challenge(challenge_id)
        after = store.world_challenge_history.get(challenge_id, {}).get("wins", 0)
        if won and before == 0 and after == 1:
            ks = WORLD_CHALLENGE_KEEPSAKES.get(challenge_id)
            if ks:
                grant_possession(ks, "worldchal_" + challenge_id)
            ch = WORLD_CHALLENGES[challenge_id]
            record_accomplishment("wc_%s_firstwin" % challenge_id, ch["label"],
                                  ch["reward_tier"].get(result["tier"], {}).get("label", ""),
                                  ch.get("category", "general"),
                                  {"challenge": challenge_id, "tier": result["tier"]})
        return result, won

    # ---- career promotions --------------------------------------------------
    _p69_orig_promote = promote

    def promote(cid=None):
        ok = _p69_orig_promote(cid)
        if ok:
            _cid = cid if cid is not None else store.job_id
            rank = store.active_careers.get(_cid, {}).get("rank", 0)
            grant_possession("promotion_certificate",
                             "promoted_%s_r%d" % (_cid, rank),
                             {"career": _cid, "rank": rank})
            record_personal_best("highest_career_rank", rank, "higher")
            record_accomplishment("promoted_%s_r%d" % (_cid, rank), "Promotion",
                                  "Promoted to %s." % (store.job_title or _cid),
                                  "career", {"career": _cid, "rank": rank})
        return ok

    # ---- music --------------------------------------------------------------
    _p69_orig_open_mic_resolve = open_mic_resolve

    def open_mic_resolve(*a, **kw):
        res = _p69_orig_open_mic_resolve(*a, **kw)
        record_personal_best("best_open_mic_tier", res["tier"], "tier")
        if res["tier"] in ("great", "critical"):
            if grant_possession("first_paid_gig_stub", "open_mic_day%d" % store.day):
                res["keepsake"] = "first_paid_gig_stub"
            record_accomplishment("open_mic_great", "The Room Listened",
                                  "A great open mic performance.", "music",
                                  {"tier": res["tier"]})
        return res

    _p69_orig_busking_resolve = busking_resolve

    def busking_resolve(*a, **kw):
        res = _p69_orig_busking_resolve(*a, **kw)
        record_personal_best("highest_busking_tips", res["tips"], "higher")
        record_personal_best("best_busking_tier", res["perf_tier"], "tier")
        return res

    # ---- painting -----------------------------------------------------------
    _p69_orig_new_artwork = new_artwork

    def new_artwork(*a, **kw):
        art = _p69_orig_new_artwork(*a, **kw)
        record_personal_best("best_artwork_quality", art["quality"], "tier")
        record_personal_best("best_artwork_estimated_value", art["estimated_value"], "higher")
        return art

    # ---- mechanics ----------------------------------------------------------
    _p69_orig_mech_attempt_repair = mech_attempt_repair

    def mech_attempt_repair(job):
        out = _p69_orig_mech_attempt_repair(job)
        if out:
            record_personal_best("best_repair_tier", out["tier"], "tier")
            if out["tier"] == "critical":
                if grant_possession("mechanics_restoration_badge", "mech_" + job["id"]):
                    out["keepsake"] = "mechanics_restoration_badge"
        return out

    # ---- cooking ------------------------------------------------------------
    _p69_orig_do_catering = do_catering

    def do_catering(order):
        res = _p69_orig_do_catering(order)
        if res:
            record_personal_best("best_catering_tier", res["tier"], "tier")
        return res

    # ---- practice tracking (feeds the preparation bonus) --------------------
    _p69_orig_gain_skill_practice = gain_skill_practice

    def gain_skill_practice(key, base_xp, hours=1):
        xp = _p69_orig_gain_skill_practice(key, base_xp, hours)
        d = dict(store._p69_last_practice)
        d[key] = store.day
        store._p69_last_practice = d
        return xp

    # ---- derived sync -------------------------------------------------------
    def p69_sync_derived():
        """Awards that can be read straight off existing history. Idempotent, so
        it also back-fills saves made before this phase existed. Cheap: a few
        list scans over collections that are tens of items at most.
        ponytail: O(n) rescan each day; upgrade path is event hooks if these
        lists ever grow past a few hundred entries.

        The very first run on a given save is a BACKFILL — it silently awards
        everything the player already earned before this phase existed. Without
        the silent flag a veteran save would open on a day summary listing two
        dozen keepsakes it 'earned' overnight."""
        backfill = store._p69_synced_day < 0
        store._p69_synced_day = store.day

        # Bar games
        for token, ks in BAR_FIRST_WIN_KEEPSAKES.items():
            if token in store.bar_first_wins:
                grant_possession(ks, "bar_" + token, silent=backfill)
        for token, opp_id in (("marcus_pool", "pool_marcus"),
                              ("professor_pool", "pool_professor")):
            if token in store.bar_first_wins:
                record_personal_best("highest_pool_opponent_defeated",
                                     _POOL_OPPONENT_TIER[opp_id], "tier")

        # Freelance
        for h in store.freelance_history:
            r = h.get("rating")
            if r:
                record_personal_best("best_freelance_rating", r, "rating")
            if r == "S":
                grant_possession("freelance_client_card",
                                 "fl_%s_day%s" % (h.get("template_id", "?"), h.get("day", 0)),
                                 {"rating": r}, silent=backfill)

        # City events attended (non-challenge ones are the community/festival
        # kind). Capped: a wall of identical wristbands is clutter, not memory.
        if len([p for p in store.player_possessions
                if p["item_id"] == "festival_wristband"]) < FESTIVAL_WRISTBAND_CAP:
            for e in store.city_event_schedule:
                if e.get("attended") and not city_challenge_spec(e):
                    grant_possession("festival_wristband", "cityevent_" + e["id"],
                                     {"title": e.get("title", "")}, silent=backfill)

        # Art scene contact
        if store.art_reputation >= 25:
            grant_possession("art_market_vendor_card", "art_rep_25", silent=backfill)

        # The one pure-luck find. Stable-seeded on the day so it cannot be
        # re-rolled by reloading, and only on a "lucky" day condition.
        if not has_possession("rare_vintage_coin") and store.day >= 10:
            import random as _r69r
            if daily_condition()["id"] in ("local_event", "beautiful_weather"):
                if _r69r.Random(store.day * 66601 + 17).random() < 0.06:
                    grant_possession("rare_vintage_coin", "lucky_find_day%d" % store.day)

    _p69_orig_new_day = new_day

    def new_day():
        _p69_orig_new_day()
        p69_sync_derived()
