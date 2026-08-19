# -*- coding: utf-8 -*-
"""Hero visual, general audience.

100 squares = USD 100 of consumer spending destroyed by one layoff. Filled
squares = how much lands back on the firm that caused it.

Variant discipline, stated so the choices cannot be read as convenient:
  * Walmart uses the MAXIMUM numerator (U.S. segment + Sam's Club U.S.), because
    the card claims "best case in the U.S." Every other variant is in the footnote.
  * Block excludes bitcoin passthrough. Asset purchases are not consumption and
    PCE excludes them by construction, so counting them in the numerator while
    the denominator excludes them would break numerator/denominator consistency —
    the same rule applied to third-party-paid health revenue.

Laid out in pixels against a 1200x1600 canvas (3:4).
"""
from matplotlib.patches import Rectangle
import style as S

S.setup()
fig = S.figure()

cards = [
    ("What the model assumes", "the economics paper, four-firm market", 25, "$25.00",
     "At this level a company feels its own damage.\nIt has a reason to stop."),
    ("Walmart", "the best case in the entire U.S. economy", 3, "$2.64",
     "Its laid-off cashiers spend almost all their\nmoney somewhere that isn't Walmart."),
    ("Block", "the paper's own opening example", 0, "$0.03",
     "Dorsey cut half the staff citing AI.\nIts engineers were never its customers."),
]

L, RGT = 90, 1110                      # left / right content edges

# ------------------------------------------------------------------- header
S.text_px(fig, L,   62, "The recapture ratio", size=15, color=S.INK_SOFT, weight=S.M)
S.text_px(fig, RGT, 62, "Nick Cerutti", size=15, color=S.INK_SOFT, ha="right")
S.rule_px(fig, L, RGT, 100)

S.text_px(fig, L, 180, "Fire a worker.",             size=52, color=S.INK, weight=S.B)
S.text_px(fig, L, 250, "$100 of spending disappears.", size=52, color=S.INK, weight=S.B)
S.text_px(fig, L, 312, "How much lands back on you?", size=27, color=S.ACCENT, weight=S.M)

# --------------------------------------------------------------------- cards
CARD_TOP, CARD_H, GAP = 380, 250, 28
CELL, PAD = 17, 3
for i, (name, sub, n_fill, money, note) in enumerate(cards):
    top = CARD_TOP + i * (CARD_H + GAP)
    S.card_px(fig, L, top, RGT - L, CARD_H)

    gx, gy = L + 34, top + 26
    for k in range(100):
        r, c = divmod(k, 10)
        fig.patches.append(Rectangle(
            (S.fx(gx + c * (CELL + PAD)), S.fy(gy + r * (CELL + PAD) + CELL)),
            S.fw(CELL), S.fh(CELL), transform=fig.transFigure, zorder=3,
            linewidth=0, facecolor=S.ACCENT if k < n_fill else S.CARD_SOFT))

    tx = gx + 10 * CELL + 9 * PAD + 44
    S.text_px(fig, tx, top + 52,  name,  size=25, color=S.ON_CARD, weight=S.M)
    S.text_px(fig, tx, top + 80,  sub,   size=14, color=S.ON_CARD_2)
    S.text_px(fig, tx, top + 142, money, size=44, color=S.ACCENT, weight=S.B)
    S.text_px(fig, tx, top + 166, "comes back to the company that fired them",
              size=13.5, color=S.ON_CARD_2)
    S.text_px(fig, tx, top + 190, note, size=14, color=S.ON_CARD,
              va="top", spacing=1.62)

# ------------------------------------------------------------------ takeaway
S.text_px(fig, L, 1250,
          "A company keeps everything it saves and absorbs almost none of the damage,",
          size=19, color=S.INK, weight=S.M)
S.text_px(fig, L, 1282,
          "because the people it fires were mostly somebody else's customers.",
          size=19, color=S.INK, weight=S.M)

# -------------------------------------------------------------------- footer
S.rule_px(fig, L, RGT, 1348)
S.text_px(fig, L, 1380,
          "Each square is one dollar of the spending a laid-off worker stops doing.",
          size=13.5, color=S.INK_SOFT)
S.text_px(fig, L, 1418,
          "Share of U.S. consumer spending captured by each company: FY2025 filings ÷ U.S. personal consumption expenditure (BEA, USD 20,956bn).\n"
          "Walmart = U.S. segment + Sam's Club U.S. (2.64%); Walmart U.S. alone is 2.21%, and 3.62% against the most adverse denominator.\n"
          "Block = Cash App excluding bitcoin passthrough — asset purchases are not consumption and PCE excludes them by construction. All of\n"
          "Cash App gives 0.07; Block's entire global revenue, 0.11.  Model figure: Falk & Tsoukalas, arXiv:2603.20617, Proposition 1.",
          size=10.5, color=S.INK_FAINT, va="top", spacing=1.9)

fig.savefig("lay_waffle.png", facecolor=S.BG)
print("saved lay_waffle.png")
