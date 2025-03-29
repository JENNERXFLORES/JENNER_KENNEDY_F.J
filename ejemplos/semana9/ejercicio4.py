compra=float(input("ingrese su gasto : "))
tarjeta=input("tipo de su tarjeta A B C  "" : ").upper()
if tarjeta=="A":
    interes=compra*0.05
    saldo=compra+interes
    monto=saldo/12
elif tarjeta=="B":
    interes=compra*0.1
    saldo=compra+interes
    monto=saldo/8
elif tarjeta=="C":
    interes=compra*0.15
    saldo=compra+interes
    monto=saldo/6
print(" interes %3.1f saldo %5.1f  monto %8.1f"
%(interes,saldo,monto))




    