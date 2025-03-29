import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Título de la app
st.title("Simulación de Resistencia Estructural de una Viga")

st.markdown("""
### 📌 Introducción
Este modelo usa el **Método de Elementos Finitos (FEM)** para calcular la deformación de una viga bajo carga. Se consideran:
- **Ecuaciones de equilibrio** de la mecánica de materiales.
- **Desplazamientos y tensiones** en cada nodo de la viga.
- **Resultados visuales** para interpretar la resistencia estructural.

Modifica los parámetros y observa cómo cambia la deformación.
""")

st.markdown("### 📖 Modelo Matemático (Cálculo de momentos flectores en vigas:)")

st.latex(r"EI \frac{d^4 w}{dx^4} = q(x)")

st.markdown("""
Donde:
- \( E \) es el módulo de Young (rigidez del material).
- \( I \) es el momento de inercia de la sección transversal.
- \( w(x) \) es la deformación de la viga en la posición \( x \).
- \( q(x) \) es la carga distribuida a lo largo de la viga.

Para resolver esta ecuación, se discretiza la viga en \( n \) nodos y se usa el **Método de Elementos Finitos (FEM)** para obtener una solución aproximada.

La ecuación diferencial se convierte en un sistema de ecuaciones lineales mediante la discretización:""")

st.latex(r"K u = F")

st.markdown("""
Donde:
- \( K \) es la matriz de rigidez ensamblada de los elementos finitos.
- \( u \) es el vector de desplazamientos en cada nodo.
- \( F \) es el vector de fuerzas aplicadas.

La matriz de rigidez de un elemento finito de la viga es:""")

st.latex(r"k_{local} = \frac{EI}{dx^3} \begin{bmatrix} 12 & -6dx \\ -6dx & 4dx^2 \end{bmatrix}")
st.markdown("""
Y la matriz global de rigidez se construye ensamblando estas matrices locales en la estructura completa.
""")

st.markdown("### 🔍 Explicación del Código")
st.markdown("""
El código está compuesto por varias secciones:

1. **Definición de parámetros**: Se utilizan `st.slider` para permitir al usuario seleccionar los valores de los parámetros físicos de la viga.
2. **Discretización**: Se divide la viga en `n` nodos y se calculan los puntos en la longitud.
3. **Construcción de la Matriz de Rigidez**:
   - Se inicializa una matriz `K` de ceros.
   - Se ensambla `K` usando la ecuación de elementos finitos.
4. **Condiciones de frontera**: Se fija el primer nodo para simular un soporte fijo.
5. **Resolución del sistema**: Se utiliza `np.linalg.solve(K, F_vector)` para calcular la deformación `u`.
6. **Visualización**: Se genera un gráfico con `matplotlib` para representar el desplazamiento de la viga.

Estos pasos permiten simular y analizar la respuesta estructural de la viga bajo diferentes condiciones de carga.
""")

st.markdown("""
#### 1️⃣ Definición de Parámetros
Se establecen los valores de los parámetros físicos de la viga usando `st.slider`.
""")
st.code("""
E = st.slider("Módulo de Young (Pa)", 1e9, 300e9, 200e9)
I = st.slider("Momento de inercia (m^4)", 1e-6, 1e-3, 0.0001)
L = st.slider("Longitud de la viga (m)", 1, 20, 10)
n = st.slider("Número de nodos", 5, 50, 10)
F = st.slider("Fuerza aplicada (N)", -10000, 10000, -1000)
""", language="python")

st.markdown("""
#### 2️⃣ Discretización de la Viga
Se divide la viga en `n` nodos para aplicar el método de elementos finitos.
""")
st.code("""
dx = L / (n - 1)
x = np.linspace(0, L, n)
""", language="python")

st.markdown("""
#### 3️⃣ Construcción de la Matriz de Rigidez
Se inicializa una matriz de rigidez `K` y un vector de fuerzas `F_vector`.
""")
st.code("""
K = np.zeros((n, n))
F_vector = np.zeros(n)
F_vector[-1] = F  # Fuerza aplicada en el último nodo
""", language="python")

st.markdown("""
Se ensambla la matriz de rigidez `K` usando el método de elementos finitos.
""")
st.code("""
for i in range(n - 1):
    k_local = (E * I / dx**3) * np.array([[12, -6*dx],
                                          [-6*dx, 4*dx**2]])
    K[i:i+2, i:i+2] += k_local
""", language="python")

st.markdown("""
#### 4️⃣ Aplicación de Condiciones de Frontera
El primer nodo se fija en `x=0` para simular un soporte fijo.
""")
st.code("""
K[0, :] = K[:, 0] = 0
K[0, 0] = 1
F_vector[0] = 0
""", language="python")

st.markdown("""
#### 5️⃣ Resolución del Sistema
Se usa `np.linalg.solve(K, F_vector)` para obtener los desplazamientos `u`.
""")
st.code("""
u = np.linalg.solve(K, F_vector)
""", language="python")

st.markdown("""
#### 6️⃣ Visualización de Resultados
Se grafican los desplazamientos de la viga bajo la carga aplicada.
""")
st.code("""
fig, ax = plt.subplots()
ax.plot(x, u, marker='o', linestyle='-', color='b')
ax.set_xlabel("Longitud de la viga (m)")
ax.set_ylabel("Desplazamiento (m)")
ax.set_title("Deformación de la viga bajo carga")
ax.grid()
st.pyplot(fig)
""", language="python")

st.markdown("### 🔍 Observaciones:")
st.markdown("""
- Aumentar **E** o **I** reduce la deformación.
- Aumentar la **carga (F)** incrementa la deformación.
- Más **nodos** mejoran la precisión.
""")


# Entrada de datos
E = st.slider("Módulo de Young (Pa)", 1e9, 300e9, 200e9)
I = st.slider("Momento de inercia (m^4)", 1e-6, 1e-3, 0.0001)
L = st.slider("Longitud de la viga (m)", 1, 20, 10)
n = st.slider("Número de nodos", 5, 50, 10)
F = st.slider("Fuerza aplicada (N)", -10000, 10000, -1000)

# Discretización de la viga
dx = L / (n - 1)
x = np.linspace(0, L, n)

# Matriz de rigidez global
K = np.zeros((n, n))
F_vector = np.zeros(n)
F_vector[-1] = F  # Fuerza aplicada en el último nodo

# Ensamblado de la matriz de rigidez
for i in range(n - 1):
    k_local = (E * I / dx**3) * np.array([[12, -6*dx],
                                          [-6*dx, 4*dx**2]])
    
    K[i:i+2, i:i+2] += k_local

# Aplicar condiciones de frontera (nodo fijo en x=0)
K[0, :] = K[:, 0] = 0
K[0, 0] = 1
F_vector[0] = 0

# Resolver el sistema de ecuaciones
u = np.linalg.solve(K, F_vector)

# Graficar los desplazamientos
fig, ax = plt.subplots()
ax.plot(x, u, marker='o', linestyle='-', color='b')
ax.set_xlabel("Longitud de la viga (m)")
ax.set_ylabel("Desplazamiento (m)")
ax.set_title("Deformación de la viga bajo carga")
ax.grid()
st.pyplot(fig)

st.markdown("### 🔍 Observaciones:")
st.markdown("""
- Aumentar **E** o **I** reduce la deformación.
- Aumentar la **carga (F)** incrementa la deformación.
- Más **nodos** mejoran la precisión.
""")
