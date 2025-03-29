#Desarrollo
sueld=float(input("Ingrese ele sueldo del trabajador: "))
if sueld <=1000:
    desc= sueld*0.10
    sneto= sueld-desc
elif sueld > 2000:
    desc=sueld*0.18
    sneto= sueld-desc
else:
    desc=sueld*0.15
    sneto= sueld-desc

print("El descuento del trabajador es",desc)
print("El sueldo neto del trabajador es",sneto)