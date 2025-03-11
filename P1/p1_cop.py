import numpy as np


def sysCall_init():
    sim = require('sim')
    global object_handle, g, m, k, b, tam_cuerda, dt, pos, vel, pos_ini

    # Obtener handle del objeto (nombre en la escena)
    object_handle = sim.getObject('/Cubo')

    # Parametros
    g = 9.81   # Gravedad (m/s^2)
    m = 80.0   # Masa de la persona (kg)
    k = 185.0  # Constante el?stica de la cuerda (N/m)
    b = 75.0   # Coeficiente de amortiguaci?n (Ns/m)
    tam_cuerda = 10.0  # Longitud de la cuerda (m)
    pos_ini = 20
    # Condiciones iniciales
    pos = pos_ini  # Altura inicial (m)
    vel = 0.0   # Velocidad inicial (m/s)

    # Configurar la posicion inicial del objeto en CoppeliaSim
    sim.setObjectPosition(object_handle, -1, [0, 0, pos])
   
def calcular_aceleracion(pos_actual,vel_actual):
    # Calcular aceleracion para cada h
    if pos_actual >= pos_ini - tam_cuerda:
        return -g # Caida libre
    else:
        stretch = (pos_ini - tam_cuerda) - pos_actual # Lo que se ha estirado mi cuerda
        return -g + (k/m) * stretch - (b/m) * vel_actual
       
def sysCall_actuation():
    global pos, vel

    dt = sim.getSimulationTimeStep()  # Obtener paso de simulaci?n

    # Calcular aceleraci?n
    accel = calcular_aceleracion(pos, vel)

    # M?todo de Euler para actualizar velocidad y posici?n
    vel += dt * accel
    pos += dt * vel

    # Si toca el suelo, detener el movimiento
    if pos < 0:
        pos = 0
        vel = 0

    # Actualizar posici?n en CoppeliaSim
    sim.setObjectPosition(object_handle, -1, [0, 0, pos])

   



def sysCall_sensing():

    # put your sensing code here

    pass



def sysCall_cleanup():

    # do some clean-up here

    pass



# See the user manual or the available code snippets for additional callback functions and details