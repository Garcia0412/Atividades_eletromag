#TRABALHO 1 - ELETROMAGNETISMO - TURMA A1 - 04/06/2026 - OPÇÃO A - CABO COAXIAL 
# INTEGRANTES DO GRUPO: LUCAS VINÍCIUS DE CARVALHO REIS - 12421EEL005 // VINÍCIUS LIMA GARCIA - 12421EEL009

# IMPORTAÇÃO DAS BIBLIOTECAS
import os
import math
import numpy as np
import matplotlib.pyplot as plt


# DEFINIÇÃO DA MALHA
def Malha_2D(val_min, val_max, n):
    x = np.linspace(val_min, val_max, n) # Vetor unidimensional de x
    y = np.linspace(val_min, val_max, n) # Vetor unidimensional de y

    X,Y = np.meshgrid(x, y, indexing='ij') # Matriz de coordenadas (malha espacial)

    # DEFINIÇÃO DO PASSO A SER DADO ENTRE CADA PONTO DA MALHA
    delta_x = (val_max - val_min)/(n - 1)
    delta_y = (val_max - val_min)/(n - 1)

    return X, Y, delta_x, delta_y

#CALCULO DA DENSIDADE (implementa a formula fornecida na questão)
def Densidade(x,y,x0):
    Dx = (p_L/(2*PI)) * (x/(x**2 + y**2 + E)) + A * ((x - x0)/((x-x0)**2 + y**2 + E))
    Dy = (p_L/(2*PI)) * (y/(x**2 + y**2 + E)) + A * ((y)/((x-x0)**2 + y**2 + E))

    return Dx,Dy

#CALCULO DA DIVERGÊNCIA NUMERICAMENTE
def Divergencia_numerica (Dx, Dy, delta_x, delta_y):
    # Tamanho da malha para o laço
    Nx = len(Dx)        
    Ny = len(Dx[0])

    ro_n = [[0.0 for _ in range(Ny)] for _ in range(Nx)] # Cria a matriz que vai guardar o rô calculado númericamente

    # Laço que percorre a malha
    for i in range(Nx):
        for j in range(Ny):

            # Derivada parcial em x
            if i == 0:
                dx = (Dx[i+1][j]-Dx[i][j])/delta_x  # Diferença unilateral progressiva
            elif i == Nx - 1:
                dx = (Dx[i][j]-Dx[i-1][j])/delta_x  # Diferença unilateral regressiva
            else:
                dx = (Dx[i+1][j] - Dx[i-1][j]) / (2 * delta_x) # Diferença centrada

            # Derivada parcial em y
            if j == 0:
                dy = (Dy[i][j+1]-Dy[i][j])/delta_y  # Diferença unilateral progressiva
            elif j == Ny - 1:
                dy = (Dy[i][j]-Dy[i][j-1])/delta_y  # Diferença unilateral regressiva
            else:
                dy = (Dy[i][j+1] - Dy[i][j-1]) / (2 * delta_y) # Diferença centrada
            # Calculo do divergente
            ro_n[i][j] = dx + dy
    return ro_n

#CALCULO DO RÔ ANALITICAMENTE 
def Divergência_analitica(X, Y, x0):
    # Tamanho da malha
    Nx = len(X)        
    Ny = len(X[0])

    ro_a = [[0.0 for _ in range(Ny)] for _ in range(Nx)] # Cria a matriz que vai guardar o rô calculado númericamente

    # Laço que percorre a malha
    for i in range(Nx):
        for j in range(Ny):
            
            x = X[i][j]
            y = Y[i][j]

            # Componentes do divergente já calculados
            dx = (p_L/(2*PI)) * ((y**2 - x**2 + E)/(y**2 + x**2 + E)**2) + A*((y**2-(x-x0)**2 + E)/((x-x0)**2 + y**2 + E)**2)
            dy = (p_L/(2*PI)) * ((x**2 - y**2 + E)/(y**2 + x**2 + E)**2) + A*(((x-x0)**2-y**2 + E)/((x-x0)**2 + y**2 + E)**2)

            ro_a[i][j] = dx + dy
    return ro_a

def plot_graficos(X, Y, ro_n, ro_a, Dx, Dy):

    #DEFININDO UM PATH PARA ALOCAR AS IMAGENS DOS GRÁFICOS E CRIANDO A PASTA
    pasta_destino = 'Resultados_Graficos'
    if not os.path.exists(pasta_destino): # Confere se a pasta não existe
        os.makedirs(pasta_destino) # Cria a pasta se não existir

    # Transforma as listas em arrays do numpy para facilitar a manipulação
    ro_a = np.array(ro_a)
    ro_n = np.array(ro_n)

    raio = np.sqrt(X**2 + Y**2)
    mascara_fora = (raio < 0.01) | (raio > 0.03) # Delimita a área de centro do condutor 

    # Exclui a área do centro do condutor para a plotagem  deixar o isolante mais visível 
    ro_n[mascara_fora] = np.nan
    ro_a[mascara_fora] = np.nan
    Dx[mascara_fora] = np.nan
    Dy[mascara_fora] = np.nan

    #VISUALIZAÇÃO DO GRÁFICO DE CAMPO VETORIAL
    plt.figure(figsize=(8, 8)) 
    p = 10 # Passo pra definir amostragem e evitar que as setas fiquem "invisíveis" pela grande quantidade de pontos

    # Fatiamento das matrizes
    X_q = X[::p, ::p]
    Y_q = Y[::p, ::p]
    Dx_q = Dx[::p, ::p]
    Dy_q = Dy[::p, ::p]

    
    modulo = np.sqrt(Dx_q**2 + Dy_q**2) # Transformação dos vetores em vetores unitários
    modulo[modulo == 0] = 1e-15 # Impede a divisão por zero

    # Transforma o vetor em unitário
    Dx_norm = Dx_q / modulo
    Dy_norm = Dy_q / modulo

    plt.quiver(X_q, Y_q, Dx_norm, Dy_norm, color='teal', pivot='mid')

    plt.title('G1: Campo Vetorial da Densidade de Fluxo Elétrico (D)')
    plt.xlabel('Eixo X (m)')
    plt.ylabel('Eixo Y (m)')
    plt.xlim(val_min, val_max)
    plt.ylim(val_min, val_max)
    #plt.show()
    plt.savefig(f'{pasta_destino}/Campo Vetorial da Densidade de Fluxo Elétrico (D).png', dpi=300, bbox_inches='tight')

    #VISUALIZAÇÃO DO GRÁFICO DENSIDADE DE CARGA NUMÉRICA
    plt.figure(figsize=(8, 6))
    plt.contourf(X, Y, ro_n, levels=50, cmap='inferno')
    plt.colorbar(label='Densidade de Carga Numérica')
    plt.title('G2: Mapa de Calor - Divergente de D (Numérico)')
    plt.xlabel('Eixo X (m)')
    plt.ylabel('Eixo Y (m)')
    #plt.show()
    plt.savefig(f'{pasta_destino}/Mapa de Calor - Divergente de D (Numérico).png', dpi=300, bbox_inches='tight')

    #VISUALIZAÇÃO DO GRÁFICO DENSIDADE DE CARGA ANALÍTICA
    plt.figure(figsize=(8, 6))
    plt.contourf(X, Y, ro_a, levels=50, cmap='inferno')
    plt.colorbar(label='Densidade de Carga analítica')
    plt.title('G3: Mapa de Calor - Divergente de D (Analítico)')
    plt.xlabel('Eixo X (m)')
    plt.ylabel('Eixo Y (m)')
    #plt.show()
    plt.savefig(f'{pasta_destino}/Mapa de Calor - Divergente de D (Analítico).png', dpi=300, bbox_inches='tight')

    #VISUALIZAÇÃO DO GRÁFICO DE ERRO ABSOLUTO
    erro_absoluto = np.abs(np.array(ro_n) - np.array(ro_a))
    plt.figure(figsize=(8, 6))
    plt.contourf(X, Y, erro_absoluto, levels=50, cmap='inferno')
    plt.colorbar(label='Erro absoluto')
    plt.title('G4: Mapa de Calor - Erro absoluto')
    plt.xlabel('Eixo X (m)')
    plt.ylabel('Eixo Y (m)')
    #plt.show()
    plt.savefig(f'{pasta_destino}/Mapa de Calor - Erro absoluto.png', dpi=300, bbox_inches='tight')

    

def main():
    #CONSTANTES 
    PI = math.pi
    A = 5 * 10**(-8)
    E = 1e-7 # Adicionado para melhorar a exibição do gráfico e diminuição de erros

    # DEFINIÇÃO DAS VARIAVEIS 
    n = 201
    val_min = - 0.03
    val_max = 0.03
    p_L = 0.000003
    Er = 2.3
    ro = 3.0
    p = [0.018 , 0]

    X, Y, delta_x, delta_y = Malha_2D(val_min, val_max, n)
    Dx, Dy = Densidade(X, Y, p[0])
    ro_n = Divergencia_numerica(Dx, Dy, delta_x, delta_y)
    ro_a = Divergência_analitica(X, Y, p[0])
    
    #PLOTANDO OS GRÁFICOS SOLICITADOS
    print("Calculo concluído! Gerando gráfico...")
    plot_graficos(X, Y, ro_n, ro_a, Dx, Dy)
    
    
main()
