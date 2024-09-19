import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parâmetros da máquina
f = 60  # Frequência em Hz
w = 2 * np.pi * f  # Velocidade angular
t = np.linspace(0, 0.1, 1000)  # Tempo, 1000 pontos de 0 a 0.1 segundos
Imax = 607.8  # Amplitude da corrente
N = 417  # Número de espiras (pode ajustar este valor)
ae = 0  # Ângulo espacial (para 2 polos, ae = 0)
ang = 0  # Ângulo inicial (pode ajustar este valor)

# Funções para as Fmm das fases (fasores a, b, c)
def fmm_a(t):
    return N * Imax * 1/2 * (np.cos(w * t + ae) + np.cos(w * t - ae))

def fmm_b(t):
    return N * Imax * 1/2 * (np.cos(w * t + ae + 4 * np.pi / 3) + np.cos(w * t - ae))

def fmm_c(t):
    return N * Imax * 1/2 * (np.cos(w * t + ae - 4 * np.pi / 3) + np.cos(w * t - ae))

# Criar figura e eixos para a animação
fig, ax = plt.subplots(figsize=(10, 6))

# Ajustar os limites dos eixos para mostrar todo o gráfico
# Baseado na soma total das Fmm que pode atingir até 3 * N * Imax
max_fmm_total = 3 * N * Imax
ax.set_xlim(0, 0.1)  # Limitar o eixo x ao tempo
ax.set_ylim(-max_fmm_total, max_fmm_total)  # Ajustar o eixo y aos valores esperados das Fmm

# Linhas das Fmm das fases e a soma
line_a, = ax.plot([], [], label='Fmm Fase A', color='r')
line_b, = ax.plot([], [], label='Fmm Fase B', color='g')
line_c, = ax.plot([], [], label='Fmm Fase C', color='b')
line_total, = ax.plot([], [], label='Fmm Total', color='k', linewidth=2)

# Inicialização dos dados (listas vazias para começar)
def init():
    line_a.set_data([], [])
    line_b.set_data([], [])
    line_c.set_data([], [])
    line_total.set_data([], [])
    return line_a, line_b, line_c, line_total

# Função de atualização para a animação
def update(frame):
    t_current = t[:frame]  # Considera o tempo até o frame atual

    # Fmm de cada fase neste instante de tempo
    fmm_a_inst = fmm_a(t[:frame])
    fmm_b_inst = fmm_b(t[:frame])
    fmm_c_inst = fmm_c(t[:frame])

    # Soma das Fmm das três fases
    fmm_total = fmm_a_inst + fmm_b_inst + fmm_c_inst

    # Atualizar as linhas de cada Fmm e a soma total
    line_a.set_data(t_current, fmm_a_inst)
    line_b.set_data(t_current, fmm_b_inst)
    line_c.set_data(t_current, fmm_c_inst)
    line_total.set_data(t_current, fmm_total)
    
    return line_a, line_b, line_c, line_total

# Criar a animação
ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=20)

# Etiquetas e legendas
plt.title('Animação das Fmm de cada fase e sua soma (gráficos senoidais)')
plt.xlabel('Tempo (s)')
plt.ylabel('Fmm')
plt.grid(True)
plt.legend()

# Mostrar a animação
plt.show()


