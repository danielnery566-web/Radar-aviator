import streamlit as st
import pandas as pd
from collections import deque

# Configuração da página para o modo estendido (melhor para tablets)
st.set_page_config(page_title="Radar Aviator Sinais Rápidos", layout="wide")

# Inicializa a memória RAM do site para guardar até 100 rodadas
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=100)

historico = st.session_state.historico

# Títulos da Interface
st.title("🎯 Radar Aviator - Modo Sinais Rápidos (2.00x - 2.50x)")
st.write("Configuração ágil para capturar correções rápidas do algoritmo")

st.divider()

# --- PAINEL LATERAL DE CONTROLE ---
st.sidebar.markdown("### 📥 Entrada de Dados")
st.sidebar.write("Digite o resultado da Betano aqui:")

# Caixa para digitar o número
novo_valor = st.sidebar.text_input("Digite a última vela (ex: 1.45) e aperte Enter:", key="input_vela")

if novo_valor:
    try:
        valor_float = float(novo_valor.replace(",", "."))
        st.session_state.historico.append(valor_float)
        st.toast(f"Vela {valor_float}x adicionada!", icon="✅")
    except ValueError:
        st.sidebar.error("Por favor, digite apenas números válidos.")

st.sidebar.divider()

# Botão para zerar os dados se você quiser recomeçar do zero
if st.sidebar.button("🗑️ Zerar Memória RAM"):
    st.session_state.historico.clear()
    st.rerun()

# --- LÓGICA MATEMÁTICA E EXIBIÇÃO DO PAINEL ---
if len(historico) > 0:
    # 1. Calcula a taxa de acerto nas últimas 20 rodadas
    ultimas_20 = list(historico)[-20:]
    greens_2x = sum(1 for v in ultimas_20 if v >= 2.0)
    porcentagem_atual = (greens_2x / len(ultimas_20)) * 100 if ultimas_20 else 0

    # 2. Descobre quantos REDs (menor que 2x) saíram em sequência no final
    reds_seguidos = 0
    for v in reversed(list(historico)):
        if v < 2.0:
            reds_seguidos += 1
        else:
            break

    # --- FILTRO DINÂMICO AGILIZADO ---
    st.markdown("### 🚨 Painel de Sinalização")
    
    # GATILHO RECALIBRADO: Mais sensível para pegar a virada mais cedo
    if reds_seguidos >= 3 and porcentagem_atual <= 45.0:
        st.error(
            f"🔥 **ALERTA DE ENTRADA ATIVO!** \n\n"
            f"Padrão de correção detectado: **{reds_seguidos} REDS** seguidos. Força atual do mercado: **{porcentagem_atual:.1f}%**.\n\n"
            f"🎯 **AÇÃO:** Entre buscando o saque entre **2.00x e 2.50x**!"
        )
    else:
        st.warning(f"⏳ **Aguardando sequência:** Atualmente com {reds_seguidos} reds. Força: {porcentagem_atual:.1f}%. O sinal vai ligar assim que bater 3 reds.")

    st.divider()

    # --- QUADROS DE INFORMAÇÃO RÁPIDA ---
    st.markdown("### 📊 Estatísticas em Tempo Real")
    col1, col2, col3 = st.columns(3)
    col1.metric("Força Recente (Alvo: <=45%)", f"{porcentagem_atual:.1f}%")
    col2.metric("Sequência de REDS (Alvo: >=3)", f"{reds_seguidos} seguidos")
    col3.metric("Rodadas Analisadas na RAM", len(historico))

    st.divider()
    
    # Exibe a lista dos últimos valores digitados para conferência
    st.markdown("📋 **Últimos valores inseridos na memória:**")
    st.info(str(list(historico)[-12:])[1:-1] + "x")
    
else:
    st.info("👋 Olá! Vá digitando os valores conforme eles saem na Betano para o radar começar a buscar os sinais rápidos.")
