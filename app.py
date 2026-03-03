import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Controle Financeiro Poliana", layout="wide")

# ----------- FUNÇÃO PARA CARREGAR CSV -----------

def carregar_csv(nome):
    if os.path.exists(nome):
        try:
            return pd.read_csv(nome, encoding="utf-8")
        except:
            return pd.read_csv(nome, encoding="latin-1")
    else:
        return pd.DataFrame()

despesas = carregar_csv("despesas_cartao.csv")
receitas = carregar_csv("receitas.csv")

# ----------- TRATAMENTO DE DATAS -----------

if not despesas.empty:
    despesas["Data da Compra"] = pd.to_datetime(despesas["Data da Compra"], dayfirst=True)
    despesas["Vencimento"] = pd.to_datetime(despesas["Vencimento"], dayfirst=True)
    despesas["Mes_Vencimento"] = despesas["Vencimento"].dt.to_period("M").astype(str)

if not receitas.empty:
    receitas["Data recebimento"] = pd.to_datetime(receitas["Data recebimento"], dayfirst=True)
    receitas["Mes_Receita"] = receitas["Data recebimento"].dt.to_period("M").astype(str)

# ----------- TÍTULO -----------

st.title("💰 Dashboard Financeiro Estratégico")

# ----------- LISTA DE MESES -----------

meses = []

if not despesas.empty:
    meses += despesas["Mes_Vencimento"].unique().tolist()

if not receitas.empty:
    meses += receitas["Mes_Receita"].unique().tolist()

meses = sorted(list(set(meses)))

if not meses:
    st.warning("Nenhum dado encontrado nos arquivos.")
    st.stop()

mes_selecionado = st.selectbox("Selecione o mês", meses)

# ----------- FILTRO POR MÊS -----------

despesas_mes = despesas[despesas["Mes_Vencimento"] == mes_selecionado]
receitas_mes = receitas[receitas["Mes_Receita"] == mes_selecionado]

# ----------- CÁLCULOS -----------

total_receitas = receitas_mes["Valor"].sum() if not receitas_mes.empty else 0
total_fatura = despesas_mes["Valor Parcela"].sum() if not despesas_mes.empty else 0

total_pago = despesas_mes[despesas_mes["Pago?"] == "SIM"]["Valor Parcela"].sum() if not despesas_mes.empty else 0
total_aberto = despesas_mes[despesas_mes["Pago?"] == "NÃO"]["Valor Parcela"].sum() if not despesas_mes.empty else 0

saldo_mes = total_receitas - total_fatura

# ----------- DASHBOARD -----------

col1, col2, col3 = st.columns(3)

col1.metric("Receitas no mês", f"R$ {total_receitas:,.2f}")
col2.metric("Total Fatura", f"R$ {total_fatura:,.2f}")
col3.metric("Saldo do mês", f"R$ {saldo_mes:,.2f}")

col4, col5 = st.columns(2)

col4.metric("Já Pago", f"R$ {total_pago:,.2f}")
col5.metric("Em Aberto", f"R$ {total_aberto:,.2f}")

# ----------- FIXO X VARIÁVEL -----------

st.subheader("Fixo x Variável")

if not despesas_mes.empty:
    resumo_tipo = despesas_mes.groupby("Fixo/Variável")["Valor Parcela"].sum()
    st.bar_chart(resumo_tipo)

# ----------- FATURA POR CARTÃO -----------

st.subheader("Fatura por Cartão")

if not despesas_mes.empty:
    resumo_cartao = despesas_mes.groupby("Cartão")["Valor Parcela"].sum()
    st.bar_chart(resumo_cartao)

# ----------- TABELAS -----------

st.subheader("Despesas do mês")
st.dataframe(despesas_mes)

st.subheader("Receitas do mês")
st.dataframe(receitas_mes)
