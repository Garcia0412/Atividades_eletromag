import streamlit as st
from pathlib import Path
from T1_EM_LUCAS_VINICIUS import main
from T2_EM_LUCAS_VINICIUS import main
from Header import Header

#CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="App",
    layout="wide" 
)

#FUNÇÃO EM CACHE PARA EVITAR RODAR NOVAMENTE QUANDO A PAGINA RECARREGAR
@st.cache_data
def gerar_gráficos():
    main()

Header() # Gera o cabeçalho

#PATH PARA LOCALIZAR ITENS PARA O CÓDIGO
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"
GRAFICOS = BASE_DIR / "Resultados_Graficos"

#MENU DE BARRA LATERAL
st.sidebar.title("Navegação")
secao = st.sidebar.selectbox(
    "Menu:",
    ["O projeto", "Capacitância"]
)

#RENDERIZAÇÃO DAS ABAS
if secao == "O projeto":
    gerar_gráficos() # Gera os gráficos em cache uma vez que o aplicativo é aberto, como não haverá mudança de parametros, a função não vai ser executada novamente quando o usuário interagir com a interface
    st.title("Modelagem em eletromagnetismo") # Titulo da aba

    # Texto da Aba
    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Diariamente, no ambiente de engenharia, é extremamente comum nos deparamos com a necessidade de modelar e analizar objetos reais por meio de ferramentas computacionais como, por exemplo, o Python. 
                Por isso, como forma de expandir os conhecimentos e estabelecer uma relação de interdiciplinaridade, foi proposto aos estudantes de engenharia elétrica e engenharia de telecomunicações a elaboração e execução de trabalhos relacionando a modelagem computacional com conhecimentos em eletromagnetismo.</p>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Para tal, decidimos elaborar uma interface web que contenha os resultados de um trabalho realizado sobre a geometria e as propriedades de um dos objetos mais comuns e utilizados na engenharia, o cabo axial. </p>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("<p style='text-align: center;'>Imagem 1: Representação de um cabo coaxial</p>", unsafe_allow_html=True) # Titulo da imagem

    Col_A, Col_B, Col_C, Col_D, Col_E = st.columns(5) # Colunas pra centralizar a imagem 
    
    with Col_C: # Coluna central
        st.image(ASSETS / "Cabo_coaxial.jpg")

    st.markdown("<p style='text-align: center;'>FONTE: Eletrica Bichuette (2026)</p>", unsafe_allow_html=True) # Fonte da imagem

    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Esse tipo de cabo está presente em diversos contextos do dia a dia das pessoas, como nas televisões, aparelhos de internet e sistemas de segurança, devido a isso, é fundamental a um futuro engenheiro o estudo e análise de como essa estrutura funciona, e possíveis falhas que podem ocorrer durante seu funcionamento, podendo assim, trabalhar com soluções antecipadamente.</p>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("""<p style="text-indent: 50px; text-align: justify;">No painel lateral encontram-se as abas de navegação da interface, sendo trabalhado a questão da existência de um efeito capacitivo defeituoso na estrutura do cabo abordando diretamente uma questão que um engenheiro deve se atentar na hora de criar o seu projeto. </p>""", unsafe_allow_html=True)


elif secao == "Capacitância":
    st.header("Estudo da capacitância do cabo coaxial") # Titulo da aba
    # Texto da aba
    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Ainda nos estudos sobre cabos coaxiais, desta vez o foco foi nos efeitos capacitivos dos cabos, quando submetidos ao desgaste do tempo ou de condições adversas de uso.
                As imagens abaixo são os resultados das modelagens da situação problema apresentada pelo professor.</p>""", unsafe_allow_html=True)
    
    Colu1, Colu2, = st.columns(2) # Cria colunas para poder colocar cada imagem lado a lado
    # Cada with define o que vai estar contido dentro de cada coluna 
    with Colu1: 
        st.markdown("<p style='text-align: center;'>Imagem 1: Distribuição Vetorial do Campo D</p>", unsafe_allow_html=True) # Titulo da imagem
        st.image(GRAFICOS / "Distribuição Vetorial do Campo D.png") # Mostra a imagem
        st.markdown("<p style='text-align: center;'>FONTE: Autoria própria (2026)</p>", unsafe_allow_html=True) # Fonte da imagem 
    with Colu2:
        st.markdown("<p style='text-align: center;'>Imagem 2: Validação da Densidade de Carga Superficial na Interface</p>", unsafe_allow_html=True)
        st.image(GRAFICOS / "Validação da Densidade de Carga Superficial na Interface.png")
        st.markdown("<p style='text-align: center;'>FONTE: Autoria própria (2026)</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    Colu3, Colu4 = st.columns(2)
    with Colu3:
        st.markdown("<p style='text-align: center;'>Imagem 3: Continuidade da Componente Tangencial</p>", unsafe_allow_html=True)
        st.image(GRAFICOS / "Continuidade da Componente Tangencial.png")
        st.markdown("<p style='text-align: center;'>FONTE: Autoria própria (2026)</p>", unsafe_allow_html=True)
    with Colu4:
        st.markdown("<p style='text-align: center;'>Imagem 4: Mapa de Calor - Erro absoluto</p>", unsafe_allow_html=True)
        st.image(GRAFICOS / "Mapa de Calor - Erro absoluto_2.png")
        st.markdown("<p style='text-align: center;'>FONTE: Autoria própria (2026)</p>", unsafe_allow_html=True)