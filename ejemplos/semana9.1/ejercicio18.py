#Desarrollo
ht=int(input("Ingrese las horas trabajadas del profesor: "))
tarifaxh=float(input("Ingrese la tarifa de pago: "))
if ht > 40:
    hextras= ht - 40
    tariincre= (tarifaxh*1.5)*hextras
    tarinorm= 40 * tarifaxh
    tatot= tariincre + tarinorm
else:
    tatot=ht*tarifaxh

print("El salario del profesor es : S/. ",tatot)