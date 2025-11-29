import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium

# ============================================================
# KONFIGURASI APLIKASI
# ============================================================
st.set_page_config(
    page_title="Peta Digital UMKM Sulawesi Barat",
    layout="wide"
)

st.title("🗺️ Aplikasi Peta Digital UMKM di Sulawesi Barat")
st.write("""
Aplikasi ini menampilkan lokasi UMKM yang ada di Provinsi Sulawesi Barat.
Gunakan filter di sebelah kiri untuk memilih Kabupaten dan kategori usaha.
""")

# ============================================================
# DATA UMKM (TANPA KONTAK)
# ============================================================
data_umkm = [
    ["UMKM Kopi Lembang", "Kuliner", "Mamasa", "Lembang, Mamasa", -2.9435, 119.3670],
    ["UMKM Sarabba Polewali", "Minuman", "Polewali Mandar", "Kec. Polewali, Polman", -3.4325, 119.3439],
    ["UMKM Kerajinan Anyaman", "Kerajinan", "Majene", "Banggae, Majene", -3.5400, 118.9700],
    ["UMKM Ikan Asap Tande", "Kuliner", "Mamuju", "Tande, Mamuju", -2.6800, 118.8900],
    ["UMKM Kue Kering Sande", "Kuliner", "Mamuju", "Simboro, Mamuju", -2.6500, 118.9000],
    ["UMKM Tenun Tradisional", "Kerajinan", "Polewali Mandar", "Binuang, Polman", -3.4820, 119.2920],
    ["UMKM Oleh-oleh Majene", "Oleh-oleh", "Majene", "Pusat Kota Majene", -3.5420, 118.9730],
    ["UMKM Rumput Laut Pasangkayu", "Pertanian & Perikanan", "Pasangkayu", "Pasangkayu", -1.1960, 119.3630],
    ["UMKM Keripik Pisang Topoyo", "Snack", "Mamuju Tengah", "Topoyo, Mateng", -2.1190, 119.3610],
    ["UMKM Kopi Tapalang", "Minuman", "Mamuju", "Tapalang, Mamuju", -2.7590, 118.7990]
]

columns = ["nama", "kategori", "kabupaten", "alamat", "latitude", "longitude"]
df = pd.DataFrame(data_umkm, columns=columns)

# ============================================================
# SIDEBAR FILTER
# ============================================================
st.sidebar.header("🔍 Filter UMKM")

kabupaten = ["Semua"] + sorted(df["kabupaten"].unique())
kategori = ["Semua"] + sorted(df["kategori"].unique())

filter_kab = st.sidebar.selectbox("Pilih Kabupaten:", kabupaten)
filter_kat = st.sidebar.selectbox("Pilih Kategori:", kategori)
keyword = st.sidebar.text_input("Cari Nama UMKM:", "")

df_filtered = df.copy()

if filter_kab != "Semua":
    df_filtered = df_filtered[df_filtered["kabupaten"] == filter_kab]

if filter_kat != "Semua":
    df_filtered = df_filtered[df_filtered["kategori"] == filter_kat]

if keyword:
    df_filtered = df_filtered[df_filtered["nama"].str.contains(keyword, case=False)]

# ============================================================
# METRIK
# ============================================================
col1, col2, col3 = st.columns(3)
col1.metric("Total UMKM", len(df))
col2.metric("UMKM Terfilter", len(df_filtered))
col3.metric("Jumlah Kabupaten", df["kabupaten"].nunique())

st.write("---")

# ============================================================
# PETA UMKM
# ============================================================
st.subheader("🗺️ Peta Lokasi UMKM Sulawesi Barat")

if not df_filtered.empty:
    center_lat = df_filtered["latitude"].mean()
    center_lon = df_filtered["longitude"].mean()

    peta = folium.Map(location=[center_lat, center_lon], zoom_start=7)

    for _, row in df_filtered.iterrows():
        popup_html = f"""
        <b>{row['nama']}</b><br>
        Kategori: {row['kategori']}<br>
        Kabupaten: {row['kabupaten']}<br>
        Alamat: {row['alamat']}
        """

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup_html,
            tooltip=row["nama"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(peta)

    st_folium(peta, width=900, height=500)
else:
    st.warning("Tidak ada data UMKM sesuai filter.")

# ============================================================
# TABEL DATA
# ============================================================
st.subheader("📄 Data UMKM")
st.dataframe(df_filtered.reset_index(drop=True))

