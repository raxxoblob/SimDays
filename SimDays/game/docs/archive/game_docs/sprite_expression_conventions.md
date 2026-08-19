# Sprite Expression Conventions
## LivingTheDream — Standardized Expression Keys

---

## Expression Key Set

All character sprites use the following standardized expression keys regardless of character or outfit:

| Key | Meaning |
|---|---|
| `normal` | Default/at rest. Used when no other expression is appropriate. |
| `talk` | Speaking. Used during dialogue where no strong emotion is present. |
| `happy` | Positive emotion — joy, approval, warmth. |
| `angry` | Negative emotion — displeasure, frustration, controlled intensity. |
| `sad` | Sorrow, defeat, resignation. |

**Characters are not required to have all five keys.** Missing expressions fall back per the rules below.

---

## Naming Convention

Image names follow the pattern:

```
<character>_<outfit?>_<expression>
```

- No outfit qualifier = default/primary outfit (usually workplace).
- Outfit qualifier used when a character has multiple distinct outfit sets.

Examples:
- `rena_normal` — Rena, kitchen outfit, at rest
- `rena_casual_talk` — Rena, casual/off-duty outfit, speaking
- `marcus_bar_normal` — Marcus, bar outfit, at rest

---

## Fallback Rule

If a required expression is not declared for a character:

1. Fall back to `<character>_<same_outfit>_normal`.
2. If that is also missing, raise an error (do not fall back to a different outfit).

**Never fall back across outfit sets.** A casual sprite must not be substituted for a kitchen sprite or vice versa. Outfit context is meaningful.

---

## Acting Direction vs. Key Names

Expression keys describe the emotional register, not acting direction. Character personality controls how the emotion is performed:

| Key | Rena (kitchen) | Marcus (casual) | Sam (park) |
|---|---|---|---|
| `happy` | One corner of the mouth; restrained approval | Open, genuine | Bright, energetic |
| `angry` | Goes quiet; controlled; this is her tell | Direct, blunt | Rare; tight |
| `talk` | Precise; declarative | Easy, unhurried | Enthusiastic |

Document acting direction in the character's own reference file (`docs/characters/<name>.md`), not in the image name.

---

## Current Declared Sprites per Character

### Rena

All sprites in `images/characters/rena/`. Kitchen and casual sets share the same folder — distinguished by the `rena_casual_` prefix.

**Kitchen:** `rena_normal`, `rena_talk`, `rena_happy`, `rena_angry`, `rena_sad`

**Casual:** `rena_casual_normal`, `rena_casual_talk`, `rena_casual_happy`, `rena_casual_angry`, `rena_casual_sad`

### Other Characters

Other characters (Marcus, Sam, Nora, etc.) predate this convention and use a mix of `normal/talk/laugh/smile/cold/worried` keys. They are grandfathered. New characters and new outfit sets should use the standardized key set above.

---

## Adding a New Sprite Set

1. Generate PNGs with standardized expression keys as suffixes.
2. Place in `images/characters/<name>/` (primary) or `images/characters/<name>/<outfit>/` (secondary outfits).
3. Declare in `images.rpy` using the `image <name>_<key> = "path"` pattern.
4. Document acting direction in `docs/characters/<name>.md` — not in the image name or declaration.
5. Note any missing expressions and their fallback behavior in the character doc.

---

## What Must Not Appear as Image Names

Personality-specific acting descriptions must not be used as technical sprite identifiers:

| Do not use | Use instead | Notes |
|---|---|---|
| `rena_assessing` | `rena_angry` | Assessing/displeased is Rena's angry |
| `rena_approving` | `rena_happy` | Approval is Rena's happy |
| `rena_assesing` | `rena_angry` | Typo variant — also not valid |
| `rena_casual_soft` | `rena_casual_happy` or `rena_casual_normal` | Soft is not a standard key |
| `marcus_park_laugh` | Grandfathered — do not add new laugh keys | Use `happy` for new characters |
