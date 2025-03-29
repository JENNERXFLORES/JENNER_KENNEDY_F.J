#DESARROLLO
dona=float(input("Ingrese el monto de la donación:"))
if dona>=10000:
    csalud= (dona*30)/100   
    repart1= dona - csalud

    comeniños= (repart1*50)/100

    inverbolsa= repart1 - comeniños

else:
    csalud= (dona*25)/100
    repart1= dona - csalud

    comeniños= (repart1*60)/100

    inverbolsa= repart1 - comeniños

print("El rubro de Salud recibirá S/.", csalud)
print("El rubro de comedor de niños recibirá S/:", comeniños)
print("El monto a invetir en el Bolsa es de S/.", inverbolsa)