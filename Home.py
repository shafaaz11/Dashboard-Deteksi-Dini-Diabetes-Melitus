import streamlit as st

def app():
    # ================================
    # Judul & Banner
    # ================================

    st.markdown(
        """
        <div style="text-align: center; padding: 15px; background-color: #D1D1D6; border-radius: 10px;">
            <h1 style="color: #2C3E50;">🩺 Deteksi Dini Diabetes Melitus</h1>
            <p style="font-size:18px; color:#2C3E50;">
                Platform Interaktif Untuk Mendukung Tenaga Medis dan Masyarakat
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("<br>", unsafe_allow_html=True)

    st.image('diabetes.webp', width='stretch')
    
    # ================================
    # Identifikasi Masalah
    # ================================
    st.markdown(
        """
        <div style="background-color:#EFEFF2; padding:20px; border-radius:10px; margin-top:20px;">
            <h3>📌 Identifikasi Masalah</h3>
            <p>Diabetes Melitus merupakan salah satu penyebab utama kematian dan komplikasi, baik di Indonesia maupun global. 
            Jumlah penderita yang terus meningkat serta keterbatasan tenaga medis menimbulkan urgensi untuk mencari solusi teknologi 
            yang efektif dalam deteksi dini penyakit ini.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ================================
    # Identifikasi Tujuan
    # ================================
    st.markdown(
        """
        <div style="background-color:#EFEFF2; padding:20px; border-radius:10px; margin-top:20px;">
            <h3>🎯 Identifikasi Tujuan</h3>
            <p><b>Membandingkan performa algoritma <span style="color:green;">XGBoost</span> dan 
            <span style="color:blue;">LDA</span> dalam mendeteksi dini Diabetes Melitus.</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ================================
    # Edukasi
    # ================================
    st.markdown(
        """
        <div style="background-color:#EFEFF2; padding:30px; border-radius:10px; margin-top:20px;">
            <h3 style="text-align:center;">🌱 Edukasi Hidup Sehat Cegah Diabetes</h3>
            <br>
            <div style="display:flex; justify-content:space-around; text-align:center;">
                <div style="width:30%;">
                    <img src="https://cdn-icons-png.flaticon.com/512/3075/3075977.png" width="80">
                    <h4>Pola Makan</h4>
                    <p>Konsumsi makanan bergizi seimbang, kurangi gula, perbanyak sayur & buah.</p>
                </div>
                <div style="width:30%;">
                    <img src="https://cdn-icons-png.flaticon.com/512/2964/2964514.png" width="80">
                    <h4>Aktivitas Fisik</h4>
                    <p>Lakukan olahraga minimal <b>30 menit/hari</b> untuk menjaga metabolisme tubuh.</p>
                </div>
                <div style="width:30%;">
                    <img src="https://cdn-icons-png.flaticon.com/512/4151/4151022.png" width="80">
                    <h4>Pola Tidur</h4>
                    <p>Tidur cukup (7–8 jam) dan hindari stres berlebih agar hormon tetap seimbang.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ================================
    # Tips Interaktif
    # ================================
    with st.expander("💡 Tips Tambahan Cegah Diabetes"):
        st.markdown(
            """
            - 🚭 Hindari merokok & alkohol berlebih.  
            - 💧 Minum air putih minimal 8 gelas per hari.  
            - 🩺 Lakukan cek kesehatan rutin (glukosa, tekanan darah, kolesterol).  
            - ⚖️ Jaga berat badan tetap ideal.  
            """
        )

    st.markdown("---")
    st.markdown(
        """
        <p style='text-align:center; color:gray;'>
            💙 Dibuat untuk penelitian <b>Deteksi Dini Diabetes Melitus</b><br>
        </p>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    app()
