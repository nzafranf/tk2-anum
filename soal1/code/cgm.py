"""Conjugate Gradient Method nonlinear (Tugas i-ii). d_{k+1} = -g_{k+1} + beta_k d_k.

Dua rumus beta_k dipilih tim (mis. Fletcher-Reeves, Polak-Ribiere+, Hestenes-Stiefel, Dai-Yuan).
"""
from __future__ import annotations

from typing import Callable

import numpy as np

from common import MAX_ITER, TOL, Problem, Result

# beta_rule(g_new, g_old, d_old) -> float
BETA_RULES: dict[str, Callable[[np.ndarray, np.ndarray, np.ndarray], float]] = {
    # "FR": ...,
    # "PR+": ...,
}


def cgm(prob: Problem, x0: np.ndarray, linesearch: Callable, beta: str,
        tol: float = TOL, max_iter: int = MAX_ITER) -> Result:
    """Jalankan CGM. Henti saat ||g|| <= tol atau iterasi = max_iter.

    linesearch: pembungkus yang cocok dengan linesearch.binary_search / armijo.
    Restart ke -g bila d bukan arah turun. Isi Result.path dan Result.gnorm_hist
    (indeks 0 = titik awal) dan salin prob.n_f / prob.n_g ke Result.
    """
    raise NotImplementedError
