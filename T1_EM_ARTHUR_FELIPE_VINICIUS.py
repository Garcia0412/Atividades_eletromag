"""
==========================================================================
DISCIPLINA : FEELT31405 - Eletromagnetismo (2026-2)
TRABALHO   : Sonda Capacitiva de Nivel no Conservador de um Transformador
DATA       : 03/11/2026
ALUNOS     : Arthur de Freitas Silva ........... Matricula: 12511EEL017
             Felipe Eduardo Oliveira Carvalho .. Matricula: 12421EEL013	
             Vinicius Lima Garcia .............. Matricula: 12421EEL009
             
==========================================================================
"""

import os # Para os Path dos gráficos gerados
import numpy as np # Para os calculos matemáticos

# Para a plotagem dos gráficos
import matplotlib 
matplotlib.use("Agg")  # Salva PNG e nao bloqueia a execucao
import matplotlib.pyplot as plt


# CONSTANTES (parametros do trabalho)

E0 = 8.854e-12             # permissividade do vacuo [F/m]
H = 0.80                   # comprimento util da sonda [m]
R_HASTE = 5.0e-3           # raio da haste (diametro 10,0 mm) [m]
R_TUBO = 15.0e-3           # raio interno do tubo (diametro 30,0 mm) [m]
ESP_INI = 0.50e-3          # espessura inicial da capa [m]
ER_AR = 1.0                # permissividades relativas
ER_OLEO = 2.2
ER_AGUA = 80.0
ER_PTFE = 2.1
C_FUNDO_ESCALA = 150e-12   # fundo de escala da eletronica [F]
RESOLUCAO_C = 0.1e-12      # resolucao da eletronica [F]
R2_LIMITE_MM = 1.8         # R2: menor variacao de nivel detectavel [mm]
HW_PIOR_CASO = 0.10        # R1: 10 cm de agua decantada [m]
HW_MAX = 0.10              # maior espessura de agua no Passo 5(c) [m]
HW_1CM = 0.01              # 1 cm de agua [m]
N_PONTOS = 100             # pontos das curvas C(h) e erro(hw)

# Validacao Aula 08
R_VALID = [1.0e-3, 3.0e-3, 5.0e-3]
E_VALID = [2.1, 2.3]
C_REF_VALID = 74.6e-12     # [F/m]

# Leituras de campo e inspecao
LEITURAS_PF = [54.0, 68.5, 83.0]
H_VARETA = 0.45            # altura total medida com a vareta [m]
C_VARETA_PF = 85.5         # capacitancia registrada [pF]

# Materiais candidatos e varredura de espessura
NOMES_MATERIAIS = ["PTFE", "Poliimida", "Epóxi"]
E_CAPAS = [2.1, 3.4, 3.6]
ESPESSURAS = np.linspace(0.2e-3, 1.0e-3, 81)   # [m]

# Configuracao inicial
RAIOS_INI = [R_HASTE, R_HASTE + ESP_INI, R_TUBO]
E_CALIB = [ER_PTFE, ER_OLEO, ER_AR]            # [capa, oleo, ar]
E_AGUA = [ER_PTFE, ER_AGUA, ER_OLEO, ER_AR]    # [capa, agua, oleo, ar]

# Graficos
HW_TESTE_G4 = [0.0, 0.01, 0.05]                # [m]
PASTA = os.path.dirname(os.path.abspath(__file__))


# FUNCOES DO MODELO

# 3(a)
def capacitancia_metro(r, e):
    """
    Capacitancia por unidade de comprimento de camadas
    dieletricas coaxiais concentricas (camadas radiais em SERIE):

        C' = 2*pi*eps0 / sum_i [ ln(r_i / r_(i-1)) / er_i ]

    Parametros:
      r (lista): raios [r0, r1, ..., rn] em m  (len(r) = len(e) + 1).
      e (lista): permissividades relativas das n camadas.
    Retorna: capacitancia por metro [F/m].
    """
    denominador = 0
    for i in range(1, len(r)):
        denominador += (1 / e[i - 1]) * np.log(r[i] / r[i - 1])
    return 2 * np.pi * E0 / denominador

# 3(b)
def capacitancia_total(r, e, l):
    """
    Capacitancia total da sonda (trechos em PARALELO).

    Parametros:
      r (lista): raios [r_haste, r_capa, r_tubo] em m.
      e (lista): [er_capa, er_trecho1, er_trecho2, ...].
      l (lista): comprimento de cada trecho em m (len(l) = len(e) - 1).
                 Ex.: sem agua  e = [capa, oleo, ar],         l = [h, H-h]
                      com agua  e = [capa, agua, oleo, ar],   l = [hw, h-hw, H-h]
    Retorna: capacitancia total [F].
    """
    capacitancia = 0
    for i in range(len(l)):
        capacitancia += capacitancia_metro(r, [e[0], e[i + 1]]) * l[i]
    return capacitancia

# 3(c)
def nivel_sonda(C, r, e):
    """
    Nivel indicado pela sonda para uma capacitancia medida,
    considerando APENAS oleo e ar (calibracao de projeto).

    Parametros:
      C (float ou array): capacitancia medida [F].
      r (lista): raios [r_haste, r_capa, r_tubo] em m.
      e (lista): permissividades; somente e[0] (capa) e usado.
    Retorna: nivel indicado [m] (sem limitar a [0, H]: permite extrapolacao).
    """
    c_oleo = capacitancia_metro(r, [e[0], ER_OLEO])  # F/m com oleo
    c_ar = capacitancia_metro(r, [e[0], ER_AR])      # F/m com ar
    C_vazio = c_ar * H                               # sonda toda no ar
    return (C - C_vazio) / (c_oleo - c_ar)

# Validação
def validacao_a(r, e):
    """
    Compara C' obtido com o valor de referencia.
    Retorna: valor obtido [F/m], referencia [F/m], erro relativo [%].
    """
    valida = capacitancia_metro(r, e)
    erro_relativo = abs((valida - C_REF_VALID) / C_REF_VALID) * 100
    return valida, C_REF_VALID, erro_relativo



# CURVA DE CALIBRACAO E LEITURA DE CAMPO

# 4(a)
def curva_calibracao(r, e):
    """
    Curva C(h) com oleo limpo (hw = 0), 0 <= h <= H.

    Parametros:
      r (lista): raios [r_haste, r_capa, r_tubo] em m.
      e (lista): [er_capa, er_oleo, er_ar].
    Retorna: h_vect [m], C_x [F], sensibilidade [pF/cm].
    """
    h_vect = np.linspace(0, H, N_PONTOS) # Criação vetor de pontos de altura
    C_x = np.zeros(len(h_vect))          # Criação vetor zerado para preencher de capacitância
    
    for i, h in enumerate(h_vect):
        C_x[i] = capacitancia_total(r, [e[0], e[1], e[2]], [h, H - h])
    sensibilidade = ((C_x[-1] - C_x[0]) * 1e12) / (H * 100)  # pF/cm
    return h_vect, C_x, sensibilidade

# 4(c) e 4(d)
def leitura_resolucao(C, r, e):
    """
    Nivel correspondente a cada leitura e menor variacao
    de nivel detectavel.

    Parametros:
      C (lista): capacitancias medidas [pF].
      r (lista): raios [r_haste, r_capa, r_tubo] em m.
      e (lista): [er_capa, er_oleo, er_ar].
    Retorna: lista de niveis [m] e menor variacao detectavel [mm].
    """
    _, _, sensibilidade = curva_calibracao(r, e)
    nivel = []
    for i in range(len(C)):
        nivel.append(float(nivel_sonda(C[i] * 1e-12, r, e)))  # funcao do Passo 3(c)
    h_min = (RESOLUCAO_C * 1e12 / sensibilidade) * 10         # pF / (pF/cm) -> cm -> mm
    return nivel, h_min



# SISTEMA COM AGUA DECANTADA

def investigacao_anomalia(r, e, C, h):
    """
    Investigacao da anomalia da agua decantada.

    Parametros:
      r (lista): raios [r_haste, r_capa, r_tubo] em m.
      e (lista): [er_capa, er_agua, er_oleo, er_ar].
      C (float): capacitancia medida [pF] (usada nos itens a e b).
      h (float): altura total de liquido medida [m].
    Retorna: nivel indicado [m], erro de indicacao [m], hw [m], vetor hw [m],
             vetor de erros [m], erro para 1 cm [m], hw em que C > C_cheio [m],
             hw em que C > 150 pF [m].
    """
    C = C * 1e-12  # pF -> F

    # a) 
    nivel_divergente = nivel_sonda(C, r, e)
    diferenca = nivel_divergente - h

    # b) 
    C_normal = capacitancia_total(r, e, [0, h, H - h])  # hw = 0 (so oleo e ar)
    c_agua = capacitancia_metro(r, [e[0], e[1]])
    c_oleo = capacitancia_metro(r, [e[0], e[2]])
    h_w = (C - C_normal) / (c_agua - c_oleo)

    # c) 
    hw_vector = np.linspace(0, HW_MAX, N_PONTOS)
    erro = np.zeros(len(hw_vector))
    for i, w in enumerate(hw_vector):
        C_w = capacitancia_total(r, e, [w, h - w, H - h])
        erro[i] = nivel_sonda(C_w, r, e) - h  

    # Erro provocado por 1 cm de agua
    C_1cm = capacitancia_total(r, e, [HW_1CM, h - HW_1CM, H - h])
    erro_1cm = nivel_sonda(C_1cm, r, e) - h

    # hw em que C ultrapassa C_cheio e em que ultrapassa o fundo de escala
    C_cheio = capacitancia_total(r, e, [0, H, 0])
    hw_cheio = (C_cheio - C_normal) / (c_agua - c_oleo)
    hw_saturacao = (C_FUNDO_ESCALA - C_normal) / (c_agua - c_oleo)

    return (nivel_divergente, diferenca, h_w, hw_vector, erro, erro_1cm,
            hw_cheio, hw_saturacao)



# REVISAO DA CAPA ISOLANTE

def revisao_capa(r, e_capas, e):
    """
    Varredura de material x espessura da capa.

    Parametros:
      r (lista): raios iniciais [r_haste, r_capa, r_tubo] em m.
      e_capas (lista): permissividades dos materiais candidatos.
      e (lista): [er_capa, er_agua, er_oleo, er_ar] (e[0] e sobrescrito).
    Retorna:
      resultados: dicionario com as configuracoes validas de maior sensibilidade;
      ini: dicionario com C_pior, h_min, R1 e R2 da configuracao inicial;
      matriz_C_pior [pF] e matriz_resolucao [mm] (material x espessura).
    """
    r_copia = r.copy()   # copias para nao alterar os vetores originais
    e_copy = e.copy()

    l_pior = [HW_PIOR_CASO, H - HW_PIOR_CASO, 0.0]  # cheio com 10 cm de agua
    possiveis_casos = {}
    resultados = {}
    ini = {}

    matriz_C_pior = np.zeros((len(e_capas), len(ESPESSURAS)))
    matriz_resolucao = np.zeros((len(e_capas), len(ESPESSURAS)))

    for i, e_capa in enumerate(e_capas):
        e_copy[0] = e_capa
        e_ideal = [e_capa, e_copy[2], e_copy[3]]  # [capa, oleo, ar] p/ calibracao

        for j, esp in enumerate(ESPESSURAS):
            r_copia[1] = r_copia[0] + esp   # Novo raio externo da capa

            C_nova = capacitancia_total(r_copia, e_copy, l_pior)    # pior caso (R1)
            _, _, sensibilidade = curva_calibracao(r_copia, e_ideal)
            h_minimo = (RESOLUCAO_C * 1e12 / sensibilidade) * 10    # mm (R2)

            matriz_C_pior[i, j] = C_nova * 1e12
            matriz_resolucao[i, j] = h_minimo

            atende_R1 = C_nova <= C_FUNDO_ESCALA
            atende_R2 = h_minimo <= R2_LIMITE_MM

            if atende_R1 and atende_R2:
                possiveis_casos[f"Material_{i}_Espessura_{j}"] = {
                    "Material": NOMES_MATERIAIS[i],
                    "Permissividade": e_capa,
                    "Espessura": esp,
                    "Capacitância": C_nova,
                    "Sensibilidade": sensibilidade,
                    "Resolução": h_minimo,
                }

            # guarda R1 e R2 da configuracao inicial separadamente (Passo 6a)
            if np.isclose(e_capa, ER_PTFE) and np.isclose(esp, ESP_INI):
                ini = {"C_pior": C_nova, "h_min": h_minimo,
                       "R1": atende_R1, "R2": atende_R2}

    # Configurações de maior sensibilidade 
    if possiveis_casos:
        melhor_valor = max(d["Sensibilidade"] for d in possiveis_casos.values())
        melhores = [k for k, d in possiveis_casos.items()
                    if np.isclose(d["Sensibilidade"], melhor_valor)]
        resultados = {k: possiveis_casos[k] for k in melhores}

    return resultados, ini, matriz_C_pior, matriz_resolucao



# GRAFICOS G1 a G4

def plotar_G1(h_vect, C_x, leituras_pF, niveis_medidos):
    plt.figure(figsize=(10, 6))  # Criação da figura
    C_x_pF = C_x * 1e12          # F -> pF

    # Desenha a linha contínua do gráfico
    plt.plot(h_vect, C_x_pF, "b-", linewidth=2, label="C(h), óleo limpo (configuração inicial)")

    # Extremos (vazio e cheio) com os valores anotados
    plt.scatter([0, H], [C_x_pF[0], C_x_pF[-1]], color="black", zorder=5, s=50, 
                label="C_vazio e C_cheio") # Plota os pontos (vazio e cheio)

    # Escreve o texto gráfico nas coordenadas específicas
    plt.annotate(f"C_vazio = {C_x_pF[0]:.2f} pF".replace(".", ","), (0, C_x_pF[0]),
                 textcoords="offset points", xytext=(8, -14))
    plt.annotate(f"C_cheio = {C_x_pF[-1]:.2f} pF".replace(".", ","), (H, C_x_pF[-1]),
                 textcoords="offset points", xytext=(-110, -16))

    # Leituras L1, L2 e L3
    cores = ["red", "green", "orange"]
    for i in range(3):
        plt.scatter(niveis_medidos[i], leituras_pF[i], color=cores[i], zorder=5, s=70,
                    label=f"L{i+1}: {leituras_pF[i]:.1f} pF → h = {niveis_medidos[i]:.3f} m".replace(".", ","))
        # Plot de linhas verticais e horizontais
        plt.vlines(niveis_medidos[i], C_x_pF[0], leituras_pF[i], linestyle="--", color=cores[i], alpha=0.7)
        plt.hlines(leituras_pF[i], 0, niveis_medidos[i], linestyle="--", color=cores[i], alpha=0.7)

    
    plt.title("G1 – Capacitância × altura de líquido (óleo limpo)", fontsize=14) # Titulo
    plt.xlabel("Altura de líquido h (m)", fontsize=12)                           # Rotulos dos eixos
    plt.ylabel("Capacitância C (pF)", fontsize=12)
    plt.grid(True, linestyle=":", alpha=0.7)                                     # Grade de fundo
    plt.legend(loc="upper left")                                                 # Mostra legenda
    plt.tight_layout()                                                           # Ajuste automático das margens
    plt.savefig(os.path.join(PASTA, "G1_C_x_h.png"), dpi=200)                    # Salva a imagem gerada
    plt.close()                                                                  # Limpa a figura da memoria


def plotar_G2(hw_vector, erro, erro_1cm, hw_cheio, hw_sat):
    plt.figure(figsize=(10, 6))
    hw_cm = hw_vector * 100  # m -> cm
    plt.plot(hw_cm, erro * 100, "r-", linewidth=2,
             label=f"Erro de indicação (h = {H_VARETA:.2f} m)".replace(".", ","))

    # 1 cm de agua
    plt.scatter(1.0, erro_1cm * 100, color="blue", zorder=5, s=60,
                label=f"Erro para 1 cm de água: {erro_1cm*100:.2f} cm".replace(".", ","))
    # Linha independente que cruza o gráfico de ponta a ponta
    # hw em que C ultrapassa C_cheio
    plt.axvline(hw_cheio * 100, color="orange", linestyle="--", linewidth=2,
                label=f"C > C_cheio em hw = {hw_cheio*100:.2f} cm".replace(".", ","))
    # hw em que C ultrapassa o fundo de escala
    plt.axvline(hw_sat * 100, color="black", linestyle="-.", linewidth=2,
                label=f"C > 150 pF em hw = {hw_sat*100:.2f} cm".replace(".", ","))

    plt.title("G2 – Erro de indicação de nível × espessura de água decantada", fontsize=14)
    plt.xlabel("Espessura da camada de água hw (cm)", fontsize=12)
    plt.ylabel("Erro de indicação de nível (cm)", fontsize=12)
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA, "G2_erro_x_hw.png"), dpi=200)
    plt.close()


def plotar_G3(espessura, matriz_C_pior, matriz_resolucao, e_capas, config_final=None):
    """
    G3: dois paineis (R1 e R2) x espessura da capa, uma curva por material.
    config_final (opcional): tupla (permissividade, espessura [m]) para marcar a escolha.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6)) # Cria uma figura dividida em vários quadros
    esp_mm = espessura * 1000
    cores = ["blue", "green", "purple"]

    for i in range(len(e_capas)):
        rotulo = f"{NOMES_MATERIAIS[i]} (εr = {e_capas[i]:.1f})".replace(".", ",")
        # Plota as curvas em cada painel (ax1 == esquerdo e ax2 == direito)
        ax1.plot(esp_mm, matriz_C_pior[i, :], color=cores[i], linewidth=2, label=rotulo)
        ax2.plot(esp_mm, matriz_resolucao[i, :], color=cores[i], linewidth=2, label=rotulo)

    # Condicional para caso queria e exista a configuração diferente da padrão do projeto
    if config_final is not None:
        i_f = int(np.argmin(np.abs(np.array(e_capas) - config_final[0])))
        j_f = int(np.argmin(np.abs(espessura - config_final[1])))
        ax1.scatter(esp_mm[j_f], matriz_C_pior[i_f, j_f], color="black", marker="*", s=160,
                    zorder=6, label="Configuração escolhida")
        ax2.scatter(esp_mm[j_f], matriz_resolucao[i_f, j_f], color="black", marker="*", s=160,
                    zorder=6, label="Configuração escolhida")

    # Linhas horizontais de ponta a ponta em cada um dos paineis
    # Limites de R1 e R2
    ax1.axhline(C_FUNDO_ESCALA * 1e12, color="red", linestyle="--", linewidth=2,
                label="Limite R1 (150 pF)")
    ax2.axhline(R2_LIMITE_MM, color="red", linestyle="--", linewidth=2,
                label=f"Limite R2 ({R2_LIMITE_MM:.1f} mm)".replace(".", ","))

    ax1.set_ylim(0, 400)                                               # Limite na escala de y 
    ax1.set_title("R1 – Capacitância máxima (cheio + 10 cm de água)")  # Equivalentes de uma estrutura normal de plotagem só que para cada painel
    ax1.set_xlabel("Espessura da capa t (mm)")
    ax1.set_ylabel("Capacitância máxima (pF)")
    ax2.set_title("R2 – Menor variação de nível detectável")
    ax2.set_xlabel("Espessura da capa t (mm)")
    ax2.set_ylabel("Menor variação de nível Δh (mm)")
    for ax in (ax1, ax2):
        ax.grid(True, linestyle=":", alpha=0.7)
        ax.legend()

    plt.suptitle("G3 – Varredura de material e espessura da capa isolante",
                 fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA, "G3_varredura_capa.png"), dpi=200)
    plt.close()


def plotar_G4(r_ini, e_ini, r_fin, e_fin, rotulo_ini, rotulo_fin):
    """
    G4: C x h para hw = 0, 1 cm e 5 cm; configuracao inicial x final.
    e_ini e e_fin = [er_capa, er_agua, er_oleo, er_ar].
    """
    h_vect = np.linspace(0, H, N_PONTOS)
    cores = ["blue", "orange", "red"]
    labels_hw = ["hw = 0", "hw = 1 cm", "hw = 5 cm"]

    fig, axs = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    # Laço para selecionar o painel
    for ax, r, e, titulo in zip(axs, (r_ini, r_fin), (e_ini, e_fin), (rotulo_ini, rotulo_fin)):
        # Atribuições de rotulos e linhas coloridas corretas
        for hw, cor, label in zip(HW_TESTE_G4, cores, labels_hw):
            C_pF = np.zeros(len(h_vect))
            for i, h in enumerate(h_vect):
                hw_real = min(h, hw)  # a agua nao pode superar a altura total
                C_pF[i] = capacitancia_total(r, e, [hw_real, h - hw_real, H - h]) * 1e12
            ax.plot(h_vect, C_pF, color=cor, linewidth=2, label=label)
        ax.axhline(C_FUNDO_ESCALA * 1e12, color="black", linestyle="--", linewidth=2,
                   label="Fundo de escala (150 pF)")
        ax.set_title(titulo)
        ax.set_xlabel("Altura total de líquido h (m)")
        ax.grid(True, linestyle=":", alpha=0.7)
        ax.legend(loc="upper left")
    axs[0].set_ylabel("Capacitância C (pF)")

    plt.suptitle("G4 – Efeito da água decantada: configuração inicial × final",
                 fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA, "G4_agua_inicial_x_final.png"), dpi=200)
    plt.close()



# EXECUCAO 

if __name__ == "__main__":

    # PASSO 3 
    print("=" * 70)
    print("PASSO 3 - Implementação e validação")
    print("=" * 70)
    valida, referencia, erro_rel = validacao_a(R_VALID, E_VALID)
    print(f"{'Grandeza':<14}{'Obtido':>14}{'Referência':>14}{'Erro relativo':>16}")
    print(f"{'C/L [pF/m]':<14}{valida*1e12:>14.3f}{referencia*1e12:>14.3f}"
          f"{erro_rel:>14.3f} %".replace(".", ","))
    print("Passo 3 (validação):", "APROVADA" if erro_rel < 1 else "REPROVADA")


    # PASSO 4 
    print("\n" + "=" * 70)
    print("PASSO 4 - Curva de calibração e leitura de campo")
    print("=" * 70)
    h_vect, C_x, sens = curva_calibracao(RAIOS_INI, E_CALIB)
    print(f"Passo 4 (a): C_vazio = {C_x[0]*1e12:.2f} pF".replace(".", ","))
    print(f"Passo 4 (a): C_cheio = {C_x[-1]*1e12:.2f} pF".replace(".", ","))
    print(f"Passo 4 (a): sensibilidade = {sens:.4f} pF/cm".replace(".", ","))

    
    coef = np.polyfit(h_vect, C_x * 1e12, 1) # Ajuste de reta linerar por mínimos quadrados
    ajuste = np.polyval(coef, h_vect) # Calculo das alturas em cada ponto pro desvio padrão
    desvio_max = np.max(np.abs(C_x * 1e12 - ajuste)) # Desvio máximo em relação à reta ajustada
    
    print(f"Passo 4 (b): Ajuste C = {coef[0]/100:.4f}·h[cm] + {coef[1]:.2f} pF;"
          f"desvio máximo = {desvio_max:.2e} pF".replace(".", ","))
    print("Passo 4 (b): A linearidade matematica se prova por meio do baixo valor de desvio dos pontos da reta ajustada.")

    niveis, h_min = leitura_resolucao(LEITURAS_PF, RAIOS_INI, E_CALIB)
    for i in range(3):
        print(f"Passo 4 (c): L{i+1} = {LEITURAS_PF[i]:.1f} pF -> h = {niveis[i]*100:.2f} cm "
              f"({niveis[i]:.4f} m)".replace(".", ","))
    print(f"Passo 4 (d): menor variação de nível distinguível = {h_min:.3f} mm".replace(".", ","))

    # PASSO 5 
    print("\n" + "=" * 70)
    print("PASSO 5 - Investigação de uma anomalia: água decantada")
    print("=" * 70)
    (nivel_ind, dif, hw_obt, hw_vector, erro_vec,
     erro_1cm, hw_cheio, hw_sat) = investigacao_anomalia(RAIOS_INI, E_AGUA, C_VARETA_PF, H_VARETA)
    print(f"Passo 5 (a): nível indicado = {nivel_ind:.4f} m ({nivel_ind*100:.2f} cm)".replace(".", ","))
    print(f"Passo 5 (a): erro em relação à altura medida = {dif*100:.2f} cm "
          f"({dif/H_VARETA*100:.1f} %)".replace(".", ","))
    print(f"Passo 5 (b): hw = {hw_obt*100:.2f} cm".replace(".", ","))
    print(f"Passo 5 (c): erro por 1 cm de água = {erro_1cm*100:.2f} cm de nível".replace(".", ","))
    print(f"Passo 5 (c): C > C_cheio para hw > {hw_cheio*100:.2f} cm".replace(".", ","))
    print(f"Passo 5 (c): C > 150 pF (fundo de escala) para hw > {hw_sat*100:.2f} cm".replace(".", ","))
    print("Passo 5 (d): discussão qualitativa (água com perdas) no relatório.")

    # PASSO 6 
    print("\n" + "=" * 70)
    print("PASSO 6 - Decisão de projeto: revisão da capa isolante")
    print("=" * 70)
    resultados, ini, mat_C, mat_dh = revisao_capa(RAIOS_INI, E_CAPAS, E_AGUA)

    # (a) configuracao inicial
    print(f"Passo 6 (a): R1 - C_max = {ini['C_pior']*1e12:.2f} pF (limite 150 pF) -> "
          f"{'ATENDE' if ini['R1'] else 'NÃO ATENDE'}".replace(".", ","))
    print(f"Passo 6 (a): R2 - Δh_min = {ini['h_min']:.3f} mm (limite {R2_LIMITE_MM:.1f} mm) -> "
          f"{'ATENDE' if ini['R2'] else 'NÃO ATENDE'}".replace(".", ","))

    # (b) varredura: faixas de espessura em que cada requisito e atendido
    limite_R1 = C_FUNDO_ESCALA * 1e12
    for i in range(len(E_CAPAS)):
        t_r1 = ESPESSURAS[mat_C[i] <= limite_R1] * 1e3          # mm
        t_r2 = ESPESSURAS[mat_dh[i] <= R2_LIMITE_MM] * 1e3      # mm
        t_ok = ESPESSURAS[(mat_C[i] <= limite_R1) & (mat_dh[i] <= R2_LIMITE_MM)] * 1e3
        s1 = f"t ≥ {t_r1.min():.2f} mm" if t_r1.size else "nunca"
        s2 = f"t ≤ {t_r2.max():.2f} mm" if t_r2.size else "nunca"
        s3 = f"{t_ok.min():.2f} a {t_ok.max():.2f} mm" if t_ok.size else "vazia"
        print(f"Passo 6 (b): {NOMES_MATERIAIS[i]:<10} R1: {s1:<14} R2: {s2:<14} "
              f"faixa válida: {s3}".replace(".", ","))

    # (c) configuracao final
    if not resultados:
        print("Passo 6 (c): nenhuma configuração atende R1 e R2.")
        raise SystemExit
    final = list(resultados.values())[0]
    er_f, t_f = final["Permissividade"], final["Espessura"]
    print(f"Passo 6 (c): escolhida = {final['Material']} (εr = {er_f:.1f}), "
          f"t = {t_f*1e3:.2f} mm".replace(".", ","))
    print(f"Passo 6 (c): sensibilidade = {final['Sensibilidade']:.4f} pF/cm; "
          f"C_max (R1) = {final['Capacitância']*1e12:.2f} pF "
          f"(folga {C_FUNDO_ESCALA*1e12 - final['Capacitância']*1e12:.2f} pF); "
          f"Δh_min (R2) = {final['Resolução']:.3f} mm".replace(".", ","))

    # (d) recalculo para a configuracao final e comparacao com a inicial
    r_final = [R_HASTE, R_HASTE + t_f, R_TUBO]
    e_final = [er_f, ER_AGUA, ER_OLEO, ER_AR]
    e_calib_final = [er_f, ER_OLEO, ER_AR]
    _, C_fin, sens_fin = curva_calibracao(r_final, e_calib_final)
    # reutiliza a funcao do Passo 5 (C_VARETA_PF so afeta os itens a e b)
    (_, _, _, _, erro_vec_f, erro_1cm_f, hw_cheio_f, hw_sat_f) = investigacao_anomalia(
        r_final, e_final, C_VARETA_PF, H_VARETA)

    print(f"{'Passo 6 (d):':<13}{'Grandeza':<40}{'Inicial':>10}{'Final':>10}")
    tabela = [
        ("C_vazio [pF]", C_x[0] * 1e12, C_fin[0] * 1e12, 2),
        ("C_cheio [pF]", C_x[-1] * 1e12, C_fin[-1] * 1e12, 2),
        ("Sensibilidade [pF/cm]", sens, sens_fin, 4),
        ("Δh_min [mm]", h_min, final["Resolução"], 3),
        ("Erro por 1 cm de água (h = 0,45 m) [cm]", erro_1cm * 100, erro_1cm_f * 100, 2),
        ("hw com C > C_cheio [cm]", hw_cheio * 100, hw_cheio_f * 100, 2),
        ("hw com C > 150 pF [cm]", hw_sat * 100, hw_sat_f * 100, 2),
        ("C_max em R1 [pF]", ini["C_pior"] * 1e12, final["Capacitância"] * 1e12, 2),
    ]
    for nome, a, b, nd in tabela:
        print(f"{'':<13}{nome:<40}{a:>10.{nd}f}{b:>10.{nd}f}".replace(".", ","))

    # GRAFICOS 
    print("\n" + "=" * 70)
    print("GRÁFICOS G1 a G4 (salvos em PNG na pasta do script)")
    print("=" * 70)
    plotar_G1(h_vect, C_x, LEITURAS_PF, niveis)
    plotar_G2(hw_vector, erro_vec, erro_1cm, hw_cheio, hw_sat)
    plotar_G3(ESPESSURAS, mat_C, mat_dh, E_CAPAS, config_final=(er_f, t_f))
    plotar_G4(RAIOS_INI, E_AGUA, r_final, e_final,
              f"Configuração inicial (PTFE, {ESP_INI*1e3:.2f} mm)".replace(".", ","),
              f"Configuração final ({final['Material']}, {t_f*1e3:.2f} mm)".replace(".", ","))
    print("Gráficos G1 a G4 salvos em:", PASTA)
    print("\nExecução concluída.")
