n1=float(input("Ingrese Nota 1:"))
n2=float(input("Ingrese Nota 2:"))
n3=float(input("Ingrese Nota 3:"))
n4=float(input("Ingrese Nota 4:"))
if n1<n2 and n1<n3 and n1<n4:
    prom=(n2+n3+n4)/3
    anulada=n1
elif n2<n1 and n2<n3 and n2<n4:
    prom=(n1+n3+n4)/3
    anulada=n2
elif n3<n1 and n3<n2 and n3<n4:
    prom=(n1+n2+n4)/3
    anulada=n3
else:
    prom=(n1+n2+n3)/3
    anulada=n4

if prom>=12:
    obser="Aprobado"
else:
    obser="Desaprobado"
    
print("El promedio de las 3 notas superiores es:",prom)
print("La nota anulada es:",anulada)
print("Observación:",obser)