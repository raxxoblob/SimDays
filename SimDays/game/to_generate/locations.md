# Locations (backgrounds) to generate

Eye-level, realistic-anime, 16:9 (1920x1080), same style as existing backgrounds.
Drop into `images/locations/`, register in `game/images.rpy`.

---

## ✅ Done (generated + registered)

`hub_day`, `hub_night`, `college_day`, `hospital_exam`, `hospital_night`,
`bank_day`, `bank_night`, `nightclub`, `bar_rooftop_night`, `vip_lounge_airport`,
`cardealer_day`, `basketball_court_day`, `kitchen_dayandnight`,
`casino_night`, `lombard_day`, `sandbeach_night`
(sandbeach_night = nocna plaża dla zoe_swim sceny; beachnight.webp już istnieje jako główne tło plaży)

---

## ❌ Still needed

### Flea market (high priority — placeholder active)
| File | What | Notes |
|---|---|---|
| `flea_market_day` | Outdoor weekend market — vendor stalls, colourful awnings, weekend crowd, cobblestones | `location_flea_market` currently uses `mallday` placeholder. Now lives in Quayside (Nadbrzeże) on weekends |

```
Outdoor flea market on a cobblestone waterfront square, weekend morning,
colourful vendor stalls with striped awnings, people browsing, relaxed atmosphere,
warm daylight, painterly anime-realistic, 16:9
```

---

### Quayside / Nadbrzeże (new zone — needs art)
Current venues: The Anchor bar + Riverside Terrace (placeholder art active).
Proposed new venues below — wire into `nadbrzeze_hub` in `map.rpy` once art exists.

#### Tło strefy (hub background — widok gdy wchodzisz do Nadbrzeże)
Używane w `location_nadbrzeze` przed wejściem do venue. Aktualnie placeholder `restaurantday/night`.

| File | What | Notes |
|---|---|---|
| `nadbrzeze_day` | Widok nabrzeża z zewnątrz — bulwar nad rzeką, kamienice po lewej, woda i most w tle, dzień | Hub background — dzień |
| `nadbrzeze_night` | To samo miejsce wieczorem — latarnie, refleksy na wodzie, ludzie spacerujący, klimat portowy | Hub background — noc (od 19:00) |

```
# nadbrzeze_day
Waterfront promenade in a mid-sized European city, daytime — cobblestone walkway
along a river, old brick tenement buildings on the left side, a bridge visible in
the distance, moored small boats along the quay, a few people walking, trees with
summer foliage, warm afternoon light, painterly anime-realistic, 16:9

# nadbrzeze_night
Same waterfront promenade at night — old-style streetlamps lit, warm reflections
on the dark river, bridge lit in the distance, small groups of people on the quay,
bar and terrace signs glowing softly on the left, atmospheric and lively without
being a nightclub, painterly anime-realistic, 16:9
```

---

#### Venue interiors

| File | What | Hours | Notes |
|---|---|---|---|
| `anchor_night` | Waterfront bar interior — nautical touches, low lighting, view of river through windows | 17:00–03:00 | Uses `bar` placeholder |
| `terrace_day` | Outdoor riverside terrace — wooden decking, river view, parasols, warm daylight | 12:00–22:00 | Uses `restaurantday` placeholder |
| `terrace_night` | Same terrace at dusk — string lights, warm glow, river reflections in water | 18:00–22:00 | Uses `restaurantnight` placeholder |
| `lombard_day` | ✅ na dysku | — | — |
| `casino_night` | ✅ na dysku | — | — |

```
# anchor_night
Dark cosy bar interior, nautical/maritime details (rope coils, ship lanterns, porthole
windows), warm amber lighting, large windows showing dark river and city lights outside,
few people at the bar, intimate atmosphere, painterly anime-realistic, 16:9

# terrace_day
Outdoor riverside terrace, wooden decking, white parasols, river view with bridge in
background, people sitting with coffee, warm afternoon light, relaxed European vibe,
painterly anime-realistic, 16:9

# terrace_night
Same terrace at night, string lights overhead, warm orange glow, river reflecting the
lights, quieter crowd, romantic atmosphere, painterly anime-realistic, 16:9

# lombard_day
Small pawn shop interior, cluttered wooden shelves lined with second-hand electronics,
instruments, antiques and oddities, long glass display counter with jewellery and
watches inside, warm dusty lighting, faded posters on the walls, one old fan running,
lived-in and slightly chaotic, painterly anime-realistic, 16:9

# casino_night
Upscale casino interior, green felt roulette tables, slot machines in background,
crystal chandeliers, deep red and gold decor, elegant smartly dressed guests,
moody warm lighting, painterly anime-realistic, 16:9
```

Register all in `images.rpy` once dropped in.

---

### Scene backgrounds (potrzebne do nowych scen)
| File | What | Scena |
|---|---|---|
| `beach_night` | ✅ `sandbeach_night.png` na dysku — użyj tego | `zoe_swim` |
| `gallery_night` | Mała prywatna galeria sztuki wieczorem — białe ściany, obrazy pod spotami, parkiet | `elle_gallery` |
| `rooftop_radio` | Dach nocą z improwizowanym sprzętem radiowym — stary mikser, antena, miasto w dole | `zoe_radio` |

```
# gallery_night
Small intimate art gallery at night, white walls with framed paintings, warm
spotlight lighting on the art, a few well-dressed guests visible in background,
wood floors, sophisticated quiet atmosphere, painterly anime-realistic, 16:9
```

---

### Hospital reception (career event)
| File | What | Notes |
|---|---|---|
| `hospital_reception` | Hospital reception / main hall — clean, bright, professional | Used in "You're a doctor now" promotion scene |

```
Modern hospital reception hall, clean white and light blue interior,
reception desk, natural light from large windows, professional calm atmosphere,
painterly anime-realistic, 16:9
```
