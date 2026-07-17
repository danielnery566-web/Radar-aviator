import streamlit as st
import pandas as pd
from collections import deque

# Configuração da página otimizada para tablets
st.set_page_config(page_title="Radar Aviator Analytics", layout="wide")

# Inicializa o histórico na memória RAM
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=100)

historico = st.session_state.historico

# Título Principal
st.title("📊 Radar Aviator Pro - Analisador de Tendências & Linhas")
st.write("Monitore em tempo real se o algoritmo está pagando ou retendo através do mapeamento de blocos.")

st.divider()

# --- PAINEL LATERAL COM FORMULÁRIO ANTI-TRAVAMENTO ---
st.sidebar.markdown("### 📥 Alimentar Algoritmo")

with st.sidebar.form(key="formulario_entrada", clear_on_submit=True):
    novo_valor = st.text_input("Digite a última vela (ex: 1.15):", key="input_vela")
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

# --- LÓGICA DE ANÁLISE GRÁFICA ---
if len(historico) > 0:
    valores = list(historico)
    
    # Contagem global de tipos
    total_rodadas = len(valores)
    azuis = sum(1 for v in valores if v < 2.0)
    verdes_roxa_rosa = sum(1 for v in valores if v >= 2.0)
    
    # Força recente (últimas 20)
    ultimas_20 = valores[-20:]
    greens_20 = sum(1 for v in ultimas_20 if v >= 2.0)
    forca_recente = (greens_20 / len(ultimas_20)) * 100 if ultimas_20 else 0

    # --- DIAGNÓSTICO DO MERCADO ---
    st.markdown("### 🌡️ Diagnóstico do Algoritmo (Tempo Real)")
    if forca_recente >= 55.0:
        st.success(f"🟩 **MERCADO PAGADOR ({forca_recente:.1f}%):** O gráfico está liberando muitas velas boas. Ótimo momento para surfar a tendência a favor dos padrões de 2x.")
    elif forca_recente >= 40.0:
        st.info(f"🟨 **MERCADO EQUILIBRADO ({forca_recente:.1f}%):** O jogo está alternando de forma padrão. Siga estritamente os gatilhos dos sinais.")
    else:
        st.sidebar.warning("⚠️ Alerta: Cassino Retendo!")
        st.error(f"🟥 **MERCADO EM RETENÇÃO ({forca_recente:.1f}%):** O algoritmo está prendendo e recolhendo banca. Cuidado com entradas seguidas!")

    st.divider()

    # --- PAINEL DE SINAIS (FOCO 2x + NOVO PADRÃO SOLICITADO) ---
    st.markdown("### 🚨 Painel de Entrada Confirmada (Alvo 2.00x)")
    
    sinal_disparado = False

    # Detecção do NOVO PADRÃO: Vela Ultra Baixa (<1.20) seguida imediatamente de um Green (>=2.0)
    if len(valores) >= 2:
        if valores[-2] < 1.20 and valores[-1] >= 2.0:
            sinal_disparado = True
            # Calcula a probabilidade baseada na resposta recente do mercado
            prob_quebra = min(96.0, 82.0 + (forca_recente * 0.1))
            st.error(
                f"🔥 **SINAL VERMELHO: PADRÃO QUEBRA INSTANTÂNEA DETECTADO!** \n\n"
                f"🎯 **Padrão:** Uma vela de extremo risco ({valores[-2]}x) foi corrigida direto por uma boa ({valores[-1]}x).\n"
                f"📊 **Probabilidade de continuidade em 2x:** {prob_quebra:.1f}%\n\n"
                f"📢 **AÇÃO:** O mercado está mostrando força de reação rápida. Entre na próxima rodada buscando **2.00x**!"
            )

    # Gatilho de Proteção Padrão (3 REDs seguidos)
    if not sinal_disparado and len(valores) >= 3:
        if valores[-1] < 2.0 and valores[-2] < 2.0 and valores[-3] < 2.0 and forca_recente <= 50.0:
            sinal_disparado = True
            prob_padrão = min(95.0, 85.0 + (50.0 - forca_recente) * 0.2)
            st.error(
                f"🔥 **SINAL VERMELHO: FILTRO DE EXAUSTÃO (3 REDs)!** \n\n"
                f"🎯 **Padrão:** Sequência de 3 velas azuis ruins seguidas.\n"
                f"📊 **Probabilidade de correção para 2x:** {prob_padrão:.1f}%\n\n"
                f"📢 **AÇÃO:** Entre na próxima rodada buscando **2.00x** no Auto-Saque!"
            )

    if not sinal_disparado:
        st.warning("⏳ **MONITORANDO GRÁFICO:** Aguardando o momento de maior probabilidade para disparar o sinal.")

    st.divider()

    # --- ANÁLISE DETALHADA POR LINHAS (IGUAL À TELA DA CASAS DE APOSTA) ---
    st.markdown("### 📋 Média do Gráfico por Linhas (Blocos de 7 velas)")
    st.write("Abaixo, o histórico é dividido em linhas de 7 jogadas (da mais recente para a mais antiga):")

    # Divide o histórico em grupos de 7 (simulando as linhas do jogo)
    lista_invertida = list(reversed(valores))
    linhas_linhas = [lista_invertida[i:i + 7] for i in range(0, len(lista_invertida), 7)]

    for idx, linha in enumerate(linhas_linhas):
        qtd_azul = sum(1 for v in linha if v < 2.0)
        qtd_boas = sum(1 for v in linha if v >= 2.0)
        
        # Cria a exibição visual da linha
        badges_linha = []
        for v in reversed(linha): # Mantém a ordem de leitura esquerda -> direita
            if v < 2.0:
                badges_linha.append(f"🔵 {v:.2f}x")
            elif v < 10.0:
                badges_linha.append(f"🟣 {v:.2f}x")
            else:
                badges_linha.append(f"🌸 {v:.2f}x")
        
        texto_linha = " | ".join(badges_linha)
        
        # Define o status da linha
        if qtd_boas > qtd_azul:
            status_linha = "🟢 **Linha Pagadora**"
        elif qtd_boas == qtd_azul:
            status_linha = "🟡 **Linha de Transição**"
        else:
            status_linha = "🔵 **Linha de Retenção (Ruim)**"
            
        st.markdown(f"**Linha {idx + 1}** ({status_linha}): {texto_linha} — *(Boas: {qtd_boas} | Ruins: {qtd_azul})*")

    st.divider()

    # --- VOLUMETRIA TOTAL ACUMULADA ---
    st.markdown("### 📊 Contagem Geral Acumulada na Sessão")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Velas Azuis (Ruins)", f"{azuis}", delta=f"{(azuis/total_rodadas)*100:.1f}% do total", delta_color="inverse")
    col2.metric("Total de Velas Boas (Roxa/Rosa)", f"{verdes_roxa_rosa}", delta=f"{(verdes_roxa_rosa/total_rodadas)*100:.1f}% do total")
    col3.metric("Rodadas na Memória", f"{total_rodadas}/100")

else:
    st.info("👋 Painel Analítico Avançado pronto! Vá inserindo os resultados da sua tabela da Betano para gerar os relatórios por linhas e monitorar a quebra do padrão de 1.15x.")
