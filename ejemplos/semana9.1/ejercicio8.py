#Desarrollo
import math
A=int(input("coeficiente de la variable caudratica a!=0 \n :"))
B=int(input("coeficiente de la variable lienal \n :"))
C=int(input("termino independiente \n :"))
X1=0
X2=0
if ((B**2)-4*A*C) < 0:
    print("X ∈ R")
else:
    X1=(-B+math.sqrt(((B**2)-4*A*C)))/(2*A)
    X2=(-B-math.sqrt(((B**2)-4*A*C)))/(2*A)
    print("resultado :")
    print("x1=",X1)
    print("x2=",X2)
