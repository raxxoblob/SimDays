# casino.rpy — Blackjack + Roulette
# Cards: images/ui/cards_cropped_53/ (126×187 px, ~2:3)
# Displayed at CARD_W×CARD_H; back uses old cards/card_back.png.

init python:
    CARD_W = 105
    CARD_H = 156

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

    # Chip denominations: (label, amount, fill_color, text_color)
    _CHIPS = [
        ("5",     5,    "#e8e8e8", "#111"),
        ("25",   25,    "#2a8a2a", "#fff"),
        ("100",  100,   "#111111", "#fff"),
        ("250",  250,   "#7b3fa0", "#fff"),
        ("500",  500,   "#c8a000", "#111"),
    ]

    # ── Blackjack ─────────────────────────────────────────────────────────────
    class _BJ:
        def __init__(self):
            self.deck     = _bj_new_deck()
            self.player   = []
            self.dealer   = []
            self.bet      = 25
            self.hand_bet = 25
            self.phase    = "betting"   # betting | playing | result
            self.msg      = ""

        def new_game(self):
            if len(self.deck) < 15:
                self.deck = _bj_new_deck()
            self.player   = []
            self.dealer   = []
            self.phase    = "betting"
            self.msg      = ""
            self.hand_bet = self.bet

        def add_chip(self, amt):
            self.bet = min(2000, self.bet + amt)

        def clear_bet(self):
            self.bet = 0

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
            self.result   = None
            self.bets     = []   # list of {"type":str, "num":int|None, "amt":int}
            self.chip_amt = 25   # currently selected chip denomination
            self.msg      = ""
            self.phase    = "betting"
            self._pending = 0

        def _find_bet(self, bet_type, num):
            for b in self.bets:
                if b["type"] == bet_type and b.get("num") == num:
                    return b
            return None

        def add_bet(self, bet_type, num=None):
            existing = self._find_bet(bet_type, num)
            if existing:
                existing["amt"] += self.chip_amt
            else:
                self.bets.append({"type": bet_type, "num": num, "amt": self.chip_amt})

        def remove_bet(self, bet_type, num=None):
            self.bets = [b for b in self.bets
                         if not (b["type"] == bet_type and b.get("num") == num)]

        def total_bet(self):
            return sum(b["amt"] for b in self.bets)

        def clear_bets(self):
            self.bets = []

        def bet_on(self, bet_type, num=None):
            """Amount staked on this exact position (0 if none)."""
            b = self._find_bet(bet_type, num)
            return b["amt"] if b else 0

        def start_spin(self):
            if not self.bets:
                self.msg = "Place at least one bet."; return False
            if not try_spend(self.total_bet(), category="gambling", toast=False):
                self.msg = "Not enough money."; return False
            self._pending = renpy.random.randint(0, 36)
            self.result   = None
            self.msg      = ""
            self.phase    = "spinning"
            return True

        def finish_spin(self):
            n      = self._pending
            self.result = n
            red    = (n in _ROU_REDS)
            staked = self.total_bet()
            returned = 0
            for b in self.bets:
                bt, ba, bn = b["type"], b["amt"], b.get("num")
                mult = 0
                if   bt == "red"    and n != 0 and red:        mult = 2
                elif bt == "black"  and n != 0 and not red:    mult = 2
                elif bt == "even"   and n != 0 and n % 2 == 0: mult = 2
                elif bt == "odd"    and n % 2 == 1:            mult = 2
                elif bt == "low"    and 1 <= n <= 18:          mult = 2
                elif bt == "high"   and 19 <= n <= 36:         mult = 2
                elif bt == "doz1"   and 1 <= n <= 12:          mult = 3
                elif bt == "doz2"   and 13 <= n <= 24:         mult = 3
                elif bt == "doz3"   and 25 <= n <= 36:         mult = 3
                elif bt == "number" and n == bn:               mult = 37
                returned += ba * mult
            if returned:
                store.money += returned
                self.msg = "No. %d  —  +$%d!" % (n, returned - staked)
            else:
                self.msg = "No. %d  —  -$%d" % (n, staked)
            self.phase = "result"

        def reset(self):
            self.result = None
            self.msg    = ""
            self.phase  = "betting"
            self.bets   = []

    bj_game  = _BJ()
    rou_game = _Rou()


# ── Entry ──────────────────────────────────────────────────────────────────────

label location_casino:
    $ current_loc = "location_casino"
    if hour < 20 and hour >= 4:
        "The casino doesn't open until 8 PM."
        jump location_nadbrzeze
    if stat_chr < 25:
        "The doorman barely glances at you. \"Members and guests only.\" He doesn't move."
        jump location_nadbrzeze
    scene casino_night
    show screen hud
    $ bj_game.new_game()
    jump casino_blackjack_loop

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
    elif _return == "roulette":
        $ rou_game.reset()
        jump casino_roulette_loop
    elif _return == "leave":
        jump location_nadbrzeze
    jump casino_blackjack_loop

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
    elif _return == "blackjack":
        $ bj_game.new_game()
        jump casino_blackjack_loop
    elif _return == "leave":
        jump location_nadbrzeze
    jump casino_roulette_loop


# ── Shared left sidebar ────────────────────────────────────────────────────────
# Used as `use casino_sidebar(active)` inside both game screens.
# active: "blackjack" | "roulette"

screen casino_sidebar(active):
    frame:
        xpos 0 ypos 0
        xsize 210 ysize 1080
        background "#0d0f0eee"
        padding (14, 30, 14, 20)
        vbox:
            spacing 0
            # Casino logo / title
            text "CASINO" xalign 0.5 font PROFILE_FONT size 28 color "#d4af37"
            null height 4
            text "ROYAL" xalign 0.5 font PROFILE_FONT size 13 color "#a07820"
            null height 20
            # Balance
            frame:
                xfill True
                background "#1a2a1a"
                padding (10, 8, 10, 8)
                vbox:
                    spacing 2
                    text "BALANCE" xalign 0.5 font PROFILE_FONT size 11 color "#5a8a5a"
                    text "$[money]" xalign 0.5 font PROFILE_FONT size 22 color "#7fd06a"
            null height 30
            # Game tabs
            text "GAMES" xalign 0.5 font PROFILE_FONT size 11 color "#5a6a5a"
            null height 8
            textbutton "♠ Blackjack":
                xfill True
                action (NullAction() if active == "blackjack" else Return("blackjack"))
                background ("#1a3a1a" if active == "blackjack" else "#111811")
                hover_background "#1a3a1a"
                padding (10, 10, 10, 10)
                text_font PROFILE_FONT text_size 16
                text_color ("#d4af37" if active == "blackjack" else "#9ab89a")
                text_hover_color "#d4af37"
            null height 6
            textbutton "◉ Roulette":
                xfill True
                action (NullAction() if active == "roulette" else Return("roulette"))
                background ("#1a3a1a" if active == "roulette" else "#111811")
                hover_background "#1a3a1a"
                padding (10, 10, 10, 10)
                text_font PROFILE_FONT text_size 16
                text_color ("#d4af37" if active == "roulette" else "#9ab89a")
                text_hover_color "#d4af37"
            null height 40
            # Leave
            textbutton "← Leave":
                xfill True
                action Return("leave")
                background "#0d0f0e"
                hover_background "#1a1a1a"
                padding (10, 8, 10, 8)
                text_font ACT_FONT text_size 15
                text_color "#5a6a5a" text_hover_color "#9ab89a"



# ── Blackjack screen ───────────────────────────────────────────────────────────

screen casino_blackjack():
    add "casino_night"
    use casino_sidebar("blackjack")

    # ── Main table area (x 210 → 1920) ────────────────────────────────────────
    frame:
        xpos 210 ypos 0
        xsize 1710 ysize 1080
        background "#00000000"
        padding (0, 0, 0, 0)

        # Green felt
        frame:
            xalign 0.5 yalign 0.5
            xsize 1300 ysize 820
            background "#0a2a0a"
            padding (0, 0, 0, 0)

            # ── DEALER section ─────────────────────────────────────────────────
            text "DEALER" xalign 0.5 ypos 24 font PROFILE_FONT size 14 color "#3a7a3a"

            # dealer total (hidden during play)
            if bj_game.dealer and bj_game.phase != "playing":
                $ _dt = _bj_total(bj_game.dealer)
                $ _dt_col = ("#e05050" if _dt > 21 else "#ffffff")
                text str(_dt) xalign 0.5 ypos 52 font PROFILE_FONT size 30 color _dt_col

            # dealer cards centred
            fixed xalign 0.5 ypos 90 xsize 800 ysize 170:
                if bj_game.dealer:
                    $ _dw = len(bj_game.dealer) * CARD_W + (len(bj_game.dealer)-1) * 10
                    hbox:
                        xpos max(0, (800 - _dw) // 2)
                        spacing 10
                        for _di, (_dr, _ds) in enumerate(bj_game.dealer):
                            if _di == 1 and bj_game.phase == "playing":
                                add _CARD_BACK xysize (CARD_W, CARD_H)
                            else:
                                add _card_img(_dr, _ds) xysize (CARD_W, CARD_H)

            # ── Centre divider ─────────────────────────────────────────────────
            frame:
                xalign 0.5 ypos 290
                xsize 900 ysize 2
                background "#1a4a1a"

            # BET DISPLAY centred
            if bj_game.phase == "betting":
                frame:
                    xalign 0.5 ypos 310
                    xsize 220 ysize 60
                    background "#0d200d"
                    padding (12, 8, 12, 8)
                    hbox:
                        xalign 0.5 spacing 12 yalign 0.5
                        text "BET" font PROFILE_FONT size 14 color "#5a8a5a" yalign 0.5
                        text ("$%d" % bj_game.bet) font PROFILE_FONT size 26 color "#d4af37" yalign 0.5
                        if bj_game.bet > 0:
                            textbutton "✕":
                                action Return("clear_bet")
                                background None hover_background None
                                text_font PROFILE_FONT text_size 18
                                text_color "#883333" text_hover_color "#cc4444"
                                yalign 0.5

            # ── PLAYER section ─────────────────────────────────────────────────
            # player cards centred
            fixed xalign 0.5 ypos 400 xsize 800 ysize 170:
                if bj_game.player:
                    $ _pw = len(bj_game.player) * CARD_W + (len(bj_game.player)-1) * 10
                    hbox:
                        xpos max(0, (800 - _pw) // 2)
                        spacing 10
                        for _pr, _ps in bj_game.player:
                            add _card_img(_pr, _ps) xysize (CARD_W, CARD_H)

            if bj_game.player:
                $ _pt = _bj_total(bj_game.player)
                $ _pt_col = ("#e05050" if _pt > 21 else ("#d4af37" if _pt == 21 else "#ffffff"))
                text str(_pt) xalign 0.5 ypos 574 font PROFILE_FONT size 30 color _pt_col

            text "YOU" xalign 0.5 ypos 612 font PROFILE_FONT size 14 color "#3a7a3a"

            # ── Message ────────────────────────────────────────────────────────
            if bj_game.msg:
                text bj_game.msg xalign 0.5 ypos 650 font PROFILE_FONT size 26 color "#f0d060"

            # ── Controls ───────────────────────────────────────────────────────
            if bj_game.phase == "betting":
                # Chip strip — centred on the felt
                hbox:
                    xalign 0.5 ypos 695 spacing 10
                    for _clbl, _camt, _cfill, _ctxt in _CHIPS:
                        button:
                            xysize (64, 56)
                            background Solid(_cfill)
                            hover_background Solid(_cfill)
                            action Return(("chip", _camt))
                            text ("$" + _clbl) xalign 0.5 yalign 0.5 font PROFILE_FONT size 13 color _ctxt

                textbutton "DEAL":
                    xalign 0.5 ypos 762
                    action Return("deal")
                    background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                    hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                    padding (40, 12, 40, 12)
                    text_font PROFILE_FONT text_size 28 text_color "#d4af37" text_hover_color "#ffffff"

            elif bj_game.phase == "playing":
                hbox:
                    xalign 0.5 ypos 720 spacing 20

                    textbutton "HIT":
                        action Return("hit")
                        background "#1a3a1a"
                        hover_background "#2a5a2a"
                        padding (28, 12, 28, 12)
                        text_font PROFILE_FONT text_size 24 text_color "#d4af37" text_hover_color "#ffffff"

                    textbutton "STAND":
                        action Return("stand")
                        background "#3a1a1a"
                        hover_background "#5a2a2a"
                        padding (28, 12, 28, 12)
                        text_font PROFILE_FONT text_size 24 text_color "#e08080" text_hover_color "#ffffff"

                    if money >= bj_game.hand_bet and len(bj_game.player) == 2:
                        textbutton "DOUBLE":
                            action Return("double")
                            background "#1a1a3a"
                            hover_background "#2a2a5a"
                            padding (22, 12, 22, 12)
                            text_font PROFILE_FONT text_size 22 text_color "#80a0e0" text_hover_color "#ffffff"

            elif bj_game.phase == "result":
                hbox:
                    xalign 0.5 ypos 730 spacing 20
                    textbutton "Play Again":
                        action Return("new_game")
                        background "#1a3a1a" hover_background "#2a5a2a"
                        padding (24, 10, 24, 10)
                        text_font PROFILE_FONT text_size 22 text_color "#d4af37" text_hover_color "#ffffff"
                    textbutton "Roulette":
                        action Return("roulette")
                        background "#1a1a3a" hover_background "#2a2a5a"
                        padding (20, 10, 20, 10)
                        text_font ACT_FONT text_size 18 text_color "#9ab8e0" text_hover_color "#ffffff"


# ── Roulette screen ────────────────────────────────────────────────────────────

transform _rou_spin_anim:
    rotate 0.0
    linear 2.5 rotate 1440.0

transform _rou_static(angle):
    rotate angle

screen casino_roulette():
    if rou_game.phase == "spinning":
        timer 2.5 action Return("spin_done")

    add "casino_night"
    use casino_sidebar("roulette")

    # ── Main area x=210 ───────────────────────────────────────────────────────
    frame:
        xpos 218 ypos 30
        xsize 1680 ysize 1020
        background "#00000000"
        padding (0, 0, 0, 0)

        # ── Betting table (left 1060px) ────────────────────────────────────────
        frame:
            xpos 0 ypos 0
            xsize 1060 ysize 700
            background "#0a2a0a"
            padding (12, 12, 12, 12)

            # 0 — green cell
            $ _b0 = rou_game.bet_on("number", 0)
            button:
                xysize (52, 213)
                xpos 0 ypos 0
                action Return(("add_bet", "number", 0))
                background ("#145214" if not _b0 else "#1e7a1e")
                hover_background "#1e7a1e"
                vbox:
                    xalign 0.5 yalign 0.5
                    text "0" xalign 0.5 yalign 0.5 font PROFILE_FONT size 20 color "#ffffff"
                    if _b0:
                        text ("$%d" % _b0) xalign 0.5 font ACT_FONT size 11 color "#d4af37"

            # Numbers 1–36: col 0-11, row 0-2  → n = col*3 + (3-row)
            for _col in range(12):
                for _row in range(3):
                    $ _n   = _col * 3 + (3 - _row)
                    $ _bn  = rou_game.bet_on("number", _n)
                    $ _red = (_n in _ROU_REDS)
                    $ _base_bg = ("#4a1010" if _red else "#0f0f0f")
                    $ _sel_bg  = ("#7a2020" if _red else "#2a2a2a")
                    button:
                        xysize (78, 69)
                        xpos 58 + _col * 82
                        ypos _row * 72
                        action Return(("add_bet", "number", _n))
                        background (_sel_bg if _bn else _base_bg)
                        hover_background _sel_bg
                        vbox:
                            xalign 0.5 yalign 0.5
                            text str(_n) xalign 0.5 yalign 0.5 font PROFILE_FONT size 18 color "#ffffff"
                            if _bn:
                                text ("$%d" % _bn) xalign 0.5 font ACT_FONT size 11 color "#d4af37"

            # Dozens row
            for _di, (_dl, _dt) in enumerate([("1st 12","doz1"),("2nd 12","doz2"),("3rd 12","doz3")]):
                $ _bd = rou_game.bet_on(_dt)
                button:
                    xysize (328, 46)
                    xpos 58 + _di * 332
                    ypos 218
                    action Return(("add_bet", _dt))
                    background ("#2a3a1a" if _bd else "#151515")
                    hover_background "#2a3a1a"
                    hbox:
                        xalign 0.5 yalign 0.5 spacing 8
                        text _dl xalign 0.5 yalign 0.5 font PROFILE_FONT size 14 color "#cccccc"
                        if _bd:
                            text ("$%d" % _bd) font ACT_FONT size 12 color "#d4af37" yalign 0.5

            # Outside bets row
            for _oi, (_ol, _ot, _obg, _ohov) in enumerate([
                ("1-18",  "low",   "#111","#222"),
                ("EVEN",  "even",  "#111","#222"),
                ("RED",   "red",   "#4a1010","#7a2020"),
                ("BLACK", "black", "#0f0f0f","#2a2a2a"),
                ("ODD",   "odd",   "#111","#222"),
                ("19-36", "high",  "#111","#222"),
            ]):
                $ _bo = rou_game.bet_on(_ot)
                button:
                    xysize (160, 46)
                    xpos 58 + _oi * 164
                    ypos 270
                    action Return(("add_bet", _ot))
                    background (_ohov if _bo else _obg)
                    hover_background _ohov
                    hbox:
                        xalign 0.5 yalign 0.5 spacing 6
                        text _ol xalign 0.5 yalign 0.5 font PROFILE_FONT size 14 color "#ffffff"
                        if _bo:
                            text ("$%d" % _bo) font ACT_FONT size 12 color "#d4af37" yalign 0.5

            # ── Chip selector ──────────────────────────────────────────────────
            text "CHIP" xpos 0 ypos 334 font PROFILE_FONT size 12 color "#5a8a5a"
            hbox:
                xpos 0 ypos 352
                spacing 8
                for _clbl, _camt, _cfill, _ctxt in _CHIPS:
                    $ _csel = (rou_game.chip_amt == _camt)
                    button:
                        xysize (70, 60)
                        background Solid(_cfill)
                        hover_background Solid(_cfill)
                        action Return(("set_chip", _camt))
                        vbox:
                            xalign 0.5 yalign 0.5
                            text ("$" + _clbl) xalign 0.5 yalign 0.5 font PROFILE_FONT size 14 color _ctxt
                        if _csel:
                            frame:
                                xysize (70, 60)
                                background "#00000000"
                                foreground Frame("images/ui/act_bar_idle.png", 5, 5)

            # total bet + clear
            hbox:
                xpos 0 ypos 430 spacing 16
                text ("Total bet: $%d" % rou_game.total_bet()) font PROFILE_FONT size 18 color "#d4af37" yalign 0.5
                if rou_game.bets:
                    textbutton "Clear":
                        action Return("clear_bets")
                        background "#2a1010" hover_background "#4a1010"
                        padding (12, 6, 12, 6)
                        text_font ACT_FONT text_size 15 text_color "#cc6060" text_hover_color "#ffffff"

        # ── Right panel: wheel + controls (x=1080) ────────────────────────────
        frame:
            xpos 1080 ypos 0
            xsize 580 ysize 700
            background "#0d0d0d"
            padding (24, 24, 24, 24)

            # Wheel
            fixed xalign 0.5 ypos 0 xsize 532 ysize 260:
                fixed xalign 0.5 yalign 0.0 xsize 240 ysize 240:
                    if rou_game.phase == "spinning":
                        add Transform("images/ui/roulette_wheel_transparent.png", size=(240,240)) at _rou_spin_anim
                    elif rou_game.result is not None:
                        add Transform("images/ui/roulette_wheel_transparent.png", size=(240,240)) at _rou_static(rou_game.result * 137)
                    else:
                        add Transform("images/ui/roulette_wheel_transparent.png", size=(240,240)) at _rou_static(0)
                # result badge in centre
                if rou_game.result is not None:
                    $ _rn  = rou_game.result
                    $ _rbc = ("#145214" if _rn == 0 else ("#5a1010" if _rn in _ROU_REDS else "#0f0f0f"))
                    frame:
                        xalign 0.5 ypos 88
                        xysize (64, 64)
                        background _rbc
                        text str(_rn) xalign 0.5 yalign 0.5 font PROFILE_FONT size 28 color "#ffffff"

            # Message
            if rou_game.msg:
                text rou_game.msg xalign 0.5 ypos 268 font PROFILE_FONT size 22 color "#f0d060" xmaximum 530

            # Active bets summary
            if rou_game.bets:
                null height 0
                viewport:
                    xpos 0 ypos 310
                    xsize 530 ysize 200
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
                                text ("· %s" % _sbk) font ACT_FONT size 15 color "#cccccc" yalign 0.5 xsize 160
                                text ("$%d" % _sba) font PROFILE_FONT size 15 color "#d4af37" yalign 0.5
                                textbutton "✕":
                                    action Return(("remove_bet", _sbt, _sbn))
                                    background None hover_background None
                                    padding (4, 0, 4, 0)
                                    text_font ACT_FONT text_size 14
                                    text_color "#664444" text_hover_color "#cc4444"

            # Spin / result buttons
            if rou_game.phase == "betting":
                textbutton "SPIN":
                    xalign 0.5 ypos 530
                    action Return("spin")
                    background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                    hover_background Frame("images/ui/act_bar_hover_clean.png", 20, 20)
                    padding (50, 14, 50, 14)
                    text_font PROFILE_FONT text_size 32 text_color "#d4af37" text_hover_color "#ffffff"
            elif rou_game.phase == "spinning":
                text "Spinning..." xalign 0.5 ypos 544 font PROFILE_FONT size 24 color "#d4af37"
            else:
                hbox:
                    xalign 0.5 ypos 530 spacing 16
                    textbutton "Spin Again":
                        action Return("reset")
                        background "#1a3a1a" hover_background "#2a5a2a"
                        padding (20, 10, 20, 10)
                        text_font PROFILE_FONT text_size 20 text_color "#d4af37" text_hover_color "#ffffff"
                    textbutton "Blackjack":
                        action Return("blackjack")
                        background "#1a1a3a" hover_background "#2a2a5a"
                        padding (16, 10, 16, 10)
                        text_font ACT_FONT text_size 17 text_color "#9ab8e0" text_hover_color "#ffffff"
