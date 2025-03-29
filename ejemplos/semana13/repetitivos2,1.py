smt=0
cuenta=0
nota=1
while nota>=0 and nota<=20:
    nota=float(input("ingrese nota finaliza <0 o >20:"))
    if nota>=0 and nota<=20:
        smt=smt+nota
        cuenta=cuenta+1
#fin while
prom=smt/cuenta
print("# de personas ",cuenta)
print("promedio de nota :",prom)


