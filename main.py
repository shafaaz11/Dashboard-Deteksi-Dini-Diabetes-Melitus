import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu
import Home
import EDA
import Modelling
import Prediction

# Read the data
data = pd.read_csv('cleaned_diabetes.csv')

st.set_page_config(
    page_title="Deteksi Dini Diabetes Melitus",
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        with st.sidebar:  
            # Tambahkan watermark teks di atas logo
            st.markdown(
                """
                <div style="text-align: center; color: gray; font-size:12px; line-height:1.2; margin-bottom:10px;">
                    Universitas Mulawarman<br>
                    Sistem Informasi
                </div>
                """,
                unsafe_allow_html=True
            )

            # Logo berdampingan (kiri-kanan)
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.image("unmul.png", width=1000)
            # with col2:
            #     st.image("inforsa.png", use_container_width=True)

            # st.markdown("<br>", unsafe_allow_html=True)  # jarak sedikit

            # Menu navigasi
            app = option_menu(
                menu_title='Menu',
                options=['Home', 'EDA', 'Modelling', 'Prediction'],
                icons=['house-fill', 'graph-up', 'robot', 'pencil'],
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": "white"},
                    "icon": {"color": "black", "font-size": "23px"}, 
                    "nav-link": {
                        "color": "black",
                        "font-size": "20px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "lightblue"
                    },
                    "nav-link-selected": {"background-color": "#3498DB", "color": "white"},  # biru
                }
            )

        if app == "Home":
            Home.app()
        if app == "EDA":
            EDA.app()    
        if app == "Modelling":
            Modelling.app()        
        if app == 'Prediction':
            Prediction.app()

    run()

