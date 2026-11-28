"""Jalankan seluruh eksperimen Soal 1 dan tulis hasil ke ../results/ serta ../report/generated/.

    python soal1/code/run_experiments.py

Keluaran:
  results/linesearch_table.csv         Tugas i   (uji, metode, iterasi, eval f, eval grad, f, ||g||)
  results/cgm_all_combinations.csv     Uji kombinasi CGM x pencari langkah
  results/qn_all_combinations.csv      Uji kombinasi Quasi-Newton x pencari langkah
  results/variants_table.csv           Tugas iii (8 baris perbandingan varian + jarak ke x*)
  results/trajectory.pdf               Tugas iv  (lintasan pada kontur log f, uji 1)
  results/gradnorm.pdf                 Tugas iv  (log_10 ||grad f||_2 vs iterasi k, uji 1)
  report/generated/linesearch_table.tex
  report/generated/variants_table.tex
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exp_linesearch  # noqa: E402
from cgm import BETA_RULES, cgm  # noqa: E402
from common import START_POINTS, X_STAR, Problem, Result  # noqa: E402
from linesearch import LINESEARCHES, binary_search  # noqa: E402
from quasi_newton import UPDATES, quasi_newton  # noqa: E402

BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
GENERATED = BASE / "report" / "generated"


def sci(v: float) -> str:
    r"""Notasi ilmiah LaTeX, mis. 4.83\times10^{-18}."""
    if v == 0.0:
        return "0"
    m, e = f"{v:.2e}".split("e")
    return m + r"\times10^{" + str(int(e)) + "}"


def are_equally_accurate(r1: Result, r2: Result, ratio_bound: float = 10.0) -> bool:
    """Dua hasil dinilai setara akurasinya bila keduanya konvergen dan ketiga ukuran
    galat akhir (f, ||grad f||_2, ||x - x*||_2) berada dalam satu orde besaran (< 10x).
    """
    if r1.converged != r2.converged:
        return False
    for a, b in ((r1.f, r2.f), (r1.gnorm, r2.gnorm), (r1.dist_to_opt, r2.dist_to_opt)):
        hi, lo = max(a, b), max(min(a, b), 1e-300)
        if hi / lo >= ratio_bound:
            return False
    return True


def choose_representative(r1: Result, r2: Result) -> Result:
    """Pilih satu hasil per algoritma pada Uji 1 sesuai aturan Tugas (iv):
    bila akurasi akhir setara, pilih iterasi paling sedikit (seri dipecah dengan
    total evaluasi fungsi + gradien terkecil); bila tidak setara, pilih yang lebih akurat.
    """
    if are_equally_accurate(r1, r2):
        return min((r1, r2), key=lambda r: (r.iters, r.n_f + r.n_g))
    return min((r1, r2), key=lambda r: (not r.converged, r.dist_to_opt, r.gnorm))


def rosenbrock_grid(xlim: tuple[float, float], ylim: tuple[float, float],
                    n: int = 400) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    X, Y = np.meshgrid(xs, ys)
    F = 100.0 * (Y - X ** 2) ** 2 + (1.0 - X) ** 2
    return X, Y, np.maximum(F, 1e-4)


def plot_trajectories(r_cgm: Result, r_qn: Result, out_path: Path) -> None:
    """Plot dua panel berdampingan lintasan x_k di atas kontur f berskala logaritmik."""
    mpl.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "font.size": 10,
        "axes.labelsize": 10.5,
        "axes.titlesize": 10.5,
    })
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5), constrained_layout=True)

    xlim_a, ylim_a = (-3.7, 2.7), (-0.6, 12.0)
    xlim_b, ylim_b = (-1.45, 1.70), (-0.15, 2.35)
    levels = np.logspace(-3, 4.5, 16)
    line_levels = np.logspace(-2, 4, 7)
    norm = LogNorm(vmin=1e-3, vmax=10 ** 4.5)

    configs = [
        (axes[0], r_cgm, xlim_a, ylim_a, "#c0392b",
         f"(a) CGM PR+ ({r_cgm.iters} iterasi)"),
        (axes[1], r_qn, xlim_b, ylim_b, "#1f618d",
         f"(b) Quasi-Newton BFGS ({r_qn.iters} iterasi)"),
    ]

    cf = None
    for ax, res, xlim, ylim, color, title in configs:
        X, Y, F = rosenbrock_grid(xlim, ylim)
        cf = ax.contourf(X, Y, F, levels=levels, norm=norm, cmap="YlGnBu",
                         alpha=0.80, extend="both")
        ax.contour(X, Y, F, levels=line_levels, norm=norm, colors="#5d6d7e",
                   linewidths=0.55, alpha=0.55)

        vx = np.linspace(xlim[0], xlim[1], 300)
        ax.plot(vx, vx ** 2, linestyle=":", color="#2c3e50", linewidth=1.0,
                alpha=0.75, label=r"Dasar lembah $y = x^2$")

        pts = np.array(res.path)
        ax.plot(pts[:, 0], pts[:, 1], "-o", color=color, linewidth=1.4,
                markersize=3.6, markerfacecolor="white", markeredgewidth=1.1,
                label=r"Lintasan $\mathbf{x}_k$", zorder=4)
        ax.plot(pts[0, 0], pts[0, 1], marker="s", linestyle="None",
                color="#111111", markersize=6.8,
                label=r"Titik awal $(-1.2, 1)$", zorder=6)
        ax.plot(X_STAR[0], X_STAR[1], marker="*", linestyle="None",
                markerfacecolor="#f1c40f", markeredgecolor="#111111",
                markeredgewidth=0.9, markersize=13.0,
                label=r"Titik minimum $(1, 1)$", zorder=7)
        ax.plot(pts[-1, 0], pts[-1, 1], marker="^", linestyle="None",
                markerfacecolor="none", markeredgecolor=color,
                markeredgewidth=1.7, markersize=8.5,
                label=r"Titik akhir $\mathbf{x}_K$", zorder=8)

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        ax.set_title(title)
        ax.legend(loc="upper right" if ax is axes[0] else "lower left",
                  fontsize=8.3, framealpha=0.92)

    rect = Rectangle(
        (xlim_b[0], ylim_b[0]),
        xlim_b[1] - xlim_b[0],
        ylim_b[1] - ylim_b[0],
        linewidth=1.1, edgecolor="#111111", facecolor="none", linestyle="--", zorder=5,
    )
    axes[0].add_patch(rect)
    axes[0].annotate(
        "Wilayah panel (b)", xy=(xlim_b[0], ylim_b[1]),
        xytext=(-3.50, 3.35), fontsize=8.0, color="#111111",
        bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": "#555555", "alpha": 0.90},
        arrowprops={"arrowstyle": "->", "color": "#111111", "lw": 0.9},
        zorder=7,
    )

    cbar = fig.colorbar(cf, ax=axes, shrink=0.92, pad=0.02)
    cbar.set_label(r"$f(x, y)$ (skala logaritmik)")
    fig.savefig(out_path)
    plt.close(fig)


def plot_gradnorm(r_cgm: Result, r_qn: Result, out_path: Path) -> None:
    """Plot log_10 ||grad f(x_k)||_2 terhadap nomor iterasi k pada Uji 1."""
    mpl.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "font.size": 10,
        "axes.labelsize": 10.5,
        "axes.titlesize": 10.5,
    })
    fig, ax = plt.subplots(figsize=(7.2, 3.9), constrained_layout=True)

    k_cgm = np.arange(len(r_cgm.gnorm_hist))
    k_qn = np.arange(len(r_qn.gnorm_hist))
    log_cgm = np.log10(np.maximum(r_cgm.gnorm_hist, 1e-30))
    log_qn = np.log10(np.maximum(r_qn.gnorm_hist, 1e-30))

    ax.plot(k_cgm, log_cgm, "-o", color="#c0392b", linewidth=1.4, markersize=4.0,
            markerfacecolor="white", markeredgewidth=1.1,
            label=f"CGM PR+ ({r_cgm.iters} iterasi)")
    ax.plot(k_qn, log_qn, "-s", color="#1f618d", linewidth=1.5, markersize=4.4,
            markerfacecolor="white", markeredgewidth=1.1,
            label=f"Quasi-Newton BFGS ({r_qn.iters} iterasi)")
    ax.axhline(-6.0, color="#2c3e50", linestyle="--", linewidth=1.0,
               label=r"Ambang konvergensi $\log_{10}(10^{-6}) = -6$")

    ax.set_xlabel(r"Nomor iterasi $k$")
    ax.set_ylabel(r"$\log_{10} \left\Vert \nabla f(\mathbf{x}_k) \right\Vert_2$")
    ax.set_xlim(-0.8, max(r_cgm.iters, r_qn.iters) + 1.2)
    ax.set_ylim(-7.6, 3.9)
    ax.grid(True, linestyle=":", linewidth=0.6, alpha=0.65)
    ax.legend(loc="upper right", fontsize=9.0, framealpha=0.92)
    fig.savefig(out_path)
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)

    # Tugas (i): jalankan skrip 1A agar seluruh berkas hasil konsisten.
    exp_linesearch.main()

    # Uji tambahan semua kombinasi Quasi-Newton x pencari langkah (bahan analisis).
    with open(RESULTS / "qn_all_combinations.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["uji", "varian", "pencari_langkah", "iterasi", "eval_f",
                    "eval_grad", "x1", "x2", "f_akhir", "gnorm_akhir",
                    "jarak_ke_x_star", "konvergen"])
        for u, x0 in START_POINTS.items():
            for upd in UPDATES:
                for key, ls in LINESEARCHES.items():
                    r = quasi_newton(Problem(), x0, ls, upd)
                    w.writerow([u, upd, key, r.iters, r.n_f, r.n_g, *r.x,
                                r.f, r.gnorm, r.dist_to_opt, r.converged])

    # Tugas (iii): jalankan keempat varian dengan binary_search pada kedua titik awal.
    by_test: dict[int, dict[str, Result]] = {1: {}, 2: {}}
    variant_rows = []
    tex_lines = []
    for u, x0 in START_POINTS.items():
        runs = [
            ("CGM", "FR", cgm(Problem(), x0, binary_search, "FR")),
            ("CGM", "PR+", cgm(Problem(), x0, binary_search, "PR+")),
            ("Quasi-Newton", "BFGS", quasi_newton(Problem(), x0, binary_search, "BFGS")),
            ("Quasi-Newton", "DFP", quasi_newton(Problem(), x0, binary_search, "DFP")),
        ]
        for alg, var, r in runs:
            by_test[u][f"{alg}-{var}"] = r
            variant_rows.append([
                u, alg, var, r.x[0], r.x[1], r.f, r.gnorm,
                r.dist_to_opt, r.iters, r.n_f, r.n_g, r.converged,
            ])
            x_str = f"({r.x[0]:.7f},\\,{r.x[1]:.7f})"
            tex_lines.append(
                f"{u} & {alg} & {var} & ${x_str}$ & ${sci(r.f)}$ & "
                f"${sci(r.gnorm)}$ & ${sci(r.dist_to_opt)}$ & {r.iters}\\\\\n"
            )
        if u == 1:
            tex_lines.append("\\midrule\n")

    with open(RESULTS / "variants_table.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["uji", "algoritma", "varian", "x1", "x2", "f_akhir",
                    "gnorm_akhir", "jarak_ke_x_star", "iterasi", "eval_f",
                    "eval_grad", "konvergen"])
        w.writerows(variant_rows)

    (GENERATED / "variants_table.tex").write_text("".join(tex_lines), encoding="utf-8")

    # Tugas (iv): pilih satu hasil per algoritma pada Uji 1 lalu buat kedua grafik.
    best_cgm = choose_representative(by_test[1]["CGM-FR"], by_test[1]["CGM-PR+"])
    best_qn = choose_representative(
        by_test[1]["Quasi-Newton-BFGS"], by_test[1]["Quasi-Newton-DFP"]
    )
    print(f"Pilihan visualisasi Uji 1: {best_cgm.name} ({best_cgm.iters} iter) vs "
          f"{best_qn.name} ({best_qn.iters} iter)")

    plot_trajectories(best_cgm, best_qn, RESULTS / "trajectory.pdf")
    plot_gradnorm(best_cgm, best_qn, RESULTS / "gradnorm.pdf")


if __name__ == "__main__":
    main()
