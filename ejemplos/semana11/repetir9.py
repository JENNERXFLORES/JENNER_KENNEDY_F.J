mcando=int(input("Ingrese el numero que corresponde al multiplicando: "))
mcador=int(input("Ingrese el numero que corresponde al multiplicador: "))
produc=0
for n in range(1,mcador+1,1):
    produc=produc+mcando
    print(n)
print("El producto es", produc)