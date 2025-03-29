import random
cf=0; cm=0; smf=0; smm=0
print("nro sexo edad")
for n in range(1,21):
  sexo=random.randint(0,1)
  edad=random.randint(16,40)
if sexo==0:
    cad="Femenino"
    cf=cf+1; smf=smf+edad
else:
    cad="Masculino"
    cm=cm+1 ; smm=smm+edad
print("%5d  %10s %5d"%(n,cad,edad))
prof=smf/cf
prom=smm/cm
print("# fecmmenino %d promedio  edad %4.1f "%(cf,prof))
print("#masculino %d promedio edad %4.1f  "%(cm,prom))

