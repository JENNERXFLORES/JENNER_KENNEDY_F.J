#DESARROLLO
hor=int(input("Ingrese la hora, del tiempo en el que parte de la ciudad el ciclista:"))
min=int(input("Ingrese los minutos, del tiempo en el que parte de la ciudad el ciclista:"))
seg=int(input("Ingrese los segundos, del tiempo en el que parte de la ciudad el ciclista:"))
#Tiempo de viaje
tviaje=int(input("Ingrese el tiempo de viaje de una ciudad a otra, en segundos :"))

if (seg+tviaje) >=60:
    totseg=(seg+tviaje)%60
    segamin=(seg+tviaje)//60
    totmin=min+segamin
    tothor=hor

    if (min+segamin)>=60:
        totmin=(min+segamin)%60
        minahor=(min+segamin)//60
        tothor=hor+minahor

else:
    totseg=seg+tviaje
    totmin=min
    tothor=hor

print("La hora del llegada del ciclista es %d horas con %d minutos y %d segundos."%(tothor,totmin,totseg))