resp="s"
smt=0 #acumulador  de totales
while resp=="s":
    nombre=input("producto :")
    puni=float(input("precio unitario:"))
    can=int(input("unidades a comprar:"))
    tot=puni*can
    print("total parcial ",tot)
    smt=smt+tot
    resp=input("otra compra s/n:").lower()
#fin del proceso mientras
print(" el total a pagar ",smt)
