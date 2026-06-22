<div align="center">
  <h1>🗜️ Lossless PNG Compression Analyzer</h1>
  <p><i>Studi Komparasi Algoritma Kompresi Gambar Interaktif Berkelas Enterprise</i></p>
  
  [![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
  [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

---

## 📖 Ringkasan

**Lossless PNG Compression Analyzer** adalah aplikasi berbasis web berperforma tinggi yang dikembangkan untuk mata kuliah **Sistem Multimedia**. Aplikasi ini menyediakan lingkungan interaktif untuk menguji (*benchmark*), memvisualisasikan, dan menganalisis secara mendalam mekanisme internal dari tiga metodologi kompresi data *lossless* pada gambar PNG.

Aplikasi ini berfokus untuk mendemonstrasikan perbedaan teoritis antara arsitektur pengkodean berbasis **Kamus (Dictionary-based)**, **Panjang Deretan (Run-Length-based)**, dan **Entropi Statistik (Entropy-based)** melalui eksekusi data secara *real-time*.

## ⚙️ Implementasi Algoritma

Proyek ini mengimplementasikan ketiga algoritma secara murni dalam bahasa Python, yang dioptimalkan secara ekstrem menggunakan fungsi bawaan tingkat-C (`memoryview`, `bytes.rfind`) untuk mencapai kecepatan proses maksimum tanpa bergantung pada pustaka eksternal C/C++.

1. **LZSS (Lempel-Ziv-Storer-Szymanski)**
   - **Pendekatan:** Kamus *Sliding-Window*.
   - **Mekanisme:** Mengganti urutan *byte* berulang dengan penunjuk `(Jarak, Panjang)` yang merujuk pada *buffer* riwayat data secara dinamis.
   - **Optimisasi:** Memanfaatkan fungsi `bytes.rfind()` bawaan Python untuk pencarian pola mundur yang sangat cepat.

2. **Modified RLE (Run-Length Encoding)**
   - **Pendekatan:** Pengelompokan Data Kontigu.
   - **Mekanisme:** Menyandikan urutan *byte* identik yang tidak terputus menjadi paket dua *byte* `(Header, Nilai)`. Secara elegan menangani blok data yang tidak dapat dikompresi (*literal blocks*).
   - **Optimisasi:** Pemindaian *pointer* memori (`memoryview`) untuk menghindari overhead dan beban komputasi Python.

3. **Arithmetic Coding**
   - **Pendekatan:** Pengkodean Entropi Statistik.
   - **Mekanisme:** Memetakan seluruh aliran *byte* gambar menjadi satu pecahan presisi tinggi di antara angka 0 dan 1, yang diatur oleh kamus probabilitas yang dikalkulasi di awal (Tabel Frekuensi).
   - **Optimisasi:** *Inlined bit-writer* dan batas probabilitas pra-kalkulasi (*pre-computed bounds*).

## ✨ Fitur Utama

- **Enterprise Dashboard UI:** Antarmuka yang bersih, profesional, responsif, dan mudah digunakan (berbasis Streamlit).
- **Validasi Pixel-Perfect:** Dilengkapi dengan uji integritas (PSNR = ∞) untuk menjamin bahwa hasil dekompresi 100% identik tanpa cacat dari data mentah aslinya.
- **Profiling Komposisi Data:** Menggunakan *Donut Charts* tersinkronisasi (Plotly) untuk membedah struktur anatomi *file* yang terkompresi secara visual (Misal: *Literal Bytes* vs *Dictionary Pointers*).
- **Automated Benchmarking:** Membandingkan waktu eksekusi (ms), rasio kompresi, dan bobot *byte* yang presisi secara berdampingan.
- **Ekspor Laporan CSV:** Pembuatan laporan analisis kuantitatif dengan satu klik untuk kebutuhan dokumentasi akademik.

## 🚀 Instalasi & Penggunaan

Untuk menjalankan aplikasi ini secara lokal di komputer Anda, ikuti langkah berikut:

### 1. Persyaratan Sistem
Pastikan Anda telah menginstal Python versi 3.9 atau yang lebih baru.

### 2. Kloning Repositori
```bash
git clone https://github.com/nazwaym/compression-algorithms-python.git
cd compression-algorithms-python
```

### 3. Instalasi Dependensi
Disarankan untuk menggunakan *virtual environment*.
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Aplikasi
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di *browser* bawaan Anda pada alamat `http://localhost:8501`.

## 🛠️ Stack Teknologi
- **Core Engine:** `Python 3`
- **Frontend / Framework:** `Streamlit`
- **Data Manipulation:** `NumPy`, `Pandas`
- **Image Processing:** `Pillow (PIL)`
- **Data Visualization:** `Plotly Graph Objects`

## 📝 Referensi Akademik
Dikembangkan untuk memenuhi kurikulum akademik mata kuliah Sistem Multimedia.

<p align="center">Dibuat dengan ❤️ untuk Kesempurnaan Teknikal</p>
