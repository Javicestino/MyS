import numpy as np
import matplotlib.pyplot as plt

# Parámetros generales
m1, m2 = 2.0, 1.0       # masas (puedes modificar para los distintos escenarios)
Fm1, Fm2 = 2.0, 10.0     # fuerza de empuje de cada motor
x1_init, x2_init = 10.0, 0.0  # posiciones iniciales: se asume que x1 > x2
b1, b2 = 0.5, 0.3       # coeficientes de rozamiento viscosa
total_time, dt = 20.0, 0.01
car_length = 1.25       # longitud de cada coche
k = 1000.0              # constante elástica del choque

def car_collision_force_analysis(m1, m2, Fm1, Fm2, b1, b2, k, total_time, dt, car_length):
    """
    Simula la colisión entre dos coches usando un modelo de fuerza elástica (resorte).
    Se considera que los motores actúan hasta que se detecta el inicio de la colisión.
    Tras el choque, los motores se apagan y la interacción se rige por la fuerza del resorte.
    """
    t_eval = np.arange(0, total_time, dt)
    num_steps = len(t_eval)
    y_euler = np.zeros((4, num_steps))
    # Estado inicial: [posición coche1, velocidad coche1, posición coche2, velocidad coche2]
    y_euler[:, 0] = [x1_init, 0, x2_init, 0]
    
    # Bandera para indicar si ya ocurrió la colisión (se activa la fuerza de resorte y se apagan motores)
    collision_occurred = False
    collision_time = None

    for i in range(num_steps - 1):
        x1, v1, x2, v2 = y_euler[:, i]
        
        # Verificar si se inicia la colisión: la condición es que la distancia entre coches sea menor a car_length.
        if not collision_occurred and (x1 - x2) <= car_length:
            collision_occurred = True
            collision_time = t_eval[i]
        
        # Durante la simulación, mientras no ocurra la colisión, se aplican las fuerzas de empuje.
        if not collision_occurred:
            F1 = Fm1 - b1*v1
            F2 = Fm2 - b2*v2
        else:
            # Tras el choque, se apagan los motores: Fm = 0, y se añade la fuerza elástica si hay solapamiento.
            # Calcular el solapamiento:
            overlap = max(0, car_length - (x1 - x2))
            F_spring = k * overlap  # fuerza elástica repulsiva
            # Se suma la fuerza de rozamiento (que siempre actúa) y la fuerza de resorte:
            F1 = -b1*v1 + F_spring      # el coche delantero recibe fuerza en +x
            F2 = -b2*v2 - F_spring      # el coche trasero recibe fuerza en -x
        
        # Ecuaciones de movimiento: 
        # dx/dt = v   y   dv/dt = Fuerza / masa
        a1 = F1 / m1
        a2 = F2 / m2
        
        # Integración con método de Euler
        y_euler[0, i+1] = x1 + dt * v1
        y_euler[1, i+1] = v1 + dt * a1
        y_euler[2, i+1] = x2 + dt * v2
        y_euler[3, i+1] = v2 + dt * a2

    return t_eval, y_euler, collision_time

# Simulación
t, y, collision_time = car_collision_force_analysis(m1, m2, Fm1, Fm2, b1, b2, k, total_time, dt, car_length)

# Gráficos
plt.figure(figsize=(12, 6))

# --- Gráfico de posiciones ---
plt.subplot(2, 1, 1)
plt.plot(t, y[0, :], label='Coche 1 (x1)', color='blue', linewidth=2)
plt.plot(t, y[2, :], label='Coche 2 (x2)', color='orange', linewidth=2)
if collision_time is not None:
    plt.axvline(collision_time, color='red', linestyle='--', label='Inicio de colisión')
    idx = int(collision_time / dt)
    plt.plot(collision_time, y[0, idx], 'bo', markersize=10)
    plt.plot(collision_time, y[2, idx], 'o', color='orange', markersize=10)
plt.ylabel('Posición (m)')
plt.title('Colisión de Coches (Análisis de Fuerzas)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# --- Gráfico de velocidades ---
plt.subplot(2, 1, 2)
plt.plot(t, y[1, :], label='Coche 1 (v1)', color='blue', linewidth=2)
plt.plot(t, y[3, :], label='Coche 2 (v2)', color='orange', linewidth=2)
if collision_time is not None:
    plt.axvline(collision_time, color='red', linestyle='--')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (m/s)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
