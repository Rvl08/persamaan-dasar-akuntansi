# Persamaan Dasar Akuntansi

Aplikasi web interaktif yang dibangun menggunakan Streamlit untuk membantu pengguna memahami dan mempraktikkan konsep dasar akuntansi. Aplikasi ini menyediakan antarmuka yang ramah pengguna untuk mencatat transaksi keuangan dan secara otomatis menghasilkan laporan keuangan dasar.

## Fitur Utama

- **Pencatatan Transaksi:** Memasukkan berbagai jenis transaksi akuntansi seperti pembelian aset, pembayaran biaya, penerimaan pendapatan, dan lainnya.
- **Laporan Keuangan:** Menghasilkan laporan keuangan penting secara otomatis, termasuk:
  - Laporan Laba Rugi
  - Laporan Perubahan Ekuitas
  - Neraca
- **Visualisasi Data:** Menampilkan visualisasi data untuk aset, kewajiban, dan ekuitas dalam bentuk diagram batang.
- **Ekspor ke Excel:** Mengekspor laporan keuangan ke dalam format file `.xlsx` untuk analisis lebih lanjut.

## Teknologi yang Digunakan

- **Python:** Bahasa pemrograman utama.
- **Streamlit:** Kerangka kerja untuk membangun aplikasi web interaktif.
- **Pandas:** Pustaka untuk manipulasi dan analisis data.
- **Matplotlib & Seaborn:** Pustaka untuk visualisasi data.

## Cara Menjalankan Aplikasi

1.  **Clone Repositori:**
    ```bash
    git clone https://github.com/username/persamaan-dasar-akuntansi.git
    cd persamaan-dasar-akuntansi
    ```

2.  **Instal Dependensi:**
    Pastikan Anda memiliki Python 3.x terinstal. Kemudian, instal semua pustaka yang diperlukan menggunakan `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Aplikasi Streamlit:**
    ```bash
    streamlit run akuntansi.py
    ```

4.  **Akses Aplikasi:**
    Buka browser web Anda dan arahkan ke alamat URL yang ditampilkan di terminal (biasanya `http://localhost:8501`).
