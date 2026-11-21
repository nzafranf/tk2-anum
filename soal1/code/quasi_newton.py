"""Quasi-Newton (Tugas ii). Arah d_k = -B_k^{-1} g_k, s_k = x_{k+1}-x_k, y_k = g_{k+1}-g_k.

Dua rumus pembaruan dipilih tim (mis. BFGS, DFP, SR1, Broyden). Karena matriks hanya 2x2,
"menyelesaikan" B d = -g harus dengan implementasi sendiri (mis. rumus invers 2x2 atau
pembaruan langsung pada H = B^{-1}); dilarang np.linalg.solve / inv.
"""
from __future__ import annotations

from typing import Callable

import numpy as np

from common import MAX_ITER, TOL, Problem, Result

UPDATES: dict[str, Callable] = {
    # "BFGS": ...,
    # "DFP": ...,
}


def quasi_newton(prob: Problem, x0: np.ndarray, linesearch: Callable, update: str,
                 tol: float = TOL, max_iter: int = MAX_ITER) -> Result:
    """Jalankan quasi-Newton dengan B_0 = I. Lewati/jaga pembaruan bila s^T y <= 0 (curvature)."""
    raise NotImplementedError
