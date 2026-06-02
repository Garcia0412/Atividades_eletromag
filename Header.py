import streamlit as st
from pathlib import Path

def Header():
    #PATH PARA LOCALIZAR ITENS PARA O CÓDIGO
    BASE_DIR = Path(__file__).resolve().parent
    ASSETS = BASE_DIR / "assets"

    #COLUNAS COM PROPORÇÃO
    col_esq, col_meio, col_dir = st.columns([1, 4, 1])

    #IMAGEM ESQUERDA
    with col_esq:
        st.image(ASSETS/"logo_ufu_45.png", use_container_width=True)

    #CENTRO
    with col_meio:
        None

    #IMAGEM DIREITA
    with col_dir:
        st.image(ASSETS/"logo_feelt.png", use_container_width=True)

    #DIVIDE O CABEÇALHO DO RESTO DA PÁGINA
    st.divider()
