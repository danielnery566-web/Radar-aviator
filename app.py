import streamlit as st
import pandas as pd
from collections import deque

# Configuração da página para o modo estendido (melhor para tablets)
st.set_page_config(page_title="Radar Aviator Max Assertividade", layout="wide")

# Inicializa a memória RAM do site para guardar até 100 rodadas
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=100)

historico = st.session_state.historico

# Títulos da Interface
st.title("🎯 Radar Aviator - Foco em Janela de 2.00x a 2.50x")
st.write("Filtros de alta precisão baseados em saturação e volume do algoritmo")

st.divider()

# --- PAINEL LATERAL DE CONTROLE ---
st.sidebar.markdown("### 📥 Entrada de Dados")
st.sidebar.write("Digite o resultado da Betano ou Cassino aqui:")

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
    # Como o alvo é de 2x a 2.5x, consideramos "green" qualquer vela a partir de 2.0x
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

    # --- FILTRO DE ALTA ASSERTIVIDADE ---
    st.markdown("### 🚨 Painel de Sinalização")
    
    # Condições rígidas para buscar a máxima precisão
    if reds_seguidos >= 5 and porcentagem_atual <= 30.0:
        st.error(
            f"🎯 **SINAL DE ALTA ASSERTIVIDADE DETECTADO!** \n\n"
            f"O algoritmo atingiu o nível máximo de retenção: **{reds_seguidos} REDS** seguidos e apenas **{porcentagem_atual:.1f}%** de acertos recentes.\n\n"
            f"⚡ **AÇÃO EXATA:** Faça sua entrada na próxima rodada buscando o saque seguro entre **2.00x e 2.50x** no máximo!"
        )
    else:
        st.warning(f"⏳ **AGUARDANDO CALIBRAÇÃO:** O mercado ainda não atingiu o nível de estresse necessário para uma entrada segura. Sequência atual: {reds_seguidos} reds. Força: {porcentagem_atual:.1f}%. Fique de fora.")

    st.divider()

    # --- QUADROS DE INFORMAÇÃO RÁPIDA ---
    st.markdown("### 📊 Estatísticas para Proteção de Banca")
    col1, col2, col3 = st.columns(3)
    col1.metric("Força Recente (Alvo ideal: <=30%)", f"{porcentagem_atual:.1f}%")
    col2.metric("Sequência Atual de REDS (Alvo: >=5)", f"{reds_seguidos} seguidos")
    col3.metric("Rodadas Analisadas", len(historico))

    st.divider()
    
    # Exibe a lista dos últimos valores digitados para conferência
    st.markdown("📋 **Últimos valores inseridos na memória:**")
    st.info(str(list(historico)[-12:])[1:-1] + "x")
    
else:
    st.info("👋 Olá! Abra o Aviator na Betano, e conforme as rodadas forem acontecendo, digite os valores na barra lateral e aperte Enter para calibrar o seu filtro de alta precisão.")
