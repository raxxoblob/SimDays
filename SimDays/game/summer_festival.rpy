# Downtown Summer Festival — a single authored evening, once per campaign.
#
# This is NOT a world-pulse random event. The pulse (world_pulse.rpy) rolls one
# major event per day out of a weighted pool; an authored beat that must happen
# exactly once, with four specific NPCs present, cannot come out of that lottery.
# So the WRITE side is authored here and the READ side is reused: the festival is
# injected into world_pulse_data[day]["major_events"] once it is scheduled, which
# is what makes active_world_event_at() / known_upcoming_events() / the location
# modifier stack see it without any of them needing to know it exists.
#
# "Downtown" is location_centrum (locations.rpy:1792) — the street-level hub the
# venue icons hang off. There is no "location_downtown" in this project.
#
# ponytail: the whole event lives in one state dict rather than a dozen flags.
# Ceiling: only one festival per save. If a yearly festival is ever wanted, the
# upgrade path is keying the dict by year and moving the "already ran" guard from
# `scheduled_day >= 0` to `year not in summer_festival_state`.

default summer_festival_state = {
    "scheduled_day": -1,
    "eligible": False,
    "discovered": False,
    "attended": False,
    "missed": False,
    "blackout_choice": None,     # "technical" / "organize" / "group"
    "blackout_result": None,     # Phase 60 tier, or "na"
    "shelter_focus": None,       # which NPC the player leaned into in the shelter
    "keepsake_awarded": False,
    "follow_up_mail_queued": False,
    "aftermath_done": False,
    "sync_run_day": -1,
}

# Scene-local scratch. Declared so a debug jump straight into a mid-event label
# doesn't hit an undefined name on the way out.
default _sf_start_hour   = 18.0
default _sf_marcus_tone  = "neutral"
default _sf_call         = None
default _sf_right        = None


# init 2: WORLD_EVENT_TEMPLATES is built in world_pulse.rpy's `init 1 python`,
# so registering into it has to happen after that block has run.
init 2 python:

    SF_EVENT_ID   = "summer_festival"
    SF_LOCATION   = "location_centrum"
    SF_NPCS       = ["marcus", "eli", "zoe", "nora"]
    SF_MIN_DAY    = 14          # roughly two in-game weeks of progression
    SF_HOURS      = (18, 23)

    # Registered so name/blurb lookups and active_world_event_at() work. An empty
    # day_weights map means generate_world_pulse() can never pick it: the weight
    # lookup returns 0 and the template is skipped before anything else runs.
    WORLD_EVENT_TEMPLATES["summer_festival"] = {
        "name": "Downtown Summer Festival",
        "location": SF_LOCATION,
        "hours": SF_HOURS,
        "day_weights": {},
        "cooldown_days": 9999,
        "npc_affinities": ["social", "music", "art", "food"],
        "ambient_count": 0,
        "location_modifiers": {"social_density": 40, "busking_crowd": 20},
        "blurb": "Stalls down the length of the street, a stage at the far end.",
    }

    for _sf_i, _sf_name in [
            ("summer_festival_01_arrival",          "sf_arrival"),
            ("summer_festival_02_marcus_eli",       "sf_marcus_eli"),
            ("summer_festival_03_marcus_challenge", "sf_challenge"),
            ("summer_festival_04_zoe_art_stall",    "sf_zoe"),
            ("summer_festival_05_nora_food_stall",  "sf_nora"),
            ("summer_festival_06_group_meeting",    "sf_group"),
            ("summer_festival_07_main_performance", "sf_performance"),
            ("summer_festival_08_blackout",         "sf_blackout"),
            ("summer_festival_09_blackout_group",   "sf_blackout_group"),
            ("summer_festival_10_rain_shelter",     "sf_rain"),
            ("summer_festival_11_shelter_moment",   "sf_shelter"),
            ("summer_festival_12_lights_return",    "sf_lights"),
            ("summer_festival_13_festival_ending",  "sf_ending"),
    ]:
        renpy.image(_sf_name, Transform(
            "images/scenes/summer_festival/%s.png" % _sf_i, size=(1920, 1080)))

    # ── Eligibility + scheduling ─────────────────────────────────────────────

    def summer_festival_eligible():
        """All four NPCs known, and enough of the game has happened to care."""
        if store.day < SF_MIN_DAY:
            return False
        return all(getattr(store, n + "_met", False) for n in SF_NPCS)

    def _sf_event_key(fest_day):
        return "%s_d%d" % (SF_EVENT_ID, fest_day)

    def schedule_summer_festival(force_day=None):
        """Pick a stable Friday/Saturday evening 4-7 days out. Idempotent —
        once scheduled_day is set, this is a no-op, so reload cannot reschedule."""
        sf = store.summer_festival_state
        if sf.get("scheduled_day", -1) >= 0:
            return sf["scheduled_day"]
        if force_day is None and not summer_festival_eligible():
            return -1

        if force_day is not None:
            target = int(force_day)
        else:
            import random as _r
            # Seeded off the campaign seed, not wall-clock, so a replayed save
            # picks the same night.
            rng = _r.Random(_ensure_campaign_seed() * 31 + 5417)
            window = list(range(store.day + 4, store.day + 8))
            weekend = [d for d in window if d % 7 in (4, 5)]   # Fri / Sat
            target = rng.choice(weekend or window)

        sf["eligible"] = True
        sf["scheduled_day"] = target

        # World-state registration: the festival exists whether or not the
        # player ever hears about it.
        generate_world_pulse(target)          # must run first — it early-returns
        pulse = store.world_pulse_data.get(target)
        if pulse is not None and not any(e["id"] == _sf_event_key(target)
                                         for e in pulse["major_events"]):
            t = WORLD_EVENT_TEMPLATES[SF_EVENT_ID]
            pulse["major_events"].append({
                "id": _sf_event_key(target), "template_id": SF_EVENT_ID,
                "name": t["name"], "location": SF_LOCATION,
                "hours": list(SF_HOURS), "day": target, "blurb": t["blurb"],
                "location_modifiers": dict(t["location_modifiers"]),
                "npcs": list(SF_NPCS), "resolved": False,
            })
            store.world_pulse_data = dict(store.world_pulse_data)

        add_calendar_event("Downtown Summer Festival", target, SF_HOURS[0],
                           duration=SF_HOURS[1] - SF_HOURS[0], category="event")
        schedule_festival_npcs(target)
        return target

    def schedule_festival_npcs(fest_day):
        """Marcus, Eli, Zoe and Nora are downtown that evening instead of their
        usual haunts. source_id dedupes, expires_day retires them automatically."""
        for npc_id in SF_NPCS:
            add_schedule_override(
                npc_id, fest_day, 17, 23, SF_LOCATION, "at_festival",
                public=True, interactable=False,
                expires_day=fest_day, source_id="summer_festival")

    # ── Discovery ────────────────────────────────────────────────────────────

    def _sf_discover(channel):
        store.summer_festival_state["discovered"] = True
        discover_event(_sf_event_key(store.summer_festival_state["scheduled_day"]),
                       channel)

    def _sf_announce():
        """Social post two days out, one casual NPC text the day before.
        Marcus sends it — he works a bar two streets away and is the only one of
        the four who would text about a street party unprompted."""
        sf = store.summer_festival_state
        d = sf["scheduled_day"]
        # Retried on d-1 as well: the pulse's 3-posts-a-day budget can swallow
        # the first attempt on a busy day.
        if d - 2 <= store.day < d and not sf["discovered"]:
            if _pulse_social_post(
                    "sf_announce_d%d" % d,
                    "Downtown Summer Festival, %s evening from six. Live music, "
                    "food stalls, local artists. Street's closed to traffic."
                    % DAY_NAMES[d % 7]):
                _sf_discover("social")
        if store.day == d - 1:
            queue_phone_message(
                "marcus",
                "They're shutting the street tomorrow evening for that festival "
                "thing. Food, music, the works. Going?",
                store.day, "summer_festival_marcus_ping")
            _sf_discover("npc")

    # ── Availability ─────────────────────────────────────────────────────────

    def summer_festival_open_now():
        """True when the player is standing downtown during the festival and
        hasn't already been in (or missed it)."""
        sf = store.summer_festival_state
        return (sf.get("scheduled_day", -1) == store.day
                and SF_HOURS[0] <= store.hour < SF_HOURS[1]
                and not sf.get("attended") and not sf.get("missed"))

    # ── Expiry + aftermath ───────────────────────────────────────────────────

    def check_festival_expiry():
        """The festival happened without the player. No failure state, no popup."""
        sf = store.summer_festival_state
        if (sf.get("scheduled_day", -1) >= 0
                and store.day > sf["scheduled_day"]
                and not sf.get("attended") and not sf.get("missed")):
            sf["missed"] = True
            return True
        return False

    def _queue_festival_aftermath(attended):
        """Next-day world reaction. The city post lands either way — the world
        does not check whether you turned up."""
        sf = store.summer_festival_state
        d = sf["scheduled_day"]
        _pulse_social_post(
            "sf_after_d%d" % d,
            "Last night's Downtown Summer Festival lost power mid-set, then it "
            "rained. Nobody left. Best one in years.")

        if not attended:
            return

        # Exactly one personal follow-up — the NPC the player leaned into in the
        # shelter. Sending four texts would read as a quest reward, not people.
        focus = sf.get("shelter_focus")
        _texts = {
            "marcus": "Still can't believe the lights went out right before the "
                      "good part. Rematch at that booth. I'm not letting that stand.",
            "eli":    "The outage was a distribution fault, not the stage rig. I "
                      "looked it up. Thought you'd want to know.",
            "zoe":    "I drew the rain thing. It's bad. I'm keeping it anyway.",
            "nora":   "My shoes are still wet. Worth it. That was a good night.",
        }
        if focus in _texts:
            queue_phone_message(focus, _texts[focus], store.day,
                                "summer_festival_followup_" + focus)

        if sf.get("follow_up_mail_queued"):
            queue_mail(
                "Downtown Events Team",
                "Festival — thank you for your help",
                "Hi,\n\nWe heard you were one of the people who helped sort out "
                "the power the other night. We've added you to the contact list "
                "for future events — we can always use someone who keeps their "
                "head when the lights go out.\n\nHope you enjoyed the rest of "
                "your evening.\n\n- Downtown Events Team",
                "opportunity", store.day + 3, "summer_festival_organizer_followup")

    # ── Daily entry point (called from new_day) ──────────────────────────────

    def sync_summer_festival():
        """One pass per day. Idempotent via sync_run_day."""
        sf = store.summer_festival_state
        if sf.get("sync_run_day", -1) == store.day:
            return
        sf["sync_run_day"] = store.day

        if sf.get("scheduled_day", -1) < 0:
            if schedule_summer_festival() < 0:
                return
        d = sf["scheduled_day"]

        if store.day < d:
            _sf_announce()
        elif store.day > d:
            check_festival_expiry()
            if store.day == d + 1 and not sf.get("aftermath_done"):
                _queue_festival_aftermath(sf.get("attended", False))
                sf["aftermath_done"] = True


# ═══════════════════════════════════════════════════════════════════════════
#  THE EVENING
# ═══════════════════════════════════════════════════════════════════════════

label summer_festival_main:
    $ set_hud("hidden")
    $ summer_festival_state["attended"] = True
    $ summer_festival_state["discovered"] = True
    $ _sf_start_hour = hour
    $ _sf_marcus_tone = "neutral"

    # ── CG01 — arrival ────────────────────────────────────────────────────
    scene sf_arrival with dissolve
    show screen hud
    "The barricades start two blocks early. By the time you're past them the street doesn't sound like a street any more."
    "Stalls down both sides. Cabling taped flat across the tarmac in long silver strips. Somebody at the far end is still testing a microphone and losing."
    "Downtown at eight on an ordinary evening is four people and a bus. This is not that."
    mc "Huh."
    "You'd expected a few tables and a speaker."
    "It takes a minute of standing still before you start picking faces out of it."
    "And then you don't have to look, because one of them is already shouting your name."

    # ── CG02 — Marcus and Eli ─────────────────────────────────────────────
    scene sf_marcus_eli with dissolve
    show screen hud
    m "There he is. Neighbor."
    "Marcus has a paper tray of something fried in one hand and no visible intention of eating it."
    m "Told you it was worth coming to."
    mc "You texted me nine words."
    m "Nine good words."
    "Eli is standing slightly out of the current of people, the way you stand when you've done the maths on where the current is."
    eli "Marcus has walked the entire length of this street twice."
    m "Reconnaissance."
    eli "You were looking for the prize table."
    m "Reconnaissance."
    "Eli doesn't smile so much as briefly stop not smiling."
    eli "There's a booth about forty metres that way. Some kind of strength thing. He's been circling it since we got here."
    m "I am building anticipation."
    eli "You're building an alibi."

    menu:
        "Knowing Marcus, he's already scoped out the challenge booth.":
            $ _sf_marcus_tone = "knowing"
            mc "You've already priced it out, haven't you."
            m "I have assessed the field."
            eli "He asked the woman running it what the record was."
            m "That's assessment."
        "I'm not betting against whoever Marcus decides to challenge.":
            $ _sf_marcus_tone = "competitive"
            mc "Whoever's holding that record has about four minutes left."
            m "See, this is why we're friends."
            eli "That is a very low bar for friendship."
            m "It's a bar. It counts."
        "Good luck getting him away from anything with a prize.":
            $ _sf_marcus_tone = "teasing"
            mc "There's a prize, isn't there."
            m "There's a prize."
            eli "It's a keyring."
            m "It's a {i}principle{/i}."

    "He's already moving. You and Eli follow, which appears to have been the plan the entire time."

    # ── CG03 — Marcus challenge ───────────────────────────────────────────
    scene sf_challenge with dissolve
    show screen hud
    "The booth is a high striker — mallet, plate, bell at the top that nobody in the last twenty minutes has reached."
    "Marcus hands his tray to Eli without asking. Eli holds it at arm's length like evidence."
    m "Watch the grip. Everyone chokes up too high."
    mc "Everyone, or the two people you watched?"
    m "Statistically significant."

    $ _sf_odds = calculate_check_chance("festival_striker_prediction", 0, 55)
    show screen check_distribution_scr(_sf_odds, "Call it?")
    menu:
        "Think he'll manage it?"
        "\"He rings it first swing.\"":
            $ _sf_call = "yes"
        "\"Second swing. He'll overthink the first.\"":
            $ _sf_call = "no"
        "Say nothing and watch.":
            $ _sf_call = None
    hide screen check_distribution_scr

    if _sf_call is not None:
        $ _sf_pred = roll_check("festival_striker_prediction", 0, 55, stable=True)
        $ _sf_right = (_sf_pred["tier"] in ("success", "great", "critical")) == (_sf_call == "yes")
    else:
        $ _sf_right = None

    "He takes it in both hands, drops his shoulder, and hits the plate like it owes him money."
    "The puck goes up. It goes up a long way. It stops about a hand's width short."
    m "That's the plate."
    eli "That's the plate's fault, yes."
    m "The plate is soft on the left."
    eli "You struck it on the right."
    m "Which is how I know."
    "The woman running the booth, who has clearly had this conversation before, silently hands him a second mallet."
    "Second swing. The bell goes off loud enough that three people at the next stall turn around."
    m "{i}Thank{/i} you."
    eli "He didn't correct anything. He just hit it harder."
    m "That {i}is{/i} the correction."

    if _sf_right is True:
        mc "Called it."
        m "Nobody likes this about you."
        eli "I like this about him."
    elif _sf_right is False:
        mc "I had that completely backwards."
        m "You did. I'm choosing to find that charming."

    "The prize is a keyring shaped like a bell. Marcus puts it on his keys immediately, in front of everyone, with no irony whatsoever."
    if _sf_marcus_tone == "teasing":
        mc "The principle."
        m "The principle."
    "Eli hands back the tray. The food is cold. Nobody mentions it."
    "You lose them somewhere around the drinks stall — Marcus knows the person pouring, which is the least surprising thing that has happened all evening."

    # ── CG04 — Zoe, art stalls ────────────────────────────────────────────
    scene sf_zoe with dissolve
    show screen hud
    "The art end of the street is quieter. Trestle tables, clip frames, a lot of very carefully lit small work."
    "Zoe is standing in front of one of them with her arms folded, not moving."
    z "Don't talk for a second."
    "You don't."
    "She tilts her head about two degrees."
    z "Okay. Now it's fine."
    mc "What was wrong with it?"
    z "Nothing. I was deciding whether the frame was doing the work or the painting was."
    mc "And?"
    z "Painting. Barely."

    if skill_art >= 4:
        z "You see it, right? The whole left third is a decision. The rest is just finishing."
        mc "The rest is the part they'll sell."
        z "The rest is the part they'll sell, yes. Thank you, that's very cheering."
        "She says it without any heat. It's the closest thing she has to agreement."
        z "That's the trade. You make one honest decision and then you spend a month making it presentable."
        mc "Is that what the waterfront pieces are?"
        z "The waterfront pieces are eleven honest decisions and no month."
        "A beat."
        z "Which is why they're not on a table like this one."
    else:
        mc "How can you tell?"
        z "Cover the frame with your hand."
        "You do. It's a slightly worse object and a slightly better painting."
        mc "Huh."
        z "Yeah. Huh."
        z "Most people look at the whole thing at once and decide whether they like it. You can do that. It's just less interesting."

    z "Half these stalls are people doing this for the first time. You can tell — everything's hung too high and priced too low."
    mc "Is that bad?"
    z "It's honest. Which is more than the last group show I was in managed."
    "She doesn't elaborate. She's watching a woman two tables down rearrange the same three prints for the third time."
    z "She's going to move them back."
    "The woman moves them back."
    z "Every park has one good rain shelter and every art fair has one person who can't leave the table alone."
    mc "You've catalogued this."
    z "I've catalogued a lot of things. It's a problem."
    "She unfolds her arms, which for Zoe is a whole sentence."
    z "There's food further up. I've been smelling it for twenty minutes and pretending I'm not."

    # ── CG05 — Nora, food stalls ──────────────────────────────────────────
    scene sf_nora with dissolve
    show screen hud
    $ _sf_nora_fam = npc_rel("nora", "familiarity")
    "The food end of the street is where the crowd actually is. Six stalls, two queues that have merged into one queue that nobody is managing."
    "Nora is at the edge of it with a paper cup of something in each hand and the expression of a professional evaluating amateurs."
    n "Their queue system is a crime."
    mc "Hi to you too."
    n "Hi. Their queue system is a crime."
    "She hands you one of the cups without asking whether you wanted it."

    if _sf_nora_fam >= 60:
        n "Don't make the face. It's not coffee. Nobody out here can make coffee and I've stopped hoping."
        mc "I wasn't making a face."
        n "You were pre-loading a face."
        "She's right, and she knows she's right, and she takes a drink instead of saying so."
        n "Three years behind a counter and I still can't stand in a queue like a normal person. I keep wanting to go round and fix it."
        mc "So go fix it."
        n "I'm off tonight. I'm allowed to just be annoyed about things."
        "She says it like a rule she's still getting used to."
    elif _sf_nora_fam >= 30:
        n "It's not coffee. Manage your expectations early, it saves time."
        mc "That's the most reassuring thing anyone's said to me tonight."
        n "I'm full of those."
        "She watches the stall for a moment — genuinely watching, the way you watch a shift you're not on."
        n "He's plating with one hand and taking money with the other. That's how you lose forty seconds a customer."
        mc "You've timed him."
        n "I've timed him twice."
    else:
        n "It's not coffee, so don't get excited. It's warm and it's brown and that's the whole review."
        mc "Fair."
        n "Everyone out here is doing four jobs at once. I respect it and I'd never do it."
        mc "You do four jobs at once every morning."
        n "Yes, but indoors, where I control the temperature."

    n "You know what the actual good thing is about this?"
    mc "The food?"
    n "The food's fine. The good thing is that half these people have never met and by nine they'll be sharing a table because there aren't enough tables."
    n "You can't design that. Somebody just didn't order enough furniture and accidentally made a nice evening."
    "She finishes her cup, looks at it, and doesn't throw it away, because there's nowhere to throw it away."
    n "Right. Who else is here?"

    # ── CG06 — group convergence ──────────────────────────────────────────
    scene sf_group with dissolve
    show screen hud
    "It happens the way these things happen — you're standing with two people, then three, then somebody waves at somebody, and the group exists before anyone decides it should."
    m "There she is. Two coffees?"
    n "One of them was his. Don't start."
    m "I'm not starting."
    n "You're a whole paragraph into starting."
    m "Ask me what I won."
    n "No."
    m "Ask me."
    n "Marcus."
    m "I rang the bell."
    "He holds up the keyring. Nora looks at it for a long, flat second."
    n "That's a keyring."
    m "That is a {i}bell{/i}."
    eli "It took two swings."
    m "It took one {i}confirmed{/i} swing."
    z "What's the striker calibrated to?"
    "Everyone looks at Zoe."
    z "What? They're weighted. They have to be, or nobody ever wins and the stall dies. I'm asking a real question."
    eli "That's the first sensible thing anyone has said about it."
    m "It is not."
    z "I'm Zoe."
    eli "Eli."
    z "Right — the constraint system one."
    eli "Yes."
    z "I've been thinking about that. I'm still annoyed about it."
    eli "Good."
    n "Are these two going to be a problem?"
    m "They're going to be a problem."
    "Nora points at a stall about ten metres off."
    n "That one's the best thing here and there's about six portions left. I'm saying this as a professional."
    m "How professional?"
    n "I watched him for six minutes."
    m "That's professional."
    "By the time the six portions are four portions, the five of you have somehow acquired a corner of a table and nobody has suggested going anywhere else."
    mc "So we're doing this all evening."
    z "Apparently."
    eli "It appears to have been decided without a vote."
    n "Most good things are."

    $ record_game_event("summer_festival_group", "relation",
                        "Spent the festival evening with Marcus, Eli, Zoe and Nora",
                        summary=True, journal=True,
                        metadata={"participants": SF_NPCS, "day": day})
    python:
        for _sfn in SF_NPCS:
            apply_relationship_change(_sfn, "summer_festival_group",
                                      "shared_activity", familiarity=1)

    # ── CG07 — main performance ───────────────────────────────────────────
    scene sf_performance with dissolve
    show screen hud
    "The stage at the far end turns out to be a flatbed trailer with a lighting rig bolted to scaffolding above it."
    "Four people, no introduction. They just start."
    m "Oh, these are good."
    n "You've heard four bars."
    m "Four good bars."
    "The crowd does the thing crowds do — pulls in about two metres and gets quieter."
    if skill_music >= 4:
        "You watch the bass player instead of the singer, because the bass player is the reason it works."
        "She's playing behind the beat by a hair and dragging the whole band into the pocket with her."
        mc "The bassist's carrying it."
        z "...yeah. She is."
        "Zoe says it in a slightly different voice than the one she's been using all evening."
        z "Don't."
        mc "I didn't say anything."
        z "You were about to."
        "You were about to."
    else:
        "You don't know enough to say why it's good. It's good."
        mc "They're better than they need to be for a street."
        eli "Most things are, when nobody's grading them."
    "Somewhere in the third song the lights above the stage flicker. Once. Nobody reacts."
    "They flicker again, longer, and the band's guitarist glances up mid-phrase without stopping."
    n "That's not good."
    m "That's a bulb."
    n "That's not a bulb."

    scene black with Dissolve(0.15)
    "Then the whole street goes out at once."

    # ── CG08 — blackout ───────────────────────────────────────────────────
    scene sf_blackout with dissolve
    show screen hud
    "Not just the stage. The stalls, the strings of bulbs over the road, the sign on the building at the end — everything."
    "The sound cuts a half-second after the light, which is somehow worse."
    "Then: about four hundred phone torches, all at once, like a very slow firework."
    "Nobody screams. Nobody runs. Four hundred people go \"{i}ohhh{/i}\" in the tone of mild disappointment and then start talking louder than before."
    m "What was that? Was that the whole street?"
    eli "The whole street. The sign on the corner building went too, and that's not on the event supply."
    m "So that's — what, bad?"
    eli "It means it isn't the stage rig. It's further back."
    z "The stalls at the top don't have torches. The candle ones. Somebody's going to walk into a table."
    "She's already turned around to look, which is the entire personality in one movement."
    n "Right — the food end's got hot oil on open burners and no lights."
    n "That's the actual problem. Everything else is just dark."
    "Two people in event t-shirts come past at speed, not running, talking into a radio that isn't answering."
    m "Somebody should probably do something."
    eli "Somebody usually is. It's rarely the person saying that."
    m "I walked right into that."
    eli "You did."
    "The staff member with the radio stops a few metres away, looks at the crowd, and visibly runs out of plan."

    # ── CG09 — the choice ─────────────────────────────────────────────────
    scene sf_blackout_group with dissolve
    show screen hud
    "Four hundred people in the dark, being very polite about it, and about six staff."

    menu:
        "\"Let me take a look at the power setup. I might be able to help.\"" if skill_mech >= 3:
            jump summer_festival_blackout_technical
        "\"I can help keep people moving and pointed the right way.\"":
            jump summer_festival_blackout_organize
        "\"Let's just stay together.\"":
            jump summer_festival_blackout_group


label summer_festival_blackout_technical:
    mc "Where's your distribution board?"
    "The staff member looks at you with the specific gratitude of someone who has been asked a question they can answer."
    "It's behind the stage trailer — a weatherproof cabinet, a lot of cable, and a residual current device that has very clearly tripped."

    $ _sf_mech_diff = 52
    $ _sf_mech_odds = calculate_check_chance("festival_blackout_repair",
                                             skill_val=skill_mech,
                                             difficulty=_sf_mech_diff)
    show screen check_distribution_scr(_sf_mech_odds, "Fault-finding")
    "Torch in your teeth. No meter, no proper tools, and a cabinet somebody else wired."
    hide screen check_distribution_scr

    $ _sf_mech_res = roll_check("festival_blackout_repair", skill_val=skill_mech,
                                difficulty=_sf_mech_diff, stable=True)
    $ summer_festival_state["blackout_choice"] = "technical"
    $ summer_festival_state["blackout_result"] = _sf_mech_res["tier"]
    call screen check_result_scr(_sf_mech_res, title="Downtown — Power Fault")

    if _sf_mech_res["tier"] in ("great", "critical"):
        "You work backwards. Everything on the board is dead, so it isn't the board — it's what the board is hanging off."
        "Which is a daisy chain of four extension runs feeding the top of the street, and the last one in the chain is a fryer."
        mc "You've got the whole top row on one leg. And someone plugged a fryer into it."
        "The staff member says a word into the radio that the radio finally answers."
        "It takes eleven minutes and a lot of unplugging. The bell on the striker booth rings on its own when the power comes back up, which nobody has an explanation for."
        $ summer_festival_state["follow_up_mail_queued"] = True
        $ apply_relationship_change("marcus", "festival_blackout_fix", "competence_display", respect=3)
        $ apply_relationship_change("zoe", "festival_blackout_fix", "competence_display", respect=2)
        $ apply_relationship_change("eli", "festival_blackout_fix", "competence_display", respect=2)
        m "Okay. What did you do."
        mc "Told them which plug to pull."
        m "That's it?"
        eli "That is almost always it."
    elif _sf_mech_res["tier"] == "success":
        "You get as far as working out it isn't the board, which narrows it from everything to most things."
        "The staff member's colleague — who does this for a living — takes it from there and finds the overloaded leg in about ninety seconds."
        $ apply_relationship_change("marcus", "festival_blackout_assist", "competence_display", respect=1)
        $ apply_relationship_change("eli", "festival_blackout_assist", "competence_display", respect=1)
        mc "I found the half of it that wasn't broken."
        eli "That's the half that takes longest."
    else:
        $ gain_skill_practice("mech", 4)
        "You spend eight minutes with a torch in your teeth confirming that a cabinet you've never seen before is wired in a way you don't understand."
        "By the time you've got a theory, someone with a meter and a laminated diagram has already fixed it."
        mc "I had a theory."
        eli "Was it the right theory?"
        mc "It was a theory."
        eli "That's most of the job."

    jump summer_festival_post_blackout


label summer_festival_blackout_organize:
    $ summer_festival_state["blackout_choice"] = "organize"
    $ summer_festival_state["blackout_result"] = "na"
    mc "Kill the burners at the top end first. Then get people off the middle of the road."
    "The staff member with the dead radio nods twice and goes, which is what people do when someone finally says a sentence with a verb in it."
    "It isn't heroic. It's standing in one place with your phone torch pointed at the ground and saying \"step down here\" four hundred times."
    n "Right. I've got the food end."
    "Nora is gone before anyone agrees to anything."
    "Zoe takes the top of the street and starts walking people around the candle stalls with the flat efficiency of someone who has thought about crowds before."
    "Marcus gets recruited to physically move a barrier, which is exactly the correct use of Marcus."
    m "This is the best night I've had in a month."
    eli "You're carrying a fence."
    m "I'm carrying a fence {i}with purpose{/i}."
    "By the time the staff have a working plan, the crowd has already sorted itself into something that isn't a hazard."
    "Nobody thanks anybody. It's the kind of help that only shows up as an absence of problems."
    $ apply_relationship_change("nora", "festival_blackout_organize", "helping_npc", trust=2, respect=2)
    $ apply_relationship_change("eli", "festival_blackout_organize", "helping_npc", respect=2)
    $ apply_relationship_change("zoe", "festival_blackout_organize", "helping_npc", respect=1)
    n "You're good at that."
    mc "I pointed at the floor."
    n "You pointed at the floor {i}first{/i}. That's the whole skill."
    jump summer_festival_post_blackout


label summer_festival_blackout_group:
    $ summer_festival_state["blackout_choice"] = "group"
    $ summer_festival_state["blackout_result"] = "na"
    mc "There's six staff and four hundred of us. Let's not add to it."
    m "That's the least heroic thing I've ever heard you say."
    mc "It's also correct."
    eli "It's also correct."
    m "Two of you. Great."
    "So you stay where you are, in a rough circle of five phone torches, and the street goes on being dark around you."
    "It turns out a crowd in the dark is mostly a crowd making jokes."
    z "Someone down there is doing shadow puppets."
    n "Is it good?"
    z "It's a dog. It's aggressively a dog."
    m "Every blackout I've ever been in, someone starts singing within four minutes."
    eli "That's not true."
    m "It's true."
    "Ninety seconds later somebody near the stage starts singing, badly, and about thirty people join in."
    m "Four minutes."
    eli "That was ninety seconds. Your claim was wrong and you were also lucky."
    m "I'll take it."
    n "You'd take anything."
    m "I would."
    "In the dark, standing close because that's where the light is, the five of you turn into a much smaller and more specific group than you were an hour ago."
    $ apply_relationship_change("nora", "festival_blackout_together", "shared_activity", familiarity=2)
    $ apply_relationship_change("marcus", "festival_blackout_together", "shared_activity", familiarity=2)
    $ apply_relationship_change("zoe", "festival_blackout_together", "shared_activity", familiarity=1)
    $ apply_relationship_change("eli", "festival_blackout_together", "shared_activity", familiarity=1)
    jump summer_festival_post_blackout


label summer_festival_post_blackout:
    if summer_festival_state["blackout_choice"] == "technical":
        z "You just walked off into the dark with a stranger and a torch."
        mc "He asked."
        z "He asked {i}everyone{/i}. You answered."
    elif summer_festival_state["blackout_choice"] == "organize":
        m "You went full site foreman."
        mc "Somebody had to."
        m "I'm not criticising. I'm noting it."
    else:
        n "Nobody died. I'm calling that a win."
        m "Low bar."
        n "Cleared bar."

    "Something lands on the back of your hand."
    "Then on the tarmac, in that specific pattern where the first ten drops arrive individually and the eleventh brings everyone else."

    # ── CG10 — rain ───────────────────────────────────────────────────────
    scene sf_rain with dissolve
    show screen hud
    "Four hundred people who were being extremely calm about a blackout lose their composure entirely about water."
    m "Go, go, go —"
    "Stall owners are throwing tarpaulins. Somebody's paper plate becomes a hat and then, immediately, doesn't."
    z "Under the awning. The wide one. Go."
    "You end up crushed under the canopy of a closed hardware shop with about forty other people, four of whom you came with."
    "The rain hits the awning like applause."

    # ── CG11 — shelter ────────────────────────────────────────────────────
    scene sf_shelter with dissolve
    show screen hud
    "It's warm rain. Summer rain. The kind that makes everyone smell like the pavement."
    n "My shoes."
    m "Your shoes are fine."
    n "My shoes are a swimming pool."
    m "Your shoes are a swimming pool that's fine."
    eli "The power outage and the rain are probably related."
    z "How."
    eli "Pressure drop, wind ahead of the front, something moved that shouldn't have. It's the sort of thing that happens forty minutes before rain rather than during it."
    m "So we could have known."
    eli "We could have known if any of us had looked up."
    m "I was busy."
    n "You were holding a fence."
    if summer_festival_state["blackout_choice"] == "organize":
        m "I was holding a fence {i}strategically{/i}."
    else:
        m "I was holding a {i}keyring{/i}."
    z "You are still holding the keyring."
    m "I will be holding this keyring for some time."

    "The conversation goes the way conversations go when everyone's damp and slightly tired and nobody has anywhere to be."
    "Somebody two metres away is telling a stranger their entire job history. Somebody else has produced a bag of crisps for forty people."
    n "This is the good part, by the way."
    mc "The standing under an awning part?"
    n "The nobody-leaves part. Everyone had a reason to go home twenty minutes ago and nobody's gone."

    "The group drifts into pairs, the way it does. There's a gap next to each of them."

    menu:
        "Marcus is quieter than he's been all night.":
            $ summer_festival_state["shelter_focus"] = "marcus"
            "He's watching the stage end of the street, where the band is sitting on the edge of the trailer with their instruments in bin bags."
            m "They're going to go back on."
            mc "In this?"
            m "Look at them. They've already decided. They just haven't said it."
            "A pause."
            m "I used to be able to tell that about people. On a court, I mean. Who'd already decided."
            mc "You still can."
            m "Yeah, well. Fewer courts."
            "He says it lightly and then doesn't say anything else, which for Marcus is the whole story."
            m "Anyway. They'll go back on."
            $ apply_relationship_change("marcus", "festival_shelter_moment",
                                        "meaningful_talk", affection=2, familiarity=1, meaningful=True)
        "Eli has gone quiet in an interesting way.":
            $ summer_festival_state["shelter_focus"] = "eli"
            "Eli is looking out at the rain running off the awning in a single unbroken sheet."
            eli "I've been avoiding a chapter for six weeks."
            mc "Still?"
            eli "Seven weeks, then. I'm rounding down."
            eli "The thing I keep getting stuck on is that all of this is measurable. Crowd density, load on the supply, drainage on this street. Somebody modelled all of it. Probably badly."
            mc "And?"
            eli "And nobody standing here cares, and it worked anyway."
            "A beat."
            eli "That's supposed to be reassuring. I haven't decided if it is."
            mc "You don't have to decide tonight."
            eli "No. That's the part I'm bad at."
            $ apply_relationship_change("eli", "festival_shelter_moment",
                                        "meaningful_talk", familiarity=2, trust=2, meaningful=True)
        "Zoe's watching the rain with that look she gets.":
            $ summer_festival_state["shelter_focus"] = "zoe"
            "She's not looking at the rain. She's looking at the light in it — the one string of bulbs still lit somewhere up the street, coming apart in the water."
            z "That."
            mc "That what?"
            z "That's the thing I've been trying to get out of the waterfront pieces for four months."
            z "It's not the reflection. It's that you can't tell where the light stops being the light."
            "She doesn't take a photo. She doesn't reach for a sketchbook."
            mc "You're not drawing it."
            z "It doesn't translate. That's the entire point of it."
            "A pause."
            z "I'll remember it wrong in about a week and paint that instead. That's usually better anyway."
            $ apply_relationship_change("zoe", "festival_shelter_moment",
                                        "meaningful_talk", affection=2, familiarity=1, meaningful=True)
        "Nora is laughing at something and it makes the whole awning lighter.":
            $ summer_festival_state["shelter_focus"] = "nora"
            "Someone has given her half a very bad pastry and she is reviewing it out loud to a stranger, at length, without mercy."
            n "— and it's not underbaked, that's the thing, it's {i}confidently{/i} underbaked —"
            "The stranger is delighted. Two more people have moved closer to listen."
            "She catches you watching and stops."
            n "What."
            mc "Nothing."
            n "You've got a face."
            mc "You're going to be good at the course."
            "That lands somewhere. She looks at the pastry instead of at you."
            n "I'm going to be terrible at it for about a year."
            mc "And then good at it."
            n "And then good at it."
            "She takes another bite of the bad pastry. She doesn't say thank you out loud."
            $ apply_relationship_change("nora", "festival_shelter_moment",
                                        "meaningful_talk", affection=2, familiarity=2, meaningful=True)

    m "Right — someone find out if that band's going back on."
    z "They're going back on. Look at them."
    n "Ten minutes. They'll want the rain to stop being the story."
    "The rain starts being less of a story."

    # ── CG12 — lights return ──────────────────────────────────────────────
    scene sf_lights with dissolve
    show screen hud
    "The bulbs over the road come up first, one string at a time, in the wrong order."
    "Half the street stays dark. Nobody minds. It looks better."
    if summer_festival_state["blackout_choice"] == "technical" and summer_festival_state["blackout_result"] in ("great", "critical"):
        "The staff member from earlier goes past, spots you, and gives you a thumbs up that is about seventy percent relief."
        z "Was that for you?"
        mc "Probably for the guy with the meter."
        eli "It was for you. He looked directly at you."
        m "Take the thumb."
        mc "I'm taking the thumb."
    elif summer_festival_state["blackout_choice"] == "technical":
        "Whoever finally sorted it doesn't come out to be looked at. That's usually how it goes."
        eli "You were closer than the first three people who tried."
        mc "Is that a compliment?"
        eli "It's a measurement."
    else:
        "Nobody comes out to explain what happened. The lights are on, so the question stops existing."
    "About a third of the crowd has gone home. The third that's left is the third that was always going to stay."
    "The band goes back on. Three songs, no lighting rig, and the sound is worse and better at the same time."
    m "Told you."
    z "Everyone told you. You just said it loudest."

    # ── CG13 — ending ─────────────────────────────────────────────────────
    scene sf_ending with dissolve
    show screen hud
    "The stalls come down faster than they went up. Trestle tables folding, cable being coiled by someone who is clearly not being paid enough to coil it properly."
    "The street starts being a street again."

    n "Right. I'm at six tomorrow."
    m "Six."
    n "Six."
    if summer_festival_state["shelter_focus"] == "nora":
        n "Text me when you get in. Not because anything's going to happen to you. Just do it."
    else:
        n "This was better than it had any right to be. Somebody should have organised it worse."
    "She goes. She's dry from the knees up and completely soaked below, and she's not going to mention it again."

    if npc_rel("zoe", "affection") >= 45:
        z "I'm walking. It's twenty minutes and I want to look at the wet buildings."
        mc "That's a real sentence you just said."
        z "It's the best sentence I've said all week."
    else:
        z "I'm walking. The light's still doing the thing."
    if summer_festival_state["shelter_focus"] == "zoe":
        z "I'll show you the wrong version. When it exists."
        mc "The wrong version."
        z "The good one."
    "She goes up the street rather than down it, which is the long way, which is obviously the point."

    eli "I have a chapter."
    m "It's midnight."
    eli "I have a chapter and now I have a reason not to open it, which is a better position than I was in this morning."
    if summer_festival_state["shelter_focus"] == "eli":
        "Eli pauses at the edge of the awning."
        eli "Thank you for not telling me to just write it."
        mc "Would that have helped?"
        eli "No. That's why."
    m "Get some sleep."
    eli "That was the plan and now it's the schedule."

    m "Well."
    "Marcus turns the keyring over in his hand once and puts it back in his pocket."
    if summer_festival_state["shelter_focus"] == "marcus":
        m "They went back on."
        mc "They went back on."
        m "Good."
        "That's the whole conversation and it's enough for him."
    elif summer_festival_state["blackout_choice"] == "technical":
        m "You disappeared into a dark alley to look at a fuse box for a street party. On a Friday."
        mc "It wasn't an alley."
        m "It was an alley."
    else:
        m "Nine words. Nine {i}good{/i} words."
    m "Knock if you need anything. Standing offer, still stands."
    "He walks the fifty metres home that you're also walking, which he does not comment on, and neither do you."

    "The barricades are already coming off the top of the road. Somebody's sweeping."
    "By tomorrow lunchtime there'll be nothing here but a street with buses on it."
    "You'd come out expecting a few tables and a speaker."
    "Your shoes are ruined."

    python:
        if not store.summer_festival_state["keepsake_awarded"]:
            if grant_possession("festival_wristband",
                                "summer_festival_day%d" % store.summer_festival_state["scheduled_day"]):
                store.summer_festival_state["keepsake_awarded"] = True
        record_accomplishment(
            "attended_summer_festival",
            "A Night at the Festival",
            "Spent an evening at the Downtown Summer Festival with Marcus, Eli, Zoe and Nora.",
            "social",
            {"blackout_choice": store.summer_festival_state["blackout_choice"],
             "shelter_focus": store.summer_festival_state["shelter_focus"]})
        record_game_event("summer_festival_attended", "journal",
                          "The Downtown Summer Festival",
                          summary=True, journal=True,
                          metadata={"blackout": store.summer_festival_state["blackout_choice"]})

    # The evening ends around 23:00 no matter which hour you walked in at, so
    # arriving late costs less time rather than pushing you past DAY_END.
    $ spend_time(max(1.0, 23.0 - _sf_start_hour))
    $ store.need_energy = max(0, store.need_energy - 20)
    $ set_hud("full")
    if summer_festival_state["keepsake_awarded"]:
        $ renpy.notify("Kept: Festival Wristband")
    jump location_centrum
