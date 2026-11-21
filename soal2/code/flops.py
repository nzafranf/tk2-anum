"""Hitungan FLOP (Tugas vi).

Konvensi soal: tiap +, -, *, / bilangan riil = 1 FLOP. Pembandingan, pengindeksan, pemindahan
data TIDAK dihitung. Operasi penyusunan sistem / pembentukan koefisien DIHITUNG.
Pisahkan: (a) pembentukan model, (b) evaluasi pada 5 titik uji.

Tulis fungsi analitik, mis. flops_fit_poly(d), flops_eval_poly(d, n_pts=5), ...
dan sertakan penurunan rumus di laporan. Verifikasi dengan penghitung operasi pada
implementasi (opsional, tapi sangat membantu menghindari selisih hitung).
"""
from __future__ import annotations


def flops_fit_poly(d: int) -> int:
    raise NotImplementedError


def flops_eval_poly(d: int, n_pts: int = 5) -> int:
    raise NotImplementedError


def flops_fit_linear_spline(n: int = 10) -> int:
    raise NotImplementedError


def flops_eval_linear_spline(n_pts: int = 5) -> int:
    raise NotImplementedError


def flops_fit_cubic_spline(n: int = 10) -> int:
    raise NotImplementedError


def flops_eval_cubic_spline(n_pts: int = 5) -> int:
    raise NotImplementedError
