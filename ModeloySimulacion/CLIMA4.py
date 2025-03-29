import numpy as np
from hmmlearn import hmm

# estados del clima (0: soleado, 1: nublado, 2: lluvioso)
# datos de observación (0: seco, 1: húmedo)
observations = np.array([0, 1, 0, 1, 1, 0, 0, 1])

# Definimos los nombres de los estados y observaciones
states = np.array(["soleado", "nublado", "lluvioso"])
obs_names = np.array(["seco", "húmedo"])

# Definición del modelo oculto de Markov
model = hmm.MultinomialHMM(n_components=3, n_iter=100)

# Matriz de transición entre estados 
model.startprob_ = np.array([0.6, 0.3, 0.1])#inicial
model.transmat_ = np.array([[0.7, 0.2, 0.1],
                            [0.3, 0.4, 0.3],
                            [0.2, 0.3, 0.5]])

# Matriz de probabilidad de emisión (observaciones dadas por estados)
#Define la matriz de emisión que relaciona estados ocultos con observaciones.
model.emissionprob_ = np.array([[0.8, 0.2],
                                [0.4, 0.6],
                                [0.1, 0.9]])

# Entrenamiento del modelo con las observaciones
model.fit(observations.reshape(-1, 1))

# Predicción de estados ocultos
hidden_states = model.predict(observations.reshape(-1, 1))

print("Observaciones:", [obs_names[o] for o in observations])
print("Estados ocultos predichos:", [states[s] for s in hidden_states])

# Predicción para el próximo día
# Utilizamos el último estado oculto predicho y la matriz de transición
last_state = hidden_states[-1]
next_state_prob = model.transmat_[last_state]

# El estado con la mayor probabilidad es el predicho
predicted_next_state = np.argmax(next_state_prob)
print(f"Estado oculto predicho para mañana: {states[predicted_next_state]}")

# Probabilidad de observaciones dado el estado predicho
next_observation_prob = model.emissionprob_[predicted_next_state]

# La observación con la mayor probabilidad es la predicha
predicted_next_observation = np.argmax(next_observation_prob)
print(f"Observación predicha para mañana: {obs_names[predicted_next_observation]}")
