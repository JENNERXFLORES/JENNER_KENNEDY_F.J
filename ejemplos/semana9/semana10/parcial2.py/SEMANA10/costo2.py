# ejerccio con lista 3
octanaje=["","85oct","90oct","95oct","97oct","98oct"]
precio=[0,14.5,18.7,21.5,23.4,25.2]
print(octanaje)
num=int(input("ingrese tipo:"))
npas=int(input("numero de galones: "))
importe=npas*precio[num]
print((" tipo de octajeno:", octanaje[num]))
print(("precio del galon :", precio[num]))
print(("importe a pagar :", importe))

