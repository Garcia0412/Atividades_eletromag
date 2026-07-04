#TRABALHO 2 - ELETROMAGNETISMO - TURMA A1 - 09/07/2026 - OPÇÃO  -  
# INTEGRANTES DO GRUPO: LUCAS VINÍCIUS DE CARVALHO REIS - 12421EEL005 // VINÍCIUS LIMA GARCIA - 12421EEL009

# IMPORTAÇÃO DAS BIBLIOTECAS
import os
import math
import numpy as np
import matplotlib.pyplot as plt

# VALORES FORNECIDOS


e_r1 = 2.3
e_r2 = 3.0



# DEFINIÇÃO DA MALHA
def Malha_2D(val_min, val_max, n):
    x = np.linspace(val_min, val_max, n) # Vetor unidimensional de x
    y = np.linspace(val_min, val_max, n) # Vetor unidimensional de y

    X,Y = np.meshgrid(x, y, indexing='ij') # Matriz de coordenadas (malha espacial)

    # DEFINIÇÃO DO PASSO A SER DADO ENTRE CADA PONTO DA MALHA
    delta_x = (val_max - val_min)/(n - 1)
    delta_y = (val_max - val_min)/(n - 1)

    return X, Y, delta_x, delta_y

# CALCULOS DAS DENSIDADES PARA CADA INTERFACE
def Densidade_XLPE ( X, Y, p):
    B = 0.00000003
    ro_L = 0.000004
    PI = math.pi
    Dx = ((ro_L)/(2*PI)) * (X/(X**2 + Y**2)) + B * ((X-p[0])/((X-p[0])**2 + Y**2))
    Dy = ((ro_L)/(2*PI)) * (Y/(X**2 + Y**2)) + B * (Y/((X-p[0])**2 + Y**2))

    return Dx, Dy

def Densidade_EPR ( X, Y, p):
    B = 0.00000003
    ro_L = 0.000004
    PI = math.pi
    Dx = ((ro_L)/(2*PI)) * (X/(X**2 + Y**2)) - B * ((X-p[0])/((X-p[0])**2 + Y**2))
    Dy = ((ro_L)/(2*PI)) * (Y/(X**2 + Y**2)) - B * (Y/((X-p[0])**2 + Y**2))

    return Dx, Dy


def plot_graficos(X, Y, ro_n, ro_a, Dx, Dy):

    # DEFININDO UM PATH PARA ALOCAR AS IMAGENS DOS GRÁFICOS E CRIANDO A PASTA
    pasta_destino = 'Resultados_Graficos'
    if not os.path.exists(pasta_destino): # Confere se a pasta não existe
        os.makedirs(pasta_destino) # Cria a pasta se não existir

    # Transforma as listas em arrays do numpy para facilitar a manipulação
    ro_a = np.array(ro_a)
    ro_n = np.array(ro_n)

    """ 
    raio = np.sqrt(X**2 + Y**2)
    mascara_fora = (raio < 0.01) | (raio > 0.03) # Delimita a área de centro do condutor 

    # Exclui a área do centro do condutor para a plotagem deixar o isolante mais visível 
    ro_n[mascara_fora] = np.nan
    ro_a[mascara_fora] = np.nan
    Dx[mascara_fora] = np.nan
    Dy[mascara_fora] = np.nan
    """

    #VISUALIZAÇÃO DO GRÁFICO DE CAMPO VETORIAL
    plt.figure(figsize=(8, 8)) # Define o tamanho do gráfico
    p = 10 # Passo pra definir amostragem e evitar que as setas fiquem "invisíveis" pela grande quantidade de pontos

    # Fatiamento das matrizes
    X_q = X[::p, ::p]
    Y_q = Y[::p, ::p]
    Dx_q = Dx[::p, ::p]
    Dy_q = Dy[::p, ::p]

    
    modulo = np.sqrt(Dx_q**2 + Dy_q**2) # Obtém o módulo do vetor
    modulo[modulo == 0] = 1e-15 # Impede a divisão por zero

    # Transforma o vetor em unitário
    Dx_norm = Dx_q / modulo
    Dy_norm = Dy_q / modulo

    plt.quiver(X_q, Y_q, Dx_norm, Dy_norm, color='teal', pivot='mid') # Recebe os valores para gerar o gráfico
    plt.title('G1: Campo Vetorial da Densidade de Fluxo Elétrico (D)') # Gera o título do gráfico
    plt.xlabel('Eixo X (m)') # Eixo x
    plt.ylabel('Eixo Y (m)') # Eixo y
    plt.xlim(val_min, val_max) # Limites do eixo x
    plt.ylim(val_min, val_max) # Limites do eixo y
    plt.savefig(f'{pasta_destino}/Campo Vetorial da Densidade de Fluxo Elétrico (D).png', dpi=300, bbox_inches='tight') # Salva o gráfico na pasta escolhida para apresentar na interface

    #VISUALIZAÇÃO DO GRÁFICO DENSIDADE DE CARGA NUMÉRICA (Tirando o que foi comentado a abixo, tds os outros seguem a mesma funcionalidade do de cima)
    plt.figure(figsize=(8, 8))
    plt.contourf(X, Y, ro_n, levels=50, cmap='inferno') # Recebe os valores para gerar o gráfico
    plt.colorbar(label='Densidade de Carga Numérica') # Define a barra de cor
    plt.title('G2: Mapa de Calor - Divergente de D (Numérico)')
    plt.xlabel('Eixo X (m)')
    plt.ylabel('Eixo Y (m)')
    plt.savefig(f'{pasta_destino}/Mapa de Calor - Divergente de D (Numérico).png', dpi=300, bbox_inches='tight')

    #VISUALIZAÇÃO DO GRÁFICO DENSIDADE DE CARGA ANALÍTICA
    plt.figure(figsize=(8, 8))
    plt.contourf(X, Y, ro_a, levels=50, cmap='inferno')
    plt.colorbar(label='Densidade de Carga analítica')
    plt.title('G3: Mapa de Calor - Divergente de D (Analítico)')
    plt.xlabel('Eixo X (m)')
    plt.ylabel('Eixo Y (m)')
    plt.savefig(f'{pasta_destino}/Mapa de Calor - Divergente de D (Analítico).png', dpi=300, bbox_inches='tight')

    #VISUALIZAÇÃO DO GRÁFICO DE ERRO ABSOLUTO
    erro_absoluto = np.abs(np.array(ro_n) - np.array(ro_a))
    plt.figure(figsize=(8, 8))
    plt.contourf(X, Y, erro_absoluto, levels=50, cmap='inferno')
    plt.colorbar(label='Erro absoluto')
    plt.title('G4: Mapa de Calor - Erro absoluto')
    plt.xlabel('Eixo X (m)')
    plt.ylabel('Eixo Y (m)')
    plt.savefig(f'{pasta_destino}/Mapa de Calor - Erro absoluto.png', dpi=300, bbox_inches='tight')
