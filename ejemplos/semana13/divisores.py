#ingrese un numero y muestre sus divisores y la suma de sus divisores
#sin incluir el mismo numero
numero=int(input("ingrese un numero :"))
smd=0
for d in range(1,numero):
    if numero%d==0:
        smd=smd+d
        print(d,end=", ")
print("la suma de divisores=",smd)
