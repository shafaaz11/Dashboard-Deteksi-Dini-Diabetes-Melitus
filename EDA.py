import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def app():
    # Read the data
    data = pd.read_csv('data.csv')
    datamap = pd.read_csv('data_normalized.csv')
    
    # Korelasi Metrik Heatmap
    numeric_data = datamap.select_dtypes(include=['int', 'float'])
    correlation_matrix = numeric_data.corr()
    st.title('Correlation Heatmap')
    fig = px.imshow(correlation_matrix, 
                    labels=dict(x="Features", y="Features", color="Correlation"),
                    x=correlation_matrix.index,
                    y=correlation_matrix.columns,
                    color_continuous_scale='RdBu_r')

    fig.update_layout(width=800,
                      height=600)

    st.plotly_chart(fig)

    st.markdown("""
    <div style='text-align: justify;'>

    Pada visualisasi diatas kita bisa melihat hubungan fitur fitur yang ada dengan fitur WRI, pada hasil pengamatan kita memutuskan untuk memakai seluruh fitur yang ada karena semua berada diatas nilai 0 dan tidak ada yang ngeatif, berarti fitur fitur yang ada berhubungan atau berkorelasi dengan fitur WRI. Namun kita tidak memakai kolom WRI karena kolom WRI itu sendiri yang akan diprediksi
    """, unsafe_allow_html=True)
    
    # Sidebar Tahun
    st.sidebar.title('🌊 WRI Score Dashboard')
    selected_year = st.sidebar.selectbox('Select a year', sorted(data['Year'].unique(), reverse=True))

    st.title(f'Top and Bottom 10 Regions with WRI Score in {selected_year}')

    # Fungsi buat nampilin top 10 wri tertinggi
    def top10(year):
        return data[data['Year'] == year].sort_values(by='WRI', ascending=False).head(10)

    # Fungsi buat nampilin bottom 10 wri terendah
    def bottom10(year):
        return data[data['Year'] == year].sort_values(by='WRI').head(10)

    # Plot top 10 negara tertinggi
    top10_data = top10(selected_year)
    fig_top10 = px.bar(top10_data, x='WRI', y='Region', orientation='h', title=f'Top 10 Regions with Highest WRI Score in {selected_year}', color='WRI')
    st.plotly_chart(fig_top10)
    
    st.markdown("""
    <div style='text-align: justify;'>

    Pada gambar diatas kita bisa melihat 10 negara dengan skor WRI tertinggi, kita bisa memfilter tahunnya pada bagian sidebar untuk melihat 10 negara dengan risiko bencana tertinggi disetiap tahunnnya
    """, unsafe_allow_html=True)
    
    # Plot bottom 10 negara terendah
    bottom10_data = bottom10(selected_year)
    fig_bottom10 = px.bar(bottom10_data, x='WRI', y='Region', orientation='h', title=f'Top 10 Regions with Lowest WRI Score in {selected_year}', color='WRI')
    st.plotly_chart(fig_bottom10)

    st.markdown("""
    <div style='text-align: justify;'>

    Pada gambar diatas kita bisa melihat 10 negara dengan skor WRI terendah, kita bisa memfilter tahunnya pada bagian sidebar untuk melihat 10 negara dengan risiko bencana terendah disetiap tahunnnya
    """, unsafe_allow_html=True)

# Jika file ini dijalankan sebagai script utama, jalankan fungsi `app()`
if __name__ == "__main__":
    app()
