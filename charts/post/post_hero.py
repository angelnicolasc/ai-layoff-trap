# -*- coding: utf-8 -*-
"""Hero post: the recapture ratio, for a general audience."""
from matplotlib.patches import Rectangle
import post_style as S

S.setup()
fig = S.figure()
L, RGT = S.L, S.RGT

cards = [
    ("The model assumes",      "a four-firm market",       25, "$25.00"),
    ("Walmart",                "the best case in America",  3, "$2.64"),
    ("Block",                  "the paper's own example",   0, "$0.03"),
]

S.header(fig)
S.text(fig, L, 200, "Fire a worker.",               size=52, color=S.INK, weight=S.B)
S.text(fig, L, 264, "$100 of spending disappears.", size=52, color=S.INK, weight=S.B)
S.text(fig, L, 326, "How much comes back to the firm that fired them?",
       size=30, color=S.ACCENT, weight=S.M)

CARD_TOP, CARD_H, GAP = 384, 262, 22
CELL, PAD = 19, 4
GRID = 10 * CELL + 9 * PAD                       # 226

for i, (name, sub, n_fill, money) in enumerate(cards):
    top = CARD_TOP + i * (CARD_H + GAP)
    S.card(fig, L, top, RGT - L, CARD_H)

    gx, gy = L + 36, top + (CARD_H - GRID) // 2
    for k in range(100):
        r, c = divmod(k, 10)
        fig.patches.append(Rectangle(
            (S.fx(gx + c * (CELL + PAD)), S.fy(gy + r * (CELL + PAD) + CELL)),
            S.fw(CELL), S.fh(CELL), transform=fig.transFigure, zorder=3,
            linewidth=0, facecolor=S.ACCENT if k < n_fill else S.CARD_SOFT))

    tx = gx + GRID + 56
    S.text(fig, tx, top + 135, name, size=32, color=S.ON_CARD, weight=S.M)
    S.text(fig, tx, top + 172, sub,  size=20, color=S.ON_CARD_2)
    S.text(fig, RGT - 44, top + 158, money, size=62, color=S.ACCENT,
           weight=S.B, ha="right")

S.text(fig, L, 1288, "The people you fire don't shop at your store.",
       size=30, color=S.INK, weight=S.M)
S.rule(fig, L, RGT, 1330)
S.text(fig, L, 1378,
       "Each square is $1 of the spending a laid-off worker stops doing.",
       size=17, color=S.INK_SOFT)
S.text(fig, L, 1410,
       "Company revenue ÷ U.S. consumer spending, FY2025 filings and BEA.",
       size=17, color=S.INK_SOFT)

fig.savefig("post_hero.png", facecolor=S.BG)
print("saved post_hero.png")
