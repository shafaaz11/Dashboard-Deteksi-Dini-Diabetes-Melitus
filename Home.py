import streamlit as st

def app():
    st.markdown("<h1 style='text-align: center;'>DISASTER RISK SCORE PREDICTION</h1>", unsafe_allow_html=True)
    st.image('bencana.jpg', use_column_width=True)

    st.markdown("""
    <div style='text-align: justify;'>
    <h2>Business Objective</h2>
    Mengembangkan model prediktif untuk memperkirakan skor risiko bencana di berbagai negara, yang dapat digunakan untuk meningkatkan pemahaman tentang risiko bencana global dan membantu negara-negara dalam mengidentifikasi dan mengelola risiko tersebut.

    <h2>Assess Situation</h2>
    Risiko bencana alam ekstrem merupakan ancaman serius bagi keberlanjutan dan kesejahteraan negara-negara di seluruh dunia. Pengembangan model prediktif untuk memperkirakan skor risiko bencana dapat memberikan pandangan yang lebih jelas tentang faktor-faktor yang berkontribusi terhadap risiko bencana dan membantu dalam pengambilan keputusan yang lebih efektif dalam manajemen risiko. Data historis tentang paparan dan kerentanan terhadap bahaya alam ekstrem memberikan wawasan berharga tentang tren dan pola dalam risiko bencana global.

    <h2>Data Mining Goals</h2>
    <p>1. Mengembangkan model prediktif untuk memperkirakan skor risiko bencana di berbagai negara berdasarkan data historis paparan dan kerentanan.</p>
    <p>2. Menganalisis kontribusi relatif dari berbagai faktor terhadap risiko bencana dan mengidentifikasi variabel yang paling penting dalam memprediksi risiko bencana.</p>
    <p>3. Menyajikan hasil analisis dengan cara yang mudah dimengerti dan dapat digunakan oleh pemangku kepentingan untuk menginformasikan kebijakan dan tindakan.</p>
    </div>
    """, unsafe_allow_html=True)
    
if __name__ == "__main__":
    app()