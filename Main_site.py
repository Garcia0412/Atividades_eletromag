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
    "Ir para:",
    ["O projeto", "Resultados Finais", "Conclusões"]
)

#RENDERIZAÇÃO DAS ABAS
if secao == "O projeto":
    gerar_gráficos() # Gera os gráficos em cache uma vez que o aplicativo é aberto, como não haverá mudança de parametros, a função não vai ser executada novamente quando o usuário interagir com a interface
    st.title("Modelagem em eletromagnetismo") # Titulo da aba

    # Texto da Aba
    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Diariamente, no ambiente de engenharia, é extremamente comum nos deparamos com a necessidade de modelar e analizar objetos reais por meio de ferramentas computacionais como, por exemplo, o Python. 
                Por isso, como forma de expandir os conhecimentos e estabelecer uma relação de interdiciplinaridade, foi proposto aos estudantes de engenharia elétrica e engenharia de telecomunicações uma atividade envolvendo a Primeira Lei de Mawxell, também conhecida como Lei de Gauss na forma diferencial, de maneira que ela seja aplicada na verificação de falhas em objetos encontrados em uma situação cotidiana.</p>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Para realizar tal atividade, decidimos pela opção do cabo coaxial com dielétrico rompido devido ao uso, e assim, prosseguimos com a atividade seguindo os passos a passos indicados no roteiro, partindo da elaboração do código que permite calcular o divergente utilizando diferenças centradas e unilaterais e finalizando em uma interface web que usamos para apresentar os resultados obtidos. Abaixo segue uma ilustração de um cabo coaxial com blindagem</p>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("<p style='text-align: center;'>Imagem 1: Representação de um cabo coaxial</p>", unsafe_allow_html=True) # Titulo da imagem

    Col_A, Col_B, Col_C, Col_D, Col_E = st.columns(5) # Colunas pra centralizar a imagem 
    
    with Col_C: # Coluna central
        st.image(ASSETS / "Cabo_coaxial.jpg")

    st.markdown("<p style='text-align: center;'>FONTE: Eletrica Bichuette (2026)</p>", unsafe_allow_html=True) # Fonte da imagem

    st.markdown("<br>", unsafe_allow_html=True) # Usado para gerar espaço entre os textos

    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Nas proximas abas de navegação contidas na side bar apresentaremos os gráficos obtidos e as conclusões que obtivemos após a realização dessa simulação.</p>""", unsafe_allow_html=True)

elif secao == "Resultados Finais":
    st.header("Resultados Gráficos") # Titulo da aba

    # Texto da aba
    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Após a criação e execução do código, os resultados da modelagem foram agrupados em gráficos, sendo divididos em 2 tipos, campos vetoriais e mapas de calor, conforme solicitado em roteiro.
                O primeiro deles é o de campos vetoriais sob o isolante de revestimento do cabo. O segundo e o terceiro estão os dados obtidos por meio dos calculos dos divergentes, sendo o primeiro analiticamente e o segundo numericamente. Por fim, o ultimo deles representa o erro entre os dois calculos de divergente.
                A seguir estão os gráficos descritos acima. </p> """, unsafe_allow_html=True)
    
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

elif secao == "Conclusões":
    st.header("Conclusões") # Titulo da aba
    # Texto da aba
    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Por fim, concluimos que, fisicamente, a simulação representa a região do dielétrico de um cabo coaxial, localizada entre o raio interno de 0.01 metros e o raio externo de 0.03 metros. A lei de Gauss na forma diferencial estabelece que o divergente da densidade de fluxo elétrico é igual à densidade volumétrica de carga. Em um cabo coaxial ideal e sem defeitos, não há cargas livres na região isolante, logo, a densidade de carga deveria ser zero em toda essa área. No entanto, as imagens revelam uma anomalia localizada exatamente nas coordenadas x igual a 0.018 e y igual a zero. Fisicamente, essa anomalia representa uma impureza, um defeito pontual no dielétrico ou uma carga espúria aprisionada, atuando como uma fonte pontual secundária de campo elétrico dentro do material isolante.</p>""", unsafe_allow_html=True)
    st.markdown("""<p style="text-indent: 50px; text-align: justify;">Atingindo dessa forma, exatamente o que se pretendia com a simulação dessa superfície de dielétrico, a comprovação de que existia um defeito sob a superfície do dielétrico que permitia um acúmulo irregular de cargas em sua superfície, e assim comprovando a eficiência dos conhecimentos aprendidos em sala de aula no dia a dia de um engenheiro eletricista ou engenheiro eletrônico.</p>""", unsafe_allow_html=True)