# -*- coding: utf-8 -*-
"""Replication of Proposition 1 in Falk & Tsoukalas (2026), arXiv:2603.20617.

This is the sanity check that the model is being read correctly before anything
is built on top of it. Two independent routes to the over-automation wedge must
agree exactly:

    alpha_NE = min((s - l/N)/k, 1)          Nash equilibrium automation rate
    alpha_CO = min(max((s - l)/k, 0), 1)    cooperative optimum
    wedge    = l(1 - 1/N)/k                 the paper's closed form

with  s = w - c  (per-task cost saving)  and  l = lam(1-eta)w  (demand lost per
automated task). Parameters below are the paper's own illustrative values.
"""
import numpy as np


def alpha_ne(s, l, N, k):
    return float(np.clip((s - l / N) / k, 0, 1))


def alpha_co(s, l, k):
    return float(np.clip((s - l) / k, 0, 1))


w, c, lam, eta, k, N = 1.0, 0.30, 0.5, 0.30, 1.0, 7
s = w - c
l = lam * (1 - eta) * w

ne, co = alpha_ne(s, l, N, k), alpha_co(s, l, k)
closed_form = l * (1 - 1 / N) / k

print("=" * 68)
print("Proposition 1  (c/w=0.30, lam=0.5, eta=0.30, N=7, k=1)")
print("=" * 68)
print(f"  s = w - c              = {s:.4f}")
print(f"  l = lam(1-eta)w        = {l:.4f}")
print(f"  N* = l/s               = {l/s:.4f}     (a firm automates iff N > N*)")
print(f"  alpha_NE               = {ne:.4f}")
print(f"  alpha_CO               = {co:.4f}")
print("-" * 68)
print(f"  wedge, from the rates  = {ne - co:.4f}")
print(f"  wedge, closed form     = {closed_form:.4f}")
print(f"  Pigouvian rate tau*    = {l * (1 - 1/N):.4f}")
print("-" * 68)
assert l < s < k + l, "this point is not interior; Prop 1(iii) does not apply"
assert (s - l / N) / k <= 1, "alpha_NE is at the corner; the closed form is not the wedge"
assert abs((ne - co) - closed_form) < 1e-12, "replication failed"
print(f"  interiority l < s < k+l:  {l:.2f} < {s:.2f} < {k+l:.2f}  -- checked, not assumed")
print("  MATCH to machine precision. The model is read correctly.")
print()
print("  A single point can match by coincidence, so the same identity is swept")
print("  over a grid in tests.py section 1: it holds on every interior point and")
print("  is correctly excluded on every corner point.")

# Comparative statics the paper states, reproduced numerically.
print("\n" + "=" * 68)
print("Internalisation and wedge across market structures")
print("=" * 68)
print(f"{'N':>8}{'internalised':>16}{'wedge x k/l':>16}")
print("-" * 68)
for n in (1, 2, 4, 7, 20, 100, 10_000):
    print(f"{n:>8}{1/n*100:>15.2f}%{1 - 1/n:>16.4f}")
print("-" * 68)
print("  A monopolist internalises everything and needs no correction; the wedge")
print("  rises monotonically with N toward its maximum of l/k. Whether any real")
print("  firm occupies the low-N end is the question identity.py answers.")
