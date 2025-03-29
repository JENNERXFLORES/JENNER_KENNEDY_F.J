cat=input("ingrese c1, c2, c3, c4 :" ) 
horas=int(input("hora trabajadas:"))
if cat=="C1" or cat=="c1":
    tarifa=45
elif cat=="C2" or cat=="c2":
    tarifa=37.5
elif cat=="C3" or cat=="c3":
    tarifa=35
else:# por defecto es c4
    tarifa=32.5
pagobruto=tarifa*horas
des=pagobruto*0.15
total=pagobruto - des
print("tarifa   ",tarifa)
print("pago bruto  ",pagobruto)
print("descuento   ",des)
print("pago total  ",total)
