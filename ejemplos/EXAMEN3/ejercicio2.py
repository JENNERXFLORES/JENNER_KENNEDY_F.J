#DESARROLLO
import random
nump=int(input("ingrese numero de empleados:"))
smafp=0
print("Nro     Sueldo     AFP     Total")
for n in range(1,nump+1):
    sueldo=random.randint(800,4000)
    afp=sueldo*0.11
    total=sueldo+afp
    print("%2d     %6d    %3.2f    %6.2f"%(n,sueldo,afp,total))
    sumafp=sumafp+total
    print("total afp ",smafp)

      