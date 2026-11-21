"""Eksperimen 1A: Tugas (i) pemilihan pencarian langkah + uji awal CGM (Tugas ii).

    python soal1/code/exp_linesearch.py

Varian CGM untuk Tugas (i): PR+ (VARIANT). Keluaran:
  results/linesearch_table.csv         tabel Tugas (i)
  results/cgm_all_combinations.csv    FR dan PR+ x kedua pencari langkah x kedua titik awal (bahan analisis)
  report/generated/linesearch_table.tex  isi tabular siap \\isitabel
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cgm import BETA_RULES, cgm                      # noqa: E402
from common import START_POINTS, Problem  # noqa: E402
from linesearch import LINESEARCHES      # noqa: E402

BASE = Path(__file__).resolve().parents[1]
VARIANT = "PR+"
LABEL = {"binary": "Binary search", "armijo": "Armijo"}


def main() -> None:
    (BASE / "results").mkdir(exist_ok=True)
    (BASE / "report" / "generated").mkdir(parents=True, exist_ok=True)
    rows = []
    for u, x0 in START_POINTS.items():
        for key, ls in LINESEARCHES.items():
            r = cgm(Problem(), x0, ls, VARIANT)
            rows.append([u, LABEL[key], r.iters, r.n_f, r.n_g, r.f, r.gnorm, r.converged])
    with open(BASE / "results" / "linesearch_table.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["uji", "metode", "iterasi", "eval_f", "eval_grad", "f_akhir", "gnorm_akhir", "konvergen"])
        w.writerows(rows)
    with open(BASE / "results" / "cgm_all_combinations.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["uji", "beta", "pencari_langkah", "iterasi", "eval_f", "eval_grad",
                    "x1", "x2", "f_akhir", "gnorm_akhir", "jarak_ke_x_star", "konvergen"])
        for u, x0 in START_POINTS.items():
            for b in BETA_RULES:
                for key, ls in LINESEARCHES.items():
                    r = cgm(Problem(), x0, ls, b)
                    w.writerow([u, b, key, r.iters, r.n_f, r.n_g, *r.x, r.f, r.gnorm,
                                r.dist_to_opt, r.converged])
    tex = "".join(
        f"{u} & {m} & {it} & {nf} & {ng} & ${f:.2e}$ & ${gn:.2e}$\\\\\n"
        for u, m, it, nf, ng, f, gn, _ in rows)
    (BASE / "report" / "generated" / "linesearch_table.tex").write_text(tex, encoding="utf-8")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
