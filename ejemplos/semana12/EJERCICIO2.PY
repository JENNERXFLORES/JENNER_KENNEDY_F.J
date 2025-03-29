smt=0
cnt=0
talla=1
while talla>0:
    talla=float(input("ingrese talla 0=finaliza :"))
    if talla>0:
        smt=smt+talla
        cnt=cnt+1
#fin while
prom=smt/cnt
print("# de personas",cnt)
print("promedio de talla ",prom)
