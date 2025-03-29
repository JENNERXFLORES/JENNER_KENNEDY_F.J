#DESARROLLO
correc=int(input("Escriba la cantidad de respuestas correctas:"))
incorrec=int(input("Escriba la  cantidad de respuestas incorrectas:"))
vacio=int(input("Escriba la cantidad de preguntas sin responder:"))
nota = (correc*5) + (incorrec*-1) + (vacio*0)
print("La nota que le corresponde al estudiante es:",nota)