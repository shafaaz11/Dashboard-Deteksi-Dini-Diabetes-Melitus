import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import xgboost as xgb

def linear_regression_visualization(X_train, X_test, y_train, y_test):
    # membuat dan melatih model regresi linear
    model = LinearRegression(fit_intercept=True)
    model.fit(X_train, y_train)

    # menguji model latih
    y_pred = model.predict(X_test)

    # visualisasi validasi silang
    df = pd.DataFrame({'Actual WRI': y_test, 'Predicted WRI': y_pred})

    st.title("Modelling Linear Regression")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Actual WRI'],
        y=df['Predicted WRI'],
        mode='markers',
        marker=dict(color='blue'),
        text=df.index,
        hoverinfo='text+x+y'
    ))

    fig.add_trace(go.Scatter(
        x=[df['Actual WRI'].min(), df['Actual WRI'].max()],
        y=[df['Actual WRI'].min(), df['Actual WRI'].max()],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Identity Line'
    ))

    fig.update_layout(
        xaxis_title='Actual WRI',
        yaxis_title='Predicted WRI',
        title='Linear Regression (fit_intercept=True)',
        height=600,
        width=800
    )

    st.plotly_chart(fig)

    st.markdown("""
    <div style='text-align: justify;'>

    Validasi silang y_pred dengan data aktual y_test. Ini berguna untuk evaluasi kinerja model karena memungkinkan kita untuk melihat seberapa baik model melakukan prediksi pada data baru yang belum pernah dilihat selama pelatihan. Pada hasil visualisasi diatas bisa dilihat nilai aktual cukuo tersebar dan sulit diprediksi dengan benar namun tetap ada nilai nilai yang berhasil diprediksi
    """, unsafe_allow_html=True)

def xgboost_regression_visualization(X_train, X_test, y_train, y_test):
    # Create XGBoost Regressor model
    lr = 0.1
    model = xgb.XGBRegressor(learning_rate=lr)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Create a DataFrame for plotting
    df = pd.DataFrame({'Actual WRI': y_test, 'Predicted WRI': y_pred})

    # Create a scatter plot with tooltips
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Actual WRI'],
        y=df['Predicted WRI'],
        mode='markers',
        marker=dict(color='blue'),
        text=df.index,
        hoverinfo='text+x+y'
    ))

    # Add identity line
    fig.add_trace(go.Scatter(
        x=[df['Actual WRI'].min(), df['Actual WRI'].max()],
        y=[df['Actual WRI'].min(), df['Actual WRI'].max()],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Identity Line'
    ))

    # Update layout
    fig.update_layout(
        xaxis_title='Actual WRI',
        yaxis_title='Predicted WRI',
        title='XGBoost Regressor (learning_rate=0.1)',
        height=600,
        width=800
    )

    # Display the plot in Streamlit
    st.title("Modelling XGBoost Regressor")
    st.plotly_chart(fig)

    st.markdown("""
    <div style='text-align: justify;'>

    Validasi silang y_pred dengan data aktual y_test. Ini berguna untuk evaluasi kinerja model karena memungkinkan kita untuk melihat seberapa baik model melakukan prediksi pada data baru. Pada hasil visualisasi diatas bisa dilihat hampir seluruh nilai aktual diprediksi dengan benar namun ada beberapa nilai yang sedikit melenceng dari hasil prediksi tapi tidak begitu jauh dari hasil prediksi
    """, unsafe_allow_html=True)

def app():
    # Load data
    data_normalized = pd.read_csv('data_normalized.csv')

    # split data
    X = data_normalized.drop(['WRI'], axis=1)
    y = data_normalized['WRI']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # visualisasi regresi linear
    linear_regression_visualization(X_train, X_test, y_train, y_test)

    # visualisasi XGBoost Regressor
    xgboost_regression_visualization(X_train, X_test, y_train, y_test)

    # Display metric comparison
    display_metric_comparison()

def display_metric_comparison():
    data = {
        'Metric': ['MAE', 'MSE', 'RMSE', 'R^2 Score'],
        'Linear Regression(fit_intercept=True)': [0.337602003267724, 0.2703338878379385, 0.519936426727286, 0.9417344600297715],
        'XGBoost(learning_rate=0.1)': [0.11263247125601507, 0.07180614258589653, 0.26796668185783196, 0.9845234953545497]
    }

    df = pd.DataFrame(data)

    fig = go.Figure()

    colors = ['blue', 'green']
    for i, model in enumerate(['Linear Regression(fit_intercept=True)', 'XGBoost(learning_rate=0.1)']):
        values = df[model].tolist()
        fig.add_trace(go.Bar(x=df['Metric'], y=values, name=model, marker_color=[colors[i] if val > 0 else 'red' for val in values]))

    fig.update_layout(
        title='Comparison of Evaluation Metrics',
        xaxis=dict(title='Metric', tickangle=-45),
        yaxis=dict(title='Value', range=[0, 1]),
        legend=dict(title='Model')
    )

    st.plotly_chart(fig)

    st.markdown("""
    <div style='text-align: justify;'>

    Dari perbandingan skor metrik ini dapat disimpulkan bahwa model XGBoost secara konsisten lebih unggul dari Linear Regression dalam semua metrik yang dievaluasi. Jadi berdasarkan hasil ini model XGBoost dianggap lebih baik dalam memprediksi target daripada model Linear Regression untuk kasus ini
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
