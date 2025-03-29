#Desarrollo 
ht=int(input("Ingrese las horas trabajadas: "))
tarifaxh=float(input("Ingrese la tarifa de pago: "))
if ht >= 80:
    hextras= ht - 80
    tariincre= (tarifaxh*1.2)*hextras
    tarinorm= 80 * tarifaxh
    tatot= tariincre + tarinorm
else:
    tatot=ht*tarifaxh

print("El salario del trabajador es", tatot)