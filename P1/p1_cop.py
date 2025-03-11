import numpy as np
import sim # no hace falta en coppellia simplemente para que no salgan errores

def sysCall_init():
    global object_handle, g, m, k, b, tam_cuerda, dt, pos, vel

    # Obtener handle del objeto (nombre en la escena)
    object_handle = sim.getObject('/puenting')

    # Parámetros físicos
    g = 9.81   # Gravedad (m/s^2)
    m = 80.0   # Masa de la persona (kg)
    k = 185.0  # Constante elástica de la cuerda (N/m)
    b = 75.0   # Coeficiente de amortiguación (Ns/m)
    tam_cuerda = 10.0  # Longitud de la cuerda (m)
    
    # Condiciones iniciales
    pos = 20.0  # Altura inicial (m)
    vel = 0.0   # Velocidad inicial (m/s)

    # Configurar la posición inicial del objeto en CoppeliaSim
    sim.setObjectPosition(object_handle, -1, [0, 0, pos])

def calcular_aceleracion(pos_actual, vel_actual):
    """Calcula la aceleración en cada instante."""
    if pos_actual >= 20 - tam_cuerda:
        return -g  # Caída libre
    else:
        stretch = (20 - tam_cuerda) - pos_actual  # Estiramiento de la cuerda
        return -g + (k / m) * stretch - (b / m) * vel_actual  # Fuerzas elásticas y de amortiguación

def sysCall_actuation():
    global pos, vel

    dt = sim.getSimulationTimeStep()  # Obtener paso de simulación

    # Calcular aceleración
    accel = calcular_aceleracion(pos, vel)

    # Método de Euler para actualizar velocidad y posición
    vel += dt * accel
    pos += dt * vel

    # Si toca el suelo, detener el movimiento
    if pos < 0:
        pos = 0
        vel = 0

    # Actualizar posición en CoppeliaSim
    sim.setObjectPosition(object_handle, -1, [0, 0, pos])
