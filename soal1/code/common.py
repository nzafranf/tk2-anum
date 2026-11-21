"""Antarmuka bersama Soal 1 (Rosenbrock). JANGAN ubah tanda tangan fungsi tanpa kabar ke anggota lain.

Semua algoritma (pencarian langkah, CGM, quasi-Newton) memakai `Problem` agar jumlah
evaluasi f dan grad f tercatat otomatis dan terpisah (syarat tabel Tugas i).
Aturan TK: DILARANG memakai pustaka algoritma utama (solve, lstsq, optimize.minimize, dst.).
numpy hanya untuk array dan aritmetika dasar.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

X_STAR = np.array([1.0, 1.0])
START_POINTS = {1: np.array([-1.2, 1.0]), 2: np.array([3.0, -2.0])}
TOL = 1e-6        # ||grad f||_2 <= TOL
MAX_ITER = 10_000


class Problem:
    """Fungsi Rosenbrock + penghitung evaluasi."""

    def __init__(self) -> None:
        self.n_f = 0
        self.n_g = 0

    def f(self, x: np.ndarray) -> float:
        self.n_f += 1
        return 100.0 * (x[1] - x[0] ** 2) ** 2 + (1.0 - x[0]) ** 2

    def grad(self, x: np.ndarray) -> np.ndarray:
        self.n_g += 1
        return np.array([
            -400.0 * x[0] * (x[1] - x[0] ** 2) - 2.0 * (1.0 - x[0]),
            200.0 * (x[1] - x[0] ** 2),
        ])

    def reset(self) -> None:
        self.n_f = 0
        self.n_g = 0


@dataclass
class Result:
    """Keluaran seragam semua solver (dipakai tabel dan grafik)."""

    name: str                      # mis. "CGM-FR" / "QN-BFGS"
    x: np.ndarray                  # titik akhir
    f: float                       # f akhir
    gnorm: float                   # ||grad f||_2 akhir
    iters: int
    n_f: int                       # evaluasi f
    n_g: int                       # evaluasi grad f
    converged: bool
    path: list[np.ndarray] = field(default_factory=list)       # x_k, k = 0..iters
    gnorm_hist: list[float] = field(default_factory=list)      # ||g_k||, k = 0..iters

    @property
    def dist_to_opt(self) -> float:
        return float(np.linalg.norm(self.x - X_STAR))
