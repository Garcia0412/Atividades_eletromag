import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
#import plotly.express as px
from TRABALHO_1 import Malha_2D, Densidade, Divergencia_numerica, Divergência_analitica, plot_graficos

#CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Cabo coaxial com rompimento no dielétrico",
    layout="wide" 
)

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"
GRAFICOS = BASE_DIR / "Resultados_Graficos"

# 2. Menu de Navegação na Barra Lateral
st.sidebar.title("Navegação")
secao = st.sidebar.selectbox(
    "Ir para:",
    ["O projeto", "Modelo analizado", "Resultados Finais", "Conclusões"]
)

# 3. Lógica de renderização de cada seção
if secao == "O projeto":
    st.title("O cabo coaxial")
    st.markdown(""" Diariamente, no ambiente de engenharia, é extremamente comum nos deparamos com a configuração de um cabo coaxial, por isso, na disciplina de eletromagnetismo ele foi um dos casos estudados.
            Dessa maneira, como uma forma de validar e por em prática conhecimentos interdisciplinares de engenharia, foi proposto como uma atividade pelo professor a criação de um script que trabalhe uma
            situação  """)
    
    st.markdown("<p style='text-align: center;'>Imagem 1: Representação de um cabo coaxial</p>", unsafe_allow_html=True)
    Col_A, Col_B, Col_C, Col_D, Col_E = st.columns(5) # Colunas pra centralizar a imagem 
    
    with Col_C:
        st.image(ASSETS / "Cabo_coaxial.jpg")
    st.markdown("<p style='text-align: center;'>FONTE: Eletrica Bichuette</p>", unsafe_allow_html=True)



elif secao == "Análise Exploratória":
    st.header("Análise Exploratória dos Dados")
    # Aqui entrarão tabelas e filtros

elif secao == "Resultados Finais":
    st.header("Resultados Finais e Gráficos")
    st.markdown("Após a criação e execução do ")

elif secao == "Conclusões":
    st.header("Conclusões")
    st.success("O projeto demonstrou que...")