def _cuenta(prestamo,meses):
    cuota=prestamo/meses
    return cuota

def _prestamo():
    prestamo= input("Monto del prestamo:  ")
    meses=input("Meses para pagar:  ")
    print ("Cantidad a pagar por mes:  ",_cuenta(prestamo,meses))

