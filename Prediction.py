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
    st.write(data.head())
    st.warning("⚠️ Silahkan masukkan data pasien untuk memprediksi pasien (tidak diabetes (0) & diabetes (1)")
    # Buat tata letak grid untuk input
    col1, col2, col3 = st.columns(3)

    with col1:
        pregnancies = st.number_input("Jumlah Kehamilan (Pregnancies)", min_value=0, max_value=20, step=1)

    with col2:
        glucose = st.number_input("Kadar Glukosa (Glucose) (mg/dL)", min_value=0, max_value=300, step=1)

    with col3:
        bmi = st.number_input("Indeks Massa Tubuh (BMI)", min_value=0.0, max_value=70.0, step=0.1)

    with col1:
        dpf = st.number_input(
            "Diabetes Pedigree Function",
            min_value=0.0,
            max_value=3.0,
            step=0.001,
            format="%.3f"
        )

    with col2:
        age = st.number_input("Usia (Age)", min_value=0, max_value=120, step=1)

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
                     "Namun Kondisi ini sangat berbahaya dan bisa menyebabkan gejala serius "
                     "Segera lakukan pemeriksaan medis lebih lanjut!")

        elif glucose < 70:
            st.warning("⚠️ **Glukosa Rendah (<70 mg/dL)**. "
                       "Kondisi ini tidak normal dan perlu perhatian. "
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
                st.error("🚨 **Diabetes Terdeteksi**: Glukosa (≥126 mg/dL)"
                         "Disarankan segera konsultasi ke tenaga medis dan terapkan pola hidup sehat.")
            else:
                st.warning("⚠️ **Glukosa Tinggi (≥126mg/dL)** namun model tidak mendeteksi diabetes. "
                           "Ini bisa menunjukkan bahwa pasien melakukan pemeriksaan glukosa sewaktu. Namun sebaiknya lakukan pemeriksaan lanjutan dan lakukan pola hidup sehat.")

        elif glucose >= 200:
            if prediction[0] == 1:
                st.error("🚨 **Diabetes Terdeteksi (Glukosa ≥200 mg/dL)**. "
                         "Kondisi ini sangat kuat mengarah ke diabetes. Segera lakukan konsultasi medis.")
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
            - Hasil prediksi diatas bertujuan untuk Mendeteksi Dini Diabetes Melitus  
            - Diagnosis Diabetes Melitus **tidak hanya berdasarkan glukosa saja**, tetapi juga faktor lain seperti **BMI, usia, dan riwayat keluarga (DPF)**.  
            - Hasil ini adalah **prediksi model** dan bukan pengganti konsultasi medis.  
            - Untuk kepastian diagnosis, lakukan pemeriksaan lanjutan seperti **HbA1c, GTT (Tes Toleransi Glukosa), dan konsultasi dengan tenaga medis.**
            """
        )

if __name__ == "__main__":
    app()