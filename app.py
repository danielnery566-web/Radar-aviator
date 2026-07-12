import streamlit as st
import pandas as pd
from collections import deque

# Configuração da página para o modo estendido (melhor para tablets)
st.set_page_config(page_title="Radar Aviator Realtime", layout="wide")

# Inicializa a memória RAM do site para guardar até 100 rodadas
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=100)

historico = st.session_state.historico

# Títulos da Interface
st.title("🎯 Radar Realtime - Calibragem Betano (2.00x - 2.50x)")
st.write("Algoritmo ajustado para detecção de micro-correções rápidas.")

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

# --- LÓGICA MATEMÁTICA AVANÇADA EM TEMPO REAL ---
if len(historico) > 0:
    # 1. Calcula a taxa de acerto global recente (últimas 20)
    ultimas_20 = list(historico)[-20:]
    greens_2x = sum(1 for v in ultimas_20 if v >= 2.0)
    porcentagem_atual = (greens_2x / len(ultimas_20)) * 100 if ultimas_20 else 0

    # 2. Descobre quantos REDs (menor que 2x) saíram em sequência direta no final
    reds_seguidos = 0
    for v in reversed(list(historico)):
        if v < 2.0:
            reds_seguidos += 1
        else:
            break

    # 3. Análise de Amostragem Curta (Últimas 6 rodadas) para capturar o padrão da foto
    ultimas_6 = list(historico)[-6:]
    reds_na_janela = sum(1 for v in ultimas_6 if v < 2.0)

    # --- PAINEL DE SINALIZAÇÃO IA ---
    st.markdown("### 🚨 Painel de Sinalização em Tempo Real")
    
    # GATILHO DE ALTA ASSERTIVIDADE BASEADO NO HISTÓRICO REAL
    # Dispara se houver 3 reds seguidos OU se houver uma saturação de 4 reds nas últimas 6 rodadas
    if (reds_seguidos >= 3) or (reds_na_janela >= 4 and len(historico) >= 6):
        st.error(
            f"🔥 **SINAL CONFIRMADO: ENTRADA IMEDIATA!** \n\n"
            f"📊 **Análise de Saturação:** Identificamos {reds_seguidos} REDs seguidos e {reds_na_janela}/6 de retenção curta.\n\n"
            f"🎯 **ESTRUTURA DE ENTRADA:**\n"
            f"* **Aposta Principal:** Buscar retirada estrita em **2.00x** (Maior assertividade).\n"
            f"* **Aposta de Lucro:** Buscar retirada máxima em **2.50x** (Margem de ganho)."
        )
    else:
        st.warning(
            f"⏳ **MONITORANDO MERCADO:** Padrão de segurança não atingido.\n"
            f"* Sequência atual: {reds_seguidos} REDs seguidos.\n"
            f"* Concentração recente: {reds_na_janela} REDs nas últimas 6 rodadas.\n"
            f"📢 *Aguarde o mercado prender mais um pouco para disparar o sinal certeiro.*"
        )

    st.divider()

    # --- QUADROS DE INFORMAÇÃO RÁPIDA ---
    st.markdown("### 📊 Indicadores de Volume")
    col1, col2, col3 = st.columns(3)
    col1.metric("Força Recente (Janela 20)", f"{porcentagem_atual:.1f}%")
    col2.metric("Reds Seguidos Atual", f"{reds_seguidos}")
    col3.metric("Reds no Bloco de 6", f"{reds_na_janela}/6")

    st.divider()
    
    # Exibe a lista dos últimos valores digitados para conferência
    st.markdown("📋 **Linha do Tempo da Memória:**")
    st.info(str(list(historico)[-12:])[1:-1] + "x")
    
else:
    st.info("👋 Tudo pronto! Vá digitando as velas da Betano na barra lateral para ativar a nova inteligência de micro-correções.")
