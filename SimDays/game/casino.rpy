# casino.rpy — Casino Royal: location floor + Blackjack + Roulette
# Cards: images/ui/cards_cropped_53/ (126×187 px, ~2:3)
# Chips: images/ui/casino/chips/chip_N.png (128×128 circular transparent PNG)

init python:
    CARD_W = 122
    CARD_H  = 181

    _BJ_RANKS  = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    _BJ_SUITS  = ["♠","♥","♦","♣"]
    _RANK_IDX  = {"A":0,"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,"8":7,"9":8,"10":9,"J":10,"Q":11,"K":12}
    _SUIT_DATA = {"♣":("clubs",1),"♥":("hearts",14),"♠":("spades",27),"♦":("diamonds",40)}

    def _card_img(rank, suit):
        suit_name, offset = _SUIT_DATA[suit]
        n = offset + _RANK_IDX[rank]
        return "images/ui/cards_cropped_53/%02d_%s_%s.png" % (n, rank, suit_name)

    _CARD_BACK = "images/ui/cards/card_back.png"

    def _bj_new_deck():
        d = [(r, s) for s in _BJ_SUITS for r in _BJ_RANKS]
        renpy.random.shuffle(d)
        return d

    def _bj_val(rank):
        if rank in ("J","Q","K"): return 10
        if rank == "A": return 11
        return int(rank)

    def _bj_total(hand):
        t = sum(_bj_val(r) for r, s in hand)
        a = sum(1 for r, s in hand if r == "A")
        while t > 21 and a:
            t -= 10; a -= 1
        return t

    _ROU_REDS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}

    # Chip denominations: (img_key, amount, text for tray label)
    _CHIPS = [
        (5,   "chip_5"),
        (25,  "chip_25"),
        (100, "chip_100"),
        (250, "chip_250"),
        (500, "chip_500"),
    ]

    def _chip_img(amt):
        return "images/ui/casino/chips/chip_%d.png" % amt

    # ── Blackjack ─────────────────────────────────────────────────────────────
    class _BJ:
        def __init__(self):
            self.deck      = _bj_new_deck()
            self.player    = []
            self.dealer    = []
            self.bet       = 0          # sum of bet_chips
            self.bet_chips = []         # list of chip denominations placed
            self.hand_bet  = 0
            self.phase     = "betting"  # betting | playing | result
            self.msg       = ""

        def new_game(self):
            if len(self.deck) < 15:
                self.deck = _bj_new_deck()
            self.player    = []
            self.dealer    = []
            self.phase     = "betting"
            self.msg       = ""
            self.hand_bet  = self.bet
            # bet_chips preserved so Play Again re-uses last stake

        def add_chip(self, amt):
            chips = getattr(self, 'bet_chips', [])
            chips = list(chips)     # copy so old saves don't mutate unexpectedly
            chips.append(amt)
            total = sum(chips)
            if total > 2000:
                return              # silently cap
            self.bet_chips = chips
            self.bet       = total

        def clear_bet(self):
            self.bet_chips = []
            self.bet       = 0

        def deal(self):
            if self.bet <= 0:
                self.msg = "Place a bet first."; return False
            if not try_spend(self.bet, category="gambling", toast=False):
                self.msg = "Not enough money."; return False
            self.hand_bet = self.bet
            self.player   = [self.deck.pop(), self.deck.pop()]
            self.dealer   = [self.deck.pop(), self.deck.pop()]
            self.phase    = "playing"
            if _bj_total(self.player) == 21:
                self._finish()
            return True

        def hit(self):
            self.player.append(self.deck.pop())
            if _bj_total(self.player) > 21:
                self.msg = "Bust!"; self.phase = "result"

        def stand(self):
            while _bj_total(self.dealer) < 17:
                self.dealer.append(self.deck.pop())
            self._finish()

        def double_down(self):
            if not try_spend(self.hand_bet, category="gambling", toast=False):
                self.msg = "Not enough to double."; return
            self.hand_bet *= 2
            self.player.append(self.deck.pop())
            if _bj_total(self.player) > 21:
                self.msg = "Bust!"; self.phase = "result"
            else:
                self.stand()

        def _finish(self):
            pt  = _bj_total(self.player)
            dt  = _bj_total(self.dealer)
            nat = (pt == 21 and len(self.player) == 2)
            if pt > 21:
                self.msg = "Bust. Lost $%d." % self.hand_bet
            elif dt > 21 or pt > dt:
                gain = int(self.hand_bet * 1.5) if nat else self.hand_bet
                store.money += self.hand_bet + gain
                self.msg = ("Blackjack! +$%d" if nat else "You win! +$%d") % gain
            elif pt == dt:
                store.money += self.hand_bet
                self.msg = "Push — bet returned."
            else:
                self.msg = "Dealer wins. Lost $%d." % self.hand_bet
            self.phase = "result"

    # ── Roulette — multi-bet ──────────────────────────────────────────────────
    class _Rou:
        def __init__(self):
            self.result       = None
            self.bets         = []    # list of {"type":str, "num":int|None, "amt":int, "chips":[int,...]}
            self.chip_amt     = 25    # currently selected chip denomination
            self.msg          = ""
            self.phase        = "betting"
            self._pending     = 0
            self._locked_bets = []    # snapshot taken at start_spin(); settlement uses this

        def _find_bet(self, bet_type, num):
            for b in self.bets:
                if b["type"] == bet_type and b.get("num") == num:
                    return b
            return None

        def add_bet(self, bet_type, num=None):
            existing = self._find_bet(bet_type, num)
            amt = self.chip_amt
            if existing:
                existing["amt"] += amt
                existing.setdefault("chips", []).append(amt)
            else:
                self.bets.append({"type": bet_type, "num": num, "amt": amt, "chips": [amt]})

        def remove_bet(self, bet_type, num=None):
            self.bets = [b for b in self.bets
                         if not (b["type"] == bet_type and b.get("num") == num)]

        def total_bet(self):
            return sum(b["amt"] for b in self.bets)

        def clear_bets(self):
            self.bets = []

        def bet_on(self, bet_type, num=None):
            b = self._find_bet(bet_type, num)
            return b["amt"] if b else 0

        def bet_chips_on(self, bet_type, num=None):
            """Return chip list for a position, or reconstruct from amt for old saves."""
            b = self._find_bet(bet_type, num)
            if not b:
                return []
            chips = b.get("chips")
            if chips:
                return chips
            # old-save reconstruction: fill with largest denominations that fit
            amt = b["amt"]
            result = []
            for denom in [500, 250, 100, 25, 5]:
                while amt >= denom:
                    result.append(denom); amt -= denom
            return result

        def start_spin(self):
            if not self.bets:
                self.msg = "Place at least one bet."; return False
            if not try_spend(self.total_bet(), category="gambling", toast=False):
                self.msg = "Not enough money."; return False
            # Snapshot paid bets before animation — settlement must use this, not live self.bets
            self._locked_bets = [dict(b) for b in self.bets]
            self._pending = renpy.random.randint(0, 36)
            self.result   = None
            self.msg      = ""
            self.phase    = "spinning"
            return True

        def finish_spin(self):
            n      = self._pending
            self.result = n
            red    = (n in _ROU_REDS)
            # Use locked snapshot — immune to any bet mutation during spin animation
            locked = getattr(self, '_locked_bets', list(self.bets))
            staked = sum(b["amt"] for b in locked)
            returned = 0
            for b in locked:
                bt, ba, bn = b["type"], b["amt"], b.get("num")
                mult = 0
                if   bt == "red"    and n != 0 and red:         mult = 2
                elif bt == "black"  and n != 0 and not red:     mult = 2
                elif bt == "even"   and n != 0 and n % 2 == 0:  mult = 2
                elif bt == "odd"    and n % 2 == 1:             mult = 2
                elif bt == "low"    and 1 <= n <= 18:           mult = 2
                elif bt == "high"   and 19 <= n <= 36:          mult = 2
                elif bt == "doz1"   and 1 <= n <= 12:           mult = 3
                elif bt == "doz2"   and 13 <= n <= 24:          mult = 3
                elif bt == "doz3"   and 25 <= n <= 36:          mult = 3
                elif bt == "number" and n == bn:                mult = 37
                returned += ba * mult
            if returned:
                store.money += returned
                net = returned - staked
                color_tag = ("GREEN" if n == 0 else ("RED" if red else "BLACK"))
                self.msg = "%d  %s\n+$%d" % (n, color_tag, net)
            else:
                color_tag = ("GREEN" if n == 0 else ("RED" if red else "BLACK"))
                self.msg = "%d  %s\n-$%d" % (n, color_tag, staked)
            self.phase = "result"

        def reset(self):
            self.result       = None
            self.msg          = ""
            self.phase        = "betting"
            self.bets         = []
            self._locked_bets = []

    bj_game  = _BJ()
    rou_game = _Rou()


# ── Transforms ────────────────────────────────────────────────────────────────

transform _rou_spin_anim:
    rotate 0.0
    linear 2.5 rotate 1440.0

transform _rou_static(angle):
    rotate angle

transform _chip_selected:
    zoom 1.08 yoffset -5

transform _chip_idle:
    zoom 1.0 yoffset 0


# ── Location entry ─────────────────────────────────────────────────────────────

label location_casino:
    $ current_loc = "location_casino"
    if hour < 20 and hour >= 4:
        "The casino doesn't open until 8 PM."
        jump location_nadbrzeze
    if stat_chr < 25:
        "The doorman barely glances at you. \"Members and guests only.\" He doesn't move."
        jump location_nadbrzeze
    jump casino_floor_actions

label casino_floor_actions:
    $ current_loc = "location_casino"
    $ activity_exit_jump = "location_nadbrzeze"
    $ activity_exit_name = "Quayside"
    scene casino_night
    show screen hud
    hide screen people_here_dock
    # World Event Director
    $ _wed_amb = wed_poll_ambient("location_casino")
    if _wed_amb:
        call expression _wed_amb
    $ _wed_per = wed_poll_personal("location_casino")
    if _wed_per:
        call expression _wed_per
    # Living-world pipeline: invitation → crossover → ambient (once per visit)
    $ _lw = process_location_entry("location_casino")
    if _lw:
        if _lw[0] == "invitation":
            call run_npc_invitation(_lw[1]["id"])
        elif _lw[0] == "crossover":
            call run_crossover(_lw[1])
        elif _lw[0] == "ambient":
            $ record_location_ambient(_lw[1]["id"], "location_casino")
            $ renpy.notify(_lw[1]["text"])
        else:
            call run_living_world_extra(_lw[0], _lw[1])
    $ _vis = location_sprites()
    call show_public_sprites
    show screen people_here_dock("casino_floor_actions")
    menu (screen="activity"):
        "Blackjack Table (0.25h per hand)":
            $ bj_game.new_game()
            hide screen people_here_dock
            $ set_hud("hidden")
            jump casino_blackjack_loop
        "Roulette Table (0.25h per spin)":
            $ rou_game.reset()
            hide screen people_here_dock
            $ set_hud("hidden")
            jump casino_roulette_loop
        "Casino Bar — have a drink ($8, 0.5h)":
            $ spend_time(0.5)
            $ gain_money(-8)
            "The bartender sets down a heavy crystal glass. You nurse it slowly, watching the tables."
            jump casino_floor_actions
        "Look Around (0.5h)":
            $ spend_time(0.5)
            "The casino hums with restrained energy — the soft clatter of chips, a dealer's murmur, the faint click of a roulette ball finding its number."
            jump casino_floor_actions
        "Leave":
            jump location_nadbrzeze


# ── Blackjack loop ─────────────────────────────────────────────────────────────

label casino_blackjack_loop:
    call screen casino_blackjack
    if not isinstance(_return, (str, tuple)):
        jump casino_blackjack_loop
    if isinstance(_return, tuple) and _return[0] == "chip":
        $ bj_game.add_chip(_return[1])
    elif _return == "clear_bet":
        $ bj_game.clear_bet()
    elif _return == "deal":
        if bj_game.deal():
            $ spend_time(0.25)
    elif _return == "hit":
        $ bj_game.hit()
    elif _return == "stand":
        $ bj_game.stand()
    elif _return == "double":
        $ bj_game.double_down()
    elif _return == "new_game":
        $ bj_game.new_game()
    elif _return == "back":
        $ set_hud("full")
        jump casino_floor_actions
    jump casino_blackjack_loop


# ── Roulette loop ──────────────────────────────────────────────────────────────

label casino_roulette_loop:
    call screen casino_roulette
    if not isinstance(_return, (str, tuple)):
        jump casino_roulette_loop
    if isinstance(_return, tuple):
        if _return[0] == "add_bet":
            $ rou_game.add_bet(_return[1], _return[2] if len(_return) > 2 else None)
        elif _return[0] == "remove_bet":
            $ rou_game.remove_bet(_return[1], _return[2] if len(_return) > 2 else None)
        elif _return[0] == "set_chip":
            $ rou_game.chip_amt = _return[1]
    elif _return == "clear_bets":
        $ rou_game.clear_bets()
    elif _return == "spin":
        if rou_game.start_spin():
            $ spend_time(0.25)
    elif _return == "spin_done":
        $ rou_game.finish_spin()
    elif _return == "reset":
        $ rou_game.reset()
    elif _return == "back":
        $ set_hud("full")
        jump casino_floor_actions
    jump casino_roulette_loop


# ── Shared chip-stack sub-screen ───────────────────────────────────────────────
# chips: list of int denominations (oldest first, newest last = visually on top)
# compact: True = 56px chips, False = 72px chips
# xsize/ysize of this screen adjusts to content; parent places it with xalign/ypos.

screen casino_chip_stack(chips, compact=False):
    $ _sz   = 56 if compact else 72
    $ _step = 8  if compact else 11
    $ _shown = list(chips)[-5:] if chips else []
    $ _count = len(_shown)
    fixed:
        xsize _sz
        ysize (_sz + max(0, _count - 1) * _step + 4)
        for _ci, _ca in enumerate(_shown):
            # _ci=0 is oldest (bottom of stack, drawn first = behind)
            # _ci=N-1 is newest (top of stack, drawn last = in front)
            # bottom chip sits at highest ypos (visually lowest in fixed)
            add _chip_img(_ca):
                xysize (_sz, _sz)
                xpos 0
                ypos (_count - 1 - _ci) * _step


# ── Blackjack screen ───────────────────────────────────────────────────────────
# Returns: ("chip", amount) | "clear_bet" | "deal" | "hit" | "stand" | "double"
#          "new_game" | "back"
# Background: casino_night scene underneath; dark overlay here.

screen casino_blackjack():
    # Dark overlay so casino bg remains visible but table pops
    add Solid("#00000096") xpos 0 ypos 0 xsize 1920 ysize 1080

    # Main panel — centered
    frame:
        xalign 0.5 yalign 0.5
        xsize 1500 ysize 880
        background "#161616f5"
        padding (0, 0, 0, 0)

        # ── Header bar ──────────────────────────────────────────────────────
        frame:
            xfill True ysize 58
            background "#0d0d0dee"
            padding (28, 0, 20, 0)
            hbox:
                xfill True yalign 0.5 spacing 0
                text "♠  BLACKJACK":
                    font PROFILE_FONT size 22 color "#d4af37" yalign 0.5
                null xfill True
                text ("Balance  $%d" % money):
                    font ACT_FONT size 18 color "#b8b0a0" yalign 0.5
                null width 28
                textbutton "← Back to Casino":
                    action Return("back")
                    background None hover_background None
                    padding (16, 0, 0, 0)
                    text_font ACT_FONT text_size 17
                    text_color "#7a8a7a" text_hover_color "#c0d4c0"
                    yalign 0.5

        # ── Felt table area ─────────────────────────────────────────────────
        frame:
            xalign 0.5 ypos 66
            xsize 1460 ysize 806
            background "#0b2e0bdd"
            padding (0, 0, 0, 0)

            # Subtle brass border (drawn as a second frame on top)
            frame:
                xfill True yfill True
                background "#00000000"
                foreground Frame("images/ui/act_bar_idle.png", 6, 6)

            # ── DEALER ────────────────────────────────────────────────────
            text "DEALER":
                xalign 0.5 ypos 22
                font PROFILE_FONT size 16 color "#3a7040"

            if bj_game.dealer and bj_game.phase != "playing":
                $ _dt = _bj_total(bj_game.dealer)
                $ _dt_col = ("#e05050" if _dt > 21 else "#f0f0f0")
                text str(_dt):
                    xalign 0.5 ypos 48
                    font PROFILE_FONT size 34 color _dt_col

            # Dealer cards — centered row
            fixed xalign 0.5 ypos 90 xsize 900 ysize 190:
                if bj_game.dealer:
                    $ _dw = len(bj_game.dealer) * CARD_W + (len(bj_game.dealer)-1) * 10
                    hbox:
                        xpos max(0, (900 - _dw) // 2)
                        spacing 10
                        for _di, (_dr, _ds) in enumerate(bj_game.dealer):
                            if _di == 1 and bj_game.phase == "playing":
                                add _CARD_BACK xysize (CARD_W, CARD_H)
                            else:
                                add _card_img(_dr, _ds) xysize (CARD_W, CARD_H)

            # ── Centre divider ────────────────────────────────────────────
            frame:
                xalign 0.5 ypos 306
                xsize 1000 ysize 2
                background "#1e5a1e"

            # ── Betting spot ──────────────────────────────────────────────
            # Circular felt area showing stacked chips
            $ _bchips = getattr(bj_game, 'bet_chips', [])
            frame:
                xalign 0.5 ypos 318
                xsize 150 ysize 100
                background "#092e09"
                padding (0, 0, 0, 0)
                # Chips inside the circle area
                if _bchips:
                    fixed xalign 0.5 yalign 0.5:
                        use casino_chip_stack(_bchips, compact=True)
                else:
                    text "BET":
                        xalign 0.5 yalign 0.5
                        font PROFILE_FONT size 13 color "#2a5a2a"

            # Bet total below the circle
            if bj_game.phase == "betting":
                hbox:
                    xalign 0.5 ypos 424
                    spacing 14
                    text ("$%d" % bj_game.bet):
                        font PROFILE_FONT size 28 color "#d4af37" yalign 0.5
                    if _bchips:
                        textbutton "✕":
                            action Return("clear_bet")
                            background None hover_background None
                            padding (0, 0, 0, 0)
                            text_font PROFILE_FONT text_size 20
                            text_color "#883030" text_hover_color "#cc4040"
                            yalign 0.5

            # ── PLAYER cards ──────────────────────────────────────────────
            fixed xalign 0.5 ypos 436 xsize 900 ysize 190:
                if bj_game.player:
                    $ _pw = len(bj_game.player) * CARD_W + (len(bj_game.player)-1) * 10
                    hbox:
                        xpos max(0, (900 - _pw) // 2)
                        spacing 10
                        for _pr, _ps in bj_game.player:
                            add _card_img(_pr, _ps) xysize (CARD_W, CARD_H)

            if bj_game.player:
                $ _pt = _bj_total(bj_game.player)
                $ _pt_col = ("#e05050" if _pt > 21 else ("#d4af37" if _pt == 21 else "#f0f0f0"))
                text str(_pt):
                    xalign 0.5 ypos 630
                    font PROFILE_FONT size 34 color _pt_col

            text "YOU":
                xalign 0.5 ypos 672
                font PROFILE_FONT size 16 color "#3a7040"

            # ── Message ───────────────────────────────────────────────────
            if bj_game.msg:
                text bj_game.msg:
                    xalign 0.5 ypos 700
                    font PROFILE_FONT size 26 color "#f0d060"

            # ── Controls ──────────────────────────────────────────────────
            if bj_game.phase == "betting":
                # Chip tray
                hbox:
                    xalign 0.5 ypos 466 spacing 14
                    for _camt, _ckey in _CHIPS:
                        button:
                            xysize (76, 76)
                            background None hover_background None
                            action Return(("chip", _camt))
                            add _chip_img(_camt) xysize (76, 76)

                # Deal button
                textbutton "DEAL":
                    xalign 0.5 ypos 550
                    action Return("deal")
                    background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                    hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                    padding (48, 14, 48, 14)
                    text_font PROFILE_FONT text_size 26 text_color "#d4af37" text_hover_color "#ffffff"

            elif bj_game.phase == "playing":
                hbox:
                    xalign 0.5 ypos 720 spacing 18
                    textbutton "HIT":
                        action Return("hit")
                        background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                        padding (32, 12, 32, 12)
                        text_font PROFILE_FONT text_size 20 text_color "#d4af37" text_hover_color "#ffffff"
                    textbutton "STAND":
                        action Return("stand")
                        background Frame("images/ui/act_bar_idle.png", 20, 20)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                        padding (32, 12, 32, 12)
                        text_font PROFILE_FONT text_size 20 text_color "#c0c0c0" text_hover_color "#ffffff"
                    if money >= bj_game.hand_bet and len(bj_game.player) == 2:
                        textbutton "DOUBLE":
                            action Return("double")
                            background Frame("images/ui/act_bar_idle.png", 20, 20)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                            padding (26, 12, 26, 12)
                            text_font PROFILE_FONT text_size 20 text_color "#a0b8c0" text_hover_color "#ffffff"

            elif bj_game.phase == "result":
                hbox:
                    xalign 0.5 ypos 730 spacing 18
                    textbutton "Play Again":
                        action Return("new_game")
                        background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                        padding (28, 12, 28, 12)
                        text_font PROFILE_FONT text_size 19 text_color "#d4af37" text_hover_color "#ffffff"
                    textbutton "Back to Casino":
                        action Return("back")
                        background Frame("images/ui/act_bar_idle.png", 20, 20)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                        padding (24, 12, 24, 12)
                        text_font ACT_FONT text_size 17 text_color "#9ab89a" text_hover_color "#ffffff"


# ── Roulette screen ────────────────────────────────────────────────────────────
# Returns: ("add_bet", type, num) | ("remove_bet", type, num) | ("set_chip", amt)
#          "clear_bets" | "spin" | "spin_done" | "reset" | "back"

screen casino_roulette():
    if rou_game.phase == "spinning":
        timer 2.5 action Return("spin_done")

    # Dark overlay
    add Solid("#00000096") xpos 0 ypos 0 xsize 1920 ysize 1080

    # Main panel — centered
    frame:
        xalign 0.5 yalign 0.5
        xsize 1540 ysize 880
        background "#161616f5"
        padding (0, 0, 0, 0)

        # ── Header bar ──────────────────────────────────────────────────────
        frame:
            xfill True ysize 58
            background "#0d0d0dee"
            padding (28, 0, 20, 0)
            hbox:
                xfill True yalign 0.5 spacing 0
                text "◉  ROULETTE":
                    font PROFILE_FONT size 22 color "#d4af37" yalign 0.5
                null xfill True
                text ("Balance  $%d" % money):
                    font ACT_FONT size 18 color "#b8b0a0" yalign 0.5
                null width 28
                textbutton "← Back to Casino":
                    action Return("back")
                    background None hover_background None
                    padding (16, 0, 0, 0)
                    text_font ACT_FONT text_size 17
                    text_color "#7a8a7a" text_hover_color "#c0d4c0"
                    yalign 0.5

        # ── Content area ────────────────────────────────────────────────────
        frame:
            xpos 0 ypos 58
            xsize 1540 ysize 822
            background "#00000000"
            padding (0, 0, 0, 0)

            # ── Left: Betting mat (~920px) ────────────────────────────────
            frame:
                xpos 0 ypos 0
                xsize 920 ysize 822
                background "#0b2e0bcc"
                padding (12, 16, 12, 12)

                # Relative positions of cells (within the 896×790 inner area):
                #   0:      xpos 0,     ypos 0, xysize (58, 219)
                #   n 1-36: col=(n-1)//3, row=2-((n-1)%3)
                #           xpos=62+col*70, ypos=row*73, xysize(68,71)
                #   Dozens: xpos=62+di*278, ypos=222, xysize(276,46)
                #   Outside:xpos=62+oi*140, ypos=272, xysize(138,46)

                # Is betting locked?
                $ _rou_locked = (rou_game.phase != "betting")

                # Zero button
                $ _b0 = rou_game.bet_on("number", 0)
                button:
                    xysize (58, 219)
                    xpos 0 ypos 0
                    action (NullAction() if _rou_locked else Return(("add_bet", "number", 0)))
                    sensitive (not _rou_locked)
                    background "#145214dd"
                    hover_background ("#145214dd" if _rou_locked else "#1e7a1edd")
                    text "0":
                        xalign 0.5 yalign 0.5
                        font PROFILE_FONT size 22 color "#ffffff"

                # Numbers 1–36
                for _col in range(12):
                    for _row in range(3):
                        $ _n   = _col * 3 + (3 - _row)
                        $ _red = (_n in _ROU_REDS)
                        $ _base_bg = ("#4a1010cc" if _red else "#101010cc")
                        $ _hov_bg  = ("#6a1818cc" if _red else "#2a2a2acc")
                        button:
                            xysize (68, 71)
                            xpos 62 + _col * 70
                            ypos _row * 73
                            action (NullAction() if _rou_locked else Return(("add_bet", "number", _n)))
                            sensitive (not _rou_locked)
                            background _base_bg
                            hover_background (_base_bg if _rou_locked else _hov_bg)
                            text str(_n):
                                xalign 0.5 yalign 0.5
                                font PROFILE_FONT size 19 color "#f0f0f0"

                # Dozens row
                for _di, (_dl, _dt) in enumerate([("1st 12","doz1"),("2nd 12","doz2"),("3rd 12","doz3")]):
                    button:
                        xysize (276, 46)
                        xpos 62 + _di * 278
                        ypos 222
                        action (NullAction() if _rou_locked else Return(("add_bet", _dt)))
                        sensitive (not _rou_locked)
                        background "#141a10cc"
                        hover_background ("#141a10cc" if _rou_locked else "#243010cc")
                        text _dl:
                            xalign 0.5 yalign 0.5
                            font PROFILE_FONT size 15 color "#cccccc"

                # Outside bets row
                for _oi, (_ol, _ot, _obg, _ohov) in enumerate([
                    ("1–18",  "low",   "#111111cc","#222222cc"),
                    ("EVEN",  "even",  "#111111cc","#222222cc"),
                    ("RED",   "red",   "#4a1010cc","#6a1818cc"),
                    ("BLACK", "black", "#101010cc","#2a2a2acc"),
                    ("ODD",   "odd",   "#111111cc","#222222cc"),
                    ("19–36", "high",  "#111111cc","#222222cc"),
                ]):
                    button:
                        xysize (138, 46)
                        xpos 62 + _oi * 140
                        ypos 272
                        action (NullAction() if _rou_locked else Return(("add_bet", _ot)))
                        sensitive (not _rou_locked)
                        background _obg
                        hover_background (_obg if _rou_locked else _ohov)
                        text _ol:
                            xalign 0.5 yalign 0.5
                            font PROFILE_FONT size 15 color "#f0f0f0"

                # ── Chip overlay layer: show chips directly on positions ───
                # Zero
                if rou_game.bet_on("number", 0):
                    fixed xpos 0 ypos 0 xsize 58 ysize 219:
                        $ _zchips = rou_game.bet_chips_on("number", 0)
                        frame xalign 0.5 yalign 0.5 background "#00000000" padding(0,0,0,0):
                            use casino_chip_stack(_zchips, compact=True)

                # Numbers
                for _col in range(12):
                    for _row in range(3):
                        $ _n = _col * 3 + (3 - _row)
                        if rou_game.bet_on("number", _n):
                            $ _ncx = 62 + _col * 70
                            $ _ncy = _row * 73
                            fixed xpos _ncx ypos _ncy xsize 68 ysize 71:
                                $ _nchips = rou_game.bet_chips_on("number", _n)
                                frame xalign 0.5 yalign 0.5 background "#00000000" padding(0,0,0,0):
                                    use casino_chip_stack(_nchips, compact=True)

                # Dozens
                for _di, (_dl2, _dt2) in enumerate([("1st 12","doz1"),("2nd 12","doz2"),("3rd 12","doz3")]):
                    if rou_game.bet_on(_dt2):
                        $ _dcx = 62 + _di * 278
                        fixed xpos _dcx ypos 222 xsize 276 ysize 46:
                            $ _dchips = rou_game.bet_chips_on(_dt2)
                            frame xalign 0.5 yalign 0.5 background "#00000000" padding(0,0,0,0):
                                use casino_chip_stack(_dchips, compact=True)

                # Outside
                for _oi2, (_ol2, _ot2) in enumerate([
                    ("1–18","low"),("EVEN","even"),("RED","red"),
                    ("BLACK","black"),("ODD","odd"),("19–36","high")
                ]):
                    if rou_game.bet_on(_ot2):
                        $ _ocx = 62 + _oi2 * 140
                        fixed xpos _ocx ypos 272 xsize 138 ysize 46:
                            $ _ochips = rou_game.bet_chips_on(_ot2)
                            frame xalign 0.5 yalign 0.5 background "#00000000" padding(0,0,0,0):
                                use casino_chip_stack(_ochips, compact=True)

                # ── Chip tray (below the table) ───────────────────────────
                text "SELECT CHIP":
                    xpos 0 ypos 332
                    font ACT_FONT size 13 color "#6a8a6a"
                hbox:
                    xpos 0 ypos 352 spacing 14
                    for _camt2, _ckey2 in _CHIPS:
                        $ _csel = (rou_game.chip_amt == _camt2)
                        button:
                            xysize (72, 72)
                            background None hover_background None
                            action (NullAction() if _rou_locked else Return(("set_chip", _camt2)))
                            sensitive (not _rou_locked)
                            at (_chip_selected if _csel else _chip_idle)
                            add _chip_img(_camt2) xysize (72, 72)
                            if _csel:
                                frame:
                                    xfill True yfill True
                                    background "#00000000"
                                    foreground Frame("images/ui/act_bar_hover_clean.png", 8, 8)

                # Total bet + clear
                hbox:
                    xpos 0 ypos 440 spacing 16
                    text ("Total  $%d" % rou_game.total_bet()):
                        font PROFILE_FONT size 20 color "#d4af37" yalign 0.5
                    if rou_game.bets and not _rou_locked:
                        textbutton "Clear All":
                            action Return("clear_bets")
                            background Frame("images/ui/act_bar_idle.png", 16, 16)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 16, 16)
                            padding (14, 6, 14, 6)
                            text_font ACT_FONT text_size 15
                            text_color "#cc6060" text_hover_color "#ffffff"

                # Active bets list (compact summary)
                if rou_game.bets:
                    viewport:
                        xpos 0 ypos 478
                        xsize 896 ysize 160
                        mousewheel True
                        vbox:
                            spacing 4
                            for _sb in rou_game.bets:
                                $ _sbt = _sb["type"]
                                $ _sbn = _sb.get("num")
                                $ _sba = _sb["amt"]
                                $ _sbk = ("No. %d" % _sbn if _sbt == "number" else _sbt.upper())
                                hbox:
                                    spacing 10
                                    text ("· %s" % _sbk):
                                        font ACT_FONT size 15 color "#cccccc" yalign 0.5 xsize 130
                                    text ("$%d" % _sba):
                                        font PROFILE_FONT size 15 color "#d4af37" yalign 0.5
                                    if not _rou_locked:
                                        textbutton "✕":
                                            action Return(("remove_bet", _sbt, _sbn))
                                            background None hover_background None
                                            padding (4, 0, 4, 0)
                                            text_font ACT_FONT text_size 14
                                            text_color "#664444" text_hover_color "#cc4444"

            # ── Right: Wheel + result + spin ─────────────────────────────
            frame:
                xpos 920 ypos 0
                xsize 620 ysize 822
                background "#111111dd"
                padding (28, 24, 28, 24)

                # Wheel — 360×360
                fixed xalign 0.5 ypos 0 xsize 564 ysize 370:
                    fixed xalign 0.5 yalign 0.0 xsize 360 ysize 360:
                        if rou_game.phase == "spinning":
                            add Transform("images/ui/roulette_wheel_transparent.png", size=(360,360)) at _rou_spin_anim
                        elif rou_game.result is not None:
                            add Transform("images/ui/roulette_wheel_transparent.png", size=(360,360)) at _rou_static(rou_game.result * 137)
                        else:
                            add Transform("images/ui/roulette_wheel_transparent.png", size=(360,360)) at _rou_static(0)
                    # Result badge centered on wheel
                    if rou_game.result is not None:
                        $ _rn  = rou_game.result
                        $ _rbc = ("#145214" if _rn == 0 else ("#5a1010" if _rn in _ROU_REDS else "#111111"))
                        frame:
                            xalign 0.5 ypos 148
                            xysize (76, 76)
                            background _rbc
                            text str(_rn):
                                xalign 0.5 yalign 0.5
                                font PROFILE_FONT size 32 color "#ffffff"

                # Result message
                if rou_game.msg:
                    text rou_game.msg:
                        xalign 0.5 ypos 382
                        font PROFILE_FONT size 24 color "#f0d060"
                        xmaximum 560 text_align 0.5

                # Spin / result controls
                if rou_game.phase == "betting":
                    textbutton "SPIN":
                        xalign 0.5 ypos 680
                        action Return("spin")
                        background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                        hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                        padding (60, 16, 60, 16)
                        text_font PROFILE_FONT text_size 32 text_color "#d4af37" text_hover_color "#ffffff"
                elif rou_game.phase == "spinning":
                    text "Spinning…":
                        xalign 0.5 ypos 700
                        font PROFILE_FONT size 24 color "#d4af37"
                else:
                    hbox:
                        xalign 0.5 ypos 680 spacing 16
                        textbutton "Spin Again":
                            action Return("reset")
                            background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                            padding (24, 12, 24, 12)
                            text_font PROFILE_FONT text_size 19 text_color "#d4af37" text_hover_color "#ffffff"
                        textbutton "Back to Casino":
                            action Return("back")
                            background Frame("images/ui/act_bar_idle.png", 20, 20)
                            hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                            padding (20, 12, 20, 12)
                            text_font ACT_FONT text_size 17 text_color "#9ab89a" text_hover_color "#ffffff"
