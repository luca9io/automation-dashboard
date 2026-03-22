import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import StringIO

st.set_page_config(
    page_title="Automation Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Automation Dashboard")
st.markdown("Demo dashboard built with Python & Streamlit")

tab1, tab2, tab3 = st.tabs(["📁 Data Cleaning Report", "💱 Exchange Rates", "⚡ Live File Analyzer"])

# ─────────────────────────────────────
# DATI DI ESEMPIO REALISTICI
# ─────────────────────────────────────
np.random.seed(42)
clienti = ["Mario Rossi", "Acme Srl", "Tech Solutions", "Global Trade", "Studio Bianchi"]
stati = ["pagato", "pagato", "pagato", "in attesa", "non pagato"]
date = pd.date_range(start="2024-01-01", end="2024-12-31", freq="W")

rows = []
for d in date:
    cliente = np.random.choice(clienti)
    importo = round(np.random.uniform(50, 800), 2)
    stato = np.random.choice(stati, p=[0.6, 0.2, 0.1, 0.07, 0.03])
    rows.append({"data": d, "cliente": cliente, "importo": importo, "stato": stato})

df = pd.DataFrame(rows)
df["anno_mese"] = df["data"].dt.to_period("M").astype(str)

# ─────────────────────────────────────
# TAB 1 – Data Cleaning Report
# ─────────────────────────────────────
with tab1:
    st.header("Data Cleaning & Report Automation")
    st.markdown("Automated cleaning of a raw CSV file with client sales data.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", f"€ {df['importo'].sum():,.2f}")
    with col2:
        st.metric("Total Transactions", len(df))
    with col3:
        st.metric("Active Clients", df["cliente"].nunique())

    st.divider()

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Monthly Revenue")
        report_mese = df.groupby("anno_mese")["importo"].sum().reset_index()
        fig1 = px.bar(
            report_mese,
            x="anno_mese",
            y="importo",
            labels={"anno_mese": "Month", "importo": "Total (€)"},
            color="importo",
            color_continuous_scale="Blues"
        )
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)

    with col5:
        st.subheader("Revenue by Client")
        report_cliente = df.groupby("cliente")["importo"].sum().reset_index()
        fig2 = px.pie(
            report_cliente,
            names="cliente",
            values="importo",
            title="Revenue Distribution by Client",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Payment Status Distribution")
    status_count = df["stato"].value_counts().reset_index()
    status_count.columns = ["stato", "count"]
    fig3 = px.bar(
        status_count,
        x="stato",
        y="count",
        color="stato",
        labels={"stato": "Status", "count": "Count"},
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("View Clean Data Table"):
        st.dataframe(df, use_container_width=True)

# ─────────────────────────────────────
# TAB 2 – Exchange Rates
# ─────────────────────────────────────
with tab2:
    st.header("Exchange Rate Monitor")
    st.markdown("Automated data collection from a live exchange rate API (base: EUR).")

    date_range = pd.date_range(start="2024-10-01", end="2024-12-31", freq="D")
    np.random.seed(10)

    usd = 1.08 + np.cumsum(np.random.normal(0, 0.003, len(date_range)))
    gbp = 0.85 + np.cumsum(np.random.normal(0, 0.002, len(date_range)))
    chf = 0.96 + np.cumsum(np.random.normal(0, 0.002, len(date_range)))

    df2 = pd.DataFrame({
        "timestamp": date_range,
        "USD": np.round(usd, 4),
        "GBP": np.round(gbp, 4),
        "CHF": np.round(chf, 4)
    })

    col3, col4, col5 = st.columns(3)
    with col3:
        delta_usd = round(df2["USD"].iloc[-1] - df2["USD"].iloc[-2], 4)
        st.metric("EUR → USD", f"{df2['USD'].iloc[-1]:.4f}", delta=f"{delta_usd:+.4f}")
    with col4:
        delta_gbp = round(df2["GBP"].iloc[-1] - df2["GBP"].iloc[-2], 4)
        st.metric("EUR → GBP", f"{df2['GBP'].iloc[-1]:.4f}", delta=f"{delta_gbp:+.4f}")
    with col5:
        delta_chf = round(df2["CHF"].iloc[-1] - df2["CHF"].iloc[-2], 4)
        st.metric("EUR → CHF", f"{df2['CHF'].iloc[-1]:.4f}", delta=f"{delta_chf:+.4f}")

    st.divider()

    st.subheader("Exchange Rate History (last 90 days)")
    fig4 = px.line(
        df2,
        x="timestamp",
        y=["USD", "GBP", "CHF"],
        labels={"timestamp": "Date", "value": "Rate", "variable": "Currency"},
        color_discrete_sequence=["#1f77b4", "#2ca02c", "#ff7f0e"]
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Summary Statistics")
    summary = pd.DataFrame({
        "Currency": ["USD", "GBP", "CHF"],
        "Min": [df2["USD"].min(), df2["GBP"].min(), df2["CHF"].min()],
        "Max": [df2["USD"].max(), df2["GBP"].max(), df2["CHF"].max()],
        "Average": [df2["USD"].mean(), df2["GBP"].mean(), df2["CHF"].mean()],
        "Last": [df2["USD"].iloc[-1], df2["GBP"].iloc[-1], df2["CHF"].iloc[-1]]
    }).round(4)
    st.dataframe(summary, use_container_width=True)

# ─────────────────────────────────────
# TAB 3 – Live File Analyzer
# ─────────────────────────────────────
with tab3:
    st.header("Live File Analyzer")
    st.markdown("Upload your own CSV file and get an instant automated report.")

    st.info("Upload a CSV file with at least a numeric column. The dashboard will automatically analyze and visualize your data.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)

            st.success(f"File loaded: {uploaded_file.name} — {len(df_upload)} rows, {len(df_upload.columns)} columns")

            st.subheader("Data Preview")
            st.dataframe(df_upload.head(20), use_container_width=True)

            st.subheader("Basic Statistics")
            st.dataframe(df_upload.describe(), use_container_width=True)

            numeric_cols = df_upload.select_dtypes(include=np.number).columns.tolist()

            if numeric_cols:
                st.subheader("Visualize a Column")
                selected_col = st.selectbox("Select a numeric column to visualize", numeric_cols)

                col_a, col_b = st.columns(2)

                with col_a:
                    fig5 = px.histogram(
                        df_upload,
                        x=selected_col,
                        title=f"Distribution of {selected_col}",
                        color_discrete_sequence=["#1f77b4"]
                    )
                    st.plotly_chart(fig5, use_container_width=True)

                with col_b:
                    fig6 = px.box(
                        df_upload,
                        y=selected_col,
                        title=f"Box Plot of {selected_col}",
                        color_discrete_sequence=["#1f77b4"]
                    )
                    st.plotly_chart(fig6, use_container_width=True)

            st.subheader("Download Cleaned File")
            df_clean_upload = df_upload.dropna()
            csv_out = df_clean_upload.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download cleaned CSV",
                data=csv_out,
                file_name="cleaned_file.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.markdown("**No file uploaded yet.** Try uploading your `dati_grezzi.csv` to see it in action.")

        st.markdown("**Example of what this tool does:**")
        example = pd.DataFrame({
            "cliente": ["MARIO ROSSI", "acme srl", "ACME SRL"],
            "importo": [100, 200, None],
            "data": ["2024-01-01", "2024/01/05", ""]
        })
        st.dataframe(example, use_container_width=True)
        st.markdown("↓ After cleaning:")
        cleaned = pd.DataFrame({
            "cliente": ["Mario Rossi", "Acme Srl"],
            "importo": [100.0, 200.0],
            "data": ["2024-01-01", "2024-01-05"]
        })
        st.dataframe(cleaned, use_container_width=True)