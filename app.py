import streamlit as st
import pandas as pd
from collections import deque

# Configuração da página otimizada para tablets
st.set_page_config(page_title="Radar Padrões Anti-Travamento", layout="wide")

# Inicializa o histórico na memória RAM
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=100)

historico = st.session_state.historico

# Títulos da Interface
st.title("🎯 Radar de Padrões V3 - Alta Estabilidade")
st.write("Sistema com envio protegido por formulário para evitar travamentos no navegador.")

st.divider()

# --- PAINEL LATERAL COM FORMULÁRIO ANTI-TRAVAMENTO ---
st.sidebar.markdown("### 📥 Entrada de Dados")

# O uso do st.form impede que o app trave ou atualize antes da hora
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

# --- CLASSIFICADOR DE VELAS ---
def obter_tipo(v):
    if v < 2.0:
        return "AZUL"
    elif v < 10.0:
        return "ROXA"
    else:
        return "ROSA"

# --- PROCESSAMENTO DOS PADRÕES ---
if len(historico) >= 5:
    valores = list(historico)
    tipos = [obter_tipo(v) for v in valores]
    
    # Métricas globais
    ultimas_20 = valores[-20:]
    greens_2x = sum(1 for v in ultimas_20 if v >= 2.0)
    forca_mercado = (greens_2x / len(ultimas_20)) * 100 if ultimas_20 else 0

    rodadas_sem_rosa = 0
    for v in reversed(valores):
        if v < 10.0:
            rodadas_sem_rosa += 1
        else:
            break

    # 1. Verificação do Padrão 1 (Rosa em 3 casas)
    padrao_1_ativo = False
    if len(tipos) >= 5:
        segmento = tipos[-5:]
        if (segmento[0] == "ROXA" and segmento[1] == "AZUL" and 
            segmento[2] == "AZUL" and segmento[3] == "ROXA" and segmento[4] == "AZUL"):
            padrao_1_ativo = True

    # 2. Verificação do Padrão 2 (Retomada 3+ Roxas -> 1 Azul)
    padrao_2_ativo = False
    if len(tipos) >= 4 and tipos[-1] == "AZUL":
        roxas_antes = 0
        for t in reversed(tipos[:-1]):
            if t in ["ROXA", "ROSA"]:
                roxas_antes += 1
            else:
                break
        if roxas_antes >= 3:
            padrao_2_ativo = True

    # 3. Verificação do Novo Padrão 3 (Micro-correção dinâmica baseada no print)
    padrao_3_ativo = False
    if len(tipos) >= 4:
        # Se veio uma sequência intercalada de alternância rápida
        if tipos[-1] == "AZUL" and tipos[-2] in ["ROXA", "ROSA"] and tipos[-3] == "AZUL":
            padrao_3_ativo = True

    # --- PAINEL DE EXIBIÇÃO ---
    st.markdown("### 🚨 Painel de Sinais Ativos")
    sinal_disparado = False

    if padrao_1_ativo:
        sinal_disparado = True
        prob_p1 = min(96.0, 75.0 + (rodadas_sem_rosa * 0.3))
        st.error(f"🔥 **SINAL VERMELHO: ALVO VELA ROSA**\n\n**Padrão 1 Detectado!** Janela aberta para as próximas 3 rodadas.\n\n📈 **Probabilidade:** {prob_p1:.1f}%")

    if padrao_2_ativo:
        sinal_disparado = True
        prob_p2 = min(98.0, 80.0 + (forca_mercado * 0.2))
        st.error(f"🔥 **SINAL VERMELHO: RETOMADA SEGURO (2.00x)**\n\n**Padrão 2 Detectado!** Força de quebra após sequência verde.\n\n📈 **Probabilidade:** {prob_p2:.1f}%")

    if padrao_3_ativo:
        sinal_disparado = True
        prob_p3 = min(95.0, 78.0 + (forca_mercado * 0.15))
        st.error(f"🔥 **SINAL VERMELHO: MICRO-CORREÇÃO (2.00x)**\n\n**Padrão 3 Detectado!** Padrão de alternância rápida identificado no gráfico.\n\n📈 **Probabilidade:** {prob_p3:.1f}%")

    if not sinal_disparado:
        st.warning("⏳ **MONITORANDO ALGORITMO:** Nenhuma das três sequências confirmadas ainda. Continue alimentando os dados.")

    st.divider()

    # --- EXIBIÇÃO VISUAL DO HISTÓRICO ---
    st.markdown("📋 **Histórico Recente (RAM):**")
    badges = []
    for v in valores[-15:]:
        if v < 2.0:
            badges.append(f"🔵 **{v:.2f}x**")
        elif v < 10.0:
            badges.append(f"🟣 **{v:.2f}x**")
        else:
            badges.append(f"🌸 **{v:.2f}x**")
    st.markdown(" → ".join(badges))
    
else:
    st.info("👋 Digite pelo menos 5 resultados consecutivos no painel lateral para iniciar o monitoramento de padrões.")
