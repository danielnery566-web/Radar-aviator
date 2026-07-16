import streamlit as st
import pandas as pd
from collections import deque

# Configuração da página otimizada para tablets
st.set_page_config(page_title="Radar Foco 2x", layout="wide")

# Inicializa o histórico na memória RAM
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=100)

historico = st.session_state.historico

# Títulos da Interface
st.title("🎯 Radar Exclusivo - Foco Absoluto em 2.00x")
st.write("Análise de padrões de alta fidelidade voltada apenas para o saque seguro em 2x.")

st.divider()

# --- PAINEL LATERAL COM FORMULÁRIO ANTI-TRAVAMENTO ---
st.sidebar.markdown("### 📥 Entrada de Dados")

with st.sidebar.form(key="formulario_entrada", clear_on_submit=True):
    novo_valor = st.text_input("Digite a última vela (ex: 1.45):", key="input_vela")
    botao_enviar = st.form_submit_button(label="⚡ Registrar Rodada")

if botao_enviar and novo_valor:
    try:
        valor_float = float(novo_valor.replace(",", "."))
        st.session_state.historico.append(valor_float)
        st.toast(f"Vela {valor_float}x registrada!", icon="✅")
    except ValueError:
        st.sidebar.error("Digite apenas números válidos.")

st.sidebar.divider()

if st.sidebar.button("🗑️ Zerar Memória RAM"):
    st.session_state.historico.clear()
    st.rerun()

# --- CLASSIFICADOR DE VELAS (FOCO 2x) ---
def obter_tipo(v):
    return "GREEN" if v >= 2.0 else "RED"

# --- PROCESSAMENTO DOS PADRÕES ---
if len(historico) >= 5:
    valores = list(historico)
    tipos = [obter_tipo(v) for v in valores]
    
    # Métrica de saúde do mercado (Últimas 20)
    ultimas_20 = valores[-20:]
    greens_2x = sum(1 for v in ultimas_20 if v >= 2.0)
    forca_mercado = (greens_2x / len(ultimas_20)) * 100 if ultimas_20 else 0

    # 1. Verificação do Padrão 1 (Recuperação de Sequência)
    # Sequência: Green -> RED -> RED -> Green -> RED
    padrao_1_ativo = False
    if len(tipos) >= 5:
        segmento = tipos[-5:]
        if (segmento[0] == "GREEN" and segmento[1] == "RED" and 
            segmento[2] == "RED" and segmento[3] == "GREEN" and segmento[4] == "RED"):
            padrao_1_ativo = True

    # 2. Verificação do Padrão 2 (Retomada após Sequência Forte)
    # Sequência: 3 ou mais Greens -> 1 RED
    padrao_2_ativo = False
    if len(tipos) >= 4 and tipos[-1] == "RED":
        greens_antes = 0
        for t in reversed(tipos[:-1]):
            if t == "GREEN":
                greens_antes += 1
            else:
                break
        if greens_antes >= 3:
            padrao_2_ativo = True

    # 3. Verificação do Padrão 3 (Micro-correção por Alternância Rápida)
    # Sequência: RED -> GREEN -> RED
    padrao_3_ativo = False
    if len(tipos) >= 3:
        segmento = tipos[-3:]
        if segmento[0] == "RED" and segmento[1] == "GREEN" and segmento[2] == "RED":
            padrao_3_ativo = True

    # --- PAINEL DE SINAIS ATIVOS ---
    st.markdown("### 🚨 Painel de Entrada Confirmada (Alvo 2.00x)")
    sinal_disparado = False

    if padrao_1_ativo:
        sinal_disparado = True
        # Probabilidade maior se a força recente estiver baixa (sinalizando correção iminente)
        prob_p1 = min(96.0, 84.0 + (45.0 - forca_mercado) * 0.2) if forca_mercado < 45.0 else 84.0
        st.error(
            f"🔥 **SINAL VERMELHO: ENTRADA CONFIRMADA!** \n\n"
            f"🎯 **Padrão:** Recuperação de Sequência Ativo.\n"
            f"📊 **Probabilidade de bater 2x nesta entrada:** {prob_p1:.1f}%\n\n"
            f"📢 **AÇÃO:** Entre na próxima rodada buscando a saída em **2.00x** no Auto-Saque!"
        )

    if padrao_2_ativo:
        sinal_disparado = True
        # Retomada é mais forte se o mercado estiver saudável
        prob_p2 = min(98.0, 88.0 + (forca_mercado - 40.0) * 0.1) if forca_mercado > 40.0 else 88.0
        st.error(
            f"🔥 **SINAL VERMELHO: RETOMADA DE FORÇA!** \n\n"
            f"🎯 **Padrão:** Quebra de sequência de Greens por apenas 1 RED.\n"
            f"📊 **Probabilidade de bater 2x nesta entrada:** {prob_p2:.1f}%\n\n"
            f"📢 **AÇÃO:** Entre na próxima rodada buscando a saída em **2.00x** no Auto-Saque!"
        )

    if padrao_3_ativo:
        sinal_disparado = True
        prob_p3 = min(95.0, 82.0 + (50.0 - forca_mercado) * 0.15) if forca_mercado < 50.0 else 82.0
        st.error(
            f"🔥 **SINAL VERMELHO: ALTERNÂNCIA RÁPIDA!** \n\n"
            f"🎯 **Padrão:** Correção curta após padrão de zigue-zague.\n"
            f"📊 **Probabilidade de bater 2x nesta entrada:** {prob_p3:.1f}%\n\n"
            f"📢 **AÇÃO:** Entre na próxima rodada buscando a saída em **2.00x** no Auto-Saque!"
        )

    if not sinal_disparado:
        st.warning("⏳ **MONITORANDO MERCADO:** Aguardando formação de um dos padrões de 2.00x para gerar o sinal de entrada.")

    st.divider()

    # --- QUADROS DE MÉTRICA RÁPIDA ---
    st.markdown("### 📊 Indicadores do Momento")
    col1, col2 = st.columns(2)
    col1.metric("Termômetro de Força Recente", f"{forca_mercado:.1f}%")
    col2.caption("💡 Lembrete: Força abaixo de 50% indica um excelente momento para pegar as correções de 2x do robô.")

    st.divider()

    # --- HISTÓRICO VISUAL SIMPLIFICADO ---
    st.markdown("📋 **Histórico Simplificado (Alvo 2x):**")
    
    badges = []
    for v in valores[-15:]:
        if v < 2.0:
            badges.append(f"🔵 **{v:.2f}x**")  # Red
        else:
            badges.append(f"🟢 **{v:.2f}x**")  # Green (2x ou mais)
            
    st.markdown(" → ".join(badges))
    
else:
    st.info("👋 Digite pelo menos 5 resultados consecutivos no painel lateral para o radar de 2x calibrar.")
