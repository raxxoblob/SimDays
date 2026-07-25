# Replayable CG Sequence Backlog

Visual-direction rule: a replayable cinematic activity should have at least three distinct CG beats
(Setup/arrival · Main interaction · Closing reaction). The current generated images cover Beat 2.
Beat 1 and Beat 3 are documented here but **not yet referenced in gameplay**.

Do not add gameplay references for missing beats until the files exist.

---

## Replayability status

| Activity | Repeatable? | One-time flag | Notes |
|---|---|---|---|
| `home_eli_side_project_scene` | No — one-time under current impl | `message_already_queued("eli_side_project_invite")` (permanent) | Designed with repeatable intent; `message_already_queued` blocks re-invite until that gate is redesigned |
| `home_nora_coffee_scene` | No — one-time | `home_coffee_calibrated` + `message_already_queued("nora_coffee_invite")` | Calibration event; prerequisite for cooking scene |
| `home_zoe_guitar_scene` | No — one-time under current impl | `message_already_queued("zoe_guitar_invite")` (permanent) | Designed with repeatable intent; same re-invite block as eli_side_project |
| `home_dinner_scene_eli` | No — one-time | `eli_dinner_done` | Milestone scene; `add_relationship_memory` and flag both set |
| `scene_nora_cheap_home_cooking` | No — one-time | `nora_cheap_home_cooking_done` | Cheap-home only; not available after apartment upgrade |

---

## Eli side project — beat backlog

**Current:** Beat 2 only (`cg_eli_side_project_cheap/good/rich`)

### Beat 1 — Arrival / setup
- **Proposed filename:** `cg_eli_side_project_arrival_cheap.png` / `_good` / `_rich`
- **Scene moment:** Eli arriving with a laptop bag, sitting down, setting up. "No preamble." The apartment visible in the background.
- **Characters visible:** Eli (`eli_normal`); MC implied/back-of-head or absent.
- **Outfit:** Eli casual or smart-casual; not gym/formal.
- **Home variants required:** Yes — cheap/good/rich (apartment visible in BG).
- **Emotional purpose:** Establishes intimacy (she's comfortable enough to arrive and start immediately) and the contrast between her focus and the domestic setting.

### Beat 3 — Closing reaction
- **Proposed filename:** `cg_eli_side_project_closing_cheap.png` / `_good` / `_rich`
- **Scene moment:** After the pipeline fix or the "close the laptops" choice — Eli reading the merged result, or both sitting back quietly in the apartment. The working tension resolved.
- **Characters visible:** Eli; MC optional.
- **Outfit:** Same as Beat 2.
- **Home variants required:** Yes.
- **Emotional purpose:** The payoff — problem solved, or connection chosen over productivity.

---

## Nora coffee — beat backlog

**Current:** Beat 2 only (`cg_nora_coffee_cheap/good/rich`)
**Note:** This scene is one-time. The three-beat rule matters less here than for repeatable activities, but a Beat 1 and Beat 3 would still improve the sequence.

### Beat 1 — Nora inspecting the machine
- **Proposed filename:** `cg_nora_coffee_inspect_cheap.png` / `_good` / `_rich`
- **Scene moment:** Nora walks straight to the coffee machine, inspects it, reacts. "How long have you owned this and not adjusted the grind size?" The machine itself is the subject.
- **Characters visible:** Nora (`nora_casual_normal`) at the machine; MC absent or barely implied.
- **Outfit:** Nora casual.
- **Home variants required:** Yes — machine is a real object; apartment context visible.
- **Emotional purpose:** Establishes Nora's expertise and her comfort taking over in your space.

### Beat 3 — Tasting / approval
- **Proposed filename:** `cg_nora_coffee_approval_cheap.png` / `_good` / `_rich`
- **Scene moment:** Both drinking the third (corrected) espresso. Nora's expression: not quite pride, but satisfaction.
- **Characters visible:** Nora, possibly MC hands/mug.
- **Outfit:** Nora casual.
- **Home variants required:** Yes.
- **Emotional purpose:** "Your apartment smells like a proper café." The lifestyle memory that closes the scene.

---

## Zoe guitar — beat backlog

**Current:** Beat 2 only (`cg_zoe_guitar_cheap/good/rich`)

### Beat 1 — Sceptical arrival
- **Proposed filename:** `cg_zoe_guitar_arrival_cheap.png` / `_good` / `_rich`
- **Scene moment:** Zoe arriving, sitting in the corner, sketchbook under arm. "Go on then. Prove it isn't furniture." Her expression: expecting to be underwhelmed.
- **Characters visible:** Zoe (`zoe_street_neutral`); guitar visible in the background (the object of scepticism).
- **Outfit:** Zoe street/casual.
- **Home variants required:** Yes.
- **Emotional purpose:** Sets the tone — she's testing you, not expecting much.

### Beat 3 — Quiet reaction after the performance
- **Proposed filename:** `cg_zoe_guitar_closing_cheap.png` / `_good` / `_rich`
- **Scene moment:** Zoe still sketching, glancing up. Or: she shows you the sketch (you, mid-play, not quite your face). The hour passed without her asking you to stop.
- **Characters visible:** Zoe; sketch visible; guitar optional.
- **Outfit:** Zoe street/casual.
- **Home variants required:** Yes.
- **Emotional purpose:** The shift from scepticism to quiet approval. The connection that happened without being announced.

---

## Eli dinner — beat backlog

**Current:** Beat 2 only (`cg_eli_home_dinner_cheap/good/rich`)
**Note:** `eli_dinner_done` is set — this scene is one-time. Three beats still improve the single playthrough significantly.

### Beat 1 — Arrival / the rice
- **Proposed filename:** `cg_eli_dinner_arrival_cheap.png` / `_good` / `_rich`
- **Scene moment:** Eli at the door or just inside, rice packet in hand, looking at the table. "I didn't think that through." The opening beat of the bookend.
- **Characters visible:** Eli (`eli_normal`), rice packet visible.
- **Outfit:** Eli casual.
- **Home variants required:** Yes.
- **Emotional purpose:** Establishes the rice motif and Eli's calm self-analysis.

### Beat 3 — "I like it here"
- **Proposed filename:** `cg_eli_dinner_closing_cheap.png` / `_good` / `_rich`
- **Scene moment:** Near-end of the meal. Eli looking at something in the apartment — or at the counter, where the rice still sits. A quiet moment before the line. Not sentimental; just present.
- **Characters visible:** Eli; the rice packet on the counter (deliberately in frame).
- **Outfit:** Eli casual.
- **Home variants required:** Yes.
- **Emotional purpose:** The bookend closes. The rice is still there. The line lands.

---

## Generation order for missing beats

When commissioned: Beat 1 before Beat 3 (establishes character entrance for continuity).
Priority: Eli dinner beats (one-time, highest emotional weight) > Zoe guitar (repeatable, strongest visual arc) > Eli side project (repeatable, functional) > Nora coffee (one-time, lower urgency).

Do not reference any of these filenames in gameplay code until the files physically exist.
