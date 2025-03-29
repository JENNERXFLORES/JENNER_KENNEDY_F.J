lista=["Juan","Luis","Alex","Maria","Ana"]
print(lista)
print("en forma vertical")
for x in lista:
    print(x)
lista.append("Jose")
lista.insert(1,"Bety")
lista.sort()
lista.reverse()
print("otra forma de leer ")
for i in range(len(lista)):
    print("indice %d  contenido %12s"%(i,lista[i]))
