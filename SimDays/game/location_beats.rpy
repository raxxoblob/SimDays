# ═══════════════════════════════════════════════════════════════════════════
# TIER A LOCATION BEAT — Nora Cover Shift
# Pattern: location entry → eligibility fn → jump to beat → sprite conversation
#          → time/needs/relationship effects → jump back into the location flow
# Visual cost: zero new assets (cafe_bg() + existing nora_cafe_* sprites).
#
# The reusable shape, for the beats that follow:
#   1. Two defaults in data.rpy: <beat>_triggered (fired) + <beat>_outcome (chosen).
#   2. One can_-style eligibility function here, returning a label name or None.
#      Pure reads only — no state mutation, so it is cheap to call on every entry
#      and testable from tests/location_beats_selfcheck.py.
#   3. One `if check_X(): jump X` line in the location label's story-beat
#      priority chain (locations.rpy), below the authored pending scenes.
#   4. set_hud("hidden") … set_hud("full") around the beat (summer_festival.rpy
#      is the reference), each branch exiting with an explicit jump.
# ═══════════════════════════════════════════════════════════════════════════

init python:

    def check_nora_cover_scene():
        """Eligibility for the Nora cover-shift beat. Returns a label or None.

        Window rationale (differs from the original brief's 17-21 / midnight):
        the café's venue hours are 07:00-19:00 and Nora's only late shift is the
        weekend 10:00-18:00 one, so 15:00-18:00 while she is actually
        `working_shift` is the only slot where "cover the rest of my shift" is
        true. Covering therefore runs to close (19:00), not to midnight."""
        if store.nora_cover_shift_triggered:
            return None
        if not store.nora_met:
            return None
        # She has to still work here for the favour to make sense.
        if store.nora_life_state != "cafe":
            return None
        if not npc_here("nora", "location_cafe"):
            return None
        if resolve_npc_state("nora")["activity_id"] != "working_shift":
            return None
        if not (15.0 <= float(store.hour) < 18.0):
            return None
        return "nora_cover_shift_scene"


# ── The beat ──────────────────────────────────────────────────────────────────
label nora_cover_shift_scene:
    $ set_hud("hidden")
    $ nora_cover_shift_triggered = True
    $ story_scene_active = True
    scene expression cafe_bg()
    show screen hud
    hide screen people_here_dock
    $ _nora_fam = npc_rel("nora", "familiarity")

    show nora_cafe_normal at sprite_r
    "Nora is wiping down the same stretch of counter she was wiping when you walked in."
    show nora_cafe_talk at sprite_r, react_lean_in
    n "Oh — hey."
    mc "Hey. Everything okay?"
    n "Yeah. Mostly."
    show nora_cafe_talk at sprite_r, react_nod
    n "I was actually hoping I'd run into you."

    if _nora_fam >= 40:
        mc "Uh-oh."
        show nora_cafe_laugh at sprite_r, react_bounce
        n "Don't make that face. I haven't even asked yet."
    else:
        mc "That sounds suspicious."
        show nora_cafe_talk at sprite_r, react_nod
        n "It's not that bad."

    # ── The request ───────────────────────────────────────────────────────────
    show nora_cafe_talk at sprite_r, react_lean_in
    n "Any chance you could cover the rest of my shift?"
    mc "How late?"
    n "Close. Henry locks up at seven."
    mc "That's not the rest of your shift. That's most of an evening."
    show nora_cafe_sad at sprite_r, react_sigh
    n "I know."

    # Her reason — pulled from her actual story state rather than invented.
    if nora_school_revealed:
        n "The nursing thing. There's a session I said I'd go to and I've already skipped one."
        n "If I skip this one too I think I stop being someone who's going."
    else:
        show nora_cafe_sad at sprite_r, react_sigh
        n "Something personal came up. I'll explain it properly sometime."
    n "I wouldn't ask if I had a better option."

    menu:
        "\"Yeah, I can cover.\"":
            jump nora_cover_accept

        "\"What's in it for me?\"" if _nora_fam >= 35:
            mc "What's in it for me?"
            show nora_cafe_laugh at sprite_r, react_bounce
            n "My eternal gratitude."
            mc "That's not legal tender."
            show nora_cafe_talk at sprite_r, react_shake
            n "Then you're out of luck."
            menu:
                "\"Alright. I'll stay.\"":
                    jump nora_cover_accept
                "\"I can't tonight either way.\"":
                    jump nora_cover_decline

        "\"I can't tonight.\"":
            jump nora_cover_decline


label nora_cover_accept:
    mc "Alright. I'll stay."
    show nora_cafe_normal at sprite_r, react_step_back
    n "Seriously?"
    mc "Yeah."
    show nora_cafe_laugh at sprite_r, react_lean_in
    n "Thank you."
    n "I owe you one."
    "She has the apron off and her bag over her shoulder faster than you've ever seen her move."
    # ponytail: nora_cafe_* are separate one-word image tags, so a new expression
    # stacks on top of the old rather than replacing it (project-wide convention —
    # see scene_zoe_spontaneous). Both branches therefore exit through a `scene`
    # statement, which clears the layer, instead of hiding tags one by one.

    $ covered_nora_shift = True
    # Runs to café close (19:00) — see check_nora_cover_scene() for why not midnight.
    $ _hours_to_cover = max(1.0, 19.0 - float(store.hour))
    $ spend_time(_hours_to_cover)
    # On top of spend_time()'s hourly decay — standing behind a counter costs
    # more than the same hours spent sitting. Mirrors cafe_work_shift (-20/4h).
    $ store.need_energy = max(0, store.need_energy - 15)
    $ store.need_hunger = max(0, store.need_hunger - 10)
    # No pay: this is a favour, not a shift Henry booked.

    $ apply_relationship_change(
        "nora",
        source_id="nora_cover_shift",
        source_category="helping_npc",
        trust=4,
        familiarity=1,
        meaningful=True,
    )
    $ queue_phone_message(
        "nora",
        "Seriously, thanks again. You really saved me last night.",
        day + 1,
        "nora_cover_shift_thanks",
    )

    scene expression cafe_bg()
    show screen hud
    "You spend the rest of the evening on the wrong side of the counter."
    "By the time Henry starts stacking chairs, the place is down to one couple and the hum of the fridge."
    "He looks mildly confused about who you are, and pays you in a coffee you don't especially want."
    $ story_scene_active = False
    $ set_hud("full")
    jump map


label nora_cover_decline:
    mc "Sorry. I can't tonight."
    show nora_cafe_normal at sprite_r, react_nod
    n "That's okay."
    n "I figured it was worth asking."
    # No penalty — nothing was promised, so nothing was broken.
    $ story_scene_active = False
    $ set_hud("full")
    # cafe_actions re-runs `scene expression cafe_bg()`, clearing the sprite layer.
    jump cafe_actions
