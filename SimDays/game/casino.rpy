# casino.rpy — Blackjack + Roulette

init python:
    _BJ_RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    _BJ_SUITS = ["♠","♥","♦","♣"]
    _SUIT_KEY  = {"♣":"c","♥":"h","♠":"s","♦":"d"}

    def _card_img(rank, suit):
        return "images/ui/cards/card_%s_%s.png" % (_SUIT_KEY[suit], rank)

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
            t -= 10
            a -= 1
        return t

    _ROU_REDS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}

    class _BJ:
        def __init__(self):
            self.deck   = _bj_new_deck()
            self.player = []
            self.dealer = []
            self.bet    = 25
            self.phase  = "betting"   # betting | playing | result
            self.msg    = ""

        def new_game(self):
            if len(self.deck) < 15:
                self.deck = _bj_new_deck()
            self.player = []
            self.dealer = []
            self.phase  = "betting"
            self.msg    = ""

        def deal(self):
            if self.bet > store.money:
                self.msg = "Not enough money."; return
            store.money -= self.bet
            self.player = [self.deck.pop(), self.deck.pop()]
            self.dealer = [self.deck.pop(), self.deck.pop()]
            self.phase  = "playing"
            if _bj_total(self.player) == 21:
                self._finish()

        def hit(self):
            self.player.append(self.deck.pop())
            if _bj_total(self.player) > 21:
                self.msg = "Bust!"; self.phase = "result"

        def stand(self):
            while _bj_total(self.dealer) < 17:
                self.dealer.append(self.deck.pop())
            self._finish()

        def double_down(self):
            if self.bet > store.money:
                self.msg = "Not enough to double."; return
            store.money -= self.bet
            self.bet    *= 2
            self.player.append(self.deck.pop())
            if _bj_total(self.player) > 21:
                self.msg = "Bust after double!"; self.phase = "result"
            else:
                self.stand()

        def _finish(self):
            pt  = _bj_total(self.player)
            dt  = _bj_total(self.dealer)
            nat = (pt == 21 and len(self.player) == 2)
            if pt > 21:
                self.msg = "Bust. Lost $%d." % self.bet
            elif dt > 21 or pt > dt:
                gain = int(self.bet * 1.5) if nat else self.bet
                store.money += self.bet + gain
                self.msg = ("Blackjack! +$%d" if nat else "You win! +$%d") % gain
            elif pt == dt:
                store.money += self.bet
                self.msg = "Push — bet returned."
            else:
                self.msg = "Dealer wins. Lost $%d." % self.bet
            self.phase = "result"

    class _Rou:
        def __init__(self):
            self.result   = None
            self.bet_type = "red"
            self.bet_num  = 7
            self.bet_amt  = 25
            self.msg      = ""
            self.phase    = "betting"   # betting | spinning | result
            self._pending = 0           # drawn number, revealed after animation

        def start_spin(self):
            if self.bet_amt > store.money:
                self.msg = "Not enough money."; return
            store.money -= self.bet_amt
            self._pending = renpy.random.randint(0, 36)
            self.result   = None
            self.msg      = ""
            self.phase    = "spinning"

        def finish_spin(self):
            n   = self._pending
            self.result = n
            red = (n in _ROU_REDS)
            win = 0
            bt  = self.bet_type
            if   bt == "red"    and n != 0 and red:         win = self.bet_amt
            elif bt == "black"  and n != 0 and not red:     win = self.bet_amt
            elif bt == "even"   and n != 0 and n % 2 == 0:  win = self.bet_amt
            elif bt == "odd"    and n % 2 == 1:              win = self.bet_amt
            elif bt == "low"    and 1 <= n <= 18:            win = self.bet_amt
            elif bt == "high"   and 19 <= n <= 36:           win = self.bet_amt
            elif bt == "doz1"   and 1 <= n <= 12:            win = self.bet_amt * 2
            elif bt == "doz2"   and 13 <= n <= 24:           win = self.bet_amt * 2
            elif bt == "doz3"   and 25 <= n <= 36:           win = self.bet_amt * 2
            elif bt == "number" and n == self.bet_num:       win = self.bet_amt * 35
            if win:
                store.money += self.bet_amt + win
                self.msg = "Number %d — Win $%d!" % (n, win)
            else:
                self.msg = "Number %d — Lose $%d." % (n, self.bet_amt)
            self.phase = "result"

        def reset(self):
            self.result   = None
            self.msg      = ""
            self.phase    = "betting"

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
    jump casino_hub_label

label casino_hub_label:
    call screen casino_hub
    if _return == "blackjack":
        $ bj_game.new_game()
        jump casino_blackjack_loop
    elif _return == "roulette":
        $ rou_game.reset()
        jump casino_roulette_loop
    else:
        jump location_nadbrzeze

label casino_blackjack_loop:
    call screen casino_blackjack
    if   _return == "bet_up":   $ bj_game.bet = min(500, bj_game.bet + 25)
    elif _return == "bet_down": $ bj_game.bet = max(5,   bj_game.bet - 25)
    elif _return == "deal":     $ bj_game.deal()
    elif _return == "hit":      $ bj_game.hit()
    elif _return == "stand":    $ bj_game.stand()
    elif _return == "double":   $ bj_game.double_down()
    elif _return == "new_game": $ bj_game.new_game()
    elif _return == "roulette":
        $ rou_game.reset()
        jump casino_roulette_loop
    elif _return == "hub":   jump casino_hub_label
    elif _return == "leave": jump location_nadbrzeze
    jump casino_blackjack_loop

label casino_roulette_loop:
    call screen casino_roulette
    if isinstance(_return, tuple):
        if   _return[0] == "bet_num":
            $ rou_game.bet_num  = _return[1]
            $ rou_game.bet_type = "number"
        elif _return[0] == "bet_type":
            $ rou_game.bet_type = _return[1]
    elif _return == "bet_up":    $ rou_game.bet_amt = min(1000, rou_game.bet_amt + 25)
    elif _return == "bet_down":  $ rou_game.bet_amt = max(5,    rou_game.bet_amt - 25)
    elif _return == "spin":      $ rou_game.start_spin()
    elif _return == "spin_done": $ rou_game.finish_spin()
    elif _return == "reset":     $ rou_game.reset()
    elif _return == "blackjack":
        $ bj_game.new_game()
        jump casino_blackjack_loop
    elif _return == "hub":   jump casino_hub_label
    elif _return == "leave": jump location_nadbrzeze
    jump casino_roulette_loop


# ── Screens ───────────────────────────────────────────────────────────────────

screen casino_hub():
    add "casino_night"
    frame:
        background "#000000bb"
        xalign 0.5 yalign 0.5
        xysize (440, 360)
        padding (50, 40, 50, 40)
        vbox:
            spacing 18
            xalign 0.5
            text "CASINO" xalign 0.5 size 44 color "#d4af37" font PROFILE_FONT
            text "Balance: $[money]" xalign 0.5 size 22 color "#ccffcc"
            null height 10
            textbutton "Blackjack" action Return("blackjack") xalign 0.5 text_size 24 text_font PROFILE_FONT
            textbutton "Roulette"  action Return("roulette")  xalign 0.5 text_size 24 text_font PROFILE_FONT
            textbutton "Leave"     action Return("leave")     xalign 0.5 text_size 20 text_color "#888888"


screen casino_blackjack():
    add "casino_night"
    frame:
        background "#000000bb"
        xalign 0.5 yalign 0.5
        xysize (1280, 660)
        padding (30, 20, 30, 20)

        # Top bar
        text "BLACKJACK" xalign 0.5 ypos 8 size 30 color "#d4af37" font PROFILE_FONT
        text "Balance: $[money]" xpos 20 ypos 12 size 18 color "#aaffaa"
        textbutton "← Back" action Return("hub") xpos 1140 ypos 8 text_size 16 text_color "#888888"

        # Dealer
        text "Dealer" xpos 20 ypos 58 size 16 color "#777777"
        if bj_game.dealer:
            hbox xpos 110 ypos 72 spacing 6:
                for _i, (_r, _s) in enumerate(bj_game.dealer):
                    if _i == 1 and bj_game.phase == "playing":
                        add "images/ui/cards/card_back.png" xysize (90, 126)
                    else:
                        add _card_img(_r, _s) xysize (90, 126)
            if bj_game.phase != "playing":
                text str(_bj_total(bj_game.dealer)) xpos 20 ypos 120 size 24 color "#ffffff"

        # Player
        text "You" xpos 20 ypos 278 size 16 color "#777777"
        if bj_game.player:
            hbox xpos 110 ypos 295 spacing 6:
                for _r, _s in bj_game.player:
                    add _card_img(_r, _s) xysize (90, 126)
            text str(_bj_total(bj_game.player)) xpos 20 ypos 340 size 24 color "#ffffff"

        # Message
        if bj_game.msg:
            text bj_game.msg xalign 0.5 ypos 458 size 22 color "#f0d060"

        # Controls
        if bj_game.phase == "betting":
            hbox xalign 0.5 ypos 510 spacing 16:
                textbutton "-$25" action Return("bet_down") text_size 18
                text "Bet: $[bj_game.bet]" yalign 0.5 size 20 color "#ffffff"
                textbutton "+$25" action Return("bet_up")   text_size 18
            textbutton "DEAL" xalign 0.5 ypos 568 action Return("deal") text_size 26 text_color "#d4af37" text_font PROFILE_FONT

        elif bj_game.phase == "playing":
            hbox xalign 0.5 ypos 530 spacing 28:
                textbutton "HIT"   action Return("hit")   text_size 22
                textbutton "STAND" action Return("stand") text_size 22
                if money >= bj_game.bet and len(bj_game.player) == 2:
                    textbutton "DOUBLE" action Return("double") text_size 22 text_color "#f0d060"

        elif bj_game.phase == "result":
            hbox xalign 0.5 ypos 530 spacing 22:
                textbutton "Play Again" action Return("new_game") text_size 20
                textbutton "Roulette"   action Return("roulette") text_size 20
                textbutton "Leave"      action Return("leave")    text_size 18 text_color "#888888"


transform _rou_spin_anim:
    rotate 0.0
    linear 2.5 rotate 1440.0

transform _rou_static(angle):
    rotate angle

screen casino_roulette():
    if rou_game.phase == "spinning":
        timer 2.5 action Return("spin_done")
    add "casino_night"
    frame:
        background "#000000bb"
        xalign 0.5 yalign 0.5
        xysize (1280, 660)
        padding (20, 14, 20, 14)

        text "ROULETTE" xalign 0.5 ypos 8 size 30 color "#d4af37" font PROFILE_FONT
        text "Balance: $[money]" xpos 20 ypos 12 size 18 color "#aaffaa"
        textbutton "← Back" action Return("hub") xpos 1140 ypos 8 text_size 16 text_color "#888888"

        # ── Number grid (3 rows × 12 cols, standard layout) ──────────────────
        fixed xpos 18 ypos 52 xysize (870, 290):

            # 0 — green
            $ _s0 = (rou_game.bet_type == "number" and rou_game.bet_num == 0)
            button:
                background (_s0 and "#d4af37" or "#145214")
                xysize (50, 177)
                xpos 0 ypos 0
                action Return(("bet_num", 0))
                text "0" xalign 0.5 yalign 0.5 size 20 color ("#000" if _s0 else "#fff")

            # Numbers 1-36: col 0-11, row 0-2 → n = col*3 + (3-row)
            for _col in range(12):
                for _row in range(3):
                    $ _n  = _col * 3 + (3 - _row)
                    $ _sn = (rou_game.bet_type == "number" and rou_game.bet_num == _n)
                    $ _bg = (_sn and "#d4af37" or (_n in _ROU_REDS and "#6b1515" or "#181818"))
                    button:
                        background _bg
                        xysize (66, 57)
                        xpos 56 + _col * 68
                        ypos _row * 60
                        action Return(("bet_num", _n))
                        text str(_n) xalign 0.5 yalign 0.5 size 17 color ("#000" if _sn else "#fff")

            # Dozens
            for _di, (_dl, _dt) in enumerate([("1st 12","doz1"),("2nd 12","doz2"),("3rd 12","doz3")]):
                $ _sd = (rou_game.bet_type == _dt)
                button:
                    background (_sd and "#d4af37" or "#2a2a2a")
                    xysize (264, 40)
                    xpos 56 + _di * 268
                    ypos 184
                    action Return(("bet_type", _dt))
                    text _dl xalign 0.5 yalign 0.5 size 14 color ("#000" if _sd else "#ccc")

            # Outside bets: 1-18, Even, Red, Black, Odd, 19-36
            for _oi, (_ol, _ot, _obg) in enumerate([
                ("1-18","low","#222"),("EVEN","even","#222"),
                ("RED","red","#6b1515"),("BLACK","black","#181818"),
                ("ODD","odd","#222"),("19-36","high","#222"),
            ]):
                $ _so = (rou_game.bet_type == _ot)
                button:
                    background (_so and "#d4af37" or _obg)
                    xysize (130, 40)
                    xpos 56 + _oi * 133
                    ypos 230
                    action Return(("bet_type", _ot))
                    text _ol xalign 0.5 yalign 0.5 size 14 color ("#000" if _so else "#fff")

        # ── Right panel ───────────────────────────────────────────────────────
        fixed xpos 910 ypos 52 xysize (340, 580):

            # Roulette wheel — spinning ATL or static at result angle
            fixed xpos 60 ypos 0 xysize (220, 220):
                if rou_game.phase == "spinning":
                    add Transform("images/ui/roulette_wheel_transparent.png", size=(220, 220)) at _rou_spin_anim
                elif rou_game.result is not None:
                    add Transform("images/ui/roulette_wheel_transparent.png", size=(220, 220)) at _rou_static(rou_game.result * 137)
                else:
                    add Transform("images/ui/roulette_wheel_transparent.png", size=(220, 220)) at _rou_static(0)

            # Result number overlay on wheel centre
            if rou_game.result is not None:
                $ _rn  = rou_game.result
                $ _rbc = ("#145214" if _rn == 0 else ("#6b1515" if _rn in _ROU_REDS else "#181818"))
                frame:
                    background _rbc
                    xysize (52, 52)
                    xpos 144 ypos 84
                    text str(_rn) xalign 0.5 yalign 0.5 size 26 color "#fff"

            # Bet amount
            text "Bet Amount" xpos 0 ypos 228 size 16 color "#888"
            hbox xpos 0 ypos 252 spacing 10:
                textbutton "-$25" action Return("bet_down") text_size 17
                text "$[rou_game.bet_amt]" yalign 0.5 size 20 color "#fff"
                textbutton "+$25" action Return("bet_up") text_size 17

            # Current bet type
            $ _bt_names = {
                "red":"Red","black":"Black","even":"Even","odd":"Odd",
                "low":"1-18","high":"19-36",
                "doz1":"1st Dozen","doz2":"2nd Dozen","doz3":"3rd Dozen",
                "number":"Number %d" % rou_game.bet_num,
            }
            text ("Bet: " + _bt_names.get(rou_game.bet_type, "?")) xpos 0 ypos 310 size 16 color "#ccc"

            # Message
            text rou_game.msg xpos 0 ypos 345 size 15 color "#f0d060" xmaximum 340

            # Buttons — locked during spin
            if rou_game.phase == "betting":
                textbutton "SPIN" xpos 80 ypos 400 action Return("spin") text_size 30 text_color "#d4af37" text_font PROFILE_FONT
            elif rou_game.phase == "spinning":
                text "Spinning..." xpos 80 ypos 412 size 22 color "#d4af37"
            else:
                textbutton "Spin Again" xpos 20 ypos 400 action Return("reset") text_size 19
                textbutton "Blackjack" xpos 20 ypos 445 action Return("blackjack") text_size 17 text_color "#aaa"

            if rou_game.phase != "spinning":
                textbutton "Leave Casino" xpos 20 ypos 510 action Return("leave") text_size 17 text_color "#777"
