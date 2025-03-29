import random
mes=["","Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Set",
    "Oct","Nov","Dic"]
print("mes     venta      mensaje")
for m in range(1,13):
    venta=random.randint(500,3000)
    if venta<1200:
        mensaje="venta baja"
    elif venta<2000:
        mensaje="venta regular"
    else:
        mensaje="venta buena"
    print("%-10s  %5d  %-20s"%(mes[m],venta,mensaje))
