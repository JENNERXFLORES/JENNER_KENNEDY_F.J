largo=float(input("Ingrese medida de largo de la base de pirámide:"))
ancho=float(input("Ingrese medida de amcho de la base de pirámide:"))
altura=float(input("Ingrese medida de altura de la pirámide:"))
#Hallar área
area = largo*ancho
#Hallar volumen
vol = (area*altura)/3

print("El área de la base de la pirámide es:",area)
print("El volumen de la pirámide es:",vol)
