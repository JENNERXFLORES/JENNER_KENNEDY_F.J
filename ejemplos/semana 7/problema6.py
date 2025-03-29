Deb=float(input("Ingrese la cantidad de dinero aportada por Débora:"))
Raq=float(input("Ingrese la cantidad de dinero aportada por Raquel:"))
Séf=float(input("Ingrese la cantidad de dinero aportada por Séfora:"))
#Capital
cap= Deb+Raq+Séf
#Porcentaje que aportan
porcDeb= (Deb*100)/cap
porcRaq= (Raq*100)/cap
porcSef= (Séf*100)/cap

print("El monto del capital formado es: S/",cap)
print("El porcentaje del capital que aporta Débora:%",porcDeb)
print("El porcentaje del capital que aporta Raquel:%",porcRaq)
print("El porcentaje del capital que aporta Séfora:%",porcSef)
