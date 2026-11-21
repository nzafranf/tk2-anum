"""Jalankan seluruh eksperimen Soal 1 dan tulis hasil ke ../results/ (CSV + PNG/PDF).

    python soal1/code/run_experiments.py

Keluaran yang diharapkan (nama dipakai oleh laporan; ubah bersama):
  results/linesearch_table.csv   Tugas i   (uji, metode, iterasi, eval f, eval grad, f akhir, ||g|| akhir)
  results/variants_table.csv     Tugas iii (8 baris, + jarak ke x*)
  results/trajectory.pdf         Tugas iv  (lintasan di kontur log f, uji 1)
  results/gradnorm.pdf           Tugas iv  (log ||g|| vs k)
Tabel LaTeX untuk laporan ditulis ke ../report/generated/*.tex agar angka tidak diketik manual.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RESULTS = Path(__file__).resolve().parents[1] / "results"


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    raise NotImplementedError("Lengkapi setelah linesearch/cgm/quasi_newton selesai.")


if __name__ == "__main__":
    main()
