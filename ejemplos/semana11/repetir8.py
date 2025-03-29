numero = int(input("numero  "))
contador = 0
print("los divisores de ",numero)
for divisor in range(1,numero+1):
    if (numero % divisor) == 0 :
        print(divisor,end=",")
        contador= contador+ 1
print("\nel numero ",numero," tiene ",contador," divisores")