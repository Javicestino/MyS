import numpy as np
import matplotlib.pyplot as plt

# Condiciones iniciales
g = 9.81  # Gravedad (m/s^2)
m = 80.0  # Masa de la persona (kg)
y0 = [20, 0]  # [x0, v0] siendo x la altura y v la velocidad
t_span = [0, 30]  # Tiempo de simulación (s)
h = 0.1  # Paso de tiempo (s)
t_eval = np.arange(t_span[0], t_span[1], h)  # Array de tiempos
k = 185  # Constante elástica de la cuerda (N/m)
b = 75  # Coeficiente de amortiguación (Ns/m)
tam_cuerda = 10  # Longitud de la cuerda (m)

# Resultados
pos = np.zeros(len(t_eval))  
vel = np.zeros(len(t_eval))  
accel = np.zeros(len(t_eval))  

# Condiciones iniciales
pos[0] = y0[0]  
vel[0] = y0[1]  
accel[0] = -g  

# Función para calcular la aceleración
def calcular_aceleracion(pos_actual, vel_actual):
    if pos_actual >= y0[0] - tam_cuerda:
        # caída libre (solo gravedad)
        return -g
    else:
        # Fase elástica (cuerda estirada)
        stretch = (y0[0] - tam_cuerda) -pos_actual  # Estiramiento de la cuerda y0[0] - tam_cuerda me dice a partir de cuando se estira la cuerda y al restarle la pos_actual se cuanto se estira en cada momento, es decir la distancia en la que esta ejerciendo fuerza elastica
        return -g + (k / m) * stretch - (b / m) * vel_actual

# Bucle principal de Euler
for i in range(0, len(t_eval) - 1):
    # Calcular la aceleración en el paso actual
    accel[i] = calcular_aceleracion(pos[i], vel[i])
    
    # Actualizar velocidad y posición
    vel[i + 1] = vel[i] + h * accel[i]
    pos[i + 1] = pos[i] + h * vel[i + 1]
    
    # Si toca el suelo, detener la simulación
    if pos[i + 1] < 0:
        pos[i + 1] = 0  # Evitar posiciones negativas
        break

# Graficar resultados
plt.plot(t_eval[:len(pos)], pos, label='Posición vertical')
plt.axhline(y=y0[0] - tam_cuerda, color='r', linestyle='--', label='Comienzo frenado cuerda')
plt.axhline(y=0, color='k', linestyle='-', label='Suelo')
plt.legend()
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición (m)')
plt.grid()
plt.show()