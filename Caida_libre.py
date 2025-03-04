import numpy as np
import matplotlib.pyplot as plt

# En este problema queremos conocer la posición (x) y velocidad (dx/dt) del objeto a lo
# largo del tiempo, a estas variables es a lo que llamaremos “estado (y)”. Como es una
# ODE de segundo orden, las condiciones iniciales son: x(t=0), dx/dt(t=0).


# Condiciones iniciales
g = 9.81
m = 10.0
y0 = [60,0] # [x0, v0] siendo x la altura y v la velocidad
t_span = [0, 15] # Cuanto tiempo queremos simularlo
h = 0.1
t_eval = np.arange(t_span[0], t_span[1], h)

# Coeficiente elastico
e = 0.5

# Euler

pos = np.zeros(len(t_eval))
vel = np.zeros(len(t_eval))
pos[0] = y0[0]
vel[0] = y0[1]
accel = np.zeros(len(t_eval))
accel[0] = -g

for i in range(0, len(t_eval) -1):
    accel = -g # aceleracion constante de la gravedad
    vel[i+1] = vel[i] + h * accel
    pos[i+1] = pos[i] + h * vel[i]

    # Si toca el suelo pare o rebote
    if pos[i+1] < 0:  
        pos[i+1] = 0
        vel[i+1] = -e * vel[i] # Rebote
        if vel[i+1] < 0.1: # Si la velocidad es muy baja, pare
            break

plt.plot(t_eval, pos)
plt.legend(['Posición vertical'])
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición (m)')
plt.show()

