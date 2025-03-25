import numpy as np
import matplotlib.pyplot as plt

# Parámetros del sistema
m1 = 1.0  # Masa 1 (kg)
m2 = 2.0  # Masa 2 (kg)
l1 = 1.0  # Longitud 1 (m)
l2 = 1.0  # Longitud 2 (m)
g = 9.81  # Aceleración debido a la gravedad (m/s^2)

# Momento de inercia del balancín
J = m1 * l1**2 + m2 * l2**2

# Condiciones iniciales
theta0 = 0.0  # Ángulo inicial (rad)
omega0 = 0.0  # Velocidad angular inicial (rad/s)
y0 = [theta0, omega0]  # Vector de condiciones iniciales [theta, omega]

# Parámetros de la simulación
tf = 10.0  # Tiempo final (s)
h = 0.001  # Paso de tiempo (s)
t_eval = np.arange(0, tf, h)  # Vector de tiempos

# Función de caída libre
def caida_libre(t_act, pos_ini, vel_ini):
    print("Caída libre")
    print("Posición inicial:", pos_ini, "Velocidad inicial:", vel_ini)
    
    # Calcular el tamaño necesario para pos y vel
    tamaño = len(t_eval) - t_act
    pos = np.zeros(tamaño)
    vel = np.zeros(tamaño)
    
    pos[0] = pos_ini
    vel[0] = vel_ini
    
    for i in range(tamaño - 1):
        accel = -g
        vel[i + 1] = vel[i] + h * accel
        pos[i + 1] = pos[i] + h * vel[i + 1]
        if pos[i + 1] <= 0:
            pos[i + 1:] = 0  # Asegurar que la posición sea 0 después del impacto
            vel[i + 1:] = 0  # Detener la velocidad
            break
    
    return pos, vel

# Definir el sistema de ecuaciones diferenciales de primer orden
def second_order_ode(t, y):
    theta, omega = y  
    k = m1 * g * l1 * np.cos(theta) - m2 * g * l2 * np.cos(theta)
    alpha = k / J
    dydt = [omega, alpha]
    return np.array(dydt)

# Método de Euler para resolver el sistema de ODEs
y_euler = np.zeros((2, len(t_eval)))  
y_euler[:, 0] = y0 


pos = np.zeros(len(t_eval))  
vel = np.zeros(len(t_eval))  
# Aplicar el método de Euler
for i in range(0, len(t_eval) - 1):
    dydt = second_order_ode(t_eval[i], y_euler[:, i])
    y_euler[:, i + 1] = y_euler[:, i] + h * dydt
    
    if abs(y_euler[0, i + 1]) > np.radians(45):  # Comprobar si el ángulo supera los 45 grados
        # Calcular la velocidad lineal de la masa 1: v1 = w * l1
        vel_ini = y_euler[1, i + 1] * -l1
        pos_ini = -l1 * np.sin(y_euler[0, i + 1]) 
        y_euler[1, i + 1] = 0.0  # Detener el movimiento (velocidad angular = 0)
        
        # Llamar a la función de caída libre
        pos_caida, vel_caida = caida_libre(i, pos_ini, vel_ini)
        
        # Asignar los valores de caída libre a los arreglos pos y vel
        pos[i:] = pos_caida
        vel[i:] = vel_caida
        break

# Extraer theta y omega de la solución
theta = y_euler[0, :]
omega = y_euler[1, :]

# Cálculo de las posiciones verticales de las masas
x1 = -l1 * np.sin(theta)
x2 = l2 * np.sin(theta)
# Encontrar el índice donde comienza la caída libre
indice_caida_libre = np.argmax(abs(theta) > np.radians(45))

# Gráficas
plt.figure(figsize=(12, 10))

# 1. Ángulo theta en función del tiempo
plt.subplot(3, 1, 1)
plt.plot(t_eval[:indice_caida_libre], np.degrees(theta[:indice_caida_libre]), 'b-', label='θ(t) (Balancín)')
plt.plot(t_eval[indice_caida_libre:], np.degrees(theta[indice_caida_libre:]), 'b--', label='θ(t) (Caída libre)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Ángulo (grados)')
plt.title('Ángulo del balancín en función del tiempo')
plt.legend()
plt.grid()

# 2. Posición vertical de las masas en función del tiempo
plt.subplot(3, 1, 2)
plt.plot(t_eval[:indice_caida_libre], x1[:indice_caida_libre], 'r-', label='x1(t) (Balancín)')
plt.plot(t_eval[:indice_caida_libre], x2[:indice_caida_libre], 'g-', label='x2(t) (Balancín)')
plt.plot(t_eval[indice_caida_libre:], pos[indice_caida_libre:], 'r--', label='x1(t) (Caída libre)')
plt.plot(t_eval[indice_caida_libre:], x2[indice_caida_libre:], 'g--', label='x2(t) (Caída libre)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición vertical (m)')
plt.title('Posición vertical de las masas en función del tiempo')
plt.legend()
plt.grid()

# 3. Velocidades de las masas en función del tiempo
plt.subplot(3, 1, 3)
# Velocidad angular (omega) antes y después de la caída libre
plt.plot(t_eval[:indice_caida_libre], omega[:indice_caida_libre], 'm-', label='m2 (Balancín)')
plt.plot(t_eval[indice_caida_libre:], omega[indice_caida_libre:], 'm--', label='m2 (Caída libre)')
# Velocidad lineal de la masa 1 antes y después de la caída libre
v1 = omega * -l1  # Velocidad lineal de la masa 1
plt.plot(t_eval[:indice_caida_libre], v1[:indice_caida_libre], 'c-', label='m1 (Balancín)')
plt.plot(t_eval[indice_caida_libre:], vel[indice_caida_libre:], 'c--', label='m1 (Caída libre)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (rad/s o m/s)')
plt.title('Velocidades de las masas en función del tiempo')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()