octanaje=["","1=85","2=90","3=95","4=97","5=98"]
precio=[0,14.5,18.7,21.5,23,4,25,2]
print(octanaje)
num=int(input("ingrese el tipo de octanaje :"))
galones=int(input("numero de galones :"))
importe=galones*precio[num]
print("octanaje",octanaje[num])
print("precio por galon :",precio[num])
print("importe a pagar :",importe)
