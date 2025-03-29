# tirar virtualmente dos dados si sale 7 o 12 gana , sino colocar
#un mensaje intente de nuevo 
import random 
dado1=random.randint(1,6)
dado2=random.randint(1,6)
sm=dado1+dado2 
if sm==7 or sm==12:
    print("gano!!!",sm)
else:
    print("intente de nuevo dado1 %d dado2 %d "%(dado1,dado2))
