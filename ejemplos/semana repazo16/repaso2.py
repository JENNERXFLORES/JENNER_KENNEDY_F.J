smp=0; con=0
resp="s"
while resp=="s":
    con=con+1
    curso=input("numero de curso %d:"%(con))
    nro=int(input("# de notas:"))
    sm=0
    for n in range(1,nro+1):
        nota=int(input("ingrese nota%d:"%(n)))
        sm=sm+nota
    prom=sm/nro
    smp=smp+prom
    print("%s su promedio %3.1f"%(curso,prom))
    resp=input("otra materia s/n:").lower()
procic=smp/con
print("promedio de ciclo:%3.2f"%(procic))
