import streamlit as st
import pandas as pd
from collections import deque

# Configuração da página para o modo estendido (melhor para tablets)
st.set_page_config(page_title="Radar Multi-Alvos Aviator", layout="wide")

# Inicializa a memória RAM do site para guardar até 100 rodadas
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=100)

historico = st.session_state.historico

# Títulos da Interface
st.title("⚡ Radar Aviator Inteligente - Painel de Alertas")
st.write("Análise de Múltiplos Alvos (2x, 2.5x e Velas Altas de 5x) sem gráficos")

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
    # 1. Cálculos de tendência de curto prazo
    ultimas_20 = list(historico)[-20:]
    greens_2x = sum(1 for v in ultimas_20 if v >= 2.0)
    porcentagem_atual = (greens_2x / len(ultimas_20)) * 100 if ultimas_20 else 0

    # 2. Contagem de REDs seguidos (abaixo de 2x)
    reds_seguidos = 0
    for v in reversed(list(historico)):
        if v < 2.0:
            reds_seguidos += 1
        else:
            break

    # 3. Contagem de rodadas sem nenhuma Vela Alta (>= 5.0x)
    rodadas_sem_5x = 0
    for v in reversed(list(historico)):
        if v < 5.0:
            rodadas_sem_5x += 1
        else:
            break

    # --- BLOCO CENTRAL DE ALERTAS INTELIGENTES ---
    st.markdown("### 🚨 Sinais e Alertas Disponíveis")
    
    # Flag para controlar se há algum sinal ativo na tela
    sinal_ativo = False

    # ALERTA 1: Alvo Estrito de 2.00x a 2.50x (Baseado em sequência de Reds)
    if reds_seguidos >= 4 and porcentagem_atual < 40:
        sinal_ativo = True
        st.error(
            f"🔥 **ALERTA DE ENTRADA DISPARADO! (Alvo: 2.00x - 2.50x)** \n\n"
            f"O mercado acumulou uma sequência de **{reds_seguidos} REDS** seguidos abaixo de 2x.\n\n"
            f"🎯 **AÇÃO:** Faça sua entrada na próxima rodada e coloque o Cashout Automático configurado entre **2.00x ou 2.50x** para garantir a correção do algoritmo!"
        )

    # ALERTA 2: Possível Vela Alta de 5.00x+ (Baseado em tempo de espera/seca de payout)
    if rodadas_sem_5x >= 15:
        sinal_ativo = True
        st.info(
            f"🚀 **ALERTA DE VELA ALTA DETECTADO! (Alvo: 5.00x+)** \n\n"
            f"O jogo já está há **{rodadas_sem_5x} rodadas seguidas** sem pagar nenhuma vela maior ou igual a 5x.\n\n"
            f"🎯 **AÇÃO:** Se for operar agora, reserve uma pequena parte da sua aposta para tentar buscar uma saída em **5.00x**, pois o algoritmo está entrando na janela matemática de liberação de bônus alto."
        )

    # Se nenhum padrão acima foi atingido
    if not sinal_ativo:
        st.warning(f"⏳ **AGUARDANDO PADRÃO:** Análise em execução... Sequência atual: {reds_seguidos} reds. Janela sem 5x: {rodadas_sem_5x} rodadas. Mercado morno, fique de fora.")

    st.divider()

    # --- QUADROS DE INFORMAÇÃO RÁPIDA ---
    st.markdown("### 📊 Dados de Monitoramento")
    col1, col2, col3 = st.columns(3)
    col1.metric("Força Recente (Janela 20)", f"{porcentagem_atual:.1f}%")
    col2.metric("Sequência Atual de REDS (<2x)", f"{reds_seguidos} seguidos")
    col3.metric("Tempo sem Vela Alta (>=5x)", f"{rodadas_sem_5x} rodadas")

    st.divider()
    
    # Exibe a lista dos últimos valores digitados para conferência
    st.markdown("📋 **Últimos valores inseridos na memória:**")
    st.success(str(list(historico)[-12:])[1:-1] + "x")
    
else:
    st.info("👋 Olá! Abra a Betano, e conforme as rodadas forem acontecendo, digite os valores na barra lateral e aperte Enter para o painel começar a calcular as janelas de 2x, 2.5x e 5x.")
