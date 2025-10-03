import streamlit as st
import pandas as pd
import numpy as np
import pickle

def app():

    # Load dataset & model
    data = pd.read_csv('cleaned_diabetes.csv')
    model = pickle.load(open("xgboost_model.sav", "rb"))

    st.markdown(
        """
        <div style="text-align: center; padding: 15px; background-color: #D1D1D6; border-radius: 10px;">
            <h2 style="color: #2C3E50;">🔮 Prediksi Diabetes dengan XGBoost</h2>
            <p style="font-size:18px; color:#2C3E50;">
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background-color:#EFEFF2; padding:10px; border-radius:8px; margin-bottom:10px;">
            <h5>📋 Contoh Data Pasien</h5>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write(data.head())
    st.warning("⚠️ Silahkan masukkan data pasien untuk memprediksi pasien (0 = Tidak Diabetes) & (1 = Diabetes)")

    # Buat tata letak grid untuk input
    col1, col2, col3 = st.columns(3)

    with col1:
        pregnancies = st.number_input(
            "Jumlah Kehamilan (Pregnancies)",
            min_value=0, max_value=15, step=1,
            help="Jumlah kehamilan yang pernah dialami pasien wanita. "
                 "Nilai 0 berarti belum pernah hamil."
        )

    with col2:
        glucose = st.number_input(
            "Kadar Glukosa (Glucose) (mg/dL)",
            min_value=40, max_value=300, step=1,
            help="Kadar glukosa darah pasien setelah melakukan tes glukosa. "
                 "Kadar yang tinggi menjadi indikator utama risiko diabetes melitus."
        )

    with col3:
        # Default input BMI
        bmi = st.number_input(
            "Indeks Massa Tubuh (BMI)",
            min_value=10.0, max_value=60.0, step=0.1,
            help="Perbandingan berat badan terhadap tinggi badan pasien. "
                 "BMI = Berat Badan (kg) / (Tinggi Badan (m))²"
        )

        # Kalkulator BMI otomatis (rapi dengan expander & kolom)
        with st.expander("Klik Untuk Menghitung BMI Anda"):
            col_berat, col_tinggi = st.columns(2)

            with col_berat:
                berat = st.number_input(
                    "Berat Badan (kg)", min_value=20.0, max_value=200.0, step=0.1
                )
            with col_tinggi:
                tinggi = st.number_input(
                    "Tinggi Badan (cm)", min_value=100.0, max_value=220.0, step=0.1
                )

            if tinggi > 0:
                bmi_hitung = berat / ((tinggi / 100) ** 2)
                st.success(f"📌 Hasil Perhitungan BMI Anda: **{bmi_hitung:.2f}**")
                bmi = round(bmi_hitung, 2)  # Override nilai BMI dari hasil kalkulasi

    with col1:
        dpf = st.number_input(
            "Diabetes Pedigree Function (DPF)",
            min_value=0.0, max_value=2.5, step=0.001, format="%.3f",
            help="""Indeks yang mengukur riwayat/genetik diabetes dalam keluarga:
- 0.0–0.1 : Risiko rendah / tidak ada riwayat
- 0.4–0.7 : Ada keluarga dekat terkena diabetes
- 0.7–1.0 : Banyak keluarga terkena diabetes"""
        )

    with col2:
        age = st.number_input(
            "Usia (Age)",
            min_value=10, max_value=100, step=1,
            help="Usia pasien dalam tahun. Risiko diabetes meningkat seiring bertambahnya usia."
        )

    # Tombol prediksi
    if st.button("Prediksi Diabetes"):
        # ==============================
        # Validasi input
        # ==============================
        if glucose == 0 or bmi == 0 or age == 0:
            st.error("❌ Input tidak valid: nilai **Glucose, BMI, atau Age** tidak boleh 0. "
                     "Periksa kembali data input sebelum melakukan prediksi.")
            st.stop()

        # Masukkan input ke dalam array
        input_values = np.array([[pregnancies, glucose, bmi, dpf, age]])

        # Lakukan prediksi
        prediction = model.predict(input_values)

        # ==============================
        # Hasil prediksi model
        # ==============================
        if prediction[0] == 1:
            st.error("⚠️ Pasien diprediksi **POSITIF Diabetes**.")
        else:
            st.success("✅ Pasien diprediksi **Tidak Diabetes**.")

        # ==============================
        # Penjelasan tambahan berdasarkan glukosa
        # ==============================
        st.subheader("📌 Keterangan Tambahan")

        if glucose < 54:
            st.error("🚨 **Hipoglikemia Berat (Glukosa <54 mg/dL)**. "
                     "Kondisi ini sangat berbahaya. Segera lakukan pemeriksaan medis lebih lanjut!")

        elif glucose < 70:
            st.warning("⚠️ **Glukosa Rendah (<70 mg/dL)**. "
                       "Segera lakukan pemeriksaan medis untuk mencegah hipoglikemia lebih lanjut.")

        elif glucose < 100:
            if prediction[0] == 1:
                st.warning("⚠️ Meskipun kadar glukosa **<100 mg/dL (normal)**, model memprediksi diabetes. "
                           "Hal ini bisa dipengaruhi oleh faktor lain seperti **BMI, usia, atau riwayat keluarga (DPF)**.")
            else:
                st.info("✅ **Glukosa Normal (<100 mg/dL)** dan model memprediksi sehat. "
                        "Tetap jaga pola hidup sehat ya! 💪")

        elif 100 <= glucose < 126:
            if prediction[0] == 1:
                st.warning("⚠️ Glukosa berada di rentang **Pradiabetes (100–125 mg/dL)** "
                           "dan model memprediksi pasien terkena diabetes. "
                           "Hal ini bisa disebabkan faktor lain seperti **kelebihan berat badan, usia lebih tua, atau riwayat keluarga**.")
            else:
                st.warning("⚠️ **Pradiabetes (100–125 mg/dL)** terdeteksi. "
                           "Model tidak memprediksi diabetes, namun kondisi ini tetap berisiko. "
                           "Sebaiknya lakukan pola hidup sehat dan lakukan kontrol rutin.")

        elif 126 <= glucose < 200:
            if prediction[0] == 1:
                st.error("🚨 **Diabetes Terdeteksi**: Glukosa (≥126 mg/dL). "
                         "Disarankan segera konsultasi ke tenaga medis dan terapkan pola hidup sehat.")
            else:
                st.warning("⚠️ **Glukosa Tinggi (≥126mg/dL)** namun model tidak mendeteksi diabetes. "
                           "Ini bisa menunjukkan pemeriksaan sewaktu. Lakukan pemeriksaan lanjutan.")

        elif glucose >= 200:
            if prediction[0] == 1:
                st.error("🚨 **Diabetes Terdeteksi (Glukosa ≥200 mg/dL)**. "
                         "Kondisi ini sangat kuat mengarah ke diabetes. Segera konsultasi medis.")
            else:
                st.warning("⚠️ **Glukosa Sangat Tinggi (≥200 mg/dL)** namun model tidak memprediksi diabetes. "
                           "Kondisi ini tidak normal. Segera lakukan pemeriksaan lanjutan ke dokter.")

        else:
            st.info("ℹ️ Data glukosa tidak sesuai kategori standar diagnosis.")

        # Catatan edukasi
        st.markdown(
            """
            ---
            📝 **Catatan Penting:**
            - Hasil prediksi di atas bertujuan untuk **Deteksi Dini Diabetes Melitus**.  
            - Diagnosis Diabetes Melitus **tidak hanya berdasarkan glukosa saja**, tetapi juga faktor lain seperti **BMI, usia, dan riwayat keluarga (DPF)**.  
            - Hasil ini adalah **prediksi model** dan bukan pengganti konsultasi medis.  
            - Untuk kepastian diagnosis, lakukan pemeriksaan lanjutan seperti **HbA1c, GTT (Tes Toleransi Glukosa), dan konsultasi dengan tenaga medis.**
            """
        )

if __name__ == "__main__":
    app()
