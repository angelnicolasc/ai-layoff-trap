# -*- coding: utf-8 -*-
"""Post slide 3: competitors a firm has, versus competitors it behaves as if it had."""
import numpy as np
import post_style as S

S.setup()
fig = S.figure()
L, RGT = S.L, S.RGT
PCE = 20_956.0
BLUE = "#4E97F0"

firms = [("Walmart",     462.415 + 90.238, 4),
         ("Amazon",      426.0,            4),
         ("Home Depot",  152.0,            2),
         ("Microsoft",    30.0,            3),
         ("Salesforce",    0.2,            5)]

S.header(fig)
S.text(fig, L, 200, "Nobody is where the",     size=52, color=S.INK, weight=S.B)
S.text(fig, L, 264, "model thinks they are.",  size=52, color=S.INK, weight=S.B)
S.text(fig, L, 326, "Competitors a firm has, and competitors it acts like it has.",
       size=27, color=S.ACCENT, weight=S.M)

CA_TOP, CA_H = 384, 800
S.card(fig, L, CA_TOP, RGT - L, CA_H)

ax = S.axes(fig, L + 290, CA_TOP + 70, 640, 600)
ax.set_facecolor("none")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#454B55"); ax.spines["bottom"].set_linewidth(1.2)
ax.grid(axis="x", color="#333941", lw=1.2, zorder=0)
ax.set_axisbelow(True)
ax.tick_params(colors=S.ON_CARD_2, labelsize=20, length=0, pad=12)

yp = np.arange(len(firms))
for y, (name, rev, n) in zip(yp, firms):
    ne = 1 / (rev / PCE)
    ax.plot([n, ne], [y, y], color="#4A515C", lw=3, zorder=2, solid_capstyle="round")
    ax.plot([n],  [y], "o", ms=17, color=BLUE,     mec=S.CARD, mew=3, zorder=5)
    ax.plot([ne], [y], "o", ms=17, color=S.ACCENT, mec=S.CARD, mew=3, zorder=5)
    ax.text(ne * 1.7, y, f"{n}  →  {ne:,.0f}", va="center", fontsize=25,
            color=S.ON_CARD, fontweight=S.M)

ax.set_yticks(yp)
ax.set_yticklabels([f[0] for f in firms], fontsize=27, color=S.ON_CARD)
ax.invert_yaxis()
ax.set_xscale("log"); ax.set_xlim(1.2, 9e6); ax.set_ylim(len(firms) - .45, -.8)
ax.set_xticks([10, 1_000, 100_000])
ax.set_xticklabels(["10", "1,000", "100,000"])

S.text(fig, L + 290 + 320, CA_TOP + 736, "Number of competitors",
       size=22, color=S.ON_CARD_2, ha="center")

for i, (col, lab) in enumerate([(BLUE, "competitors it has"),
                                (S.ACCENT, "competitors it acts like it has")]):
    x0 = L + 150 + i * 400
    fig.add_artist(__import__("matplotlib").lines.Line2D(
        [S.fx(x0)], [S.fy(CA_TOP + 768)], marker="o", markersize=17,
        transform=fig.transFigure, color=col, zorder=6))
    S.text(fig, x0 + 26, CA_TOP + 776, lab, size=21, color=S.ON_CARD_2)

S.text(fig, L, 1288, "Concentration buys no protection at all.",
       size=30, color=S.INK, weight=S.M)
S.rule(fig, L, RGT, 1330)
S.text(fig, L, 1378,
       "Competitors it acts like it has = U.S. consumer spending ÷ the firm's share of it.",
       size=17, color=S.INK_SOFT)
S.text(fig, L, 1410,
       "FY2025 filings and BEA. Full method and code: github.com/angelnicolasc/ai-layoff-trap",
       size=17, color=S.INK_SOFT)

fig.savefig("post_effective_n.png", facecolor=S.BG)
print("saved post_effective_n.png")
