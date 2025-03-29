#DESARROLLO 1:
tipo=["","1-97oct","2-95oct","3-90oct","4-84oct"]
pxgalon=[0,22.30,20.50,17.50,15.20]

print(tipo)
tipogaso=int(input("Ingrese el tipo de Gasolina: "))
cant=int(input("Ingrese la canidad de Galones: "))
impcomp=pxgalon[tipogaso]*cant

#DESCUENTO
if cant <= 6:
    desc=impcomp*0.05
    impaplic=impcomp-desc
elif cant >6 and cant <=12:
    desc=impcomp*0.07
    impaplic=impcomp-desc
elif cant >12 and cant <=18:
    desc=impcomp*0.09
    impaplic=impcomp-desc
else:
    desc=impcomp*0.11
    impaplic=impcomp-desc
print("----------------------------------")
print("El importe de la compra es : %1.1f"%(impcomp))
print("El importe del descuento es: %1.1f"%(desc))
print("El importe total a pagar es: %1.1f"%(impaplic))
print("----------------------------------")
print("PREMIO!")
if tipogaso==1:
    print("¡¡¡Se ganó una Gorra!!!")
else:
    print("¡¡¡Se ganó un palicero!!!")