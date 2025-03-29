import math
import random
print("20 valores de 30-90 grados ")
print("angulo  seno     raiz")
for n in range(1,21):
    angulo=random.randint(30,90)
    rad=math.radians(angulo)
    seno=math.sin(rad)
    raiz=math.sqrt(angulo)
    print("%-5d %6.3f  %8.2f "%(angulo,seno,raiz))

