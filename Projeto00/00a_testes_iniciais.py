from turtle import *


# Desenhe o que foi solicitado no enunciado do PDF aqui embaixo

# Desenha retangulo 100x50
penup()
goto(-20,200)
pendown()
forward(100)
left(90)
forward(50)
left(90)
forward(100)
left(90)
forward(50)

# Desenha triangulo equilatero
penup()
goto(200,0)
pendown()
forward(80)
left(120)
forward(80)
left(120)
forward(80)
left(120)

# Desenha circulo
penup()
goto(0,-150)
pendown()
circle(50)

# Desenha espiral
penup()
goto(-200,0)
pendown()
raio = [70, 60, 50, 40, 30, 20]
for el in raio:
    circle(el,180)
    
# Desenha coordenadas
penup()
def imprime_coordenadas(x,y):
    goto(x,y)
    texto = "x= " + str(x) + " y= " + str(y)
    write(texto, True)
    
onscreenclick(imprime_coordenadas)




# Mantém a janela do Turtle aberta
mainloop()
