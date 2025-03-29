import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Título de la presentación
st.title("🚶‍♂️📊 Caminata Aleatoria en 1D")

st.write("""
Esta presentación explica paso a paso cómo funciona una **caminata aleatoria en 1D**.
En este modelo, un caminante empieza en la posición 0 y en cada paso puede moverse:
- **Hacia la derecha (+1)**
- **Hacia la izquierda (-1)**  

Cada dirección tiene la misma probabilidad.  
La simulación mostrará cómo se mueve el caminante a lo largo del tiempo.
""")

#codigo

st.code("""
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
""", language="python")

# Paso 1: Importar librerías
if st.button("📌 Paso 1: Importar librerías"):
    st.code("""
import numpy as np
import matplotlib.pyplot as plt
""", language="python")
    st.write("""
- **`numpy`**: Nos permite manejar datos numéricos y generar números aleatorios.
- **`matplotlib.pyplot`**: Se usa para graficar la caminata.
""")

# Paso 2: Definir parámetros
if st.button("⚙️ Paso 2: Definir parámetros"):
    st.code("""
n_steps = 1000  # Número total de pasos
step_size = 1   # Distancia de cada paso
""", language="python")
    st.write("""
Aquí definimos dos variables clave:
- **`n_steps`**: Es el número total de pasos que tomará el caminante (1000 en este caso).
- **`step_size`**: Es la distancia de cada paso (1 unidad).  
Esto significa que el caminante puede moverse **1 unidad a la izquierda o a la derecha** en cada paso.
""")

# Paso 3: Generar pasos aleatorios
if st.button("🎲 Paso 3: Generar pasos aleatorios"):
    st.code("""
steps = np.random.choice([-1, 1], size=n_steps) * step_size
""", language="python")
    st.write("""
- **`np.random.choice([-1, 1], size=n_steps)`**:  
  Esta función genera una lista de `n_steps` valores que pueden ser **-1** o **+1**, simulando la caminata aleatoria.
- **Multiplicamos por `step_size`** para asegurarnos de que cada paso tenga la distancia correcta.  
Así, obtenemos una lista de pasos aleatorios donde:
  - `-1` significa un paso a la izquierda.
  - `+1` significa un paso a la derecha.
""")

# Paso 4: Calcular la posición en cada paso
if st.button("📈 Paso 4: Calcular la posición acumulada"):
    st.code("""
positions = np.cumsum(steps)
""", language="python")
    st.write("""
- **`np.cumsum(steps)`**:  
  Calcula la **suma acumulada** de los pasos. Esto nos dice en qué posición está el caminante después de cada paso.  
Ejemplo:
  - Si los pasos son `[-1, +1, +1, -1, -1]`, las posiciones acumuladas serán `[-1, 0, 1, 0, -1]`.  
  - Se observa cómo el caminante se mueve a la izquierda y a la derecha con cada paso.
""")

# Paso 5: Graficar la caminata aleatoria
if st.button("📊 Paso 5: Graficar la caminata"):
    st.code("""
plt.figure(figsize=(10, 6))
plt.plot(positions, label='Caminata Aleatoria')
plt.xlabel('Número de Pasos')
plt.ylabel('Posición')
plt.title('Caminata Aleatoria en 1D')
plt.legend()
plt.grid(True)
plt.show()
""", language="python")
    st.write("""
Esta sección usa **matplotlib** para visualizar la caminata:
- **`plt.plot(positions)`** dibuja la trayectoria del caminante.
- **`plt.xlabel` y `plt.ylabel`** agregan etiquetas a los ejes.
- **`plt.title`** coloca un título a la gráfica.
- **`plt.legend()`** agrega una leyenda para identificar la línea.
- **`plt.grid(True)`** muestra una cuadrícula en la gráfica.  
Al final, la gráfica nos muestra cómo el caminante se mueve aleatoriamente con el tiempo.
""")

# Ejecutar todo el código y mostrar la gráfica
if st.button("🚀 Paso 6: Ejecutar Código Completo"):
    # Generar datos
    n_steps = 1000
    step_size = 1
    steps = np.random.choice([-1, 1], size=n_steps) * step_size
    positions = np.cumsum(steps)

    # Crear gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(positions, label="Caminata Aleatoria", color='blue')
    ax.set_xlabel("Número de Pasos")
    ax.set_ylabel("Posición")
    ax.set_title("Caminata Aleatoria en 1D")
    ax.legend()
    ax.grid(True)

    # Mostrar en Streamlit
    st.pyplot(fig)

    st.write("""
🔍 **Observaciones de la caminata aleatoria:**  
- La línea representa la posición del caminante a medida que avanza.  
- Algunas veces el caminante se mueve en una dirección por un tiempo antes de cambiar.  
- La caminata es completamente aleatoria, por lo que la trayectoria cambia cada vez que ejecutas el código.  
    """)

