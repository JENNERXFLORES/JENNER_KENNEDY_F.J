sm=0
cont=0
nfin=int(input("Ingrese un numero superior a 20: "))
print("Numeros comprendidos entre 20 y",nfin)
for n in range(20+1,nfin):
    print(n)
    cont=cont+1
    sm=sm+n
print("\nEl promedio es:")
prom=sm/cont
print(prom)