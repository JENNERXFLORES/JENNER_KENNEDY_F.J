monto=float(input("Ingrese el monto de la donación recibida:"))
salud1= monto*0.25
escuela1= monto*0.35 
asilo= monto-salud1-escuela1
#Hallamos monto de comedor
comedor1=escuela1*0.45
escuela2=escuela1-comedor1

#Hallamos monto de biblioteca
biblioteca1=(comedor1+escuela2)*0.17
reduc1=biblioteca1/2

comedor2=comedor1-reduc1
escuela3=escuela2-reduc1

biblioteca2=salud1*0.40
salud2=salud1-biblioteca2

biblioteca3= biblioteca1+biblioteca2 

print("El área de Centro de salud recibirá. S/.",salud2)
print("El área de Comedor recibirá. S/.",comedor2)
print("El área de Biblioteca recibirá. S/.",biblioteca3)
print("El área de Escuela recibirá. S/.",escuela3)
print("El área de Asilo de ancianos recibirá. S/.",asilo)
#Comprovación
Montoreci=salud2+comedor2+biblioteca3+escuela3+asilo
print("\n La donación recibida fue de: S/",Montoreci)
