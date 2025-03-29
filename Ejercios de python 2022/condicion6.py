categoria=input("ingrese A  B:")
horas=int(input("# de horas :"))
hijos=int(input("# de hijos :"))
if categoria=="A" or categoria=="B":
   sueldob=45*horas
else:
    sueldob=37.5*horas
if hijos<=3:
    bonif=40.5*hijos
else:
     bonif=35*hijos
bruto=sueldob+bonif
if bruto>=3500:
   des=0.135*bruto
else:
    des=0.1*bruto
neto=bruto-des
print("sueldo basico:",sueldob)
print("numero de hijos:",hijos)
print("sueldo bruto:",bruto)
print("descuento:",des)
print("total a pagar:",neto)
