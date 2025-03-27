import numpy as np
import matplotlib.pyplot as plt

# Parámetros
m1, m2 = 2.0, 1.0
Fm1, Fm2 = 2.0, 10.0   # Fuerza aplicada a cada coche
x1_init, x2_init = 10.0, 0.0
b1, b2 = 0.5, 0.3
e = 0.99
total_time, dt = 20.0, 0.01
car_length = 1.25  # Longitud de cada coche

def car_collision_both_moving(m1, m2, Fm1, Fm2, b1, b2, e, total_time, dt, car_length):
    t_eval = np.arange(0, total_time, dt)
    num_steps = len(t_eval)
    y_euler = np.zeros((4, num_steps))
    # Coche 1 inicia en x=10 y Coche 2 en x=0, ambos en reposo
    y_euler[:, 0] = [x1_init, 0, x2_init, 0]

    def system_ode(t, y, Fm1_active, Fm2_active):
        x1, v1, x2, v2 = y
        # La aceleración se calcula aplicando la fuerza solo si está activa
        dv1dt = (Fm1_active * Fm1 - b1 * v1) / m1  
        dv2dt = (Fm2_active * Fm2 - b2 * v2) / m2
        return np.array([v1, dv1dt, v2, dv2dt])

    def update_velocities(v1, v2, m1, m2, e):
        v1f = ((m1 - e * m2) * v1 + (1 + e) * m2 * v2) / (m1 + m2)
        v2f = ((m2 - e * m1) * v2 + (1 + e) * m1 * v1) / (m1 + m2)
        return v1f, v2f

    Fm1_active = 1
    Fm2_active = 1
    collision_occurred = False
    collision_time = None

    for i in range(num_steps - 1):
        # Se verifica si la distancia entre los coches es menor o igual a la longitud de un coche.
        if not collision_occurred and abs(y_euler[0, i] - y_euler[2, i]) <= car_length:
            collision_occurred = True
            collision_time = t_eval[i]
            # Se desactivan las fuerzas en ambos coches tras la colisión
            Fm1_active = 0  
            Fm2_active = 0  
            # Actualiza las velocidades según la colisión
            y_euler[1, i], y_euler[3, i] = update_velocities(y_euler[1, i], y_euler[3, i], m1, m2, e)

        dydt = system_ode(t_eval[i], y_euler[:, i], Fm1_active, Fm2_active)
        y_euler[:, i+1] = y_euler[:, i] + dt * dydt

    return t_eval, y_euler, collision_time

# Simulación
t, y, collision_time = car_collision_both_moving(m1, m2, Fm1, Fm2, b1, b2, e, total_time, dt, car_length)

# Gráfico
plt.figure(figsize=(12, 6))

# --- Posiciones ---
plt.subplot(2, 1, 1)
plt.plot(t, y[0, :], label='Coche 1 (x1)', color='blue', linewidth=2)
plt.plot(t, y[2, :], label='Coche 2 (x2)', color='orange', linewidth=2)
if collision_time is not None:
    plt.axvline(collision_time, color='red', linestyle='--', label='Choque')
    idx = int(collision_time / dt)
    plt.plot(collision_time, y[0, idx], 'bo', markersize=10)
    plt.plot(collision_time, y[2, idx], 'o', color='orange', markersize=10)
plt.ylabel('Posición (m)')
plt.title('Colisión de Coches - Ambos coches en movimiento')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# --- Velocidades ---
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
