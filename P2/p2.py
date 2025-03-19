import numpy as np
import matplotlib.pyplot as plt

# Parámetros del sistema
m1 = 1.0  # Masa 1 (kg)
m2 = 1.25  # Masa 2 (kg)
l1 = 1.0  # Longitud 1 (m)
l2 = 1.0  # Longitud 2 (m)
g = 9.81  # Aceleración debido a la gravedad (m/s^2)

# Momento de inercia del balancín
J = m1 * l1**2 + m2 * l2**2

# Condiciones iniciales
theta0 = 0.0  # Ángulo inicial (rad) -> Ahora funciona incluso con theta0 = 0
omega0 = 0.0  # Velocidad angular inicial (rad/s)
y0 = [theta0, omega0]  # Vector de condiciones iniciales [theta, omega]

# Parámetros de la simulación
t0 = 0.0  # Tiempo inicial (s)
tf = 10.0  # Tiempo final (s)
h = 0.0001  # Paso de tiempo (s)
t_eval = np.arange(t0, tf, h)  # Vector de tiempos

# Definir el sistema de ecuaciones diferenciales de primer orden
def second_order_ode(t, y):
    theta, omega = y  
    k = m1 * g * l1 * np.cos(theta) - m2 * g * l2 * np.cos(theta)
    alpha = k / J
    # d(theta)/dt = omega, d(omega)/dt = alpha
    dydt = [omega, alpha]
    return np.array(dydt)

# Método de Euler para resolver el sistema de ODEs
y_euler = np.zeros((2, len(t_eval)))  
y_euler[:, 0] = y0 

# Aplicar el método de Euler
for i in range(0, len(t_eval) - 1):
    dydt = second_order_ode(t_eval[i], y_euler[:, i])
    # y(t+1) = y(t) + h * dy/dt
    y_euler[:, i + 1] = y_euler[:, i] + h * dydt

# Extraer theta y omega de la solución
theta = y_euler[0, :]
omega = y_euler[1, :]

# Cálculo de las posiciones verticales de las masas (usando seno para la componente vertical)
x1 = l1 * np.sin(theta)
x2 = -l2 * np.sin(theta)

# Gráficas
plt.figure(figsize=(12, 8))

# Ángulo theta en función del tiempo
plt.subplot(3, 1, 1)
plt.plot(t_eval, np.degrees(theta), label='θ(t)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Ángulo (grados)')
plt.title('Ángulo del balancín en función del tiempo')
plt.legend()
plt.grid()

# Posición vertical de las masas en función del tiempo
plt.subplot(3, 1, 2)
plt.plot(t_eval, x1, label='x1(t)')
plt.plot(t_eval, x2, label='x2(t)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición vertical (m)')
plt.title('Posición vertical de las masas en función del tiempo')
plt.legend()
plt.grid()

# Velocidad angular en función del tiempo
plt.subplot(3, 1, 3)
plt.plot(t_eval, omega, label='ω(t)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad angular (rad/s)')
plt.title('Velocidad angular del balancín en función del tiempo')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()