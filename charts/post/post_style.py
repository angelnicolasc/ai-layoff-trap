# -*- coding: utf-8 -*-
"""Visual system for the LinkedIn/X post versions.

Differences from charts/style.py, all driven by mobile legibility:
  * canvas 1240x1450, matching the reference posts rather than 3:4
  * every type size roughly doubled; nothing below 15pt (~21px)
  * the faint tertiary ink is gone — secondary is the floor, so no text sits
    close in value to the ground it is printed on
  * far less text per figure: a card carries a label, a number and a caption
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG        = "#DCDCDA"
CARD      = "#1E2126"
CARD_SOFT = "#31363F"   # lifted so unfilled waffle cells stay visible
INK       = "#0B0B0B"
INK_SOFT  = "#5A5A58"   # darkened for contrast against BG
ON_CARD   = "#FFFFFF"
ON_CARD_2 = "#A2A6AE"   # lifted for contrast against CARD
ACCENT    = "#EB6834"
RULE      = "#BFBFBC"

FONT = "SF Pro Display"
R, M, B = 400, 500, 700

W_PX, H_PX = 1240, 1450
SIZE = (W_PX / 100, H_PX / 100)
L, RGT = 80, 1160                    # content edges


def setup():
    plt.rcParams.update({
        "font.family": FONT, "font.weight": R,
        "axes.unicode_minus": False,
        "figure.dpi": 100, "savefig.dpi": 100, "text.usetex": False,
    })


def figure():
    fig = plt.figure(figsize=SIZE)
    fig.patch.set_facecolor(BG)
    return fig


def fx(px): return px / W_PX
def fy(px): return 1.0 - px / H_PX
def fw(px): return px / W_PX
def fh(px): return px / H_PX


def card(fig, x, y, w, h, color=CARD, radius_px=30, z=1):
    p = FancyBboxPatch((fx(x), fy(y + h)), fw(w), fh(h),
                       transform=fig.transFigure, zorder=z,
                       boxstyle=f"round,pad=0,rounding_size={radius_px / W_PX}",
                       linewidth=0, facecolor=color,
                       mutation_aspect=SIZE[0] / SIZE[1])
    fig.patches.append(p)
    return p


def text(fig, x, y, s, size=20, color=INK, weight=R, ha="left", va="baseline",
         spacing=1.5, **kw):
    return fig.text(fx(x), fy(y), s, fontsize=size, color=color, fontweight=weight,
                    ha=ha, va=va, linespacing=spacing, **kw)


def rule(fig, x0, x1, y, color=RULE, lw=1.2):
    fig.add_artist(plt.Line2D([fx(x0), fx(x1)], [fy(y), fy(y)],
                              transform=fig.transFigure, color=color,
                              linewidth=lw, zorder=0))


def axes(fig, x, y, w, h, z=3):
    ax = fig.add_axes([fx(x), fy(y + h), fw(w), fh(h)])
    ax.set_zorder(z)
    ax.patch.set_visible(False)
    return ax


def header(fig, left="The recapture ratio", right="Nick Cerutti"):
    text(fig, L,   72, left,  size=20, color=INK_SOFT, weight=M)
    text(fig, RGT, 72, right, size=20, color=INK_SOFT, ha="right")
    rule(fig, L, RGT, 108)
