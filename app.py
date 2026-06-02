import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Farming Kelompok 2", page_icon="🍃", layout="wide")

st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    div[data-testid="stMetricValue"] {font-size: 24px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🍃 Sistem Monitoring & Simulasi IoT Bayam Brazil")
st.subheader("Analisis Data Sensor - Kelompok 2 (Arduino Uno)")
st.markdown("---")

raw_data = {
    'No': list(range(1, 41)),
    'Hari': ['Kamis','Kamis','Kamis','Kamis','Kamis','Sabtu','Sabtu','Sabtu','Sabtu','Sabtu','Selasa','Selasa','Selasa','Selasa','Rabu','Rabu','Rabu','Rabu','Kamis','Kamis','Kamis','Kamis','Jumat','Jumat','Jumat','Jumat','Sabtu','Sabtu','Sabtu','Sabtu','Minggu','Minggu','Minggu','Minggu','Senin','Senin','Senin','Senin','Selasa','Selasa'],
    'Tanggal': ['14/05/2026']*5 + ['16/05/2026']*5 + ['19/05/2026']*4 + ['20/05/2026']*4 + ['21/05/2026']*4 + ['22/05/2026']*4 + ['23/05/2026']*4 + ['24/05/2026']*4 + ['25/05/2026']*4 + ['26/05/2026']*2,
    'Jam': ['14:00','14:30','15:00','15:30','16:00','07:45','08:15','08:45','09:15','09:45','15:07','15:37','16:07','16:37','12:00','12:30','13:00','13:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','14:00','14:30','15:00','15:30','10:00','10:30','11:00','11:30','16:00','16:30','17:00','17:30','08:00','08:30'],
    'HST': [10]*40,
    'Soil Moisture (%)': [52, 50, 47, 45, 43, 46, 48, 50, 52, 51, 100, 99, 84, 73, 33, 27, 30, 35, 55, 58, 60, 57, 42, 38, 35, 31, 65, 63, 61, 59, 48, 45, 42, 40, 70, 68, 66, 64, 53, 50],
    'Suhu (°C)': [32.0, 32.4, 32.8, 32.5, 32.0, 28.0, 27.8, 27.5, 27.3, 27.1, 27.0, 31.0, 29.8, 28.5, 30.3, 31.1, 31.0, 30.5, 29.0, 29.5, 30.0, 30.2, 31.5, 32.0, 32.5, 32.8, 28.5, 28.8, 29.0, 29.2, 30.0, 30.5, 30.8, 31.0, 27.5, 27.8, 28.0, 28.2, 29.1, 29.4],
    'Keterangan': ['Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Basah','Basah','Basah','Basah','Kering','Kering','Kering','Kering','Ideal','Ideal','Ideal','Ideal','Ideal','Kering','Kering','Kering','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal','Ideal']
}
df = pd.DataFrame(raw_data)
data_terakhir = df.iloc[-1]

st.header("📊 Ringkasan Data Sensor Terkini")
st.markdown(f"**Data Terakhir (Baris ke-40):** Hari {data_terakhir['Hari']}, {data_terakhir['Tanggal']} | Kelembapan: `{data_terakhir['Soil Moisture (%)']}%` | Suhu: `{data_terakhir['Suhu (°C)']}°C` | Status Tanaman: **{data_terakhir['Keterangan'].upper()}**")
st.markdown("---")

st.header("🤖 Simulasi Logika Keputusan Perangkat")
k_in_1, k_in_2 = st.columns(2)
with k_in_1:
    simulasi_moisture = st.slider("Atur Simulasi Kelembapan Tanah (%)", 0, 100, int(data_terakhir['Soil Moisture (%)']))
with k_in_2:
    simulasi_suhu = st.slider("Atur Simulasi Suhu Udara (°C)", 15.0, 45.0, float(data_terakhir['Suhu (°C)']), step=0.1)

st.markdown("### 📢 Status Respon Otomatisasi Pompa Kelompok 2:")
if simulasi_moisture < 40:
    st.error(f"🚨 KONDISI KERING ({simulasi_moisture}%) -> ARDUINO UNO MENYALAKAN POMPA AIR (RELAY ON)")
elif 40 <= simulasi_moisture <= 75:
    st.success(f"✅ KONDISI IDEAL ({simulasi_moisture}%) -> POMPA AIR MATI (RELAY OFF)")
else:
    st.warning(f"⚠️ KONDISI BASAH ({simulasi_moisture}%) -> POMPA AIR MATI")

st.markdown("---")

st.header("📋 Tabel Log Data Monitoring (Scroll Kebawah / Samping)")
st.dataframe(df, height=350, use_container_width=True)

st.markdown("---")

st.header("📈 Visualisasi Grafik Tren Sensor")
k_grafik_1, k_grafik_2 = st.columns(2)

with k_grafik_1:
    st.subheader("Garis Tren Kelembapan Tanah (%)")
    fig1, ax1 = plt.subplots(figsize=(6, 3.5))
    ax1.plot(df['Soil Moisture (%)'], color='#1f77b4', linewidth=2, marker='o')
    ax1.axhline(40, color='red', linestyle='--', label='Batas Kering (40%)')
    ax1.axhline(75, color='green', linestyle='--', label='Batas Ideal (75%)')
    ax1.set_xlabel("Sampel Data Ke-")
    ax1.set_ylabel("Persentase (%)")
    ax1.legend(loc='lower left')
    ax1.grid(True, linestyle=':', alpha=0.6)
    st.pyplot(fig1)

with k_grafik_2:
    st.subheader("Garis Tren Suhu Udara (°C)")
    fig2, ax2 = plt.subplots(figsize=(6, 3.5))
    ax2.plot(df['Suhu (°C)'], color='#ff7f0e', linewidth=2, marker='s')
    ax2.set_xlabel("Sampel Data Ke-")
    ax2.set_ylabel("Derajat Celcius (°C)")
    ax2.grid(True, linestyle=':', alpha=0.6)
    st.pyplot(fig2)