#Desarrollo
Articulo=input("Ingrese el articulo a adquirir: ")
unidades=int(input("Ingrese las unidades a adquirir: "))
precio=float(input("Ingrese el precio del articulo: "))
pventa= precio*unidades
iva = pventa*0.15
pbruto= pventa + iva
if pbruto > 500:
    desc= pbruto*0.05
    pbruto=pbruto-desc
else: 
    desc=0
    pbruto=pbruto-desc

print("----------------FACTURA-----------------")
print("----------------------------------------")
print("Descripción      Unidades      precio")
print("%5s %14d %16.1f"%(Articulo,unidades,precio))
print("-----------------------------------------")
print("El precio bruto es",pbruto,"Bolivianos")
print("-----------------------------------------")