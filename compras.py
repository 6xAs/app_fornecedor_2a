
import streamlit as st
import pandas as pd
from datetime import datetime


# Caminhos dos arquivos
produtos_path = "database/produtos/produtos.csv"
vendas_path = "database/vendas/vendas.csv"


st.title("🛒 Compras - Fornecedor 2ºA")

# Estado do carrinho
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# Carregamento dos dados com tratamento de erro
try:
    df_produtos = pd.read_csv(produtos_path)
    assert not df_produtos.empty, "Arquivo de produtos está vazio!"
    assert "Nome do Produto" in df_produtos.columns, "Coluna 'Nome do Produto' não encontrada!"
except Exception as e:
    st.error(f"❌ Erro ao carregar produtos: {e}")
    st.stop()

try:
    df_vendas = pd.read_csv(vendas_path)
except:
    df_vendas = pd.DataFrame(columns=[
        "Data da Compra", "Nome do Comprador", "Empresa", "Email",
        "Produto", "Categoria", "Quantidade", 
        "Valor Unitário (R$)", "Valor Total (R$)", "Encargo (%)", "Encargo (R$)"
    ])

# Seleção do produto com erro visível
try:
    produto_selecionado = st.selectbox("Selecione um produto", df_produtos["Nome do Produto"].unique())
    produto_info = df_produtos[df_produtos["Nome do Produto"] == produto_selecionado]

    if produto_info.empty:
        st.error("❗ Produto não encontrado na base de dados.")
        st.stop()

    produto_info = produto_info.iloc[0]
except Exception as e:
    st.error(f"❌ Erro ao selecionar produto: {e}")
    st.stop()

# Exibir dados do produto
try:
    st.subheader("📦 Detalhes do Produto")
    st.write(f"**Categoria:** {produto_info['Categoria']}")
    st.write(f"**Descrição:** {produto_info.get('Descrição', '---')}")
    st.write(f"**Estoque Disponível:** {int(produto_info['Estoque Disponível'])}")
    st.write(f"**Preço Final c/ Impostos (R$):** R$ {produto_info['Preço Final c/ Impostos (R$)']:.2f}")

    quantidade = st.number_input("Quantidade", min_value=1, max_value=int(produto_info["Estoque Disponível"]), step=1)
except Exception as e:
    st.error(f"Erro ao mostrar detalhes: {e}")
    st.stop()

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
    st.dataframe(pd.DataFrame(st.session_state.carrinho))

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
                    df_vendas = pd.concat([df_vendas, pd.DataFrame([nova_venda])], ignore_index=True)

                df_vendas.to_csv(vendas_path, index=False)
                st.success("✅ Pedido finalizado com sucesso!")
                st.session_state.carrinho = []
            except Exception as e:
                st.error(f"Erro ao registrar vendas: {e}")
else:
    st.info("Seu carrinho está vazio.")
