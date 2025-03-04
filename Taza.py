import numpy as np
import matplotlib.pyplot as plt


# Condiciones iniciales

T0 = 100
K = 0.02
Tamb = 24
h = 0.1
t_span = [0, 5*60] # Cuanto tiempo queremos simularlo
t_eval = np.arange(t_span[0], t_span[1], h)

# Euler

T = np.zeros(len(t_eval))
T[0] = T0

for i in range(0, len(t_eval) -1):
   dT_dt = -K * (T[i-1] - Tamb)
   T[i+1] = T[i] + h * dT_dt

plt.plot(t_eval, T)
plt.xlabel('Tiempo (s)')
plt.ylabel('Temperatura (°C)')
plt.show()

