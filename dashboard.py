
import streamlit as st
import pandas as pd

# Caminho do arquivo de vendas
vendas_path = "database/vendas/vendas.csv"

st.title("📊 Dashboard de Vendas - Fornecedor 2ºA")

try:
    df_vendas = pd.read_csv(vendas_path)
except FileNotFoundError:
    df_vendas = pd.DataFrame()

if not df_vendas.empty:
    total_vendas = df_vendas["Valor Total (R$)"].sum()
    total_encargos = df_vendas["Encargo (R$)"].sum()
    total_itens = df_vendas["Quantidade"].sum()
    lucro_liquido = total_vendas - total_encargos

    st.metric("🛍️ Total em Vendas (R$)", f"{total_vendas:,.2f}")
    st.metric("📉 Total de Encargos (R$)", f"{total_encargos:,.2f}")
    st.metric("📦 Quantidade Total Vendida", int(total_itens))
    st.metric("💰 Lucro Líquido Estimado (R$)", f"{lucro_liquido:,.2f}")

    st.subheader("📄 Vendas Registradas")
    st.dataframe(df_vendas)
else:
    st.warning("Nenhuma venda registrada ainda.")
