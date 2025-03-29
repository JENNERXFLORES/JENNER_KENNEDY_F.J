lista=[]
def ingreso(num):
    lista.append(num)

def muestra():
    print("indice valor ")
    
    filas=len(lista) 
    for n in range(filas):
        print("%5d  %5d "%(n,lista[n]))
def calculo():
    mayor=max(lista)
    menor=min(lista)
    suma=sum(lista)
    print("el mayor valor ",mayor)
    print("menor valor  ",menor)
    print("la suma es  ",suma)
#principal
ingreso(45);ingreso(40);ingreso(20);ingreso(80)
ingreso(34); ingreso(60)
muestra()
calculo()
