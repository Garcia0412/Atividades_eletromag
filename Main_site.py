import streamlit as st
from pathlib import Path
from T1_EM_LUCAS_VINICIUS import main
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
    ["O projeto", "Falha no dielétrico", "Capacitância"]
)

#RENDERIZAÇÃO DAS ABAS
if secao == "O projeto":
    gerar_gráficos() # Gera os gráficos em cache uma vez que o aplicativo é aberto, como não haverá mudança de parametros, a função não vai ser executada novamente quando o usuário interagir com a interface
    st.title("Modelagem em eletromagnetismo") # Titulo da aba

    # Texto da Aba
    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Diariamente, no ambiente de engenharia, é extremamente comum nos deparamos com a necessidade de modelar e analizar objetos reais por meio de ferramentas computacionais como, por exemplo, o Python. 
                Por isso, como forma de expandir os conhecimentos e estabelecer uma relação de interdiciplinaridade, foi proposto aos estudantes de engenharia elétrica e engenharia de telecomunicações a elaboração e execução de trabalhos relacionando a modelagem computacional com conhecimentos em eletromagnetismo.</p>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Para tal, decidimos elaborar uma interface web que contenha os três trabalhos realizados em sob a geometria e propriedades de um dos objetos mais comuns e utilizados na engenharia, o cabo axial. </p>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("<p style='text-align: center;'>Imagem 1: Representação de um cabo coaxial</p>", unsafe_allow_html=True) # Titulo da imagem

    Col_A, Col_B, Col_C, Col_D, Col_E = st.columns(5) # Colunas pra centralizar a imagem 
    
    with Col_C: # Coluna central
        st.image(ASSETS / "Cabo_coaxial.jpg")

    st.markdown("<p style='text-align: center;'>FONTE: Eletrica Bichuette (2026)</p>", unsafe_allow_html=True) # Fonte da imagem

    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Esse tipo de cabo está presente em diversos contextos do dia a dia das pessoas, como nas televisões, aparelhos de internet e sistemas de segurança, devido a isso, é fundamental a um futuro engenheiro o estudo e análise de como essa estrutura funciona, e possíveis falhas que podem ocorrer durante seu funcionamento, podendo assim, trabalhar com soluções antecipadamente.</p>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("""<p style="text-indent: 50px; text-align: justify;">No painel lateral encontram-se as abas de navegação da interface, sendo trabalhado em cada uma um aspecto do cabo que um engenheiro deve se atentar na hora de criar o seu projeto. </p>""", unsafe_allow_html=True)

elif secao == "Falha no dielétrico":
    st.header("Estudo do dielétrico do cabo coaxial") # Titulo da aba

    # Texto da aba
    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Uma das maiores caracteristicas do cabo coaxial é a sua alta blindagem contra ondas eletromagnéticas do ambiente, contudo, com o passar dos anos e desgastes ocorridos por condições adversas o dielétrico desses cabos pode apresentar falhas e isso pode ocasionar problemas na sua aplicação. 
                Devido a isso, foi-se elaborado um progrma que utiliza os dados fornecidos pelo professor, mapeia e plota em forma de 4 gráficos os resultados do que seria um estudo em campo do teste da integridade do dielétrico de um cabo coaxial.</p> """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    Col1, Col2, = st.columns(2) # Cria colunas para poder colocar cada imagem lado a lado
    # Cada with define o que vai estar contido dentro de cada coluna 
    with Col1: 
        st.markdown("<p style='text-align: center;'>Imagem 1: Campo Vetorial da Densidade de Fluxo Elétrico (D)</p>", unsafe_allow_html=True) # Titulo da imagem
        st.image(GRAFICOS / "Campo Vetorial da Densidade de Fluxo Elétrico (D).png") # Mostra a imagem
        st.markdown("<p style='text-align: center;'>FONTE: Autoria própria (2026)</p>", unsafe_allow_html=True) # Fonte da imagem 
    with Col2:
        st.markdown("<p style='text-align: center;'>Imagem 2: Mapa de Calor - Divergente de D (Analítico)</p>", unsafe_allow_html=True)
        st.image(GRAFICOS / "Mapa de Calor - Divergente de D (Analítico).png")
        st.markdown("<p style='text-align: center;'>FONTE: Autoria própria (2026)</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    Col3, Col4 = st.columns(2)
    with Col3:
        st.markdown("<p style='text-align: center;'>Imagem 3: Mapa de Calor - Divergente de D (Numérico)</p>", unsafe_allow_html=True)
        st.image(GRAFICOS / "Mapa de Calor - Divergente de D (Numérico).png")
        st.markdown("<p style='text-align: center;'>FONTE: Autoria própria (2026)</p>", unsafe_allow_html=True)
    with Col4:
        st.markdown("<p style='text-align: center;'>Imagem 4: Mapa de Calor - Erro absoluto</p>", unsafe_allow_html=True)
        st.image(GRAFICOS / "Mapa de Calor - Erro absoluto.png")
        st.markdown("<p style='text-align: center;'>FONTE: Autoria própria (2026)</p>", unsafe_allow_html=True)

elif secao == "Capacitância":
    st.header("Estudo da capacitância do cabo coaxial") # Titulo da aba
    # Texto da aba
    st.markdown("""<p style="text-indent: 50px; text-align: justify;"> </p>""", unsafe_allow_html=True)
