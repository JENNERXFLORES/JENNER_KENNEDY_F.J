#DESARROLLO
cat=input("Ingrese la categoria del empleado, A o B:")
canths=int(input("Cantidad de horas trabajadas:"))
canthj=int(input("Cantidad de Hijos:"))
if cat=="A" or cat=="a":
    sueldob= 45*canths
else:
    sueldob= 37.5*canths

if canthj<=3:
    boni=40.5*canthj
else:
    boni=35*canthj

sbruto= sueldob+boni

if sbruto>=3500:
    des=(13.5*sbruto)/100
else:
    des=0.10*sbruto

sneto= sbruto - des

print("El sueldo basico es", sueldob)
print("El sueldo bruto es", sbruto)
print("El descuento es", des)
print("El suekdo neto es", sneto)