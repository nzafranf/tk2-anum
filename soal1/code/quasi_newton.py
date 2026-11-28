"""Quasi-Newton (Tugas ii): d_k = -B_k^{-1} g_k, s_k = x_{k+1}-x_k, y_k = g_{k+1}-g_k.

Pemilik: Amar (1B). Dua rumus pembaruan matriks hampiran Hessian B_k (2x2):
BFGS dan DFP, dengan invers 2x2 eksplisit sendiri (tanpa np.linalg.solve / inv).
"""
from __future__ import annotations

from typing import Callable

import numpy as np

from common import MAX_ITER, TOL, Problem, Result


def inv2x2(B: np.ndarray) -> np.ndarray | None:
    """Invers eksplisit matriks 2x2; mengembalikan None bila determinan ~ 0."""
    det = float(B[0, 0] * B[1, 1] - B[0, 1] * B[1, 0])
    if abs(det) <= 1e-30:
        return None
    return np.array([[B[1, 1], -B[0, 1]],
                     [-B[1, 0], B[0, 0]]], dtype=float) / det


def update_bfgs(B: np.ndarray, s: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Pembaruan BFGS pada B_k; dilewati bila syarat kelengkungan s^T y <= 0."""
    sy = float(s @ y)
    norm_sy = float(np.sqrt(float(s @ s) * float(y @ y)))
    if sy <= 1e-14 * norm_sy:
        return B
    Bs = B @ s
    sBs = float(s @ Bs)
    if sBs <= 0.0:
        return B
    B_new = B - np.outer(Bs, Bs) / sBs + np.outer(y, y) / sy
    return 0.5 * (B_new + B_new.T)


def update_dfp(B: np.ndarray, s: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Pembaruan DFP pada B_k; dilewati bila syarat kelengkungan s^T y <= 0."""
    sy = float(s @ y)
    norm_sy = float(np.sqrt(float(s @ s) * float(y @ y)))
    if sy <= 1e-14 * norm_sy:
        return B
    P = np.eye(2) - np.outer(y, s) / sy
    B_new = P @ B @ P.T + np.outer(y, y) / sy
    return 0.5 * (B_new + B_new.T)


UPDATES: dict[str, Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]] = {
    "BFGS": update_bfgs,
    "DFP": update_dfp,
}


def quasi_newton(prob: Problem, x0: np.ndarray, linesearch: Callable, update: str,
                 tol: float = TOL, max_iter: int = MAX_ITER) -> Result:
    """Jalankan quasi-Newton dari B_0 = I hingga ||g||_2 <= tol atau max_iter."""
    rule = UPDATES[update]
    prob.reset()
    x = np.asarray(x0, dtype=float).copy()
    fx = prob.f(x)
    g = prob.grad(x)
    B = np.eye(2)
    path, gh = [x.copy()], [float(np.linalg.norm(g))]
    k = 0
    while gh[-1] > tol and k < max_iter:
        B_inv = inv2x2(B)
        if B_inv is None:
            B = np.eye(2)
            d = -g
        else:
            d = -(B_inv @ g)
        if float(g @ d) >= 0.0:
            B = np.eye(2)
            d = -g
        alpha = linesearch(prob, x, d, g, fx)
        if alpha <= 0.0:
            B = np.eye(2)
            d = -g
            alpha = linesearch(prob, x, d, g, fx)
            if alpha <= 0.0:
                break
        x_new = x + alpha * d
        fx = prob.f(x_new)
        g_new = prob.grad(x_new)
        B = rule(B, x_new - x, g_new - g)
        x, g = x_new, g_new
        k += 1
        path.append(x.copy())
        gh.append(float(np.linalg.norm(g)))
    return Result(name=f"QN-{update}", x=x, f=fx, gnorm=gh[-1], iters=k,
                  n_f=prob.n_f, n_g=prob.n_g, converged=gh[-1] <= tol,
                  path=path, gnorm_hist=gh)
