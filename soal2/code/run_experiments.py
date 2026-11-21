"""Jalankan seluruh eksperimen Soal 2 dan tulis hasil ke ../results/.

    python soal2/code/run_experiments.py

Keluaran yang diharapkan:
  results/coef_poly.csv, coef_linear.csv, coef_cubic.csv   (Tugas i-iii)
  results/errors.csv                                       (Tugas iv: z_hat, z, |galat|, norma l2)
  results/fig1_curves.pdf, results/fig2_errors.pdf         (Tugas v)
  results/flops.csv                                        (Tugas vi)
  results/timing.csv + environment.json                    (Tugas vii)
Tabel LaTeX untuk laporan ditulis ke ../report/generated/*.tex agar angka tidak diketik manual.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RESULTS = Path(__file__).resolve().parents[1] / "results"


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    raise NotImplementedError("Lengkapi setelah models.py selesai.")


if __name__ == "__main__":
    main()
