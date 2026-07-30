# warehouse_arc.rpy — Warehouse professional judgment arc (Phase 48)
# NPC: Natalie (nat) — floor manager, direct, safety-focused
# No career progression or review system; aftermath queues from followup label.

label wh_damaged_shipment:
    $ wh_safety_done = True
    scene pov_warehouse
    show screen hud
    "Midway through the afternoon: a pallet from the late delivery sits at the edge of the bay. One corner is raised — unstable load."
    "The route to the dock is partially blocked by maintenance equipment. Operations is already running ninety minutes behind schedule."
    show natalie_normal at sprite_r
    nat "Urgent dispatch on bay four. We're moving it now or it misses the transport window."
    mc "The pallet's not secure. One corner is raised."
    nat "How bad?"
    mc "Bad enough that if it shifts during movement, we lose the shipment. Maybe worse."
    "She looks at it."
    nat "Your call. You're on floor lead today."
    $ _wev_relbar_open("natalie")
    show screen npc_relbar("natalie")
    menu:
        "Stop the movement and secure the area.":
            $ wh_safety_choice = "stopped"
            $ wh_safety_outcome = "stopped"
            mc "We're not moving it. I want the area flagged and the pallet secured before anyone goes back in that bay."
            "Operations flags the shipment as delayed. The transport window closes."
            nat "That's going to be a conversation with the depot manager."
            mc "Send them to me."
            hide natalie_normal
            $ _work_perf(6)
            $ _apply_trust("natalie", 3)
        "Reroute the shipment, document the hazard, isolate the pallet.":
            $ wh_safety_choice = "rerouted"
            $ wh_safety_outcome = "rerouted"
            mc "Reroute via bay six. Log the hazard formally, cordon the pallet, and hold the rest of the movement until it's secured."
            "The route adds forty minutes. The dispatch log gets the hazard note."
            nat "Late, but intact."
            mc "And documented."
            hide natalie_normal
            $ _work_perf(3)
            $ _apply_trust("natalie", 2)
        "Continue carefully to protect the deadline.":
            $ wh_safety_choice = "continued"
            $ wh_safety_outcome = "continued"
            mc "We move it carefully. Keep people clear of the pallet and watch the corner."
            "The movement starts. The raised corner draws eyes but no intervention."
            "The pallet clears the bay. The shipment makes the window."
            hide natalie_normal
            $ _work_perf(-8)
            $ _apply_trust("natalie", -3)
    $ _wev_relbar_close()
    hide screen npc_relbar
    $ wh_safety_followup_pending = True
    $ wh_safety_followup_shift = wh_shifts + 2
    return


label wh_damaged_shipment_followup:
    scene pov_warehouse
    show screen hud
    show natalie_normal at sprite_r
    if wh_safety_outcome == "stopped":
        "Two shifts later: the pallet that was isolated failed during static storage — the load shifted while stationary, bracing gave way."
        nat "It went while it was sitting there."
        mc "If we'd moved it, that would have happened in motion."
        nat "Yeah."
        "A pause."
        nat "The depot manager came by. I told them you made the right call."
        hide natalie_normal
        $ _work_perf(2)
        $ _apply_trust("natalie", 2)
    elif wh_safety_outcome == "rerouted":
        "Two shifts later: the hazard note from the dispatch log triggered a review of the bay's loading procedure. The process gap it exposed had been on the near-miss list for two months."
        nat "The documentation did more than log the delay."
        mc "The gap was already there."
        nat "Someone needed to write it down. You did."
        hide natalie_normal
        $ _work_perf(1)
        $ _apply_trust("natalie", 1)
    else:
        "Two shifts later: the incident report. The load shifted during handling at the depot. Damage to the shipment, one minor handling injury."
        nat "The pallet that went out on bay four."
        mc "I moved it."
        "She looks at you."
        nat "Why?"
        hide natalie_normal
        $ _wev_relbar_open("natalie")
        show screen npc_relbar("natalie")
        show natalie_normal at sprite_r
        menu:
            "Accept responsibility immediately.":
                $ wh_safety_owned_mistake = True
                mc "I knew it was unstable and I moved it anyway. The schedule pressure affected my call. That's on me."
                nat "Operations will want a written account."
                mc "I'll write it tonight."
                nat "Okay."
                "No absolution. Just the next thing to do."
                hide natalie_normal
                $ _work_perf(1)
                $ _apply_trust("natalie", 2)
                $ wh_safety_review_extra_shifts = 1
            "Blame the schedule and handling conditions.":
                $ wh_safety_owned_mistake = False
                mc "The schedule was already ninety minutes behind. The handling conditions at the depot contributed — the damage happened after it left our floor."
                nat "You flagged the corner before the move."
                mc "I assessed it as manageable."
                nat "You had what you needed to stop it."
                "She writes up the report herself."
                hide natalie_normal
                $ _work_perf(-2)
                $ _apply_trust("natalie", -2)
                $ wh_safety_review_extra_shifts = 2
        $ _wev_relbar_close()
        hide screen npc_relbar
    $ wh_safety_followup_done = True
    $ wh_safety_followup_pending = False
    python:
        _lwh_oc = store.wh_safety_outcome
        if _lwh_oc == "continued":
            _lwh_oc = "continued_owned" if store.wh_safety_owned_mistake else "continued_defended"
        _queue_story_aftermath("natalie", "wh_damaged_shipment", "wh_safety", _lwh_oc,
                               store.day, store.day + 1, "aftermath_wh_damaged_shipment")
    return
