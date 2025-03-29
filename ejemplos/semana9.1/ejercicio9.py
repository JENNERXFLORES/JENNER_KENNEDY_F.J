#Desarrollo 
durallama=int(input("Ingrese la duración de su llamada:"))
if durallama <= 3:
    precio=0.50
else:
    minextra=durallama-3
    precio=0.50+(0.1*minextra)
print("El costo de la llamada es S/. %3.1f"%(precio))