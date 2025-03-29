#Desarrollo
nseg=int(input("Ingrese un numero en segundos: "))
if nseg>60:
    min=nseg//60
    seg=nseg%60
  
    hr=min//60
    min=min%60

else:
    seg=nseg
    min=0
    hr=0
print("horas minutos segundos")
print("%3d %6d %8d"%(hr,min,seg))