import numpy as np


# Parámetros físicos
m1 = 1.0
m2 = 2.0
l1 = 1.0
l2 = 1.0
g = 9.81
J = m1 * l1**2 + m2 * l2**2

# Estado del sistema
theta = 0.0
omega = 0.0
h = 0.01
t = 0.0
tiempo_total = 10.0
caida = False
caida_terminada = False

# Variables de caída libre
pos = 0.0
vel = 0.0

# Handles y posición base
masa1 = -1
masa2 = -1
pos_masa1_base = [0, 0, 0]
pos_masa2_base = [0, 0, 0]

def caida_libre_step(pos, vel):
    accel = -g
    vel += h * accel
    pos += h * vel
    if pos <= 0:
        pos = 0
        vel = 0
        global caida_terminada
        caida_terminada = True
    return pos, vel

def sysCall_init():
    sim = require('sim')
    global masa1, masa2, theta, omega, t
    global pos_masa1_base, pos_masa2_base

    

    masa1 = sim.getObject('/Cuboid_MySS1')
    masa2 = sim.getObject('/Cuboid_MySS2')

    pos_masa1_base = sim.getObjectPosition(masa1, -1)
    pos_masa2_base = sim.getObjectPosition(masa2, -1)

    theta = 0.0
    omega = 0.0
    t = 0.0

def sysCall_actuation():
    global theta, omega, t, caida, pos, vel, caida_terminada

    if t >= tiempo_total or caida_terminada:
        return

    if not caida:
        # Ecuación del movimiento angular (Euler)
        k = m1 * g * l1 * np.cos(theta) - m2 * g * l2 * np.cos(theta)
        alpha = k / J
        omega += h * alpha
        theta += h * omega

        # Alturas relativas
        z1 = -l1 * np.sin(theta)
        z2 = l2 * np.sin(theta)

        # Aplicar solo el cambio en Z manteniendo X e Y
        sim.setObjectPosition(masa1, -1, [pos_masa1_base[0], pos_masa1_base[1], pos_masa1_base[2] + z1])
        sim.setObjectPosition(masa2, -1, [pos_masa2_base[0], pos_masa2_base[1], pos_masa2_base[2] + z2])

        if abs(theta) > np.radians(45):
            caida = True
            omega = 0.0
            vel = -l1 * omega  # omega ya es 0
            pos = pos_masa1_base[2] + z1  # altura absoluta actual de la masa
            
    else:
        pos, vel = caida_libre_step(pos, vel)
        sim.setObjectPosition(masa1, -1, [pos_masa1_base[0], pos_masa1_base[1], pos])

    t += h

def sysCall_sensing():
    pass

def sysCall_cleanup():
    pass
