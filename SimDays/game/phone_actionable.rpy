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

    # ── Phase 49: home-visit initiative response lists ────────────────────────
    _NORA_HOME_COFFEE_INI_RESP = [
        {"id": "accept",  "text": "Come over whenever.",               "label": "npc_ini_nora_home_coffee_accept"},
        {"id": "decline", "text": "We're surviving.",                  "label": "npc_ini_nora_home_coffee_decline"},
        {"id": "playful", "text": "The machine is doing great.",        "label": "npc_ini_nora_home_coffee_playful"},
    ]
    _ELI_HOME_DINNER_INI_RESP = [
        {"id": "accept",  "text": "Come over. I'll cook.",             "label": "npc_ini_eli_home_dinner_accept"},
        {"id": "decline", "text": "I maintain it wasn't complicated.",  "label": "npc_ini_eli_home_dinner_decline"},
        {"id": "playful", "text": "Evidence has been noted.",           "label": "npc_ini_eli_home_dinner_playful"},
    ]
    _ZOE_HOME_GUITAR_INI_RESP = [
        {"id": "accept",  "text": "Come over and find out.",           "label": "npc_ini_zoe_home_guitar_accept"},
        {"id": "decline", "text": "It's furniture. It's fine.",        "label": "npc_ini_zoe_home_guitar_decline"},
        {"id": "playful", "text": "It plays ambient noise when no one is looking.", "label": "npc_ini_zoe_home_guitar_playful"},
    ]
    # Phase 50: Zoe exhibition invitation
    _ZOE_EXHIBITION_INI_RESP = [
        {"id": "accept",  "text": "I'll be there.",     "label": "npc_ini_zoe_exhibition_accept"},
        {"id": "decline", "text": "I can't make it.",   "label": "npc_ini_zoe_exhibition_decline"},
        {"id": "playful", "text": "Define 'weird'.",    "label": "npc_ini_zoe_exhibition_playful"},
    ]

    # ── Phase 30: NPC-initiated message response lists ────────────────────────

    _MARCUS_PARK_RESP = [
        {"id": "yeah",  "text": "Yeah. I'll stop by.",   "label": "npc_ini_marcus_park_yeah"},
        {"id": "maybe", "text": "Maybe.",                 "label": "npc_ini_marcus_park_maybe"},
        {"id": "no",    "text": "Not today.",             "label": "npc_ini_marcus_park_no"},
    ]
    _NORA_TRY_DRINK_RESP = [
        {"id": "risky", "text": "That sounds risky.",    "label": "npc_ini_nora_drink_risky"},
        {"id": "what",  "text": "What is it?",           "label": "npc_ini_nora_drink_what"},
        {"id": "other", "text": "Ask someone else.",     "label": "npc_ini_nora_drink_other"},
    ]
    _NORA_DATE_STATIC_RESP = [
        {"id": "asking", "text": "What's the occasion?", "label": "npc_ini_nora_date_asking"},
        {"id": "where",  "text": "Which bar?",           "label": "npc_ini_nora_date_where"},
        {"id": "not",    "text": "Not tonight.",         "label": "npc_ini_nora_date_not"},
    ]
    _ZOE_DATE_BEACH_RESP = [
        {"id": "date",  "text": "That sounds like a date.", "label": "npc_ini_zoe_beach_date"},
        {"id": "come",  "text": "I'll come by.",            "label": "npc_ini_zoe_beach_come"},
        {"id": "not",   "text": "Not today.",               "label": "npc_ini_zoe_beach_not"},
    ]

    _MARCUS_CHECKIN_RESP = [
        {"id": "mostly", "text": "Mostly.",                  "label": "npc_ini_marcus_checkin_mostly"},
        {"id": "busy",   "text": "Busy.",                    "label": "npc_ini_marcus_checkin_busy"},
        {"id": "why",    "text": "Why?",                     "label": "npc_ini_marcus_checkin_why"},
    ]
    _MARCUS_FOOD_RESP = [
        {"id": "again",  "text": "Again?",                   "label": "npc_ini_marcus_food_again"},
        {"id": "invite", "text": "Is this an invitation?",   "label": "npc_ini_marcus_food_invite"},
        {"id": "save",   "text": "Save it for tomorrow.",    "label": "npc_ini_marcus_food_save"},
    ]
    _NORA_SHIFT_RESP = [
        {"id": "answer", "text": "Did you answer?",          "label": "npc_ini_nora_shift_answer"},
        {"id": "six",    "text": "Six?",                     "label": "npc_ini_nora_shift_six"},
        {"id": "normal", "text": "Sounds normal.",           "label": "npc_ini_nora_shift_normal"},
    ]
    _NORA_REC_RESP = [
        {"id": "why",    "text": "Why?",                     "label": "npc_ini_nora_rec_why"},
        {"id": "warn",   "text": "Was that a warning?",      "label": "npc_ini_nora_rec_warn"},
        {"id": "going",  "text": "I was going to.",          "label": "npc_ini_nora_rec_going"},
    ]
    _ZOE_PARK_OPINION_RESP = [
        {"id": "stopby",  "text": "I can stop by.",               "label": "npc_ini_zoe_park_stopby"},
        {"id": "what",    "text": "What is it?",                  "label": "npc_ini_zoe_park_what"},
        {"id": "no",      "text": "Not today.",                   "label": "npc_ini_zoe_park_no"},
    ]
    _ELI_LIBRARY_TABLE_RESP = [
        {"id": "save",    "text": "Save me one.",                 "label": "npc_ini_eli_table_save"},
        {"id": "both",    "text": "Both outlets work?",           "label": "npc_ini_eli_table_both"},
        {"id": "busy",    "text": "I'm busy.",                    "label": "npc_ini_eli_table_busy"},
    ]

    _ZOE_PHOTO_RESP = [
        {"id": "wrong",  "text": "Wrong compared to what?", "label": "npc_ini_zoe_photo_wrong"},
        {"id": "proof",  "text": "Send proof.",              "label": "npc_ini_zoe_photo_proof"},
        {"id": "build",  "text": "Maybe the building is wrong.", "label": "npc_ini_zoe_photo_build"},
    ]
    _ZOE_QUESTION_RESP = [
        {"id": "three",  "text": "Three.",                   "label": "npc_ini_zoe_question_three"},
        {"id": "five",   "text": "Five.",                    "label": "npc_ini_zoe_question_five"},
        {"id": "birds",  "text": "Depends on the birds.",    "label": "npc_ini_zoe_question_birds"},
    ]
    _ELI_BUG_RESP = [
        {"id": "which",   "text": "Which one?",              "label": "npc_ini_eli_bug_which"},
        {"id": "congrats","text": "Congratulations.",        "label": "npc_ini_eli_bug_congrats"},
        {"id": "home",    "text": "Go home.",                "label": "npc_ini_eli_bug_home"},
    ]
    _ELI_LIBRARY_RESP = [
        {"id": "report", "text": "Did you report it?",       "label": "npc_ini_eli_library_report"},
        {"id": "walk",   "text": "Walk away.",               "label": "npc_ini_eli_library_walk"},
        {"id": "off",    "text": "Turn it off and on.",      "label": "npc_ini_eli_library_off"},
    ]

    # ── Phase 39: tier-specific response lists ───────────────────────────────
    _MARCUS_FAMILIAR_FOOD_RESP = [
        {"id": "yes",      "text": "Yes.",                                          "label": "npc_ini_marcus_familiar_food_yes"},
        {"id": "notyet",   "text": "Not yet.",                                      "label": "npc_ini_marcus_familiar_food_notyet"},
        {"id": "vending",  "text": "Vending machines provide.",                     "label": "npc_ini_marcus_familiar_food_vending"},
    ]
    _MARCUS_CLOSE_CHECKIN_RESP = [
        {"id": "fine",     "text": "I'm fine.",                                     "label": "npc_ini_marcus_close_checkin_fine"},
        {"id": "tired",    "text": "Just tired.",                                   "label": "npc_ini_marcus_close_checkin_tired"},
        {"id": "notreally","text": "Not really.",                                   "label": "npc_ini_marcus_close_checkin_notreally"},
    ]
    _NORA_FAMILIAR_CUSTOMER_RESP = [
        {"id": "wanted",   "text": "What did they want?",                           "label": "npc_ini_nora_familiar_customer_wanted"},
        {"id": "again",    "text": "Surprise them again.",                          "label": "npc_ini_nora_familiar_customer_again"},
        {"id": "refuse",   "text": "Refuse.",                                       "label": "npc_ini_nora_familiar_customer_refuse"},
    ]
    _NORA_CLOSE_DISTRACTION_RESP = [
        {"id": "dog",      "text": "I saw a dog carrying a stick twice its size.",  "label": "npc_ini_nora_close_distraction_dog"},
        {"id": "city",     "text": "The city nearly defeated me.",                  "label": "npc_ini_nora_close_distraction_city"},
        {"id": "coffee",   "text": "I only have coffee-related material.",          "label": "npc_ini_nora_close_distraction_coffee"},
    ]
    _ZOE_FAMILIAR_SKETCH_RESP = [
        {"id": "wrong",    "text": "Was I wrong?",                                  "label": "npc_ini_zoe_familiar_sketch_wrong"},
        {"id": "show",     "text": "Show me the new one.",                          "label": "npc_ini_zoe_familiar_sketch_show"},
        {"id": "relevant", "text": "I preferred being relevant.",                   "label": "npc_ini_zoe_familiar_sketch_relevant"},
    ]
    _ZOE_CLOSE_QUIET_RESP = [
        {"id": "where",    "text": "Where?",                                        "label": "npc_ini_zoe_close_quiet_where"},
        {"id": "keeping",  "text": "Are you keeping it?",                           "label": "npc_ini_zoe_close_quiet_keeping"},
        {"id": "suspect",  "text": "That sounds suspicious.",                       "label": "npc_ini_zoe_close_quiet_suspect"},
    ]
    _ELI_FAMILIAR_DEBUG_RESP = [
        {"id": "fixed",    "text": "Did you fix it?",                               "label": "npc_ini_eli_familiar_debug_fixed"},
        {"id": "noone",    "text": "Tell no one.",                                  "label": "npc_ini_eli_familiar_debug_noone"},
        {"id": "twenty",   "text": "Only twenty?",                                  "label": "npc_ini_eli_familiar_debug_twenty"},
    ]
    _ELI_CLOSE_COMPANY_RESP = [
        {"id": "company",  "text": "Want company?",                                 "label": "npc_ini_eli_close_company_company"},
        {"id": "home",     "text": "Go home.",                                      "label": "npc_ini_eli_close_company_home"},
        {"id": "silence",  "text": "Enjoy the silence.",                            "label": "npc_ini_eli_close_company_silence"},
    ]

    # ── Phase 38: Wave 2 atmospheric response lists ──────────────────────────
    _MARTHA_REVISION_RESP = [
        {"id": "final",    "text": "Was it final?",         "label": "npc_ini_martha_revision_final"},
        {"id": "official", "text": "That sounds official.", "label": "npc_ini_martha_revision_official"},
        {"id": "delete",   "text": "Delete it.",            "label": "npc_ini_martha_revision_delete"},
    ]
    _MARTHA_CALENDAR_RESP = [
        {"id": "accept",  "text": "Did you accept?",        "label": "npc_ini_martha_calendar_accept"},
        {"id": "decline", "text": "Decline it.",            "label": "npc_ini_martha_calendar_decline"},
        {"id": "work",    "text": "Maybe it will work.",    "label": "npc_ini_martha_calendar_work"},
    ]
    _LENA_COFFEE_RESP = [
        {"id": "legal",   "text": "That is no longer coffee.",  "label": "npc_ini_lena_coffee_legal"},
        {"id": "water",   "text": "Drink some water.",          "label": "npc_ini_lena_coffee_water"},
        {"id": "fourth",  "text": "Fourth time?",               "label": "npc_ini_lena_coffee_fourth"},
    ]
    _LENA_WAITING_RESP = [
        {"id": "stopped",  "text": "Maybe the weather stopped.", "label": "npc_ini_lena_waiting_stopped"},
        {"id": "off",      "text": "Turn it off.",               "label": "npc_ini_lena_waiting_off"},
        {"id": "accurate", "text": "At least it is accurate.",   "label": "npc_ini_lena_waiting_accurate"},
    ]
    _SAM_SORENESS_RESP = [
        {"id": "no",     "text": "No.",                    "label": "npc_ini_sam_soreness_no"},
        {"id": "down",   "text": "Only going down.",       "label": "npc_ini_sam_soreness_down"},
        {"id": "slowly", "text": "Depends how slowly.",   "label": "npc_ini_sam_soreness_slowly"},
    ]
    _SAM_MUSIC_RESP = [
        {"id": "good",   "text": "Good workout song?",    "label": "npc_ini_sam_music_good"},
        {"id": "change", "text": "Change it.",            "label": "npc_ini_sam_music_change"},
        {"id": "sing",   "text": "Sing along.",           "label": "npc_ini_sam_music_sing"},
    ]
    _NATALIE_DELIVERY_RESP = [
        {"id": "efficient", "text": "Efficient.",          "label": "npc_ini_natalie_delivery_efficient"},
        {"id": "back",      "text": "Send it back.",       "label": "npc_ini_natalie_delivery_back"},
        {"id": "worse",     "text": "Could be worse.",     "label": "npc_ini_natalie_delivery_worse"},
    ]
    _NATALIE_CLIPBOARD_RESP = [
        {"id": "found",   "text": "Did you find it?",     "label": "npc_ini_natalie_clipboard_found"},
        {"id": "another", "text": "Buy another one.",     "label": "npc_ini_natalie_clipboard_another"},
        {"id": "ask",     "text": "Ask everyone.",        "label": "npc_ini_natalie_clipboard_ask"},
    ]

    # ── Phase 40: Wave 2 tier-specific response lists ─────────────────────────
    _MARTHA_FAMILIAR_ATTACHMENT_RESP = [
        {"id": "used",    "text": "Did you use it?",      "label": "npc_ini_martha_familiar_attachment_used"},
        {"id": "reassure","text": "Very reassuring.",     "label": "npc_ini_martha_familiar_attachment_reassure"},
        {"id": "back",    "text": "Send it back.",        "label": "npc_ini_martha_familiar_attachment_back"},
    ]
    _MARTHA_CLOSE_LONG_DAY_RESP = [
        {"id": "productive","text": "Productive.",        "label": "npc_ini_martha_close_long_day_productive"},
        {"id": "tired",   "text": "You sound tired.",     "label": "npc_ini_martha_close_long_day_tired"},
        {"id": "yours",   "text": "Was it your decision?","label": "npc_ini_martha_close_long_day_yours"},
    ]
    _LENA_FAMILIAR_LUNCH_RESP = [
        {"id": "halfway", "text": "That only counts halfway.",    "label": "npc_ini_lena_familiar_lunch_halfway"},
        {"id": "eat",     "text": "Eat it now.",                  "label": "npc_ini_lena_familiar_lunch_eat"},
        {"id": "what",    "text": "What was it?",                 "label": "npc_ini_lena_familiar_lunch_what"},
    ]
    _LENA_CLOSE_SHIFT_RESP = [
        {"id": "you",     "text": "And you?",             "label": "npc_ini_lena_close_shift_you"},
        {"id": "notquestion","text": "That was not the question.", "label": "npc_ini_lena_close_shift_notquestion"},
        {"id": "rest",    "text": "Get some rest.",       "label": "npc_ini_lena_close_shift_rest"},
    ]
    _SAM_FAMILIAR_PROGRAM_RESP = [
        {"id": "strong",  "text": "Strong start.",        "label": "npc_ini_sam_familiar_program_strong"},
        {"id": "why",     "text": "Why write it?",        "label": "npc_ini_sam_familiar_program_why"},
        {"id": "tomorrow","text": "Follow it tomorrow.",  "label": "npc_ini_sam_familiar_program_tomorrow"},
    ]
    _SAM_CLOSE_REST_RESP = [
        {"id": "needed",  "text": "You needed it.",       "label": "npc_ini_sam_close_rest_needed"},
        {"id": "anyway",  "text": "Go train anyway.",     "label": "npc_ini_sam_close_rest_anyway"},
        {"id": "nothing", "text": "Enjoy doing nothing.", "label": "npc_ini_sam_close_rest_nothing"},
    ]
    _NATALIE_FAMILIAR_LABEL_RESP = [
        {"id": "what",    "text": "What was on it?",      "label": "npc_ini_natalie_familiar_label_what"},
        {"id": "accurate","text": "Accurate?",            "label": "npc_ini_natalie_familiar_label_accurate"},
        {"id": "relabel", "text": "Relabel it.",          "label": "npc_ini_natalie_familiar_label_relabel"},
    ]
    _NATALIE_CLOSE_QUIET_RESP = [
        {"id": "enjoy",   "text": "Enjoy it.",            "label": "npc_ini_natalie_close_quiet_enjoy"},
        {"id": "ominous", "text": "That sounds ominous.", "label": "npc_ini_natalie_close_quiet_ominous"},
        {"id": "home",    "text": "Go home.",             "label": "npc_ini_natalie_close_quiet_home"},
    ]

    # ── Phase 41: VERY_CLOSE response lists ──────────────────────────────────
    _MARCUS_VERY_CLOSE_BAD_DAY_RESP = [
        {"id": "itwas",   "text": "It was.",              "label": "npc_ini_marcus_very_close_bad_day_itwas"},
        {"id": "notreally","text": "Not really.",         "label": "npc_ini_marcus_very_close_bad_day_notreally"},
        {"id": "maybe",   "text": "Maybe a little.",      "label": "npc_ini_marcus_very_close_bad_day_maybe"},
    ]
    _NORA_VERY_CLOSE_THOUGHT_RESP = [
        {"id": "fourth",  "text": "This is the fourth?", "label": "npc_ini_nora_very_close_thought_fourth"},
        {"id": "couldve", "text": "You could have.",      "label": "npc_ini_nora_very_close_thought_couldve"},
        {"id": "happened","text": "What happened?",       "label": "npc_ini_nora_very_close_thought_happened"},
    ]
    _ZOE_VERY_CLOSE_REMINDER_RESP = [
        {"id": "whatwas", "text": "What was it?",         "label": "npc_ini_zoe_very_close_reminder_whatwas"},
        {"id": "why",     "text": "Why annoying?",        "label": "npc_ini_zoe_very_close_reminder_why"},
        {"id": "honoured","text": "I'm honoured.",        "label": "npc_ini_zoe_very_close_reminder_honoured"},
    ]
    _ELI_VERY_CLOSE_BAD_DAY_RESP = [
        {"id": "stillcan","text": "You still can.",       "label": "npc_ini_eli_very_close_bad_day_stillcan"},
        {"id": "howbad",  "text": "How bad?",             "label": "npc_ini_eli_very_close_bad_day_howbad"},
        {"id": "okay",    "text": "You okay?",            "label": "npc_ini_eli_very_close_bad_day_okay"},
    ]
    _MARTHA_VERY_CLOSE_LEFT_EARLY_RESP = [
        {"id": "proud",   "text": "Proud of you.",        "label": "npc_ini_martha_very_close_left_early_proud"},
        {"id": "wrong",   "text": "What went wrong?",     "label": "npc_ini_martha_very_close_left_early_wrong"},
        {"id": "again",   "text": "Do it again tomorrow.","label": "npc_ini_martha_very_close_left_early_again"},
    ]
    _LENA_VERY_CLOSE_QUIET_RESP = [
        {"id": "sitdown", "text": "Sit down.",            "label": "npc_ini_lena_very_close_quiet_sitdown"},
        {"id": "callme",  "text": "Call me next time.",   "label": "npc_ini_lena_very_close_quiet_callme"},
        {"id": "silence", "text": "Enjoy the silence.",   "label": "npc_ini_lena_very_close_quiet_silence"},
    ]
    _SAM_VERY_CLOSE_REST_RESP = [
        {"id": "recognised","text": "Recognised.",        "label": "npc_ini_sam_very_close_rest_recognised"},
        {"id": "exhausted","text": "You were exhausted?", "label": "npc_ini_sam_very_close_rest_exhausted"},
        {"id": "again",   "text": "Rest again tomorrow.", "label": "npc_ini_sam_very_close_rest_again"},
    ]
    _NATALIE_VERY_CLOSE_DAYLIGHT_RESP = [
        {"id": "andyou",  "text": "And you?",             "label": "npc_ini_natalie_very_close_daylight_andyou"},
        {"id": "enjoy",   "text": "Enjoy it.",            "label": "npc_ini_natalie_very_close_daylight_enjoy"},
        {"id": "survive", "text": "They will survive.",   "label": "npc_ini_natalie_very_close_daylight_survive"},
    ]

    _INITIATIVE_MSGS = {
        "marcus_msg_checkin":      {"text": "Still alive?",                 "responses": _MARCUS_CHECKIN_RESP},
        "marcus_msg_food":         {"text": "I ordered too much food.",     "responses": _MARCUS_FOOD_RESP},
        "marcus_msg_park":         {"text": "I'm heading to the park later. You around?", "responses": _MARCUS_PARK_RESP},
        "nora_msg_shift":          {"text": "Someone ordered a drink with six modifications and then asked why it took longer.", "responses": _NORA_SHIFT_RESP},
        "nora_msg_recommendation": {"text": "Do not order the seasonal special today.", "responses": _NORA_REC_RESP},
        "nora_msg_try_drink":      {"text": "I need an unbiased opinion on something before I put it on the board.", "responses": _NORA_TRY_DRINK_RESP},
        "zoe_msg_photo":           {"text": "I found a wall that is the wrong colour.", "responses": _ZOE_PHOTO_RESP},
        "zoe_msg_question":        {"text": "How many birds make a pattern?", "responses": _ZOE_QUESTION_RESP},
        "zoe_msg_park_opinion":    {"text": "I need a second opinion on something. Park?", "responses": _ZOE_PARK_OPINION_RESP},
        "eli_msg_bug":             {"text": "I fixed the bug.",             "responses": _ELI_BUG_RESP},
        "eli_msg_library":         {"text": "The library printer is making the same noise again.", "responses": _ELI_LIBRARY_RESP},
        "eli_msg_library_table":   {"text": "I found a library table with two working outlets. This may not last.", "responses": _ELI_LIBRARY_TABLE_RESP},
        "nora_msg_date_static":    {"text": "You should come to Static tonight.",        "responses": _NORA_DATE_STATIC_RESP},
        "zoe_msg_date_beach":      {"text": "I'm at the beach. You should be too.",      "responses": _ZOE_DATE_BEACH_RESP},
        "martha_msg_revision":     {"text": "I received a document called FINAL_v7_ACTUAL.", "responses": _MARTHA_REVISION_RESP},
        "martha_msg_calendar":     {"text": "Someone scheduled a meeting to discuss reducing meetings.", "responses": _MARTHA_CALENDAR_RESP},
        "lena_msg_coffee":         {"text": "I reheated the same coffee three times and still have not tasted it.", "responses": _LENA_COFFEE_RESP},
        "lena_msg_waiting_room":   {"text": "The waiting room television has been showing the same weather report for an hour.", "responses": _LENA_WAITING_RESP},
        "sam_msg_soreness":        {"text": "Important question. Do stairs count as recovery?", "responses": _SAM_SORENESS_RESP},
        "sam_msg_gym_music":       {"text": "Someone put a twelve-minute ballad on the gym playlist.", "responses": _SAM_MUSIC_RESP},
        "natalie_msg_delivery":        {"text": "A delivery arrived early, incomplete and somehow in the wrong bay.", "responses": _NATALIE_DELIVERY_RESP},
        "natalie_msg_clipboard":       {"text": "Someone moved my clipboard.",               "responses": _NATALIE_CLIPBOARD_RESP},
        "martha_msg_familiar_attachment": {"text": "Someone sent me an attachment called use_this_one_revised_final.", "responses": _MARTHA_FAMILIAR_ATTACHMENT_RESP},
        "martha_msg_close_long_day":      {"text": "Today contained four meetings and one actual decision.",           "responses": _MARTHA_CLOSE_LONG_DAY_RESP},
        "lena_msg_familiar_lunch":        {"text": "I remembered to bring lunch and forgot to eat it.",               "responses": _LENA_FAMILIAR_LUNCH_RESP},
        "lena_msg_close_shift":           {"text": "Long shift. Everyone is stable, which is the important part.",    "responses": _LENA_CLOSE_SHIFT_RESP},
        "sam_msg_familiar_program":       {"text": "I wrote a new training plan and immediately ignored it.",         "responses": _SAM_FAMILIAR_PROGRAM_RESP},
        "sam_msg_close_rest_day":         {"text": "I took a rest day. I hate how reasonable it feels.",             "responses": _SAM_CLOSE_REST_RESP},
        "natalie_msg_familiar_label":     {"text": "Someone labelled a pallet miscellaneous.",                       "responses": _NATALIE_FAMILIAR_LABEL_RESP},
        "natalie_msg_close_quiet":        {"text": "The warehouse is finally quiet.",                                 "responses": _NATALIE_CLOSE_QUIET_RESP},
        "marcus_msg_very_close_bad_day":  {"text": "You don't have to answer immediately. Just checking whether today was one of the bad ones.", "responses": _MARCUS_VERY_CLOSE_BAD_DAY_RESP},
        "nora_msg_very_close_thought":    {"text": "I almost texted you three times today and then decided that sounded excessive.",             "responses": _NORA_VERY_CLOSE_THOUGHT_RESP},
        "zoe_msg_very_close_reminder":    {"text": "I found something today that made me think of you. Annoying, because now I have to admit that.", "responses": _ZOE_VERY_CLOSE_REMINDER_RESP},
        "eli_msg_very_close_bad_day":     {"text": "I had a bad day and almost sent you a very long message about it.",                          "responses": _ELI_VERY_CLOSE_BAD_DAY_RESP},
        "martha_msg_very_close_left_early":{"text": "I left the office on time. I am documenting this before it becomes disputed.",              "responses": _MARTHA_VERY_CLOSE_LEFT_EARLY_RESP},
        "lena_msg_very_close_quiet":      {"text": "I had ten quiet minutes today and realised I did not know what to do with them.",            "responses": _LENA_VERY_CLOSE_QUIET_RESP},
        "sam_msg_very_close_rest":        {"text": "I cancelled training because I was exhausted. I would like this decision officially recognised as mature.", "responses": _SAM_VERY_CLOSE_REST_RESP},
        "natalie_msg_very_close_daylight":{"text": "I went home while there was still daylight. Nobody at the warehouse knows how to process this.", "responses": _NATALIE_VERY_CLOSE_DAYLIGHT_RESP},
        "marcus_msg_familiar_food":    {"text": "Did you eat something that did not come from a vending machine today?", "responses": _MARCUS_FAMILIAR_FOOD_RESP},
        "marcus_msg_close_checkin":    {"text": "You seemed a little off earlier. Everything okay?",                     "responses": _MARCUS_CLOSE_CHECKIN_RESP},
        "nora_msg_familiar_customer":  {"text": "A customer told me to surprise them and then rejected every surprise.", "responses": _NORA_FAMILIAR_CUSTOMER_RESP},
        "nora_msg_close_distraction":  {"text": "Long day. Tell me something that has nothing to do with coffee.",       "responses": _NORA_CLOSE_DISTRACTION_RESP},
        "zoe_msg_familiar_sketch":     {"text": "I changed the drawing. Your opinion is now technically obsolete.",      "responses": _ZOE_FAMILIAR_SKETCH_RESP},
        "zoe_msg_close_quiet":         {"text": "I found somewhere in the city that is almost completely quiet.",        "responses": _ZOE_CLOSE_QUIET_RESP},
        "eli_msg_familiar_debug":      {"text": "I spent twenty minutes debugging something that was not plugged in.",   "responses": _ELI_FAMILIAR_DEBUG_RESP},
        "eli_msg_close_company":       {"text": "I am working late. The office is quieter when nobody is trying to help.", "responses": _ELI_CLOSE_COMPANY_RESP},
        # Phase 49: home-visit invitation variants
        "nora_msg_home_coffee": {"text": "I keep thinking about that machine in your kitchen. It deserves better than whatever you're doing to it.", "responses": _NORA_HOME_COFFEE_INI_RESP},
        "eli_msg_home_dinner":  {"text": "You said dinner at your place wouldn't be complicated. I have retained the message as evidence.", "responses": _ELI_HOME_DINNER_INI_RESP},
        "zoe_msg_home_guitar":  {"text": "Do you actually play that guitar, or is it part of the furniture?", "responses": _ZOE_HOME_GUITAR_INI_RESP},
        # Phase 50: Zoe exhibition invitation
        "zoe_msg_exhibition_invite": {"text": "The group show is actually happening. You can come, but you're not allowed to make it weird.", "responses": _ZOE_EXHIBITION_INI_RESP},
    }

    _INITIATIVE_COOLDOWNS = {"marcus": 3, "nora": 4, "zoe": 4, "eli": 5,
                             "martha": 5, "lena": 5, "sam": 4, "natalie": 6}
    _INITIATIVE_VARIANTS  = {
        "marcus":  ["marcus_msg_checkin",   "marcus_msg_food",          "marcus_msg_park",
                    "marcus_msg_familiar_food", "marcus_msg_close_checkin",
                    "marcus_msg_very_close_bad_day"],
        "nora":    ["nora_msg_shift",       "nora_msg_recommendation",  "nora_msg_try_drink", "nora_msg_date_static",
                    "nora_msg_familiar_customer", "nora_msg_close_distraction",
                    "nora_msg_very_close_thought", "nora_msg_home_coffee"],
        "zoe":     ["zoe_msg_photo",        "zoe_msg_question",         "zoe_msg_park_opinion", "zoe_msg_date_beach",
                    "zoe_msg_familiar_sketch", "zoe_msg_close_quiet",
                    "zoe_msg_very_close_reminder", "zoe_msg_home_guitar",
                    "zoe_msg_exhibition_invite"],
        "eli":     ["eli_msg_bug",          "eli_msg_library",          "eli_msg_library_table",
                    "eli_msg_familiar_debug", "eli_msg_close_company",
                    "eli_msg_very_close_bad_day", "eli_msg_home_dinner"],
        "martha":  ["martha_msg_revision",  "martha_msg_calendar",
                    "martha_msg_familiar_attachment", "martha_msg_close_long_day",
                    "martha_msg_very_close_left_early"],
        "lena":    ["lena_msg_coffee",      "lena_msg_waiting_room",
                    "lena_msg_familiar_lunch", "lena_msg_close_shift",
                    "lena_msg_very_close_quiet"],
        "sam":     ["sam_msg_soreness",     "sam_msg_gym_music",
                    "sam_msg_familiar_program", "sam_msg_close_rest_day",
                    "sam_msg_very_close_rest"],
        "natalie": ["natalie_msg_delivery", "natalie_msg_clipboard",
                    "natalie_msg_familiar_label", "natalie_msg_close_quiet",
                    "natalie_msg_very_close_daylight"],
    }
    _INITIATIVE_WEIGHT = {"high": 3, "medium": 2, "low": 1}
    _INITIATIVE_NPCS   = ["marcus", "nora", "zoe", "eli", "martha", "lena", "sam", "natalie"]
    # Variants that create an invitation — excluded while one is already active.
    _INV_VARIANTS = {"marcus_msg_park", "nora_msg_try_drink", "zoe_msg_park_opinion", "eli_msg_library_table",
                     "nora_msg_date_static", "zoe_msg_date_beach",
                     "nora_msg_home_coffee", "eli_msg_home_dinner", "zoe_msg_home_guitar",
                     "zoe_msg_exhibition_invite"}
    # Date invitation variants — require CLOSE tier and romance eligibility.
    _DATE_VARIANTS = {"nora_msg_date_static", "zoe_msg_date_beach"}
    _DATE_INVITE_COOLDOWNS = {"nora": 12, "zoe": 14}
    # Per-variant weights: atmospheric=4 (default), familiar=3, close=2, invitation=2, date=1.
    _VARIANT_WEIGHTS = {
        "marcus_msg_park":            2,
        "nora_msg_try_drink":         2,
        "zoe_msg_park_opinion":       2,
        "eli_msg_library_table":      2,
        "nora_msg_date_static":       1,
        "zoe_msg_date_beach":         1,
        "marcus_msg_familiar_food":   3,
        "marcus_msg_close_checkin":   2,
        "nora_msg_familiar_customer": 3,
        "nora_msg_close_distraction": 2,
        "zoe_msg_familiar_sketch":    3,
        "zoe_msg_close_quiet":        2,
        "eli_msg_familiar_debug":     3,
        "eli_msg_close_company":      2,
        "martha_msg_familiar_attachment": 3,
        "martha_msg_close_long_day":      2,
        "lena_msg_familiar_lunch":        3,
        "lena_msg_close_shift":           2,
        "sam_msg_familiar_program":       3,
        "sam_msg_close_rest_day":         2,
        "natalie_msg_familiar_label":     3,
        "natalie_msg_close_quiet":        2,
        "marcus_msg_very_close_bad_day":  2,
        "nora_msg_very_close_thought":    2,
        "zoe_msg_very_close_reminder":    2,
        "eli_msg_very_close_bad_day":     2,
        "martha_msg_very_close_left_early": 2,
        "lena_msg_very_close_quiet":      2,
        "sam_msg_very_close_rest":        2,
        "natalie_msg_very_close_daylight":2,
        # Phase 49: home-visit invitation variants — weight 1 (lower than all other invitations)
        "nora_msg_home_coffee": 1,
        "eli_msg_home_dinner":  1,
        "zoe_msg_home_guitar":  1,
        # Phase 50: Zoe exhibition — story event, moderate weight; guitar bonus applied in _avail_initiative_variants
        "zoe_msg_exhibition_invite": 2,
    }

    # ── Phase 36: relationship tier ──────────────────────────────────────────
    _TEXT_TIER_ACQUAINTANCE = 0
    _TEXT_TIER_FAMILIAR     = 1
    _TEXT_TIER_CLOSE        = 2
    _TEXT_TIER_VERY_CLOSE   = 3

    def _texting_tier(npc_id):
        """Read-only: returns texting relationship tier, or None if NPC not yet a contact."""
        if npc_id not in store.npc_contacts:
            return None
        aff   = npc_aff(npc_id)
        trust = npc_trust(npc_id)
        if trust >= 65 and aff >= 55:
            return _TEXT_TIER_VERY_CLOSE
        if trust >= 45 and aff >= 35:
            return _TEXT_TIER_CLOSE
        if trust >= 20 or aff >= 20:
            return _TEXT_TIER_FAMILIAR
        return _TEXT_TIER_ACQUAINTANCE

    # Keyed by integer tier constant for safe dict lookup.
    _TIER_GLOBAL_PROB    = {0: 0.25, 1: 0.35, 2: 0.45, 3: 0.55}
    _TIER_WEIGHT_MULT    = {0: 0.75, 1: 1.0,  2: 1.5,  3: 2.0}
    _TIER_COOLDOWN_DELTA = {0: 1,    1: 0,    2: -1,   3: -1}
    _MIN_EFFECTIVE_COOLDOWN = 2
    # Invitation variants require FAMILIAR (1) minimum; date and close-tier variants require CLOSE (2).
    _VARIANT_MIN_TIER = {
        "marcus_msg_park":            1,
        "nora_msg_try_drink":         1,
        "zoe_msg_park_opinion":       1,
        "eli_msg_library_table":      1,
        "nora_msg_date_static":       2,
        "zoe_msg_date_beach":         2,
        "marcus_msg_familiar_food":   1,
        "marcus_msg_close_checkin":   2,
        "nora_msg_familiar_customer": 1,
        "nora_msg_close_distraction": 2,
        "zoe_msg_familiar_sketch":    1,
        "zoe_msg_close_quiet":        2,
        "eli_msg_familiar_debug":     1,
        "eli_msg_close_company":      2,
        "martha_msg_familiar_attachment": 1,
        "martha_msg_close_long_day":      2,
        "lena_msg_familiar_lunch":        1,
        "lena_msg_close_shift":           2,
        "sam_msg_familiar_program":       1,
        "sam_msg_close_rest_day":         2,
        "natalie_msg_familiar_label":     1,
        "natalie_msg_close_quiet":        2,
        "marcus_msg_very_close_bad_day":  3,
        "nora_msg_very_close_thought":    3,
        "zoe_msg_very_close_reminder":    3,
        "eli_msg_very_close_bad_day":     3,
        "martha_msg_very_close_left_early": 3,
        "lena_msg_very_close_quiet":      3,
        "sam_msg_very_close_rest":        3,
        "natalie_msg_very_close_daylight":3,
        # Phase 49: home-visit invitation variants — require CLOSE tier (2)
        "nora_msg_home_coffee": 2,
        "eli_msg_home_dinner":  2,
        "zoe_msg_home_guitar":  2,
        # Phase 50: Zoe exhibition — require CLOSE tier (2)
        "zoe_msg_exhibition_invite": 2,
    }

    # Phase 49: per-variant extra eligibility conditions.
    _VARIANT_CONDITIONS = {
        "nora_msg_home_coffee": lambda: (not store.nora_home_coffee_done
                                         and store.apartment_tier >= 1
                                         and store.own_coffee_machine),
        "eli_msg_home_dinner":  lambda: (not store.eli_home_dinner_done
                                         and store.apartment_tier >= 1),
        "zoe_msg_home_guitar":  lambda: (not store.zoe_home_guitar_done
                                         and store.apartment_tier >= 1
                                         and store.own_guitar),
        # Phase 50: Zoe exhibition — requires arc flag, trust threshold, day gate and decline cooldown
        "zoe_msg_exhibition_invite": lambda: (
            store.zoe_exhibition_invited
            and not store.zoe_exhibition_done
            and store.day >= 21
            and store.zoe_trust >= 25
            and store.day - store.zoe_exhibition_offer_last_day >= 10
        ),
    }
    # Home-invite variants — decline starts a 14-day reoffer cooldown stored in npc_date_invite_last_day.
    _HOME_INVITE_VARIANTS  = {"nora_msg_home_coffee", "eli_msg_home_dinner", "zoe_msg_home_guitar"}
    _HOME_INVITE_COOLDOWNS = {"nora": 14, "eli": 14, "zoe": 14}

    def _home_invite_offer_eligible(npc_id):
        cooldown = _HOME_INVITE_COOLDOWNS.get(npc_id, 14)
        return store.day - store.npc_date_invite_last_day.get("home:" + npc_id, -999) >= cooldown

    def _effective_cooldown(npc_id):
        base  = _INITIATIVE_COOLDOWNS[npc_id]
        tier  = _texting_tier(npc_id)
        delta = _TIER_COOLDOWN_DELTA.get(tier, 0) if tier is not None else 0
        return max(base + delta, _MIN_EFFECTIVE_COOLDOWN)

    def _date_route_eligible(npc_id):
        """Route/romance gates only — no offer cooldown. Used for acceptance, WED conditions, scene guards."""
        if store.romance_permanent_closed.get(npc_id, False):
            return False
        if not romance_is_open(npc_id):
            return False
        return True

    def _date_offer_eligible(npc_id):
        """Route eligibility plus per-NPC date-offer cooldown. Used only when filtering outgoing variants."""
        if not _date_route_eligible(npc_id):
            return False
        if store.day - store.npc_date_invite_last_day.get(npc_id, -999) < _DATE_INVITE_COOLDOWNS.get(npc_id, 99):
            return False
        return True

    def _pick_weighted_initiative_variant(npc_id, avail):
        """Weighted selection: atmospheric=4 (default), invitation=2, date=1."""
        if not avail:
            return None
        weights = [_VARIANT_WEIGHTS.get(v, 4) for v in avail]
        total = float(sum(weights))
        pick = renpy.random.random() * total
        for v, w in zip(avail, weights):
            pick -= w
            if pick <= 0:
                return v
        return avail[-1]

    def _avail_initiative_variants(npc_id):
        """Non-queued variants; invitation, tier-gated, date- and home-invite-eligibility filters applied."""
        active = (store.npc_invitation_pending is not None
                  or any(v in _INV_VARIANTS for v in store.npc_initiative_pending.values()))
        tier = _texting_tier(npc_id)
        if tier is None:
            return []
        result = [v for v in _INITIATIVE_VARIANTS[npc_id]
                  if not message_already_queued(v)
                  and (not active or v not in _INV_VARIANTS)
                  and _VARIANT_MIN_TIER.get(v, 0) <= tier
                  and (v not in _DATE_VARIANTS or _date_offer_eligible(npc_id))
                  and (v not in _HOME_INVITE_VARIANTS or _home_invite_offer_eligible(npc_id))
                  and _VARIANT_CONDITIONS.get(v, lambda: True)()]
        # Phase 50: guitar-done bonus — exhibition invite counts twice in the picker
        if (npc_id == "zoe"
                and "zoe_msg_exhibition_invite" in result
                and store.zoe_home_guitar_done):
            result = result + ["zoe_msg_exhibition_invite"]
        return result

    def _clear_initiative_pending(npc_id):
        d = dict(store.npc_initiative_pending)
        d.pop(npc_id, None)
        store.npc_initiative_pending = d

    # ── Universal NPC photo message framework ────────────────────────────────────
    # _NPC_PHOTO_MESSAGES is the generic authored-content registry, keyed by npc_id.
    # Populated by register_npc_photo_message() calls in director-owned content files
    # (game/director_phone/photo_messages_<npc_id>.rpy). Never populated here.
    # Each entry: { photo_id: { asset, text, responses, category, photo_gap } }
    _NPC_PHOTO_MESSAGES = {}

    def _npc_photo_base(photo_id, path, npc_id, photo_gap=4):
        """Shared base eligibility for all NPC photo initiative variants.

        Checks:
          1. asset exists on disk (variant ineligible until director creates file)
          2. once-ever: photo has not been queued this save
          3. per-NPC cooldown: at least photo_gap days since last photo from this NPC

        Per-variant conditions (relationship stage, romance state, callbacks)
        are authored in each photo entry's lambda, calling this as the base.
        photo_gap defaults to 4; register_npc_photo_message passes the per-entry value.
        """
        return (renpy.loadable(path)
                and photo_id not in store.npc_photo_messages_sent
                and store.day - store.npc_last_photo_day.get(npc_id, -999) >= photo_gap)

    # Relationship stage sets for photo eligibility conditions.
    # Mirrors npc_relationship_stage() return values.
    _REL_STAGE_ACQUAINTANCE_UP = frozenset({"acquaintance", "friendly", "friend", "close", "trusted"})
    _REL_STAGE_FRIENDLY_UP     = frozenset({"friendly", "friend", "close", "trusted"})

    # Photo intimacy bands — documentation only; authored entries specify exact conditions.
    # band 0: observation  — Familiar >= 15  (friendship-only NPCs eligible)
    # band 1: shared life  — Familiar >= 30, Affection >= 25
    # band 2: personal     — Familiar >= 35, Affection >= 35, Chemistry >= 20; romance-capable only
    # band 3: dating       — Familiar >= 45, Affection >= 45, Chemistry >= 35; dating/committed
    # band 4: established  — Familiar >= 60, Affection >= 55, Chemistry >= 45; committed

    # Attachment registry — populated by per-NPC photo files (e.g. zoe_phone_photos.rpy)
    # via init 5 python. Empty here; old callers unaffected if a variant has no entry.
    _VARIANT_ATTACHMENTS = {}

    def _queue_initiative_message(npc_id, variant):
        msg  = _INITIATIVE_MSGS[variant]
        att  = _VARIANT_ATTACHMENTS.get(variant)
        queue_phone_message(npc_id, msg["text"], store.day, variant,
                            responses=msg["responses"], attachment=att)
        # Track photo cooldown at queue time so back-to-back eligibility
        # checks can't pick two different photos on adjacent days.
        if att:
            _d = dict(store.npc_last_photo_day)
            _d[npc_id] = store.day
            store.npc_last_photo_day = _d

    def _check_npc_initiative():
        if store.npc_initiative_last_global_day >= store.day:
            return
        eligible = []
        for npc_id in _INITIATIVE_NPCS:
            if _texting_tier(npc_id) is None:
                continue
            if store.npc_initiative_pending.get(npc_id):
                continue
            if store.day - store.npc_initiative_last_day.get(npc_id, -999) < _effective_cooldown(npc_id):
                continue
            if not _avail_initiative_variants(npc_id):
                continue
            eligible.append(npc_id)
        if not eligible:
            return
        best_tier = max(_texting_tier(n) for n in eligible)
        prob = _TIER_GLOBAL_PROB.get(best_tier, 0.25)
        _r = renpy.random
        if _r.random() >= prob:
            return
        # combined initiative × relationship weight; soft 0.5 penalty for repeat sender
        weights = []
        _last_sender = store.npc_initiative_last_sender
        _multi_eligible = len(eligible) > 1
        for n in eligible:
            base_w = _INITIATIVE_WEIGHT.get(npc_social_trait(n, "initiative", "medium"), 2)
            mult   = _TIER_WEIGHT_MULT.get(_texting_tier(n), 1.0)
            w = base_w * mult
            if _multi_eligible and n == _last_sender:
                w *= 0.5
            weights.append(w)
        total = float(sum(weights))
        pick = _r.random() * total
        npc_id = eligible[-1]
        for i, w in enumerate(weights):
            pick -= w
            if pick <= 0:
                npc_id = eligible[i]
                break
        avail = _avail_initiative_variants(npc_id)
        if not avail:
            return
        variant = _pick_weighted_initiative_variant(npc_id, avail)
        if variant is None:
            return
        _queue_initiative_message(npc_id, variant)
        deliver_message_now(variant)
        _ld = dict(store.npc_initiative_last_day)
        _ld[npc_id] = store.day
        store.npc_initiative_last_day = _ld
        _pd = dict(store.npc_initiative_pending)
        _pd[npc_id] = variant
        store.npc_initiative_pending = _pd
        store.npc_initiative_last_global_day = store.day
        store.npc_initiative_last_sender = npc_id
        if variant in _DATE_VARIANTS:
            _dd = dict(store.npc_date_invite_last_day)
            _dd[npc_id] = store.day
            store.npc_date_invite_last_day = _dd


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
    show martha_neutral as focus_martha at sprite_r
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
    hide focus_martha
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
    $ gain_skill("prog", 40)
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
    show drlena_normal as focus_lena at sprite_r
    "The third-year presents the case. Complex, bilateral involvement, non-obvious history."
    "Lena listens without interrupting for two minutes. Then she asks one question. Everything shifts."
    lena "Write down what changed after the question. Not the answer — what the question did."
    hide focus_lena
    "You fill half a page in your notes."
    $ _apply_trust("lena", 3)
    $ gain_skill("med", 50)
    $ add_relationship_memory("lena", "lena_case_observation", "Ward B case observation")
    $ lena_case_observation_done = True
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
    show nora_cafe_normal as focus_nora at sprite_r
    "Closing the café is quieter than a shift. Chairs up. Counters wiped. Henry went home at nine."
    n "Okay, I have a theory about the foam. Are you ready for this theory?"
    "You tell her you are."
    n "It's not the milk. It's the temperature. Everyone blames the milk."
    "She makes you a perfect flat white at 10pm to prove her point."
    $ _apply_aff("nora", 4)
    $ _apply_trust("nora", 2)
    hide focus_nora
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
    python:
        # Create a special Eli freelance project (2h, no pay — reward via process_freelance_payments is_eli)
        store.freelance_active_project = {
            "template_id": "eli_side_remote",
            "title": "Eli's feature branch",
            "client": "Eli",
            "required_skill": 2,
            "accepted_day": store.day,
            "deadline_day": store.day + 5,
            "required_hours": 2,
            "worked_hours": 0,
            "pay": 0,
            "exp": 8,
            "status": "active",
            "is_eli": True,
        }
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


# ── Phase 30: NPC initiative reply labels ────────────────────────────────────

label npc_ini_marcus_checkin_mostly:
    $ queue_phone_message("marcus", "Good enough. City standard.", day, "marcus_msg_checkin_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_checkin_busy:
    $ queue_phone_message("marcus", "That usually means yes.", day, "marcus_msg_checkin_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_checkin_why:
    $ queue_phone_message("marcus", "Neighbourhood quality control.", day, "marcus_msg_checkin_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_food_again:
    $ queue_phone_message("marcus", "Consistency matters.", day, "marcus_msg_food_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_food_invite:
    $ queue_phone_message("marcus", "It was becoming one.", day, "marcus_msg_food_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_food_save:
    $ queue_phone_message("marcus", "Optimistic, but noted.", day, "marcus_msg_food_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_nora_shift_answer:
    $ queue_phone_message("nora", "Professionally.", day, "nora_msg_shift_r1")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_shift_six:
    $ queue_phone_message("nora", "I stopped counting at six.", day, "nora_msg_shift_r2")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_shift_normal:
    $ queue_phone_message("nora", "That is the concerning part.", day, "nora_msg_shift_r3")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_rec_why:
    $ queue_phone_message("nora", "I have standards.", day, "nora_msg_rec_r1")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_rec_warn:
    $ queue_phone_message("nora", "A public service.", day, "nora_msg_rec_r2")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_rec_going:
    $ queue_phone_message("nora", "You are welcome.", day, "nora_msg_rec_r3")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_zoe_photo_wrong:
    $ queue_phone_message("zoe", "The building.", day, "zoe_msg_photo_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_photo_proof:
    $ queue_phone_message("zoe", "The photo makes it look reasonable.", day, "zoe_msg_photo_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_photo_build:
    $ queue_phone_message("zoe", "That is less fixable.", day, "zoe_msg_photo_r3")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_question_three:
    $ queue_phone_message("zoe", "Too easy.", day, "zoe_msg_question_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_question_five:
    $ queue_phone_message("zoe", "Arbitrary. Better.", day, "zoe_msg_question_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_question_birds:
    $ queue_phone_message("zoe", "Correct and unhelpful.", day, "zoe_msg_question_r3")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_eli_bug_which:
    $ queue_phone_message("eli", "That is the problem.", day, "eli_msg_bug_r1")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_bug_congrats:
    $ queue_phone_message("eli", "The tests disagree.", day, "eli_msg_bug_r2")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_bug_home:
    $ queue_phone_message("eli", "Eventually.", day, "eli_msg_bug_r3")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_library_report:
    $ queue_phone_message("eli", "It printed the report incorrectly.", day, "eli_msg_library_r1")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_library_walk:
    $ queue_phone_message("eli", "I respect the strategy.", day, "eli_msg_library_r2")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_library_off:
    $ queue_phone_message("eli", "It knows I know that.", day, "eli_msg_library_r3")
    $ _clear_initiative_pending("eli")
    return


# ── Phase 31: Marcus park invitation replies ─────────────────────────────────

label npc_ini_marcus_park_yeah:
    if store.npc_invitation_pending is None:
        $ store.npc_invitation_pending = {"npc_id": "marcus", "invitation_id": "marcus_park_invite", "target_location": "location_park", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("marcus", "Good. I'll try not to make it look organised.", day, "marcus_msg_park_r1")
    else:
        $ queue_phone_message("marcus", "Let me know when you're free.", day, "marcus_msg_park_r1b")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_park_maybe:
    $ queue_phone_message("marcus", "Strong commitment. I respect it.", day, "marcus_msg_park_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_park_no:
    $ queue_phone_message("marcus", "Fair. More park for me.", day, "marcus_msg_park_r3")
    $ _clear_initiative_pending("marcus")
    return


# ── Phase 31: Nora drink invitation replies ───────────────────────────────────

label npc_ini_nora_drink_risky:
    if store.npc_invitation_pending is None:
        $ store.npc_invitation_pending = {"npc_id": "nora", "invitation_id": "nora_grounds_invite", "target_location": "location_cafe", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("nora", "For you, mostly.", day, "nora_msg_drink_r1")
    else:
        $ queue_phone_message("nora", "Another time then.", day, "nora_msg_drink_r1b")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_drink_what:
    $ queue_phone_message("nora", "If I explain it first, the opinion becomes biased.", day, "nora_msg_drink_r2")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_drink_other:
    $ queue_phone_message("nora", "I did. They were wrong.", day, "nora_msg_drink_r3")
    $ _clear_initiative_pending("nora")
    return


# ── Phase 33: Zoe park invitation replies ─────────────────────────────────────

label npc_ini_zoe_park_stopby:
    if store.npc_invitation_pending is None:
        $ store.npc_invitation_pending = {"npc_id": "zoe", "invitation_id": "zoe_park_invite", "target_location": "location_park", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("zoe", "Bring opinions. Not solutions.", day, "zoe_msg_park_r1")
    else:
        $ queue_phone_message("zoe", "Some other time.", day, "zoe_msg_park_r1b")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_park_what:
    $ queue_phone_message("zoe", "If I explain it first, you'll arrive biased.", day, "zoe_msg_park_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_park_no:
    $ queue_phone_message("zoe", "Fine. I'll distrust my own judgement.", day, "zoe_msg_park_r3")
    $ _clear_initiative_pending("zoe")
    return


# ── Phase 33: Eli library invitation replies ──────────────────────────────────

label npc_ini_eli_table_save:
    if store.npc_invitation_pending is None:
        $ store.npc_invitation_pending = {"npc_id": "eli", "invitation_id": "eli_library_invite", "target_location": "location_library", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("eli", "I'm guarding it with a cable.", day, "eli_msg_table_r1")
    else:
        $ queue_phone_message("eli", "Understood. Next time.", day, "eli_msg_table_r1b")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_table_both:
    $ queue_phone_message("eli", "I tested them before making the claim.", day, "eli_msg_table_r2")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_table_busy:
    $ queue_phone_message("eli", "Reasonable. The table is statistically temporary.", day, "eli_msg_table_r3")
    $ _clear_initiative_pending("eli")
    return


# ── Phase 37: Nora Static date invitation replies ─────────────────────────────

label npc_ini_nora_date_asking:
    if store.npc_invitation_pending is None and _date_route_eligible("nora"):
        $ store.npc_invitation_pending = {"npc_id": "nora", "invitation_id": "nora_static_date", "target_location": "location_bar", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("nora", "Does there need to be one?", day, "nora_msg_date_r1")
    else:
        $ queue_phone_message("nora", "Another time then.", day, "nora_msg_date_r1b")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_date_where:
    $ queue_phone_message("nora", "Static. Mercer Street.", day, "nora_msg_date_r2")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_date_not:
    $ queue_phone_message("nora", "Some other time.", day, "nora_msg_date_r3")
    $ _clear_initiative_pending("nora")
    return


# ── Phase 37: Zoe beach date invitation replies ───────────────────────────────

label npc_ini_zoe_beach_date:
    if store.npc_invitation_pending is None and _date_route_eligible("zoe"):
        $ store.npc_invitation_pending = {"npc_id": "zoe", "invitation_id": "zoe_beach_date", "target_location": "location_sandbeach", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("zoe", "Confirmed.", day, "zoe_msg_beach_r1")
    else:
        $ queue_phone_message("zoe", "Some other time.", day, "zoe_msg_beach_r1b")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_beach_come:
    if store.npc_invitation_pending is None and _date_route_eligible("zoe"):
        $ store.npc_invitation_pending = {"npc_id": "zoe", "invitation_id": "zoe_beach_date", "target_location": "location_sandbeach", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("zoe", "Good.", day, "zoe_msg_beach_r2")
    else:
        $ queue_phone_message("zoe", "Some other time.", day, "zoe_msg_beach_r2b")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_beach_not:
    $ queue_phone_message("zoe", "Fine. More sand for me.", day, "zoe_msg_beach_r3")
    $ _clear_initiative_pending("zoe")
    return


# ── Phase 38: Martha replies ──────────────────────────────────────────────────

label npc_ini_martha_revision_final:
    $ queue_phone_message("martha", "It was not even version seven.", day, "martha_msg_revision_r1")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_revision_official:
    $ queue_phone_message("martha", "That is how they get you.", day, "martha_msg_revision_r2")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_revision_delete:
    $ queue_phone_message("martha", "Tempting. Traceable, but tempting.", day, "martha_msg_revision_r3")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_calendar_accept:
    $ queue_phone_message("martha", "I need to see how this ends.", day, "martha_msg_calendar_r1")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_calendar_decline:
    $ queue_phone_message("martha", "Then they would schedule a follow-up.", day, "martha_msg_calendar_r2")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_calendar_work:
    $ queue_phone_message("martha", "Your optimism lacks corporate experience.", day, "martha_msg_calendar_r3")
    $ _clear_initiative_pending("martha")
    return


# ── Phase 38: Lena replies ────────────────────────────────────────────────────

label npc_ini_lena_coffee_legal:
    $ queue_phone_message("lena", "It remains legally recognisable.", day, "lena_msg_coffee_r1")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_coffee_water:
    $ queue_phone_message("lena", "An unexpectedly responsible suggestion.", day, "lena_msg_coffee_r2")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_coffee_fourth:
    $ queue_phone_message("lena", "That would make it a treatment plan.", day, "lena_msg_coffee_r3")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_waiting_stopped:
    $ queue_phone_message("lena", "I will update the differential.", day, "lena_msg_waiting_r1")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_waiting_off:
    $ queue_phone_message("lena", "Then everyone starts watching me.", day, "lena_msg_waiting_r2")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_waiting_accurate:
    $ queue_phone_message("lena", "It is reporting yesterday.", day, "lena_msg_waiting_r3")
    $ _clear_initiative_pending("lena")
    return


# ── Phase 38: Sam replies ─────────────────────────────────────────────────────

label npc_ini_sam_soreness_no:
    $ queue_phone_message("sam", "Unnecessarily direct.", day, "sam_msg_soreness_r1")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_soreness_down:
    $ queue_phone_message("sam", "Finally, science.", day, "sam_msg_soreness_r2")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_soreness_slowly:
    $ queue_phone_message("sam", "Very slowly. Professionally slowly.", day, "sam_msg_soreness_r3")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_music_good:
    $ queue_phone_message("sam", "For emotional endurance.", day, "sam_msg_music_r1")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_music_change:
    $ queue_phone_message("sam", "I want to see who breaks first.", day, "sam_msg_music_r2")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_music_sing:
    $ queue_phone_message("sam", "That would clear the floor.", day, "sam_msg_music_r3")
    $ _clear_initiative_pending("sam")
    return


# ── Phase 38: Natalie replies ─────────────────────────────────────────────────

label npc_ini_natalie_delivery_efficient:
    $ queue_phone_message("natalie", "In three incompatible directions.", day, "natalie_msg_delivery_r1")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_delivery_back:
    $ queue_phone_message("natalie", "I am considering sending the driver with it.", day, "natalie_msg_delivery_r2")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_delivery_worse:
    $ queue_phone_message("natalie", "Never say that near a warehouse.", day, "natalie_msg_delivery_r3")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_clipboard_found:
    $ queue_phone_message("natalie", "Exactly where I left it. That is not the point.", day, "natalie_msg_clipboard_r1")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_clipboard_another:
    $ queue_phone_message("natalie", "Then there would be two unsecured clipboards.", day, "natalie_msg_clipboard_r2")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_clipboard_ask:
    $ queue_phone_message("natalie", "They are already afraid. No need to escalate.", day, "natalie_msg_clipboard_r3")
    $ _clear_initiative_pending("natalie")
    return


# ── Phase 39: Marcus tier replies ─────────────────────────────────────────────

label npc_ini_marcus_familiar_food_yes:
    $ queue_phone_message("marcus", "Suspiciously fast answer.", day, "marcus_msg_familiar_food_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_familiar_food_notyet:
    $ queue_phone_message("marcus", "That was not permission.", day, "marcus_msg_familiar_food_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_familiar_food_vending:
    $ queue_phone_message("marcus", "They provide consequences.", day, "marcus_msg_familiar_food_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_close_checkin_fine:
    $ queue_phone_message("marcus", "That answer has never convinced anyone.", day, "marcus_msg_close_checkin_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_close_checkin_tired:
    $ queue_phone_message("marcus", "Acceptable. Get actual sleep.", day, "marcus_msg_close_checkin_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_close_checkin_notreally:
    $ queue_phone_message("marcus", "All right. I'm around.", day, "marcus_msg_close_checkin_r3")
    $ _clear_initiative_pending("marcus")
    return


# ── Phase 39: Nora tier replies ───────────────────────────────────────────────

label npc_ini_nora_familiar_customer_wanted:
    $ queue_phone_message("nora", "Their usual order with emotional theatre.", day, "nora_msg_familiar_customer_r1")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_familiar_customer_again:
    $ queue_phone_message("nora", "Escalation is rarely customer service.", day, "nora_msg_familiar_customer_r2")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_familiar_customer_refuse:
    $ queue_phone_message("nora", "You are ready for management.", day, "nora_msg_familiar_customer_r3")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_close_distraction_dog:
    $ queue_phone_message("nora", "Excellent. Immediate improvement.", day, "nora_msg_close_distraction_r1")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_close_distraction_city:
    $ queue_phone_message("nora", "Nearly is doing useful work there.", day, "nora_msg_close_distraction_r2")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_close_distraction_coffee:
    $ queue_phone_message("nora", "Then we are both trapped.", day, "nora_msg_close_distraction_r3")
    $ _clear_initiative_pending("nora")
    return


# ── Phase 39: Zoe tier replies ────────────────────────────────────────────────

label npc_ini_zoe_familiar_sketch_wrong:
    $ queue_phone_message("zoe", "That is not what obsolete means.", day, "zoe_msg_familiar_sketch_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_familiar_sketch_show:
    $ queue_phone_message("zoe", "Eventually.", day, "zoe_msg_familiar_sketch_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_familiar_sketch_relevant:
    $ queue_phone_message("zoe", "Briefly, you were.", day, "zoe_msg_familiar_sketch_r3")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_close_quiet_where:
    $ queue_phone_message("zoe", "Telling people would damage it.", day, "zoe_msg_close_quiet_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_close_quiet_keeping:
    $ queue_phone_message("zoe", "For now.", day, "zoe_msg_close_quiet_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_close_quiet_suspect:
    $ queue_phone_message("zoe", "Quiet usually does to loud people.", day, "zoe_msg_close_quiet_r3")
    $ _clear_initiative_pending("zoe")
    return


# ── Phase 39: Eli tier replies ────────────────────────────────────────────────

label npc_ini_eli_familiar_debug_fixed:
    $ queue_phone_message("eli", "I connected it. Technically yes.", day, "eli_msg_familiar_debug_r1")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_familiar_debug_noone:
    $ queue_phone_message("eli", "The logs know.", day, "eli_msg_familiar_debug_r2")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_familiar_debug_twenty:
    $ queue_phone_message("eli", "That is not supportive.", day, "eli_msg_familiar_debug_r3")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_close_company_company:
    $ queue_phone_message("eli", "Not tonight. But thank you.", day, "eli_msg_close_company_r1")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_close_company_home:
    $ queue_phone_message("eli", "That remains the theoretical plan.", day, "eli_msg_close_company_r2")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_close_company_silence:
    $ queue_phone_message("eli", "I am trying to.", day, "eli_msg_close_company_r3")
    $ _clear_initiative_pending("eli")
    return

# ── Phase 40: Wave 2 tier-specific reply labels ───────────────────────────────

label npc_ini_martha_familiar_attachment_used:
    $ queue_phone_message("martha", "I opened it in a controlled environment.", day, "martha_msg_familiar_attachment_r1")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_familiar_attachment_reassure:
    $ queue_phone_message("martha", "The filename was not.", day, "martha_msg_familiar_attachment_r2")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_familiar_attachment_back:
    $ queue_phone_message("martha", "With or without a risk assessment?", day, "martha_msg_familiar_attachment_r3")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_close_long_day_productive:
    $ queue_phone_message("martha", "Statistically, perhaps.", day, "martha_msg_close_long_day_r1")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_close_long_day_tired:
    $ queue_phone_message("martha", "I sound professionally composed.", day, "martha_msg_close_long_day_r2")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_close_long_day_yours:
    $ queue_phone_message("martha", "Naturally. That is why it took four meetings.", day, "martha_msg_close_long_day_r3")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_lena_familiar_lunch_halfway:
    $ queue_phone_message("lena", "I was hoping for partial credit.", day, "lena_msg_familiar_lunch_r1")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_familiar_lunch_eat:
    $ queue_phone_message("lena", "A remarkably direct treatment plan.", day, "lena_msg_familiar_lunch_r2")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_familiar_lunch_what:
    $ queue_phone_message("lena", "At this point, an archaeological question.", day, "lena_msg_familiar_lunch_r3")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_close_shift_you:
    $ queue_phone_message("lena", "Operational.", day, "lena_msg_close_shift_r1")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_close_shift_notquestion:
    $ queue_phone_message("lena", "I noticed.", day, "lena_msg_close_shift_r2")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_close_shift_rest:
    $ queue_phone_message("lena", "Eventually. I am accepting that as an instruction.", day, "lena_msg_close_shift_r3")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_sam_familiar_program_strong:
    $ queue_phone_message("sam", "I believe in flexible methodology.", day, "sam_msg_familiar_program_r1")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_familiar_program_why:
    $ queue_phone_message("sam", "For the sense of structure.", day, "sam_msg_familiar_program_r2")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_familiar_program_tomorrow:
    $ queue_phone_message("sam", "Tomorrow Sam is very reliable.", day, "sam_msg_familiar_program_r3")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_close_rest_needed:
    $ queue_phone_message("sam", "That sounds suspiciously informed.", day, "sam_msg_close_rest_r1")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_close_rest_anyway:
    $ queue_phone_message("sam", "Thank you for enabling me.", day, "sam_msg_close_rest_r2")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_close_rest_nothing:
    $ queue_phone_message("sam", "I do not have the technique.", day, "sam_msg_close_rest_r3")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_natalie_familiar_label_what:
    $ queue_phone_message("natalie", "Several reasons not to write miscellaneous.", day, "natalie_msg_familiar_label_r1")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_familiar_label_accurate:
    $ queue_phone_message("natalie", "Accuracy without usefulness is decoration.", day, "natalie_msg_familiar_label_r2")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_familiar_label_relabel:
    $ queue_phone_message("natalie", "I have begun the investigation.", day, "natalie_msg_familiar_label_r3")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_close_quiet_enjoy:
    $ queue_phone_message("natalie", "I am monitoring it.", day, "natalie_msg_close_quiet_r1")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_close_quiet_ominous:
    $ queue_phone_message("natalie", "Quiet usually means someone forgot something.", day, "natalie_msg_close_quiet_r2")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_close_quiet_home:
    $ queue_phone_message("natalie", "A compelling but operationally weak proposal.", day, "natalie_msg_close_quiet_r3")
    $ _clear_initiative_pending("natalie")
    return

# ── Phase 41: VERY_CLOSE reply labels ────────────────────────────────────────

label npc_ini_marcus_very_close_bad_day_itwas:
    $ queue_phone_message("marcus", "All right. No fixing. I'm here.", day, "marcus_msg_very_close_bad_day_r1")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_very_close_bad_day_notreally:
    $ queue_phone_message("marcus", "Good. Still counts as checking.", day, "marcus_msg_very_close_bad_day_r2")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_marcus_very_close_bad_day_maybe:
    $ queue_phone_message("marcus", "That is usually how the bad ones introduce themselves.", day, "marcus_msg_very_close_bad_day_r3")
    $ _clear_initiative_pending("marcus")
    return

label npc_ini_nora_very_close_thought_fourth:
    $ queue_phone_message("nora", "Technically the first successful one.", day, "nora_msg_very_close_thought_r1")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_very_close_thought_couldve:
    $ queue_phone_message("nora", "Dangerous precedent.", day, "nora_msg_very_close_thought_r2")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_very_close_thought_happened:
    $ queue_phone_message("nora", "Nothing dramatic. I just wanted to talk to you.", day, "nora_msg_very_close_thought_r3")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_zoe_very_close_reminder_whatwas:
    $ queue_phone_message("zoe", "A terrible sign with confident typography.", day, "zoe_msg_very_close_reminder_r1")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_very_close_reminder_why:
    $ queue_phone_message("zoe", "Because patterns become habits.", day, "zoe_msg_very_close_reminder_r2")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_very_close_reminder_honoured:
    $ queue_phone_message("zoe", "Do not become difficult about it.", day, "zoe_msg_very_close_reminder_r3")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_eli_very_close_bad_day_stillcan:
    $ queue_phone_message("eli", "I might edit it down to a manageable disaster.", day, "eli_msg_very_close_bad_day_r1")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_very_close_bad_day_howbad:
    $ queue_phone_message("eli", "Mostly ordinary. Repeatedly.", day, "eli_msg_very_close_bad_day_r2")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_very_close_bad_day_okay:
    $ queue_phone_message("eli", "I will be. That answer is more accurate than 'fine.'", day, "eli_msg_very_close_bad_day_r3")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_martha_very_close_left_early_proud:
    $ queue_phone_message("martha", "Keep that off the record.", day, "martha_msg_very_close_left_early_r1")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_very_close_left_early_wrong:
    $ queue_phone_message("martha", "Nothing. That is what makes it suspicious.", day, "martha_msg_very_close_left_early_r2")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_martha_very_close_left_early_again:
    $ queue_phone_message("martha", "Let us not turn progress into policy.", day, "martha_msg_very_close_left_early_r3")
    $ _clear_initiative_pending("martha")
    return

label npc_ini_lena_very_close_quiet_sitdown:
    $ queue_phone_message("lena", "An advanced technique.", day, "lena_msg_very_close_quiet_r1")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_very_close_quiet_callme:
    $ queue_phone_message("lena", "That would have used at least eight.", day, "lena_msg_very_close_quiet_r2")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_lena_very_close_quiet_silence:
    $ queue_phone_message("lena", "I tried. It was louder than expected.", day, "lena_msg_very_close_quiet_r3")
    $ _clear_initiative_pending("lena")
    return

label npc_ini_sam_very_close_rest_recognised:
    $ queue_phone_message("sam", "Thank you. I will frame this.", day, "sam_msg_very_close_rest_r1")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_very_close_rest_exhausted:
    $ queue_phone_message("sam", "Do not sound so surprised.", day, "sam_msg_very_close_rest_r2")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_sam_very_close_rest_again:
    $ queue_phone_message("sam", "Let's not overcorrect.", day, "sam_msg_very_close_rest_r3")
    $ _clear_initiative_pending("sam")
    return

label npc_ini_natalie_very_close_daylight_andyou:
    $ queue_phone_message("natalie", "Poorly, but off-site.", day, "natalie_msg_very_close_daylight_r1")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_very_close_daylight_enjoy:
    $ queue_phone_message("natalie", "I am attempting to.", day, "natalie_msg_very_close_daylight_r2")
    $ _clear_initiative_pending("natalie")
    return

label npc_ini_natalie_very_close_daylight_survive:
    $ queue_phone_message("natalie", "That remains an operational hypothesis.", day, "natalie_msg_very_close_daylight_r3")
    $ _clear_initiative_pending("natalie")
    return


# ── Phase 49: home-visit invitation replies ───────────────────────────────────

label npc_ini_nora_home_coffee_accept:
    if store.npc_invitation_pending is None:
        $ store.npc_invitation_pending = {"npc_id": "nora", "invitation_id": "nora_home_coffee", "target_location": "location_home", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("nora", "Good. Don't touch the settings before I arrive.", day, "nora_home_coffee_r1")
    else:
        $ queue_phone_message("nora", "When your schedule clears.", day, "nora_home_coffee_r1b")
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_home_coffee_decline:
    $ queue_phone_message("nora", "The machine is lying to you.", day, "nora_home_coffee_r2")
    python:
        _dd = dict(store.npc_date_invite_last_day)
        _dd["home:nora"] = store.day
        store.npc_date_invite_last_day = _dd
    $ _clear_initiative_pending("nora")
    return

label npc_ini_nora_home_coffee_playful:
    $ queue_phone_message("nora", "It isn't.", day, "nora_home_coffee_r3")
    python:
        _dd = dict(store.npc_date_invite_last_day)
        _dd["home:nora"] = store.day
        store.npc_date_invite_last_day = _dd
    $ _clear_initiative_pending("nora")
    return


label npc_ini_eli_home_dinner_accept:
    if store.npc_invitation_pending is None:
        $ store.npc_invitation_pending = {"npc_id": "eli", "invitation_id": "eli_home_dinner", "target_location": "location_home", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("eli", "Fine. I will bring nothing.", day, "eli_home_dinner_r1")
    else:
        $ queue_phone_message("eli", "When the plan is clear.", day, "eli_home_dinner_r1b")
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_home_dinner_decline:
    $ queue_phone_message("eli", "The record exists. I will wait.", day, "eli_home_dinner_r2")
    python:
        _dd = dict(store.npc_date_invite_last_day)
        _dd["home:eli"] = store.day
        store.npc_date_invite_last_day = _dd
    $ _clear_initiative_pending("eli")
    return

label npc_ini_eli_home_dinner_playful:
    $ queue_phone_message("eli", "I have retained the record.", day, "eli_home_dinner_r3")
    python:
        _dd = dict(store.npc_date_invite_last_day)
        _dd["home:eli"] = store.day
        store.npc_date_invite_last_day = _dd
    $ _clear_initiative_pending("eli")
    return


label npc_ini_zoe_home_guitar_accept:
    if store.npc_invitation_pending is None:
        $ store.npc_invitation_pending = {"npc_id": "zoe", "invitation_id": "zoe_home_guitar", "target_location": "location_home", "accepted_day": day, "expiry_day": day + 7}
        $ queue_phone_message("zoe", "I'll bring a second opinion.", day, "zoe_home_guitar_r1")
    else:
        $ queue_phone_message("zoe", "Another time.", day, "zoe_home_guitar_r1b")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_home_guitar_decline:
    $ queue_phone_message("zoe", "Confirmed furniture.", day, "zoe_home_guitar_r2")
    python:
        _dd = dict(store.npc_date_invite_last_day)
        _dd["home:zoe"] = store.day
        store.npc_date_invite_last_day = _dd
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_home_guitar_playful:
    $ queue_phone_message("zoe", "Storage.", day, "zoe_home_guitar_r3")
    python:
        _dd = dict(store.npc_date_invite_last_day)
        _dd["home:zoe"] = store.day
        store.npc_date_invite_last_day = _dd
    $ _clear_initiative_pending("zoe")
    return


# ── Phase 50: Zoe exhibition invitation replies ───────────────────────────────

label npc_ini_zoe_exhibition_accept:
    if store.npc_invitation_pending is None:
        $ store.npc_invitation_pending = {"npc_id": "zoe", "invitation_id": "zoe_exhibition", "target_location": "location_gallery", "accepted_day": day, "expiry_day": day + 7}
        $ store.zoe_exhibition_offer_last_day = day
        $ queue_phone_message("zoe", "Opening's Friday. Come before the pretentious bit.", day, "zoe_exhibition_r1")
    else:
        $ queue_phone_message("zoe", "Sort your schedule. I'll tell you when.", day, "zoe_exhibition_r1b")
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_exhibition_decline:
    $ queue_phone_message("zoe", "Fine. Someone will explain it to you eventually.", day, "zoe_exhibition_r2")
    $ store.zoe_exhibition_offer_last_day = day
    $ _clear_initiative_pending("zoe")
    return

label npc_ini_zoe_exhibition_playful:
    $ queue_phone_message("zoe", "It's a gallery. Weird is the baseline.", day, "zoe_exhibition_r3")
    $ store.zoe_exhibition_offer_last_day = day
    $ _clear_initiative_pending("zoe")
    return
