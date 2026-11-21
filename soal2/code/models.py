"""Antarmuka model Soal 2. Tiga keluarga model, semuanya dengan pola yang sama:

    model = fit_xxx(t_train, z_train, ...)   # PEMBENTUKAN (dihitung ulang dari data tiap panggilan)
    z_hat = model.eval(t)                    # EVALUASI    (memakai koefisien yang sudah jadi)

`model.coef` menyimpan koefisien untuk tabel laporan. Aturan TK: Gauss pivot parsial,
Horner, dan algoritma spline diimplementasikan sendiri (dilarang numpy.linalg.solve,
np.polyfit, scipy.interpolate, dst.).

Pembagian: polinomial + spline linear + spline kubik -> lihat WORK_SPLIT.md.
Hitung FLOP berdasarkan algoritma yang BENAR-BENAR dijalankan: `flops.py` menghitung
secara analitik dan boleh diverifikasi dengan penghitung operasi (opsional).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Model:
    name: str
    coef: np.ndarray              # format bebas per model (jelaskan di docstring fit_*)

    def eval(self, t):            # t: skalar atau array -> z_hat
        raise NotImplementedError


# ---------- Tugas (i): polinomial basis standar ----------
def gauss_pivot_solve(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Eliminasi Gauss pivot parsial + substitusi mundur (implementasi sendiri)."""
    raise NotImplementedError


def horner(c: np.ndarray, x):
    """Evaluasi sum_k c[k] x^k dengan skema Horner."""
    raise NotImplementedError


def fit_poly(t: np.ndarray, z: np.ndarray, d: int) -> Model:
    """Ambil d+1 titik latih dengan indeks i_j = floor(9 j / d + 1/2), j = 0..d;
    x = 2 t / 9 - 1; bentuk Vandermonde; selesaikan dengan gauss_pivot_solve."""
    raise NotImplementedError


# ---------- Tugas (ii): spline linear ----------
def fit_linear_spline(t: np.ndarray, z: np.ndarray) -> Model:
    """Koefisien per segmen dalam koordinat lokal (t - t_i): S_i(t) = a_i + b_i (t - t_i)."""
    raise NotImplementedError


# ---------- Tugas (iii): spline kubik natural ----------
def fit_natural_cubic_spline(t: np.ndarray, z: np.ndarray) -> Model:
    """S_i(t) = a_i + b_i (t - t_i) + c_i (t - t_i)^2 + d_i (t - t_i)^3, S'' = 0 di kedua ujung.
    Sebutkan algoritma yang dipakai (mis. Sauer) di laporan."""
    raise NotImplementedError
