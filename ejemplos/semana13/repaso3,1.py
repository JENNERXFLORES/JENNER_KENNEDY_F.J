dsep=float(input("distancia de separacion en mts:"))
va=float(input("velocidad de A mts/seg :"))
vb=float(input("velocidad de B mts/seg:"))
#calculos
tenc=int(dsep/(va+vb))
print("tiempo   distA    DistB")
for t in range(2, tenc+1,2):
    da=va*t
    db=vb*t
    print("%5d   %8.1f   %8.1f"%(t,da,db))
