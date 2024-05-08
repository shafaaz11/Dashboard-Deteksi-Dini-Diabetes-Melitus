import streamlit as st
import pandas as pd
import numpy as np
import pickle

def app():
    data = pd.read_csv('data_normalized.csv')
    model = pickle.load(open("xgboost.sav", "rb"))

    st.title("Disaster Risk Score Predict")
    st.write(data.head())

    # Buat tata letak grid untuk input
    col1, col2, col3 = st.columns(3)

    with col1:
        Exposure = st.text_input("Tingkat Paparan Risiko(E)")

    with col2:
        Vulnerability = st.text_input("Kerentanan Terkena Risiko(V)")

    with col3:
        Susceptibility = st.text_input("Kerentanan Terpengaruh Risiko(S)")

    with col1:
        Lack_of_Coping_Capabilities = st.text_input("Tidak Mampu Mengatasi Risiko(LCC)")

    with col2:
        Lack_of_Adaptive_Capacities = st.text_input("Tidak Mampu Beradaptasi(LAC)")

    with col3:
        Exposure_Category = st.text_input("Kategori Tingkat Paparan Risiko(EC)")

    with col1:
        WRI_Category = st.text_input("Kategori Skor Risiko(WC)")

    with col2:
        Vulnerability_Category = st.text_input("Kategori Terkena Risiko(VC)")

    with col3:
        Susceptibility_Category = st.text_input("Kategori Terpengaruh Risiko(SC)")
    
    if st.button("Disaster Risk Score Predict"):
        input_values = []
        for input_value in [
            Exposure, Vulnerability, Susceptibility, 
            Lack_of_Coping_Capabilities, Lack_of_Adaptive_Capacities, 
            Exposure_Category, WRI_Category, Vulnerability_Category, 
            Susceptibility_Category
        ]:
            if input_value.strip() == '':
                st.error("Please fill all input values")
                break
            input_values.append(float(input_value.strip()))
        else:
            predicted_WRI = model.predict([input_values])
            st.write("Predicted WRI:", predicted_WRI[0])
            

if __name__ == "__main__":
    app()
