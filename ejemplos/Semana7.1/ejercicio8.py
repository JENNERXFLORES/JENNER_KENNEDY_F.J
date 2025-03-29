#Pide al usuario dos pares de números x1,y2 y x2,y2, que representen dos
#puntos en el plano. Calcula y muestra la distancia entre ellos.

X1=(float(input('''Ingrese X1              :''')))
Y1=(float(input('''Ingrese Y1              :''')))
X2=(float(input('''Ingrese X2              :''')))
Y2=(float(input('''Ingrese Y2              :''')))
D= (((X2-X1)**2)+((Y1-Y2)**2))
D1=(D ** (1/2))
print('La distancia entre los dos puntos es: ',round(D1,3))