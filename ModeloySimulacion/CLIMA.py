import numpy as np
from hmmlearn import hmm

# Estados ocultos (Soleado, Nublado, Lluvioso)
states = ["Soleado", "Nublado", "Lluvioso"]
n_states = len(states)

# Observaciones (Temperatura: alta, media, baja)
observations = ["Alta", "Media", "Baja"]
n_observations = len(observations)

# Matriz de transición de estados
transition_matrix = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.4, 0.3],
    [0.2, 0.3, 0.5]
])

# Matriz de emisión (probabilidad de observación dado el estado)
emission_matrix = np.array([
    [0.6, 0.3, 0.1],  # Soleado
    [0.3, 0.4, 0.3],  # Nublado
    [0.1, 0.3, 0.6]   # Lluvioso
])

# Probabilidades iniciales
start_probabilities = np.array([0.5, 0.3, 0.2])

# Crear el modelo HMM
model = hmm.MultinomialHMM(n_components=n_states)
model.startprob_ = start_probabilities
model.transmat_ = transition_matrix
model.emissionprob_ = emission_matrix

# Entrenamiento con datos historicos

# Datos de observación (codificados: Alta=0, Media=1, Baja=2)
observations_data = np.array([[0, 1, 2, 1, 0, 1, 2]]).T

# Entrenar el modelo (si tenemos datos más extensos, podemos usarlos aquí)
model.fit(observations_data)

# Prediccion del clima

# Nuevas observaciones (Temperatura: alta, media, baja)
new_observations = np.array([[0, 1, 2]]).T  # Supongamos observaciones recientes

# Predecir los estados ocultos (clima)
predicted_states = model.predict(new_observations)

# Mapeo de estados a nombres de clima
predicted_climate = [states[state] for state in predicted_states]

print("Observaciones:", new_observations.T[0])
print("Clima Predicho:", predicted_climate)
