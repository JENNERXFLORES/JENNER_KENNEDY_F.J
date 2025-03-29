
print("\nModelo1")
resp="si"
while resp=="si":
    num=int(input("Ingrese el numero: "))
    mitad=num/2
    print("La mitad del numero es",mitad)
    resp=input("otra compra si or no: ").lower()
print("Fin")

#2
print("\nModelo2")
num1=int(input("Ingrese el numero inicial del grupo a calcular: "))
num2=int(input("Ingrese el numero final del grupo a calcular: "))
for n in range(num1,num2+1):
    print("La mitad de:",n)
    n = n/2
    print(n)
    
#3
print("\nModelo3")
nro=int(input("Ingrese la cantidad de numeros a calcular:    "))
sm=0
for n in range(1,nro+1):
        num=int(input("Ingrese el numero %d:    "%(n)))
        num=num/2
        print(num)


