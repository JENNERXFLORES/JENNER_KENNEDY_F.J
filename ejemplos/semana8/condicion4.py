#DESARROLLO
sbasi=float(input("Ingrese su Sueldo básico:"))
imptot=float(input("Ingrese el importe total vendido:"))
canth=int(input("Ingrese la cantidad de Hijos:"))
if imptot>=15000:
    comi= imptot*0.93
else:
    comi= imptot*0.95

if canth<5:
    boni= canth*25
else:
    boni= canth*22

sueldob = sbasi + comi + boni

if sueldob>3500:
    desc= sueldob*0.15
else:
    desc= sueldob*0.11

sneto= sueldob-desc

print("El sueldo básico es S/.", sbasi)
print("La comisión es S/.", comi)
print("La bonificación es S/.", boni)
print("El sueldo bruto es S/.", sueldob)
print("El descuento es S/.", desc)
print("El sueldo neto es S/.", sneto)