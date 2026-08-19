# ── Zoe romantic milestone spine — M2 / M4 / M5 / M6 / M7 ────────────────────
# M3 (beach_after_dark) exists in locations.rpy (label zoe_beach_night_scene).
# M1 (spontaneous nightclub) exists in gameplay_expansion_scenes.rpy.
# This file owns M2 (first date + first kiss), M4 (ordinary home evening),
# M5 (group public recognition), M6 (commitment — location_terrace), M7 (love spoken).
#
# Trigger architecture:
#   M2 → phone invite (zoe_msg_first_date) → commitment → location_cafe check
#   M3 → location_sandbeach direct gate (can_trigger_zoe_beach_after_dark)
#   M4 → phone invite (zoe_msg_home_come_over) → commitment → location_home check
#   M6 → phone invite (zoe_msg_commitment_beach) → commitment → location_terrace check
#   M7 → direct eligibility check in location_home (no commitment needed)
#   M5 → coda of marcus_zoe_static_small_group in story_direct_pass.rpy

# ── Default store vars ────────────────────────────────────────────────────────

default zoe_first_date_done        = False
default zoe_first_date_pending     = False   # phone accepted, awaiting location visit
default zoe_first_date_target      = -1      # game day the date is set for
default zoe_first_date_declined_day = -1     # day of last "can't tomorrow" for cooldown
default zoe_dating_day             = -1      # set when first kiss lands

default zoe_beach_dating_done      = False   # M2 beach breakpoint completed
default zoe_beach_dating_pending   = False   # beach invite accepted, awaiting location visit
default zoe_beach_dating_declined_day = -1   # day of last "can't tonight" for cooldown

default zoe_home_no_reason_done    = False
default zoe_home_no_reason_day     = -1
default zoe_home_pending           = False
default zoe_home_pending_day       = -1
default zoe_home_declined_day      = -1

default zoe_m4_marcus_done         = False

default zoe_commitment_done        = False
default zoe_committed_day          = -1
default zoe_commitment_pending     = False
default zoe_commitment_pending_day = -1
default zoe_commitment_declined_day = -1

default zoe_love_spoken            = False
default zoe_love_spoken_day        = -1
default zoe_m6_pending             = False   # scene has started (prevents double-entry)


# ── Eligibility helpers + _commit_first_kiss ──────────────────────────────────

init python:

    def _zoe_m2_eligible():
        """M2 (Grounds first date) gate — DISABLED.
        The canonical M2 is now the beach dating breakpoint.
        The Grounds invite (zoe_msg_first_date) will not fire.
        """
        return False

    def _zoe_m2_beach_eligible():
        """M2 beach breakpoint gate.
        Zoe initiates naturally 1–3 eligible days after thresholds are met.
        """
        if store.zoe_beach_dating_done or store.zoe_beach_dating_pending:
            return False
        if relationship_memory_exists("zoe", "first_kiss_zoe"):
            return False
        if get_romance_state("zoe") != "interested":
            return False
        # 2+ days since interest became explicit
        state_day = store.romance_last_choice_day.get("zoe", 0)
        if store.day - state_day < 2:
            return False
        # 3-day window after last "can't tonight"
        if store.day - store.zoe_beach_dating_declined_day < 3:
            return False
        aff = npc_aff("zoe")
        tr  = npc_trust("zoe")
        fam = npc_rel("zoe", "familiarity")
        if aff < 50 or tr < 45 or fam < 45:
            return False
        return True

    def _zoe_m3_eligible():
        """M3 (home evening) gate."""
        if store.zoe_home_no_reason_done or store.zoe_home_pending:
            return False
        if get_romance_state("zoe") != "dating":
            return False
        if not relationship_memory_exists("zoe", "first_kiss_zoe"):
            return False
        if not store.zoe_first_date_done:
            return False
        dating_day = store.zoe_dating_day if store.zoe_dating_day > 0 else \
                     store.romance_last_choice_day.get("zoe", 0)
        if store.day - dating_day < 3:
            return False
        if store.day - store.zoe_home_declined_day < 4:
            return False
        tr  = npc_trust("zoe")
        fam = npc_rel("zoe", "familiarity")
        return tr >= 50 and fam >= 55

    def _zoe_m5_eligible():
        """M5 (commitment) gate."""
        if store.zoe_commitment_done or store.zoe_commitment_pending:
            return False
        if get_romance_state("zoe") != "dating":
            return False
        if not relationship_memory_exists("zoe", "first_kiss_zoe"):
            return False
        dating_day = store.zoe_dating_day if store.zoe_dating_day > 0 else \
                     store.romance_last_choice_day.get("zoe", 0)
        if store.day - dating_day < 10:
            return False
        if store.day - store.zoe_commitment_declined_day < 7:
            return False
        aff = npc_aff("zoe")
        tr  = npc_trust("zoe")
        fam = npc_rel("zoe", "familiarity")
        if aff < 60 or tr < 65 or fam < 65:
            return False
        # M3 — Beach After Dark must have happened before commitment
        if not store.zoe_beach_night_done:
            return False
        # M4 — home evening must have happened before commitment
        if not store.zoe_home_no_reason_done:
            return False
        # Vulnerability / personal memory (any one of these)
        _vuln = [
            "zoe_coffee_not_advice", "zoe_just_stay_done_mem",
            "zoe_not_ready_shown",   "zoe_spontaneous_direction_romance",
            "zoe_after_deadline",
        ]
        if not any(relationship_memory_exists("zoe", m) for m in _vuln):
            return False
        # Friction/repair — at least one repaired tension cycle, OR high-trust bypass
        _friction_done = (
            (store.rc_zoe_f1_done and store.rc_zoe_repair_done)
            or (store.rc_zoe_f2_done and store.rc_zoe_repair_done)
            or (store.zoe_disagreement_done and store.zoe_disagreement_repair_done)
        )
        if not _friction_done and not (tr >= 75 and fam >= 75):
            return False
        return True

    def can_trigger_zoe_beach_after_dark():
        """Gate for the Beach After Dark scene (M3 in spine).
        Called from locations.rpy / label location_sandbeach.
        """
        if store.zoe_beach_night_done:
            return False
        if get_romance_state("zoe") != "dating":
            return False
        if not relationship_memory_exists("zoe", "first_kiss_zoe"):
            return False
        if not store.zoe_first_date_done:
            return False
        dating_day = store.zoe_dating_day if store.zoe_dating_day > 0 else \
                     store.romance_last_choice_day.get("zoe", 0)
        if store.day - dating_day < 2:
            return False
        if store.hour < 20:
            return False
        return True

    def _migrate_zoe_beach_after_dark():
        """Old-save: committed players legitimately passed the M3 period — mark done.
        Guards against the repositioned scene re-firing on saves that advanced
        past dating before Beach After Dark was a requirement.
        """
        if store.zoe_beach_night_done:
            return
        if store.zoe_commitment_done:
            store.zoe_beach_night_done = True

    if _migrate_zoe_beach_after_dark not in config.after_load_callbacks:
        config.after_load_callbacks.append(_migrate_zoe_beach_after_dark)

    def _zoe_m6_eligible():
        """M6 (love spoken) gate."""
        if store.zoe_love_spoken or store.zoe_m6_pending:
            return False
        if get_romance_state("zoe") != "committed":
            return False
        if not store.zoe_commitment_done:
            return False
        committed_day = store.zoe_committed_day if store.zoe_committed_day > 0 else \
                        store.romance_last_choice_day.get("zoe", 0)
        if store.day - committed_day < 10:
            return False
        tr  = npc_trust("zoe")
        fam = npc_rel("zoe", "familiarity")
        if tr < 70 or fam < 70:
            return False
        if not store.zoe_home_no_reason_done:
            return False
        # 2+ meaningful memories
        _mem = [
            "first_kiss_zoe", "zoe_first_date", "zoe_home_no_reason",
            "zoe_coffee_not_advice", "zoe_just_stay_done_mem",
            "zoe_spontaneous_direction_romance",
        ]
        if sum(1 for m in _mem if relationship_memory_exists("zoe", m)) < 2:
            return False
        return True

    def _commit_first_kiss(npc_id):
        """Central first-kiss state mutation.
        Called by do_kiss() (via its first-kiss branch) and the M2 authored scene.
        ponytail: do_kiss() already checks relationship_memory_exists before calling here;
        the authored M2 scene also guards — do not remove either guard.
        """
        kp = KISS_PROFILES.get(npc_id, {})
        add_relationship_memory(npc_id, "first_kiss_" + npc_id, "First kiss")
        _apply_aff(npc_id, kp.get("aff_gain", 5))
        _apply_trust(npc_id, kp.get("trust_gain", 3))
        if get_romance_state(npc_id) == "interested":
            set_romance_state(npc_id, "dating", source="first_kiss")
        _lk = dict(store.npc_last_kiss_day)
        _lk[npc_id] = store.day
        store.npc_last_kiss_day = _lk
        _fa = dict(store.failed_physical_attempts)
        _fa[(npc_id, "kiss")] = 0
        store.failed_physical_attempts = _fa


# ── Old-save migration ────────────────────────────────────────────────────────

init python:
    def _zoe_romance_milestone_backfill():
        """Conservative old-save repair. Runs on every load; all branches are idempotent."""
        import store
        _rs = get_romance_state("zoe")
        _has_fk = relationship_memory_exists("zoe", "first_kiss_zoe")

        # Case B: first kiss exists but milestone flags missing
        if _has_fk:
            if not store.zoe_first_date_done:
                store.zoe_first_date_done = True
            if store.zoe_dating_day < 0:
                _sd = store.romance_last_choice_day.get("zoe", 0)
                store.zoe_dating_day = _sd if _sd > 0 else max(0, store.day - 15)

        # Case C: already committed
        if _rs == "committed":
            if not store.zoe_first_date_done:
                store.zoe_first_date_done = True
            if not store.zoe_commitment_done:
                store.zoe_commitment_done = True
            if store.zoe_committed_day < 0:
                _sd = store.romance_last_choice_day.get("zoe", 0)
                store.zoe_committed_day = _sd if _sd > 0 else max(0, store.day - 10)
            if store.zoe_dating_day < 0:
                store.zoe_dating_day = max(0, store.zoe_committed_day - 12)

        # Case D: old save has first_kiss memory but state is still "interested"
        # (invariant violation: first_kiss implies dating)
        if _has_fk and _rs == "interested":
            set_romance_state("zoe", "dating", source="milestone_backfill")
            if store.zoe_dating_day < 0:
                store.zoe_dating_day = max(0, store.day - 12)

        # Beach dating breakpoint (M2): backfill for saves that reached dating via
        # the old Grounds route or any other pre-beach-M2 path.
        if not store.zoe_beach_dating_done:
            if _has_fk or _rs in ("dating", "committed", "paused", "closed"):
                store.zoe_beach_dating_done = True
        # Cancel stale pending for the old Grounds invite if beach route is now active
        if store.zoe_beach_dating_done and store.zoe_first_date_pending:
            store.zoe_first_date_pending = False

        # Cancel any stale pending flags from a crash/rollback
        if store.zoe_first_date_done and store.zoe_first_date_pending:
            store.zoe_first_date_pending = False
        if store.zoe_beach_dating_done and store.zoe_beach_dating_pending:
            store.zoe_beach_dating_pending = False
        if store.zoe_home_no_reason_done and store.zoe_home_pending:
            store.zoe_home_pending = False
        if store.zoe_commitment_done and store.zoe_commitment_pending:
            store.zoe_commitment_pending = False

    config.after_load_callbacks.append(_zoe_romance_milestone_backfill)


# ── Phone initiative extensions ───────────────────────────────────────────────
# Added at init 5 — after phone_actionable.rpy (init 0) and zoe_arc.rpy (init 3).

init 5 python:

    # Response dicts — same format as phone_actionable.rpy

    _ZOE_BEACH_DATING_RESP = [
        {"id": "ok",    "text": "Everything okay?", "label": "npc_ini_zoe_bdating_ok"},
        {"id": "nine",  "text": "Nine?",             "label": "npc_ini_zoe_bdating_nine"},
        {"id": "cant",  "text": "Can't tonight.",    "label": "npc_ini_zoe_bdating_cant"},
    ]
    _ZOE_FIRST_DATE_RESP = [
        {"id": "specific", "text": "That's oddly specific.",  "label": "npc_ini_zoe_fdate_specific"},
        {"id": "there",    "text": "I'll be there.",          "label": "npc_ini_zoe_fdate_there"},
        {"id": "cant",     "text": "Can't tomorrow.",         "label": "npc_ini_zoe_fdate_cant"},
    ]
    _ZOE_HOME_COME_OVER_RESP = [
        {"id": "thirty",   "text": "Thirty-one?",             "label": "npc_ini_zoe_home_thirty"},
        {"id": "come",     "text": "Come over.",              "label": "npc_ini_zoe_home_come"},
        {"id": "bad",      "text": "Bad night.",              "label": "npc_ini_zoe_home_bad"},
    ]
    _ZOE_COMMITMENT_BEACH_RESP = [
        {"id": "ok",       "text": "Everything okay?",        "label": "npc_ini_zoe_cbeach_ok"},
        {"id": "there",    "text": "I'll be there.",          "label": "npc_ini_zoe_cbeach_there"},
        {"id": "not",      "text": "Not tonight.",            "label": "npc_ini_zoe_cbeach_not"},
    ]
    _ZOE_DATING_FREE_RESP = [
        {"id": "yes",      "text": "I'm free.",               "label": "npc_ini_zoe_dfree_yes"},
        {"id": "later",    "text": "Later tonight.",          "label": "npc_ini_zoe_dfree_later"},
        {"id": "no",       "text": "Busy tonight.",           "label": "npc_ini_zoe_dfree_no"},
    ]
    _ZOE_DATING_GROUNDS_RESP = [
        {"id": "yes",      "text": "On my way.",              "label": "npc_ini_zoe_dgrounds_yes"},
        {"id": "late",     "text": "Give me an hour.",        "label": "npc_ini_zoe_dgrounds_late"},
        {"id": "no",       "text": "Can't today.",            "label": "npc_ini_zoe_dgrounds_no"},
    ]
    _ZOE_DATING_DAYS_RESP = [
        {"id": "sorry",    "text": "I know. Sorry.",          "label": "npc_ini_zoe_ddays_sorry"},
        {"id": "fix",      "text": "Let's fix that.",         "label": "npc_ini_zoe_ddays_fix"},
        {"id": "been",     "text": "Has it really?",          "label": "npc_ini_zoe_ddays_been"},
    ]
    _ZOE_COMMITTED_OVER_RESP = [
        {"id": "yes",      "text": "Come over.",              "label": "npc_ini_zoe_cover_yes"},
        {"id": "bit",      "text": "Give me a bit.",          "label": "npc_ini_zoe_cover_bit"},
        {"id": "not",      "text": "Not tonight.",            "label": "npc_ini_zoe_cover_not"},
    ]
    _ZOE_COMMITTED_GROUNDS_RESP = [
        {"id": "yes",      "text": "Sounds good.",            "label": "npc_ini_zoe_cgr_yes"},
        {"id": "late",     "text": "Give me an hour.",        "label": "npc_ini_zoe_cgr_late"},
        {"id": "no",       "text": "Can't today.",            "label": "npc_ini_zoe_cgr_no"},
    ]
    _ZOE_COMMITTED_DAYS_RESP = [
        {"id": "sorry",    "text": "I know. Sorry.",          "label": "npc_ini_zoe_cdays_sorry"},
        {"id": "fix",      "text": "Let's fix that.",         "label": "npc_ini_zoe_cdays_fix"},
    ]
    _ZOE_COMMITTED_SAW_RESP = [
        {"id": "when",     "text": "When do I get to see it?","label": "npc_ini_zoe_csaw_when"},
        {"id": "ominous",  "text": "That's ominous.",         "label": "npc_ini_zoe_csaw_ominous"},
    ]

    # Extend _INITIATIVE_MSGS
    _INITIATIVE_MSGS.update({
        "zoe_msg_beach_dating": {
            "text": "Beach later?",
            "responses": _ZOE_BEACH_DATING_RESP,
        },
        "zoe_msg_first_date": {
            "text": "Grounds. Tomorrow. Five. No sketchbook.",
            "responses": _ZOE_FIRST_DATE_RESP,
        },
        "zoe_msg_home_come_over": {
            "text": "Your place tonight? I have food and a film with a 31% audience score.",
            "responses": _ZOE_HOME_COME_OVER_RESP,
        },
        "zoe_msg_commitment_beach": {
            "text": "Riverside terrace. After nine. I'll be there.",
            "responses": _ZOE_COMMITMENT_BEACH_RESP,
        },
        "zoe_msg_dating_free": {
            "text": "You free later or am I pretending not to ask?",
            "responses": _ZOE_DATING_FREE_RESP,
        },
        "zoe_msg_dating_grounds": {
            "text": "Grounds. Same table. I already stole the good chair.",
            "responses": _ZOE_DATING_GROUNDS_RESP,
        },
        "zoe_msg_dating_days": {
            "text": "Haven't seen you in four days. This is now objectively excessive.",
            "responses": _ZOE_DATING_DAYS_RESP,
        },
        "zoe_msg_committed_over": {
            "text": "Thinking of coming over later. Bad night?",
            "responses": _ZOE_COMMITTED_OVER_RESP,
        },
        "zoe_msg_committed_grounds": {
            "text": "Grounds after work?\nNo reason.",
            "responses": _ZOE_COMMITTED_GROUNDS_RESP,
        },
        "zoe_msg_committed_days": {
            "text": "Four days.\nThis is objectively too long now.",
            "responses": _ZOE_COMMITTED_DAYS_RESP,
        },
        "zoe_msg_committed_saw": {
            "text": "Saw something you'd hate. Saved it for when I see you.",
            "responses": _ZOE_COMMITTED_SAW_RESP,
        },
    })

    # Extend _INITIATIVE_VARIANTS["zoe"]
    _INITIATIVE_VARIANTS["zoe"] = list(_INITIATIVE_VARIANTS["zoe"]) + [
        "zoe_msg_first_date",
        "zoe_msg_beach_dating",
        "zoe_msg_home_come_over",
        "zoe_msg_commitment_beach",
        "zoe_msg_dating_free",
        "zoe_msg_dating_grounds",
        "zoe_msg_dating_days",
        "zoe_msg_committed_over",
        "zoe_msg_committed_grounds",
        "zoe_msg_committed_days",
        "zoe_msg_committed_saw",
    ]

    # Invitation-type variants (excluded when npc_invitation_pending is set)
    # ponytail: milestone invites use dedicated pending flags not npc_invitation_pending,
    # so they don't block standard invitations — only add to _INV_VARIANTS if that logic changes.
    # For now, they're gated via _VARIANT_CONDITIONS which checks the pending flag directly.

    # Date-route variants — require romance_is_open
    _DATE_VARIANTS.add("zoe_msg_beach_dating")
    _DATE_VARIANTS.add("zoe_msg_first_date")
    _DATE_VARIANTS.add("zoe_msg_commitment_beach")

    # Weights
    _VARIANT_WEIGHTS.update({
        "zoe_msg_beach_dating":     2,
        "zoe_msg_first_date":       2,
        "zoe_msg_home_come_over":   2,
        "zoe_msg_commitment_beach": 2,
        "zoe_msg_dating_free":      2,
        "zoe_msg_dating_grounds":   2,
        "zoe_msg_dating_days":      2,
        "zoe_msg_committed_over":   2,
        "zoe_msg_committed_grounds":2,
        "zoe_msg_committed_days":   2,
        "zoe_msg_committed_saw":    2,
    })

    # Min texting tier (CLOSE = 2 for all romance/milestone variants)
    _VARIANT_MIN_TIER.update({
        "zoe_msg_beach_dating":     2,
        "zoe_msg_first_date":       2,
        "zoe_msg_home_come_over":   2,
        "zoe_msg_commitment_beach": 2,
        "zoe_msg_dating_free":      2,
        "zoe_msg_dating_grounds":   2,
        "zoe_msg_dating_days":      2,
        "zoe_msg_committed_over":   2,
        "zoe_msg_committed_grounds":2,
        "zoe_msg_committed_days":   2,
        "zoe_msg_committed_saw":    2,
    })

    # Extra eligibility conditions
    _VARIANT_CONDITIONS.update({
        "zoe_msg_beach_dating": lambda: _zoe_m2_beach_eligible(),
        "zoe_msg_first_date": lambda: _zoe_m2_eligible(),
        "zoe_msg_home_come_over": lambda: _zoe_m3_eligible(),
        "zoe_msg_commitment_beach": lambda: _zoe_m5_eligible(),
        "zoe_msg_dating_free": lambda: (
            get_romance_state("zoe") in ("dating", "committed")
        ),
        "zoe_msg_dating_grounds": lambda: (
            get_romance_state("zoe") in ("dating", "committed")
        ),
        "zoe_msg_dating_days": lambda: (
            get_romance_state("zoe") in ("dating", "committed")
        ),
        "zoe_msg_committed_over": lambda: get_romance_state("zoe") == "committed",
        "zoe_msg_committed_grounds": lambda: get_romance_state("zoe") == "committed",
        "zoe_msg_committed_days": lambda: get_romance_state("zoe") == "committed",
        "zoe_msg_committed_saw": lambda: get_romance_state("zoe") == "committed",
    })

    # Add "zoe" entry to _MISSED_TEXTS so missed milestone commitments get a response
    try:
        _MISSED_TEXTS["zoe"] = "Fine. Another day."
    except (NameError, AttributeError):
        pass


# ── Phone reply labels ────────────────────────────────────────────────────────

# M2 — First date invite replies

label npc_ini_zoe_fdate_specific:
    $ queue_phone_message("zoe", "I'm experimenting with clarity.", day, "zoe_fdate_r1a")
    $ queue_phone_message("zoe", "Don't make me regret it.", day + 1, "zoe_fdate_r1b")
    $ add_commitment("zoe_first_date_1", "zoe", "Coffee with Zoe at Grounds", day + 1, 17, "location_cafe", "zoe_first_date_scene", grace=4.0)
    $ store.zoe_first_date_pending = True
    $ store.zoe_first_date_target  = day + 1
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_fdate_there:
    $ queue_phone_message("zoe", "Good.", day, "zoe_fdate_r2")
    $ add_commitment("zoe_first_date_1", "zoe", "Coffee with Zoe at Grounds", day + 1, 17, "location_cafe", "zoe_first_date_scene", grace=4.0)
    $ store.zoe_first_date_pending = True
    $ store.zoe_first_date_target  = day + 1
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_fdate_cant:
    $ queue_phone_message("zoe", "Fine.", day, "zoe_fdate_r3a")
    $ queue_phone_message("zoe", "Another day.", day, "zoe_fdate_r3b")
    $ store.zoe_first_date_declined_day = day
    $ _clear_initiative_pending("zoe")
    return


# M2 — Beach dating invite replies

label npc_ini_zoe_bdating_ok:
    $ queue_phone_message("zoe", "Yeah.", day, "zoe_bdating_r1a")
    $ queue_phone_message("zoe", "That's why I'm asking.", day, "zoe_bdating_r1b")
    $ add_commitment("zoe_beach_dating_1", "zoe", "Beach with Zoe", day, 21, "location_sandbeach", "zoe_beach_dating_scene", grace=3.0)
    $ store.zoe_beach_dating_pending = True
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_bdating_nine:
    $ queue_phone_message("zoe", "Nine.", day, "zoe_bdating_r2")
    $ add_commitment("zoe_beach_dating_1", "zoe", "Beach with Zoe", day, 21, "location_sandbeach", "zoe_beach_dating_scene", grace=3.0)
    $ store.zoe_beach_dating_pending = True
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_bdating_cant:
    $ queue_phone_message("zoe", "Fine.", day, "zoe_bdating_r3a")
    $ queue_phone_message("zoe", "Another night.", day + 1, "zoe_bdating_r3b")
    $ store.zoe_beach_dating_declined_day = day
    $ _clear_initiative_pending("zoe")
    return


# M3 — Home invite replies

label npc_ini_zoe_home_thirty:
    $ queue_phone_message("zoe", "Exactly.", day, "zoe_home_r1")
    $ add_commitment("zoe_home_no_reason_1", "zoe", "Zoe coming over", day, 19, "location_home", "zoe_home_no_reason_scene", grace=3.0)
    $ store.zoe_home_pending     = True
    $ store.zoe_home_pending_day = day
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_home_come:
    $ queue_phone_message("zoe", "Good.", day, "zoe_home_r2")
    $ add_commitment("zoe_home_no_reason_1", "zoe", "Zoe coming over", day, 19, "location_home", "zoe_home_no_reason_scene", grace=3.0)
    $ store.zoe_home_pending     = True
    $ store.zoe_home_pending_day = day
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_home_bad:
    $ queue_phone_message("zoe", "Fine. The film will remain terrible tomorrow.", day, "zoe_home_r3")
    $ store.zoe_home_declined_day = day
    $ _clear_initiative_pending("zoe")
    return


# M5 — Commitment beach invite replies

label npc_ini_zoe_cbeach_ok:
    $ queue_phone_message("zoe", "Yes.", day, "zoe_cbeach_r1a")
    $ queue_phone_message("zoe", "That's why I'm asking before something goes wrong.", day, "zoe_cbeach_r1b")
    $ add_commitment("zoe_commitment_beach_1", "zoe", "Terrace with Zoe", day, 20, "location_terrace", "zoe_commitment_beach_scene", grace=3.0)
    $ store.zoe_commitment_pending     = True
    $ store.zoe_commitment_pending_day = day
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_cbeach_there:
    $ queue_phone_message("zoe", "Good.", day, "zoe_cbeach_r2")
    $ add_commitment("zoe_commitment_beach_1", "zoe", "Terrace with Zoe", day, 20, "location_terrace", "zoe_commitment_beach_scene", grace=3.0)
    $ store.zoe_commitment_pending     = True
    $ store.zoe_commitment_pending_day = day
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_cbeach_not:
    $ queue_phone_message("zoe", "Okay.", day, "zoe_cbeach_r3a")
    $ queue_phone_message("zoe", "Another night.", day + 1, "zoe_cbeach_r3b")
    $ store.zoe_commitment_declined_day = day
    $ _clear_initiative_pending("zoe")
    return


# Dating reactive replies (low-pressure; no commitment created)

label npc_ini_zoe_dfree_yes:
    $ queue_phone_message("zoe", "Good.", day, "zoe_dfree_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_dfree_later:
    $ queue_phone_message("zoe", "Fine.", day, "zoe_dfree_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_dfree_no:
    $ queue_phone_message("zoe", "Fine. Tomorrow exists.", day + 1, "zoe_dfree_r3")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_dgrounds_yes:
    $ queue_phone_message("zoe", "Good.", day, "zoe_dgr_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_dgrounds_late:
    $ queue_phone_message("zoe", "The chair will be here.", day, "zoe_dgr_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_dgrounds_no:
    $ queue_phone_message("zoe", "Fine. Tomorrow exists.", day + 1, "zoe_dgr_r3")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_ddays_sorry:
    $ queue_phone_message("zoe", "I know.", day, "zoe_ddays_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_ddays_fix:
    $ queue_phone_message("zoe", "Good.", day, "zoe_ddays_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_ddays_been:
    $ queue_phone_message("zoe", "Objectively.", day, "zoe_ddays_r3")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_cover_yes:
    $ queue_phone_message("zoe", "Good.", day, "zoe_cover_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_cover_bit:
    $ queue_phone_message("zoe", "Fine.", day, "zoe_cover_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_cover_not:
    $ queue_phone_message("zoe", "Fine. Tomorrow exists.", day + 1, "zoe_cover_r3")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_cgr_yes:
    $ queue_phone_message("zoe", "Good.", day, "zoe_cgr_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_cgr_late:
    $ queue_phone_message("zoe", "The chair will be here.", day, "zoe_cgr_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_cgr_no:
    $ queue_phone_message("zoe", "Fine. Tomorrow exists.", day + 1, "zoe_cgr_r3")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_cdays_sorry:
    $ queue_phone_message("zoe", "I know.", day, "zoe_cdays_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_cdays_fix:
    $ queue_phone_message("zoe", "Good.", day, "zoe_cdays_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_csaw_when:
    $ queue_phone_message("zoe", "When I see you.", day, "zoe_csaw_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_csaw_ominous:
    $ queue_phone_message("zoe", "Exactly.", day, "zoe_csaw_r2")
    $ _clear_initiative_pending("zoe")
    return


# ── M2 — PAST TENSE IS SAFER ─────────────────────────────────────────────────
# First deliberate date + first kiss.
# Triggered from location_cafe when commitment_available("zoe_first_date_1").

label zoe_first_date_scene:
    $ story_scene_active = True
    $ clear_npc_sprites()
    hide screen npc_relbar
    hide screen npc_actions
    hide screen hud

    # ── PART 1: Grounds ───────────────────────────────────────────────────────
    scene expression cafe_bg() with dissolve
    show screen hud
    # DIRECTOR CG SLOT: zoe_first_date / Zoe at corner table, no sketchbook, two coffees, waiting
    show zoe_street_neutral as npcsprite at sprite_center

    "Zoe is already at the bad table with the good light."
    "There is no sketchbook in front of her."
    "No laptop either."

    z "You're late."
    mc "By two minutes."
    z "I arrived early."
    z "I needed the moral advantage."
    mc "No sketchbook."
    z "Don't make it weird."
    mc "I haven't said anything."
    z "You looked at my hands."
    mc "Apparently that's weird now."
    z "Tonight? Slightly."

    "She pushes a coffee toward you."
    mc "You ordered for me?"
    z "I made an educated guess."
    mc "And if it's wrong?"
    z "Then this ends very early."

    pause 0.3

    mc "What exactly is this?"
    z "Coffee."
    mc "Right."
    z "You asked."
    mc "I didn't."
    z "Your face did."
    mc "My face needs boundaries."
    z "Desperately."

    pause 0.3

    z "Walk?"
    mc "Where?"
    z "I was hoping you wouldn't ask."
    mc "Strong plan."
    z "Thank you."

    # ── PART 2: Walk ──────────────────────────────────────────────────────────
    scene expression ("centerstreet_night" if hour >= 19 else "centerstreet_day") with dissolve
    show zoe_street_neutral as npcsprite at sprite_r
    show screen hud
    # DIRECTOR CG SLOT: zoe_first_date / Evening walk through Quayside, both heading nowhere, ordinary conversation body language

    "You leave Grounds without deciding on a destination."
    "For a while the conversation goes nowhere useful."
    "A bad storefront sign."
    "Someone cycling where they shouldn't."
    "The temperature dropping faster than either of you dressed for."

    z "I've been thinking about the club."
    mc "That's dangerous."
    z "Not the whole night."

    pause 0.5

    z "One very specific thirty seconds."
    mc "The part you didn't walk back?"
    z "Yes."
    z "Congratulations on making that sentence worse."
    mc "I've had time to refine it."
    z "Clearly."

    pause 0.3

    z "I don't want to keep doing that."
    mc "Walking things back?"
    z "Pretending I don't know what I'm doing."
    mc "Do you?"
    z "No."
    z "But apparently that's not stopping me."

    # ── PART 3: Decision — Riverside Terrace ─────────────────────────────────
    scene sandbeach_night with dissolve
    show zoe_street_neutral as npcsprite at sprite_center
    show screen hud
    # DIRECTOR CG SLOT: zoe_first_date / Riverside Terrace at night, before the decision menu

    menu:
        "\"Then don't.\"" if renpy.has_label("zoe_first_date_kiss"):
            jump zoe_first_date_branch_a
        "\"I like this. I'm just not ready yet.\"":
            jump zoe_first_date_branch_b
        "\"I think we're better as friends.\"":
            jump zoe_first_date_branch_c

    # ── BRANCH A — Romantic ───────────────────────────────────────────────────
    label zoe_first_date_branch_a:
        mc "Then don't."
        z "..."
        z "Okay."
        mc "Okay?"
        z "I'm trying brevity."
        mc "How's it going?"
        z "Badly."

        pause 0.4

        z "Also, for the record—"
        mc "Yeah?"
        z "This was a date."
        mc "Was?"
        z "Past tense is safer."
        mc "And now?"
        z "Now you're making me do all the difficult parts."
        mc "Which part?"

        $ show_npc_expr("zoe", "talk")
        z "This one."

        # =====================================================================
        # DIRECTOR HANDOFF
        #
        # CREATE FILE:
        # game/director_romance/zoe_first_date_romance.rpy
        #
        # REQUIRED LABEL:
        # zoe_first_date_kiss
        #
        # ENTRY MOMENT:
        # Zoe says "This one." and moves closer — Riverside Terrace at night.
        # Background: sandbeach_night. Sprite: zoe_street_neutral at sprite_center.
        #
        # ENTRY STATE:
        # get_romance_state("zoe") == "interested"
        # relationship_memory_exists("zoe", "first_kiss_zoe") == False
        # zoe_first_date_done == False
        #
        # DIRECTOR-OWNED CONTENT:
        # CG-driven first-kiss sequence (approach CG + kiss CG).
        # Director label must call:
        #   _commit_first_kiss("zoe")
        #   store.zoe_dating_day = store.day
        # =====================================================================
        if renpy.has_label("zoe_first_date_kiss"):
            call zoe_first_date_kiss

            # DIRECTOR CG SLOT: zoe_first_date / After first kiss — small gap restored, genuine smile, not quite composed

            "For a second neither of you moves."
            z "That was..."
            mc "Careful."
            z "Don't."
            mc "You were about to review it."
            z "I was going to say good."
            mc "That's worse."
            z "I know."

            $ show_npc_expr("zoe", "laugh")

            z "Walk me home?"
            mc "Yeah."
            z "Good."

            # Milestone bookkeeping
            $ zoe_first_date_done   = True
            $ zoe_first_date_pending = False
            $ complete_commitment("zoe_first_date_1")
            $ add_relationship_memory("zoe", "zoe_first_date", "Coffee, the long walk, and the first kiss")
            $ apply_relationship_change("zoe", "zoe_first_date", "authored", familiarity=3, attraction=4)
            $ story_scene_active = False
            jump location_cafe
        else:
            if config.developer:
                $ renpy.notify("DIRECTOR SUBSCENE MISSING: zoe_first_date_kiss")
            # Director subscene absent — reconverge as "not yet", no kiss, no state change.
            $ store.zoe_first_date_declined_day = day
            $ store.zoe_first_date_pending = False
            $ cancel_commitment("zoe_first_date_1")
            $ story_scene_active = False
            jump location_cafe

    # ── BRANCH B — Not ready ──────────────────────────────────────────────────
    label zoe_first_date_branch_b:
        mc "I like this."
        mc "I'm just not ready yet."
        z "..."
        z "Okay."
        mc "Okay?"
        z "That's an actual answer."
        z "I'm not going to argue with an actual answer."
        mc "I don't want this to get weird."
        z "It was already weird."
        z "We'll survive."
        "She bumps her shoulder lightly against yours as you start walking again."

        # Cooldown — retry possible after 5+ days; not-ready does NOT set first_date_done
        $ store.zoe_first_date_declined_day = day
        $ store.zoe_first_date_pending = False
        $ cancel_commitment("zoe_first_date_1")
        $ story_scene_active = False
        jump location_cafe

    # ── BRANCH C — Friends ────────────────────────────────────────────────────
    label zoe_first_date_branch_c:
        mc "I think we're better as friends."
        "She looks away for a second."
        z "Okay."
        mc "Zoe—"
        z "No."
        z "I mean it."

        pause 0.4

        z "Give me a day to be annoyed at the universe."
        z "Not you."
        mc "Fair."
        z "And don't disappear."
        z "That would make it dramatic."

        # Route to "friends" — reopenable via existing romance-reopen architecture
        $ set_romance_state("zoe", "friends", source="zoe_first_date_friends")
        $ store.zoe_first_date_pending = False
        $ cancel_commitment("zoe_first_date_1")
        $ story_scene_active = False
        jump location_cafe


# ── M2 — BEACH DATING BREAKPOINT ─────────────────────────────────────────────
# Canonical interested -> dating scene. Zoe invites MC to the beach at night.
# Triggered from location_sandbeach when commitment_available("zoe_beach_dating_1").
# Director subscene: game/director_romance/romantic_subscene_zoe_beach_dating.rpy

label zoe_beach_dating_scene:
    $ zoe_beach_dating_pending = False
    $ story_scene_active = True
    $ clear_npc_sprites()
    hide screen npc_relbar
    hide screen npc_actions
    hide screen hud

    scene beachnight with dissolve
    show screen hud
    show zoe_beach_neutral as npcsprite at sprite_r

    "Zoe is already near the water when you get there."
    "She notices you before you say anything."
    z "You came."
    mc "You invited me."
    z "I know."
    mc "Strong start."
    z "I'm establishing facts."
    mc "Any others?"
    z "Not yet."

    pause 0.4

    mc "You've been here long?"
    z "Ten minutes."
    mc "That's very exact."
    z "I checked because I knew you'd ask."
    mc "You planned this conversation badly."
    z "Extensively."

    # They start walking.
    hide npcsprite

    "For a while, neither of you says anything useful."
    "The water keeps reaching slightly farther up the sand and then changing its mind."

    mc "You haven't told me why I'm here."
    z "I said beach."
    mc "That's a location."
    z "Technically also an activity."
    mc "Standing?"
    z "Walking."
    mc "We're doing very well."
    z "Give it time."

    pause 0.4

    z "I've been thinking about the club."
    mc "There it is."
    z "Don't sound pleased."
    mc "I'm not."
    z "You are."
    mc "A little."
    z "Annoying."

    # Callback to the nightclub moment.
    z "You remember what you said?"
    mc "Depends which part."
    z "The part where you decided I was walking something back."
    mc "You said you weren't."
    z "I wasn't."

    pause 0.3

    mc "Okay."
    z "That's it?"
    mc "You want me to argue?"
    z "No."
    mc "Then okay."

    "She watches him for a moment."

    z "This is why talking to you is occasionally a problem."
    mc "Because I listen?"
    z "Because sometimes you do."

    # Deeper turn — they stop somewhere quieter.
    show zoe_beach_neutral as npcsprite at sprite_r
    $ show_npc_expr("zoe", "neutral")

    "They stop somewhere quieter along the beach."

    z "I thought it would get less obvious."
    mc "What would?"
    z "This."
    mc "Very descriptive."
    z "You know what I mean."
    mc "I do."

    pause 0.3

    z "That's also annoying."
    mc "Sorry."
    z "You're not."
    mc "No."
    z "Right."

    pause 0.5

    z "Before the club, I could pretend I hadn't decided anything."
    mc "And after?"
    z "After was less convenient."
    mc "Zoe."
    z "I know."
    mc "Do you?"
    z "Unfortunately."

    "She looks away toward the water."

    $ show_npc_expr("zoe", "talk")

    z "I like seeing you."
    z "Not accidentally."
    z "Not because Marcus is somewhere nearby."
    z "Not because I happen to be working."
    z "Just..."

    pause 0.5

    z "You."

    pause 0.6

    mc "That's inconvenient."

    "She looks back at him."

    z "Extremely."
    mc "For what it's worth—"
    z "Don't."
    mc "Don't what?"
    z "Make it easier before I've finished."

    pause 0.3

    z "I don't want to keep pretending I don't know what I'm doing."
    mc "Do you know?"
    z "No."

    pause 0.3

    z "But apparently that's not stopping me."

    # =====================================================================
    # DIRECTOR HANDOFF
    #
    # CREATE FILE:
    # game/director_romance/romantic_subscene_zoe_beach_dating.rpy
    #
    # REQUIRED LABEL:
    # romantic_subscene_zoe_beach_dating
    #
    # ENTRY LINE:
    # z "But apparently that's not stopping me."
    #
    # ENTRY STATE:
    # get_romance_state("zoe") == "interested"
    # relationship_memory_exists("zoe", "first_kiss_zoe") == False
    #
    # PURPOSE:
    # CG-driven romantic resolution. Director owns: final choices,
    # kiss/no-kiss presentation, first-kiss helper where applicable,
    # interested -> dating transition if successful, retry state if not.
    #
    # RETURN:
    # plain return
    # =====================================================================

    if renpy.has_label("romantic_subscene_zoe_beach_dating"):
        call romantic_subscene_zoe_beach_dating
    else:
        if renpy.config.developer:
            $ renpy.notify("DIRECTOR SUBSCENE MISSING: romantic_subscene_zoe_beach_dating")
        # Cannot resolve breakpoint without director content. Set retry cooldown.
        $ store.zoe_beach_dating_declined_day = day
        $ store.zoe_beach_dating_pending = False
        $ cancel_commitment("zoe_beach_dating_1")
        $ story_scene_active = False
        jump location_sandbeach

    # ── Post-return reconvergence ──────────────────────────────────────────
    $ _post_state = get_romance_state("zoe")
    if _post_state == "dating":
        $ zoe_beach_dating_done = True
        $ zoe_first_date_done   = True   # backward compat: M4 gate checks this flag
        if store.zoe_dating_day < 0:
            $ zoe_dating_day = day
        $ complete_commitment("zoe_beach_dating_1")
        $ add_relationship_memory("zoe", "zoe_beach_dating", "Not stopping me")
        "You stay until the cold finally becomes harder to ignore."
        z "We should go."
        mc "Yeah."
        z "Walk with me?"
        mc "Obviously."
        z "Careful."
        z "You'll make that sound normal."
        mc "Maybe it is."
        "She doesn't argue."
    else:
        # Director chose not to advance, or player declined.
        # Respect retry/cooldown state the director subscene set.
        $ store.zoe_beach_dating_pending = False
        $ cancel_commitment("zoe_beach_dating_1")

    $ story_scene_active = False
    jump location_sandbeach


# ── M3 — NO REASON ───────────────────────────────────────────────────────────
# First ordinary private evening.
# Triggered from location_home_actions when commitment_available("zoe_home_no_reason_1").

label zoe_home_no_reason_scene:
    $ story_scene_active = True
    $ clear_npc_sprites()
    hide screen npc_relbar
    hide screen npc_actions
    hide screen hud

    scene expression home_bg() with dissolve
    show screen hud
    # DIRECTOR CG SLOT: zoe_home_no_reason / Zoe arriving with takeaway bags, MC POV
    show zoe_street_neutral as npcsprite at sprite_l

    "Zoe arrives carrying two paper bags and the expression of someone who has made a decision she refuses to defend."
    z "One of these is yours."
    mc "Which one?"
    z "You'll know if your mouth goes numb."
    mc "Reassuring."
    z "I asked for mild."
    mc "And?"
    z "I don't think they respected me."

    # She settles in
    pause 0.3

    # DIRECTOR CG SLOT: zoe_home_no_reason / Both watching film, screen glow, takeaway packaging
    show zoe_street_neutral as npcsprite at sprite_r

    "Forty minutes later, the film has introduced a second identical briefcase and killed a character who was apparently important."
    z "No."
    mc "What?"
    z "Absolutely not."
    mc "You picked this."
    z "I picked badly with confidence."
    z "That's different."
    mc "He's definitely dead."
    z "He was definitely dead twenty minutes ago."
    mc "Maybe it's his twin."
    z "If he has a twin, I'm leaving."

    pause 0.5

    "The identical twin appears."

    z "I hate you."
    mc "I didn't write it."
    z "You manifested it."

    # DIRECTOR CG SLOT: zoe_home_no_reason / Zoe leaning against MC's shoulder, eyes on film, weight actually resting

    "Somewhere in the last half hour, the space between you has disappeared."
    mc "Comfortable?"
    z "Don't make it a survey."
    mc "That means yes."
    z "That means stop talking during the film."

    pause 0.5

    z "Also yes."

    # DIRECTOR CG SLOT: zoe_home_no_reason / Film ended, both still sitting close, quiet room, she hasn't moved

    "The credits roll."
    "Neither of you moves immediately."
    mc "Want me to walk you home?"
    z "In a minute."
    mc "Film's over."
    z "I noticed."

    pause 0.3

    mc "You came over specifically to watch that?"
    z "No."
    mc "Food?"
    z "Also no."
    mc "Then why?"
    z "..."
    z "No reason."

    "The answer sits there."
    mc "Good reason."
    z "I thought so."

    pause 0.5

    z "This was nice."
    mc "High praise."
    z "Don't get used to it."

    "She starts to get up, stops."

    z "Actually—"
    mc "Yeah?"
    z "Do."
    z "That's probably the point."

    "Then she leaves."

    $ zoe_home_no_reason_done = True
    $ zoe_home_no_reason_day  = day
    $ zoe_home_pending        = False
    $ complete_commitment("zoe_home_no_reason_1")
    $ add_relationship_memory("zoe", "zoe_home_no_reason", "The terrible film and no particular reason")
    $ apply_relationship_change("zoe", "zoe_home_no_reason", "authored", affection=2, trust=1, familiarity=4)
    $ story_scene_active = False
    jump location_home_actions


# ── M4 — APPARENTLY ──────────────────────────────────────────────────────────
# Group recognition. Called as coda from marcus_zoe_static_small_group.
# Gated externally — only enter when get_romance_state("zoe") in dating/committed
# and not zoe_m4_marcus_done.

label zoe_m4_marcus_recognition:
    $ zoe_m4_marcus_done = True

    m "Oh."
    z "Don't."
    m "I said one syllable."
    z "It was an ambitious syllable."
    m "So this is a thing now?"

    menu:
        "\"Yeah.\"":
            mc "Yeah."
            m "Huh."
            z "What?"
            m "Nothing."
            z "That's worse."
            m "I'm being supportive."
            z "Try less."

        "\"Ask Zoe.\"":
            mc "Ask Zoe."
            z "Coward."
            m "That's a yes."
            z "Apparently."

        "\"Define thing.\"":
            mc "Define thing."
            m "Absolutely not."
            m "I'm not getting cross-examined by both of you."
            z "Smartest thing you've said all night."

    # Small physical cue — no forced display; let art deliver it
    $ apply_relationship_change("zoe", "zoe_m4_marcus", "authored", familiarity=2)
    $ add_relationship_memory("zoe", "zoe_m4_marcus", "Marcus figured it out")
    return


# ── M6 — NO MORE QUALIFIERS ──────────────────────────────────────────────────
# Commitment. Triggered from location_terrace when commitment_available("zoe_commitment_beach_1").
# Visual: restaurantnight background (Riverside Terrace, late evening).
# ponytail: commitment ID remains "zoe_commitment_beach_1" for save-file stability.
# ponytail: sprite "zoe_beach_neutral" retained — no new sprite assets introduced.

label zoe_commitment_beach_scene:
    $ story_scene_active = True
    $ clear_npc_sprites()
    hide screen npc_relbar
    hide screen npc_actions
    hide screen hud

    scene restaurantnight with dissolve
    show screen hud
    # DIRECTOR CG SLOT: zoe_commitment / Zoe already there, quiet city evening behind her
    show zoe_beach_neutral as npcsprite at sprite_l

    "She is already there when he arrives."
    pause 0.3
    z "I wasn't sure this was a good idea."
    mc "Meeting up?"
    z "Saying it out loud."

    pause 0.3

    # DIRECTOR CG SLOT: zoe_commitment / Both at the terrace, medium-wide, quiet conversation
    show zoe_beach_neutral as npcsprite at sprite_r

    z "I've been trying to decide if this needs a conversation."
    mc "That's usually how conversations start."
    z "And already I regret it."
    mc "Want me to pretend I didn't hear?"
    z "No."
    z "That's the problem."

    pause 0.3

    z "Are we doing the thing where we both know what this is and refuse to name it?"
    mc "I thought you liked refusing to name things."
    z "I do."

    $ show_npc_expr("zoe", "talk")

    # DIRECTOR CG SLOT: zoe_commitment_beach / Close Zoe shot — direct eye contact after "I'm making an exception"

    z "I'm making an exception."

    menu:
        "\"Then let's name it.\"" if renpy.has_label("zoe_commitment_payoff"):
            jump zoe_commitment_branch_a
        "\"I want you. I don't know if I need the label yet.\"":
            jump zoe_commitment_branch_b

    # ── BRANCH A — Committed ──────────────────────────────────────────────────
    label zoe_commitment_branch_a:
        mc "Then let's name it."
        z "That's very ominous."
        mc "I want this."
        mc "Properly."
        z "We're already doing it properly."
        mc "Then officially."
        z "I hate that word."
        mc "Zoe."

        pause 0.5

        z "Fine."
        mc "Fine?"
        z "Yes."
        z "Us."
        z "No qualifiers."
        mc "That sounded painful."
        z "It was."
        mc "Worth it?"
        z "Ask me in six months."

        pause 0.6

        z "..."
        z "Yes."

        pause 0.8

        # =====================================================================
        # DIRECTOR HANDOFF
        #
        # CREATE FILE:
        # game/director_romance/zoe_commitment_romance.rpy
        #
        # REQUIRED LABEL:
        # zoe_commitment_payoff
        #
        # ENTRY MOMENT:
        # Zoe has said "Yes." — Riverside Terrace, late evening, commitment
        # accepted with no qualifiers. Background: restaurantnight.
        # Sprite: zoe_beach_neutral at sprite_r.
        #
        # ENTRY STATE:
        # get_romance_state("zoe") == "dating"
        # zoe_commitment_done == False
        # zoe_first_date_done == True, zoe_beach_night_done == True
        # relationship_memory_exists("first_kiss_zoe") == True
        # =====================================================================
        if renpy.has_label("zoe_commitment_payoff"):
            call zoe_commitment_payoff
            $ set_romance_state("zoe", "committed", source="zoe_commitment_beach")
            $ zoe_commitment_done  = True
            $ zoe_committed_day    = day
            $ zoe_commitment_pending = False
            $ complete_commitment("zoe_commitment_beach_1")
            $ add_relationship_memory("zoe", "zoe_commitment_beach", "No qualifiers")
            $ apply_relationship_change("zoe", "zoe_commitment_beach", "authored",
                  affection=2, trust=3, familiarity=2, attraction=2)
            $ story_scene_active = False
            jump location_terrace
        else:
            if config.developer:
                $ renpy.notify("DIRECTOR SUBSCENE MISSING: zoe_commitment_payoff")
            # Director subscene absent — reconverge as "not yet", remain dating, no state change.
            $ store.zoe_commitment_declined_day = day
            $ store.zoe_commitment_pending = False
            $ cancel_commitment("zoe_commitment_beach_1")
            $ story_scene_active = False
            jump location_terrace

    # ── BRANCH B — Not yet ────────────────────────────────────────────────────
    label zoe_commitment_branch_b:
        mc "I want you."
        mc "I don't know if I need the label yet."
        "Zoe looks at him."
        z "That's a no wrapped in a philosophy."
        mc "It's a not-yet."

        pause 0.3

        z "Okay."
        mc "Okay?"
        z "I said I'd make an exception."
        z "I didn't say you had to."
        mc "I don't want this to change."
        z "Then don't make it change."
        "She takes his hand anyway."
        z "Not-yet is an answer."

        # Retry after 7+ days; no relationship loss
        $ store.zoe_commitment_declined_day = day
        $ store.zoe_commitment_pending = False
        $ cancel_commitment("zoe_commitment_beach_1")
        $ story_scene_active = False
        jump location_terrace


# ── M6 — DON'T MAKE IT AN EVENT ──────────────────────────────────────────────
# First spoken love. Triggered directly from location_home_actions when
# _zoe_m6_eligible() and 10 <= hour <= 17.

label zoe_love_spoken_scene:
    $ zoe_m6_pending   = True
    $ story_scene_active = True
    $ clear_npc_sprites()
    hide screen npc_relbar
    hide screen npc_actions
    hide screen hud

    scene expression home_bg() with dissolve
    show screen hud
    # DIRECTOR CG SLOT: zoe_love_spoken / Daytime apartment, Zoe comfortable and occupying space, window light
    show zoe_street_neutral as npcsprite at sprite_r

    "Zoe has been at your place for most of an hour."
    "She has changed seats twice because the light moved."

    z "Move."
    mc "Hello to you too."
    z "You're blocking the window."
    mc "You've been here an hour."
    z "And the sun has demonstrated object permanence."
    mc "Proud of it."
    z "Move."

    "He moves enough."

    z "Thank you."

    pause 0.3

    "You hand her coffee."
    z "Too much milk."
    mc "You drank it like this last time."
    z "I was being polite."
    mc "You?"
    z "Rare archival footage."

    "She looks back toward whatever caught her attention."

    pause 0.5

    "Then, entirely casually:"

    $ show_npc_expr("zoe", "talk")
    z "Love you. Move another inch."

    pause 0.6

    # DIRECTOR CG SLOT: zoe_love_spoken / Beat after the admission — she realises what she said, briefly caught

    "She realises what she said."
    mc "What?"
    z "You heard me."
    mc "I did."
    z "Then don't make it an event."

    menu:
        "\"Love you too.\"":
            jump zoe_love_branch_a
        "[Kiss her.]":
            jump zoe_love_branch_b
        "\"That sounded suspiciously like a label.\"":
            jump zoe_love_branch_c

    # ── BRANCH A ──────────────────────────────────────────────────────────────
    label zoe_love_branch_a:
        mc "Love you too."
        pause 0.4
        z "Good."
        mc "That's it?"
        z "What were you expecting?"
        mc "I don't know."
        z "Fireworks?"
        mc "One, maybe."
        z "No."
        $ show_npc_expr("zoe", "laugh")
        z "But you can stay where you are."
        mc "Thought I was blocking the light."
        z "You are."
        mc "And?"
        z "I've decided to tolerate it."
        jump zoe_love_after

    # ── BRANCH B ──────────────────────────────────────────────────────────────
    label zoe_love_branch_b:
        "You lean over and kiss her."
        "She lets you."
        pause 0.3
        "When you separate:"
        $ show_npc_expr("zoe", "talk")
        z "Acceptable response."
        mc "You're reviewing it again."
        z "Some traditions matter."
        pause 0.3
        mc "Love you too."
        "She looks at him."
        z "I know."
        jump zoe_love_after

    # ── BRANCH C ──────────────────────────────────────────────────────────────
    label zoe_love_branch_c:
        mc "That sounded suspiciously like a label."
        z "I can take it back."
        mc "Don't."
        pause 0.3
        z "Wasn't going to."
        mc "Good."
        z "You can say it too, by the way."
        mc "Love you."
        z "There."
        z "Horrible."
        mc "Devastating."
        z "We'll recover."
        jump zoe_love_after

    # ── AFTER (all branches) ──────────────────────────────────────────────────
    label zoe_love_after:
        # =====================================================================
        # DIRECTOR HANDOFF
        #
        # CREATE FILE:
        # game/director_romance/zoe_love_spoken_romance.rpy
        #
        # REQUIRED LABEL:
        # zoe_love_spoken_payoff
        #
        # ENTRY MOMENT:
        # All three response branches have converged — "Love you too." / kiss /
        # "Love you." The emotional payoff of the love confession resolves here.
        # Background: home_bg(). Sprite: zoe_street_neutral at sprite_r.
        #
        # ENTRY STATE:
        # get_romance_state("zoe") == "committed"
        # zoe_love_spoken == False (set by parent after return)
        # In MC's apartment, daytime (10:00–17:00).
        #
        # DIRECTOR-OWNED CONTENT:
        # CG-driven visual climax: small smile, close comfort, understated.
        # No romance-state mutation needed. Return with plain `return`.
        # =====================================================================
        if renpy.has_label("zoe_love_spoken_payoff"):
            call zoe_love_spoken_payoff
        # Safe reconvergence: re-establish home scene for the aftermath narration.
        # DIRECTOR CG SLOT: zoe_love_spoken / Response payoff — small smile, close comfort, understated
        scene expression home_bg() with dissolve
        show zoe_street_neutral as npcsprite at sprite_r
        show screen hud

        pause 0.4

        "A few minutes later, you're arguing about whether the building opposite is actually crooked or whether the window frame is."
        "Nothing else changes."
        "Which is how you know something did."

        $ zoe_love_spoken     = True
        $ zoe_love_spoken_day = day
        $ zoe_m6_pending      = False
        $ add_relationship_memory("zoe", "zoe_love_spoken", "Don't make it an event")
        $ apply_relationship_change("zoe", "zoe_love_spoken", "authored",
              affection=2, trust=2, familiarity=2)
        $ story_scene_active = False
        jump location_home_actions
