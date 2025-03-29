import streamlit as st
import numpy as np
from hmmlearn import hmm

# Configuración de la aplicación
st.set_page_config(page_title="Explicación HMM - Predicción del Clima", layout="wide")
st.title("📊 Explicación Interactiva del Modelo HMM para Predicción del Clima")

# Introducción Detallada
st.write("""
## 📝 Introducción
Este código implementa un **Modelo Oculto de Markov (HMM)** para predecir el clima basado en observaciones de humedad.

### 🔍 ¿Qué diferencia este modelo de los anteriores?
- **Utiliza observaciones de humedad (seco o húmedo) para inferir el clima real (soleado, nublado, lluvioso).**
- **Predice el estado climático del día siguiente basado en probabilidades de transición.**
- **Usa un enfoque probabilístico sin aprendizaje automático adicional.**

### 📌 ¿Cómo funciona?
1. Se definen los estados ocultos (clima) y las observaciones (humedad).
2. Se establece la matriz de transición y de emisión del modelo HMM.
3. Se entrena el modelo con datos históricos de humedad.
4. Se predicen los estados ocultos más probables basados en las observaciones.
5. Se estima el estado climático del día siguiente.
""")

# Definir variables globales
states = np.array(["soleado", "nublado", "lluvioso"])
obs_names = np.array(["seco", "húmedo"])

# Crear el modelo globalmente
model = hmm.MultinomialHMM(n_components=3, n_iter=100)
model.startprob_ = np.array([0.6, 0.3, 0.1])
model.transmat_ = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.4, 0.3],
    [0.2, 0.3, 0.5]
])
model.emissionprob_ = np.array([
    [0.8, 0.2],
    [0.4, 0.6],
    [0.1, 0.9]
])

if st.button("📈 Paso 5: Entrenar el Modelo con Observaciones"):
    st.code("""
observations = np.array([0, 1, 0, 1, 1, 0, 0, 1])
model.fit(observations.reshape(-1, 1))
    """, language="python")
    st.write("Se entrena el modelo con una secuencia de observaciones de humedad.")

if st.button("🔍 Paso 6: Predecir Estados Ocultos"):
    observations = np.array([0, 1, 0, 1, 1, 0, 0, 1])
    model.fit(observations.reshape(-1, 1))
    hidden_states = model.predict(observations.reshape(-1, 1))
    
    st.code("""
hidden_states = model.predict(observations.reshape(-1, 1))
    """, language="python")
    st.write("Se predicen los estados ocultos más probables (clima real) a partir de las observaciones de humedad.")

if st.button("🚀 Paso 7: Predicción para el Próximo Día"):
    observations = np.array([0, 1, 0, 1, 1, 0, 0, 1])
    model.fit(observations.reshape(-1, 1))
    hidden_states = model.predict(observations.reshape(-1, 1))
    
    last_state = hidden_states[-1]
    next_state_prob = model.transmat_[last_state]
    predicted_next_state = np.argmax(next_state_prob)
    
    next_observation_prob = model.emissionprob_[predicted_next_state]
    predicted_next_observation = np.argmax(next_observation_prob)
    
    st.write("### 🔥 Resultados de la Predicción:")
    st.write(f"**Estado oculto predicho para mañana:** {states[predicted_next_state]}")
    st.write(f"**Observación predicha para mañana:** {obs_names[predicted_next_observation]}")