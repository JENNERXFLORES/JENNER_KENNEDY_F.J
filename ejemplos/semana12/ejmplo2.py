# nro de aprobados y jalados
import random 
num=int(input("# de alumnos:"))
cap=0 ; cds=0
print("nro   nota1    nota2    promedio")
for n in range(1,num+1):
    nota1=random.randint(0,20)
    nota2=random.randint(0,20)
    pro=(nota1+nota2)/2
    if pro>=10.5:
        cap=cap+1 # lo cuento como aprobado
    else:
        cds=cds+1 #lo 
    print("%3d  %5d    %5d    %4.1f"%(n,nota1,nota2,pro))
print("numero aprobados :",cap)
print("numero desaprobados :",cds)
