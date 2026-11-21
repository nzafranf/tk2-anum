"""Data Soal 2 (Tabel 2 dan 3 pada soal). Hanya data latih yang boleh dipakai membentuk model."""
import numpy as np

T_TRAIN = np.arange(10, dtype=float)
Z_TRAIN = np.array([
    0.03501094, 0.05515598, 0.09835319, 0.21396731, 0.60645765,
    0.91460833, 0.33256351, 0.13532421, 0.07021726, 0.04244032,
])

T_TEST = np.array([0.25, 1.5, 4.5, 7.5, 8.75])
Z_TEST = np.array([0.03887572, 0.07225289, 0.94117647, 0.09517515, 0.04761730])

T_MIN, T_MAX = 0.0, 9.0
N_GRID = 201                      # titik evaluasi kurva untuk grafik (sama jarak pada [0, 9])
DEGREES = tuple(range(2, 10))     # d = 2..9
