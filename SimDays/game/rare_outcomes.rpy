# Rare outcomes / outcome variance pass.
#
# DESIGN NOTE (read before extending):
#
#   The design target is GUARANTEED PROGRESS + VARIABLE RESULT + RARE POSITIVE
#   UPSIDE. Nothing in this file adds a failure mode, a Luck stat, or a second
#   resolution engine. Phase 60's roll_check() stays the only roller and its
#   five tiers stay the only tiers:
#
#       critical_failure < weak < success < great < critical
#
#   What this file adds is a LAYER ABOVE a finished result: given a tier that
#   already happened, does something extra also happen? At most one thing, ever,
#   per attempt. Stable-seeded, so reloading an attempt cannot re-roll it.
#
#   THREE THINGS ALREADY EXISTED AND ARE REUSED, NOT REPLACED:
#     * world_pulse.RARE_OPPORTUNITY_TEMPLATES + maybe_rare_opportunity() —
#       leads that arrive as mail and unlock an already-balanced opportunity.
#       force_rare_opportunity() below fires one of those templates on demand,
#       honouring the same cooldown map and the same daily mail budget.
#     * possessions.rpy — grant_possession / record_personal_best /
#       record_accomplishment. No new award store.
#     * npc_initiative.publish_player_fact() — how the world hears about you.
#
#   SYSTEMS DELIBERATELY LEFT ALONE (they already have real outcome variance;
#   adding a second rare layer would double-dip):
#     cooking.rpy        _cooking_rare_outcome()   4 outcomes, dedup'd
#     freelance.rpy      FREELANCE_RARE_EVENTS     4 events, per-project dedup
#     mechanics_projects _mech_referral() + materials refund + double-improve
#     careers.rpy        promotion pity + incidents
#
# ponytail: one flat weighted table per activity, O(len(table)) per attempt.
#   Upgrade path if this grows: per-NPC / per-location sub-tables keyed the same
#   way, selected before roll_rare_table() rather than inside it.
#
# ── AUDIT MATRIX ──────────────────────────────────────────────────────────────
# Guaranteed progress = what you get even on the worst roll.
# "$ EV" = effect on dollars per hour. Weekly rates: selfcheck section M.
#
# Busking          guaranteed +18 guitar XP, tips floor $3, mastery
#                  existing variance: crowd roll x performance roll, mult cap 1.9
#                  NEW rare: success+ @10%  ->  crowd_surge (repeat, cd 2d, +$8-25
#                  +2 followers) / musician_connection (unique, keepsake + mail)
#                  / venue_lead (repeat, cd 14d, mail) / memorable_performance
#                  (unique, accomplishment, PB-gated).   $ EV +0.66/h (+2.0%)
#
# Open Mic         guaranteed +25 guitar XP; gated guitar 4 + music rep 8
#                  existing variance: single roll, tier-scaled tips/followers/rep
#                  NEW rare: success+ @20% (great 30%, critical 45%) ->
#                  social_spike (repeat cd 5d, +10-24 followers + feed post) /
#                  promoter_notice (unique, mail) / venue_invitation (repeat
#                  cd 14d, mail) / first_exceptional (unique, keepsake).  $ EV 0
#
# Painting         guaranteed art XP + an artwork; market throttle owns income
#                  existing variance: quality tier -> appraisal band
#                  NEW rare: success+ @8% -> social_exposure (repeat cd 7d,
#                  +1-2 art rep + mail) / gallery_interest (cd 21d via the
#                  shared lead) / collector_interest (artwork flag) /
#                  breakthrough_piece (unique, great+, PB-gated).       $ EV 0
#
# Bar games        guaranteed mastery on win AND loss; first-win keepsakes (P69)
#                  existing variance: stable roll vs opponent difficulty
#                  NEW rare: win @8% -> local_reputation (cd 4d, +1 energy) /
#                  rematch_invite (cd 7d/opponent) / new_challenger (cd 14d).
#                  No cash, no mastery, no odds change.                  $ EV 0
#
# City challenges  guaranteed XP at every tier incl. no placement; P69 keepsakes
#                  existing variance: 5 placement tiers with distinct rewards
#                  NEW rare: placed @20% -> contact_gain (cd 10d, mail) /
#                  public_recognition (cd 7d, word of mouth + feed) /
#                  unique_first_win (unique, critical only).
#                  NEW miss branch @25% -> a per-event pointer at something that
#                  already exists in the game. No prize money either way. $ EV 0
#
# UNCHANGED — these already had real variance and would double-dip:
#   Cooking     _cooking_rare_outcome(): 10/22% on great/critical, 4 outcomes
#               (recipe variation / photo / Inspired / NPC asks), dedup'd
#   Freelance   FREELANCE_RARE_EVENTS: 5-12%, breakthrough / client hint /
#               referral flag / extra work, per-project dedup
#   Mechanics   materials refund on great, _mech_referral() on critical,
#               double condition-improve on critical restore, P69 badge
#   Careers     promotion pity, 20% shift incidents with real choices
#   Fitness     the PB attempt is already a real roll; this pass only adds
#               personal-best RECORDING (locations.rpy), no rare layer — a gym
#               session is not a place the player is looking for a surprise.

default rare_outcome_last_day = {}   # rare_id -> last day that rare_id fired
default rare_outcome_seen     = []   # unique rare ids already consumed
default rare_bar_challenger   = -1   # day a new bar challenger was unlocked (-1 none)


init python:

    # Phase 60's tiers, weakest first. Single source of truth for tier gating.
    RARE_TIER_ORDER = ["critical_failure", "weak", "success", "great", "critical"]

    def _det_hash(s):
        """Deterministic string fold — stable across process restarts.
        CPython randomises built-in hash() per process (PYTHONHASHSEED), so
        hash() would give a different seed after save/restart, making any
        stable-seeded roll save-scummable. This fold is always the same.
        Same algorithm as location_beats_tier_a._beat_seed_of()."""
        acc = 0
        for ch in str(s):
            acc = (acc * 131 + ord(ch)) % 1_000_003
        return acc

    def _rare_tier_index(tier, default=0):
        try:
            return RARE_TIER_ORDER.index(tier)
        except ValueError:
            return default

    def _rare_seed(activity_id, attempt_number, salt):
        """Same shape as roll_check's stable seed, offset by `salt` so the rare
        gate, the table pick and the size roll are independent streams that all
        still replay identically after a load."""
        return (store.day * 100003 + attempt_number * 997
                + _det_hash(activity_id + salt) % 9973)

    def check_rare_outcome(activity_id, result_tier, attempt_number=0,
                           min_tier="great", rare_pct=8):
        """True if a rare outcome fires on top of an already-resolved result.

        result_tier / min_tier are Phase 60 tier strings (RARE_TIER_ORDER).
        Stable: same activity_id + day + attempt_number -> same answer."""
        if rare_pct <= 0:
            return False
        if _rare_tier_index(result_tier, 0) < _rare_tier_index(min_tier, 3):
            return False
        import random as _rr
        rng = _rr.Random(_rare_seed(activity_id, attempt_number, "_rare"))
        return rng.randint(1, 100) <= rare_pct

    def roll_rare_table(activity_id, attempt_number, table):
        """Pick one outcome id from `table` by weight.

        table: [(weight, outcome_id, is_valid_or_None), ...]. Entries whose
        is_valid() is falsey are dropped first, so uniques cannot be handed out
        twice and cooldowns are respected without a per-caller guard.
        Returns the outcome id, or None when nothing is eligible."""
        valid = [(w, oid) for (w, oid, vfn) in table
                 if w > 0 and (vfn is None or vfn())]
        if not valid:
            return None
        import random as _rr
        rng = _rr.Random(_rare_seed(activity_id, attempt_number, "_table"))
        roll = rng.uniform(0, sum(w for w, _ in valid))
        acc = 0.0
        for w, oid in valid:
            acc += w
            if roll <= acc:
                return oid
        return valid[-1][1]

    def rare_roll_int(activity_id, attempt_number, lo, hi):
        """Stable size roll for a rare reward, so the payout cannot be
        re-rolled either."""
        import random as _rr
        return _rr.Random(_rare_seed(activity_id, attempt_number,
                                     "_size")).randint(lo, hi)

    def rare_cooldown_ok(rare_id, cooldown_days):
        return (store.day - store.rare_outcome_last_day.get(rare_id, -9999)) >= cooldown_days

    def rare_once_ok(rare_id):
        return rare_id not in store.rare_outcome_seen

    def record_rare_triggered(rare_id, once=False):
        d = dict(store.rare_outcome_last_day)
        d[rare_id] = store.day
        store.rare_outcome_last_day = d
        if once and rare_id not in store.rare_outcome_seen:
            store.rare_outcome_seen = list(store.rare_outcome_seen) + [rare_id]

    def rare_attempt_no(check_id):
        """Attempts recorded by roll_check for this check id. Read AFTER the roll
        so the number identifies this attempt."""
        return store._check_attempts.get(check_id, 0)

    # ── Leads: reuse the Phase 67 opportunity-lead pipeline ───────────────────
    def force_rare_opportunity(oid, delay_days=2):
        """Fire one RARE_OPPORTUNITY_TEMPLATES lead now, ignoring its own random
        chance but honouring its cooldown, the daily mail budget and mail dedup.
        Returns True if a lead was queued.

        These NEVER pay out. They queue mail that points at an existing,
        already-balanced opportunity — the economy note in world_pulse.rpy
        applies unchanged."""
        t = RARE_OPPORTUNITY_TEMPLATES.get(oid)
        if t is None:
            return False
        if store.day - store._rare_opportunity_last.get(oid, -999) < t["cooldown_days"]:
            return False
        if not _pulse_can_mail():
            return False
        tag = "rare_opp_%s_d%d" % (oid, store.day)
        if mail_already_queued(tag):
            return False
        queue_mail(t["sender"], t["subject"], t["body"], "opportunity",
                   store.day + max(0, delay_days), tag)
        store._pulse_mail_today += 1
        d = dict(store._rare_opportunity_last)
        d[oid] = store.day
        store._rare_opportunity_last = d
        return True

    def rare_mail(sender, subject, body, tag, delay_days=2, category="opportunity"):
        """One-off rare mail that is not a reusable lead template. Same budget
        and dedup rules as force_rare_opportunity."""
        if not _pulse_can_mail() or mail_already_queued(tag):
            return False
        queue_mail(sender, subject, body, category,
                   store.day + max(0, delay_days), tag)
        store._pulse_mail_today += 1
        return True

    # ── Per-activity rare definitions ────────────────────────────────────────
    # min_tier is the Phase 60 tier the ORDINARY result must already have
    # reached. pct is flat unless a `pct_by_tier` override names the tier.
    # TUNING NOTE. These percentages are per-attempt, but what matters is
    # rares-per-week, which is (sessions/week x P(reaching min_tier) x pct).
    # A percentage that looks generous on a once-a-week gated event is still
    # rarer than a stingy one on a three-times-a-day activity, so the rates
    # below are deliberately uneven. tests/rare_outcomes_selfcheck.py section M
    # prints the resulting weekly rate for a moderate player and fails if the
    # total drifts outside 0.25-1.5/week.
    RARE_ACTIVITY_RULES = {
        # Most-repeated monetary activity, so: cheapest rare, hard-capped money
        # branch (see the EV note on the wrapper below).
        "busking":        {"min_tier": "success", "pct": 10},
        # Gated (guitar 4 + music rep 8), 2h, roughly once a week, and the only
        # place a music career can actually open up. Strongest rare in the pass,
        # and it scales with how well the set went.
        "open_mic":       {"min_tier": "success", "pct": 20,
                           "pct_by_tier": {"great": 30, "critical": 45}},
        "painting":       {"min_tier": "success", "pct": 8},
        "bar_game":       {"min_tier": "success", "pct": 8},
        # Challenges are themselves rare (a handful a month), so a placement
        # gets a much higher rate — otherwise a player could finish the game
        # without ever seeing one.
        "city_challenge": {"min_tier": "success", "pct": 20},
        # Consolation branch: a poor showing sometimes still points somewhere.
        "city_challenge_miss": {"min_tier": "critical_failure", "pct": 25},
    }

    def rare_pct_for(activity_id, tier=None):
        r = RARE_ACTIVITY_RULES.get(activity_id)
        if not r:
            return 0
        if tier is not None and tier in r.get("pct_by_tier", {}):
            return r["pct_by_tier"][tier]
        return r["pct"]

    def rare_possible_for(activity_id):
        """For the odds preview. Mechanical activities only — never expose a
        percentage on a social or relationship check."""
        return activity_id in RARE_ACTIVITY_RULES

    # Plain-English tier names for the preview. tier_label() is for results
    # ("Great Success"); this reads as a requirement ("a great result or better").
    _RARE_TIER_ADJECTIVE = {
        "weak": "weak", "success": "successful", "great": "great",
        "critical": "exceptional",
    }

    def rare_preview_line(activity_id):
        r = RARE_ACTIVITY_RULES.get(activity_id)
        if not r:
            return ""
        adj = _RARE_TIER_ADJECTIVE.get(r["min_tier"])
        if adj is None:
            return "Rare opportunity possible."
        return "Rare opportunity possible on a %s result." % adj

    def rare_fires(activity_id, tier, attempt_number):
        r = RARE_ACTIVITY_RULES.get(activity_id)
        if not r:
            return False
        return check_rare_outcome(activity_id, tier, attempt_number,
                                  r["min_tier"], rare_pct_for(activity_id, tier))

    # ── Near-miss readout ────────────────────────────────────────────────────
    # roll_check already returns the real post-modifier score, and the tier
    # thresholds are constants, so this is genuine data rather than decoration.
    _RARE_TIER_FLOOR = {"weak": 11, "success": 40, "great": 75, "critical": 95}

    def near_miss_line(result):
        """'Score: 72   Great needs: 75' when the next tier was within 5.
        Empty string otherwise, and empty at the top tier."""
        tier = result.get("tier")
        final = result.get("final")
        if final is None or tier == "critical":
            return ""
        nxt = RARE_TIER_ORDER[_rare_tier_index(tier) + 1]
        floor = _RARE_TIER_FLOOR.get(nxt)
        if floor is None or not (0 < floor - final <= 5):
            return ""
        return "Score %d — %s needed %d." % (final, tier_label(nxt), floor)


# ── Wiring ────────────────────────────────────────────────────────────────────
# init 25: AFTER possessions.rpy's init-20 wrappers, so personal bests recorded
# there are already stored when a rare outcome asks "was that a personal best?".
# Wrapping instead of editing five activity files keeps this pass out of their
# diffs and puts every rare payout in one readable place.
init 25 python:

    # ── Busking ───────────────────────────────────────────────────────────────
    # EV NOTE. Busking base is rep*0.40 + skill*2.5 with the crowd x perf
    # multiplier capped at 1.9 and 3 sessions/day. crowd_surge is the only money
    # branch and pays $8-25 flat, i.e. at most ~$17 expected on the 60/100 slice
    # of a 10% rare after a success-or-better set: ~0.10 * 0.60 * 17 = $1.02 per
    # 1.5h session, about $0.7/hour. Phase 63B's ceiling is untouched.
    _RARE_BUSK_SURGE = (8, 25)

    _p_rare_orig_busking_resolve = busking_resolve

    def busking_resolve(*a, **kw):
        res = _p_rare_orig_busking_resolve(*a, **kw)
        attempt = rare_attempt_no("busking")
        if not rare_fires("busking", res["perf_tier"], attempt):
            return res
        pick = roll_rare_table("busking", attempt, [
            (60, "crowd_surge",           lambda: rare_cooldown_ok("busk_surge", 2)),
            (18, "musician_connection",   lambda: not has_possession("musician_contact_card")),
            (12, "venue_lead",            lambda: rare_cooldown_ok("busk_venue", 14)),
            (10, "memorable_performance", lambda: rare_once_ok("busk_memorable")),
        ])
        if pick == "crowd_surge":
            bonus = rare_roll_int("busking", attempt, *_RARE_BUSK_SURGE)
            res["tips"] += bonus
            res["followers"] += 2
            record_rare_triggered("busk_surge")
            res["rare"] = ("A knot of people stops all at once and the case fills up. "
                           "+$%d, +2 followers." % bonus)
        elif pick == "musician_connection":
            if grant_possession("musician_contact_card", "busk_day%d" % store.day):
                rare_mail("Kaz (guitar)", "That thing you were playing",
                          "I was the one with the case at the fountain. If you ever "
                          "want to split a set, I'm around most weekends. Bring the "
                          "same tuning.", "rare_busk_musician_d%d" % store.day,
                          delay_days=2, category="social")
                record_rare_triggered("busk_musician", once=True)
                res["rare"] = ("Another player waits until you finish, then swaps names "
                               "with you. (Contact kept)")
        elif pick == "venue_lead":
            if force_rare_opportunity("busking_venue_contact", delay_days=3):
                record_rare_triggered("busk_venue")
                res["rare"] = ("Someone listens to the whole set from a doorway, then "
                               "writes something down. (Mail coming)")
        elif pick == "memorable_performance":
            # Only counts if the set genuinely was the best one yet. The personal
            # best was already written by the Phase 69 wrapper, so compare to it.
            if store.player_personal_bests.get("highest_busking_tips", 0) <= res["tips"]:
                record_accomplishment("busk_memorable_set", "The Set That Landed",
                                      "A busking set that people actually stopped for.",
                                      "music", {"tips": res["tips"],
                                                "tier": res["perf_tier"]})
                record_rare_triggered("busk_memorable", once=True)
                res["rare"] = "You will remember this one. (Recorded)"
        return res

    # ── Open mic ──────────────────────────────────────────────────────────────
    # Open mic is gated (guitar 4 + music rep 8) and costs 2h, so it carries the
    # strongest rares. Its old flavour text promised "a new opportunity may
    # open" and nothing opened; venue_invitation / promoter_notice are that
    # promise made real.
    _p_rare_orig_open_mic_resolve = open_mic_resolve

    def open_mic_resolve(*a, **kw):
        res = _p_rare_orig_open_mic_resolve(*a, **kw)
        attempt = rare_attempt_no("open_mic")
        if not rare_fires("open_mic", res["tier"], attempt):
            return res
        pick = roll_rare_table("open_mic", attempt, [
            (30, "social_spike",     lambda: rare_cooldown_ok("om_social", 5)),
            (26, "promoter_notice",  lambda: rare_once_ok("om_promoter")),
            (26, "venue_invitation", lambda: rare_cooldown_ok("busk_venue", 14)),
            (18, "first_exceptional", lambda: res["tier"] == "critical"
                                              and rare_once_ok("om_first_exceptional")),
        ])
        if pick == "social_spike":
            burst = rare_roll_int("open_mic", attempt, 10, 24)
            res["followers"] += burst
            store.social_feed_posts = [{
                "id": "om_spike_d%d" % store.day, "npc_id": "you", "day": store.day,
                "text": "Played the open mic. Someone filmed it. Apparently it's going around.",
            }] + list(store.social_feed_posts)
            record_rare_triggered("om_social")
            res["rare"] = ("A clip of your third song gets passed around overnight. "
                           "+%d followers." % burst)
        elif pick == "promoter_notice":
            if rare_mail("V. Okonjo", "Booking — short sets",
                         "I run the weeknight slots and I watched your set. I am not "
                         "promising anything, but come to the next open mic and ask "
                         "for me by name. Bring more than four songs.",
                         "rare_om_promoter_d%d" % store.day, delay_days=2):
                record_rare_triggered("om_promoter", once=True)
                res["rare"] = ("Someone with a lanyard asks the bar who you are. "
                               "(Mail coming)")
        elif pick == "venue_invitation":
            if force_rare_opportunity("busking_venue_contact", delay_days=2):
                record_rare_triggered("busk_venue")
                res["rare"] = "A better room wants to talk to you. (Mail coming)"
        elif pick == "first_exceptional":
            if grant_possession("first_paid_gig_stub", "open_mic_exceptional"):
                res["keepsake"] = "first_paid_gig_stub"
            record_accomplishment("open_mic_first_exceptional", "Full Room",
                                  "Your first exceptional open mic performance.",
                                  "music", {"tier": res["tier"]})
            record_rare_triggered("om_first_exceptional", once=True)
            res["rare"] = "The room does not let you leave the stage. (Recorded)"
        return res

    # ── Painting ──────────────────────────────────────────────────────────────
    # Painting had no rare layer at all. None of these branches pay cash: the
    # market throttle in painting.rpy (per-sale ceiling + weekly gallery
    # absorption) is what limits art income and it is untouched. gallery_interest
    # and collector_interest route through existing sale channels instead.
    _p_rare_orig_do_painting = do_painting

    def do_painting(sid, subj_id=None, approach="normal", ambition="safe"):
        res = _p_rare_orig_do_painting(sid, subj_id=subj_id, approach=approach,
                                       ambition=ambition)
        art = res.get("artwork")
        if art is None:
            return res      # a practice session with nothing to show
        attempt = rare_attempt_no(_art_check_id(sid, res.get("subject")))
        if not rare_fires("painting", res["tier"], attempt):
            return res
        pick = roll_rare_table("painting", attempt, [
            (34, "social_exposure",    lambda: rare_cooldown_ok("art_social", 7)),
            (24, "gallery_interest",   lambda: art_rep_gate_open("exhibition_entry")),
            (24, "collector_interest", lambda: art_rep_gate_open("commission_board")),
            (18, "breakthrough_piece", lambda: res["tier"] in ("great", "critical")
                                              and rare_once_ok("art_breakthrough")),
        ])
        if pick == "social_exposure":
            rep = 1 if store.art_reputation > 40 else 2
            gain_art_rep(rep)
            res["rep"] += rep
            rare_mail("citycanvas", "We reposted your piece",
                      "A local art account picked up a photo of your work. No money "
                      "in it, but people are asking where they can see more. The "
                      "street stall and the commission board are both fair answers.",
                      "rare_art_social_d%d" % store.day, delay_days=1, category="social")
            record_rare_triggered("art_social")
            res["rare"] = ("A local art account reposts the piece. +%d art reputation."
                           % rep)
        elif pick == "gallery_interest":
            if force_rare_opportunity("art_market_commission", delay_days=3):
                record_rare_triggered("art_gallery")
                res["rare"] = ("Someone photographs this one and asks what else you "
                               "have. (Mail coming)")
        elif pick == "collector_interest":
            grant_possession("art_market_vendor_card", "collector_d%d" % store.day)
            update_artwork(art["id"], collector_interest=True)
            record_rare_triggered("art_collector")
            res["rare"] = ("A buyer asks you to hold this piece back from the stall. "
                           "It will sell better through the gallery.")
        elif pick == "breakthrough_piece":
            if store.player_personal_bests.get("best_artwork_quality") == res["tier"]:
                record_accomplishment("art_breakthrough_piece", "It Finally Worked",
                                      "The piece where the technique clicked.",
                                      "art", {"artwork": art["id"], "tier": res["tier"]})
                add_player_state("inspired", "art_breakthrough_d%d" % store.day)
                record_rare_triggered("art_breakthrough", once=True)
                res["rare"] = ("Something clicked in this one that has not clicked "
                               "before. (Recorded, Inspired)")
        return res

    # ── Bar games ─────────────────────────────────────────────────────────────
    # Called from bar_game_play after a win. First-win keepsakes are already
    # handled by the Phase 69 derived sync, so this layer stays social: no cash,
    # no mastery, nothing that changes the odds of the next game.
    def bar_game_rare(game_type, opponent_id, tier):
        """Returns a line to print, or ''. Win-only — the caller gates on that."""
        aid = game_type + "_" + opponent_id
        attempt = rare_attempt_no(aid)
        if not rare_fires("bar_game", tier, attempt):
            return ""
        pick = roll_rare_table("bar_game", attempt, [
            (40, "local_reputation", lambda: rare_cooldown_ok("bar_rep", 4)),
            (30, "rematch_invite",   lambda: rare_cooldown_ok("bar_rematch_" + opponent_id, 7)),
            (30, "new_challenger",   lambda: store.rare_bar_challenger < 0
                                             or store.day - store.rare_bar_challenger >= 14),
        ])
        if pick == "local_reputation":
            # Flavour plus a real +1 energy from the drink. Deliberately NOT a
            # relationship change: there is no RELATIONSHIP_SOURCE_CAPS key for
            # "a stranger at the bar", and inventing one would let a repeatable
            # 3-per-day activity feed the relationship economy.
            store.need_energy = min(100, store.need_energy + 1)
            record_rare_triggered("bar_rep")
            return "The table next to you was watching. Someone buys you the next one."
        if pick == "rematch_invite":
            record_rare_triggered("bar_rematch_" + opponent_id)
            return "They rack up again without asking. \"Tomorrow. Same time.\""
        if pick == "new_challenger":
            store.rare_bar_challenger = store.day
            record_rare_triggered("bar_challenger")
            return ("Someone you have not played before has been watching the whole "
                    "night. They will be here again.")
        return ""

    # ── City challenges ───────────────────────────────────────────────────────
    # Placement rares are contacts and recognition, never extra prize money —
    # _chal_outcomes() owns the cash and stays authoritative. The miss branch is
    # the important half: not placing now sometimes still tells you where to go.
    _p_rare_orig_resolve_city_challenge = resolve_city_challenge

    def resolve_city_challenge(event_id):
        cres = _p_rare_orig_resolve_city_challenge(event_id)
        if cres is None:
            return None
        tier = cres["tier"]
        attempt = rare_attempt_no("citychal_" + event_id)
        tmpl_id = cres.get("template_id", "")
        placed = tier in ("success", "great", "critical")

        if placed and rare_fires("city_challenge", tier, attempt):
            pick = roll_rare_table("city_challenge", attempt, [
                (36, "contact_gain",       lambda: rare_cooldown_ok("chal_contact", 10)),
                (34, "public_recognition", lambda: rare_cooldown_ok("chal_public", 7)),
                (30, "unique_first_win",   lambda: tier == "critical"
                                                   and rare_once_ok("chal_first_win")),
            ])
            if pick == "contact_gain":
                if rare_mail("Organiser — " + cres.get("title", "the event"),
                             "You should hear about the next one",
                             "You placed, so you are on the list now. We run these "
                             "every few weeks and the harder bracket is worth your "
                             "time. Watch the noticeboard.",
                             "rare_chal_contact_d%d" % store.day, delay_days=2):
                    record_rare_triggered("chal_contact")
                    cres["rare"] = ("The organiser takes your name down properly this "
                                    "time. (Mail coming)")
            elif pick == "public_recognition":
                publish_player_fact("won_city_challenge", event_id)
                store.social_feed_posts = [{
                    "id": "chal_rare_d%d" % store.day, "npc_id": "you", "day": store.day,
                    "text": "Placed at %s. Still holding the certificate."
                            % cres.get("title", "the competition"),
                }] + list(store.social_feed_posts)
                record_rare_triggered("chal_public")
                cres["rare"] = "A photo of the results board does the rounds."
            elif pick == "unique_first_win":
                record_accomplishment("chal_first_outright_win", "First Outright Win",
                                      "You won a city competition outright.",
                                      "competition", {"event": event_id,
                                                      "template_id": tmpl_id})
                record_rare_triggered("chal_first_win", once=True)
                cres["rare"] = "First time you have won one of these outright. (Recorded)"

        elif not placed and rare_fires("city_challenge_miss", tier, attempt):
            alt = _RARE_CHALLENGE_ALTERNATIVES.get(tmpl_id)
            if alt:
                record_rare_triggered("chal_miss_hint")
                cres["rare"] = alt
        return cres

    # Miss-branch hints. Point at something that already exists in the game —
    # never invent an activity the player cannot go and do.
    _RARE_CHALLENGE_ALTERNATIVES = {
        "cook_off":          "A judge catches you afterwards: \"Your technique is fine. "
                             "Cook one dish forty times instead of forty dishes once.\"",
        "art_exhibition":    "Another entrant suggests the street stall first. Sell a few, "
                             "come back with a name.",
        "coding_workshop":   "Someone shows you their solution on the walk out. It is "
                             "shorter than yours and you know why.",
        "fitness_challenge": "The organiser tells you the bracket you should have entered. "
                             "It runs again.",
        "music_showcase":    "\"Open mic first,\" says the sound tech, not unkindly. "
                             "\"Everyone here did open mic first.\"",
        "networking_pitch":  "A woman waiting for her coat tells you your pitch had two "
                             "ideas in it, and one of them was good.",
        "trivia_night":      "The winning table invites you to sit with them next week.",
    }

    # ── Old-save migration ────────────────────────────────────────────────────
    def p_rare_sync():
        """Initialise this pass's fields on a save made before it existed, and
        back-fill the two 'once' flags from records that already prove the moment
        happened — so a veteran save is not offered a first-time rare it already
        earned. Idempotent; runs once per day alongside p69_sync_derived().
        ponytail: three list scans over collections of tens of items. Upgrade
        path is the same as p69_sync_derived's — hook the write sites instead."""
        if not hasattr(store, "rare_outcome_last_day") or store.rare_outcome_last_day is None:
            store.rare_outcome_last_day = {}
        if not hasattr(store, "rare_outcome_seen") or store.rare_outcome_seen is None:
            store.rare_outcome_seen = []
        if not hasattr(store, "rare_bar_challenger"):
            store.rare_bar_challenger = -1
        done = set(store.rare_outcome_seen)
        have = set(a["id"] for a in store.player_accomplishments)
        for flag, acc_id in (("om_first_exceptional", "open_mic_first_exceptional"),
                             ("chal_first_win",       "chal_first_outright_win"),
                             ("art_breakthrough",     "art_breakthrough_piece"),
                             ("busk_memorable",       "busk_memorable_set")):
            if acc_id in have and flag not in done:
                done.add(flag)
        if has_possession("musician_contact_card"):
            done.add("busk_musician")
        if len(done) != len(store.rare_outcome_seen):
            store.rare_outcome_seen = sorted(done)

    _p_rare_orig_new_day = new_day

    def new_day():
        _p_rare_orig_new_day()
        p_rare_sync()


# ── Rare reveal ───────────────────────────────────────────────────────────────
# A separator and a label, shown after the ordinary rewards have been read.
# Deliberately quiet: the point is "something extra happened", not a jackpot.

screen rare_reveal_row(text_line, header="LUCKY BREAK"):
    vbox:
        spacing 6
        xalign 0.5
        null height 4
        frame:
            background "#ffd66a20"
            padding (12, 6, 12, 8)
            xalign 0.5
            vbox:
                spacing 4
                text header:
                    font PROFILE_FONT size 12 color "#ffd66a" xalign 0.5
                text text_line:
                    font ACT_FONT size 13 color "#ffe9b0" xalign 0.5 xsize 380


# ── Debug ─────────────────────────────────────────────────────────────────────
# Read-only. The point of a stable-seeded rare is that you cannot re-roll it, so
# this panel deliberately offers no "force a rare" button — it shows what WOULD
# fire for the current day and the live cooldown/unique state instead. To test a
# specific branch, clear its cooldown and advance the day.

init python:
    def _dbg_rare_rows():
        """(activity, min_tier, pct, would_fire_now) for the current day."""
        out = []
        for aid in sorted(RARE_ACTIVITY_RULES):
            r = RARE_ACTIVITY_RULES[aid]
            pct = rare_pct_for(aid, "critical")
            fires = check_rare_outcome(aid, "critical", 1, r["min_tier"], pct)
            out.append((aid, r["min_tier"], pct, fires))
        return out


screen debug_rare_scr():
    modal True
    zorder 400
    add "#000000e0"
    frame:
        xalign 0.5 yalign 0.5
        xsize 860 ysize 640
        background "#0d1117f8"
        padding (24, 18, 24, 18)
        vbox:
            spacing 8
            text "RARE OUTCOMES — day [day]" font PROFILE_FONT size 20 color "#7fd06a"
            text "Read-only: rares are stable-seeded per (activity, day, attempt).":
                font ACT_FONT size 12 color "#4a6080"
            null height 6
            viewport:
                ysize 480
                scrollbars "vertical"
                mousewheel True
                vbox:
                    spacing 4
                    text "RULES  (attempt #1, top tier, this day)" font PROFILE_FONT size 14 color "#9fb6d6"
                    for _aid, _mt, _pct, _f in _dbg_rare_rows():
                        text ("  %-22s min=%-16s %3d%%   %s"
                              % (_aid, _mt, _pct, "WOULD FIRE" if _f else "-")):
                            font ACT_FONT size 13 color ("#ffd66a" if _f else "#cfe0f5")
                    null height 8
                    text "COOLDOWNS  (rare_id -> last fired)" font PROFILE_FONT size 14 color "#9fb6d6"
                    if not rare_outcome_last_day:
                        text "  (none yet)" font ACT_FONT size 13 color "#4a6080"
                    for _rid in sorted(rare_outcome_last_day):
                        text ("  %-28s day %d  (%d ago)"
                              % (_rid, rare_outcome_last_day[_rid],
                                 day - rare_outcome_last_day[_rid])):
                            font ACT_FONT size 13 color "#cfe0f5"
                    null height 8
                    text "UNIQUES CONSUMED" font PROFILE_FONT size 14 color "#9fb6d6"
                    if not rare_outcome_seen:
                        text "  (none yet)" font ACT_FONT size 13 color "#4a6080"
                    for _s in rare_outcome_seen:
                        text ("  " + _s) font ACT_FONT size 13 color "#c07ee6"
                    null height 8
                    text "OPPORTUNITY LEADS  (shared with world pulse)" font PROFILE_FONT size 14 color "#9fb6d6"
                    for _oid in sorted(RARE_OPPORTUNITY_TEMPLATES):
                        $ _last = _rare_opportunity_last.get(_oid, -999)
                        $ _cd = RARE_OPPORTUNITY_TEMPLATES[_oid]["cooldown_days"]
                        text ("  %-26s cd %2dd   %s"
                              % (_oid, _cd,
                                 "ready" if day - _last >= _cd
                                 else "blocked %dd" % (_cd - (day - _last)))):
                            font ACT_FONT size 13 color "#cfe0f5"
                    null height 8
                    text "MAIL BUDGET TODAY: [_pulse_mail_today] / [PULSE_MAX_MAIL_PER_DAY]":
                        font ACT_FONT size 13 color "#8fb0d0"
                    text "BAR CHALLENGER UNLOCKED: day [rare_bar_challenger]":
                        font ACT_FONT size 13 color "#8fb0d0"
            null height 6
            hbox:
                spacing 12
                textbutton "Clear all cooldowns":
                    action [SetVariable("rare_outcome_last_day", {}), Show("debug_rare_scr")]
                    text_size 14 text_color "#e8a24d"
                textbutton "Clear uniques":
                    action [SetVariable("rare_outcome_seen", []), Show("debug_rare_scr")]
                    text_size 14 text_color "#e8a24d"
                textbutton "Back":
                    action [Hide("debug_rare_scr"), Show("debug_menu")]
                    text_size 15 text_color "#7fd06a"
