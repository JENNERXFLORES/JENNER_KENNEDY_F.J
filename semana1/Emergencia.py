import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
num_agentes = 50 
tamano_edificio = (20, 20)
salidas = [(0, 10), (19, 10)]
class Agente:
    def __init__(self, id_agente):
        self.id = id_agente
        self.posicion = (random.randint(0, tamano_edificio[0]-1), random.randint(0, tamano_edificio[1]-1))
        self.ruta_escape = self.calcular_ruta_escape()
        self.ha_escapado = False

    def calcular_ruta_escape(self):
        return random.choice(salidas) 
    def mover(self):
        if not self.ha_escapado:
            x_diff = np.sign(self.ruta_escape[0] - self.posicion[0])
            y_diff = np.sign(self.ruta_escape[1] - self.posicion[1])
            self.posicion = (self.posicion[0] + x_diff, self.posicion[1] + y_diff)
            if self.posicion == self.ruta_escape:
                self.ha_escapado = True
                return True
def inicializar_simulacion():
    agentes = [Agente(i) for i in range(num_agentes)]
    return agentes
def actualizar(frame, agentes, edificio_imagen):
    for agente in agentes:
        agente.mover()

    edificio = np.zeros(tamano_edificio)
    for agente in agentes:
        edificio[agente.posicion] += 1

    edificio_imagen.set_array(edificio)
    return edificio_imagen,
def obtenerEvacuados():
    agentes = [Agente(i) for i in range(num_agentes)]
    tiempo_salida = {}
    for time_step in range(100):
        for agente in agentes:
            if not agente.ha_escapado:
                if agente.mover():
                    tiempo_salida[agente.id] = time_step

    agentes_evacuados = sum(agente.ha_escapado for agente in agentes)

    if agentes_evacuados > 0:
        tiempo_promedio = sum(tiempo_salida.values()) / agentes_evacuados
    else:
        tiempo_promedio = 0
    print(f"Total de agentes evacuados: {agentes_evacuados}")
    print(f"Tiempo promedio de evacuación: {tiempo_promedio:.2f} pasos de tiempo")

def configurar_visualizacion():
    fig, ax = plt.subplots()
    edificio = np.zeros(tamano_edificio)
    edificio_imagen = ax.imshow(edificio, cmap='cool', interpolation='nearest')
    plt.colorbar(edificio_imagen, ax=ax, label='Número de Agentes')
    ax.set_title('Simulación de Evacuación en Edificio')
    return fig, edificio_imagen

if __name__ == "__main__":
    agentes = inicializar_simulacion()
    obtenerEvacuados()
    fig, edificio_imagen = configurar_visualizacion()
    ani = animation.FuncAnimation(fig, actualizar, fargs=(agentes, edificio_imagen), frames=100, interval=200, blit=True)
    plt.show()
