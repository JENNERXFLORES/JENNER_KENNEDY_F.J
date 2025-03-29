lista=[]
def ingreso(num):
    lista.append(num)

def muestra():
    print("indice valor ")
    filas=len(lista) 
    for n in range(filas):
        print("%5d  %5d "%(n,lista[n]))
