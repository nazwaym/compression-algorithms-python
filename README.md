<div align="center">
  <h1>🗜️ Lossless PNG Compression Analyzer</h1>
  <p><i>An Interactive, Enterprise-Grade Comparative Study of Image Compression Algorithms</i></p>
  
  [![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
  [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

---

## 📖 Overview

**Lossless PNG Compression Analyzer** is a high-performance, web-based tool developed for the **Multimedia Systems (Sistem Multimedia)** course. It provides an interactive environment to benchmark, visualize, and analyze the internal mechanics of three distinct lossless data compression methodologies on PNG images.

The application focuses on demonstrating the theoretical differences between **Dictionary-based**, **Run-Length-based**, and **Entropy-based** encoding architectures through real-time execution and visualization.

## ⚙️ Algorithms Implemented

This project implements three algorithms purely in Python, heavily optimized using C-level backend functions (`memoryview`, `bytes.rfind`) to achieve maximum processing speed without relying on external C/C++ extensions.

1. **LZSS (Lempel-Ziv-Storer-Szymanski)**
   - **Approach:** Sliding-Window Dictionary.
   - **Mechanics:** Replaces recurring byte sequences with a `(Distance, Length)` pointer referencing a dynamic history buffer.
   - **Optimization:** Utilizes Python's native `bytes.rfind()` for ultra-fast backward pattern matching.

2. **Modified RLE (Run-Length Encoding)**
   - **Approach:** Contiguous Data Grouping.
   - **Mechanics:** Encodes unbroken sequences of identical bytes into two-byte packets `(Header, Value)`. Handles non-compressible data gracefully using literal blocks.
   - **Optimization:** Memory pointer (`memoryview`) scanning to avoid redundant string allocation.

3. **Arithmetic Coding**
   - **Approach:** Statistical Entropy Encoding.
   - **Mechanics:** Maps the entire byte stream into a highly precise fractional number between 0 and 1, governed by a pre-calculated probability dictionary (Frequency Table).
   - **Optimization:** Inlined bit-writer and pre-computed probability bounds.

## ✨ Key Features

- **Enterprise Dashboard UI:** A clean, professional, and responsive interface built with Streamlit.
- **Pixel-Perfect Validation:** Includes an integrity check (PSNR = ∞) to guarantee that decompression results in a 100% identical copy of the original raw data.
- **Data Composition Profiling:** Uses synchronized Donut Charts (Plotly) to visually dissect the anatomy of the compressed file (e.g., Literal Bytes vs. Dictionary Pointers).
- **Automated Benchmarking:** Compares execution time (ms), compression ratios, and exact byte sizes side-by-side.
- **CSV Export:** One-click generation of quantitative analysis reports for academic documentation.

## 🚀 Installation & Usage

To run this application locally on your machine, follow these steps:

### 1. Prerequisites
Ensure you have Python 3.9 or newer installed.

### 2. Clone the Repository
```bash
git clone https://github.com/nazwaym/compression-algorithms-python.git
cd compression-algorithms-python
```

### 3. Install Dependencies
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```
The application will automatically open in your default web browser at `http://localhost:8501`.

## 🛠️ Technology Stack
- **Core Engine:** `Python 3`
- **Frontend / Framework:** `Streamlit`
- **Data Manipulation:** `NumPy`, `Pandas`
- **Image Processing:** `Pillow (PIL)`
- **Data Visualization:** `Plotly Graph Objects`

## 📝 Acknowledgments
Developed as a fulfillment for the Multimedia Systems curriculum.

<p align="center">Made with ❤️ for Engineering Excellence</p>
