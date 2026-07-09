import streamlit as st
import pandas as pd
import plotly.express as px
from collections import deque

# Configuração da página para o modo estendido (melhor visualização em tablets)
st.set_page_config(page_title="Radar Aviator Android", layout="wide")

# Inicializa a memória RAM do site para guardar até 100 rodadas
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=100)

historico = st.session_state.historico

# Títulos da Interface
st.title("📊 Painel Estatístico Aviator - Modo Manual")
st.write("Insira os resultados na barra lateral para calcular as porcentagens e tendências em tempo real.")

st.divider()

# --- PAINEL LATERAL DE CONTROLE ---
st.sidebar.markdown("### 📥 Entrada de Dados")
st.sidebar.write("Olhe o resultado que saiu na Betano e digite abaixo:")

# Caixa para digitar o número
novo_valor = st.sidebar.text_input("Digite a última vela (ex: 1.45 ou 3.20) e aperte Enter:", key="input_vela")

if novo_valor:
    try:
        # Converte o texto em número (aceita ponto ou vírgula)
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
    # Pega no máximo as últimas 20 rodadas gravadas para calcular a tendência recente
    ultimas_20 = list(historico)[-20:]
    greens_2x = sum(1 for v in ultimas_20 if v >= 2.0)
    porcentagem_atual = (greens_2x / len(ultimas_20)) * 100 if ultimas_20 else 0

    # Descobre quantos REDs (menor que 2x) saíram em sequência no final
    reds_seguidos = 0
    for v in reversed(list(historico)):
        if v < 2.0:
            reds_seguidos += 1
        else:
            break

    # --- SINAL DE ALERTA DINÂMICO ---
    st.markdown("### 🚨 Status do Sinal")
    if reds_seguidos >= 4 and porcentagem_atual < 40:
        st.error(f"🔥 **ALERTA DE ENTRADA DISPARADO!** \n\n Sequência perigosa de {reds_seguidos} REDS seguidos. Força recente de 2x+: {porcentagem_atual:.1f}%. Alta probabilidade matemática de correção. Entre buscando acima de 2.00x!")
    else:
        st.warning(f"⏳ **Aguardando padrão mínimo:** {reds_seguidos} reds seguidos. Força recente do mercado: {porcentagem_atual:.1f}%. Não entre agora.")

    st.divider()

    # --- QUADROS DE MÉTRICAS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Porcentagem Recente (Janela 20)", f"{porcentagem_atual:.1f}%")
    col2.metric("Sequência Atual de REDS", f"{reds_seguidos} seguidos")
    col3.metric("Total de Rodadas na RAM", len(historico))

    st.divider()

    # --- CONSTRUÇÃO DO GRÁFICO ---
    st.markdown("### 📈 Gráfico de Tendência da Porcentagem")
    if len(historico) >= 5:
        dados_grafico = []
        lista_velas = list(historico)
        tamanho_janela = min(10, len(lista_velas))
        
        # Cria a linha de média móvel para plotar
        for i in range(tamanho_janela, len(lista_velas) + 1):
            janela = lista_velas[i-tamanho_janela:i]
            pct = (sum(1 for v in janela if v >= 2.0) / tamanho_janela) * 100
            dados_grafico.append({"Rodada": i, "Porcentagem_2x": pct})

        df = pd.DataFrame(dados_grafico)
        fig = px.line(df, x="Rodada", y="Porcentagem_2x", title="Evolução da Força do Mercado", markers=True)
        
        # Linhas de meta no gráfico
        fig.add_hline(y=40, line_dash="dash", line_color="green", annotation_text="ZONA DE ENTRADA (Mercado pagou pouco)")
        fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="ZONA DE PERIGO (Mercado pagou muito)")
        fig.update_yaxes(range=[0, 101])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insira pelo menos 5 rodadas para o gráfico começar a desenhar a linha de tendência.")
        
    st.markdown("📋 **Últimos valores salvos na RAM:** " + str(list(historico)[-10:])[1:-1] + "x")
else:
    st.info("👋 Olá! Abra o Aviator na Betano em outra aba ou divida a tela do seu tablet. Conforme as rodadas forem acontecendo, digite os valores na barra lateral e aperte Enter para ativar este painel.")
