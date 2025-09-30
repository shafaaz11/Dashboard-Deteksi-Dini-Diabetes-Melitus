import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from xgboost import XGBClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis



def app():
    # Load dataset
    data = pd.read_csv("cleaned_diabetes.csv")

    # Pisahkan fitur & target
    X = data.drop(['Outcome'], axis=1)
    y = data['Outcome']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ========================
    # Judul Halaman
    # ========================
    st.markdown(
        """
        <div style="background-color:#D1D1D6; padding:20px; border-radius:10px; margin-bottom:20px;">
            <h2 style="text-align:center; color:#2C3E50;">🔎 Modelling: XGBoost vs LDA</h2>
            <p style="text-align:center; font-size:16px; color:#2C3E50;">
                Perbandingan dua algoritma Machine Learning untuk mendeteksi dini Diabetes Melitus
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================
    # XGBoost
    # ========================
    st.markdown(
        """
        <div style="background-color:#EFEFF2; padding:20px; border-radius:10px; margin-top:10px;">
            <h3>📌 Model XGBoost</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Implementasi XGBoost sesuai teori 
    xgb_model = XGBClassifier(
        n_estimators=100,            # t -> jumlah iterasi/pohon
        learning_rate=0.1,           # η -> step size shrinkage
        max_depth=5,                 # kedalaman pohon
        gamma=0.1,                   # γ -> penalti jumlah daun
        reg_lambda=1.0,              # λ -> regulasi L2 bobot daun
        reg_alpha=0.5,               # α -> regulasi L1 bobot daun
        subsample=0.8,               # sampling baris
        colsample_bytree=0.8,        # sampling fitur
        objective="binary:logistic", # fungsi objektif -> logloss
        eval_metric="logloss",       # evaluasi loss logistik
    )

    # Training model
    xgb_model.fit(X_train, y_train)

    # Prediksi
    y_pred_xgb = xgb_model.predict(X_test)

    # Confusion Matrix
    cm_xgb = confusion_matrix(y_test, y_pred_xgb)
    z_text = [[str(y) for y in x] for x in cm_xgb]

    fig_xgb = ff.create_annotated_heatmap(
        z=cm_xgb, x=['Negatif', 'Positif'], y=['Negatif', 'Positif'],
        annotation_text=z_text, colorscale='Blues'
    )
    fig_xgb.update_layout(title="Confusion Matrix - XGBoost")
    st.plotly_chart(fig_xgb, use_container_width=True)

    # Evaluasi
    acc_xgb = accuracy_score(y_test, y_pred_xgb)
    prec_xgb = precision_score(y_test, y_pred_xgb)
    rec_xgb = recall_score(y_test, y_pred_xgb)
    f1_xgb = f1_score(y_test, y_pred_xgb)

    st.info(f"""
    **Hasil Evaluasi XGBoost**  
    - Accuracy: {acc_xgb:.4f}  
    - Precision: {prec_xgb:.4f}  
    - Recall: {rec_xgb:.4f}  
    - F1 Score: {f1_xgb:.4f}  
    """)


    # ========================
    # LDA
    # ========================
    st.markdown(
        """
        <div style="background-color:#EFEFF2; padding:20px; border-radius:10px; margin-top:20px;">
            <h3>📌 Model LDA</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    lda_model = LinearDiscriminantAnalysis(solver='eigen')
    lda_model.fit(X_train, y_train)
    y_pred_lda = lda_model.predict(X_test)

    cm_lda = confusion_matrix(y_test, y_pred_lda)
    z_text = [[str(y) for y in x] for x in cm_lda]

    fig_lda = ff.create_annotated_heatmap(
        z=cm_lda, x=['Negatif', 'Positif'], y=['Negatif', 'Positif'],
        annotation_text=z_text, colorscale='Blues'
    )
    fig_lda.update_layout(title="Confusion Matrix - LDA")
    st.plotly_chart(fig_lda, use_container_width=True)

    acc_lda = accuracy_score(y_test, y_pred_lda)
    prec_lda = precision_score(y_test, y_pred_lda)
    rec_lda = recall_score(y_test, y_pred_lda)
    f1_lda = f1_score(y_test, y_pred_lda)

    st.info(f"""
    **Hasil Evaluasi LDA**  
    - Accuracy: {acc_lda:.4f}  
    - Precision: {prec_lda:.4f}  
    - Recall: {rec_lda:.4f}  
    - F1 Score: {f1_lda:.4f}  
    """)

    # ========================
    # Perbandingan Evaluasi
    # ========================
    st.markdown(
        """
        <div style="background-color:#EFEFF2; padding:20px; border-radius:10px; margin-top:20px;">
            <h3>📊 Perbandingan Evaluasi Model</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    df_eval = pd.DataFrame({
        "Model": ["XGBoost", "LDA"],
        "Accuracy": [acc_xgb, acc_lda],
        "Precision": [prec_xgb, prec_lda],
        "Recall": [rec_xgb, rec_lda],
        "F1 Score": [f1_xgb, f1_lda]
    })

    df_visual = df_eval.melt(id_vars="Model", var_name="Metrik", value_name="Score")

    fig_compare = px.bar(
        df_visual, x="Metrik", y="Score", color="Model",
        barmode="group", text="Score",
        title="Perbandingan Evaluasi Model XGBoost vs LDA",
        labels={"Score": "Nilai", "Metrik": "Jenis Evaluasi"},
        color_discrete_map={"XGBoost": "#CBDCEB", "LDA": "#6D94C5"}  # soft blue & teal
    )
    fig_compare.update_traces(texttemplate='%{text:.4f}', textposition='outside')
    fig_compare.update_layout(yaxis=dict(range=[0, 1]))
    st.plotly_chart(fig_compare, use_container_width=True)

    st.info("👉 Dari hasil evaluasi, model **XGBoost** menunjukkan performa lebih baik dibandingkan **LDA** di semua metrik.")

if __name__ == "__main__":
    app()
