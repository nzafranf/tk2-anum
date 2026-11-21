# TK 2 Analisis Numerik -- Kelompok A9 (Optimisasi & Interpolasi)

Anggota: Naufal Zafran Fadil (2406402542), AMAR HAKIM (2406429563), Refki Septian (2406397196), JENISA BUNGA SOLAGRACIA (2406431334).
Deadline: **Sabtu, 5 Desember 2026, 23.59 WIB** (target submit paling lambat 1 jam sebelumnya).

Pembagian kerja: lihat [`WORK_SPLIT.md`](WORK_SPLIT.md). Soal dan petunjuk penulisan: `docs/`.

## Struktur

```
common/            preamble.tex (format laporan) + cover.tex (halaman sampul, pakta integritas, tanda tangan)
soal1/code/        Rosenbrock: common.py, linesearch.py, cgm.py, quasi_newton.py, run_experiments.py
soal1/results/     CSV + grafik hasil (dibuat run_experiments.py)
soal1/report/      soal1.tex  (+ generated/ = tabel LaTeX otomatis, figures/)
soal2/code/        Interpolasi: data.py, models.py, flops.py, timing.py, run_experiments.py
soal2/results/     CSV + grafik hasil
soal2/report/      soal2.tex  (+ generated/, figures/)
ignore/            tanda tangan ttd_naufal.png, ttd_amar.png, ttd_refki.png, ttd_jenisa.png (TIDAK di-commit)
build.py           menggabung cover + soal1 + soal2 -> submission/TK2_A9_<NPM>.pdf dan .zip
```

## Menjalankan

Python 3.12, lalu `pip install -r requirements.txt`.

```bash
python soal1/code/run_experiments.py     # hasil Soal 1 -> soal1/results/
python soal2/code/run_experiments.py     # hasil Soal 2 -> soal2/results/
python build.py soal1                    # cek cepat satu laporan -> build/soal1/soal1.pdf
python build.py                          # PDF gabungan + ZIP -> submission/
```

Butuh `pdflatex` (MiKTeX/TeX Live) di PATH. Tiap laporan bisa dikompilasi sendiri-sendiri
sehingga anggota tidak saling mengganggu; `build.py` yang menggabungkannya.

## Aturan dari soal (jangan dilanggar)

- Dilarang pustaka algoritma utama (transformasi matriks, penyelesaian SPL, kuadrat terkecil,
  `scipy.optimize`, `scipy.interpolate`, `np.polyfit`, `np.linalg.solve/inv`, dst.). Implementasi sendiri.
  numpy hanya untuk array/aritmetika dasar; matplotlib untuk grafik.
- Halaman pertama berkas: pernyataan "Dengan ini, kami menyatakan bahwa tugas ini adalah hasil pekerjaan kelompok sendiri"
  + tanda tangan semua anggota (sudah ada di `common/cover.tex`). Tanpa ini project tidak diperiksa.
- Nama berkas: `TK2_A9_<NPM...>.pdf` dan `.zip` (ZIP berisi kode + README ini). Yang mengumpulkan cukup 1 anggota.
- Kode yang dirujuk laporan harus disebut namanya di laporan.

## Aturan penulisan laporan (ringkas dari Petunjuk Penulisan)

- Dua technical report (Soal 1 dan Soal 2) dalam satu PDF; A4, font standar LaTeX 12pt, margin >= 2.54 cm.
- Urutan: Judul (1 baris) -> Rangkuman (~1/2 hal) -> Daftar Isi (~1/2 hal) -> Pendahuluan (1/2--1 hal) ->
  Bagian isi bernomor (2--7 hal) -> Kesimpulan (1/2--1 hal) -> Referensi -> Lampiran (1--3 hal).
  Judul, rangkuman, daftar isi **tidak dinomori**; sisanya mulai dari 1. Template sudah mengikuti urutan ini.
- Gambar/tabel/kode dinomori per bagian (Tabel 3.1, Gambar 3.2, Kode 3.1), punya caption, dan **harus dijelaskan di teks**
  dekat objeknya (jangan masukkan jika tidak dijelaskan). Tabel rumit -> Lampiran.
- Prosedur ditulis sebagai pseudocode di badan laporan (`algorithm` + `algpseudocode`); kode asli di Lampiran.
  Pembaca harus paham tanpa membuka program.
- Setiap variabel dalam rumus dijelaskan sebelum dipakai. Rumus penting ditulis satu baris sendiri.
- Referensi: buku/paper/URL; **jangan** merujuk slide kuliah. Sumber ide/fakta orang lain wajib dirujuk.
- Urutan menulis yang disarankan: bagian isi -> Kesimpulan -> Pendahuluan -> Rangkuman.
- Penilaian: kebenaran 70%, penyusunan 20%, format & tata bahasa 10%.
