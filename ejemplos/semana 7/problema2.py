mrepartir=float(input("Monto de dinero a repartir:"))
#Repartición
Jo=mrepartir*0.27
Dani=mrepartir*0.25
Davi=(mrepartir-Jo-Dani)

Tamar=Jo*0.85
Josué=Jo-Tamar

caleb = (Josué + Dani)*0.23

reduc1= caleb/2
Mjosue=Josué-reduc1
Mdaniel=Dani-reduc1

total=Tamar+Mjosue+caleb+Mdaniel+Davi

print("El monto que recibió Tamar es:S/",Tamar)
print("El monto que recibió Josué es:S/",Mjosue)
print("El monto que recibió Caleb es:S/",caleb)
print("El monto que recibió Daniel es:S/",Mdaniel)
print("El monto que recibió David es:S/",Davi)
print("El total es", total)
