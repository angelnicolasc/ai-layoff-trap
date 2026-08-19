# -*- coding: utf-8 -*-
"""Shared visual system for every chart in this repo.

Design targets: SF Pro Display, a light neutral ground, dark rounded cards,
one accent colour, generous margins, 3:4 portrait. Import and call `setup()`
before building a figure.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------- palette
BG        = "#DCDCDA"   # page ground
CARD      = "#1E2126"   # dark card
CARD_SOFT = "#2A2E35"   # inner wells on a dark card
INK       = "#0B0B0B"   # primary text on light
INK_SOFT  = "#6E6E6E"   # secondary text on light
INK_FAINT = "#9A9A98"   # tertiary text on light
ON_CARD   = "#FFFFFF"   # primary text on dark
ON_CARD_2 = "#8E9199"   # secondary text on dark
ACCENT    = "#EB6834"   # single accent
ACCENT_2  = "#2A78D6"   # second series, only where two must be told apart
RULE      = "#C6C6C3"   # hairline on light

FONT = "SF Pro Display"
R, M, B = 400, 500, 700          # regular / medium / bold

# 3:4 portrait at 100 dpi
SIZE = (12.0, 16.0)


def setup():
    plt.rcParams.update({
        "font.family":       FONT,
        "font.weight":       R,
        "axes.unicode_minus": False,
        "figure.dpi":        100,
        "savefig.dpi":       100,
        "text.usetex":       False,
    })


def figure(size=SIZE):
    fig = plt.figure(figsize=size)
    fig.patch.set_facecolor(BG)
    return fig


def card(fig, x, y, w, h, color=CARD, radius=0.022, z=1):
    """Rounded card in figure coordinates. Returns the patch."""
    p = FancyBboxPatch((x, y), w, h, transform=fig.transFigure, zorder=z,
                       boxstyle=f"round,pad=0,rounding_size={radius}",
                       linewidth=0, facecolor=color, mutation_aspect=SIZE[0] / SIZE[1])
    fig.patches.append(p)
    return p


def text(fig, x, y, s, size=14, color=INK, weight=R, ha="left", va="baseline",
         spacing=1.55, **kw):
    return fig.text(x, y, s, fontsize=size, color=color, fontweight=weight,
                    ha=ha, va=va, linespacing=spacing, **kw)


def rule(fig, x0, x1, y, color=RULE, lw=1.0):
    fig.add_artist(plt.Line2D([x0, x1], [y, y], transform=fig.transFigure,
                              color=color, linewidth=lw, zorder=0))


def footer(fig, left, right, y=0.028, size=12.5):
    text(fig, 0.075, y, left,  size=size, color=INK_SOFT, weight=R)
    text(fig, 0.925, y, right, size=size, color=INK_SOFT, weight=R, ha="right")


# ------------------------------------------------------------------ px layout
# Figure coordinates are fractions of width/height, so a square drawn with equal
# fractional sides is not square on a non-square canvas. These helpers let every
# chart be laid out in pixels against a 1200x1600 canvas and converted once.
W_PX, H_PX = SIZE[0] * 100, SIZE[1] * 100


def fx(px):
    """Pixel x -> figure x."""
    return px / W_PX


def fy(px):
    """Pixel y measured from the TOP -> figure y."""
    return 1.0 - px / H_PX


def fw(px):
    """Pixel width -> figure width."""
    return px / W_PX


def fh(px):
    """Pixel height -> figure height."""
    return px / H_PX


def card_px(fig, x, y, w, h, color=CARD, radius_px=26, z=1):
    """Rounded card positioned in pixels, y measured from the top."""
    return card(fig, fx(x), fy(y + h), fw(w), fh(h), color=color,
                radius=radius_px / W_PX, z=z)


def text_px(fig, x, y, s, size=14, color=INK, weight=R, ha="left", va="baseline",
            spacing=1.55, **kw):
    """Text positioned in pixels, y measured from the top."""
    return text(fig, fx(x), fy(y), s, size=size, color=color, weight=weight,
                ha=ha, va=va, spacing=spacing, **kw)


def rule_px(fig, x0, x1, y, color=RULE, lw=1.0):
    rule(fig, fx(x0), fx(x1), fy(y), color=color, lw=lw)


# ------------------------------------------------- axes inside a dark card
ON_CARD_GRID  = "#2E333B"
ON_CARD_SPINE = "#3A404A"
SERIES_A = "#3987E5"   # dark-surface step, for the model curve
SERIES_B = "#D95926"   # measured reality (dark-surface step; validated pair)


def axes_px(fig, x, y, w, h, z=3):
    """Axes positioned in pixels, y measured from the top.

    z defaults above the card zorder: figure-level patches and axes are drawn in
    a single zorder-sorted pass, so an axes left at the default 0 renders behind
    any card placed over it.
    """
    ax = fig.add_axes([fx(x), fy(y + h), fw(w), fh(h)])
    ax.set_zorder(z)
    ax.patch.set_visible(False)
    return ax


def style_dark_axes(ax, grid_axis="y"):
    ax.set_facecolor("none")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(ON_CARD_SPINE)
        ax.spines[s].set_linewidth(1)
    ax.grid(axis=grid_axis, color=ON_CARD_GRID, lw=1, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(colors=ON_CARD_2, labelsize=13, length=0, pad=9)
    return ax
