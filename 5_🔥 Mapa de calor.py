import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Carregar os dados
@st.cache_data
def load_data():
    data = pd.read_csv("C:/Users/asus/Desktop/ETEC/Nova pasta/TCC/Pages/Produtos.csv", sep=";", encoding="latin1")
    
    # Converter Latitude e Longitude para numérico
    data["Latitude"] = pd.to_numeric(data["Latitude"].str.replace(",", "."), errors="coerce")
    data["Longitude"] = pd.to_numeric(data["Longitude"].str.replace(",", "."), errors="coerce")
    
    # Remover valores inválidos
    data = data.dropna(subset=["Latitude", "Longitude"])
    return data

# Criar mapa interativo com camada de calor
def create_heatmap_with_layer(data, produto, cidades):
    # Filtrar os dados com base no produto e nas cidades selecionadas
    filtered_data = data[(data["Produto"] == produto) & (data["Cidade"].isin(cidades))]
    
    # Calcular desempenho relativo
    max_venda = filtered_data["Venda Qtd"].max()
    def define_color(venda):
        if venda > 0.8 * max_venda:
            return "green"
        elif venda > 0.5 * max_venda:
            return "yellow"
        return "red"
    
    # Criar o mapa base
    m = folium.Map(location=[filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()], zoom_start=7)
    
    # Adicionar os mercados ao mapa
    for _, row in filtered_data.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=row["Venda Qtd"] / 1000,  # Escalar o tamanho pelo valor de vendas
            popup=(
                f"<b>Cidade:</b> {row['Cidade']}<br>"
                f"<b>Vendas:</b> {row['Venda Qtd']}<br>"
                f"<b>Produto:</b> {row['Produto']}"
            ),
            color=define_color(row["Venda Qtd"]),
            fill=True,
            fill_color=define_color(row["Venda Qtd"]),
            fill_opacity=0.7
        ).add_to(m)
    
    # Adicionar a camada de calor
    heat_data = [
        [row["Latitude"], row["Longitude"], row["Venda Qtd"]]
        for _, row in filtered_data.iterrows()
    ]
    HeatMap(heat_data, radius=50, blur=55, max_zoom=52).add_to(m)
    
    return m

# Streamlit App
st.title("Dashboard de Vendas de Mercados")
st.write("Visualize as vendas geolocalizadas por produto e região.")

# Carregar os dados
data = load_data()

# Filtros de seleção
produto_selecionado = st.selectbox("Escolha um Produto", options=data["Produto"].unique())
cidades_selecionadas = st.multiselect("Escolha as Cidades", options=data["Cidade"].unique())





# Gerar visualização somente após seleção
if produto_selecionado and cidades_selecionadas:
    st.subheader("Mapa de Vendas Geolocalizadas com Calor")
    heatmap = create_heatmap_with_layer(data, produto_selecionado, cidades_selecionadas)
    st_folium(heatmap, width=700, height=500)
else:
    st.write("Por favor, selecione um produto e pelo menos uma cidade para visualizar o mapa.")
