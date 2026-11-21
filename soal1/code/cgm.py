"""Conjugate Gradient Method nonlinear (Tugas i-ii). d_{k+1} = -g_{k+1} + beta_k d_k.

Pemilik: Naufal (1A). Dua rumus beta_k: Fletcher-Reeves (FR) dan Polak-Ribiere+ (PR+).
"""
from __future__ import annotations

from typing import Callable

import numpy as np

from common import MAX_ITER, TOL, Problem, Result


def beta_fr(g_new: np.ndarray, g_old: np.ndarray, d_old: np.ndarray) -> float:
    """Fletcher-Reeves: ||g_{k+1}||^2 / ||g_k||^2."""
    return float(g_new @ g_new) / float(g_old @ g_old)


def beta_prp(g_new: np.ndarray, g_old: np.ndarray, d_old: np.ndarray) -> float:
    """Polak-Ribiere+: max(0, g_{k+1}^T (g_{k+1} - g_k) / ||g_k||^2)."""
    return max(0.0, float(g_new @ (g_new - g_old)) / float(g_old @ g_old))


BETA_RULES: dict[str, Callable[[np.ndarray, np.ndarray, np.ndarray], float]] = {
    "FR": beta_fr,
    "PR+": beta_prp,
}


def cgm(prob: Problem, x0: np.ndarray, linesearch: Callable, beta: str,
        tol: float = TOL, max_iter: int = MAX_ITER) -> Result:
    """Jalankan CGM. Henti saat ||g||_2 <= tol atau iterasi = max_iter.

    linesearch: ls(prob, x, d, g, fx) -> alpha (linesearch.binary_search / armijo).
    Bila d bukan arah turun (g^T d >= 0) atau pencari langkah mengembalikan alpha <= 0,
    arah di-restart ke -g. Result.path / gnorm_hist berindeks 0 = titik awal.
    """
    rule = BETA_RULES[beta]
    prob.reset()
    x = np.asarray(x0, dtype=float).copy()
    fx = prob.f(x)
    g = prob.grad(x)
    d = -g
    path, gh = [x.copy()], [float(np.linalg.norm(g))]
    k = 0
    while gh[-1] > tol and k < max_iter:
        if float(g @ d) >= 0.0:
            d = -g
        alpha = linesearch(prob, x, d, g, fx)
        if alpha <= 0.0:
            d = -g
            alpha = linesearch(prob, x, d, g, fx)
            if alpha <= 0.0:
                break                                  # macet: tidak ada langkah turun
        x = x + alpha * d
        fx = prob.f(x)
        g_new = prob.grad(x)
        d = -g_new + rule(g_new, g, d) * d
        g = g_new
        k += 1
        path.append(x.copy())
        gh.append(float(np.linalg.norm(g)))
    return Result(name=f"CGM-{beta}", x=x, f=fx, gnorm=gh[-1], iters=k,
                  n_f=prob.n_f, n_g=prob.n_g, converged=gh[-1] <= tol,
                  path=path, gnorm_hist=gh)
