# Stock market. Several stocks, each drifting independently every night by a
# random % in its own range (slight upward bias). View a 2-week line chart,
# buy/sell with a small spread. Chart is drawn via a Creator-Defined Displayable
# using Ren'Py's Render.canvas() (pygame line drawing).

# symbol, name, start price, max daily drop, max daily rise
define STOCK_META = [
    ("NEXS", "Nexus Corp",     120.0, 0.05, 0.06),   # steady blue-chip
    ("HUBX", "Hub Systems",     45.0, 0.09, 0.10),   # volatile tech
    ("IRON", "Iron Gate Fit",   30.0, 0.03, 0.035),  # low-risk, low-reward
    ("GRND", "Grounds Coffee",  18.0, 0.05, 0.055),
    ("LOGI", "LogiCity Freight", 60.0, 0.06, 0.06),
]
define STOCK_NAME = {m[0]: m[1] for m in STOCK_META}

default stock_price = {}   # symbol -> current price (float)
default stock_hist  = {}   # symbol -> [price history], last ~30 days
default stock_owned = {}   # symbol -> shares held

init python:
    import math

    def stocks_init():
        if store.stock_price:
            return
        for sym, name, p, dn, up in STOCK_META:
            # seed ~10 days of plausible history so the chart shows a line day 1
            val = p
            hist = [val]
            for _ in range(10):
                val = max(1.0, val * (1.0 + renpy.random.uniform(-dn, up)))
                hist.append(val)
            store.stock_price[sym] = val   # today = end of the seeded history
            store.stock_hist[sym]  = hist
            store.stock_owned[sym] = 0

    def stocks_step():
        stocks_init()
        for sym, name, p, dn, up in STOCK_META:
            pct = renpy.random.uniform(-dn, up)
            new = max(1.0, store.stock_price[sym] * (1.0 + pct))
            store.stock_price[sym] = new
            h = store.stock_hist[sym]
            h.append(new)
            del h[:-30]   # keep last 30 days

    def stock_buy_price(sym):  return int(math.ceil(store.stock_price[sym] * 1.01))   # +1% spread
    def stock_sell_price(sym): return int(math.floor(store.stock_price[sym] * 0.99))  # -1% spread

    def stock_buy(sym, n=1):
        cost = stock_buy_price(sym) * n
        if store.money >= cost:
            store.money -= cost
            store.stock_owned[sym] += n

    def stock_sell(sym, n=1):
        n = min(n, store.stock_owned[sym])
        if n > 0:
            store.money += stock_sell_price(sym) * n
            store.stock_owned[sym] -= n

    def portfolio_value():
        return sum(int(store.stock_price[s]) * store.stock_owned[s] for s in store.stock_owned)

    # ── Line-chart displayable (last 14 days) ──────────────────────────
    class StockChart(renpy.Displayable):
        def __init__(self, symbol, w=600, h=280, **kw):
            renpy.Displayable.__init__(self, **kw)
            self.symbol, self.w, self.h = symbol, w, h

        def render(self, width, height, st, at):
            r = renpy.Render(self.w, self.h)
            c = r.canvas()
            pad = 30
            data = list(store.stock_hist.get(self.symbol, []))[-14:]
            # panel bg + baseline grid
            c.rect((18, 30, 58, 255), (0, 0, self.w, self.h))
            c.line((70, 95, 150, 255), (pad, self.h - pad), (self.w - pad, self.h - pad), 2)
            c.line((70, 95, 150, 255), (pad, pad), (pad, self.h - pad), 2)
            if len(data) >= 2:
                mn, mx = min(data), max(data)
                rng = max(1.0, mx - mn)
                def pt(i, v):
                    x = pad + (self.w - 2 * pad) * i / (len(data) - 1)
                    y = (self.h - pad) - (self.h - 2 * pad) * (v - mn) / rng
                    return (int(x), int(y))
                up = data[-1] >= data[0]
                col = (90, 210, 130, 255) if up else (230, 110, 95, 255)
                for i in range(len(data) - 1):
                    c.line(col, pt(i, data[i]), pt(i + 1, data[i + 1]), 3)
                # end dot
                ex, ey = pt(len(data) - 1, data[-1])
                c.circle(col, (ex, ey), 5)
            return r


# ── Market screen: list + chart + trade ────────────────────────────────
screen stock_market():
    modal True
    default sel = STOCK_META[0][0]

    add "#000000aa"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1120
        ysize 660
        background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
        padding (34, 28, 34, 26)

        vbox:
            spacing 16
            hbox:
                spacing 24
                text "Stock Market" font PROFILE_FONT size 34 color "#ffffff"
                text ("Cash $%d    Portfolio $%d" % (money, portfolio_value())) font PROFILE_FONT size 20 color "#9fb6d6" yalign 1.0

            hbox:
                spacing 28
                # left: ticker list
                vbox:
                    spacing 8
                    for sym, name, _p, _d, _u in STOCK_META:
                        button:
                            xsize 300
                            padding (14, 10, 14, 10)
                            background Frame("images/ui/act_bar_idle.png", 30, 30, 30, 30)
                            hover_background Frame("images/ui/act_bar_hover.png", 30, 30, 30, 30)
                            action SetScreenVariable("sel", sym)
                            text ("%s   $%d   x%d" % (sym, int(stock_price[sym]), stock_owned[sym])) font PROFILE_FONT size 19 color ("#ffffff" if sel == sym else "#9fb6d6")

                # right: chart + trade panel
                vbox:
                    spacing 10
                    add StockChart(sel)
                    text ("%s  -  %s" % (sel, STOCK_NAME[sel])) font PROFILE_FONT size 22 color "#ffffff"
                    text ("Buy $%d     Sell $%d     You own %d" % (stock_buy_price(sel), stock_sell_price(sel), stock_owned[sel])) font PROFILE_FONT size 18 color "#cfe0f5"
                    hbox:
                        spacing 12
                        textbutton "Buy 1"   action Function(stock_buy, sel, 1)    text_font PROFILE_FONT text_size 20
                        textbutton "Buy 10"  action Function(stock_buy, sel, 10)   text_font PROFILE_FONT text_size 20
                        textbutton "Sell 1"  action Function(stock_sell, sel, 1)   text_font PROFILE_FONT text_size 20
                        textbutton "Sell all" action Function(stock_sell, sel, 999) text_font PROFILE_FONT text_size 20

            textbutton "Close" action [Hide("stock_market"), Show("phone_home")] text_font PROFILE_FONT text_size 22 text_color "#cfe0f5" text_hover_color "#ffffff"
