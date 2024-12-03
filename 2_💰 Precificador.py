import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Título da aplicação
st.markdown("<h1 style='font-size: 30px;'>Machine Learning aplicado à precificação 🎲</h1>", unsafe_allow_html=True)

# Carregar os dados do arquivo CSV
dados = st.file_uploader("Carregar arquivo CSV", type=["csv"])
if dados:
    try:
        # Lendo o CSV com suporte a separador decimal como vírgula
        df = pd.read_csv(dados, decimal=",")
        
        if 'Produto' in df.columns and 'Preco Venda' in df.columns and 'Venda Qtd' in df.columns:
            # Garantir que as colunas numéricas estejam no formato correto
            df['Preco Venda'] = pd.to_numeric(df['Preco Venda'], errors='coerce')
            df['Venda Qtd'] = pd.to_numeric(df['Venda Qtd'], errors='coerce')

            

            if df[['Preco Venda', 'Venda Qtd']].isnull().any().any():
                st.error("Alguns valores nas colunas 'Preco Venda' ou 'Venda Qtd' não puderam ser convertidos. Verifique o arquivo.")
                st.stop()

            st.success("Arquivo CSV carregado com sucesso!")
            st.subheader("Produtos carregados:")
            st.dataframe(df)
        else:
            st.error("O arquivo deve conter as colunas: 'Produto', 'Preco Venda' e 'Venda Qtd'.")
            st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        st.stop()
else:
    st.info("Por favor, carregue um arquivo CSV para começar.")
    st.stop()

# Entrada para filtrar o produto
st.markdown("<h3 style='font-size: 20px;'>Seleção de Produto</h3>", unsafe_allow_html=True)
produto = st.selectbox("Selecione o produto:", df['Produto'].unique())

# Filtrar os dados pelo produto escolhido
dados_filtrados = df[df['Produto'] == produto]

if dados_filtrados.empty:
    st.warning("Nenhum dado encontrado para o produto selecionado.")
    st.stop()

# Definir as variáveis independentes (X) e dependentes (Y)
X = dados_filtrados[['Venda Qtd']]  # Quantidade vendida
Y = dados_filtrados['Preco Venda']   # Preço de venda

# Garantir que existam dados suficientes
if len(dados_filtrados) < 2:
    st.error("Dados insuficientes para gerar a regressão. Por favor, escolha outro produto ou carregue mais dados.")
    st.stop()

# Criar o modelo de regressão linear
modelo = LinearRegression().fit(X, Y)

# Gráfico de dispersão com linha de regressão
st.markdown("<h3 style='font-size: 20px;'>Análise do Produto</h3>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(X, Y, color='blue', label='Dados observados')
ax.plot(X, modelo.predict(X), color='red', label='Linha de Regressão')
ax.set_title(f"Regressão Linear para o Produto: {produto}")
ax.set_xlabel("Venda Qtd")
ax.set_ylabel("Preco Venda")
ax.legend()
st.pyplot(fig)

# Entrada para prever o preço com base na quantidade
st.markdown("<h3 style='font-size: 20px;'>Previsão de Preço</h3>", unsafe_allow_html=True)
qtd_desejada = st.number_input("Insira a quantidade que deseja vender:", min_value=1, step=1, value=10)

# Botão para processar
processar = st.button("Calcular Preço de Venda")
#st.toast(f"Total clicks:{produto['Preco Venda'].sum()}")
if processar:
    try:
        nova_entrada = pd.DataFrame([[qtd_desejada]], columns=['Venda Qtd'])
        preco_previsto = modelo.predict(nova_entrada)
        st.header(f"Preço sugerido de venda: R$ {preco_previsto[0]:.2f}")
    except Exception as e:
        st.error(f"Erro ao calcular o preço: {e}")
