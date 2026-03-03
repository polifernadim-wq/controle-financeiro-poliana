import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Controle Financeiro", layout="wide")

st.title("💰 Controle Financeiro - Poliana")

if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=[
        "Data", "Tipo", "Categoria", "Descrição", "Valor"
    ])

with st.sidebar:
    st.header("➕ Novo Lançamento")
    data = st.date_input("Data", datetime.today())
    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
    categoria = st.text_input("Categoria")
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")

    if st.button("Adicionar"):
        novo = pd.DataFrame([[data, tipo, categoria, descricao, valor]],
                            columns=st.session_state.dados.columns)
        st.session_state.dados = pd.concat([st.session_state.dados, novo], ignore_index=True)
        st.success("Lançamento adicionado!")

st.subheader("📋 Lançamentos")
st.dataframe(st.session_state.dados, use_container_width=True)

st.subheader("📊 Resumo")

if not st.session_state.dados.empty:
    total_receitas = st.session_state.dados[
        st.session_state.dados["Tipo"] == "Receita"
    ]["Valor"].sum()

    total_despesas = st.session_state.dados[
        st.session_state.dados["Tipo"] == "Despesa"
    ]["Valor"].sum()

    saldo = total_receitas - total_despesas

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Receitas", f"R$ {total_receitas:,.2f}")
    col2.metric("Total Despesas", f"R$ {total_despesas:,.2f}")
    col3.metric("Saldo", f"R$ {saldo:,.2f}")

    st.subheader("📂 Despesas por Categoria")

    despesas = st.session_state.dados[
        st.session_state.dados["Tipo"] == "Despesa"
    ]

    if not despesas.empty:
        resumo_categoria = despesas.groupby("Categoria")["Valor"].sum()
        st.bar_chart(resumo_categoria)
else:
    st.info("Adicione lançamentos para visualizar o resumo.")
