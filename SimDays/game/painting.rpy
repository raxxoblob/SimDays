# Phase 65 — Painting. First full vertical slice on the capability architecture.
#
# Mirrors the Phase 61 Cooking system deliberately: SKILL (skill_art) sets what
# you may attempt, SUBJECT difficulty sets the challenge, MASTERY + GEAR +
# APPROACH modify the odds, and the Phase 60 roll engine sets the quality. No
# parallel RNG, no parallel inventory, no parallel event system.
#
# What painting is FOR, in priority order:
#   1. Artworks — persistent objects you can hang, gift, or keep.
#   2. Art reputation — the progression currency, gates everything else.
#   3. Art XP and portfolio entries.
#   4. Money. A distant fourth. See the ECONOMY NOTE on art_sale_price().
#
# Quality tier language (maps onto the 5 engine tiers):
#   critical_failure -> Ruined   weak -> Rough    success -> Solid
#   great -> Striking            critical -> Remarkable

default player_artworks             = []    # list of artwork dicts, see new_artwork()
default painting_mastery            = {}    # subject_id -> 0..PAINTING_MASTERY_CAP
default art_reputation              = 0     # 0..100, never decays
default _artwork_seq                = 0     # id counter
default active_painting_commissions = []    # accepted, not yet delivered
default painting_commissions_done   = 0
default _art_commission_taken_cycle = -1    # refresh cycle whose offer was used
default _art_sale_log               = []    # [{"day": d, "channel": c}] for the weekly cap
default _art_gift_week              = {}    # npc_id -> (week_index, count)

# Menu caption helpers (Ren'Py menu captions interpolate variables only).
default _p65_art_menu_label  = "Paint..."
default _p65_commission_note = ""
default _p65_result_line     = ""


init python:

    PAINTING_MASTERY_CAP = 100

    # ── Subjects ─────────────────────────────────────────────────────────────
    # `value` is the market scalar: what a Solid portrait is worth relative to a
    # Solid still life. Difficulty and value move together on purpose — the way
    # to earn more is to attempt harder work, not to repeat easy work faster.
    ART_SUBJECTS = {
        "still_life": {"name": "Still Life", "difficulty": 40, "value": 0.40,
                       "min_art": 2, "desc": "Fruit, a jug, the good lamp."},
        "landscape":  {"name": "Landscape",  "difficulty": 45, "value": 0.65,
                       "min_art": 4, "desc": "The waterfront, from memory."},
        "abstract":   {"name": "Abstract",   "difficulty": 50, "value": 0.80,
                       "min_art": 4, "desc": "No subject. Just the problem."},
        "portrait":   {"name": "Portrait",   "difficulty": 55, "value": 1.00,
                       "min_art": 4, "desc": "A face. The hardest thing there is."},
    }

    # ── Sessions ─────────────────────────────────────────────────────────────
    # `cap` is the capability required — the ONLY gate. No session names an item.
    ART_SESSIONS = {
        "sketch_practice": {
            "label": "Practice sketching", "hours": 1.0, "energy": 6, "xp": 5,
            "difficulty": 30, "practice": True, "cap": "sketching", "min_art": 0,
            "material": 0},
        "paint_practice": {
            "label": "Practice painting", "hours": 2.0, "energy": 10, "xp": 7,
            "difficulty": 30, "practice": True, "cap": "painting", "min_art": 0,
            "material": 3},
        "still_life": {
            "label": "Paint a still life", "hours": 2.0, "energy": 12, "xp": 8,
            "subject": "still_life", "cap": "painting", "min_art": 2,
            "material": 5},
        "canvas": {
            "label": "Paint a canvas", "hours": 3.0, "energy": 16, "xp": 10,
            "subject": None, "cap": "painting", "min_art": 4, "approach": True,
            "material": 8},
        "portfolio_piece": {
            "label": "Create a portfolio piece", "hours": 4.0, "energy": 22, "xp": 12,
            "subject": None, "cap": "painting", "min_art": 5, "approach": True,
            "ambition": True, "value_mult": 1.25, "material": 12},
    }

    # Ambition sets the difficulty band for a portfolio piece (spec: 45-70).
    # Harder work is worth more; that is the whole trade.
    ART_AMBITION = [
        ("safe",    "Play to your strengths", 0,  1.00,
         "Stay inside what you already do well."),
        ("stretch", "Stretch yourself",       8,  1.25,
         "Push past comfortable. Worth more if it lands."),
        ("reach",   "Reach",                  15, 1.50,
         "Genuinely beyond you today. Might be your best work."),
    ]
    ART_DIFFICULTY_CEILING = 70

    # Painting tier -> (display label, xp multiplier)
    _ART_QUALITY = {
        "critical_failure": ("Ruined",     0.6),
        "weak":             ("Rough",      0.8),
        "success":          ("Solid",      1.0),
        "great":            ("Striking",   1.15),
        "critical":         ("Remarkable", 1.3),
    }
    # Appraisal bands, straight from the phase spec.
    _ART_VALUE_BASE = {
        "critical_failure": (0, 5),
        "weak":             (15, 30),
        "success":          (50, 90),
        "great":            (120, 220),
        "critical":         (250, 400),
    }

    def art_quality_label(tier):
        return _ART_QUALITY[tier][0]

    # ── Capability / availability ────────────────────────────────────────────
    def art_session_available(sid):
        """Capability + skill gate. This is the ONLY place availability is decided."""
        s = ART_SESSIONS[sid]
        if not has_home_capability(s["cap"]):
            return False
        # Sketch practice is the beginner's path — it disappears once you own a
        # real easel, because "Practice painting" strictly supersedes it.
        if sid == "sketch_practice" and has_home_capability("painting"):
            return False
        return skill_val("art") >= s.get("min_art", 0)

    def available_art_sessions():
        return [s for s in ART_SESSIONS if art_session_available(s)]

    def art_subject_available(subj_id):
        return skill_val("art") >= ART_SUBJECTS[subj_id]["min_art"]

    def available_art_subjects():
        return [s for s in ART_SUBJECTS if art_subject_available(s)]

    # ── Mastery ──────────────────────────────────────────────────────────────
    def painting_mastery_points(subj_id):
        return store.painting_mastery.get(subj_id, 0)

    def painting_mastery_mod(subj_id):
        """0..100 points -> 0..12 roll points. Diminishing lives in the gain curve."""
        return int(min(12, painting_mastery_points(subj_id) * 0.12))

    def _gain_painting_mastery(subj_id, tier):
        pts = painting_mastery_points(subj_id)
        base = {"critical_failure": 2, "weak": 3, "success": 5,
                "great": 6, "critical": 7}[tier]
        # Diminishing above 40 (spec §6): big early, small once practiced.
        if pts >= 70:   base = max(1, base // 3)
        elif pts >= 40: base = max(1, base // 2)
        d = dict(store.painting_mastery)
        d[subj_id] = min(PAINTING_MASTERY_CAP, pts + base)
        store.painting_mastery = d

    # ── Gear ─────────────────────────────────────────────────────────────────
    def art_gear_bonus():
        """Equipment contribution in ROLL POINTS.

        home_modifier returns the fractional art_quality_modifier (basic easel
        0.04, studio 0.09, supply kit 0.04). x100 rather than x10 — the Phase 64
        proper_desk bug was exactly this: int(0.04 * 10) truncates to 0 and the
        item silently does nothing. Basic easel -> +4, studio -> +9, so studio
        over basic is +5 and the kit is +4, matching the design spec."""
        return int(round(home_modifier("art_quality_modifier") * 100))

    def has_art_supplies():
        return owns_item("art_supply_kit")

    def art_material_cost(sid):
        """Real materials cost money. Improvising is free and simply worse
        (no +4 gear bonus) — spec §2. So the cost only applies to kit owners."""
        return ART_SESSIONS[sid]["material"] if has_art_supplies() else 0

    # ── Odds ─────────────────────────────────────────────────────────────────
    def _painting_mods(sid, subj_id=None, approach="normal"):
        """ONE modifier list shared by the preview and the resolution, so the
        number shown to the player is the number that gets rolled."""
        mods = []
        if subj_id:
            m = painting_mastery_mod(subj_id)
            if m:                            mods.append(("Subject experience", m))
        g = art_gear_bonus()
        if g:                                mods.append(("Art gear", g))
        if has_player_state("inspired"):     mods.append(("Inspired", +8))
        if has_player_state("focused"):      mods.append(("Focused", +5))
        if store.need_energy < 30:           mods.append(("Low energy", -8))
        # Approach follows the Phase 61 cooking convention (careful is SAFER).
        # The spec's "-8/0/+10" reads as an inverted sign; careful costing you
        # odds would make the option strictly pointless.
        if approach == "careful":            mods.append(("Careful approach", +6))
        elif approach == "ambitious":        mods.append(("Ambitious approach", -6))
        return mods

    def art_session_difficulty(sid, subj_id=None, ambition="safe"):
        s = ART_SESSIONS[sid]
        if s.get("practice"):
            return s["difficulty"]
        base = ART_SUBJECTS[subj_id or s.get("subject") or "still_life"]["difficulty"]
        if s.get("ambition"):
            base += dict((a[0], a[2]) for a in ART_AMBITION).get(ambition, 0)
        return min(ART_DIFFICULTY_CEILING, base)

    def _art_check_id(sid, subj_id=None):
        return "painting_" + (subj_id or ART_SESSIONS[sid].get("subject") or sid)

    def painting_chance(sid, subj_id=None, approach="normal", ambition="safe"):
        return calculate_check_chance(
            _art_check_id(sid, subj_id), skill_val("art"),
            art_session_difficulty(sid, subj_id, ambition),
            _painting_mods(sid, subj_id, approach))

    def _art_xp_efficiency(sid, subj_id=None, ambition="safe"):
        """XP scales down when the work is far below the player's skill
        (anti-farm) and up modestly when it stretches them. Same shape as
        cooking's _cook_xp_efficiency. Engine difficulty -> design 1..10."""
        eng = art_session_difficulty(sid, subj_id, ambition)
        design = (eng - 25) / 5.0          # 30 -> 1, 55 -> 6, 70 -> 9
        gap = design - skill_val("art")
        if gap <= -4:  return 0.5
        if gap <= -2:  return 0.7
        if gap <= 2:   return 1.0
        return 1.25

    # ── Artworks ─────────────────────────────────────────────────────────────
    def artwork_estimated_value(tier, subj_id, skill, value_mult=1.0):
        """Appraised worth of a finished piece.

        This is the artwork's stated value: what it means in your collection,
        what a gift is worth, what the portfolio shows. It is NOT what you get
        paid — see art_sale_price(), which is throttled separately."""
        lo, hi = _ART_VALUE_BASE[tier]
        base = renpy.random.randint(lo, hi)
        scalar = ART_SUBJECTS.get(subj_id, {}).get("value", 0.4)
        skill_scale = max(0.4, 1.0 + (skill - 3) * 0.15)
        val = base * scalar * value_mult * skill_scale
        # Spec §4: cap the top band at 500 through skill 8, a little above for 9-10.
        cap = 500 if skill <= 8 else 650
        return int(max(0, min(cap, round(val))))

    def new_artwork(kind, subj_id, tier, skill, value_mult=1.0, title=None):
        """Create and store a persistent artwork. Returns the dict."""
        store._artwork_seq += 1
        art = {
            "id":              "art_%03d" % store._artwork_seq,
            "type":            kind,                  # painting / sketch / commission
            "subject":         ART_SUBJECTS.get(subj_id, {}).get("name", title or "Study"),
            "subject_id":      subj_id,
            "quality":         tier,
            "art_skill":       skill,
            "day":             store.day,
            "estimated_value": artwork_estimated_value(tier, subj_id, skill, value_mult),
            "displayed":       False,
            "in_portfolio":    False,
            "gifted_to":       None,
            "sold":            False,
            "submitted_to":    None,
        }
        store.player_artworks = list(store.player_artworks) + [art]
        return art

    def artwork_by_id(aid):
        return next((a for a in store.player_artworks if a["id"] == aid), None)

    def update_artwork(aid, **changes):
        """Artworks live in a plain list of dicts. Rewrite the list so Ren'Py's
        rollback/save machinery sees the change."""
        arts = [dict(a) for a in store.player_artworks]
        for a in arts:
            if a["id"] == aid:
                a.update(changes)
        store.player_artworks = arts
        return artwork_by_id(aid)

    def displayed_artwork_count():
        return sum(1 for a in store.player_artworks if a.get("displayed"))

    def artwork_is_free(art):
        """Not committed anywhere — still sellable/giftable."""
        return not (art["sold"] or art["gifted_to"] or art["displayed"]
                    or art["submitted_to"])

    ARTWORK_FILTERS = [
        ("all",       "All"),
        ("portfolio", "Portfolio"),
        ("displayed", "On the wall"),
        ("available", "Available"),
        ("gifted",    "Gifted"),
        ("sold",      "Sold"),
    ]

    def filtered_artworks(f="all"):
        arts = list(reversed(store.player_artworks))
        if f == "portfolio": return [a for a in arts if a["in_portfolio"]]
        if f == "displayed": return [a for a in arts if a["displayed"]]
        if f == "available": return [a for a in arts if artwork_is_free(a)]
        if f == "gifted":    return [a for a in arts if a["gifted_to"]]
        if f == "sold":      return [a for a in arts if a["sold"]]
        return arts

    # ── Art reputation ───────────────────────────────────────────────────────
    def gain_art_rep(n):
        """Never below 0, never above 100. Does not decay (spec §9)."""
        store.art_reputation = max(0, min(100, store.art_reputation + n))
        return store.art_reputation

    # Gates. Every art_reputation threshold in the game is listed here.
    ART_REP_GATES = {
        "street_sale":       0,    # always available
        "commission_board":  5,
        "gallery_sale":      10,
        "exhibition_entry":  8,
        "senior_commission": 25,
    }

    def art_rep_gate_open(gate):
        return store.art_reputation >= ART_REP_GATES[gate]

    # ── The session itself ───────────────────────────────────────────────────
    def do_painting(sid, subj_id=None, approach="normal", ambition="safe"):
        """Resolve one painting session. Charges time + energy (materials are
        charged by the caller through try_spend). Always grants XP. Returns a
        result dict for the outcome screen."""
        s = ART_SESSIONS[sid]
        subj = subj_id or s.get("subject")
        diff = art_session_difficulty(sid, subj, ambition)
        mods = _painting_mods(sid, subj, approach)

        spend_time(s["hours"] + (0.5 if approach == "careful" else 0.0))
        store.need_energy = max(0, store.need_energy - s["energy"])

        result = roll_check(_art_check_id(sid, subj), skill_val("art"), diff,
                            mods, stable=False)
        tier = result["tier"]
        qlabel, xmult = _ART_QUALITY[tier]

        # ── XP ────────────────────────────────────────────────────────────
        # gain_skill_practice applies the daily diminishing-returns curve. The
        # spec asks for practice to bypass DR; it deliberately does not. A 1h
        # action granting undiminished XP on repeat would be the best XP/hour
        # in the game and infinitely repeatable — DR exists for exactly this.
        base_xp = max(1, int(round(s["xp"] * xmult * _art_xp_efficiency(sid, subj, ambition))))
        eff_xp = gain_skill_practice("art", base_xp, max(1, int(s["hours"])))

        if subj:
            _gain_painting_mastery(subj, tier)

        # ── Artwork ───────────────────────────────────────────────────────
        art = None
        vm = s.get("value_mult", 1.0) * dict((a[0], a[3]) for a in ART_AMBITION).get(ambition, 1.0)
        if approach == "ambitious" and tier in ("great", "critical"):
            vm *= 1.2      # the ambitious approach's upside
        if not s.get("practice"):
            art = new_artwork("painting", subj, tier, skill_val("art"), vm)
        elif tier == "critical":
            # Practice does not normally produce a keepable object. A remarkable
            # session does — it gives an art-0 player something real to gift.
            art = new_artwork("sketch", subj or "still_life", tier,
                              skill_val("art"), 0.35, title="Study")

        # ── Reputation ────────────────────────────────────────────────────
        rep = 0
        if not s.get("practice"):
            rep = {"great": 1, "critical": 2}.get(tier, 0)
            if rep:
                gain_art_rep(rep)

        if tier == "critical" and not s.get("practice"):
            record_game_event("paint_%s_day%d" % (sid, store.day), "project",
                "Painted a remarkable %s" % (ART_SUBJECTS.get(subj, {}).get("name", "piece")),
                summary=True, journal=False, portfolio_domain="art",
                metadata={"session": sid, "subject": subj, "tier": tier})

        return {"roll": result, "tier": tier, "qlabel": qlabel, "xp": eff_xp,
                "artwork": art, "rep": rep, "session": sid, "subject": subj}

    def _painting_result_lines(res):
        lines = ["+%d Art XP" % res["xp"]]
        if res["rep"]:
            lines.append("+%d art reputation" % res["rep"])
        if res["artwork"]:
            lines.append("Appraised at $%d" % res["artwork"]["estimated_value"])
        if res["subject"]:
            lines.append("%s mastery %d" % (
                ART_SUBJECTS[res["subject"]]["name"],
                painting_mastery_points(res["subject"])))
        _nm = near_miss_line(res["roll"])
        if _nm:
            lines.append(_nm)
        if res.get("rare"):
            lines.append("Lucky break — " + res["rare"])
        return lines


    # ── Selling ──────────────────────────────────────────────────────────────
    #
    # ECONOMY NOTE — why sale price is not simply a fraction of appraised value.
    #
    # The Phase 60 engine caps the skill bonus at +25 and a canvas sits around
    # difficulty 45-55. At art 6 with a studio easel that is roughly +26 total,
    # which puts ~30% of rolls in the "critical" band. Criticals are not rare
    # here. Paying out a straight 50-70% of a $250-500 appraisal on a third of
    # all sessions would make painting the best income in the game by a wide
    # margin, which is the opposite of what this phase is for.
    #
    # So the appraisal keeps its full range (it is the piece's worth, and it
    # matters for gifts, portfolio and pride) and the MARKET is what is scarce:
    #   - a per-sale ceiling that scales with art_reputation, not skill, so
    #     selling better requires a name rather than a better roll, and
    #   - a weekly gallery absorption limit, because a small city's gallery
    #     cannot move four of your canvases a week at full price.
    # Street sale is always open and always small. See the EV table in
    # debug_p65.rpy for the resulting $/hour at every skill band.
    # Commissions count against the SAME weekly absorption as gallery sales.
    # Without this they stack: 2 consignments + ~1.75 commissions a week reaches
    # freelance income, which the spec explicitly forbids. One shared throttle
    # is also the truer fiction — a small city's art scene only moves so much of
    # your work, whoever is buying it.
    ART_MARKET_WEEKLY_SLOTS = 2
    _ART_SATURATED_MULT = 0.4

    def art_sale_cap(channel):
        """Per-sale ceiling. Reputation is the lever, deliberately."""
        if channel == "gallery":
            return 60 + store.art_reputation * 2      # rep 10 -> 80, rep 60 -> 180
        return 30 + store.art_reputation              # rep 10 -> 40, rep 60 -> 90

    def art_sales_this_week(channel="gallery"):
        week = store.day // 7
        return sum(1 for s in store._art_sale_log
                   if s["day"] // 7 == week and s["channel"] == channel)

    def art_market_saturated():
        return art_sales_this_week("gallery") >= ART_MARKET_WEEKLY_SLOTS

    def art_sale_channels():
        """Channels open right now, with their gate state."""
        out = [("street", "Sell on the street", True)]
        out.append(("gallery", "Consign to the gallery", art_rep_gate_open("gallery_sale")))
        return out

    def art_sale_price(art, channel, preview=False):
        """Payout for one artwork. preview=True suppresses the random variance
        so the number shown and the number paid agree in expectation."""
        share = 0.7 if channel == "gallery" else 0.5
        price = art["estimated_value"] * share
        if channel == "gallery" and art_market_saturated():
            price *= _ART_SATURATED_MULT
        price = min(art_sale_cap(channel), price)
        if not preview:
            price *= (1.0 + renpy.random.randint(-8, 8) / 100.0)
        return int(max(1, round(price)))

    def sell_artwork(art, channel):
        price = art_sale_price(art, channel)
        gain_money(price, "art_sale")
        store._art_sale_log = list(store._art_sale_log) + [
            {"day": store.day, "channel": channel}]
        update_artwork(art["id"], sold=True, sold_for=price, sold_channel=channel)
        record_game_event("artsale_%s_day%d" % (art["id"], store.day), "money",
            "Sold \"%s\"" % art["subject"], summary=True, journal=False,
            metadata={"artwork": art["id"], "price": price, "channel": channel})
        return price

    # ── Gifting ──────────────────────────────────────────────────────────────
    # Relationship effect scales with quality AND the NPC's interest in art.
    _ART_GIFT_BASE = {"critical_failure": 1, "weak": 1, "success": 2,
                      "great": 3, "critical": 4}
    _ART_INTEREST_MULT = {-1: 0.5, 0: 1.0, 1: 1.5, 2: 2.0, 3: 2.5}

    def artwork_gift_value(art, npc_id):
        base = _ART_GIFT_BASE[art["quality"]]
        mult = _ART_INTEREST_MULT.get(npc_interest(npc_id, "art"), 1.0)
        delta = int(round(base * mult))
        # Same weekly diminishing shape as the Phase 45 gift system, so a stack
        # of paintings cannot be traded for a relationship.
        week = store.day // 7
        gw = store._art_gift_week.get(npc_id, (-1, 0))
        count = gw[1] if gw[0] == week else 0
        delta = int(round(delta * [1.0, 0.5, 0.2][min(count, 2)]))
        return max(1, delta)

    def gift_artwork(art, npc_id):
        """Apply a one-time artwork gift. Returns (delta, interest_level)."""
        delta = artwork_gift_value(art, npc_id)
        interest = npc_interest(npc_id, "art")
        week = store.day // 7
        gw = store._art_gift_week.get(npc_id, (-1, 0))
        d = dict(store._art_gift_week)
        d[npc_id] = (week, (gw[1] if gw[0] == week else 0) + 1)
        store._art_gift_week = d

        _apply_aff(npc_id, delta)
        update_artwork(art["id"], gifted_to=npc_id)
        # A piece accepted by someone who genuinely cares about art is word of
        # mouth — the only reputation source that costs nothing but a painting.
        if interest >= 2 and art["quality"] in ("success", "great", "critical"):
            gain_art_rep(1)
        record_game_event("artgift_%s_day%d" % (art["id"], store.day), "relation",
            "Gave \"%s\" to %s" % (art["subject"], NPC_DATA[npc_id]["name"]),
            summary=True, journal=False,
            metadata={"artwork": art["id"], "npc": npc_id, "delta": delta})
        return delta, interest

    def artwork_giftable_npcs():
        """Met NPCs the player could plausibly hand a painting to."""
        return [n for n in NPC_INTERESTS
                if n in NPC_DATA and getattr(store, n + "_met", True)]

    ART_GIFT_LINES = {
        # interest >= 2 — they actually look at it
        "high": [
            "They hold it at arm's length, then closer, then at arm's length again. \"You made this. You actually made this.\"",
            "\"No — wait.\" They turn it toward the window and go quiet for a long moment. \"This is good. I'm not being kind.\"",
        ],
        # interest 1 — polite, warm, not expert
        "mid": [
            "\"You painted this? For me?\" They seem genuinely caught out by it.",
            "They look at it properly, which is more than most people would. \"I like it. I don't know why, but I do.\"",
        ],
        # interest 0 — polite and brief
        "low": [
            "\"Thanks. That's — yeah, thanks.\" It goes under one arm, carefully enough.",
            "They nod, say something kind and slightly generic, and change the subject.",
        ],
        # interest -1 — stated dislike. Still a gift; still lands, barely.
        "none": [
            "\"Art isn't really my thing.\" A beat. \"But you made it. So.\" They take it anyway.",
        ],
    }

    def art_gift_line(interest):
        key = "high" if interest >= 2 else "mid" if interest == 1 else "none" if interest < 0 else "low"
        return renpy.random.choice(ART_GIFT_LINES[key])

    # ── Home-visit reaction to displayed work ────────────────────────────────
    def displayed_artwork_comment(npc_id):
        """A line an art-interested visitor adds when your work is on the wall.
        Returns None when there is nothing to say."""
        if npc_interest(npc_id, "art") < 2:
            return None
        shown = [a for a in store.player_artworks if a.get("displayed")]
        if not shown:
            return None
        best = max(shown, key=lambda a: a["estimated_value"])
        name = NPC_DATA[npc_id]["name"]
        if best["quality"] in ("great", "critical"):
            return ("%s stops in front of the %s and does not say anything for a while. "
                    "\"This one. How long did this take you?\"" % (name, best["subject"].lower()))
        return ("%s notices the %s on the wall. \"That's yours, isn't it. "
                "I can tell.\"" % (name, best["subject"].lower()))


    # ── Commissions ──────────────────────────────────────────────────────────
    # Deliberately NOT the freelance system. No briefs, no revisions, no client
    # reputation ladder — one client, one piece, one deadline, one roll.
    PAINTING_COMMISSIONS = [
        {"id": "family_portrait", "subject": "portrait", "client": "A local family",
         "label": "Portrait of the three of them, for the hallway",
         "difficulty": 52, "pay": 80,  "min_quality": "success", "art_rep_min": 5,
         "hours": 3.0, "days": 5},
        {"id": "cafe_landscape", "subject": "landscape", "client": "The café on Mill Street",
         "label": "Something of the waterfront, for above the counter",
         "difficulty": 46, "pay": 65,  "min_quality": "success", "art_rep_min": 5,
         "hours": 2.5, "days": 5},
        {"id": "memorial_still", "subject": "still_life", "client": "A neighbour",
         "label": "Her mother's things, arranged the way she remembers them",
         "difficulty": 44, "pay": 60,  "min_quality": "weak", "art_rep_min": 5,
         "hours": 2.5, "days": 6},
        {"id": "album_cover", "subject": "abstract", "client": "A band you half know",
         "label": "Cover art. They cannot describe what they want",
         "difficulty": 58, "pay": 120, "min_quality": "success", "art_rep_min": 20,
         "hours": 3.5, "days": 6},
        {"id": "gallery_commission", "subject": "portrait", "client": "A gallery regular",
         "label": "A commissioned portrait, to hang in a house you will never see",
         "difficulty": 62, "pay": 150, "min_quality": "success", "art_rep_min": 25,
         "hours": 4.0, "days": 7},
    ]
    COMMISSION_REFRESH_DAYS = 4     # one offer per cycle -> at most ~1.75/week

    # Failure never pays nothing (Phase 60/61 forward-progress rule) — a piece
    # the client does not love still cost them materials and your time.
    _COMMISSION_PAY_MULT = {"critical_failure": 0.25, "weak": 0.55,
                            "success": 1.00, "great": 1.10, "critical": 1.20}
    _QUALITY_ORDER = ["critical_failure", "weak", "success", "great", "critical"]

    def quality_at_least(tier, minimum):
        return _QUALITY_ORDER.index(tier) >= _QUALITY_ORDER.index(minimum)

    def commission_cycle():
        return store.day // COMMISSION_REFRESH_DAYS

    def painting_commission_offer():
        """The commission on the board right now, or None.

        Stable for the whole refresh cycle — seeded on the cycle number, so it
        cannot be rerolled by leaving and re-entering the screen."""
        if not art_rep_gate_open("commission_board"):
            return None
        if store._art_commission_taken_cycle == commission_cycle():
            return None
        if any(c["template"] in [t["id"] for t in PAINTING_COMMISSIONS]
               for c in store.active_painting_commissions):
            return None                      # one at a time
        open_ones = [t for t in PAINTING_COMMISSIONS
                     if store.art_reputation >= t["art_rep_min"]
                     and skill_val("art") >= 4]
        if not open_ones:
            return None
        import random as _r
        rng = _r.Random(commission_cycle() * 7919 + 31)
        return rng.choice(open_ones)

    def days_until_commission_refresh():
        return COMMISSION_REFRESH_DAYS - (store.day % COMMISSION_REFRESH_DAYS)

    def accept_painting_commission(template):
        c = {
            "id":          "commission_%03d" % (store.painting_commissions_done + 1),
            "template":    template["id"],
            "subject":     template["subject"],
            "client":      template["client"],
            "label":       template["label"],
            "difficulty":  template["difficulty"],
            "pay":         template["pay"],
            "min_quality": template["min_quality"],
            "hours":       template["hours"],
            "deadline_day": store.day + template["days"],
            "accepted_day": store.day,
        }
        store.active_painting_commissions = list(store.active_painting_commissions) + [c]
        store._art_commission_taken_cycle = commission_cycle()
        return c

    def active_painting_commission():
        """The commission currently being worked, or None. Pure — no side effects,
        because menu conditions and screens both call this."""
        return store.active_painting_commissions[0] if store.active_painting_commissions else None

    def expire_painting_commissions():
        """Drop anything past its deadline. Called once per painting-menu visit,
        not from an accessor. Returns the list of expired commissions."""
        live, dead = [], []
        for c in store.active_painting_commissions:
            (dead if store.day > c["deadline_day"] else live).append(c)
        if dead:
            store.active_painting_commissions = live
            for c in dead:
                gain_art_rep(-1)
                record_game_event("commfail_%s_day%d" % (c["id"], store.day), "project",
                    "Missed a commission deadline (%s)" % c["client"],
                    summary=True, journal=False, metadata={"commission": c["id"]})
        return dead

    def _commission_mods(commission, approach="normal"):
        mods = _painting_mods("canvas", commission["subject"], approach)
        if store.painting_commissions_done >= 3:
            mods.append(("Working artist", +4))
        return mods

    def commission_chance(commission, approach="normal"):
        return calculate_check_chance("comm_" + commission["template"], skill_val("art"),
                                      commission["difficulty"],
                                      _commission_mods(commission, approach))

    def commission_pay_range(commission):
        return (int(round(commission["pay"] * min(_COMMISSION_PAY_MULT.values()))),
                int(round(commission["pay"] * max(_COMMISSION_PAY_MULT.values()))))

    def do_commission_work(commission, approach="normal"):
        """One work session delivers the commission. Charges time + energy,
        rolls, pays, applies reputation. Never: accept -> instant money."""
        spend_time(commission["hours"] + (0.5 if approach == "careful" else 0.0))
        store.need_energy = max(0, store.need_energy - (10 + int(commission["hours"] * 4)))

        mods = _commission_mods(commission, approach)
        result = roll_check("comm_" + commission["template"], skill_val("art"),
                            commission["difficulty"], mods, stable=False)
        tier = result["tier"]
        met = quality_at_least(tier, commission["min_quality"])
        pay = int(round(commission["pay"] * _COMMISSION_PAY_MULT[tier]))
        gain_money(pay, "art_commission")

        if tier == "critical_failure":
            rep = -1
        elif met:
            rep = 3
        else:
            rep = 0
        gain_art_rep(rep)

        xp = gain_skill_practice("art", 10 + int(commission["difficulty"] / 10),
                                 max(1, int(commission["hours"])))
        _gain_painting_mastery(commission["subject"], tier)

        art = new_artwork("commission", commission["subject"], tier, skill_val("art"), 1.0)
        # The client keeps the piece — it is delivered, not inventory.
        update_artwork(art["id"], sold=True, sold_for=pay, sold_channel="commission",
                       in_portfolio=met, client=commission["client"])

        store.active_painting_commissions = [
            c for c in store.active_painting_commissions if c["id"] != commission["id"]]
        store.painting_commissions_done += 1
        # A delivered commission is a piece the local market has absorbed.
        store._art_sale_log = list(store._art_sale_log) + [
            {"day": store.day, "channel": "gallery"}]

        record_game_event("comm_%s_day%d" % (commission["id"], store.day), "project",
            "Commission: %s" % commission["label"], summary=True, journal=False,
            portfolio_domain=("art" if met else None),
            metadata={"commission": commission["id"], "client": commission["client"],
                      "pay": pay, "tier": tier, "met": met})

        return {"roll": result, "tier": tier, "qlabel": art_quality_label(tier),
                "pay": pay, "xp": xp, "rep": rep, "met": met, "artwork": art,
                "commission": commission}

    def _commission_result_lines(res):
        lines = ["Paid $%d" % res["pay"], "+%d Art XP" % res["xp"]]
        if res["rep"]:
            lines.append("%+d art reputation" % res["rep"])
        if not res["met"]:
            lines.append("Below the brief — reduced payment")
        return lines


    # ── Exhibition submission ────────────────────────────────────────────────
    def scheduled_art_exhibitions():
        """Upcoming, unattended art-exhibition city events."""
        return [e for e in store.city_event_schedule
                if e.get("template_id") == "art_exhibition" and not e.get("attended")]

    def exhibition_submittable_artworks():
        """Spec §7: quality >= success, and not already committed elsewhere."""
        return [a for a in store.player_artworks
                if quality_at_least(a["quality"], "success")
                and not a["sold"] and not a["gifted_to"] and not a["submitted_to"]]

    def can_enter_exhibition():
        return (art_rep_gate_open("exhibition_entry")
                and any(a["submitted_to"] for a in store.player_artworks))

    def submitted_artwork_for(event_id):
        return next((a for a in store.player_artworks
                     if a.get("submitted_to") == event_id), None)

    def exhibition_submission_bonus(event_id):
        """The piece you entered is what gets judged — its quality is the single
        biggest factor in placing. Returns a (label, value) modifier or None."""
        art = submitted_artwork_for(event_id)
        if art is None:
            return None
        pts = {"success": 4, "great": 10, "critical": 16}.get(art["quality"], 0)
        return ("Submitted piece (%s)" % art_quality_label(art["quality"]), pts)
