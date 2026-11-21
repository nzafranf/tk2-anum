"""Pengukuran waktu (Tugas vii).

Protokol (dari soal): jam monoton beresolusi tinggi (time.perf_counter_ns); setelah pemanasan,
5 rangkaian x 100 panggilan per model; durasi rangkaian dibagi 100; laporkan MEDIAN dari 5
hasil, untuk pembentukan dan evaluasi terpisah. Di luar pengukuran: baca berkas, cetak,
hitung galat, buat grafik. Catat lingkungan (CPU, OS, versi Python/NumPy) untuk laporan.
"""
from __future__ import annotations

import platform
import sys
import time
from statistics import median

import numpy as np

N_CALLS = 100
N_RUNS = 5
N_WARMUP = 20


def time_callable(fn, n_calls: int = N_CALLS, n_runs: int = N_RUNS, n_warmup: int = N_WARMUP) -> float:
    """Median (dari n_runs) waktu per panggilan dalam detik."""
    for _ in range(n_warmup):
        fn()
    per_call = []
    for _ in range(n_runs):
        t0 = time.perf_counter_ns()
        for _ in range(n_calls):
            fn()
        per_call.append((time.perf_counter_ns() - t0) / n_calls / 1e9)
    return median(per_call)


def environment_info() -> dict[str, str]:
    return {"python": sys.version.split()[0], "numpy": np.__version__,
            "os": platform.platform(), "cpu": platform.processor()}
