#DESARROLLO
nombre = input("\ningrese tu nombre:")
apellido1 = input("\ningrese tu primer apellido:")
apellido2 = input("\ningrese tu segundo apellido:")

inicial = nombre[0]
inicial = inicial + apellido1[0]
inicial = inicial + apellido2[0]

inicial = inicial.upper()
print("Las iniciales son:",inicial)
