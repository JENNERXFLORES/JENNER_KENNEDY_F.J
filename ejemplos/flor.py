import turtle

# Configurar la pantalla
screen = turtle.Screen()
screen.bgcolor("white")

# Configurar la tortuga para dibujar
flower = turtle.Turtle()
flower.shape("turtle")
flower.speed(10)

# Función para dibujar pétalos
def draw_petal():
    for i in range(2):
        flower.circle(100, 60)
        flower.left(120)
        flower.circle(100, 60)
        flower.left(60)

# Dibujar la flor amarilla
flower.color("yellow")
for i in range(6):
    draw_petal()
    flower.right(60)

# Dibujar el centro de la flor
flower.color("brown")
flower.begin_fill()
flower.circle(50)
flower.end_fill()

# Finalizar
flower.hideturtle()
turtle.done()
