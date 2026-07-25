# phone_actionable.rpy — response option constants + accept/decline labels for the 5 invitations.
# Scene stubs live here too; replace with real content when art/writing is ready.

init python:
    _NORA_IGNORED_RESP = [
        {"id": "honest",  "text": "That's fair. I've been in my head. Coming in tomorrow.", "label": "phone_reply_nora_ignored_honest"},
        {"id": "deflect", "text": "Just busy. You know how it gets.",                        "label": "phone_reply_nora_ignored_deflect"},
        {"id": "sorry",   "text": "I'm sorry. I didn't realize.",                            "label": "phone_reply_nora_ignored_sorry"},
    ]
    _NORA_BAD_DAY_RESP = [
        {"id": "accept",  "text": "Come over.",    "label": "phone_reply_nora_bad_day_accept"},
        {"id": "decline", "text": "I'm fine.",     "label": "phone_reply_nora_bad_day_decline"},
    ]

    _MARTHA_COFFEE_RESP = [
        {"id": "accept",  "text": "That works.",     "label": "phone_reply_martha_coffee_accept"},
        {"id": "decline", "text": "Can't this week.", "label": "phone_reply_martha_coffee_decline"},
    ]
    _ELI_DEBUG_RESP = [
        {"id": "join",    "text": "I'll be there.",  "label": "phone_reply_eli_debug_join"},
        {"id": "decline", "text": "Next time.",       "label": "phone_reply_eli_debug_decline"},
    ]
    _LENA_CASE_RESP = [
        {"id": "accept",  "text": "I'll stay.",       "label": "phone_reply_lena_case_accept"},
        {"id": "decline", "text": "Not this time.",   "label": "phone_reply_lena_case_decline"},
    ]
    _NORA_CLOSING_RESP = [
        {"id": "join",    "text": "I'll be there.",  "label": "phone_reply_nora_closing_join"},
        {"id": "decline", "text": "Can't tonight.",   "label": "phone_reply_nora_closing_decline"},
    ]
    _NATALIE_SHIFT_RESP = [
        {"id": "in",      "text": "I'm in.",          "label": "phone_reply_natalie_shift_in"},
        {"id": "decline", "text": "Not this week.",   "label": "phone_reply_natalie_shift_decline"},
    ]
    _ELI_SIDE_RESP = [
        {"id": "invite",  "text": "Come over tomorrow evening.", "label": "phone_reply_eli_side_invite"},
        {"id": "remote",  "text": "Send me the repository.",     "label": "phone_reply_eli_side_remote"},
        {"id": "decline", "text": "Maybe another time.",         "label": "phone_reply_eli_side_decline"},
    ]
    _NORA_HOME_COFFEE_RESP = [
        {"id": "invite",  "text": "Come over whenever.",  "label": "phone_reply_nora_coffee_invite"},
        {"id": "decline", "text": "We'll survive.",        "label": "phone_reply_nora_coffee_decline"},
    ]
    _ZOE_GUITAR_RESP = [
        {"id": "prove",   "text": "Come over and judge.", "label": "phone_reply_zoe_guitar_invite"},
        {"id": "decline", "text": "It's decorative.",     "label": "phone_reply_zoe_guitar_decline"},
    ]
    _NORA_CHEAP_COOK_RESP = [
        {"id": "invite",  "text": "Come over, I'll have the kitchen ready.", "label": "phone_reply_nora_cheap_cook_invite"},
        {"id": "decline", "text": "Maybe another time.",                      "label": "phone_reply_nora_cheap_cook_decline"},
    ]


# ── Martha coffee ──────────────────────────────────────────────────────────────

label phone_reply_martha_coffee_accept:
    $ _day_mc = day + 1
    $ _cf = has_conflict(_day_mc, 17)
    if _cf:
        $ queue_phone_message("martha", "Good. 5pm, the Grounds on Crestwell. Don't be late.", day, "martha_coffee_confirm")
        $ queue_phone_message("martha", "(Note: you have another commitment that overlaps — %s at %02d:00)" % (_cf["title"], _cf["hour"]), day, "martha_coffee_conflict_warn")
    else:
        $ queue_phone_message("martha", "Good. 5pm tomorrow, the Grounds on Crestwell. Don't be late.", day, "martha_coffee_confirm")
    $ martha_coffee_accepted = True
    $ martha_coffee_day = _day_mc
    $ add_commitment("martha_coffee_1", "martha", "Coffee with Martha", _day_mc, 17, "Café Grounds", "phone_martha_coffee_scene")
    return

label phone_reply_martha_coffee_decline:
    $ martha_declined_invites.append("martha_coffee_1")
    $ queue_phone_message("martha", "No problem.", day, "martha_coffee_declined")
    return


label phone_martha_coffee_scene:
    $ martha_coffee_accepted = False
    $ complete_commitment("martha_coffee_1")
    scene cafeday
    show screen hud
    show martha_neutral at sprite_r
    "Martha is already there when you arrive. Two coffees on the table. She pushes one toward you."
    ma "I always order before the person gets there. Presumptuous — it's faster."
    menu:
        "\"How long have you been doing that?\"":
            ma "Fifteen years, give or take. Nobody's complained."
            $ _apply_aff("martha", 3)
        "\"Bold move.\"":
            ma "It's a latte. I took a risk."
            "A dry smile. The first one you've seen from her outside the office."
            $ _apply_aff("martha", 4)
            $ _apply_trust("martha", 2)
    ma "I wanted to say — you're handling the pressure well. Better than I did at your stage."
    ma "That's all. You can go back to being new now."
    hide martha_neutral
    $ _apply_trust("martha", 3)
    $ add_relationship_memory("martha", "martha_first_coffee", "Coffee outside work")
    return


# ── Eli debug session ──────────────────────────────────────────────────────────

label phone_reply_eli_debug_join:
    $ _day_eli = day + 1
    $ _cf = has_conflict(_day_eli, 19)
    if _cf:
        $ queue_phone_message("eli", "Hub at seven tomorrow. Bring your own headphones.", day, "eli_debug_confirm")
        $ queue_phone_message("eli", "(Note: overlaps with %s at %02d:00)" % (_cf["title"], _cf["hour"]), day, "eli_debug_conflict_warn")
    else:
        $ queue_phone_message("eli", "Hub at seven tomorrow. Bring your own headphones.", day, "eli_debug_confirm")
    $ eli_debug_joined = True
    $ eli_debug_day = _day_eli
    $ add_commitment("eli_debug_1", "eli", "Late debug session with Eli", _day_eli, 19, "The Hub", "phone_eli_debug_scene")
    return

label phone_reply_eli_debug_decline:
    $ queue_phone_message("eli", "Fine. I'll send you the notes.", day, "eli_debug_declined")
    return


label phone_eli_debug_scene:
    $ eli_debug_joined = False
    $ complete_commitment("eli_debug_1")
    scene hub_pov
    show screen hud
    "The office is empty at seven. Eli's already pulled up the flamegraph."
    eli "Pull up the profiler. I want a second read on this latency spike."
    "You work through it together. Eli talks less than usual — just asks questions."
    "An hour in, you catch something they missed."
    eli "Good catch. Write it up before you leave."
    $ _apply_trust("eli", 4)
    $ _apply_aff("eli", 2)
    $ gain_skill("prog", 4)
    $ add_relationship_memory("eli", "eli_debug_session", "Late debug session")
    return


# ── Lena case observation ──────────────────────────────────────────────────────

label phone_reply_lena_case_accept:
    $ _day_lena = next_weekday(2)
    $ _cf = has_conflict(_day_lena, 14)
    if _cf:
        $ queue_phone_message("lena", "Ward B, 2pm Wednesday. Meet me at the nursing station.", day, "lena_case_confirm")
        $ queue_phone_message("lena", "(Note: overlaps with %s at %02d:00)" % (_cf["title"], _cf["hour"]), day, "lena_case_conflict_warn")
    else:
        $ queue_phone_message("lena", "Ward B, 2pm Wednesday. Meet me at the nursing station.", day, "lena_case_confirm")
    $ lena_case_accepted = True
    $ lena_case_day = _day_lena
    $ add_commitment("lena_case_1", "lena", "Case observation with Dr. Lena", _day_lena, 14, "Hospital", "phone_lena_case_scene")
    return

label phone_reply_lena_case_decline:
    $ queue_phone_message("lena", "Another time.", day, "lena_case_declined")
    return


label phone_lena_case_scene:
    $ lena_case_accepted = False
    $ complete_commitment("lena_case_1")
    scene hospital1
    show screen hud
    show drlena_normal at sprite_r
    "The third-year presents the case. Complex, bilateral involvement, non-obvious history."
    "Lena listens without interrupting for two minutes. Then she asks one question. Everything shifts."
    lena "Write down what changed after the question. Not the answer — what the question did."
    hide drlena_normal
    "You fill half a page in your notes."
    $ _apply_trust("lena", 3)
    $ gain_skill("med", 5)
    $ add_relationship_memory("lena", "lena_case_observation", "Ward B case observation")
    return


# ── Nora closing ───────────────────────────────────────────────────────────────

label phone_reply_nora_closing_join:
    $ _day_nora = day + 1
    $ _cf = has_conflict(_day_nora, 21)
    if _cf:
        $ queue_phone_message("nora", "Good. Come in at nine tomorrow. I'll have the mop ready.", day, "nora_closing_confirm")
        $ queue_phone_message("nora", "(Note: overlaps with %s at %02d:00)" % (_cf["title"], _cf["hour"]), day, "nora_closing_conflict_warn")
    else:
        $ queue_phone_message("nora", "Good. Come in at nine tomorrow. I'll have the mop ready.", day, "nora_closing_confirm")
    $ nora_closing_accepted = True
    $ nora_closing_day = _day_nora
    $ add_commitment("nora_closing_1", "nora", "Close the café with Nora", _day_nora, 21, "Café Grounds", "phone_nora_closing_scene")
    return

label phone_reply_nora_closing_decline:
    $ queue_phone_message("nora", "Next time. Henry will be thrilled by his own company.", day, "nora_closing_declined")
    return


label phone_nora_closing_scene:
    $ nora_closing_accepted = False
    $ complete_commitment("nora_closing_1")
    scene cafenight
    show screen hud
    show nora_cafe_normal at sprite_r
    "Closing the café is quieter than a shift. Chairs up. Counters wiped. Henry went home at nine."
    n "Okay, I have a theory about the foam. Are you ready for this theory?"
    "You tell her you are."
    n "It's not the milk. It's the temperature. Everyone blames the milk."
    "She makes you a perfect flat white at 10pm to prove her point."
    $ _apply_aff("nora", 4)
    $ _apply_trust("nora", 2)
    hide nora_cafe_normal
    $ add_relationship_memory("nora", "nora_cafe_closing", "Closing the café together")
    return


# ── Natalie extra shift ────────────────────────────────────────────────────────

label phone_reply_natalie_shift_in:
    $ _day_nat = next_weekday(5)
    $ _cf = has_conflict(_day_nat, 8)
    if _cf:
        $ queue_phone_message("natalie", "Saturday 8am. Don't be late.", day, "natalie_shift_confirm")
        $ queue_phone_message("natalie", "(Note: overlaps with %s at %02d:00)" % (_cf["title"], _cf["hour"]), day, "natalie_shift_conflict_warn")
    else:
        $ queue_phone_message("natalie", "Saturday 8am. Don't be late.", day, "natalie_shift_confirm")
    $ natalie_extra_shift_day = _day_nat
    $ add_commitment("natalie_shift_1", "natalie", "Extra shift (Natalie)", _day_nat, 8, "Warehouse", "phone_natalie_extra_scene", grace=1.0)
    return

label phone_reply_natalie_shift_decline:
    $ queue_phone_message("natalie", "Fine. I'll find someone else.", day, "natalie_shift_declined")
    return


# ── Eli side project ──────────────────────────────────────────────────────────

label phone_reply_eli_side_invite:
    $ _day_esp = day + 1
    $ _cf = has_conflict(_day_esp, 19)
    if _cf:
        $ queue_phone_message("eli", "Tomorrow, 7pm then. I'll bring the repo.", day, "eli_side_project_confirm")
        $ queue_phone_message("eli", "(Note: overlaps with %s at %02d:00)" % (_cf["title"], _cf["hour"]), day, "eli_side_project_conflict")
    else:
        $ queue_phone_message("eli", "Tomorrow, 7pm then. I'll bring the repo.", day, "eli_side_project_confirm")
    $ add_commitment("eli_side_project_1", "eli", "Eli's side project", _day_esp, 19, "Your apartment", "home_eli_side_project_scene")
    return

label phone_reply_eli_side_remote:
    $ queue_phone_message("eli", "Repository link sent. Push when you have something.", day, "eli_side_project_remote")
    $ gain_skill("prog", 3)
    return

label phone_reply_eli_side_decline:
    $ queue_phone_message("eli", "No problem. I'll manage.", day, "eli_side_project_declined")
    return


# ── Nora coffee tasting ───────────────────────────────────────────────────────

label phone_reply_nora_coffee_invite:
    $ _day_nc = day + 1
    $ _cf = has_conflict(_day_nc, 10)
    if _cf:
        $ queue_phone_message("nora", "I'll be there at ten. Make sure it's clean.", day, "nora_coffee_confirm")
        $ queue_phone_message("nora", "(Note: overlaps with %s at %02d:00)" % (_cf["title"], _cf["hour"]), day, "nora_coffee_conflict")
    else:
        $ queue_phone_message("nora", "I'll be there at ten. Make sure it's clean.", day, "nora_coffee_confirm")
    $ add_commitment("nora_coffee_1", "nora", "Coffee tasting with Nora", _day_nc, 10, "Your apartment", "home_nora_coffee_scene")
    return

label phone_reply_nora_coffee_decline:
    $ queue_phone_message("nora", "Your loss. The machine will suffer.", day, "nora_coffee_declined")
    return


# ── Nora cheap-home cooking ───────────────────────────────────────────────────

label phone_reply_nora_cheap_cook_invite:
    $ _day_nck = day + 1
    $ _cf = has_conflict(_day_nck, 18)
    if _cf:
        $ queue_phone_message("nora", "I'll be there at six. Don't pre-season anything.", day, "nora_cheap_cook_confirm")
        $ queue_phone_message("nora", "(Note: overlaps with %s at %02d:00)" % (_cf["title"], _cf["hour"]), day, "nora_cheap_cook_conflict")
    else:
        $ queue_phone_message("nora", "I'll be there at six. Don't pre-season anything.", day, "nora_cheap_cook_confirm")
    $ add_commitment("nora_cheap_home_cooking_1", "nora", "Nora cooks at yours", _day_nck, 18, "Your apartment", "scene_nora_cheap_home_cooking")
    $ nora_cooking_state = "pending"
    return

label phone_reply_nora_cheap_cook_decline:
    $ nora_cooking_declined_day = day
    $ nora_cooking_state = "none"
    $ queue_phone_message("nora", "Fine. Suffer through it on your own.", day, "nora_cheap_cook_declined")
    return


# ── Zoe guitar session ────────────────────────────────────────────────────────

label phone_reply_zoe_guitar_invite:
    $ _day_zg = day + 1
    $ _cf = has_conflict(_day_zg, 17)
    if _cf:
        $ queue_phone_message("zoe", "Tomorrow at five. I'll bring my sketchbook.", day, "zoe_guitar_confirm")
        $ queue_phone_message("zoe", "(Note: overlaps with %s at %02d:00)" % (_cf["title"], _cf["hour"]), day, "zoe_guitar_conflict")
    else:
        $ queue_phone_message("zoe", "Tomorrow at five. I'll bring my sketchbook.", day, "zoe_guitar_confirm")
    $ add_commitment("zoe_guitar_1", "zoe", "Guitar session with Zoe", _day_zg, 17, "Your apartment", "home_zoe_guitar_scene")
    return

label phone_reply_zoe_guitar_decline:
    $ queue_phone_message("zoe", "It's furniture that makes ambient noise. Fine.", day, "zoe_guitar_declined")
    return


# ── Nora ignored ──────────────────────────────────────────────────────────────
label phone_reply_nora_ignored_honest:
    $ store.nora_ignored_response = "honest"
    $ _apply_aff("nora", 1)
    $ queue_phone_message("nora", "Tomorrow then.", store.day, "nora_ignored_reply_h")
    return

label phone_reply_nora_ignored_deflect:
    $ store.nora_ignored_response = "deflect"
    $ queue_phone_message("nora", "I do.", store.day, "nora_ignored_reply_d")
    return

label phone_reply_nora_ignored_sorry:
    $ store.nora_ignored_response = "sorry"
    $ queue_phone_message("nora", "Okay.", store.day, "nora_ignored_reply_s")
    return


# ── Nora bad day ──────────────────────────────────────────────────────────────
label phone_reply_nora_bad_day_accept:
    $ add_commitment("nora_bad_day_1", "nora", "Nora visits", store.day, 19, "Your apartment", "scene_nora_bad_day")
    $ queue_phone_message("nora", "On my way.", store.day, "nora_bad_day_accept_reply")
    return

label phone_reply_nora_bad_day_decline:
    $ store.nora_bad_day_pending = False
    $ queue_phone_message("nora", "Okay. Message me if that changes.", store.day, "nora_bad_day_decline_reply")
    return


label phone_natalie_extra_scene:
    $ natalie_extra_shift_day = -1
    $ complete_commitment("natalie_shift_1")
    scene pov_warehouse
    show screen hud
    "Short crew, double pace. Natalie works the line beside you for the first two hours."
    "She doesn't say much, but you notice she angles the heaviest pallets toward herself."
    "At the break she hands you a water and says: \"Not bad.\""
    "From Natalie, that's close to a speech."
    $ _apply_trust("natalie", 3)
    $ _apply_aff("natalie", 2)
    $ gain_stat("str", 8)
    $ gain_money(170)
    return
