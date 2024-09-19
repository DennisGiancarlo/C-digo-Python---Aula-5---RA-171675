import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parámetros de la máquina
f = 60  # Frecuencia en Hz
w = 2 * np.pi * f  # Velocidad angular
t = np.linspace(0, 0.1, 1000)  # Tiempo, 1000 puntos de 0 a 0.1 segundos
Imax = 607.8  # Amplitud de la corriente
N = 417  # Número de espiras (puedes ajustar este valor)
ae = 0  # Ángulo espacial (para 2 polos, ae = 0)
ang = 0  # Ángulo inicial (puedes ajustar este valor)

# Funciones para las Fmm de las fases (fasores a, b, c)
def fmm_a(t):
    return N * Imax * 1/2 * (np.cos(w * t + ae) + np.cos(w * t - ae))

def fmm_b(t):
    return N * Imax * 1/2 * (np.cos(w * t + ae + 4 * np.pi / 3) + np.cos(w * t - ae))

def fmm_c(t):
    return N * Imax * 1/2 * (np.cos(w * t + ae - 4 * np.pi / 3) + np.cos(w * t - ae))

# Crear figura y ejes para la animación
fig, ax = plt.subplots(figsize=(10, 6))

# Ajustar los límites de los ejes para mostrar toda la gráfica
# Basado en la suma total de las Fmm que puede alcanzar hasta 3 * N * Imax
max_fmm_total = 3 * N * Imax
ax.set_xlim(0, 0.1)  # Limitar el eje x al tiempo
ax.set_ylim(-max_fmm_total, max_fmm_total)  # Ajustar el eje y a los valores esperados de las Fmm

# Líneas de las Fmm de las fases y la suma
line_a, = ax.plot([], [], label='Fmm Fase A', color='r')
line_b, = ax.plot([], [], label='Fmm Fase B', color='g')
line_c, = ax.plot([], [], label='Fmm Fase C', color='b')
line_total, = ax.plot([], [], label='Fmm Total', color='k', linewidth=2)

# Inicialización de los datos (listas vacías para empezar)
def init():
    line_a.set_data([], [])
    line_b.set_data([], [])
    line_c.set_data([], [])
    line_total.set_data([], [])
    return line_a, line_b, line_c, line_total

# Función de actualización para la animación
def update(frame):
    t_current = t[:frame]  # Considera el tiempo hasta el frame actual

    # Fmm de cada fase en este instante de tiempo
    fmm_a_inst = fmm_a(t[:frame])
    fmm_b_inst = fmm_b(t[:frame])
    fmm_c_inst = fmm_c(t[:frame])

    # Suma de las Fmm de las tres fases
    fmm_total = fmm_a_inst + fmm_b_inst + fmm_c_inst

    # Actualizar las líneas de cada Fmm y la suma total
    line_a.set_data(t_current, fmm_a_inst)
    line_b.set_data(t_current, fmm_b_inst)
    line_c.set_data(t_current, fmm_c_inst)
    line_total.set_data(t_current, fmm_total)
    
    return line_a, line_b, line_c, line_total

# Crear la animación
ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=20)

# Etiquetas y leyendas
plt.title('Animación de las Fmm de cada fase y su suma (gráficas senoidales)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Fmm')
plt.grid(True)
plt.legend()

# Mostrar la animación
plt.show()


