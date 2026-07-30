# Character Bible — Living The Dream

One file per important NPC. These files are the narrative source of truth for the project.

## Rules

- Every major event, relationship-stage change, or retcon must update the relevant NPC document before or alongside the code change.
- Claude must not invent canon while updating these files. If a fact is not in the file and not confirmed in the code, it is unknown — mark it as an open thread.
- Structural eligibility (flags, counters) lives in the code. Motivation, voice, and backstory live here.
- When a character file conflicts with code, note the conflict as an open thread rather than silently resolving it.

## File per NPC

Use `_template.md` as the starting structure for each new character file.

Name each file after the NPC's lowercase identifier: `marcus.md`, `nora.md`, etc.

## Implemented Characters

NPCs with runtime declarations (NPC_DATA, sprites, relationship variables, at least one event).

| File | Character |
|---|---|
| `rena.md` | Rena (head chef, culinary arc — director-locked) |
| `marcus.md` | Marcus (neighbour) |
| `nora.md` | Nora (barista, Grounds Café) |
| `martha.md` | Martha (corporate colleague) |
| `lena.md` | Lena (doctor) |
| `natalie.md` | Natalie (friendship only, romance disabled) |
| `elle.md` | Elle (romanceable) |
| `caroline.md` | Caroline (romanceable) |
| `zoe.md` | Zoe (artist, park; Phase 6B jealousy pilot) |
| `eli.md` | Eli (IT colleague, romance disabled) |
| `sam.md` | Sam (gym regular, romance planned) |
| `kai.md` | Kai (trainer career NPC, romance planned) |

## Planned Characters

No runtime implementation. Narrative planning only. See each file for the PLANNED — NOT IMPLEMENTED notice.

| File | Character |
|---|---|
| `camila.md` | Camila Ortega (bartender, Static) |
| `owen.md` | Owen Brooks (mechanic, Static regular) |
| `sloane.md` | Sloane Mercer (events manager) |
