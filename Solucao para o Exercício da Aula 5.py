import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.animation import FuncAnimation

# Parâmetros da máquina
f = 60  # Frequência em Hz
w = 2 * np.pi * f  # Velocidade angular
t = np.linspace(0, 0.1, 1000)  # Tempo, 1000 pontos de 0 a 0.1 segundos
Imax = 608  # Amplitude da corrente
N = 417  # Número de espiras (você pode ajustar esse valor)
ae = 0  # Ângulo elétrico (para 2 polos, ae = 0)

# Funções para as Fmm das fases (fasores a, b, c)
def fmm_a(t):
    return N * Imax * 1/2 * (np.cos(w * t + ae) + np.cos(w * t - ae))

def fmm_b(t):
    return N * Imax * 1/2 * (np.cos(w * t + ae + 4 * np.pi / 3) + np.cos(w * t - ae))

def fmm_c(t):
    return N * Imax * 1/2 * (np.cos(w * t + ae - 4 * np.pi / 3) + np.cos(w * t - ae))

# Calcular as Fmm para cada fase
fmm_a_vals = fmm_a(t)
fmm_b_vals = fmm_b(t)
fmm_c_vals = fmm_c(t)

# Calcular a soma total das Fmm
fmm_total = fmm_a_vals + fmm_b_vals + fmm_c_vals

# Criar o gráfico de Fmm_total vs Tempo
plt.figure(figsize=(10, 6))
plt.plot(t, fmm_total, label='Fmm Total', color='k', linewidth=2)
plt.title('Fmm Total vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Fmm Total (A·turn)')
plt.grid(True)
plt.legend()
plt.show()

# Parâmetros adicionais para a animação das fases
frequencia = 60  # Frequência em Hz
w_e = 2 * np.pi * frequencia  # Velocidade angular elétrica (rad/s)
k_enr = 0.9  # Constante do enrolamento
N_fase = 417  # Número de voltas por fase
Phi_p = 0.8  # Fluxo magnético por polo (Wb)
t = 0.01  # Tempo em segundos
num_fases = 3  # Fases A, B, C
num_polos = 2  # Máquina de 2 polos
q = 1  # Número de bobinas por fase por polo
slots_per_pole_per_phase = 1  # Número de ranhuras por polo e por fase
total_slots = num_fases * num_polos * q * slots_per_pole_per_phase  # Ranhuras totais
raio_estator = 1.315  # Raio do estator

# Dados das fases e ângulos
fases = ['A', "A'", 'B', "B'", 'C', "C'"]
angulos = [0, 180, 120, 300, 240, 60]  # Ângulos em graus para A, A', B, B', C, C'
cores_fases = ['red', 'green', 'blue']  # A, B, C
cores_ranhuras = ['red', 'red', 'green', 'green', 'blue', 'blue']  # A, A', B, B', C, C'

# Função para calcular a tensão induzida em uma ranhura
def calcular_tensao_induzida(angulo_total, t):
    return -w_e * k_enr * N_fase * Phi_p * np.sin(np.radians(angulo_total) + w_e * t)

# Calcular os fasores (componentes real e imaginária) e as magnitudes das tensões
x_vals = []
y_vals = []
tensoes = []

for angulo in angulos:
    tensao = calcular_tensao_induzida(angulo, t)
    tensoes.append(tensao)
    # Componentes do fasor
    x_vals.append(tensao * np.cos(np.radians(angulo)))
    y_vals.append(tensao * np.sin(np.radians(angulo)))

# Definir os limites baseados nos valores dos fasores
x_min = min(x_vals + [-val for val in x_vals]) * 1.2  # Ampliar o limite inferior
x_max = max(x_vals + [-val for val in x_vals]) * 1.2  # Ampliar o limite superior
y_min = min(y_vals + [-val for val in y_vals]) * 1.2  # Ampliar o limite inferior
y_max = max(y_vals + [-val for val in y_vals]) * 1.2  # Ampliar o limite superior

# Criar a primeira figura: Diagrama Fasorial para Fases A, B e C
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.set_xlim(x_min, x_max)
ax1.set_ylim(y_min, y_max)
# Desenhar os fasores para fases A, B e C
for i in range(len(fases)):
    if fases[i] in ['A', 'B', 'C']:
        cor = cores_fases[['A', 'B', 'C'].index(fases[i])]
        ax1.add_patch(FancyArrowPatch((0, 0), (x_vals[i], y_vals[i]), color=cor, arrowstyle='-|>', mutation_scale=20, linewidth=2))
        ax1.text(x_vals[i] + 0.1 * (x_max - x_min), y_vals[i] + 0.1 * (y_max - y_min), fases[i], color=cor, ha='center', va='center', fontsize=10)
ax1.axhline(0, color='black', linewidth=0.5)
ax1.axvline(0, color='black', linewidth=0.5)
ax1.set_title('Diagrama Fasorial para Fases A, B e C')
ax1.set_xlabel('Componente Real (V)')
ax1.set_ylabel('Componente Imaginária (V)')
ax1.grid(True)
ax1.set_aspect('equal', adjustable='box')
# Adicionar legenda à figura de fases
legenda_fases = [f'{fases[i]} (Tensão: {tensoes[i]:.2f} V)' for i in range(len(fases)) if fases[i] in ['A', 'B', 'C']]
ax1.legend(legenda_fases, loc='lower left')

# Criar a segunda figura: Diagrama Fasorial para Tensões em Ranhuras A, A', B, B', C, C'
fig, ax2 = plt.subplots(figsize=(12, 6))
ax2.set_xlim(x_min, x_max)
ax2.set_ylim(y_min, y_max)
# Desenhar os fasores para tensões em ranhuras A, A', B, B', C, C'
for i in range(len(fases)):
    cor = cores_ranhuras[fases.index(fases[i])]
    if fases[i] in ["A", "B", "C"]:
        ax2.add_patch(FancyArrowPatch((0, 0), (x_vals[i], y_vals[i]), color=cor, arrowstyle='-|>', mutation_scale=20, linewidth=2))
    elif fases[i] in ["A'", "B'", "C'"]:
        ax2.add_patch(FancyArrowPatch((0, 0), (-x_vals[i], -y_vals[i]), color=cor, arrowstyle='-|>', mutation_scale=20, linewidth=2))
    # Ajustar a posição das etiquetas para evitar sobreposição
    offset = 0.1 * (x_max - x_min)
    if fases[i] in ["A"]:
        ax2.text(x_vals[i] + offset, y_vals[i] + offset, fases[i], color=cor, ha='center', va='center', fontsize=10)
    elif fases[i] in ["A'"]:
        ax2.text(-x_vals[i] - offset, -y_vals[i] - offset, fases[i], color=cor, ha='center', va='center', fontsize=10)
    elif fases[i] in ["B"]:
        ax2.text(x_vals[i] + offset, y_vals[i] - offset, fases[i], color=cor, ha='center', va='center', fontsize=10)
    elif fases[i] in ["B'"]:
        ax2.text(-x_vals[i] - offset, -y_vals[i] + offset, fases[i], color=cor, ha='center', va='center', fontsize=10)
    elif fases[i] in ["C"]:
        ax2.text(x_vals[i] - offset, y_vals[i] - offset, fases[i], color=cor, ha='center', va='center', fontsize=10)
    elif fases[i] in ["C'"]:
        ax2.text(-x_vals[i] + offset, -y_vals[i] + offset, fases[i], color=cor, ha='center', va='center', fontsize=10)
ax2.axhline(0, color='black', linewidth=0.5)
ax2.axvline(0, color='black', linewidth=0.5)
ax2.set_title('Diagrama Fasorial para Tensões em Ranhuras A, A\', B, B\', C, C\'')
ax2.set_xlabel('Componente Real (V)')
ax2.set_ylabel('Componente Imaginária (V)')
ax2.grid(True)
ax2.set_aspect('equal', adjustable='box')
# Adicionar legenda à figura de ranhuras
legenda_ranhuras = [f'{fases[i]} (Tensão: {tensoes[i % len(tensoes)]:.2f} V)' for i in range(len(fases))]
ax2.legend(legenda_ranhuras, loc='lower left')

# Definir ângulos para a animação
angles_rad = np.linspace(0, np.pi, num_fases, endpoint=False)  # Apenas para fases A, B, C
angles_rad_prima = angles_rad + np.pi  # Fases A', B', C' a 180 graus das fases A, B, C

# Combinar os dois conjuntos de ângulos
angles_rad_combined = np.empty(total_slots)
angles_rad_combined[0::2] = angles_rad  # A, B, C
angles_rad_combined[1::2] = angles_rad_prima  # A', B', C'

# Cores para cada grupo de fases
fases_cores = ['red', 'green', 'blue']

# Criar a terceira figura: Animação das Fases da Máquina
fig, ax3 = plt.subplots()
ax3.set_aspect('equal')
ax3.set_xlim(-1.5 * raio_estator, 1.5 * raio_estator)
ax3.set_ylim(-1.5 * raio_estator, 1.5 * raio_estator)
ax3.set_xlabel('Eixo X')
ax3.set_ylabel('Eixo Y')
ax3.set_title('Animação das Fases da Máquina Trifásica de 2 Polos')

# Desenhar o círculo do estator
estator = plt.Circle((0, 0), raio_estator, color='black', fill=False)
ax3.add_artist(estator)

# Inicialização dos pontos e cruzes
símbolos = []
textos = []

# Criar os pontos e cruzes iniciais
for i, theta in enumerate(angles_rad_combined):
    x = raio_estator * np.cos(theta)
    y = raio_estator * np.sin(theta)
    fase_label = fases[i % len(fases)]  # Obter a fase correspondente
    # Criar um ponto ou cruz
    if i % 2 == 0:
        símbolo, = ax3.plot(x, y, 'o', color=fases_cores[i // 2], markersize=10)
    else:
        símbolo, = ax3.plot(x, y, 'x', color=fases_cores[i // 2], markersize=10)
    símbolos.append(símbolo)
    # Numerar as ranhuras no sentido anti-horário
    texto = ax3.text(x * 1.1, y * 1.1, fase_label, fontsize=12, ha='center', va='center')
    textos.append(texto)

# Função de atualização para a animação
def atualizar(frame):
    # Determinar a cor atual a ser alterada
    índice_cor = (frame // 40) % num_fases  # Mover a cada 40 frames
    # Alternar entre ponto ('o') e cruz ('x') para a cor selecionada
    for i in range(total_slots):
        if i // 2 == índice_cor:  # Apenas os símbolos da cor atual
            if (frame // 20) % 2 == 0:
                if i % 2 == 0:
                    símbolos[i].set_marker('x')  # Mudar de ponto para cruz
                else:
                    símbolos[i].set_marker('o')  # Mudar de cruz para ponto
            else:
                if i % 2 == 0:
                    símbolos[i].set_marker('o')  # Mudar de cruz para ponto
                else:
                    símbolos[i].set_marker('x')  # Mudar de ponto para cruz
    return símbolos

# Criar a animação
ani = FuncAnimation(fig, atualizar, frames=200, interval=100, blit=False)

# Mostrar as figuras
plt.show()

