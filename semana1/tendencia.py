import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

st.title("Simulación de Tendencias de Mercado y Políticas Económicas")

# Introducción
st.markdown("""
### Introducción
El comportamiento del mercado y las políticas económicas juegan un papel clave en la evolución de los precios y la estabilidad económica. 
Este modelo matemático permite analizar cómo diferentes factores influyen en la dinámica de precios en un mercado en el tiempo. 

Se basa en principios de oferta y demanda, donde el precio evoluciona según la diferencia entre ambas.
En este caso, la demanda depende del precio, el gasto público, la masa monetaria y la inversión privada, mientras que la oferta está influenciada por el precio y los costos de producción. 

El modelo emplea una ecuación diferencial para describir la evolución del precio en función del tiempo.
""")

# Mostrar ecuaciones matemáticas en LaTeX
st.markdown("""
### Modelo Matemático
#### Ecuaciones Base
**Demanda:**
$$ D_t = a - b P_t + c G_t + d M_t + e I_t $$

**Oferta:**
$$ S_t = f + g P_t - h C_t $$

**Equilibrio de Mercado:**
$$ D_t = S_t $$

**Evolución del Precio:**
$$ \dfrac{dP}{dt} = k (D_t - S_t) $$

Donde:
- \( D_t \): Demanda en el tiempo \( t \)
- \( S_t \): Oferta en el tiempo \( t \)
- \( P_t \): Precio en el tiempo \( t \)
- \( G_t \): Gasto del gobierno
- \( M_t \): Masa monetaria
- \( I_t \): Inversión privada
- \( C_t \): Costo de producción
- \( k \): Factor de ajuste de precios
- \( a, f \): Componentes autónomos de la demanda y oferta
- \( b, c, d, e, g, h \): Sensibilidades de la demanda y oferta ante diferentes factores
""")

st.markdown("""
### Explicación del Código Fuente
Este código implementa un modelo de simulación en Streamlit para visualizar la evolución del precio de un mercado bajo distintos parámetros económicos.

1. **Definición del Modelo:** Se establecen ecuaciones de oferta y demanda para determinar la evolución del precio.
2. **Interfaz de Usuario:** Se usan sliders en Streamlit para ajustar los parámetros del modelo.
3. **Resolución Numérica:** Se emplea `odeint` de SciPy para resolver la ecuación diferencial del precio.
4. **Visualización:** Se genera una gráfica en Matplotlib que muestra la evolución del precio en el tiempo.
""")

st.markdown("""
### Código Fuente
```python
# Importamos las bibliotecas necesarias para la simulación
import streamlit as st  # Para crear una interfaz interactiva con el usuario
import numpy as np  # Para cálculos numéricos y manejo de arreglos
import matplotlib.pyplot as plt  # Para graficar la evolución de precios
from scipy.integrate import odeint  # Para resolver ecuaciones diferenciales

# Título principal de la aplicación
st.title("Simulación de Tendencias de Mercado y Políticas Económicas")

# Sección de la barra lateral para configurar parámetros del modelo
st.sidebar.header("Parámetros del Modelo")

# Parámetros de la función de DEMANDA
a = st.sidebar.slider("Demanda autónoma (a)", 50, 200, 100)  
# Representa la demanda base cuando el precio es cero (factores como la necesidad básica de un producto).

b = st.sidebar.slider("Sensibilidad de la demanda al precio (b)", 0.5, 3.0, 1.5)  
# Indica cuánto disminuye la demanda cuando el precio sube.

c = st.sidebar.slider("Sensibilidad de la demanda al gasto público (c)", 0.1, 1.0, 0.5)  
# Cuánto aumenta la demanda cuando el gobierno incrementa su gasto.

d = st.sidebar.slider("Sensibilidad de la demanda a la masa monetaria (d)", 0.1, 1.0, 0.3)  
# Indica cómo el aumento de dinero en circulación afecta la demanda.

e = st.sidebar.slider("Sensibilidad de la demanda a la inversión privada (e)", 0.1, 1.0, 0.2)  
# Representa cuánto influye la inversión privada en el aumento de la demanda.

# Parámetros de la función de OFERTA
f = st.sidebar.slider("Oferta autónoma (f)", 20, 100, 50)  
# Cantidad de productos ofrecidos en el mercado sin considerar el precio.

g = st.sidebar.slider("Sensibilidad de la oferta al precio (g)", 0.5, 2.0, 1.2)  
# Indica cómo reacciona la oferta ante cambios en el precio (a mayor precio, mayor oferta).

h = st.sidebar.slider("Sensibilidad de la oferta al costo de producción (h)", 0.1, 1.0, 0.4)  
# Mide cómo los costos de producción afectan la oferta (si aumentan los costos, la oferta disminuye).

# Factores externos que influyen en el mercado
G = st.sidebar.slider("Gasto del Gobierno (G)", 0, 50, 20)  
# Representa el gasto público, que puede aumentar la demanda al incentivar la economía.

M = st.sidebar.slider("Masa Monetaria (M)", 0, 100, 30)  
# Indica la cantidad de dinero en circulación, lo que puede afectar el consumo.

I = st.sidebar.slider("Inversión Privada (I)", 0, 100, 40)  
# Representa la inversión privada, que impulsa la producción y el empleo.

C = st.sidebar.slider("Costo de Producción (C)", 0, 50, 15)  
# Indica el costo de fabricar los productos, lo que influye en la oferta.

k = st.sidebar.slider("Factor de ajuste de precios (k)", 0.01, 0.5, 0.1)  
# Controla la velocidad con la que los precios se ajustan según la diferencia entre demanda y oferta.

# Función que modela la dinámica del mercado mediante una ecuación diferencial
def market_dynamics(P, t):
    ""
    Calcula la tasa de cambio del precio en función de la oferta y la demanda.
    - P: Precio en el tiempo t
    - t: Tiempo
    ""
    D = a - b * P + c * G + d * M + e * I  # Función de la demanda agregada
    S = f + g * P - h * C  # Función de la oferta agregada
    dPdt = k * (D - S)  # Cambio del precio basado en el desequilibrio entre demanda y oferta
    return dPdt

# Definimos el tiempo para la simulación
tiempo = np.linspace(0, 50, 500)  # 500 puntos en un rango de 0 a 50 unidades de tiempo

# Precio inicial del producto
P_inicial = 10  

# Resolvemos la ecuación diferencial utilizando odeint
P = odeint(market_dynamics, P_inicial, tiempo)

# Creamos una gráfica para mostrar la evolución del precio
fig, ax = plt.subplots()
ax.plot(tiempo, P, label='Evolución del Precio', color='b')  # Curva del precio a lo largo del tiempo
ax.set_xlabel('Tiempo')  # Etiqueta del eje X
ax.set_ylabel('Precio')  # Etiqueta del eje Y
ax.set_title('Simulación de Tendencias de Mercado')  # Título del gráfico
ax.legend()  # Muestra la leyenda del gráfico
ax.grid(True)  # Agrega una cuadrícula para facilitar la lectura de los datos

# Mostramos la gráfica en la aplicación Streamlit
st.pyplot(fig)
```
""")

st.title("Simulación de Tendencias de Mercado y Políticas Económicas")

# Parámetros ajustables y simulación...
st.sidebar.header("Parámetros del Modelo")

# Parámetros ajustables
a = st.sidebar.slider("Demanda autónoma (a)", 50, 200, 100)
b = st.sidebar.slider("Sensibilidad de la demanda al precio (b)", 0.5, 3.0, 1.5)
c = st.sidebar.slider("Sensibilidad de la demanda al gasto público (c)", 0.1, 1.0, 0.5)
d = st.sidebar.slider("Sensibilidad de la demanda a la masa monetaria (d)", 0.1, 1.0, 0.3)
e = st.sidebar.slider("Sensibilidad de la demanda a la inversión privada (e)", 0.1, 1.0, 0.2)
f = st.sidebar.slider("Oferta autónoma (f)", 20, 100, 50)
g = st.sidebar.slider("Sensibilidad de la oferta al precio (g)", 0.5, 2.0, 1.2)
h = st.sidebar.slider("Sensibilidad de la oferta al costo de producción (h)", 0.1, 1.0, 0.4)
G = st.sidebar.slider("Gasto del Gobierno (G)", 0, 50, 20)
M = st.sidebar.slider("Masa Monetaria (M)", 0, 100, 30)
I = st.sidebar.slider("Inversión Privada (I)", 0, 100, 40)
C = st.sidebar.slider("Costo de Producción (C)", 0, 50, 15)
k = st.sidebar.slider("Factor de ajuste de precios (k)", 0.01, 0.5, 0.1)

# Definir la ecuación diferencial
def market_dynamics(P, t):
    D = a - b * P + c * G + d * M + e * I
    S = f + g * P - h * C
    dPdt = k * (D - S)
    return dPdt

# Simulación
tiempo = np.linspace(0, 50, 500)
P_inicial = 10
P = odeint(market_dynamics, P_inicial, tiempo)

# Gráfica
fig, ax = plt.subplots()
ax.plot(tiempo, P, label='Evolución del Precio', color='b')
ax.set_xlabel('Tiempo')
ax.set_ylabel('Precio')
ax.set_title('Simulación de Tendencias de Mercado')
ax.legend()
ax.grid(True)

st.pyplot(fig)