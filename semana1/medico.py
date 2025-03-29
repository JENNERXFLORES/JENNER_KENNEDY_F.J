import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

st.title("Simulación de Propagación de Enfermedades")

# Introducción
st.markdown("""
### Introducción
Los modelos epidemiológicos son herramientas esenciales para comprender cómo se propagan las enfermedades en una población y evaluar la efectividad de diversas intervenciones de salud pública. 

En este modelo, analizaremos la evolución de una infección dentro de una población mediante un sistema de ecuaciones diferenciales.

El modelo considera la interacción entre células sanas, infectadas y virus en el tiempo.
""")

# Mostrar ecuaciones matemáticas en LaTeX
st.markdown("""
### Modelo Matemático
#### Ecuaciones Base

**Tasa de cambio de células sanas:**
$$ \dfrac{dS}{dt} = -\ beta S V $$

**Tasa de cambio de células infectadas:**
$$ \dfrac{dI}{dt} = \ beta S V - \delta I $$

**Tasa de cambio de virus:**
$$ \dfrac{dV}{dt} = p I - c V $$

Donde:
- \( S \): Células sanas
- \( I \): Células infectadas
- \( V \): Partículas virales
- \( \ beta \): Tasa de infección
- \( \delta \): Tasa de eliminación de células infectadas
- \( p \): Producción de virus por célula infectada
- \( c \): Tasa de eliminación del virus
""")

st.sidebar.header("Parámetros del Modelo")

# Parámetros ajustables
beta = st.sidebar.slider("Tasa de infección (β)", 0.0001, 0.01, 0.001)
delta = st.sidebar.slider("Tasa de eliminación de células infectadas (δ)", 0.1, 1.0, 0.5)
p = st.sidebar.slider("Producción de virus por célula infectada (p)", 1, 50, 10)
c = st.sidebar.slider("Tasa de eliminación del virus (c)", 0.1, 5.0, 1.0)

# Definir la ecuación diferencial
def infection_dynamics(y, t, beta, delta, p, c):
    S, I, V = y
    dSdt = -beta * S * V
    dIdt = beta * S * V - delta * I
    dVdt = p * I - c * V
    return [dSdt, dIdt, dVdt]

# Simulación
tiempo = np.linspace(0, 50, 500)
S0, I0, V0 = 1000, 10, 1  # Condiciones iniciales
y0 = [S0, I0, V0]
sol = odeint(infection_dynamics, y0, tiempo, args=(beta, delta, p, c))

# Gráfica
fig, ax = plt.subplots()
ax.plot(tiempo, sol[:, 0], label='Células Sanas', color='g')
ax.plot(tiempo, sol[:, 1], label='Células Infectadas', color='r')
ax.plot(tiempo, sol[:, 2], label='Partículas Virales', color='b')
ax.set_xlabel('Tiempo')
ax.set_ylabel('Cantidad')
ax.set_title('Simulación de Propagación de Enfermedades')
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.markdown("""
### Explicación del Código Fuente
Este código implementa un modelo epidemiológico en Streamlit para visualizar la evolución de una infección en una población celular.

1. **Definición del Modelo:** Se utilizan ecuaciones diferenciales para describir la interacción entre células sanas, infectadas y virus.
2. **Interfaz de Usuario:** Se permiten ajustes en los parámetros mediante sliders interactivos.
3. **Resolución Numérica:** Se usa `odeint` para resolver el sistema de ecuaciones.
4. **Visualización:** Se genera una gráfica con la evolución de cada componente en el tiempo.
""")

st.markdown("""
### Código Fuente
```python
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

st.title("Simulación de Propagación de Enfermedades")

st.sidebar.header("Parámetros del Modelo")

beta = st.sidebar.slider("Tasa de infección (β)", 0.0001, 0.01, 0.001)
delta = st.sidebar.slider("Tasa de eliminación de células infectadas (δ)", 0.1, 1.0, 0.5)
p = st.sidebar.slider("Producción de virus por célula infectada (p)", 1, 50, 10)
c = st.sidebar.slider("Tasa de eliminación del virus (c)", 0.1, 5.0, 1.0)

def infection_dynamics(y, t, beta, delta, p, c):
    S, I, V = y
    dSdt = -beta * S * V
    dIdt = beta * S * V - delta * I
    dVdt = p * I - c * V
    return [dSdt, dIdt, dVdt]

tiempo = np.linspace(0, 50, 500)
S0, I0, V0 = 1000, 10, 1
y0 = [S0, I0, V0]
sol = odeint(infection_dynamics, y0, tiempo, args=(beta, delta, p, c))

fig, ax = plt.subplots()
ax.plot(tiempo, sol[:, 0], label='Células Sanas', color='g')
ax.plot(tiempo, sol[:, 1], label='Células Infectadas', color='r')
ax.plot(tiempo, sol[:, 2], label='Partículas Virales', color='b')
ax.set_xlabel('Tiempo')
ax.set_ylabel('Cantidad')
ax.set_title('Simulación de Propagación de Enfermedades')
ax.legend()
ax.grid(True)

st.pyplot(fig)
```
""")