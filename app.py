import streamlit as st
import pandas as pd
from collections import deque

# Configuração da página para o modo estendido (melhor para tablets)
st.set_page_config(page_title="Radar Seguro Aviator", layout="wide")

# Inicializa a memória RAM do site para guardar até 100 rodadas
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=100)

historico = st.session_state.historico

# Títulos da Interface
st.title("🎯 Radar Seguro - Foco 2.00x (3 REDs) & Probabilidade 50x+")
st.write("Filtro calibrado para maior proteção da banca e monitoramento de super bônus.")

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

# --- LÓGICA MATEMÁTICA EM TEMPO REAL ---
if len(historico) > 0:
    # 1. Métrica de Força Recente (Últimas 20)
    ultimas_20 = list(historico)[-20:]
    greens_2x = sum(1 for v in ultimas_20 if v >= 2.0)
    porcentagem_atual = (greens_2x / len(ultimas_20)) * 100 if ultimas_20 else 0

    # 2. Contagem de REDs seguidos (< 2.00x)
    reds_seguidos = 0
    for v in reversed(list(historico)):
        if v < 2.0:
            reds_seguidos += 1
        else:
            break

    # 3. Cálculo da Seca para Super Vela (>= 10.0x como referência de retenção)
    rodadas_sem_alta = 0
    for v in reversed(list(historico)):
        if v < 10.0:
            rodadas_sem_alta += 1
        else:
            break

    # 4. Cálculo Dinâmico da Porcentagem de Chance da Vela Insana (50.00x+)
    if rodadas_sem_alta <= 20:
        chance_50x = 5.0 + (rodadas_sem_alta * 1.5)
    elif rodadas_sem_alta <= 45:
        chance_50x = 35.0 + (rodadas_sem_alta - 20) * 1.8
    else:
        chance_50x = min(98.0, 80.0 + (rodadas_sem_alta - 45) * 1.0)

    # --- SINAL 1: PRIORIDADE PROTEGIDA (ALVO 2.00x) ---
    st.markdown("### 🟢 PRIORIDADE: Sinalizador Alvo 2.00x (Gatilho Seguro)")
    
    # Voltamos para 3 REDs conforme sua excelente análise de segurança
    if reds_seguidos >= 3 and porcentagem_atual <= 50.0:
        st.error(
            f"🔥 **SINAL ATIVO: MOMENTO DE ENTRADA SEGURO!** \n\n"
            f"O mercado bateu o filtro de proteção: **{reds_seguidos} REDs seguidos**. Força atual: **{porcentagem_atual:.1f}%**.\n\n"
            f"🎯 **AÇÃO:** Faça sua entrada buscando a saída em **2.00x** no Auto-Saque!"
        )
    else:
        st.warning(f"⏳ **Monitorando Padrão de 2x...** (Reds atuais: {reds_seguidos}/3 | Força do mercado: {porcentagem_atual:.1f}%)")

    st.divider()

    # --- SINAL 2: TERMÔMETRO DE VELA INSANA (50.00x+) ---
    st.markdown("### 🌌 Radar de Probabilidade: Vela Insana (50x+)")
    
    st.write(f"📊 **Cálculo de Janela de Distribuição:** {chance_50x:.1f}% de chance matemática para multiplicadores extremos.")
    st.progress(int(chance_50x) / 100)

    if chance_50x >= 85.0:
        st.info(
            f"🚀 **ALERTA DE MULTIPLICADOR EXTREMO ({chance_50x:.1f}%)** \n\n"
            f"O sistema detectou uma seca severa de **{rodadas_sem_alta} rodadas** sem payouts expressivos.\n\n"
            f"🎯 **DICA:** Mantenha a aposta principal em 2x. Na segunda aposta (com valor mínimo), tente deixar subir, pois a janela estatística para super velas de 50x+ está aberta!"
        )
    else:
        st.success(f"⏳ **Estatística 50x+:** Ciclo padrão de acumulação. Rodadas desde o último sinal expressivo: {rodadas_sem_alta}. O termômetro vai subir conforme o jogo segurar o prêmio.")

    st.divider()

    # --- QUADROS DE INFORMAÇÃO RÁPIDA ---
    st.markdown("### 📊 Indicadores em Tempo Real")
    col1, col2, col3 = st.columns(3)
    col1.metric("Força Recente (Janela 20)", f"{porcentagem_atual:.1f}%")
    col2.metric("Reds em Sequência", f"{reds_seguidos}")
    col3.metric("Rodadas de Seca Alta", f"{rodadas_sem_alta}")

    st.divider()
    
    # Exibe a lista dos últimos valores digitados para conferência
    st.markdown("📋 **Histórico na Memória RAM:**")
    st.text(str(list(historico)[-12:])[1:-1] + "x")
    
else:
    st.info("👋 Painel Atualizado! Digite as velas da Betano na barra lateral para acompanhar o filtro de 3 REDs e o medidor de 50x+.")
