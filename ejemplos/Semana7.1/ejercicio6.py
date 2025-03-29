#Ejercicio 6
a= float(input("Ingresa la calificacion 1 :"))
b= float(input("Ingresa la calificacion 2 :"))
c= float(input("Ingresa la calificacion 3 :"))

examen= float(input("Ingresa el promedio del examen final :"))

trabajo = float(input("Ingresa la calificacion del trabajo final :"))

promedio = (a+b+c)/3

promediofinal = (promedio * 0.55)+(examen * 0.30)+(trabajo * 0.15)

print("\n El promedio final de la materia de algoritmos es: ",round(promediofinal,1))