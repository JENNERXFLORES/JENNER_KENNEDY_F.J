horast=float(input("Ingrese las horas trabajadas:"))
pagoxhoras=float(input("Tarifa de pago por hora:"))

if horast>40:
    hextra=horast-40
    pagonor=40*pagoxhoras

    pagoextra=pagoxhoras*1.5
    pxhorasextras=hextra*pagoextra
    
    salario=pagonor+pxhorasextras
else:
    salario=horast*pagoxhoras

print("El salario del profesor es: S/.", salario)
