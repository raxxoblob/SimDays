# DIRECTOR TODO

## Zoe — Beach Dating Breakpoint

File to create:
`game/director_romance/romantic_subscene_zoe_beach_dating.rpy`

Label:
`romantic_subscene_zoe_beach_dating`

Scene:
Canonical interested → dating scene. Full beach night buildup is implemented in
the parent scene (`zoe_beach_dating_scene` in `zoe_romance_milestones.rpy`).
Director takes over immediately after:

`z "But apparently that's not stopping me."`

Director implements:
CG sequence, final romantic choices, kiss / no-kiss presentation, canonical
first-kiss helper (`_commit_first_kiss("zoe")`) where applicable, and the
interested → dating state transition if successful. If player declines, director
sets its own retry state.

Relationship result:
`interested -> dating` (if successful)

End with:
`return`

---

## Zoe — Beach After Dark

File to create:
`game/director_romance/zoe_beach_after_dark_romance.rpy`

Label:
`zoe_beach_after_dark_payoff`

Scene:
Post-first-kiss dating breakpoint. Zoe brings MC to the beach at night — a place
that normally feels private to her. The full beach conversation and emotional
buildup are implemented in the parent scene. Director takes over after:

`z "Just — show up."`

Director implements:
CG-driven quiet physical intimacy / kiss / close comfort ending.

Relationship result:
remains `dating`

End with:
`return`

---

## Zoe — Commitment

File to create:
`game/director_romance/zoe_commitment_romance.rpy`

Label:
`zoe_commitment_payoff`

Scene:
Commitment breakpoint at a new neutral shared location — not the beach, not the
first-kiss spot. A place that now belongs to both of them. The full conversation
buildup is implemented in the parent scene. Director takes over after Zoe's final:

`z "Yes."`

Director implements:
physical payoff / kiss / hand-hold / CG ending.

Relationship result:
`dating -> committed`

End with:
`return`

---

## Zoe — Love Spoken

File to create:
`game/director_romance/zoe_love_spoken_romance.rpy`

Label:
`zoe_love_spoken_payoff`

Scene:
Visual climax after Zoe has already said "Love you" and the player's response
branch has finished.

Director takes over at:
`label zoe_love_after:`

Director implements:
CG-driven visual ending only.

Relationship result:
remains `committed`

End with:
`return`

---

## Summer Festival — Zoe Romance

File to create:
`game/director_romance/summer_festival_romance.rpy`

Label:
`summer_festival_zoe_romance`

Scene:
Short CG-driven romantic interlude inside Summer Festival. The shared festival
and shelter buildup are already implemented.

Director takes over after the player chooses:
`Stay near her for a moment.`

Director implements internal variants for:

- interested → possible alternate first kiss
- dating → established couple moment
- committed → quieter established intimacy

End with:
`return`

After return:
the shared Summer Festival continues normally.

---

## Phone Photo Content

Create/use directory:

`game/director_phone/`

Director-owned character files:

`game/director_phone/photo_messages_<npc_id>.rpy`

Examples:

`photo_messages_zoe.rpy`
`photo_messages_nora.rpy`
`photo_messages_elle.rpy`
`photo_messages_marcus.rpy`

Assets:

`images/phone/<npc_id>/`

Actual photo entries are registered with:

`register_npc_photo_message(...)`

The director owns:
- actual image
- filename
- photo_id
- message text
- player replies
- NPC reply labels
- relationship gates

Do NOT edit the generic phone/photo engine when adding content.

---

# RULE FOR FUTURE HANDOFFS

Whenever Claude implements a new director-owned breakpoint or content hook,
UPDATE THIS FILE in the same pass.

For each new entry include ONLY:

- file to create
- label
- 2–4 sentence scene summary
- exact handoff point
- what director implements
- relationship/state result
- return point

Keep the file short and practical.
