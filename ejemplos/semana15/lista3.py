#ingrese 6 practicas obtner su promedio con las 4 mayores notas
lista=[]  #creando una lista vacia
for n in range(1,7):
    nota=int(input("nota %d :"%(n)))
    lista.append(nota)
lista.sort() #ordenar de forma ascendente
prom= (lista[2]+lista[3]+lista[4]+lista[5])/4
print("notas anuladas %d , %d "%(lista[0],lista[1]))
print("el promedio es  ",prom)