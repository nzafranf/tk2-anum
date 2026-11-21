"""Pencarian langkah (Tugas i). Ditugaskan: lihat WORK_SPLIT.md.

Kedua fungsi mengembalikan alpha > 0 dan memakai `prob.f` / `prob.grad` agar evaluasi tercatat.
"""
from __future__ import annotations

import numpy as np

from common import Problem


def binary_search(prob: Problem, x: np.ndarray, d: np.ndarray, g: np.ndarray,
                  width_tol: float = 1e-6) -> float:
    """Bagi-dua pada phi'(a) = grad f(x + a d)^T d.

    Cari [a, b] dengan phi'(a) < 0 < phi'(b) (mulai dari a = 0 dengan phi'(0) = g^T d < 0,
    perbesar b sampai phi'(b) > 0), bagi dua sampai lebar < width_tol, kembalikan titik tengah.
    Perlu: jaga d adalah arah turun (g^T d < 0); bila tidak, tangani (mis. reset ke -g).
    """
    raise NotImplementedError


def armijo(prob: Problem, x: np.ndarray, d: np.ndarray, g: np.ndarray, fx: float,
           c1: float = 1e-4, alpha0: float = 1.0, shrink: float = 0.5) -> float:
    """Backtracking: alpha = alpha0; selama f(x+a d) > f(x) + c1*a*g^T d, alpha *= shrink."""
    raise NotImplementedError
