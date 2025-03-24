# -*- coding: utf-8 -*-
# """Dashboard

# Automatically generated by Colab.

# Original file is located at
#     https://colab.research.google.com/drive/1gURN4rNeQh0X6PZF3J4aatCrExPpH36E
# """

# !pip install -q streamlit

# Commented out IPython magic to ensure Python compatibility.
# %%writefile dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker


@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")


    reverse_mapping = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
    if df["season"].dtype == object:
        df["season"] = df["season"].map(reverse_mapping)


    valid_seasons = {1, 2, 3, 4}
    df = df[df["season"].isin(valid_seasons)]


    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df["season"] = df["season"].map(season_mapping)

    return df

df = load_data()

# Sidebar Menu
st.sidebar.title("📊 Bike Sharing Dashboard")
menu = st.sidebar.radio("Pilih Visualisasi:", ["Total Penyewaan per Musim", "Perbandingan Weekday vs. Weekend", "Heatmap Korelasi"])

# 1️⃣ Total Penyewaan Sepeda per Musim
if menu == "Total Penyewaan per Musim":
    st.subheader("📊 Total Penyewaan Sepeda Berdasarkan Musim")

    if "season" not in df.columns or "cnt" not in df.columns:
        st.error("❌ Data tidak memiliki kolom 'season' atau 'cnt'.")
    else:
        # Hitung total penyewaan per musim & urutkan dari terbesar ke terkecil
        total_season = df.groupby("season")["cnt"].sum().sort_values(ascending=False)

        # Warna disesuaikan dengan urutan baru
        season_colors = {
            "Fall": "blue",
            "Summer": "pink",
            "Winter": "lightblue",
            "Spring": "red"
        }
        colors = [season_colors[season] for season in total_season.index]

        # Plot
        fig, ax = plt.subplots(figsize=(8, 5))
        total_season.plot(kind="bar", color=colors, ax=ax)

        ax.set_xlabel("Musim")
        ax.set_ylabel("Total Penyewaan")
        ax.set_title("Total Penyewaan Sepeda Berdasarkan Musim (Diurutkan)")
        plt.xticks(rotation=0)

        # Format angka sumbu Y agar lebih mudah dibaca
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))  # Format 1.0M, 0.8M, dll.

        st.pyplot(fig)

        # Info
        max_season = total_season.idxmax()
        min_season = total_season.idxmin()
        st.write(f"🔹 **Musim dengan Penyewaan Tertinggi**: {max_season} ({total_season.max():,.0f} penyewaan)")
        st.write(f"🔸 **Musim dengan Penyewaan Terendah**: {min_season} ({total_season.min():,.0f} penyewaan)")

# 2️⃣ Perbandingan Penyewaan Sepeda: Weekday vs. Weekend
elif menu == "Perbandingan Weekday vs. Weekend":
    st.subheader("📊 Perbandingan Penyewaan Sepeda: Weekday vs. Weekend")

    if "workingday" not in df.columns or "cnt" not in df.columns:
        st.error("❌ Data tidak memiliki kolom 'workingday' atau 'cnt'.")
    else:
        workingday_stats = df.groupby("workingday")["cnt"].mean()
        workingday_labels = ["Weekend", "Weekday"]

        # Plot
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=workingday_labels, y=workingday_stats.values, palette="Set1", ax=ax)
        ax.set_xlabel("Jenis Hari")
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.set_title("Perbandingan Penyewaan Sepeda: Weekday vs. Weekend")
        st.pyplot(fig)

        # Info
        max_day = workingday_labels[np.argmax(workingday_stats.values)]
        min_day = workingday_labels[np.argmin(workingday_stats.values)]
        diff = abs(workingday_stats[1] - workingday_stats[0])

        st.write(f"🔹 **Hari dengan Penyewaan Tertinggi**: {max_day} ({workingday_stats.max():,.0f} penyewaan)")
        st.write(f"🔸 **Hari dengan Penyewaan Terendah**: {min_day} ({workingday_stats.min():,.0f} penyewaan)")
        st.write(f"📊 **Selisih Rata-rata Penyewaan**: {diff:,.0f} penyewaan")


# 3️⃣ Heatmap Korelasi Faktor-faktor Penyewaan Sepeda
elif menu == "Heatmap Korelasi":
    st.subheader("📊 Korelasi Faktor-faktor Penyewaan Sepeda")

    numeric_cols = ["cnt", "temp", "atemp", "hum", "windspeed", "weathersit", "workingday"]
    correlation_matrix = df[numeric_cols].corr()

    # Plot Heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Correlation Heatmap of Bike Sharing Data")
    st.pyplot(fig)

    # Informasi tambahan yang lebih mudah dipahami
    correlations = correlation_matrix["cnt"].drop("cnt")  # Ambil korelasi terhadap "cnt" saja
    max_corr_feature = correlations.idxmax()
    min_corr_feature = correlations.idxmin()

    st.write(f"🔹 **Faktor dengan Korelasi Tertinggi terhadap Penyewaan Sepeda**: {max_corr_feature} ({correlations.max():.2f})")
    st.write(f"🔸 **Faktor dengan Korelasi Terendah terhadap Penyewaan Sepeda**: {min_corr_feature} ({correlations.min():.2f})")

    # Interpretasi
    st.write("📌 **Interpretasi:**")
    st.write(
        f"- **{max_corr_feature}** memiliki korelasi tertinggi, artinya semakin tinggi nilai {max_corr_feature}, "
        "semakin tinggi jumlah penyewaan sepeda."
    )
    st.write(
        f"- **{min_corr_feature}** memiliki korelasi terendah (atau negatif), artinya faktor ini memiliki "
        "pengaruh paling kecil atau bahkan berlawanan terhadap penyewaan sepeda."
    )


st.sidebar.write("📌 **Data dari Bike Sharing Dataset**")


# !npm install localtunnel

# !streamlit run dashboard.py &>/content/logs.txt & npx localtunnel --port 8501 & curl ipv4.icanhazip.com
