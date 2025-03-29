#Desarrollo
minutos=int(input("ingrese los  minutos:" ))
dias=minutos//(24*60)
sobra=minutos%(24*6)
horas=sobra//60
minutoss=sobra%(60)
print("\n",dias,"dias con ",horas,"hora y",minutoss,"minutos")