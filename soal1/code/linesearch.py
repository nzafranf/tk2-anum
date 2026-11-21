"""Pencarian langkah (Tugas i). Pemilik: Naufal (1A).

Semua pencari langkah berbagi tanda tangan seragam `ls(prob, x, d, g, fx) -> alpha`
(g = grad f(x), fx = f(x)) sehingga bisa ditukar di `cgm()` / `quasi_newton()`.
Evaluasi f dan grad f dilakukan lewat `prob` agar tercatat otomatis.
"""
from __future__ import annotations

import numpy as np

from common import Problem

MAX_BRACKET = 60     # batas penggandaan untuk mencari b dengan phi'(b) > 0
MAX_BACKTRACK = 60   # batas pengecilan alpha pada Armijo


def binary_search(prob: Problem, x: np.ndarray, d: np.ndarray, g: np.ndarray,
                  fx: float | None = None, width_tol: float = 1e-6) -> float:
    """Bagi-dua pada phi'(a) = grad f(x + a d)^T d.

    a = 0 memenuhi phi'(0) = g^T d < 0. Cari b dengan phi'(b) > 0 dengan menggandakan
    b = 1, 2, 4, ...; lalu bagi dua [a, b] (pertahankan phi'(a) < 0 < phi'(b)) sampai
    lebar < width_tol. Mengembalikan titik tengah. `fx` tidak dipakai (hanya agar
    tanda tangan sama dengan armijo). Bila d bukan arah turun, kembalikan 0.0
    (pemanggil harus me-restart ke -g).
    """
    if float(g @ d) >= 0.0:
        return 0.0
    a, b = 0.0, 1.0
    for _ in range(MAX_BRACKET):
        if float(prob.grad(x + b * d) @ d) > 0.0:
            break
        a, b = b, 2.0 * b
    else:
        return a                      # tidak ada titik balik: pakai a terbesar yang turun
    while b - a >= width_tol:
        m = 0.5 * (a + b)
        dm = float(prob.grad(x + m * d) @ d)
        if dm < 0.0:
            a = m
        elif dm > 0.0:
            b = m
        else:
            return m
    return 0.5 * (a + b)


def armijo(prob: Problem, x: np.ndarray, d: np.ndarray, g: np.ndarray,
           fx: float | None = None, c1: float = 1e-4, alpha0: float = 1.0,
           shrink: float = 0.5) -> float:
    """Backtracking: alpha = alpha0; selama f(x + a d) > f(x) + c1 a g^T d, alpha *= shrink.

    f(x) diberikan lewat `fx` (tidak dievaluasi ulang); bila None dihitung sekali.
    """
    slope = float(g @ d)
    if slope >= 0.0:
        return 0.0
    if fx is None:
        fx = prob.f(x)
    alpha = alpha0
    for _ in range(MAX_BACKTRACK):
        if prob.f(x + alpha * d) <= fx + c1 * alpha * slope:
            return alpha
        alpha *= shrink
    return alpha


LINESEARCHES = {"binary": binary_search, "armijo": armijo}
