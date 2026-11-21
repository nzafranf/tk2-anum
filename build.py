"""Bangun PDF gabungan + ZIP submisi TK 2.

    python build.py            # semua: cover + soal1 + soal2 -> submission/
    python build.py soal1      # hanya satu laporan (cek cepat) -> build/soal1/soal1.pdf

Butuh: pdflatex (MiKTeX/TeX Live) di PATH dan `pip install pymupdf`.
Nama berkas mengikuti petunjuk: TK2_A9_<NPM...>.pdf / .zip
"""
from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
OUT = ROOT / "submission"
STEM = "TK2_A9_2406402542_2406429563_2406397196_2406431334"

PARTS = {  # nama -> (folder kerja, berkas tex)
    "cover": (ROOT / "common", "cover.tex"),
    "soal1": (ROOT / "soal1" / "report", "soal1.tex"),
    "soal2": (ROOT / "soal2" / "report", "soal2.tex"),
}


def latex(name: str) -> Path:
    workdir, tex = PARTS[name]
    outdir = BUILD / name
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
           f"-output-directory={outdir}", tex]
    for _ in range(2):  # 2 putaran: daftar isi dan rujukan silang
        r = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-3000:])
            sys.exit(f"pdflatex gagal pada {name}; lihat {outdir / (Path(tex).stem + '.log')}")
    return outdir / (Path(tex).stem + ".pdf")


def package(pdf: Path) -> Path:
    keep = [ROOT / "README.md", ROOT / "requirements.txt"]
    for d in ("soal1/code", "soal2/code", "soal1/results", "soal2/results"):
        keep += [p for p in (ROOT / d).rglob("*")
                 if p.is_file() and "__pycache__" not in p.parts and p.name != ".gitkeep"]
    zpath = OUT / f"{STEM}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(pdf, pdf.name)
        for p in sorted(set(keep)):
            z.write(p, p.relative_to(ROOT))
    return zpath


def main() -> None:
    if len(sys.argv) > 1:
        print("PDF:", latex(sys.argv[1]))
        return
    import pymupdf  # noqa: WPS433 (import lokal: hanya perlu untuk build penuh)

    OUT.mkdir(exist_ok=True)
    pdf = OUT / f"{STEM}.pdf"
    with pymupdf.open() as merged:
        for name in ("cover", "soal1", "soal2"):
            with pymupdf.open(latex(name)) as part:
                merged.insert_pdf(part)
        merged.save(pdf, garbage=4, deflate=True)
    print("PDF:", pdf)
    print("ZIP:", package(pdf))


if __name__ == "__main__":
    main()
