import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

st.set_page_config(
    page_title="Automation Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Automation Dashboard")
st.markdown("Demo dashboard built with Python & Streamlit")

tab1, tab2 = st.tabs(["📁 Data Cleaning Report", "💱 Exchange Rates"])

# Dati di esempio hardcoded per il deploy
DATI_PULITI = """data,cliente,importo,stato,anno_mese
2025-01-01,Mario Rossi,100,pagato,2025-01
2025-02-15,Mario Rossi,300,pagato,2025-02
"""

TASSI_CAMBIO = """timestamp,USD,GBP,CHF
2026-03-22 13:54:31,1.1555,0.86438,0.9096
2026-03-22 13:55:59,1.1555,0.86438,0.9096
"""

with tab1:
    st.header("Data Cleaning & Report Automation")
    st.markdown("Automated cleaning of a raw CSV file with client sales data.")

    df = pd.read_csv(StringIO(DATI_PULITI))
    df["data"] = pd.to_datetime(df["data"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Clean Data")
        st.dataframe(df, use_container_width=True)

    with col2:
        st.subheader("Total Revenue by Month")
        report_mese = df.groupby("anno_mese")["importo"].sum().reset_index()
        fig1 = px.bar(
            report_mese,
            x="anno_mese",
            y="importo",
            labels={"anno_mese": "Month", "importo": "Total (€)"},
            color="importo",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Total Revenue by Client")
    report_cliente = df.groupby("cliente")["importo"].sum().reset_index()
    fig2 = px.pie(
        report_cliente,
        names="cliente",
        values="importo",
        title="Revenue Distribution by Client"
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("Exchange Rate Monitor")
    st.markdown("Automated data collection from a live exchange rate API (base: EUR).")

    df2 = pd.read_csv(StringIO(TASSI_CAMBIO))
    df2["timestamp"] = pd.to_datetime(df2["timestamp"])

    col3, col4, col5 = st.columns(3)

    with col3:
        st.metric("EUR → USD", f"{df2['USD'].iloc[-1]:.4f}")
    with col4:
        st.metric("EUR → GBP", f"{df2['GBP'].iloc[-1]:.4f}")
    with col5:
        st.metric("EUR → CHF", f"{df2['CHF'].iloc[-1]:.4f}")

    st.subheader("Exchange Rate History")
    fig3 = px.line(
        df2,
        x="timestamp",
        y=["USD", "GBP", "CHF"],
        labels={"timestamp": "Date", "value": "Rate", "variable": "Currency"},
        title="EUR Exchange Rates Over Time"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Raw Data")
    st.dataframe(df2, use_container_width=True)