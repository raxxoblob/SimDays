# Scenes — image generation briefs

Format: 1920×1080, painterly anime-realistic, spójny z intro/zoe_beach.
Folder: `images/scenes/<nazwa>/`, każdy plik numerowany.

---

## System bramek (affection gates)

Każdy NPC blokuje się na progach 20 / 40 / 60 / 80 affection.
Żeby przejść przez bramkę, gracz musi zaliczyć **mini-quest** powiązany z tym NPC.
Sceny poniżej są przypisane do konkretnych progów — to one odblokowują następną bramkę.

**Sceny z rozgałęzieniem (branching):**
Scena ma jeden lub dwa momenty wyboru. W zależności od wyboru:
- wyświetla się inne CG (`_a` vs `_b` suffix albo różne numery)
- inny wynik dialogu (np. +affection vs +respect vs nic)
- potencjalnie różna ścieżka relacji w przyszłości

Przy takich scenach opisuję każdy wariant CG osobno.

---

## ✅ Done

| Scena | Folder | Próg | Status |
|---|---|---|---|
| Intro cinematic | `images/scenes/intro_scene/` | — | ✅ 7 klatek |
| Elle — "Best spot past the pier" | `images/scenes/elle_pier/` | affection 20 | ✅ 7 CGs |
| Marcus — "Shoot hoops" | `images/scenes/marcus_court/` | affection 20 | ✅ 7 CGs |
| Nora — "Closing time" | `images/scenes/nora_closing/` | affection 20 | ✅ 7 CGs |
| Zoe — "Beach meeting" | `images/scenes/zoe_beach/` | affection 20 | ✅ 7 CGs |
| Dr. Lena — "Rooftop, 3 a.m." | `images/scenes/lena_rooftop/` | affection 40 | ✅ 5 CGs |
| Martha — "After you've earned it" | `images/scenes/martha_rooftop/` | affection 40, status 35 | ✅ 6 CGs |

---

## ❌ Still needed

---

### Nora — "Właściciel przycisnął" *(affection 40 gate)*
**Folder:** `images/scenes/nora_rent/`
**Trigger:** `nora_affection >= 40`, dowolna pora
**BG:** `grounds_backroom` *(nowe — zaplecze kawiarni, małe, ciasne, praktyczne)*

**Fabuła:**
Nora dzwoni do MC między zmianami. Właściciel lokalu żąda $500 zaległego czynszu
do końca tygodnia. Nora jest spokojna na zewnątrz — MC widzi że nie jest.
Scena toczy się na zapleczu Grounds, po godzinach.

**Moment wyboru po obrazku 3:**
> "Mam to. Nie zastanawiaj się." vs "Chodź, pogadamy z nim razem." (CHR 35)

```
# nora_rent_1
Small café back room, evening — mop bucket in corner, shelf of supplies, single
bare bulb overhead, a young woman ~22 sitting on a crate looking at her phone,
worried expression she's trying to hide, painterly anime-realistic, 16:9

# nora_rent_2
Same back room, young woman talking quietly to someone (MC off-screen), hands in
her lap, not quite making eye contact, the weight of the conversation visible
in her posture, warm dim light, painterly anime-realistic, 16:9

# nora_rent_3
Close on her face — she's said the number out loud. Expression: braced for
judgement, slightly ashamed, eyes down, painterly anime-realistic, 16:9

# nora_rent_4a  [WARIANT A — pożyczasz]
Young woman looking up in surprise as a hand (MC's) offers folded cash across the
frame, her expression: not happy — overwhelmed, relieved, and something else,
café back room, painterly anime-realistic, 16:9

# nora_rent_4b  [WARIANT B — idziecie razem, CHR 35]
Young woman and a young man standing side by side in a narrow hallway facing a
door, she has her fingers lightly resting on his arm, both looking forward,
her expression: nervous but resolved, painterly anime-realistic, 16:9

# nora_rent_5a  [po A]
Young woman alone in the back room after, sitting on the same crate, looking at
the cash in her hands — not crying, but close. Something shifted in her,
warm dim light, painterly anime-realistic, 16:9

# nora_rent_5b  [po B]
The hallway — they've come back out. She's leaning against the wall, exhales.
Looks at MC sideways — less guarded than usual. Not a smile, but something opens.
Painterly anime-realistic, 16:9
```
**Wynik A:** `nora_affection += 20`, dług wdzięczności — wróci w późniejszym queście
**Wynik B:** `nora_affection += 15`, `nora_respect += 1`

---

### Marcus — "Finał ligi" *(affection 40 gate)*
**Folder:** `images/scenes/marcus_final/`
**Trigger:** `marcus_affection >= 40`, weekend
**BG:** `basketball_court_day` ✅

**Fabuła:**
Lokalny turniej ulicznego basketu. Marcus jest po drugiej stronie.
Trzy obrazki budują mecz — napięcie, ciało, zmęczenie — potem jeden decyzyjny moment.

**Moment wyboru po obrazku 4:**
> "Gram żeby wygrać." vs "Daję mu to."

```
# marcus_final_1
Outdoor street basketball court, tournament day — coloured pennants, people
watching from the sides, two teams warming up, afternoon sun, buzzy atmosphere,
painterly anime-realistic, 16:9

# marcus_final_2
Mid-game — a young Black man ~23 and MC going for the same ball, physical and
focused, both sweating, no animosity just competition, motion blur on the ball,
painterly anime-realistic, 16:9

# marcus_final_3
Last two minutes — Marcus at the free throw line, focused, crowd quiet, MC
watching from a few feet away reading his face, tense atmosphere,
painterly anime-realistic, 16:9

# marcus_final_4
Last play — MC has the ball, clear shot, Marcus closing in but too late.
The moment just before the decision: MC's expression says everything,
outdoor court, golden afternoon light, painterly anime-realistic, 16:9

# marcus_final_5a  [WARIANT A — grasz serio]
The ball goes in. Marcus stops. Looks at MC from across the court — jaw set,
competitive frustration and real respect at war in his face. First time he's
looked at MC like a peer. Painterly anime-realistic, 16:9

# marcus_final_5b  [WARIANT B — dajesz mu wygrać]
Marcus celebrates with his team. Then glances back at MC on the sideline —
something doesn't sit right with him. MC standing apart from the crowd.
His expression: good, but hollowed. Painterly anime-realistic, 16:9

# marcus_final_6  [wspólny — po obu wariantach]
After the crowd thins — Marcus walks over to MC, extends his hand. Handshake.
Neither says much. The body language does it. Painterly anime-realistic, 16:9
```
**Wynik A:** `marcus_affection += 10`, `marcus_respect += 2`
**Wynik B:** `marcus_affection += 15`, zero respect — Marcus może to wypomnieć

---

### Zoe — "Nocna kąpiel" *(affection 40 gate)*
**Folder:** `images/scenes/zoe_swim/`
**Trigger:** `zoe_affection >= 40`, wieczór 19:00–23:00
**BG:** `sandbeach_night` ✅ (na dysku)

**Fabuła:**
Zoe i MC na plaży po zmroku — wyszło przypadkowo, zostali za długo.
Zoe zdejmuje buty bez komentarza i idzie w stronę wody.
Patrzy przez ramię. To nie jest zaproszenie — to sprawdzian.

**Moment wyboru po obrazku 3:**
> "Idę." vs "Jest ciemno, nie ma sensu."

```
# zoe_swim_1
City beach at night — dark water, distant lights across the bay, sand pale under
a half-moon. A young woman with punk aesthetic walking toward the water,
shoes dangling from one hand, back to camera. MC somewhere behind her.
Painterly anime-realistic, 16:9

# zoe_swim_2
She's at the water's edge, feet in the foam, looking back over her shoulder
at MC — not asking, just checking. Expression unreadable but the question
is clear. Painterly anime-realistic, 16:9

# zoe_swim_3
MC's feet at the water's edge — the decision point. The dark sea stretching
forward. Zoe visible a few steps ahead, waiting without waiting.
Painterly anime-realistic, 16:9

# zoe_swim_4a  [WARIANT A — wchodzisz]
Both of them waist-deep in the dark water, city lights on the horizon.
She's laughing — genuinely, unguarded, completely unlike her usual edge.
It's the first time she's looked actually free. Painterly anime-realistic, 16:9

# zoe_swim_4b  [WARIANT B — odmawiasz]
She's in the water alone, chest-deep, looking back at MC on the shore.
Her expression: not angry. Just the quiet conclusion of a test failed.
She turns back to face the open water. Painterly anime-realistic, 16:9

# zoe_swim_5a  [po A]
They're sitting on the sand after, wet, close together, not talking.
The city behind them, the sea in front. The silence is comfortable.
Something changed and they both know it. Painterly anime-realistic, 16:9

# zoe_swim_5b  [po B — opcjonalny]
She walks past MC back up the beach, shoes in hand, not looking at him.
"You're like everyone else." She doesn't say it cruelly. Just factually.
Painterly anime-realistic, 16:9
```
**Wynik A:** `zoe_affection += 20` — przełamanie muru
**Wynik B:** `zoe_affection -= 5`

---

### Elle — "Szczery wernisaż" *(affection 60 gate)*
**Folder:** `images/scenes/elle_gallery/`
**Trigger:** `elle_affection >= 60`, wieczór
**BG:** `gallery_night` *(nowe)*

**Fabuła:**
Elle ma pierwszy prawdziwy wernisaż w małej galerii — nie szkolny, prawdziwy.
Zaprosiła MC. Przez pół wieczoru jest oficjalna i rozmawiająca z innymi.
Na końcu zostają sami przed jednym obrazem i pyta co MC naprawdę myśli.

**Moment wyboru po obrazku 4:**
> "Mówię szczerze." (INT 30+ = wypada dobrze; INT < 30 = rani) vs "Mówię że świetny."

```
# elle_gallery_1
Small private gallery at night — white walls, paintings under warm spotlights,
a handful of well-dressed guests with glasses of wine. A young woman ~24 with
artistic energy talking to a guest, animated, in her element.
Painterly anime-realistic, 16:9

# elle_gallery_2
She spots MC across the room — her expression shifts, something softer and more
nervous underneath the confidence. She excuses herself and walks over.
Painterly anime-realistic, 16:9

# elle_gallery_3
She and MC standing in front of her main piece — large canvas, abstract but
clearly personal. She's explaining it, hands moving, watching MC's face more
than the painting. Painterly anime-realistic, 16:9

# elle_gallery_4
The guests have thinned. Just the two of them now in front of the painting.
She asks. "What do you actually think?" Her expression: braced, open, terrified.
Painterly anime-realistic, 16:9

# elle_gallery_5a  [WARIANT A — szczerze, INT 30+]
She's listening. Really listening. Her face goes through three things at once —
hurt, recognition, something like relief. She doesn't look away.
Gallery, quiet now, warm light. Painterly anime-realistic, 16:9

# elle_gallery_5b  [WARIANT A — szczerze, INT < 30, niezgrabnie]
She flinches. A flash of hurt she doesn't hide fast enough. Then her face closes.
"Right. Thanks." Same image structure, different emotional temperature.
Painterly anime-realistic, 16:9

# elle_gallery_5c  [WARIANT B — komplementujesz]
She smiles. It's a good smile. But something behind it dims — the way a light goes
out before you notice the room got darker. She thanks him and turns back to the room.
Painterly anime-realistic, 16:9

# elle_gallery_6a  [po A, INT 30+ — zamknięcie]
Later. Outside the gallery on the steps, coats on, city sounds. She says:
"Nobody told me that before." Not sad. It's the first real thing.
Painterly anime-realistic, 16:9
```
**Wynik A (INT 30+):** `elle_affection += 25`, odblokowanie głębszych rozmów
**Wynik A (INT < 30):** `elle_affection -= 10`
**Wynik B:** `elle_affection += 5`

---

### Sam — "Torba albo twarz" *(affection 40 gate)*
**Folder:** `images/scenes/sam_gym/`
**Trigger:** `sam_affection >= 40`
**BG:** `gym_interior` *(Iron Gate — istniejący lub nowy ring interior)*

**Fabuła:**
Sam jest w ringu sama, na wpół po treningu, gdy MC wchodzi.
Rzuca rękawice w stronę MC bez pytania. Nie tłumaczy po co.
Sparing — ona jest lepsza, MC wie o tym. To nie jest o wygraniu.

**Moment wyboru po obrazku 4:**
> "Wstaję." vs "Dość."

```
# sam_gym_1
Boxing gym interior — ring ropes, heavy bags in background, hard overhead lighting.
Athletic young woman ~22 shadow-boxing alone, fluid and focused, earbuds in.
She hasn't seen MC yet. Painterly anime-realistic, 16:9

# sam_gym_2
She's facing MC now, arms crossed, boxing gloves held out — the offer without words.
Her expression: neutral, evaluating. This means something and she knows it.
Painterly anime-realistic, 16:9

# sam_gym_3
Sparring in progress — she's moving well, MC is chasing. She's not going easy.
Her face in motion: concentration, something like enjoyment.
Painterly anime-realistic, 16:9

# sam_gym_4
MC is on the mat. She landed something clean. She's standing back, arms loose,
watching — not gloating, just waiting to see what happens next.
Painterly anime-realistic, 16:9

# sam_gym_5a  [WARIANT A — wstajesz]
MC getting back up, a little unsteady, smiling anyway. She doesn't smile back —
but her chin dips slightly. Acknowledgement. The real kind.
Painterly anime-realistic, 16:9

# sam_gym_5b  [WARIANT B — rezygnujesz]
MC sitting on the mat, gloves in lap, done. She looks at him for a moment —
not contempt, something closer to quiet disappointment. She picks up her towel.
Painterly anime-realistic, 16:9

# sam_gym_6a  [po A — zamknięcie]
End of session. She's unlacing her gloves. Doesn't look up but says something.
"Same time Thursday." It's the closest thing to a compliment she gives.
Painterly anime-realistic, 16:9
```
**Wynik A:** `sam_affection += 20`, `sam_respect += 2`
**Wynik B:** `sam_affection += 5`

---

### Eli — "Coś co znalazłem" *(affection 40 gate + metal detector quest)*
**Folder:** `images/scenes/eli_find/`
**Trigger:** `eli_affection >= 40` + znaleziono co najmniej 1 przedmiot na plaży
**BG:** `beach_day` ✅

**Fabuła:**
Eli czyta na plaży. Widzi MC z detektorem. Podchodzi — zaintrygowana, trochę drwiąca.
Rozmowa nie jest o znaleziskach. Schodzi na to czego naprawdę szukamy.
Eli ma swoją wersję tej odpowiedzi — nie powie wprost, ale MC zobaczy.

Scena jest **linearna** ale zmienia się jeśli MC ma przy sobie pierścionek z questu —
Eli go rozpoznaje. To otwiera inną warstwę dialogu i daje +10 bonus do affection.

```
# eli_find_1
Sunny beach, daytime. Bookish young woman ~22 lying on a towel with a book,
looking up at something off-screen — mildly amused, mildly sceptical.
Casual, unhurried. Painterly anime-realistic, 16:9

# eli_find_2
She's sitting up now, watching MC sweep the metal detector across the sand,
arms around her knees, expression: gently curious, the teasing hasn't started yet.
Painterly anime-realistic, 16:9

# eli_find_3
Both sitting on the sand now, a few found objects between them — coins, a broken
watch, a button. She's holding one up, turning it over.
Painterly anime-realistic, 16:9

# eli_find_4
She's stopped looking at the objects. She's looking at the sea. Something shifted
in the conversation — she said something honest and is waiting to see what MC
does with it. Quiet, private moment. Painterly anime-realistic, 16:9

# eli_find_5
Sun lower now. She gets up, brushes sand off, picks up her book. Pauses.
Looks back at MC — not dramatic, just present. "See you around."
Means something slightly different now. Painterly anime-realistic, 16:9
```
**Wynik:** `eli_affection += 15` (+ 10 bonus jeśli masz pierścionek)
Odblokowany topic: "rzeczy które tracimy"

---

---

### Zoe — "Szkicownik" *(affection 60 gate)*
**Folder:** `images/scenes/zoe_sketchbook/`
**Trigger:** `zoe_affection >= 60`, dzień
**BG:** `beach_day` ✅

**Fabuła:**
Zoe wysyła MC SMS-a: "plaża". Nic więcej. Gdy MC przychodzi, ona ma swój prawdziwy
szkicownik — nie portfolio, nie zdjęcia do story. Ten, do którego nikt nie zagląda.
Pokazuje bez słowa wyjaśnienia. To jest zaufanie, nie rozmowa.
INT 25+ odblokowuje głębszy dialog (MC pyta właściwe pytanie, ona pokazuje więcej).

```
# zoe_sketchbook_1
Sunny beach, daytime. Young woman with punk aesthetic sitting cross-legged on sand,
a worn sketchbook in her lap, looking toward the water, waiting. Not visibly anxious
— just present. Painterly anime-realistic, 16:9

# zoe_sketchbook_2
Close on the sketchbook open on her lap — personal, raw sketches visible (faces,
cityscapes, fragments of text), her hand resting on the page. MC visible beside her
slightly out of focus. Painterly anime-realistic, 16:9

# zoe_sketchbook_3
She's watching MC look at the sketches — expression: unguarded, the careful
neutrality dropped. This is what she looks like when she's actually uncertain.
Painterly anime-realistic, 16:9

# zoe_sketchbook_4a  [INT 25+ — MC asks the right question]
She turns a page and shows something more personal — a self-portrait, or something
that explains the others. Her expression: quiet surprise that he asked that.
Painterly anime-realistic, 16:9

# zoe_sketchbook_4b  [INT < 25 — MC says something generic]
She closes the sketchbook. Not hurt — just: "yeah, that's enough."
Her expression: familiar small disappointment, she was almost there.
Painterly anime-realistic, 16:9

# zoe_sketchbook_5  [wspólny — słońce niżej, siedzą dalej razem]
Late afternoon. They're still there. She's drawing again, he's beside her.
The sketchbook is closed between them. The silence is easy.
Painterly anime-realistic, 16:9
```
**Wynik A (INT 25+):** `zoe_affection += 20`, nowy topic "co rysujesz"
**Wynik B:** `zoe_affection += 10`

---

### Zoe — "Pirackie radio" *(affection 80 gate)*
**Folder:** `images/scenes/zoe_radio/`
**Trigger:** `zoe_affection >= 80`, noc (21:00+)
**BG:** `rooftop_radio` *(nowe — dach z anteną i improwizowanym sprzętem radiowym)*

**Fabuła:**
Zoe robi nielegalne audycje raz w miesiącu. Pyta MC czy chce przyjść.
Dach, antena, stary mikser, miasto pod nimi. Ona mówi do mikrofonu o muzyce, sztuce,
ludziach — rzeczy których nie powie prosto w oczy. W pewnym momencie przesuwa
mikrofon w stronę MC. Wybór co powiedzieć.

**Moment wyboru po obrazku 3:**
> "Mówię o Zoe." vs "Mówię o czymś innym."

```
# zoe_radio_1
Rooftop at night — improvised radio setup: old mixer, antenna, cables taped to
a folding table, city lights below. Young woman adjusting something, headphones
around her neck, in her element. Painterly anime-realistic, 16:9

# zoe_radio_2
She's talking into a microphone, eyes half-closed, completely unselfconscious —
this is the most honest version of her, no audience to perform for.
City glow behind her. Painterly anime-realistic, 16:9

# zoe_radio_3
She slides the microphone across the table toward MC. Her expression: curious,
a little daring. "Your turn." Painterly anime-realistic, 16:9

# zoe_radio_4a  [mówisz o Zoe — on air, nie wiedząc że ona słyszy co mówisz]
MC at the microphone. The city below. Her face off to the side, listening.
Something changes in her expression — she wasn't expecting that.
Painterly anime-realistic, 16:9

# zoe_radio_4b  [mówisz o czymś innym — bezpieczna odpowiedź]
MC at the microphone saying something neutral. She's watching. Slight smile —
not disappointed, just: "okay, so that's where you are."
Painterly anime-realistic, 16:9

# zoe_radio_5a  [po A — koniec audycji]
Static cuts out. Just the two of them on the rooftop, city below.
She's looking at MC differently. She doesn't say anything. She doesn't need to.
Painterly anime-realistic, 16:9

# zoe_radio_5b  [po B — koniec audycji]
She packs up the equipment. Friendly, normal. Something didn't quite open.
But she's glad he came. Painterly anime-realistic, 16:9
```
**Wynik A:** `zoe_affection += 25`
**Wynik B:** `zoe_affection += 10`

**Nowe BG:** `rooftop_radio`
```
Urban rooftop at night, improvised radio broadcast setup — folding table with
old audio mixer, cables, a directional antenna attached to a chimney, city
lights stretching below, intimate and slightly illegal atmosphere,
painterly anime-realistic, 16:9
```

---

### Zoe — "Zostań" *(affection 95 gate)*
**Folder:** `images/scenes/zoe_stay/`
**Trigger:** `zoe_affection >= 95`, dowolna pora
**BG:** `sandbeach_night` ✅

**Fabuła:**
MC zbiera się do wyjścia. Zoe mówi "Zostań." Jedno słowo. Pierwszy raz
o cokolwiek prosi wprost. Nie tłumaczy. Nie dodaje nic.
Scena jest prosta — wielka albo nie zależy od jednej odpowiedzi MC.

**Moment wyboru — jedyny w scenie:**
> "Zostaję." vs "Muszę iść."

```
# zoe_stay_1
Beach at night. They've been here a while — shoes off, sitting close.
The city distant. MC is getting up, reaching for jacket.
Painterly anime-realistic, 16:9

# zoe_stay_2
Her face as she says it. No performance, no edge, no irony.
Just: "Stay." The most unguarded she's ever been.
Painterly anime-realistic, 16:9

# zoe_stay_3a  [zostajesz]
He sits back down. She doesn't smile — she exhales. They're both looking at
the water. The city hum. Everything that doesn't need to be said.
Painterly anime-realistic, 16:9

# zoe_stay_3b  [idziesz]
He leaves. She's still sitting there. Not watching him go — looking at the water.
The sketchbook in her lap. She knew the answer before she asked.
Painterly anime-realistic, 16:9

# zoe_stay_4a  [tylko po A — świt]
Early light. They're still there. She's asleep on his shoulder, sketchbook
open on her lap. The page is blank — she never drew anything.
Painterly anime-realistic, 16:9
```
**Wynik A:** `zoe_affection = 100`, scena relacji odblokowana
**Wynik B:** `zoe_affection -= 10`, Zoe pamięta

---

## Nowe BG potrzebne do powyższych scen

| Plik | Scena | Opis skrótowy |
|---|---|---|
| `beach_night` | zoe_swim | Nocna plaża, ciemna woda, miasto w tle |
| `gallery_night` | elle_gallery | Mała galeria sztuki wieczorem, białe ściany |

Dodać do `to_generate/locations.md`.
