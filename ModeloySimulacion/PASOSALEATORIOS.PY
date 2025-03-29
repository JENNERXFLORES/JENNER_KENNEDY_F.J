import numpy as np
import matplotlib.pyplot as plt

# Parámetros
n_steps = 1000  # Número de pasos de la caminata
step_size = 1   # Tamaño de cada paso

# Generar pasos aleatorios (-1 para izquierda, 1 para derecha)
steps = np.random.choice([-1, 1], size=n_steps) * step_size

# Calcular la posición del caminante en cada paso
positions = np.cumsum(steps)

# Graficar la caminata aleatoria
plt.figure(figsize=(10, 6))
plt.plot(positions, label='Caminata Aleatoria')
plt.xlabel('Número de Pasos')
plt.ylabel('Posición')
plt.title('Caminata Aleatoria en 1D')
plt.legend()
plt.grid(True)
plt.show()
