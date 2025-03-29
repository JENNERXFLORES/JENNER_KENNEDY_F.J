import math
def hipo(ca, cb):
    h=math.sqrt(ca*ca+cb*cb)
    return h

def tabla(num):
    print("tabla del ",num)
    for p in range(1,13):
        pro=p*num
        print("%d x %d=%d "%(p,num,pro))

#llamando a la funcion 
print("hipotenusa de lado 3 y 4 :",hipo(3,4))
print("hipotenusa de lado 12 y 18 :",hipo(12,18))
tabla(8)
print("======")
