# ═══════════════════════════════════════════════════════════════════════════
# ZOE — EARLY ONBOARDING / BOOTSTRAP PASS
# ═══════════════════════════════════════════════════════════════════════════
# The problem this solves: zoe_arc.rpy has twelve authored beats, but a fresh
# player could go a fortnight without a reason to care who Zoe is. This file
# closes the front door — it does NOT add a second Zoe.
#
# What already existed and is REUSED, not rebuilt:
#   * the authored first meeting        locations.rpy  beach_meet_zoe
#                                       (+ zoe_beach_approach / _watch / _shared,
#                                        7 CGs, already the top-priority branch
#                                        of location_beach)
#   * the beat dispatcher               zoe_arc.rpy    zoe_arc_beat_for
#   * the relationship helper           zoe_arc.rpy    _zoe_rel → npc_relationships
#   * the phone message queue           phone_messages.rpy queue_phone_message
#   * the contextual Talk chain         interact.rpy   _check_talk_followup
#   * the contact list                  interact.rpy   store.npc_contacts
#   * the beat exit                     zoe_arc.rpy    zoe_arc_exit / _zarc_dest
#
# What this file adds:
#   1. A Marcus mention of Zoe in the move-in intro (script.rpy) so she is a
#      name before she is a person.
#   2. A tail on the existing beach meeting: Marcus recognition, an open thread
#      that feeds zoe_not_ready_scene, a first-impression record, and the
#      contact exchange the initiative pool needs.
#   3. A guaranteed first callback text keyed to that impression.
#   4. A bootstrap window that relaxes ONE beat gate, then switches itself off.
#   5. Two fallbacks for a player who never walks to the beach.
#
# ponytail: the bootstrap window is a fixed 10-day flat relaxation of a single
# gate rather than a weighting curve. Ceiling: it only ever opens
# zoe_wednesday_grounds_scene early. Upgrade path if more beats need it — turn
# _ZOE_BOOTSTRAP_RELAX into a {beat_id: (fam, cooldown)} table read by the
# wrapper below instead of the one inlined branch.
# ═══════════════════════════════════════════════════════════════════════════

# ── Onboarding state ────────────────────────────────────────────────────────
default marcus_mentioned_zoe          = False
default zoe_intro_beach_done          = False
default zoe_intro_alt_done            = False
default zoe_properly_introduced       = False
default zoe_bootstrap_complete        = False
default zoe_first_impression          = ""       # "observant"/"honest"/"banter"/""
default zoe_bootstrap_start_day       = -1
default zoe_first_callback_sent       = False
default marcus_beach_reminder_sent    = False
default marcus_met_zoe_callback_done  = False


init 4 python:

    _ZOE_BOOTSTRAP_DAYS = 10     # length of the relaxed-gate window
    _ZOE_CALLBACK_DELAY = 2      # days after the intro that she texts

    # First-callback copy. Keyed by the impression the intro recorded; the
    # empty-string fallback is what an old save or a skipped menu produces.
    _ZOE_FIRST_CALLBACK = {
        "observant": "You were right about the light on that side of the page. Annoying.",
        "honest":    "First time in a while someone just admitted they didn't know something. Refreshing.",
        "banter":    "Still thinking about that last line. Didn't expect it to land.",
        "":          "Marcus gave you my number, didn't he? Actually, don't answer that.",
    }

    # Every beat id that stamps tier_a_beat_last_day for Zoe — zoe_arc.rpy's
    # twelve plus the two Tier A ones in location_beats_tier_a.rpy.
    _ZOE_BEAT_IDS = ("zoe_print", "zoe_beige", "zoe_second_opinion", "zoe_bass",
                     "zoe_coffee", "zoe_not_ready", "zoe_noticed", "zoe_wednesday",
                     "zoe_deadline", "zoe_after_deadline", "zoe_just_stay",
                     "zoe_outdoor", "zoe_walk")

    def _zoe_bootstrap_backfill():
        """Old-save safety. A save made before this file existed can already
        have met Zoe — deriving the new flags from zoe_met is what stops the
        Marcus reminder and the alternate intro firing at someone who has known
        her for forty days. Idempotent; safe to call every load and every day."""
        if store.zoe_met and not store.zoe_properly_introduced:
            store.zoe_properly_introduced = True
            store.zoe_bootstrap_complete  = True
            store.zoe_first_callback_sent = True
            store.marcus_met_zoe_callback_done = True
            if store.zoe_bootstrap_start_day < 0:
                store.zoe_bootstrap_start_day = store.day

    def zoe_in_bootstrap_window():
        """True while the early-content relaxation applies."""
        return (store.zoe_properly_introduced
                and not store.zoe_bootstrap_complete
                and store.zoe_bootstrap_start_day >= 0
                and store.day <= store.zoe_bootstrap_start_day + _ZOE_BOOTSTRAP_DAYS)

    def _zoe_beat_fired_since_intro():
        start = store.zoe_bootstrap_start_day
        if start < 0:
            return False
        return any(store.tier_a_beat_last_day.get(b, -999) >= start
                   for b in _ZOE_BEAT_IDS)

    def _zoe_mark_introduced(route):
        """Single write point for 'the player has actually met Zoe'. Called by
        both intro routes so neither can drift from the other."""
        store.zoe_met                 = True
        store.zoe_properly_introduced = True
        store.zoe_bootstrap_start_day = store.day
        if route == "beach":
            store.zoe_intro_beach_done = True
        else:
            store.zoe_intro_alt_done = True
        try:
            mark_npc_encountered("zoe")
        except Exception:
            pass
        # Contact exchange — the same one line interact.rpy's "number" action
        # runs. Without it _texting_tier("zoe") is None and every Zoe text,
        # including her own callback, is unreachable.
        if "zoe" not in store.npc_contacts:
            store.npc_contacts = store.npc_contacts + ["zoe"]

    # ── Daily tick ───────────────────────────────────────────────────────────
    # Called from new_day() in data.rpy, next to _check_npc_initiative().
    # Everything here is queue_phone_message, not the initiative picker: the
    # picker is a 0.25-0.55 daily roll against a one-message global budget
    # shared with every other NPC, which cannot honour "within 2-4 days".
    def _zoe_bootstrap_tick():
        _zoe_bootstrap_backfill()

        # E. Her first callback. Once, exactly _ZOE_CALLBACK_DELAY days after
        # the intro, no response options — it only has to prove she remembered.
        if (store.zoe_properly_introduced and not store.zoe_first_callback_sent
                and store.zoe_bootstrap_start_day >= 0
                and store.day >= store.zoe_bootstrap_start_day + _ZOE_CALLBACK_DELAY):
            queue_phone_message(
                "zoe",
                _ZOE_FIRST_CALLBACK.get(store.zoe_first_impression,
                                        _ZOE_FIRST_CALLBACK[""]),
                store.day, "zoe_first_callback")
            # This tick runs AFTER deliver_due_messages() in new_day, so a
            # same-day queue would otherwise sit undelivered until tomorrow —
            # the same reason _check_npc_initiative calls this.
            deliver_message_now("zoe_first_callback")
            store.zoe_first_callback_sent = True

        # G. Marcus nudge for a player who never walked to the beach.
        if (store.marcus_mentioned_zoe and not store.zoe_properly_introduced
                and not store.marcus_beach_reminder_sent and store.day >= 3):
            queue_phone_message(
                "marcus",
                "Ever make it to the beach? If Zoe insults your taste in something, that's basically hello.",
                store.day, "marcus_beach_reminder")
            deliver_message_now("marcus_beach_reminder")
            store.marcus_beach_reminder_sent = True

        # J. Bootstrap completion — she graduates to the standard systems.
        if (store.zoe_properly_introduced and not store.zoe_bootstrap_complete
                and store.zoe_first_callback_sent
                and store.zoe_bootstrap_start_day >= 0
                and store.day >= store.zoe_bootstrap_start_day + 3
                and (_zoe_beat_fired_since_intro()
                     or store.day >= store.zoe_bootstrap_start_day + 7)):
            store.zoe_bootstrap_complete = True

    # ── F. Early beat priority boost ─────────────────────────────────────────
    # Wraps zoe_arc.rpy's dispatcher (same interception pattern that file uses
    # on _check_talk_followup). The original keeps absolute priority; this only
    # ever adds a beat the original just declined.
    #
    # Audit of what is already reachable at fam 0 straight out of the intro:
    #   zoe_print_scene    hub, Mon-Fri 09-13, no relationship gate   → fine
    #   zoe_bass_window    hub, fam >= 20                             → ~2 beats away
    #   zoe_wednesday      cafe, fam >= 30 + 6-day cooldown           → too far
    # So exactly one gate is relaxed: ordinary time at Grounds, which is the
    # low-stakes second encounter the early window is missing. The scenes that
    # need earned Trust (coffee E, not-ready F, deadline J/K, just-stay L) are
    # untouched and stay behind their own prerequisites.
    _zoe_arc_beat_for_pre_boot = zoe_arc_beat_for

    def zoe_arc_beat_for(loc):
        result = _zoe_arc_beat_for_pre_boot(loc)
        if result is not None:
            return result
        if not zoe_in_bootstrap_window():
            return None
        if loc != "location_cafe":
            return None
        if not store.zoe_met or not npc_here("zoe", loc):
            return None
        if not _beat_global_ok():
            return None
        if npc_rel("zoe", "familiarity") >= 12 and _beat_cooldown_ok("zoe_wednesday", 3):
            return "zoe_wednesday_grounds_scene"
        return None

    # ── H. Alternate intro eligibility ───────────────────────────────────────
    # Her real schedule (npc_schedules.rpy): hub Mon-Fri 09-13, cafe Wed 13-18,
    # park Thu-Fri 14-18, sandbeach Sat-Sun 12-18, bar Sat 19-24. The two
    # locations a day-4 player is most likely to already be standing in are the
    # Hub and Grounds, and npc_here() enforces the real window for both, so no
    # hour arithmetic is duplicated here.
    def check_zoe_alt_intro(loc):
        if store.zoe_met or store.zoe_properly_introduced:
            return False
        if store.day < 4:
            return False
        if loc not in ("location_cafe", "location_hub"):
            return False
        return npc_here("zoe", loc)

    # ── I. Marcus callback ───────────────────────────────────────────────────
    _check_talk_followup_pre_zoeboot = _check_talk_followup

    def _check_talk_followup(npc_id):
        result = _check_talk_followup_pre_zoeboot(npc_id)
        if result is not None:
            return result
        if (npc_id == "marcus" and store.zoe_properly_introduced
                and not store.marcus_met_zoe_callback_done):
            return "marcus_met_zoe_callback"
        return None


# Ren'Py runs this on every load; the backfill is idempotent so a save made
# after this file shipped simply no-ops through it.
label after_load:
    $ _zoe_bootstrap_backfill()
    return


# ═══════════════════════════════════════════════════════════════════════════
# C. BEACH FIRST INTRODUCTION
# ═══════════════════════════════════════════════════════════════════════════
# The authored meeting is beach_meet_zoe in locations.rpy — approach route,
# watch route, seven CGs, already the FIRST branch of location_beach and
# therefore ahead of every commitment, authored scene and Tier A selector at
# that location. It is not re-written or duplicated. This is:
#   * a named entry point for the Scene Tester, and
#   * the tail that the shared outro calls, which is where the onboarding work
#     that did not exist before actually happens.
label zoe_beach_intro:
    jump beach_meet_zoe


label zoe_beach_intro_tail:
    # Runs on whichever zoe_beach_* CG the route left on — no new art, no scene
    # change, so the meeting still reads as one continuous conversation.

    # A. Marcus recognition. Only if he actually named her on move-in day.
    if marcus_mentioned_zoe:
        z "Marcus sent you, didn't he?"
        mc "He mentioned the beach."
        z "Right. That's how he does it."
        mc "Does what?"
        z "Collects people. Puts them somewhere and waits."
        "She doesn't sound annoyed about it. Closer to the way you'd describe weather."
        z "He's been doing it to me for three years. I've stopped fighting it."
    else:
        "She looks past you at the row of signs along the promenade and visibly loses a small argument with herself."
        z "That one. \"Beachside Kiosk.\" Two different typefaces and neither of them wanted to be there."
        mc "I'd never have noticed."
        z "You will now. Sorry."

    # Character texture — the light. She talks about it as a working problem.
    z "The light's better on this side after four. Everything on the far bay goes flat and orange and lies to you about the water."
    "She's still sketching while she says it. Short strokes, no ceremony, like someone taking notes."

    # Open thread — the more personal work. Seeds zoe_not_ready_scene (F).
    "A page shifts as she closes the sketchbook, and for about a second you see something that isn't waves. Denser. Worked over a lot more."
    mc "Was that yours?"
    z "Technically all of this is mine."
    mc "You know what I meant."
    z "Yeah."
    "She squares the sketchbook against her knee and doesn't open it again."
    z "Anyway. The tide's doing the thing where it takes the good shadows with it."

    # B. Second choice — the one that decides the impression on record.
    menu:
        "\"The water's greener where the wall breaks the swell.\"":
            $ zoe_first_impression = "observant"
            z "It is. Nobody says that."
            "She looks at the break, then at you, recalculating something."
            z "Most people describe the sea as blue and then feel like they've contributed."
            $ _zoe_rel("zoe_intro", affection=1, respect=1, familiarity=3)
        "\"I genuinely don't know anything about art.\"":
            $ zoe_first_impression = "honest"
            z "Good."
            mc "That's not usually the reaction."
            z "People who know a bit are the worst. People who know nothing just tell you what they see, and that's the only useful data there is."
            $ _zoe_rel("zoe_intro", affection=1, trust=1, familiarity=3)
        "\"Should I be worried about what you've written down about me?\"":
            $ zoe_first_impression = "banter"
            z "Yes."
            "A pause exactly long enough to be deliberate."
            z "It's mostly about the jacket."
            $ _zoe_rel("zoe_intro", affection=2, familiarity=4)

    # Contact exchange — same mechanism as interact.rpy's "number" action, but
    # earned by the conversation instead of an affection threshold. Diegetic
    # only: no system line, no notification.
    z "Give me your phone."
    "You do. She types something with the hand that isn't holding charcoal, which is not the hand you'd have chosen."
    z "That's the kiosk sign. I photographed it in June and I've never had anyone to send it to."
    "Your phone buzzes a second later. It is, in fact, a very bad sign."
    $ _zoe_mark_introduced("beach")
    return


# ═══════════════════════════════════════════════════════════════════════════
# H. ALTERNATE INTRO — day 4+, Grounds or the Hub
# ═══════════════════════════════════════════════════════════════════════════
# Shorter on purpose. It establishes the same four facts as the beach meeting
# (she makes things, she's dry about it, Marcus is the connection, you can
# reach her) and hands off to the identical flag write.
label zoe_alt_intro:
    $ set_hud("hidden")
    $ story_scene_active = True
    if current_loc == "location_cafe":
        scene expression cafe_bg()
        $ _zarc_dest = "location_cafe"
    else:
        scene expression ("hub_night" if (hour >= 20 or hour < 6) else "hub_day")
        $ _zarc_dest = "location_hub"
    show screen hud
    hide screen people_here_dock
    show zoe_street_neutral as focus_zoe at sprite_r
    "There's a woman at the end table with a sketchbook open and a coffee she has clearly forgotten about."
    "She's been looking at the same doorway for long enough that you look at it too. It's a doorway."
    show zoe_street_talk as focus_zoe at sprite_r
    z "It's off by about two degrees and they've hung a sign on it to draw attention to that."
    mc "Sorry — are you talking to me?"
    show zoe_street_neutral as focus_zoe at sprite_r
    z "Not initially."
    "She goes back to the page. Then, without looking up:"
    z "You're new. You've got the look."
    menu:
        "\"That obvious?\"":
            $ zoe_first_impression = "honest"
            show zoe_street_talk as focus_zoe at sprite_r, react_nod
            z "You looked at the menu board twice. Regulars don't."
            $ _zoe_rel("zoe_intro", affection=1, trust=1, familiarity=3)
        "\"What look is that?\"":
            $ zoe_first_impression = "banter"
            show zoe_street_laugh as focus_zoe at sprite_r
            z "Alert. It wears off."
            $ _zoe_rel("zoe_intro", affection=2, familiarity=4)
        "\"You've got charcoal on your face.\"":
            $ zoe_first_impression = "observant"
            show zoe_street_laugh as focus_zoe at sprite_r
            z "I know. I'm choosing to leave it."
            "She doesn't check. That's either confidence or a very committed bluff."
            $ _zoe_rel("zoe_intro", affection=1, respect=1, familiarity=3)
    show zoe_street_neutral as focus_zoe at sprite_r
    z "Zoe. I draw things and then complain about them, in that order."
    if marcus_mentioned_zoe:
        mc "Marcus mentioned you."
        show zoe_street_talk as focus_zoe at sprite_r, react_lean_in
        z "Of course he did."
        z "He introduces people the way other men give out business cards. He'll deny it with a lot of confidence."
    else:
        mc "[mc_name]. Just moved here."
        show zoe_street_talk as focus_zoe at sprite_r
        z "Then you know Marcus, or you will. Everyone does eventually. It's not a choice you get to make."
    "She turns the sketchbook a few degrees toward you and then, deciding something, turns it back."
    z "Not that page."
    mc "Fair enough."
    show zoe_street_neutral as focus_zoe at sprite_r, react_nod
    z "Give me your phone. I'm around — beach at weekends, here on Wednesdays when the light's tolerable."
    "She hands it back without ceremony and goes straight back to being annoyed at a doorway."
    $ _zoe_mark_introduced("alt")
    $ spend_time(0.5)
    jump zoe_arc_exit


# ═══════════════════════════════════════════════════════════════════════════
# I. MARCUS CALLBACK — first Talk after you've met her
# ═══════════════════════════════════════════════════════════════════════════
label marcus_met_zoe_callback:
    $ marcus_met_zoe_callback_done = True
    m "You meet Zoe?"
    mc "Yeah."
    m "Did she judge you?"
    mc "Immediately."
    m "Means she likes you."
    if zoe_first_impression == "banter":
        m "She only bothers being funny at people she's planning to see again."
    elif zoe_first_impression == "honest":
        m "And don't oversell yourself to her. She checks."
    $ _do_talk_accounting("marcus")
    return
