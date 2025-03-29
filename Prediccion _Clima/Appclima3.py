import streamlit as st
import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder

# Configuración de la aplicación
st.set_page_config(page_title="Explicación HMM con LabelEncoder", layout="wide")
st.title("📊 Explicación Interactiva del Modelo HMM con Codificación de Datos")

# Introducción Detallada
st.write("""
## 📝 Introducción
Este código implementa un **Modelo Oculto de Markov (HMM)** con **codificación de datos categóricos** usando `LabelEncoder`.

### 🔍 ¿Qué diferencia este modelo del anterior?
- **Usa `LabelEncoder` para transformar datos categóricos (Soleado, Nublado, Lluvioso) en valores numéricos.**
- **Trabaja con datos históricos almacenados en un `DataFrame` de pandas.**
- **Predice el próximo estado climático basado en la secuencia observada.**

### 📌 ¿Cómo funciona?
1. Se define un conjunto de datos históricos del clima en un `DataFrame`.
2. Se usa `LabelEncoder` para convertir los estados en valores numéricos.
3. Se entrena un **Modelo Oculto de Markov (HMM)** con estos datos.
4. Se usa el **algoritmo de Viterbi** para encontrar la secuencia más probable de estados.
5. Finalmente, se predice el próximo estado del clima.
""")

if st.button("📌 Paso 1: Importar Librerías"):
    st.code("""
import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder
    """, language="python")
    st.write("Este código usa librerías adicionales como:")
    st.write("- **`pandas`**: Para manejar datos en formato tabular.")
    st.write("- **`sklearn.preprocessing.LabelEncoder`**: Para convertir datos categóricos en valores numéricos.")

if st.button("📊 Paso 2: Simular Datos Históricos"):
    st.code("""
data = {
    'Estado': ['Soleado', 'Nublado', 'Lluvioso', 'Soleado', 'Nublado', 'Lluvioso', 'Lluvioso', 'Soleado', 'Soleado']
}
df = pd.DataFrame(data)
    """, language="python")
    st.write("Se crea un conjunto de datos históricos del clima en un `DataFrame` de pandas.")

if st.button("🔄 Paso 3: Codificar los Estados del Clima"):
    st.code("""
le = LabelEncoder()
df['Estado_encoded'] = le.fit_transform(df['Estado'])
X = df['Estado_encoded'].values.reshape(-1, 1)
    """, language="python")
    st.write("Se usa `LabelEncoder` para transformar las etiquetas de clima en valores numéricos.")

if st.button("🤖 Paso 4: Configurar el Modelo HMM"):
    st.code("""
model = hmm.MultinomialHMM(n_components=3, n_iter=100)
model.fit(X)
    """, language="python")
    st.write("Se configura un **Modelo Oculto de Markov** con 3 estados ocultos y se entrena con los datos históricos.")

if st.button("🔍 Paso 5: Predecir el Próximo Estado del Clima"):
    st.code("""
logprob, next_state = model.decode(X, algorithm="viterbi")
predicted_state = model.predict([[next_state[-1]]])
predicted_climate = le.inverse_transform(predicted_state)
    """, language="python")
    st.write("Se usa el **algoritmo de Viterbi** para determinar la secuencia de estados más probable.")
    st.write("Finalmente, se predice el próximo estado del clima basándose en la secuencia observada.")

if st.button("🚀 Paso 6: Ejecutar Predicción en Vivo"):
    data = {
        'Estado': ['Soleado', 'Nublado', 'Lluvioso', 'Soleado', 'Nublado', 'Lluvioso', 'Lluvioso', 'Soleado', 'Soleado']
    }
    df = pd.DataFrame(data)
    
    le = LabelEncoder()
    df['Estado_encoded'] = le.fit_transform(df['Estado'])
    X = df['Estado_encoded'].values.reshape(-1, 1)
    
    model = hmm.MultinomialHMM(n_components=3, n_iter=100)
    model.fit(X)
    
    logprob, next_state = model.decode(X, algorithm="viterbi")
    predicted_state = model.predict([[next_state[-1]]])
    predicted_climate = le.inverse_transform(predicted_state)
    
    st.write("### 🔥 Resultado de la Predicción:")
    st.write(f"**El próximo estado del clima predicho es:** {predicted_climate[0]}")
