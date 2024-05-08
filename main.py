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
data = pd.read_csv('data.csv')

st.set_page_config(
    page_title="Score Prediction",
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
            app = option_menu(
                menu_title='Menu',
                options=['Home', 'EDA' , 'Modelling' , 'Prediction'],
                icons=['house-fill', 'graph-up', 'robot', 'pencil'],
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
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
          
         

