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
        n_estimators=100,
        learning_rate=0.2,
        max_depth=7,
        gamma=0.1,
    )

    # Training model
    xgb_model.fit(X_train, y_train)

    # Prediksi
    y_pred_xgb = xgb_model.predict(X_test)

    # Confusion Matrix
    cm_xgb = confusion_matrix(y_test, y_pred_xgb)
    TP, FN, FP, TN = cm_xgb[1, 1], cm_xgb[1, 0], cm_xgb[0, 1], cm_xgb[0, 0]

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
    - True Positive (TP): {TP} → Pasien diabetes yang berhasil diprediksi benar sebagai diabetes  
    - False Negative (FN): {FN} → Pasien diabetes tetapi salah diprediksi tidak diabetes  
    - True Negative (TN): {TN} → Pasien tidak diabetes yang berhasil diprediksi benar sebagai tidak diabetes  
    - False Positive (FP): {FP} → Pasien tidak diabetes tetapi salah diprediksi sebagai diabetes  

    **Metrik Evaluasi:**  
    - Accuracy ({acc_xgb:.2%}) → Seberapa banyak prediksi yang benar dari total data  
    - Precision ({prec_xgb:.2%}) → Dari semua yang diprediksi diabetes, berapa yang benar-benar diabetes  
    - Recall ({rec_xgb:.2%}) → Dari semua pasien diabetes, berapa banyak yang bisa ditemukan  
    - F1 Score ({f1_xgb:.2%}) → Rata-rata harmonis antara Precision dan Recall  
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

    lda_model = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
    lda_model.fit(X_train, y_train)
    y_pred_lda = lda_model.predict(X_test)

    cm_lda = confusion_matrix(y_test, y_pred_lda)
    TP, FN, FP, TN = cm_lda[1, 1], cm_lda[1, 0], cm_lda[0, 1], cm_lda[0, 0]

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
    - True Positive (TP): {TP} → Pasien diabetes yang berhasil diprediksi benar sebagai diabetes  
    - False Negative (FN): {FN} → Pasien diabetes tetapi salah diprediksi tidak diabetes  
    - True Negative (TN): {TN} → Pasien tidak diabetes yang berhasil diprediksi benar sebagai tidak diabetes  
    - False Positive (FP): {FP} → Pasien tidak diabetes tetapi salah diprediksi sebagai diabetes  

    **Metrik Evaluasi:**  
    - Accuracy ({acc_lda:.2%}) → Seberapa banyak prediksi yang benar dari total data  
    - Precision ({prec_lda:.2%}) → Dari semua yang diprediksi diabetes, berapa yang benar-benar diabetes  
    - Recall ({rec_lda:.2%}) → Dari semua pasien diabetes, berapa banyak yang bisa ditemukan  
    - F1 Score ({f1_lda:.2%}) → Rata-rata harmonis antara Precision dan Recall  
    """)

    # ========================
    # Perbandingan Evaluasi
    # ========================
    st.subheader("📊 Perbandingan Evaluasi Model")

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
        color_discrete_map={"XGBoost": "#CBDCEB", "LDA": "#6D94C5"}
    )
    fig_compare.update_traces(texttemplate='%{text:.4f}', textposition='outside')
    fig_compare.update_layout(yaxis=dict(range=[0, 1]))
    st.plotly_chart(fig_compare, use_container_width=True)

    st.info("👉 Dari hasil evaluasi, model **XGBoost** menunjukkan performa lebih baik dibandingkan **LDA** di semua metrik.")


if __name__ == "__main__":
    app()
