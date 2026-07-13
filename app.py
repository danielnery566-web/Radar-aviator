import streamlit as st
import pandas as pd
from collections import deque

# Configuração da página para o modo estendido (melhor para tablets)
st.set_page_config(page_title="Radar Premium Aviator", layout="wide")

# Inicializa a memória RAM do site para guardar até 100 rodadas
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=100)

historico = st.session_state.historico

# Títulos da Interface
st.title("🎯 Radar Pro - Foco em 2.00x & Probabilidade Rosa")
st.write("Prioridade máxima em lucros seguros com termômetro para alvos longos.")

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

    # 3. Mapeamento de bloco curto (Últimas 6 rodadas)
    ultimas_6 = list(historico)[-6:]
    reds_na_janela = sum(1 for v in ultimas_6 if v < 2.0)

    # 4. Cálculo da Seca para Vela Rosa (>= 10.0x)
    rodadas_sem_rosa = 0
    for v in reversed(list(historico)):
        if v < 10.0:
            rodadas_sem_rosa += 1
        else:
            break

    # 5. Cálculo Dinâmico da Porcentagem de Chance da Vela Rosa
    if rodadas_sem_rosa <= 15:
        chance_rosa = 10.0 + (rodadas_sem_rosa * 2)  # Entre 10% e 40%
    elif rodadas_sem_rosa <= 30:
        chance_rosa = 40.0 + (rodadas_sem_rosa - 15) * 2.5  # Entre 40% e 77.5%
    else:
        # Acima de 30 rodadas sem vir nada alto, a probabilidade dispara rumo ao limite matemático
        chance_rosa = min(95.0, 77.5 + (rodadas_sem_rosa - 30) * 1.5)

    # --- SINAL 1: PRIORIDADE MÁXIMA (ALVO 2.00x) ---
    st.markdown("### 🟢 PRIORIDADE: Sinalizador Alvo 2.00x (Lucro Seguro)")
    
    if (reds_seguidos >= 3) or (reds_na_janela >= 4 and len(historico) >= 6):
        if porcentagem_atual <= 45.0:
            st.error(
                f"🔥 **SINAL CONFIRMADO PARA 2.00x!** \n\n"
                f"Saturação de mercado detectada: **{reds_seguidos} REDs seguidos**. Força recente: **{porcentagem_atual:.1f}%**.\n\n"
                f"🎯 **AÇÃO:** Faça sua entrada com o Auto-Saque programado em **exatamente 2.00x**."
            )
        else:
            st.warning("⏳ **Filtro Ativado:** A sequência de REDs bateu, mas a força geral do jogo ainda está alta ({porcentagem_atual:.1f}%). Aguarde esfriar mais um pouco para evitar falsos sinais.")
    else:
        st.warning(f"⏳ **Monitorando Padrão de 2x...** (Reds atuais: {reds_seguidos} | Concentração curta: {reds_na_janela}/6)")

    st.divider()

    # --- SINAL 2: TERMÔMETRO DE VELA ROSA (20.00x+) ---
    st.markdown("### 🌸 Radar de Probabilidade: Vela Rosa (20x+)")
    
    # Exibe a porcentagem em um formato visual de progresso
    st.write(f"📊 **Cálculo de Tendência Atual:** {chance_rosa:.1f}% de probabilidade de liberação de vela alta.")
    st.progress(int(chance_rosa) / 100)

    if chance_rosa >= 80.0:
        st.info(
            f"🚀 **ALERTA DE ALTA PROBABILIDADE ({chance_rosa:.1f}%)** \n\n"
            f"O jogo acumulou **{rodadas_sem_rosa} rodadas de seca** absoluta de velas altas.\n\n"
            f"🎯 **AÇÃO SECUNDÁRIA:** Quando você for fazer a entrada do sinal de 2x (acima), coloque uma moeda mínima na 'Aposta 2' da Betano e tente arrastar ela até **20.00x**!"
        )
    else:
        st.success(f"⏳ **Estatística da Rosa:** Algoritmo em fase de acumulação de banca. Rodadas desde a última vela alta: {rodadas_sem_rosa}. Aguarde o termômetro passar de 80%.")

    st.divider()

    # --- QUADROS DE INFORMAÇÃO RÁPIDA ---
    st.markdown("### 📊 Estatísticas Gerais")
    col1, col2, col3 = st.columns(3)
    col1.metric("Termômetro do Jogo (Força)", f"{porcentagem_atual:.1f}%")
    col2.metric("Reds em Sequência", f"{reds_seguidos}")
    col3.metric("Rodadas sem Vela Alta", f"{rodadas_sem_rosa}")

    st.divider()
    
    # Exibe a lista dos últimos valores digitados para conferência
    st.markdown("📋 **Histórico na Memória RAM:**")
    st.text(str(list(historico)[-12:])[1:-1] + "x")
    
else:
    st.info("👋 Painel Inteligente Pronto! Alimente a barra lateral com os números da Betano e veja o termômetro da vela rosa subir em tempo real.")
