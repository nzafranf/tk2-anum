# Usulan Pembagian Kerja -- Kelompok A9

Prinsip: setiap anggota **memiliki kode + bagian laporan** untuk potongannya sendiri (satu orang paham ujung ke ujung),
dua orang per soal, beban relatif seimbang, dan ketergantungan antar-orang dibatasi lewat antarmuka yang sudah
ditetapkan di skeleton (`soal1/code/common.py`, `soal2/code/models.py`).

## Soal 1 -- Optimisasi Rosenbrock (CGM vs Quasi-Newton)

| Anggota | Tugas | Kode | Bagian laporan |
|---|---|---|---|
| **Naufal Zafran Fadil** | **1A: pencarian langkah + CGM.** (i) binary search & Armijo, pilih satu varian CGM, tabel 4 baris + keputusan metode; (ii) dua rumus beta_k untuk CGM | `linesearch.py`, `cgm.py` | Sec. 2 (Pencarian Langkah), sub-bagian CGM di Sec. 3 |
| **AMAR HAKIM** | **1B: quasi-Newton + perbandingan + visual.** (ii) dua rumus pembaruan QN (invers 2x2 sendiri); (iii) tabel 8 baris + jarak ke x*; (iv) kontur log f + lintasan + grafik log gradien, kriteria kesetaraan akurasi; (v) analisis 4 pertanyaan | `quasi_newton.py`, `run_experiments.py` | Sub-bagian QN di Sec. 3, Sec. 4, 5, 6 |

Alur: 1A mengunci `linesearch.binary_search/armijo` dan `cgm()` lebih dulu (mereka dipakai 1B). 1B mulai dari `quasi_newton()`
sambil memakai line search sementara (mis. Armijo ringkas) sampai versi 1A masuk. Pendahuluan, Rangkuman, Kesimpulan Soal 1: **AMAR** (menulis terakhir).

## Soal 2 -- Prediksi Data Hilang (Polinomial dan Spline)

| Anggota | Tugas | Kode | Bagian laporan |
|---|---|---|---|
| **Refki Septian** | **2A: pembentukan model.** (i) polinomial d=2..9, Vandermonde, Gauss pivot parsial, Horner, tabel koefisien; (ii) spline linear; (iii) spline kubik natural (algoritma Sauer) | `models.py` | Sec. 2 (Data), 3, 4, 5 |
| **JENISA BUNGA SOLAGRACIA** | **2B: evaluasi dan analisis.** (iv) prediksi + galat + norma l2; (v) dua gambar; (vi) hitungan FLOP; (vii) waktu eksekusi (protokol 5x100, median); (viii) analisis | `run_experiments.py`, `flops.py`, `timing.py` | Sec. 6--10 |

Alur: 2A mengunci antarmuka `fit_*()` -> `Model.eval()` (sudah dikerangkakan) dan menyerahkan struktur koefisien + jumlah operasi per langkah
(2B butuh ini untuk FLOP). 2B bisa mulai dari skeleton: grafik, protokol timing, dan penurunan FLOP analitik tidak bergantung pada kode final.
Pendahuluan, Rangkuman, Kesimpulan Soal 2: **JENISA**.

## Tugas lintas-soal

| Hal | Penanggung jawab |
|---|---|
| Repo, `build.py`, merge PDF + ZIP, README, penamaan berkas, submit | Naufal |
| Sampul, pakta integritas, tanda tangan (4 file di `ignore/`) | Naufal mengumpulkan; tiap anggota kirim tanda tangannya |
| Silang-review: tiap orang membaca bagian milik pasangan soal lain (kebenaran angka, tata bahasa, penomoran, setiap gambar/tabel dijelaskan di teks) | Naufal <-> Jenisa, Amar <-> Refki (lihat jadwal) |
| Persentase kontribusi (`common/cover.tex`) | default 25% masing-masing; ubah bila sepakat lain |

## Usulan jadwal (deadline Sab 5 Des 2026, 23.59 WIB; target submit Sab 5 Des sebelum 22.30)

| Tanggal | Target |
|---|---|
| Sab 21 -- Mar 24 Nov | Kode inti masing-masing selesai dan lolos uji sendiri (1A: line search + CGM, 1B: QN, 2A: tiga model). Tulis bagian metode di laporan. |
| Rab 25 -- Sen 30 Nov | Eksperimen penuh (`run_experiments.py`), tabel/grafik ter-generate, bagian hasil + analisis ditulis. FLOP dan timing selesai. |
| Sel 1 -- Rab 2 Des | Silang-review, rapikan, tulis Pendahuluan/Kesimpulan/Rangkuman terakhir. Cek format vs Petunjuk. |
| Kam 3 Des | Build final, kumpulkan tanda tangan, cek PDF halaman per halaman, uji README di mesin bersih. |
| Jum 4 Des | Cadangan (buffer). Submit paling lambat Sab 5 Des 22.30. |

## Konvensi kerja (supaya tidak saling menimpa)

- Satu branch per orang: `naufal/soal1a`, `amar/soal1b`, `refki/soal2a`, `jenisa/soal2b`; merge ke `main` lewat PR kecil.
  Setiap orang hanya mengedit berkas miliknya (kolom "Kode" dan "Bagian laporan" di atas). Mau ubah antarmuka bersama
  (`common.py`, signature `models.py`) -> kabari grup dulu.
- Angka di laporan **jangan diketik manual**: `run_experiments.py` menulis CSV di `results/` dan tabel LaTeX ke `report/generated/`;
  laporan memakai `\isitabel{generated/xxx.tex}`.
- Bagian laporan yang belum ada isinya ditandai `% TODO` di `soal1.tex` / `soal2.tex`; jangan hapus komentar struktur sampai terisi.
- Setiap pseudocode/gambar/tabel: caption + dirujuk + dijelaskan di teks.

## Alternatif jika beban terasa timpang

Soal 2 secara kode lebih ringan (3 model) tetapi lebih banyak bagian laporan (FLOP, waktu); Soal 1 lebih berat di eksperimen dan tuning
(line search, CGM/QN rentan gagal konvergen pada Rosenbrock). Bila 1A/1B kewalahan, Refki (2A) bisa mengambil
bagian (iv) visualisasi Soal 1 setelah `models.py` selesai.
