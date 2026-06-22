"""
Studi Komparasi Algoritma Kompresi Gambar PNG
=================================================
Algoritma: LZSS, Modified RLE, Arithmetic Coding
Antarmuka: Enterprise/Professional UI (Bahasa Indonesia)
"""

import streamlit as st
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time, struct, math, io
from collections import Counter

# ════════════════════════════════════════════════════════════════
# KONFIGURASI HALAMAN
# ════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Analisis Kompresi Gambar PNG",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════
# CUSTOM CSS ─ Enterprise Aesthetic (User Friendly)
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, .stApp { font-family: 'Inter', sans-serif; background-color: #f8fafc; color: #0f172a; }

.header-container { padding: 2.5rem 0 1.5rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 2rem; }
.header-title { font-size: 2.2rem; font-weight: 700; color: #0f172a; margin: 0; letter-spacing: -0.02em; }
.header-subtitle { font-size: 1.05rem; color: #475569; margin-top: 0.5rem; line-height: 1.6; max-width: 800px; }
.badge { display: inline-block; padding: 0.35rem 0.85rem; border-radius: 6px; font-size: 0.85rem; font-weight: 600; background-color: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; margin-right: 0.5rem; margin-top: 1.2rem; }

.metric-card { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.25rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04); text-align: left; transition: transform 0.2s ease, box-shadow 0.2s ease; }
.metric-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-color: #cbd5e1; }
.metric-label { font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem; }
.metric-value { font-size: 1.5rem; font-weight: 700; color: #0f172a; }
.metric-value.sm { font-size: 1.1rem; word-break: break-all; }
.metric-sub { font-size: 0.85rem; color: #64748b; margin-top: 0.3rem; }

.section-title { font-size: 1.3rem; font-weight: 700; color: #0f172a; margin-top: 2.5rem; margin-bottom: 1.2rem; padding-bottom: 0.5rem; border-bottom: 2px solid #e2e8f0; }

.info-box { background-color: #f0fdf4; border-left: 4px solid #22c55e; padding: 1.2rem; border-radius: 0 6px 6px 0; margin: 1.5rem 0; box-shadow: 0 1px 2px rgba(0,0,0,0.02); transition: all 0.2s ease; }
.info-box:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.04); }
.info-box-title { font-size: 1rem; font-weight: 700; color: #166534; margin-bottom: 0.3rem; display: flex; align-items: center; }
.info-box-text { font-size: 0.9rem; color: #15803d; line-height: 1.6; }

.custom-table { width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.9rem; text-align: left; background: #fff; border-radius: 8px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }
.custom-table th { background-color: #f8fafc; color: #475569; font-weight: 600; padding: 1rem; border-bottom: 1px solid #e2e8f0; }
.custom-table td { padding: 1rem; border-bottom: 1px solid #e2e8f0; color: #334155; }
.custom-table tr:last-child td { border-bottom: none; }
.custom-table tr:hover { background-color: #f1f5f9; }
.best-value { color: #059669; font-weight: 700; }

.footer { text-align: center; padding: 2rem 0; color: #94a3b8; font-size: 0.85rem; border-top: 1px solid #e2e8f0; margin-top: 4rem; }

#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stFileUploader"] { border: 2px dashed #cbd5e1; border-radius: 8px; padding: 1.5rem; background: #f8fafc; transition: all 0.2s ease; }
div[data-testid="stFileUploader"]:hover { border-color: #94a3b8; background: #f1f5f9; }

/* Interactive Buttons */
div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2) !important;
}
div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover {
    background-color: #1d4ed8 !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 15px rgba(37, 99, 235, 0.35) !important;
    color: #ffffff !important;
}
div[data-testid="stButton"] button:active, div[data-testid="stDownloadButton"] button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2) !important;
}
div[data-testid="stButton"] button p, div[data-testid="stDownloadButton"] button p {
    color: #ffffff !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# WARNA & LAYOUT PLOTLY
# ════════════════════════════════════════════════════════════════
C = dict(
    lzss="#3b82f6", rle="#0ea5e9", ac="#6366f1",
    orig="#94a3b8", bg="rgba(0,0,0,0)", txt="#0f172a",
    secondary="#cbd5e1"
)
_PL = dict(
    font=dict(family="Inter, sans-serif", size=12, color=C["txt"]),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=C["bg"],
    margin=dict(l=40, r=20, t=50, b=40),
)

# ════════════════════════════════════════════════════════════════
# FUNGSI UTILITAS
# ════════════════════════════════════════════════════════════════

def calc_psnr(orig, recon):
    mse = np.mean((orig.astype(np.float64) - recon.astype(np.float64)) ** 2)
    if mse == 0: return float("inf")
    return 20 * math.log10(255.0 / math.sqrt(mse))

def img_to_bytes(img_arr):
    """Mengubah numpy array gambar kembali ke bytes format PNG murni untuk didownload"""
    img = Image.fromarray(img_arr)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# ════════════════════════════════════════════════════════════════
# ALGORITMA 1 ─ LZSS (Optimized)
# ════════════════════════════════════════════════════════════════

class LZSS:
    @staticmethod
    def compress(img: np.ndarray, window_size=1024, lookahead=18):
        h, w, c = img.shape
        raw_bytes = img.flatten().tobytes()
        n = len(raw_bytes)
        
        out = bytearray(struct.pack("<III", h, w, c))
        
        # Untuk Profiling Visualisasi
        stat_literal_bytes = 0
        stat_pointer_bytes = 0
        
        flags = 0
        flag_pos = len(out)
        out.append(0)
        bit_count = 0
        
        i = 0
        while i < n:
            match_len = 0
            match_dist = 0
            
            if i > 0:
                look_len = min(lookahead, n - i)
                if look_len >= 3:
                    window_start = max(0, i - window_size)
                    window_bytes = raw_bytes[window_start:i]
                    for l in range(look_len, 2, -1):
                        pos = window_bytes.rfind(raw_bytes[i:i+l])
                        if pos != -1:
                            match_len = l
                            match_dist = i - (window_start + pos)
                            break
            
            if match_len >= 3:
                flags |= (1 << bit_count)
                token = ((match_dist & 0xFFF) << 4) | (match_len - 3)
                out.extend(struct.pack(">H", token))
                i += match_len
                stat_pointer_bytes += 2
            else:
                out.append(raw_bytes[i])
                i += 1
                stat_literal_bytes += 1
            
            bit_count += 1
            if bit_count == 8:
                out[flag_pos] = flags
                flags = 0; bit_count = 0
                flag_pos = len(out)
                if i < n: out.append(0)
                    
        if bit_count > 0:
            out[flag_pos] = flags
        else:
            if flag_pos == len(out) - 1: out.pop()
                
        return bytes(out), (stat_literal_bytes, stat_pointer_bytes)

    @staticmethod
    def decompress(data: bytes):
        h, w, c = struct.unpack("<III", data[:12])
        total = h * w * c
        out = bytearray()
        off = 12
        while len(out) < total and off < len(data):
            flags = data[off]
            off += 1
            for bit_count in range(8):
                if len(out) >= total or off >= len(data): break
                if (flags & (1 << bit_count)) != 0:
                    token = struct.unpack(">H", data[off:off+2])[0]
                    off += 2
                    dist = token >> 4
                    length = (token & 0x0F) + 3
                    start = len(out) - dist
                    for _ in range(length):
                        out.append(out[start])
                        start += 1
                else:
                    out.append(data[off])
                    off += 1
        return np.frombuffer(bytes(out[:total]), dtype=np.uint8).reshape(h, w, c)

# ════════════════════════════════════════════════════════════════
# ALGORITMA 2 ─ MODIFIED RLE (Optimized)
# ════════════════════════════════════════════════════════════════

class ModifiedRLE:
    @staticmethod
    def compress(img: np.ndarray):
        h, w, c = img.shape
        raw_mv = memoryview(img.flatten().tobytes())
        n = len(raw_mv)
        buf = bytearray(struct.pack("<III", h, w, c))
        
        stat_literal_bytes = 0
        stat_run_header_bytes = 0
        
        i = 0
        while i < n:
            if i + 2 < n and raw_mv[i] == raw_mv[i+1] == raw_mv[i+2]:
                j = i + 3
                val = raw_mv[i]
                while j < n and j - i < 128 and raw_mv[j] == val:
                    j += 1
                rlen = j - i
                buf.append(0x80 | (rlen - 1))
                buf.append(val)
                stat_run_header_bytes += 2
                i = j
            else:
                lit_start = i
                while i < n and i - lit_start < 128:
                    if i + 2 < n and raw_mv[i] == raw_mv[i+1] == raw_mv[i+2]:
                        break
                    i += 1
                llen = i - lit_start
                if llen == 0:
                    llen = 1; i += 1
                buf.append(llen - 1)
                buf.extend(raw_mv[lit_start:lit_start+llen])
                # header literal 1 byte + datanya
                stat_run_header_bytes += 1
                stat_literal_bytes += llen
        return bytes(buf), (stat_literal_bytes, stat_run_header_bytes)

    @staticmethod
    def decompress(data: bytes):
        h, w, c = struct.unpack("<III", data[:12])
        total = h * w * c
        out = bytearray()
        off = 12
        while len(out) < total and off < len(data):
            ctrl = data[off]; off += 1
            if ctrl & 0x80:
                length = (ctrl & 0x7F) + 1
                val = data[off]; off += 1
                out.extend([val] * length)
            else:
                length = ctrl + 1
                out.extend(data[off:off + length])
                off += length
        return np.frombuffer(bytes(out[:total]), dtype=np.uint8).reshape(h, w, c)

# ════════════════════════════════════════════════════════════════
# ALGORITMA 3 ─ ARITHMETIC CODING (Optimized)
# ════════════════════════════════════════════════════════════════

class ArithmeticCoding:
    BITS = 32
    FULL = 1 << 32
    HALF = 1 << 31
    QTR  = 1 << 30
    TQ   = HALF + QTR
    MAX  = FULL - 1

    @staticmethod
    def compress(img: np.ndarray):
        h, w, c = img.shape
        raw = memoryview(img.flatten().tobytes())
        dlen = len(raw)
        
        freq = [0] * 256
        for b in raw: freq[b] += 1
            
        cum = [0] * 257
        for i in range(256): cum[i + 1] = cum[i] + freq[i]
        total = cum[256]
        
        bounds = [(cum[i], cum[i+1]) for i in range(256)]
        
        HALF = ArithmeticCoding.HALF
        QTR = ArithmeticCoding.QTR
        TQ = ArithmeticCoding.TQ
        
        lo, hi, pend = 0, ArithmeticCoding.MAX, 0
        wr_buf = bytearray()
        wr_byte = 0
        wr_cnt = 0
        tbits = 0
        
        for sym in raw:
            b_lo, b_hi = bounds[sym]
            rng = hi - lo + 1
            hi = lo + (rng * b_hi) // total - 1
            lo = lo + (rng * b_lo) // total
            
            while True:
                if hi < HALF:
                    wr_byte = (wr_byte << 1)
                    wr_cnt += 1; tbits += 1
                    if wr_cnt == 8: wr_buf.append(wr_byte); wr_byte = 0; wr_cnt = 0
                    for _ in range(pend):
                        wr_byte = (wr_byte << 1) | 1
                        wr_cnt += 1; tbits += 1
                        if wr_cnt == 8: wr_buf.append(wr_byte); wr_byte = 0; wr_cnt = 0
                    pend = 0
                elif lo >= HALF:
                    wr_byte = (wr_byte << 1) | 1
                    wr_cnt += 1; tbits += 1
                    if wr_cnt == 8: wr_buf.append(wr_byte); wr_byte = 0; wr_cnt = 0
                    for _ in range(pend):
                        wr_byte = (wr_byte << 1)
                        wr_cnt += 1; tbits += 1
                        if wr_cnt == 8: wr_buf.append(wr_byte); wr_byte = 0; wr_cnt = 0
                    pend = 0
                    lo -= HALF; hi -= HALF
                elif lo >= QTR and hi < TQ:
                    pend += 1
                    lo -= QTR; hi -= QTR
                else:
                    break
                lo <<= 1; hi = (hi << 1) | 1
                
        pend += 1
        if lo < QTR:
            wr_byte = (wr_byte << 1)
            wr_cnt += 1; tbits += 1
            if wr_cnt == 8: wr_buf.append(wr_byte); wr_byte = 0; wr_cnt = 0
            for _ in range(pend):
                wr_byte = (wr_byte << 1) | 1
                wr_cnt += 1; tbits += 1
                if wr_cnt == 8: wr_buf.append(wr_byte); wr_byte = 0; wr_cnt = 0
        else:
            wr_byte = (wr_byte << 1) | 1
            wr_cnt += 1; tbits += 1
            if wr_cnt == 8: wr_buf.append(wr_byte); wr_byte = 0; wr_cnt = 0
            for _ in range(pend):
                wr_byte = (wr_byte << 1)
                wr_cnt += 1; tbits += 1
                if wr_cnt == 8: wr_buf.append(wr_byte); wr_byte = 0; wr_cnt = 0
                
        if wr_cnt > 0:
            wr_byte <<= (8 - wr_cnt)
            wr_buf.append(wr_byte)

        out = bytearray()
        # header
        out.extend(struct.pack("<III", h, w, c))
        out.extend(struct.pack("<I", dlen))
        out.extend(struct.pack("<I", tbits))
        nz = [(i, f) for i, f in enumerate(freq) if f > 0]
        out.extend(struct.pack("<H", len(nz)))
        for sym, f in nz:
            out.extend(struct.pack("<BI", sym, f))
            
        header_len = len(out)
        out.extend(wr_buf)
        data_len = len(wr_buf)
        
        return bytes(out), (data_len, header_len)

    @staticmethod
    def decompress(data: bytes):
        A = ArithmeticCoding
        off = 0
        h, w, c = struct.unpack("<III", data[off:off+12]); off += 12
        dlen = struct.unpack("<I", data[off:off+4])[0]; off += 4
        tbits = struct.unpack("<I", data[off:off+4])[0]; off += 4
        nsym = struct.unpack("<H", data[off:off+2])[0]; off += 2
        
        freq = [0] * 256
        for _ in range(nsym):
            s, f = struct.unpack("<BI", data[off:off+5]); off += 5
            freq[s] = f
            
        cum = [0] * 257
        for i in range(256): cum[i + 1] = cum[i] + freq[i]
        total = cum[256]
        
        if total == 0 or dlen == 0: return np.zeros((h, w, c), dtype=np.uint8)
        
        lookup = np.zeros(total, dtype=np.uint8)
        for s in range(256):
            if freq[s] > 0: lookup[cum[s]:cum[s + 1]] = s
                
        class FastReader:
            def __init__(self, d):
                self.d = d; self.bi = 0; self.bit = 7
            def get(self):
                if self.bi >= len(self.d): return 0
                v = (self.d[self.bi] >> self.bit) & 1
                self.bit -= 1
                if self.bit < 0: self.bit = 7; self.bi += 1
                return v

        rd = FastReader(data[off:])
        lo, hi = 0, A.MAX
        val = 0
        for _ in range(A.BITS): val = (val << 1) | rd.get()
            
        result = bytearray()
        for _ in range(dlen):
            rng = hi - lo + 1
            scaled = ((val - lo + 1) * total - 1) // rng
            if scaled >= total: scaled = total - 1
            sym = int(lookup[scaled])
            result.append(sym)
            
            hi = lo + (rng * cum[sym + 1]) // total - 1
            lo = lo + (rng * cum[sym])     // total
            
            while True:
                if hi < A.HALF: pass
                elif lo >= A.HALF: lo -= A.HALF; hi -= A.HALF; val -= A.HALF
                elif lo >= A.QTR and hi < A.TQ: lo -= A.QTR; hi -= A.QTR; val -= A.QTR
                else: break
                lo <<= 1; hi = (hi << 1) | 1
                val = (val << 1) | rd.get()
                
        return np.frombuffer(bytes(result), dtype=np.uint8).reshape(h, w, c)


# ════════════════════════════════════════════════════════════════
# FUNGSI VISUALISASI
# ════════════════════════════════════════════════════════════════

def _fig(title, h=400, **kw):
    layout = {**_PL, **kw}
    layout["title"] = dict(text=title, font=dict(size=14, color=C["txt"], weight="bold"))
    layout["height"] = h
    return layout

def fig_size_bar(results, raw_kb):
    names  = ["Ukuran Asli"] + [r["name"] for r in results]
    sizes  = [raw_kb]     + [r["kb"] for r in results]
    colors = [C["orig"], C["lzss"], C["rle"], C["ac"]]
    fig = go.Figure()
    for nm, sz, cl in zip(names, sizes, colors):
        fig.add_trace(go.Bar(
            x=[nm], y=[sz], marker_color=cl,
            text=[f"{sz:.2f} KB"], textposition="outside",
            textfont=dict(size=12, family="Inter"), showlegend=False,
        ))
    fig.update_layout(**_fig("Perbandingan Ukuran File"), bargap=.4,
                      yaxis=dict(title="Ukuran (KB)", gridcolor="#e2e8f0"))
    return fig

def fig_ratio_time(results):
    names  = [r["name"] for r in results]
    ratios = [r["ratio"] for r in results]
    times  = [r["ms"]    for r in results]
    colors = [C["lzss"], C["rle"], C["ac"]]
    fig = make_subplots(1, 2, subplot_titles=["Rasio Kompresi", "Waktu Eksekusi"])
    for i, (nm, rt, tm, cl) in enumerate(zip(names, ratios, times, colors)):
        fig.add_trace(go.Bar(x=[nm], y=[rt], marker_color=cl,
                             text=[f"{rt:.2f}"], textposition="outside",
                             textfont=dict(size=12), showlegend=False), 1, 1)
        fig.add_trace(go.Bar(x=[nm], y=[tm], marker_color=cl,
                             text=[f"{tm:.1f} ms"], textposition="outside",
                             textfont=dict(size=12), showlegend=False), 1, 2)
    fig.update_layout(**_fig("Matriks Performa Algoritma", h=400))
    fig.update_yaxes(title_text="Rasio (Lebih besar lebih baik)", row=1, col=1, gridcolor="#e2e8f0")
    fig.update_yaxes(title_text="Waktu (Milidetik)", row=1, col=2, gridcolor="#e2e8f0")
    return fig

def fig_composition_donut(val1, lbl1, val2, lbl2, color1, color2, title):
    """Membuat Donut Chart seragam untuk komposisi data"""
    fig = go.Figure(data=[go.Pie(
        labels=[lbl1, lbl2],
        values=[val1, val2],
        hole=.45,
        marker=dict(colors=[color1, color2]),
        textinfo='label+percent',
        textposition='outside',
        insidetextorientation='radial'
    )])
    fig.update_layout(**_fig(title, h=380), showlegend=True,
                      legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"))
    return fig


# ════════════════════════════════════════════════════════════════
# APLIKASI UTAMA
# ════════════════════════════════════════════════════════════════

def main():
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Analisis Kompresi Gambar PNG</h1>
        <p class="header-subtitle">Studi komparasi teknis antara tiga metodologi kompresi lossless: Pendekatan Dictionary (Kamus), Run-Length, dan Entropy (Statistik).</p>
        <div>
            <span class="badge">LZSS (Dictionary)</span>
            <span class="badge">Modified RLE (Run-Length)</span>
            <span class="badge">Arithmetic Coding (Entropy)</span>
        </div>
    </div>""", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### Pengaturan Sistem")
        max_dim = st.slider("Maksimal Dimensi Proses (Pixel)", 128, 1024, 512, 64,
                            help="Memperkecil dimensi awal gambar untuk mempercepat proses komputasi.")
        
        st.markdown("---")
        st.markdown("### Referensi Teoritis")
        with st.expander("LZSS (Sliding Window)"):
            st.markdown("""
**Konsep:** Algoritma berbasis kamus dengan jendela riwayat dinamis (*sliding window*).
**Proses:** Mengganti urutan byte berulang dengan penunjuk/pointer jarak dan panjang (*Distance & Length*) ke area riwayat data.
**Kelebihan:** Sangat optimal pada gambar struktural atau ilustrasi vektor.
""")
        with st.expander("Modified RLE"):
            st.markdown("""
**Konsep:** Kompresi tingkat byte *Run-Length Encoding*.
**Proses:** Mengelompokkan byte identik berturut-turut menjadi skema grup dua byte (*Flag|Panjang*, *Nilai Data*).
**Kelebihan:** Sangat cepat dan optimal untuk gambar dengan area warna blok padat.
""")
        with st.expander("Arithmetic Coding"):
            st.markdown("""
**Konsep:** Pengkodean entropi berbasis statistik tabel probabilitas.
**Proses:** Memetakan seluruh data ke dalam satu pecahan matematis desimal antara rentang angka 0 dan 1.
**Kelebihan:** Mampu memampatkan data mendekati batas teori Shannon Entropy.
""")

    if "R" in st.session_state:
        # Jika sudah dikompres, tampilkan tombol kembali
        if st.button("Analisis Gambar Baru", type="secondary", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    else:
        st.markdown('<div class="section-title">Pemilihan Data Gambar</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Pilih File PNG Anda", type=["png"], label_visibility="collapsed")

        if uploaded is None:
            st.info("Silakan unggah sebuah gambar dengan ekstensi PNG untuk memulai analisis komparasi.")
            return

        # Preprocess gambar awal
        orig_img = Image.open(uploaded)
        if orig_img.mode == "RGBA":
            bg = Image.new("RGB", orig_img.size, (255, 255, 255))
            bg.paste(orig_img, mask=orig_img.split()[3])
            orig_img = bg
        elif orig_img.mode != "RGB":
            orig_img = orig_img.convert("RGB")

        uploaded.seek(0)
        png_kb = len(uploaded.read()) / 1024

        ow, oh = orig_img.size
        if max(ow, oh) > max_dim:
            r = max_dim / max(ow, oh)
            proc_img = orig_img.resize((int(ow * r), int(oh * r)), Image.LANCZOS)
            resized = True
        else:
            proc_img = orig_img
            resized = False

        pw, ph = proc_img.size
        img_arr = np.array(proc_img)
        raw_kb  = img_arr.nbytes / 1024

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Nama Dokumen</div>'
                        f'<div class="metric-value sm">{uploaded.name}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Resolusi Awal</div>'
                        f'<div class="metric-value">{ow} × {oh}</div></div>', unsafe_allow_html=True)
        with c3:
            rs_label = '<div class="metric-sub" style="color:#0ea5e9">Telah di-Resize</div>' if resized else ""
            st.markdown(f'<div class="metric-card"><div class="metric-label">Resolusi Diproses</div>'
                        f'<div class="metric-value">{pw} × {ph}</div>{rs_label}</div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Kapasitas Data</div>'
                        f'<div class="metric-value">{png_kb:.1f} KB</div>'
                        f'<div class="metric-sub">Bobot Pixel Murni: {raw_kb:.1f} KB</div></div>', unsafe_allow_html=True)

        st.markdown("")
        if st.button("Jalankan Algoritma Kompresi", type="primary", use_container_width=True):
            results = []
            progress = st.progress(0, "Inisialisasi sistem...")

            # LZSS
            progress.progress(10, "Mengeksekusi LZSS (Pencarian Dictionary)...")
            t0 = time.time()
            lzss_comp, (lz_lit, lz_ptr) = LZSS.compress(img_arr)
            lzss_ms = (time.time() - t0) * 1000
            progress.progress(30, "Mengeksekusi Validasi Dekompresi LZSS...")
            lzss_dec = LZSS.decompress(lzss_comp)
            results.append(dict(
                name="LZSS", color=C["lzss"],
                comp=lzss_comp, kb=len(lzss_comp)/1024,
                ratio=img_arr.nbytes/len(lzss_comp), ms=lzss_ms,
                psnr=calc_psnr(img_arr, lzss_dec), dec=lzss_dec,
                ok=np.array_equal(img_arr, lzss_dec),
                stat_a=lz_lit, stat_b=lz_ptr,
                stat_label_a="Literal Bytes (Data Tidak Padat)", stat_label_b="Dictionary Pointers (Data Padat)"
            ))

            # RLE
            progress.progress(40, "Mengeksekusi Modified RLE...")
            t0 = time.time()
            rle_comp, (rle_lit, rle_hdr) = ModifiedRLE.compress(img_arr)
            rle_ms = (time.time() - t0) * 1000
            progress.progress(60, "Mengeksekusi Validasi Dekompresi RLE...")
            rle_dec = ModifiedRLE.decompress(rle_comp)
            results.append(dict(
                name="Modified RLE", color=C["rle"],
                comp=rle_comp, kb=len(rle_comp)/1024,
                ratio=img_arr.nbytes/len(rle_comp), ms=rle_ms,
                psnr=calc_psnr(img_arr, rle_dec), dec=rle_dec,
                ok=np.array_equal(img_arr, rle_dec),
                stat_a=rle_lit, stat_b=rle_hdr,
                stat_label_a="Literal Bytes", stat_label_b="Run Headers"
            ))

            # AC
            progress.progress(70, "Mengeksekusi Arithmetic Coding (Statistik Entropy)...")
            t0 = time.time()
            ac_comp, (ac_data, ac_hdr) = ArithmeticCoding.compress(img_arr)
            ac_ms = (time.time() - t0) * 1000
            progress.progress(90, "Mengeksekusi Validasi Dekompresi Arithmetic...")
            ac_dec = ArithmeticCoding.decompress(ac_comp)
            results.append(dict(
                name="Arithmetic Coding", color=C["ac"],
                comp=ac_comp, kb=len(ac_comp)/1024,
                ratio=img_arr.nbytes/len(ac_comp), ms=ac_ms,
                psnr=calc_psnr(img_arr, ac_dec), dec=ac_dec,
                ok=np.array_equal(img_arr, ac_dec),
                stat_a=ac_data, stat_b=ac_hdr,
                stat_label_a="Encoded Bitstream", stat_label_b="Frequency Table (Metadata)"
            ))

            progress.progress(100, "Seluruh analisis komparasi selesai.")
            st.toast('Proses kompresi telah berhasil!', icon='✅')
            time.sleep(0.5)
            progress.empty()

            st.session_state["R"] = results
            st.session_state["img"] = img_arr
            st.session_state["raw_kb"] = raw_kb
            st.session_state["filename"] = uploaded.name
            st.rerun()

    if "R" not in st.session_state:
        return

    results = st.session_state["R"]
    img_arr = st.session_state["img"]
    raw_kb  = st.session_state["raw_kb"]

    # Menentukan algoritma terbaik
    best_i = min(range(len(results)), key=lambda i: results[i]["kb"])
    best_alg = results[best_i]

    st.markdown(f"""
    <div class="info-box" style="border-left-color: #059669; background-color: #ecfdf5; margin-top: 0;">
        <div class="info-box-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
            Rekomendasi Algoritma Terbaik
        </div>
        <div class="info-box-text">
            Berdasarkan dokumen uji coba ini, algoritma yang memberikan kompresi terdalam adalah <b>{best_alg['name']}</b> 
            dengan ukuran akhir <b>{best_alg['kb']:.2f} KB</b> (Rasio Kompresi {best_alg['ratio']:.3f}).
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Komparasi Visual & Unduhan
    st.markdown('<div class="section-title">Inspeksi Kualitas Visual & Unduhan</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        st.image(img_arr, caption="Data Asli", use_container_width=True)
        st.caption(f"Ukuran Mentah: **{raw_kb:.2f} KB**")

    for i, r in enumerate(results):
        with cols[i + 1]:
            st.image(r["dec"], caption=r["name"], use_container_width=True)
            st.caption(f"Ukuran: **{r['kb']:.2f} KB**")
            # Tombol Unduh
            img_png_bytes = img_to_bytes(r["dec"])
            fname = r["name"].replace(" ", "_").lower()
            st.download_button(label=f"Unduh Gambar ({r['name']})", 
                               data=img_png_bytes, 
                               file_name=f"{fname}_result.png", 
                               mime="image/png",
                               use_container_width=True,
                               key=f"dl_{i}")

    # 2. Tabel Integritas Numerik
    st.markdown('<div class="section-title">Tabel Integritas Metrik</div>', unsafe_allow_html=True)
    rows_html = ""
    for i, r in enumerate(results):
        psnr_s = "Identik (Lossless)" if r["psnr"] == float("inf") else f'{r["psnr"]:.2f} dB'
        red = (1 - r["kb"] / raw_kb) * 100
        cls = ' class="best-value"' if i == best_i else ""
        rows_html += f"""<tr>
            <td>{r['name']}</td>
            <td>{raw_kb:.2f}</td>
            <td{cls}>{r['kb']:.2f}</td>
            <td{cls}>{r['ratio']:.4f}</td>
            <td>{red:.2f}%</td>
            <td>{r['ms']:.1f}</td>
            <td>{psnr_s}</td>
            <td>{'Lulus Uji' if r['ok'] else 'Gagal Uji'}</td>
        </tr>"""

    st.markdown(f"""
    <table class="custom-table">
    <thead><tr>
        <th>Metodologi</th><th>Bobot Mentah (KB)</th><th>Hasil Kompresi (KB)</th>
        <th>Rasio Kompresi</th><th>Tingkat Reduksi (%)</th><th>Waktu Proses (ms)</th>
        <th>Nilai PSNR</th><th>Uji Integritas Pixels</th>
    </tr></thead>
    <tbody>{rows_html}</tbody>
    </table>""", unsafe_allow_html=True)

    # 3. Grafik Performa
    st.markdown('<div class="section-title">Kinerja dan Performa Kuantitatif</div>', unsafe_allow_html=True)
    gc1, gc2 = st.columns(2)
    with gc1: st.plotly_chart(fig_size_bar(results, raw_kb), use_container_width=True)
    with gc2: st.plotly_chart(fig_ratio_time(results), use_container_width=True)

    # 4. Profiling Algoritma (Bar Charts Seragam)
    st.markdown('<div class="section-title">Analisis Mendalam Struktur Kompresi (Data Composition)</div>', unsafe_allow_html=True)
    st.markdown("""<p style="color:#475569; font-size:0.95rem; margin-bottom:1.5rem;">
    Grafik berikut membedah <i>anatomi bytes</i> dari ukuran file yang dihasilkan oleh masing-masing algoritma.
    Metode yang baik akan meminimalkan ukuran data mentah (Literal Bytes) dan memaksimalkan pemakaian struktur ringkas (seperti Dictionary Pointer atau Encoded Bitstream).
    </p>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Struktur LZSS", "Struktur Modified RLE", "Struktur Arithmetic Coding"])

    with tab1:
        st.plotly_chart(fig_composition_donut(
            results[0]["stat_a"], results[0]["stat_label_a"],
            results[0]["stat_b"], results[0]["stat_label_b"],
            C["secondary"], C["lzss"], "Komposisi Data LZSS"
        ), use_container_width=True)

    with tab2:
        st.plotly_chart(fig_composition_donut(
            results[1]["stat_a"], results[1]["stat_label_a"],
            results[1]["stat_b"], results[1]["stat_label_b"],
            C["secondary"], C["rle"], "Komposisi Data Modified RLE"
        ), use_container_width=True)

    with tab3:
        st.plotly_chart(fig_composition_donut(
            results[2]["stat_a"], results[2]["stat_label_a"],
            results[2]["stat_b"], results[2]["stat_label_b"],
            C["ac"], C["secondary"], "Komposisi Data Arithmetic Coding"
        ), use_container_width=True)

    # 5. Export Laporan CSV
    st.markdown('<div class="section-title">Laporan Hasil Kompresi</div>', unsafe_allow_html=True)
    
    csv_rows = []
    for r in results:
        csv_rows.append({
            "Nama File": st.session_state.get("filename", "unknown.png"),
            "Algoritma": r["name"],
            "Ukuran Awal (KB)": f"{raw_kb:.2f}",
            "Ukuran Akhir (KB)": f'{r["kb"]:.2f}',
            "Rasio Kompresi": f'{r["ratio"]:.4f}',
            "Persentase Penghematan": f'{(1 - r["kb"]/raw_kb)*100:.2f}%',
            "Waktu Kompresi (ms)": f'{r["ms"]:.1f}'
        })
    csv_data = pd.DataFrame(csv_rows).to_csv(index=False)
    
    st.markdown(f'''
    <div class="metric-card" style="margin-bottom: 1rem;">
        <div style="font-size: 1.1rem; font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Ekspor Data Analisis Kuantitatif</div>
        <div style="font-size: 0.95rem; color: #475569; margin-bottom: 1.5rem; line-height: 1.5;">
            Unduh seluruh matriks performa kompresi (Ukuran Awal, Ukuran Akhir, Rasio, Penghematan, dan Waktu) ke dalam format <b>CSV</b>. Fitur ini mempermudah Anda untuk memindahkan data langsung ke Excel atau perangkat lunak spreadsheet lainnya untuk kebutuhan analisis komprehensif.
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.download_button("Unduh Laporan CSV", csv_data, "Laporan_Kompresi_SISMUL.csv", "text/csv", use_container_width=True)

    st.markdown('<div class="footer">Lossless Image Compression Analytics Dashboard</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
