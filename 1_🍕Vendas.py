import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração inicial do Streamlit
st.set_page_config(page_title="TCC - Etecvav, Desenvolvimento de Sistemas 3M", 
                   page_icon="🇧🇷", 
                   layout="wide")

st.title("Gráfico de colunas 📊")

# Função para carregar os dados do arquivo CSV
@st.cache_data
def carregar_dados_csv(csv_file):
    try:
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Upload de arquivo CSV
base_vendas = st.file_uploader("Carregar arquivo CSV", type=["csv"])

if base_vendas:
    df = carregar_dados_csv(base_vendas)
    if df is not None:
        st.success("Arquivo CSV carregado com sucesso!")
        
        st.subheader("Pré-visualização dos Dados")
        st.dataframe(df.head(), use_container_width=True)

        # Converter 'Venda total' para numérico se necessário
        if df['Venda total'].dtype != 'float64' and df['Venda total'].dtype != 'int64':
            df['Venda total'] = pd.to_numeric(df['Venda total'], errors='coerce')

        # Seletor de categorias (multiseleção)
        categorias = df['Categoria'].unique()
        categorias_selecionadas = st.multiselect('Selecione as categorias:', categorias)

        # Seletor de coluna para comparação
        colunas_para_comparacao = [col for col in ['Venda Qtd', 'Venda total'] if col in df.columns]
        coluna_selecionada = st.multiselect('Selecione as colunas para comparação:', colunas_para_comparacao)

        # Filtrar dados pelas categorias selecionadas
        if categorias_selecionadas:
            produtos_filtrados = df[df['Categoria'].isin(categorias_selecionadas)]

            if not produtos_filtrados.empty and coluna_selecionada:
                # Agregar os dados
                comparacao = produtos_filtrados.groupby('Categoria')[coluna_selecionada].sum().reset_index()
                st.subheader("Resultados da Comparação")
                st.dataframe(comparacao, use_container_width=True)

                # Verificar soma total após a agregação
                st.write("Soma total de `Venda Qtd` após a agregação: ", comparacao['Venda Qtd'].sum())
                st.write("Soma total de `Venda total` após a agregação: ", comparacao['Venda total'].sum())

                # Exibir gráficos para cada coluna selecionada
                for coluna in coluna_selecionada:
                    st.subheader(f"Gráfico de {coluna} por Categoria")

                    # Criando o gráfico com matplotlib para adicionar valores nas barras
                    fig, ax = plt.subplots(figsize=(10, 8))
                    bars = ax.bar(comparacao['Categoria'], comparacao[coluna], color='lightsalmon')

                    # Adicionar valores nas barras
                    for bar in bars:
                        yval = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width() / 2, yval + 5, round(yval, 2), ha='center', va='bottom')

                    # Títulos e rótulos
                    ax.set_title(f"Gráfico de {coluna} por Categoria")
                    ax.set_xlabel('Categoria')
                    ax.set_ylabel(coluna)

                    # Exibir o gráfico
                    st.pyplot(fig)

            elif produtos_filtrados.empty:
                st.warning("Nenhum produto encontrado para as categorias selecionadas.")
            elif not coluna_selecionada:
                st.warning("Selecione pelo menos uma coluna para exibir os dados.")
        else:
            st.info("Selecione ao menos uma categoria para continuar.")
    else:
        st.error("Falha ao carregar o arquivo CSV.")
else:
    st.info("Aguardando o upload de um arquivo CSV.")
