# -*- coding: utf-8 -*-
"""Post slide 2: the model's safe zone, and the fact that it is empty."""
from matplotlib.ticker import FuncFormatter
import numpy as np
import post_style as S

S.setup()
fig = S.figure()
L, RGT = S.L, S.RGT

FLOOR = 100 - (462.415 + 90.238) / 15_259.0 * 100      # 96.38 %

S.header(fig)
S.text(fig, L, 200, "Three escape hatches.", size=52, color=S.INK, weight=S.B)
S.text(fig, L, 264, "No firm can reach them.", size=48, color=S.INK, weight=S.B)
S.text(fig, L, 326, "The model says concentration saves you.",
       size=30, color=S.ACCENT, weight=S.M)

CA_TOP, CA_H = 384, 800
S.card(fig, L, CA_TOP, RGT - L, CA_H)
S.text(fig, L + 44, CA_TOP + 60, "Share of the damage a firm does NOT absorb",
       size=26, color=S.ON_CARD, weight=S.M)

ax = S.axes(fig, L + 140, CA_TOP + 108, 880, 540)
ax.set_facecolor("none")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#454B55"); ax.spines[s].set_linewidth(1.2)
ax.grid(axis="y", color="#333941", lw=1.2, zorder=0)
ax.set_axisbelow(True)
ax.tick_params(colors=S.ON_CARD_2, labelsize=20, length=0, pad=12)

N = np.logspace(0, 3, 700)
ax.axhspan(0, FLOOR, facecolor="#2B3038", zorder=1)
ax.axhspan(FLOOR, 100, facecolor=S.ACCENT, alpha=.35, zorder=2)
ax.axhline(FLOOR, color=S.ACCENT, lw=3.2, zorder=5, solid_capstyle="round")
ax.plot(N, 100 * (1 - 1 / N), color="#4E97F0", lw=3.2, zorder=4, solid_capstyle="round")

ax.set_xscale("log"); ax.set_xlim(1, 1000); ax.set_ylim(0, 103)
ax.set_yticks([0, 50, 100])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.set_xticks([1, 10, 100, 1000])
ax.set_xticklabels(["1", "10", "100", "1,000"])

ax.text(880, 86, "Every U.S. firm is in this strip", fontsize=23,
        color=S.ACCENT, fontweight=S.M, ha="right")
ax.text(30, 46, "Nothing is down here", fontsize=26, color=S.ON_CARD,
        fontweight=S.M, ha="center")
ax.text(30, 33, "the region where concentration\nis supposed to fix the problem",
        fontsize=20, color=S.ON_CARD_2, ha="center", va="top", linespacing=1.6)

S.text(fig, L + 140 + 440, CA_TOP + 716, "Number of competing firms",
       size=22, color=S.ON_CARD_2, ha="center")

for i, (col, lab) in enumerate([("#4E97F0", "what the model assumes"),
                                (S.ACCENT,  "what the data show")]):
    x0 = L + 150 + i * 470
    fig.add_artist(__import__("matplotlib").lines.Line2D(
        [S.fx(x0), S.fx(x0 + 44)], [S.fy(CA_TOP + 764)] * 2,
        transform=fig.transFigure, color=col, lw=3.2, solid_capstyle="round", zorder=6))
    S.text(fig, x0 + 60, CA_TOP + 772, lab, size=21, color=S.ON_CARD_2)

S.text(fig, L, 1288, "No firm in America is big enough to feel its own decision.",
       size=30, color=S.INK, weight=S.M)
S.rule(fig, L, RGT, 1330)
S.text(fig, L, 1378,
       "Company revenue ÷ U.S. consumer spending, FY2025 filings and BEA.",
       size=17, color=S.INK_SOFT)
S.text(fig, L, 1410,
       "Model curve from Falk & Tsoukalas, arXiv:2603.20617, Proposition 1.",
       size=17, color=S.INK_SOFT)

fig.savefig("post_escape.png", facecolor=S.BG)
print("saved post_escape.png")
