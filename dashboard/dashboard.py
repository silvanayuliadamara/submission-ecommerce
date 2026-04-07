import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

sns.set_style("whitegrid")

BASE_DIR = Path(__file__).resolve().parent


@st.cache_data
def load_data():
    main_df = pd.read_csv(BASE_DIR / "main_data.csv")
    category_df = pd.read_csv(BASE_DIR / "category_summary.csv")
    monthly_df = pd.read_csv(BASE_DIR / "monthly_summary.csv")
    rfm_df = pd.read_csv(BASE_DIR / "rfm_data.csv")

    if "order_purchase_timestamp" in main_df.columns:
        main_df["order_purchase_timestamp"] = pd.to_datetime(main_df["order_purchase_timestamp"])

    return main_df, category_df, monthly_df, rfm_df


def format_currency(value):
    return f"R$ {value:,.2f}"


try:
    main_df, category_df, monthly_df, rfm_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data dashboard: {e}")
    st.stop()


st.title("Dashboard Analisis Data E-Commerce")
st.markdown(
    """
Dashboard ini menampilkan ringkasan performa bisnis e-commerce berdasarkan:
- jumlah order
- total revenue
- kategori produk teratas
- tren penjualan bulanan
- segmentasi pelanggan menggunakan RFM analysis
"""
)

st.sidebar.header("Filter Dashboard")

top_n = st.sidebar.slider(
    "Tampilkan Top Kategori Produk",
    min_value=5,
    max_value=20,
    value=10
)

if "customer_state" in main_df.columns:
    state_list = sorted(main_df["customer_state"].dropna().unique().tolist())
    selected_state = st.sidebar.selectbox(
        "Filter State Pelanggan",
        options=["All"] + state_list,
        index=0
    )
else:
    selected_state = "All"

filtered_main_df = main_df.copy()

if selected_state != "All" and "customer_state" in filtered_main_df.columns:
    filtered_main_df = filtered_main_df[filtered_main_df["customer_state"] == selected_state]

st.subheader("Ringkasan Metrik")

total_orders = filtered_main_df["order_id"].nunique() if "order_id" in filtered_main_df.columns else 0
total_customers = filtered_main_df["customer_unique_id"].nunique() if "customer_unique_id" in filtered_main_df.columns else 0
total_revenue = filtered_main_df["total_payment"].sum() if "total_payment" in filtered_main_df.columns else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Customers", f"{total_customers:,}")
col3.metric("Total Revenue", format_currency(total_revenue))

st.markdown("---")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Top Kategori Produk Berdasarkan Revenue")

    top_category_df = (
        category_df.sort_values(by="total_revenue", ascending=False)
        .head(top_n)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=top_category_df,
        x="total_revenue",
        y="product_category",
        ax=ax
    )
    ax.set_title(f"Top {top_n} Kategori Produk")
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel("Kategori Produk")
    st.pyplot(fig)

with right_col:
    st.subheader("Top Kategori Produk Berdasarkan Jumlah Order")

    top_orders_df = (
        category_df.sort_values(by="total_orders", ascending=False)
        .head(top_n)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=top_orders_df,
        x="total_orders",
        y="product_category",
        ax=ax
    )
    ax.set_title(f"Top {top_n} Kategori Berdasarkan Order")
    ax.set_xlabel("Jumlah Order")
    ax.set_ylabel("Kategori Produk")
    st.pyplot(fig)

st.markdown("---")
st.subheader("Tren Penjualan Bulanan")

if not filtered_main_df.empty and "order_purchase_timestamp" in filtered_main_df.columns:
    filtered_main_df["order_month"] = filtered_main_df["order_purchase_timestamp"].dt.to_period("M").astype(str)

    monthly_filtered_df = (
        filtered_main_df.groupby("order_month", as_index=False)
        .agg({
            "order_id": "nunique",
            "total_payment": "sum"
        })
        .rename(columns={
            "order_id": "total_orders",
            "total_payment": "total_revenue"
        })
        .sort_values(by="order_month")
    )

    col_a, col_b = st.columns(2)

    with col_a:
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(
            data=monthly_filtered_df,
            x="order_month",
            y="total_revenue",
            marker="o",
            ax=ax
        )
        ax.set_title("Tren Revenue Bulanan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Revenue")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col_b:
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(
            data=monthly_filtered_df,
            x="order_month",
            y="total_orders",
            marker="o",
            ax=ax
        )
        ax.set_title("Tren Jumlah Order Bulanan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Order")
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    st.warning("Data tren bulanan tidak tersedia.")

st.markdown("---")
st.subheader("Segmentasi Pelanggan Berdasarkan RFM")

segment_summary = (
    rfm_df["customer_segment"]
    .value_counts()
    .reset_index()
)
segment_summary.columns = ["customer_segment", "total_customers"]

col_x, col_y = st.columns([2, 1])

with col_x:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=segment_summary,
        x="total_customers",
        y="customer_segment",
        ax=ax
    )
    ax.set_title("Jumlah Pelanggan per Segmen")
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Segmen Pelanggan")
    st.pyplot(fig)

with col_y:
    st.dataframe(segment_summary, use_container_width=True)

st.markdown("---")
st.subheader("Data Pendukung")

tab1, tab2, tab3 = st.tabs(["Kategori Produk", "Tren Bulanan", "RFM"])

with tab1:
    st.dataframe(
        category_df.sort_values(by="total_revenue", ascending=False).reset_index(drop=True),
        use_container_width=True
    )

with tab2:
    st.dataframe(monthly_df.reset_index(drop=True), use_container_width=True)

with tab3:
    st.dataframe(rfm_df.head(20), use_container_width=True)

st.markdown("---")
st.subheader("Insight Utama")

if not category_df.empty:
    top_revenue_category = category_df.sort_values(by="total_revenue", ascending=False).iloc[0]
    top_order_category = category_df.sort_values(by="total_orders", ascending=False).iloc[0]

    st.write(
        f"- Kategori dengan revenue tertinggi adalah **{top_revenue_category['product_category']}** "
        f"dengan total revenue **{format_currency(top_revenue_category['total_revenue'])}**."
    )
    st.write(
        f"- Kategori dengan jumlah order tertinggi adalah **{top_order_category['product_category']}** "
        f"dengan total order **{int(top_order_category['total_orders'])}**."
    )

if not segment_summary.empty:
    dominant_segment = segment_summary.iloc[0]
    st.write(
        f"- Segmen pelanggan terbesar adalah **{dominant_segment['customer_segment']}** "
        f"dengan jumlah **{int(dominant_segment['total_customers'])} pelanggan**."
    )

if selected_state != "All":
    st.info(f"Filter state aktif: {selected_state}")
else:
    st.info("Menampilkan seluruh data pelanggan.")