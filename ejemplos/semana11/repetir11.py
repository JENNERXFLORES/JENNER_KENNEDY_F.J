num=int(input("Ingrese número max a calcular: "))
print("Numero Mitad Cuadrado Triple")
for n in range(1,num+1):
    mitad=n/2
    cuadrado=n*n
    triple=n*3
    print("%2d %8.1f %6d %7d"%(n,mitad,cuadrado,triple))