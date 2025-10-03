import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    # Baca dataset
    datamap = pd.read_csv('cleaned_diabetes.csv')

    # Pilih hanya kolom numerik
    numeric_data = datamap.select_dtypes(include=['int', 'float'])
    correlation_matrix = numeric_data.corr()

    # ==========================
    # Judul halaman
    # ==========================
    st.markdown(
        """
        <div style="background-color:#D1D1D6; padding:20px; border-radius:10px; margin-bottom:20px;">
            <h2 style="text-align: center; color: #2C3E50;">🩺 Eksplorasi Data Diabetes</h2>
            <p style="text-align: center;">Visualisasi sederhana untuk memahami data pasien diabetes.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==========================
    # 1. Correlation Heatmap
    # ==========================
    st.markdown(
        """
        <div style="background-color:#EFEFF2; padding:20px; border-radius:10px; margin-bottom:20px;">
            <h3>📊 Korelasi Antar Variabel</h3>
        """,
        unsafe_allow_html=True
    )

    fig = px.imshow(
        correlation_matrix,
        labels=dict(x="Fitur", y="Fitur", color="Korelasi"),
        x=correlation_matrix.index,
        y=correlation_matrix.columns,
        color_continuous_scale='Blues',  # hanya biru muda → biru tua
        text_auto=True
    )
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig, use_container_width=True)

    # Penjelasan sederhana untuk orang awam
    st.info("""
    Grafik di atas memperlihatkan **hubungan antar variabel**. 
    Angka korelasi berkisar antara -1 sampai 1:
    - Semakin mendekati **1** → memiliki hubungan kuat, berwarna biru tua.  
    - Semakin mendekati **0** → memiliki hubungan lemah, berwarna biru muda.  

    Contohnya: kadar **Glucose** memiliki hubungan kuat dengan **Outcome**.  
    Artinya, semakin tinggi nilai Glucose, semakin besar kemungkinan seseorang terdeteksi diabetes.  
    """)

    st.markdown("</div>", unsafe_allow_html=True)

    # ==========================
    # 2. Distribusi Outcome per Kelompok Umur
    # ==========================
    st.markdown(
        """
        <div style="background-color:#EFEFF2; padding:20px; border-radius:10px; margin-bottom:20px;">
            <h3>🧍 Perbandingan Pasien Berdasarkan Usia</h3>
        """,
        unsafe_allow_html=True
    )

    bins = list(range(20, 81, 5))  # buat kategori umur 20-80
    labels = [f"{b}-{b+4}" for b in bins[:-1]]
    datamap['AgeGroup'] = pd.cut(datamap['Age'], bins=bins, labels=labels, right=False)

    outcome_age = datamap.groupby(['AgeGroup', 'Outcome']).size().reset_index(name='Jumlah')

    selected_groups = st.multiselect(
        "Pilih Rentang Usia:",
        options=labels,
        default=labels
    )

    if selected_groups:
        outcome_age = outcome_age[outcome_age['AgeGroup'].isin(selected_groups)]

    fig_outcome_age = px.bar(
        outcome_age,
        x='AgeGroup',
        y='Jumlah',
        color='Outcome',
        barmode='group',
        labels={'AgeGroup': 'Kelompok Usia', 'Outcome': 'Diagnosis'},
        title="Distribusi Pasien berdasarkan Kelompok Usia dan Diagnosis"
    )
    st.plotly_chart(fig_outcome_age, use_container_width=True)

    st.info("Anda bisa memilih beberapa rentang usia untuk melihat perbandingan jumlah pasien sehat (0) dan diabetes (1).")

    st.markdown("</div>", unsafe_allow_html=True)

    # ==========================
    # 3. Rata-rata Glukosa & BMI
    # ==========================
    st.markdown(
        """
        <div style="background-color:#EFEFF2; padding:20px; border-radius:10px; margin-bottom:20px;">
            <h3>⚖️ Rata-rata Glukosa & BMI pada Pasien</h3>
        """,
        unsafe_allow_html=True
    )

    avg_values = datamap.groupby("Outcome")[["Glucose", "BMI"]].mean().reset_index()
    avg_values['Outcome'] = avg_values['Outcome'].map({0: "Sehat (0)", 1: "Diabetes (1)"})

    col1, col2 = st.columns(2)
    with col1:
        fig_glucose = px.bar(avg_values, x="Outcome", y="Glucose",
                             color="Outcome", text_auto=".1f",
                             title="Rata-rata Glukosa")
        st.plotly_chart(fig_glucose, use_container_width=True)
        st.info("Pasien diabetes memiliki **rata-rata glukosa lebih tinggi** dibandingkan yang sehat.")

    with col2:
        fig_bmi = px.bar(avg_values, x="Outcome", y="BMI",
                         color="Outcome", text_auto=".1f",
                         title="Rata-rata BMI")
        st.plotly_chart(fig_bmi, use_container_width=True)
        st.info("Pasien diabetes memiliki **rata-rata BMI lebih tinggi**, cenderung overweight/obesitas.")

    st.markdown("</div>", unsafe_allow_html=True)


# Run app
if __name__ == "__main__":
    app()
