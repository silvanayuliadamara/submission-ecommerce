# Proyek Analisis Data E-Commerce

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis dataset e-commerce guna mengetahui kategori produk dengan performa terbaik, tren penjualan dari waktu ke waktu, serta karakteristik pelanggan berdasarkan RFM analysis.

## Pertanyaan Bisnis
1. Kategori produk apa yang menghasilkan jumlah order dan revenue terbesar?
2. Bagaimana tren penjualan dari waktu ke waktu?
3. Bagaimana karakteristik pelanggan berdasarkan RFM analysis?

## Struktur Direktori
submission_ecommerce
├── dashboard
│   ├── dashboard.py
│   ├── main_data.csv
│   ├── category_summary.csv
│   ├── monthly_summary.csv
│   └── rfm_data.csv
├── data
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt

## Tahapan Analisis
1. Data Gathering
2. Data Assessing
3. Data Cleaning
4. Exploratory Data Analysis (EDA)
5. Visualisasi Data
6. RFM Analysis
7. Conclusion

## Insight Utama
- Terdapat kategori produk yang memberikan kontribusi revenue paling tinggi.
- Tren penjualan bulanan menunjukkan adanya periode penjualan tertinggi dan terendah.
- RFM analysis membantu mengelompokkan pelanggan berdasarkan perilaku transaksi mereka.

## Cara Menjalankan Notebook
1. Buka file `notebook.ipynb` di Google Colab atau Jupyter Notebook.
2. Jalankan seluruh cell secara berurutan.

## Cara Menjalankan Dashboard
```bash
pip install -r requirements.txt
streamlit run dashboard/dashboard.py