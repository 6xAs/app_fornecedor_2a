
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Caminhos dos arquivos
produtos_path = "database/produtos/produtos_completos.csv"
vendas_dir = "database/vendas"
os.makedirs(vendas_dir, exist_ok=True)

st.set_page_config(page_title="Fornecedor 2ºA", layout="wide")
st.title("🛒 Sistema de Compras - Fornecedor 2ºA")

# Estado do carrinho
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# Carregamento dos dados com tratamento
try:
    df_produtos = pd.read_csv(produtos_path)
    assert not df_produtos.empty, "Arquivo de produtos está vazio!"
except Exception as e:
    st.error(f"❌ Erro ao carregar produtos: {e}")
    st.stop()

# Seleção do produto
produto_selecionado = st.selectbox("Selecione um produto", df_produtos["Nome do Produto"].unique())
produto_info = df_produtos[df_produtos["Nome do Produto"] == produto_selecionado].iloc[0]

# Exibir detalhes
st.subheader("📦 Informações do Produto")
st.write(f"**Categoria:** {produto_info['Categoria']}")
st.write(f"**Descrição:** {produto_info['Descrição']}")
st.write(f"**Preço Final (R$):** {produto_info['Preço Final c/ Impostos (R$)']:.2f}")

quantidade = st.number_input("Quantidade", min_value=1, step=1)

# Adicionar ao carrinho
if st.button("➕ Adicionar ao Carrinho"):
    try:
        item = {
            "Produto": produto_selecionado,
            "Categoria": produto_info["Categoria"],
            "Quantidade": quantidade,
            "Valor Unitário (R$)": produto_info["Preço Final c/ Impostos (R$)"],
            "Valor Total (R$)": quantidade * produto_info["Preço Final c/ Impostos (R$)"]
        }
        st.session_state.carrinho.append(item)
        st.success("Produto adicionado ao carrinho.")
    except Exception as e:
        st.error(f"Erro ao adicionar item ao carrinho: {e}")

# Mostrar carrinho
if st.session_state.carrinho:
    st.subheader("🛒 Carrinho de Compras")
    df_carrinho = pd.DataFrame(st.session_state.carrinho)
    total_geral = df_carrinho["Valor Total (R$)"].sum()
    st.dataframe(df_carrinho)
    st.markdown(f"**💰 Total da Compra: R$ {total_geral:,.2f}**")

    st.subheader("👤 Finalizar Compra")
    nome = st.text_input("Nome do Comprador")
    empresa = st.text_input("Empresa / Equipe")
    email = st.text_input("Email")
    encargo_percentual = 0.20

    if st.button("💾 Finalizar Pedido"):
        if not nome or not empresa or not email:
            st.warning("⚠️ Preencha todos os campos antes de finalizar.")
        else:
            try:
                registros = []
                for item in st.session_state.carrinho:
                    nova_venda = {
                        "Data da Compra": datetime.today().strftime('%Y-%m-%d'),
                        "Nome do Comprador": nome,
                        "Empresa": empresa,
                        "Email": email,
                        "Produto": item["Produto"],
                        "Categoria": item["Categoria"],
                        "Quantidade": item["Quantidade"],
                        "Valor Unitário (R$)": item["Valor Unitário (R$)"],
                        "Valor Total (R$)": item["Valor Total (R$)"],
                        "Encargo (%)": encargo_percentual * 100,
                        "Encargo (R$)": item["Valor Total (R$)"] * encargo_percentual
                    }
                    registros.append(nova_venda)

                df_vendas = pd.DataFrame(registros)
                nome_arquivo = f"{vendas_dir}/venda_{nome.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
                df_vendas.to_csv(nome_arquivo, index=False)

                st.success(f"✅ Pedido finalizado com sucesso! Arquivo salvo em: {nome_arquivo}")
                st.session_state.carrinho = []
            except Exception as e:
                st.error(f"Erro ao registrar vendas: {e}")
else:
    st.info("Seu carrinho está vazio.")
