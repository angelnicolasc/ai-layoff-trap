# -*- coding: utf-8 -*-
"""Effective N: the measured wallet share, expressed in the paper's own variable.

If 1/N is only "a firm's share of its sector", the paper still needs N to be a
real market-structure number — it sets the corrective rate at tau* = l(1-1/N)
and concludes that fragmented industries suffer most. Measured as a share of the
consumer wallet, every firm behaves like one facing far more rivals than it has.

Laid out in pixels against a 1200x1600 canvas (3:4).
"""
import numpy as np
import style as S

S.setup()
fig = S.figure()

PCE = 20_956.0
firms = [("Walmart  + Sam's Club",        462.415 + 90.238, 4),
         ("Amazon  North America",        426.0,            4),
         ("Costco  U.S.",                 180.0,            6),
         ("Home Depot",                   152.0,            2),
         ("Microsoft  consumer slice",     30.0,            3),
         ("Alphabet  direct-to-consumer",  15.0,            2),
         ("Salesforce",                     0.2,            5)]

L, RGT = 90, 1110

# -------------------------------------------------------------------- header
S.text_px(fig, L,   62, "The recapture ratio", size=15, color=S.INK_SOFT, weight=S.M)
S.text_px(fig, RGT, 62, "Nick Cerutti", size=15, color=S.INK_SOFT, ha="right")
S.rule_px(fig, L, RGT, 100)

S.text_px(fig, L, 178, "Nobody is where the", size=48, color=S.INK, weight=S.B)
S.text_px(fig, L, 240, "model thinks they are.", size=48, color=S.INK, weight=S.B)
S.text_px(fig, L, 300,
          "If 1/N is only a firm's share of its own sector, the paper still needs N to be a real market-structure",
          size=14.5, color=S.INK_SOFT)
S.text_px(fig, L, 326,
          "number: it sets the corrective tax at that value and concludes fragmented industries suffer most.",
          size=14.5, color=S.INK_SOFT)
S.text_px(fig, L, 352,
          "Measure the same quantity against consumer spending and every firm behaves like one facing",
          size=14.5, color=S.INK_SOFT)
S.text_px(fig, L, 378,
          "between 10 and 20,000 times more competitors than it actually has.",
          size=14.5, color=S.INK_SOFT)

# ------------------------------------------------------------------- card
CA_TOP, CA_H = 430, 800
S.card_px(fig, L, CA_TOP, RGT - L, CA_H)
S.text_px(fig, L + 40, CA_TOP + 48,
          "Competitors a firm has, and competitors it behaves as if it had",
          size=17, color=S.ON_CARD, weight=S.M)

ax = S.axes_px(fig, L + 268, CA_TOP + 96, 700, 592)
S.style_dark_axes(ax, grid_axis="x")
ax.spines["left"].set_visible(False)

yp = np.arange(len(firms))
for y, (name, rev, n) in zip(yp, firms):
    ne = 1 / (rev / PCE)
    ax.plot([n, ne], [y, y], color=S.ON_CARD_SPINE, lw=2.4, zorder=2,
            solid_capstyle="round")
    ax.plot([n],  [y], "o", ms=11, color=S.SERIES_A, mec=S.CARD, mew=2, zorder=5)
    ax.plot([ne], [y], "o", ms=11, color=S.SERIES_B, mec=S.CARD, mew=2, zorder=5)
    ax.text(ne * 1.42, y, f"{ne:,.0f}", va="center", fontsize=13,
            color=S.ON_CARD, fontweight=S.M)
    ax.text(n * 0.68, y, f"{n}", va="center", ha="right", fontsize=13, color=S.ON_CARD_2)

ax.set_yticks(yp)
ax.set_yticklabels([f[0] for f in firms], fontsize=13.5, color=S.ON_CARD)
ax.invert_yaxis()
ax.set_xscale("log"); ax.set_xlim(1.15, 7.5e5); ax.set_ylim(len(firms) - .4, -.85)
ax.set_xticks([2, 10, 100, 1_000, 10_000, 100_000])
ax.set_xticklabels(["2", "10", "100", "1,000", "10,000", "100,000"])

for i, (col, lab) in enumerate([(S.SERIES_A, "actual national competitors"),
                                (S.SERIES_B, "effective N implied by measured wallet share")]):
    S.text_px(fig, L + 268 + 22 + i * 300, CA_TOP + 742, lab,
              size=13, color=S.ON_CARD_2)
    fig.add_artist(__import__("matplotlib").lines.Line2D(
        [S.fx(L + 268 + i * 300)], [S.fy(CA_TOP + 738)], marker="o",
        markersize=11, color=col, transform=fig.transFigure, zorder=6))

S.text_px(fig, L + 268 + 350, CA_TOP + 776,
          "N  —  number of competing firms   (log scale)",
          size=13.5, color=S.ON_CARD_2, ha="center")

# ------------------------------------------------------------------ takeaway
S.text_px(fig, L, 1288,
          "Concentration buys no protection. Every firm sits far to the right of the model.",
          size=19, color=S.INK, weight=S.M)

# -------------------------------------------------------------------- footer
S.rule_px(fig, L, RGT, 1360)
S.text_px(fig, L, 1392,
          "Effective N = 1/ω, where ω is a firm's U.S. household-facing revenue ÷ U.S. personal consumption expenditure (BEA, USD 20,956bn, 2025).\n"
          "Revenues from FY2025 filings. 'Actual competitors' counts major national rivals in each firm's core consumer market.",
          size=10.5, color=S.INK_FAINT, va="top", spacing=1.9)

fig.savefig("effective_n.png", facecolor=S.BG)
print("saved effective_n.png")
