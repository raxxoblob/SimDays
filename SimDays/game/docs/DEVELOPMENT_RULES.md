# Development Rules

Rules for all coding agents (Claude, Qwen, or other) working on this project.

---

## Core Rules

**1. Current source beats old documentation.**
If an old design document conflicts with current `.rpy`/`.py` source, document and implement current source behavior. Old docs describe intentions; source describes reality.

**2. Existing systems are reused, not duplicated.**
Relationship helpers, commitment pipeline, phone/initiative, spend_time, gains system — these all exist. Use them. Do not create a parallel version.

**3. Preserve save compatibility.**
Every new `default` flag auto-initialises False on old saves. For flags that need backfilling from existing state, add a migration function to `config.after_load_callbacks`. Pattern: `_zoe_romance_milestone_backfill()`.

**4. Do not invent narrative content unless explicitly assigned authorship.**
If a scene's dialogue was not supplied or approved, write a placeholder and flag it. Do not fill in character voices speculatively.

**5. Supplied screenplay dialogue is locked.**
When the user provides exact dialogue lines, implement them exactly. Do not paraphrase, smooth, or edit them.

**6. Claude/Qwen are technical implementers for closed screenplay passes.**
When the user supplies a full scene spec, the AI's job is correct mechanical implementation, not creative rewriting.

---

## Director / CG Rules

**7. Director/user owns specified CG subscenes.**
Do not create or overwrite files in `game/director_romance/` unless explicitly instructed.

**8. Never invent CG image filenames.**
If a CG is needed and no filename was supplied, leave a clearly commented placeholder.

**9. Never create fake missing-image registrations.**
If an image is missing from disk, do not register a placeholder path. Report the gap.

**10. Guard all director handoff calls with `renpy.has_label()`.**
If the director file is absent, the parent scene must degrade gracefully without crashing.

---

## Story and Event Rules

**11. Major events reconverge.**
Branches inside a major event (Summer Festival, etc.) should return to a shared sequence. Do not create permanent splits that miss each other's content.

**12. No quest-like HUD progression for relationship scenes.**
Relationship progress is shown through behavior and authored dialogue, not progress-bar notifications.

**13. Relationship progression is behavioral, not transactional.**
Raw stat thresholds enable scenes; they do not cause them. Authored scenes make the progression emotionally real.

**14. Quiet days are valid gameplay.** Do not force events every day. Pacing needs breathing room.

**15. No permanent NPC schedule changes just to support one shared activity.**
Example: Zoe gym training does not give Zoe a permanent gym schedule entry. The shared activity is opt-in per commitment.

---

## Item Rules

**16. Every item must unlock behavior, not just add +stat.**
A better outfit unlocks location access or NPC response. A car unlocks mobility. A programming kit unlocks skill actions.

---

## Implementation Quality

**17. Non-trivial logic leaves one runnable check behind** — the smallest thing that fails if the logic breaks. A self-check, assert, or small test file. No frameworks or fixtures. Trivial one-liners need no test.

**18. Mark intentional simplifications with a ponytail comment (` # ponytail:`).**
If the shortcut has a known ceiling (global lock, O(n²) scan, naive heuristic), name the ceiling and upgrade path.

**19. Do not claim Ren'Py runtime/lint when the SDK was not actually run.**
Report what was verified by grep/read and what was not executed.

**20. Use stable sprite tags.**
`as npcsprite` / `at sprite_r` / `at sprite_l` are the established tag set. Do not invent new show/hide patterns.

---

## Ren'Py Gotchas

- Screen language `for` is valid inside `screen` blocks.
- Raw Python `for` inside an `init python:` block is different — they do not mix.
- `call` targets labels and returns; `jump` does not return.
- `return` value/caller unpack contract must match.
- `padding` on a `frame` takes a 4-tuple; on a `box` it does not.
- Text properties go in the `_text` child style, not on the container.
- `scene expression var_name` works for variable backgrounds.
- `use screen_name` is screen-language only; not valid in script context.
- `menu:` requires a colon; choice strings require colons.
- `init python:` ordering matters — helpers used at `init 5 python:` must be defined at `init python:` or earlier.
