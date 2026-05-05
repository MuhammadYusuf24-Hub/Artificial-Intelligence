import kagglehub

path = kagglehub.dataset_download("syedaeman2212/shoes-sales-dataset")
print("Path to dataset files:", path)

import streamlit as st
import pandas as pd
import kagglehub
import os
import glob

# Fungsi untuk memuat data dari Kaggle
@st.cache_data
def load_data():
    path = kagglehub.dataset_download("syedaeman2212/shoes-sales-dataset")
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    
    if csv_files:
        df = pd.read_csv(csv_files[0])
        return df
    else:
        return pd.DataFrame()

def main():
    st.set_page_config(page_title="Analisis Shoes Sales", layout="wide")
    
    st.title("👟 Dashboard Analisis Data Penjualan Sepatu")
    st.write("Eksplorasi data, melihat statistik, dan menganalisis tren penjualan sepatu.")

    # Memuat data
    df = load_data()

    if df.empty:
        st.error("File dataset (.csv) tidak ditemukan. Silakan periksa kembali.")
        return

    # Menampilkan metrik utama
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Baris Data", df.shape[0])
    col2.metric("Total Kolom", df.shape[1])
    col3.metric("Ukuran Dataset", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")

    # Membuat Tabs
    tabs = st.tabs(["📋 Pratinjau Data", "📊 Statistik Deskriptif", "📈 Analisis dan Visualisasi", "🔍 Filter Data"])

    # Tab 1: Pratinjau Data
    with tabs[0]:
        st.subheader("📋 Pratinjau Data")
        num_rows = st.slider("Pilih jumlah baris yang ingin ditampilkan", min_value=5, max_value=50, value=10)
        st.dataframe(df.head(num_rows))

    # Tab 2: Statistik Deskriptif
    with tabs[1]:
        st.subheader("📊 Statistik Deskriptif")
        st.dataframe(df.describe())
        
        st.subheader("Tipe Data Tiap Kolom")
        dtypes_df = pd.DataFrame(df.dtypes, columns=["Tipe Data"])
        st.dataframe(dtypes_df)

    # Tab 3: Analisis dan Visualisasi
    with tabs[2]:
        st.subheader("📈 Analisis dan Visualisasi Data")
        
        # Analisis numerik
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if numeric_cols:
            selected_num_col = st.selectbox("Pilih kolom numerik untuk dilihat grafiknya", numeric_cols)
            st.bar_chart(df[selected_num_col])
        else:
            st.info("Tidak ada kolom numerik yang terdeteksi.")

        # Analisis berdasarkan Brand atau Kategori
        if 'Brand' in df.columns:
            st.markdown("### Jumlah Produk Berdasarkan Brand")
            brand_counts = df['Brand'].value_counts()
            st.bar_chart(brand_counts)
            
            if 'Price' in df.columns:
                st.markdown("### Rata-rata Harga per Brand")
                avg_price = df.groupby('Brand')['Price'].mean().sort_values(ascending=False).reset_index()
                st.bar_chart(avg_price.set_index('Brand'))

    # Tab 4: Filter Data
    with tabs[3]:
        st.subheader("🔍 Filter Data")
        search_col = st.selectbox("Pilih kolom untuk difilter", df.columns, key='filter_col')
        
        if search_col:
            unique_vals = df[search_col].dropna().unique().tolist()
            selected_val = st.selectbox("Pilih nilai yang dicari", unique_vals)
            
            filtered_df = df[df[search_col] == selected_val]
            st.write(f"Menampilkan {len(filtered_df)} baris data:")
            st.dataframe(filtered_df)

if __name__ == "__main__":
    main()