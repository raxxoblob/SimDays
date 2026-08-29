# Events to generate (scripted scenes) - split by career

Each event lists the **background** and **who (sprite)** you'd need.
Career events usually trigger on **promotion**, a **crisis**, or a **milestone shift**.

Legend: 🎨 = needs new background · 🧍 = needs a character sprite · ✅ = art exists

---

## Medicine — City Hospital
| Event | Trigger | Assets |
|---|---|---|
| First shift | become Med Student | ✅ `hospital_exam` · 🧍 Dr. Lena ✅ |
| Code blue / crisis | random on shift | ✅ `hospital_exam` · 🧍 Dr. Lena ✅ |
| "You're a doctor now" | promote to Doctor | 🎨 `hospital_reception` (missing) · 🧍 Dr. Lena ✅ |
| Lena's arc (rooftop) | Trust high, night shift | ✅ `hospital_rooftop_night` · 🧍 Lena casual outfit ❌ |

## IT — The Hub
| Event | Trigger | Assets |
|---|---|---|
| Onboarding | become Junior Dev | ✅ `hub_day` · 🧍 Dave ❌ |
| Hackathon / crunch | milestone | ✅ `hub_night` · 🧍 Dave ❌ |
| Ship day / promo review | promote | ✅ `hub_day` · 🧍 team |
| Startup pitch | Jake arc | ✅ `hub_day` · 🧍 Jake (needs sprite) |

## Corporate — Nexus Tower
| Event | Trigger | Assets |
|---|---|---|
| First day politics | become Intern | ✅ `goodoffice1` · 🧍 Martha ✅, Caroline ✅ |
| After-party | milestone | ✅ `bar_rooftop_night` · 🧍 Martha ✅, Caroline ✅ |
| Promotion / power play | promote to Manager | 🧍 Martha ✅ |
| Martha scene | affection+trust | ✅ `bar_rooftop_night` · 🧍 Martha cocktail outfit ❌ |

## Trainer — Iron Gate Gym
| Event | Trigger | Assets |
|---|---|---|
| First client | become Assistant | 🧍 Victor ❌ |
| Fitness competition | milestone | 🧍 Victor ❌ |

## Culinary — Eleven
| Event | Trigger | Assets |
|---|---|---|
| Service rush | become Commis | ✅ `kitchen_dayandnight` |
| Head-chef tryout | promote to Sous/Head | ✅ `kitchen_dayandnight` · 🧍 Head Chef ❌ |

## Warehouse — LogiCity
| Event | Trigger | Assets |
|---|---|---|
| Bro moments / loan | working shifts | 🧍 Ray (needs proper sprites — currently only template) |
| Natalie arc | affection | 🧍 Natalie ✅ |

## Quayside (Nadbrzeże) — new zone
| Event | Trigger | Assets |
|---|---|---|
| Anchor bar regular | CHR/affection events | 🎨 `anchor_night` ❌ · 🧍 Dante ❌ |

---

## Suggested build order
1. IT onboarding (`hub_day` ✅ + Dave ❌) — cleanest ladder, first vertical slice
2. Medicine first shift (`hospital_exam` ✅ + Dr. Lena ✅) — showcases skill-gated career
3. Martha rooftop scene (all art either exists or in scenes.md)
