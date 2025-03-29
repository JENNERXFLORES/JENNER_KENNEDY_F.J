#problema5
hora=float(input("ingrese horas :"))
tarifa=float(input("pagox hora :"))

Suelb=hora*tarifa
print("\n sueldo basico :",Suelb)
boni=Suelb*0.2
print("\n bonificasion :",boni)
Suelbru=Suelb+boni
print("\n sueldo bruto :", Suelbru)
des=Suelbru*0.1
neto=Suelbru-des
print("\ndescuento :",des)
print("\n sueldo  neto :",neto)