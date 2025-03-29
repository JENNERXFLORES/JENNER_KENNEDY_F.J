import streamlit as st
import numpy as np
from hmmlearn import hmm

# Configuración de la aplicación
st.set_page_config(page_title="Explicación HMM - Predicción del Clima", layout="wide")
st.title("📊 Explicación Interactiva del Modelo Oculto de Markov (HMM) para Predicción del Clima")

# Introducción Detallada
st.write("""
## 📝 Introducción
Este código implementa un **Modelo Oculto de Markov (HMM)** para la predicción del clima.

### 🔍 ¿Qué es un Modelo Oculto de Markov?
Un **HMM** es un modelo matemático que representa un sistema con estados ocultos (no observables) que evolucionan con el tiempo. En nuestro caso:
- **Estados ocultos:** Representan el clima real (Soleado, Nublado, Lluvioso).
- **Observaciones:** Son los datos que podemos medir (Temperatura Alta, Media, Baja).
- **Objetivo:** Dado un conjunto de observaciones, inferir la secuencia más probable de estados ocultos.

### 🎯 ¿Cómo se distingue este código de los otros modelos?
- **No usa aprendizaje automático** como `RandomForestClassifier`.
- **No predice el futuro directamente**, sino que ajusta los estados ocultos en función de las observaciones.
- Utiliza **el algoritmo de Viterbi**, que permite encontrar la secuencia de estados más probable dado un conjunto de observaciones.

### 📌 ¿Cómo funciona?
1. Definimos los **estados ocultos** y las **observaciones**.
2. Especificamos **matrices de probabilidad** para modelar la transición entre estados y la relación entre estados y observaciones.
3. Creamos el **Modelo HMM** y lo entrenamos con datos históricos.
4. Aplicamos el **algoritmo de Viterbi** para predecir la secuencia más probable de estados ocultos.
5. Finalmente, usamos el modelo para hacer predicciones en tiempo real.
""")

# Definición del Modelo HMM
def definir_modelo():
    global model, states, observations, transition_matrix, emission_matrix
    
    states = ["Soleado", "Nublado", "Lluvioso"]
    observations = ["Alta", "Media", "Baja"]
    
    transition_matrix = np.array([
        [0.7, 0.2, 0.1],
        [0.3, 0.4, 0.3],
        [0.2, 0.3, 0.5]
    ])
    
    emission_matrix = np.array([
        [0.6, 0.3, 0.1],
        [0.3, 0.4, 0.3],
        [0.1, 0.3, 0.6]
    ])
    
    model = hmm.MultinomialHMM(n_components=len(states))
    model.startprob_ = np.array([0.5, 0.3, 0.2])
    model.transmat_ = transition_matrix
    model.emissionprob_ = emission_matrix
    
if st.button("📌 Paso 1: Importar librerías"):
    st.code("""
import numpy as np
from hmmlearn import hmm
    """, language="python")
    st.write("Estas librerías son esenciales para nuestra implementación:")
    st.write("- **`numpy`**: Nos permite manejar matrices y realizar cálculos numéricos.")
    st.write("- **`hmmlearn`**: Proporciona herramientas para trabajar con Modelos Ocultos de Markov.")

definir_modelo()

if st.button("⚙️ Paso 2: Definir Estados y Observaciones"):
    st.code(f"""
states = {states}
observations = {observations}
    """, language="python")
    st.write("Definimos los componentes clave del modelo:")
    st.write("- **Estados ocultos:** Representan el clima real que queremos modelar.")
    st.write("- **Observaciones:** Son los datos que recopilamos y usamos para inferir el clima.")

if st.button("📊 Paso 3: Definir Matrices de Transición y Emisión"):
    st.code(f"""
transition_matrix = np.array({transition_matrix.tolist()})
emission_matrix = np.array({emission_matrix.tolist()})
    """, language="python")
    st.write("Las matrices de probabilidad nos ayudan a modelar cómo cambia el clima:")
    st.write("- **Matriz de transición:** Describe la probabilidad de moverse de un estado a otro.")
    st.write("- **Matriz de emisión:** Indica la probabilidad de observar una temperatura dada un estado climático.")

if st.button("🤖 Paso 4: Crear el Modelo HMM"):
    st.code("""
model = hmm.MultinomialHMM(n_components=len(states))
model.startprob_ = np.array([0.5, 0.3, 0.2])
model.transmat_ = transition_matrix
model.emissionprob_ = emission_matrix
    """, language="python")
    st.write("Aquí configuramos nuestro modelo HMM con los parámetros definidos.")

if st.button("🔍 Paso 5: Entrenar y Predecir el Clima"):
    observations_data = np.array([[0, 1, 2, 1, 0, 1, 2]]).T
    model.fit(observations_data)
    
    new_observations = np.array([[0, 1, 2]]).T
    predicted_states = model.predict(new_observations)
    predicted_climate = [states[state] for state in predicted_states]
    
    st.write("Entrenamos el modelo con datos históricos y predecimos los estados ocultos más probables.")

if st.button("🚀 Paso 6: Ejecutar Predicción en Vivo"):
    observations_data = np.array([[0, 1, 2, 1, 0, 1, 2]]).T
    model.fit(observations_data)
    
    new_observations = np.array([[0, 1, 2]]).T
    predicted_states = model.predict(new_observations)
    predicted_climate = [states[state] for state in predicted_states]
    
    st.write("### 🔥 Resultado de la Predicción:")
    st.write(f"**Observaciones:** {[observations[o] for o in new_observations.T[0]]}")
    st.write(f"**Estados Ocultos Predichos (Clima):** {predicted_climate}")

