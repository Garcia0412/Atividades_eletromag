#TRABALHO 2 - ELETROMAGNETISMO - TURMA A1 - 09/07/2026 - OPÇÃO  -  
# INTEGRANTES DO GRUPO: LUCAS VINÍCIUS DE CARVALHO REIS - 12421EEL005 // VINÍCIUS LIMA GARCIA - 12421EEL009

# IMPORTAÇÃO DAS BIBLIOTECAS
import os
import numpy as np
import matplotlib.pyplot as plt


# DEFINIÇÃO DA MALHA
def Malhas_2D(val_min, val_max, n, L):
    # LIMITES DOS MEIOS DO DIELÉTRICO PASSADOS POR LISTA
    a = L[0] # Condutor
    c = L[1] # Região 1
    b = L[2] # Região 2

    x = np.linspace(val_min, val_max, n) # Vetor unidimensional de x
    y = np.linspace(val_min, val_max, n) # Vetor unidimensional de y

    X,Y = np.meshgrid(x, y, indexing='ij') # Matriz de coordenadas (malha espacial)

    # DEFINIÇÃO DO RAIO
    R = np.sqrt(X**2 + Y**2)

    # DEFINIÇÃO DA MALHA DE ÂNGULOS
    phi = np.linspace(0, 2 * np.pi, 500)

    # DEFINIÇÃO DAS MÁSCARAS PARA CADA REGIÃO
    regiao_1 = (R >= a) & (R <= c)
    regiao_2 = (R > c) & (R <= b)
    descarte = (R < a) | (R > b)
    reg = [descarte, regiao_1, regiao_2 ]


    return X, Y, reg, phi

# CALCULOS DAS DENSIDADES PARA CADA INTERFACE
def Densidade ( X, Y, p, reg):
    B = 3.0e-8
    ro_L = 4.0e-6
    PI = np.pi

    # CRIAÇÃO DE UMA MATRIZ VAZIA
    Dx = np.zeros_like(X)
    Dy = np.zeros_like(Y)

    # OPERAÇÃO NORMAL
    num_n = ((ro_L)/(2*PI))
    den_n = (X**2 + Y**2)

    Dx_n = num_n * (X/den_n)
    Dy_n = num_n * (Y/den_n)

    # OPERAÇÃO ANÔMALA
    den_a = ((X - p[0])**2 + (Y - p[1])**2)

    # REGIÃO 1
    Dx[reg[1]] = Dx_n[reg[1]] + B * ((X[reg[1]] - p[0]) / (den_a[reg[1]]))
    Dy[reg[1]] = Dy_n[reg[1]] + B * ((Y[reg[1]] - p[1]) / (den_a[reg[1]]))

    # REGIÃO 2
    Dx[reg[2]] = Dx_n[reg[2]] - B * ((X[reg[2]] - p[0]) / (den_a[reg[2]]))
    Dy[reg[2]] = Dy_n[reg[2]] - B * ((Y[reg[2]] - p[1]) / (den_a[reg[2]]))

    # REGIÃO DESCARTE
    Dx[reg[0]] = np.nan
    Dy[reg[0]] = np.nan

    return Dx, Dy

def cond_fronteira (Dx, Dy, L, phi, n):

    e_1 = 2.3 * 8.854e-12
    e_2 = 3.0 * 8.854e-12

    c = L[1] 
    b = L[2] 

    # AJUSTES DE PASSO DA COORDENADA PARA DETERMINAR AS CONDIÇÕES DE FRONTEIRA
    passo = (2 * b)/(n - 1)

    # PONTOS ADJACENTES ANTERIORES A INTERFACE COM ANOMALIA
    r_1 = c - passo
    x_1 = r_1 * np.cos(phi)
    y_1 = r_1 * np.sin(phi)

    # CONVERSÃO EM ÍNDICES
    idx_x1 = np.round((x_1 - (-b)) / passo).astype(int)
    idx_y1 = np.round((y_1 - (-b)) / passo).astype(int)

    # PONTOS ADJACENTES POSTERIORES A INTERFACE COM ANOMALIA
    r_2 = c + passo
    x_2 = r_2 * np.cos(phi)
    y_2 = r_2 * np.sin(phi)

    # CONVERSÃO EM ÍNDICES
    idx_x2 = np.round((x_2 - (-b)) / passo).astype(int)
    idx_y2 = np.round((y_2 - (-b)) / passo).astype(int)

    # EXTRAÇÃO DAS MATRIZES
    Dx_1 = Dx[idx_x1, idx_y1]
    Dy_1 = Dy[idx_x1, idx_y1]

    Dx_2 = Dx[idx_x2, idx_y2]
    Dy_2 = Dy[idx_x2, idx_y2]

    # CALCULO DAS COMPONENTES NORMAIS E TANGENCIAIS
    Dn_1 = Dx_1 * np.cos(phi) + Dy_1 * np.sin(phi)
    Dn_2 = Dx_2 * np.cos(phi) + Dy_2 * np.sin(phi)
    rho_s = Dn_1 - Dn_2
    Dn = [Dn_1, Dn_2, rho_s]

    Dt_1 = -Dx_1 * np.sin(phi) + Dy_1 * np.cos(phi)
    Dt_2 = -Dx_2 * np.sin(phi) + Dy_2 * np.cos(phi)
    Dt = [Dt_1, Dt_2]

    Et_1 = Dt_1 / e_1
    Et_2 = Dt_2 / e_2
    salto_Et = Et_1 - Et_2
    Et = [Et_1, Et_2, salto_Et]

    return Dn, Dt, Et    

def Calculo_analitico (phi, p):
    B = 3.0e-8
    c = 0.02

    x0 = p[0]
    y0 = p[1]
    x = c * np.cos(phi)
    y = c * np.sin(phi)


    denominador = (x - x0)**2 + (y - y0)**2
    Dx_anomalia = B * (x - x0) / denominador
    Dy_anomalia = B * (y - y0) / denominador 
    rho_a = 2 * (Dx_anomalia * np.cos(phi) + Dy_anomalia * np.sin(phi))

    return rho_a


def plot_graficos(X, Y, phi, L, Dx, Dy, Dn, Dt, Et, rho_a):
    
    # EXTRAINDO OS DADOS
    erro_abs = np.abs(Dn[2] - rho_a)
    phi_graus = np.degrees(phi)
    a = L[0] 
    c = L[1] 
    b = L[2] 

    # DEFININDO UM PATH PARA ALOCAR AS IMAGENS DOS GRÁFICOS E CRIANDO A PASTA
    pasta_destino = 'Resultados_Graficos'
    if not os.path.exists(pasta_destino): # Confere se a pasta não existe
        os.makedirs(pasta_destino) # Cria a pasta se não existir


    # VISUALIZAÇÃO DO GRÁFICO DE CAMPO VETORIAL
    plt.figure(figsize=(8, 8)) # Define o tamanho do gráfico
    p = 10 # Passo pra definir amostragem e evitar que as setas fiquem "invisíveis" pela grande quantidade de pontos

    # FATIAMENTO DAS MATRIZES
    X_q = X[::p, ::p]
    Y_q = Y[::p, ::p]
    Dx_q = Dx[::p, ::p]
    Dy_q = Dy[::p, ::p]


    # DETERMINAÇÃO DAS BORDAS DAS SUPERFÍCIES 
    condu = plt.Circle((0,0), a, color='black', fill=False, linestyle='--', label='Condutor Interno (r=a)')
    diele = plt.Circle((0,0), c, color='red', fill=False, linewidth=2, label='Dielétrico (r=c)')
    blind = plt.Circle((0,0), b, color='black', fill=False, linestyle='--', label='Blindagem (r=b)')

    plt.quiver(X_q, Y_q, Dx_q, Dy_q, color='blue', scale=5e-4, width=0.003) # Recebe os valores para gerar o gráfico

    # ADICIONANDO AS BORDAS
    plt.gca().add_patch(condu)
    plt.gca().add_patch(diele)
    plt.gca().add_patch(blind)


    plt.title('G1: Distribuição Vetorial do Campo D') # Gera o título do gráfico
    plt.xlabel('Eixo X (m)') # Eixo x
    plt.ylabel('Eixo Y (m)') # Eixo y
    plt.xlim(-b*1.1, b*1.1) # Limites do eixo x
    plt.ylim(-b*1.1, b*1.1) # Limites do eixo y
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':')
    plt.savefig(f'{pasta_destino}/Distribuição Vetorial do Campo D.png', dpi=300, bbox_inches='tight') # Salva o gráfico na pasta escolhida para apresentar na interface

    #VISUALIZAÇÃO DO GRÁFICO DENSIDADE DE CARGA NUMÉRICA (Tirando o que foi comentado a abixo, tds os outros seguem a mesma funcionalidade do de cima)
    plt.figure(figsize=(10, 5))
    plt.plot(phi_graus, Dn[2], 'b-', linewidth=3, label=r'Numérico ($\Delta D_n$)')
    plt.plot(phi_graus, rho_a, 'r--', linewidth=2, label=r'Teórico ($\rho_a$)')

    plt.title('G2: Validação da Densidade de Carga Superficial na Interface')
    plt.xlabel('Ângulo (graus)')
    plt.ylabel(r'Densidade de Carga / Salto $D_n$ ($C/m^2$)')
    plt.xlim(0, 360)
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{pasta_destino}/Validação da Densidade de Carga Superficial na Interface.png', dpi=300, bbox_inches='tight')

    #VISUALIZAÇÃO DO GRÁFICO DENSIDADE DE CARGA ANALÍTICA
    plt.figure(figsize=(10, 5))
    plt.plot(phi_graus, Et[2], 'g-', linewidth=2, label=r'Salto numérico $\Delta E_t$')
    plt.title('G3: Continuidade da Componente Tangencial')
    plt.xlabel('Ângulo (graus)')
    plt.ylabel(r'Salto do Campo Elétrico %\Delta E_t% (%V/m%)')
    plt.xlim(0, 360)
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{pasta_destino}/Continuidade da Componente Tangencial.png', dpi=300, bbox_inches='tight')

    #VISUALIZAÇÃO DO GRÁFICO DE ERRO ABSOLUTO
    
    plt.figure(figsize=(10, 3))

    erro_2d = erro_abs[np.newaxis, :]
    imagem = plt.imshow(erro_2d, aspect='auto', cmap='Reds', extent=[0, 360, 0, 1])
    plt.yticks([])
    plt.colorbar(imagem, label=r'Erro Absoluto ($C/m^2$)')
    plt.title('G4: Mapa de Calor - Erro absoluto')
    plt.xlabel('Ângulos (Graus)')
    plt.savefig(f'{pasta_destino}/Mapa de Calor - Erro absoluto_2.png', dpi=300, bbox_inches='tight')

def main():
    L = [0.01, 0.02, 0.035]
    n = 300
    X, Y, reg, phi = Malhas_2D(-L[2], L[2], n, L)
    p = [0.01, 0.01732]
    Dx, Dy = Densidade ( X, Y, p, reg)
    Dn, Dt, Et = cond_fronteira (Dx, Dy, L, phi, n)
    rho_a = Calculo_analitico (phi, p)
    plot_graficos(X, Y, phi, L, Dx, Dy, Dn, Dt, Et, rho_a)

main()