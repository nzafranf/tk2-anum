
"""Jalankan eksperimen Soal 2: Prediksi Data Hilang."""

from __future__ import annotations

import sys
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from data import (
    T_TRAIN, Z_TRAIN,
    T_TEST, Z_TEST,
    T_MIN, T_MAX, N_GRID, DEGREES
)

from models import (
    fit_poly,
    fit_linear_spline,
    fit_natural_cubic_spline
)

from timing import time_callable, environment_info

RESULTS = Path(__file__).resolve().parents[1] / "results"
GENERATED = (
    Path(__file__).resolve().parents[1]
    / "report" / "generated"
)


def build_models():
    """Membentuk seluruh model menggunakan data latih."""
    models = {}

    for d in DEGREES:
        models[f"Polynomial {d}"] = fit_poly(
            T_TRAIN, Z_TRAIN, d
        )

    models["Linear Spline"] = fit_linear_spline(
        T_TRAIN, Z_TRAIN
    )

    models["Natural Cubic Spline"] = fit_natural_cubic_spline(
        T_TRAIN, Z_TRAIN
    )

    return models


def evaluate_models(models):
    """Menghitung prediksi, galat absolut, dan norma L2."""
    rows = []

    for name, model in models.items():
        predictions = np.asarray(model.eval(T_TEST))

        errors = predictions - Z_TEST
        abs_errors = np.abs(errors)
        l2_error = np.sqrt(np.sum(errors ** 2))

        for k in range(len(T_TEST)):
            rows.append({
                "model": name,
                "t": T_TEST[k],
                "z_actual": Z_TEST[k],
                "z_predicted": predictions[k],
                "abs_error": abs_errors[k],
                "l2_error": l2_error
            })

    return pd.DataFrame(rows)
def plot_curves(models):
    """Gambar 1: Perbandingan kurva interpolasi."""
    t_grid = np.linspace(T_MIN, T_MAX, N_GRID)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Panel A: Polinomial
    for d in DEGREES:
        name = f"Polynomial {d}"
        axes[0].plot(
            t_grid,
            models[name].eval(t_grid),
            label=f"d = {d}"
        )

    # Panel B: Spline
    for name in ["Linear Spline", "Natural Cubic Spline"]:
        axes[1].plot(
            t_grid,
            models[name].eval(t_grid),
            label=name
        )

    axes[0].set_title("Interpolasi Polinomial")
    axes[1].set_title("Interpolasi Spline")

    for ax in axes:
        ax.scatter(
            T_TRAIN, Z_TRAIN,
            color="black", marker="o",
            label="Data latih", zorder=5
        )

        ax.scatter(
            T_TEST, Z_TEST,
            color="red", marker="x",
            label="Data uji", zorder=6
        )

        ax.set_xlabel("Waktu (s)")
        ax.set_ylabel("Amplitudo (mm)")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(RESULTS / "fig1_curves.pdf")
    plt.close(fig)


def plot_errors(errors):
    """Gambar 2: Perbandingan galat interpolasi."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Panel A: Galat absolut
    for name, group in errors.groupby("model"):
        axes[0].plot(
            group["t"],
            group["abs_error"],
            marker="o",
            label=name
        )

    axes[0].set_title("Galat Absolut")
    axes[0].set_xlabel("Waktu uji (s)")
    axes[0].set_ylabel("Galat absolut (mm)")
    axes[0].set_xticks(T_TEST)
    axes[0].legend(fontsize=8)

    # Panel B: Norma L2
    l2 = errors.groupby("model")["l2_error"].first()

    axes[1].plot(
        DEGREES,
        [l2[f"Polynomial {d}"] for d in DEGREES],
        marker="o",
        label="Polinomial"
    )

    axes[1].axhline(
        l2["Linear Spline"],
        linestyle="--",
        label="Linear Spline"
    )

    axes[1].axhline(
        l2["Natural Cubic Spline"],
        linestyle="--",
        label="Natural Cubic Spline"
    )

    axes[1].set_title("Perbandingan Norma L2")
    axes[1].set_xlabel("Derajat polinomial")
    axes[1].set_ylabel("Norma L2 galat (mm)")
    axes[1].set_xticks(DEGREES)
    axes[1].legend()

    for ax in axes:
        ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(RESULTS / "fig2_errors.pdf")
    plt.close(fig)

def benchmark_models(models):
    """Mengukur waktu pembentukan dan evaluasi."""
    rows = []

    factories = {}

    for d in DEGREES:
        factories[f"Polynomial {d}"] = (
            lambda d=d: fit_poly(T_TRAIN, Z_TRAIN, d)
        )

    factories["Linear Spline"] = (
        lambda: fit_linear_spline(T_TRAIN, Z_TRAIN)
    )

    factories["Natural Cubic Spline"] = (
        lambda: fit_natural_cubic_spline(T_TRAIN, Z_TRAIN)
    )

    for name, factory in factories.items():

        # Waktu pembentukan model
        fit_time = time_callable(factory)

        # Waktu evaluasi lima titik uji
        model = models[name]

        eval_time = time_callable(
            lambda: model.eval(T_TEST)
        )

        rows.append({
            "model": name,
            "fit_time_s": fit_time,
            "eval_time_s": eval_time,
            "fit_time_us": fit_time * 1e6,
            "eval_time_us": eval_time * 1e6
        })

    return pd.DataFrame(rows)

def export_latex_tables(errors, timings):
    """Membuat tabel LaTeX dari hasil eksperimen."""
    GENERATED.mkdir(parents=True, exist_ok=True)

    # Tabel prediksi dan galat absolut
    prediction_table = errors[
        ["model", "t", "z_actual",
         "z_predicted", "abs_error"]
    ].copy()

    prediction_table.to_latex(
        GENERATED / "predictions.tex",
        index=False,
        float_format="%.8f",
        escape=True
    )

    # Tabel norma L2
    l2_table = (
        errors.groupby("model", sort=False)["l2_error"]
        .first()
        .reset_index()
    )

    l2_table.to_latex(
        GENERATED / "l2_errors.tex",
        index=False,
        float_format="%.8f",
        escape=True
    )

    # Tabel waktu eksekusi
    timing_table = timings[
        ["model", "fit_time_us", "eval_time_us"]
    ].copy()

    timing_table.to_latex(
        GENERATED / "timing.tex",
        index=False,
        float_format="%.4f",
        escape=True
    )

def main():
    RESULTS.mkdir(exist_ok=True)

    models = build_models()

    # Prediksi dan galat
    errors = evaluate_models(models)
    errors.to_csv(
        RESULTS / "errors.csv",
        index=False
    )

    # Visualisasi
    plot_curves(models)
    plot_errors(errors)

    # Pengukuran waktu
    timings = benchmark_models(models)
    timings.to_csv(
        RESULTS / "timing.csv",
        index=False
    )

    # Lingkungan eksekusi
    with open(
        RESULTS / "environment.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(environment_info(), f, indent=4)

    # Ekspor tabel LaTeX
    export_latex_tables(errors, timings)

    print(errors.to_string(index=False))
    print(timings.to_string(index=False))


if __name__ == "__main__":
    main()
