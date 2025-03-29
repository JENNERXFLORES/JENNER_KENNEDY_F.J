import simpy
import random

class Autobus:
    def __init__(self, env, nombre, ruta, horario):
        self.env = env
        self.nombre = nombre
        self.ruta = ruta
        self.horario = horario
        self.proceso = env.process(self.ejecutar())

    def ejecutar(self):
        while True:
            for estacion, tiempo_viaje in self.ruta:
                yield self.env.timeout(tiempo_viaje)
                print(f"{self.nombre} llegó a {estacion} a las {self.env.now:.2f}")

                # Simular abordaje y desembarque
                yield self.env.timeout(random.uniform(1, 3))

def generar_pasajeros(env, num_pasajeros, estaciones):
    for i in range(num_pasajeros):
        estacion = random.choice(estaciones)
        print(f"Pasajero {i} llegó a {estacion} a las {env.now:.2f}")
        yield env.timeout(random.uniform(1, 5))

def simular_sistema_de_transporte():
    env = simpy.Environment()

    # Definir la ruta y horario del autobús
    ruta = [("Estación A", 5), ("Estación B", 10), ("Estación C", 15)]
    horario = [0, 20, 40, 60]

    # Crear autobuses
    autobuses = [Autobus(env, f"Autobús {i}", ruta, horario) for i in range(3)]

    # Generar pasajeros
    env.process(generar_pasajeros(env, 20, ["Estación A", "Estación B", "Estación C"]))

    # Ejecutar la simulación
    env.run(until=100)

if __name__ == "__main__":
    simular_sistema_de_transporte()
