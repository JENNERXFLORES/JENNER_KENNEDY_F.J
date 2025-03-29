#Desarrollo
monto=float(input("Ingrese el monto de compra: "))
if monto > 100:
    desc= monto*0.1
    newmonto=monto-desc
elif monto <= 50:
    desc=0
    newmonto=monto-desc
else:
    desc=monto*0.2
    newmonto=monto-desc
print("El descuento aplicado es .",desc)
print("El nuevo monto de compra es .",newmonto)