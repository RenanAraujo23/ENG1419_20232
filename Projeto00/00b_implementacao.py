from turtle import *


def desenha_retangulo(x, y, comprimento, altura, cor):
    penup()
    goto(x,y)
    setheading(0)
    pendown()
    fillcolor(cor)
    begin_fill()
    for i in range(2):
        forward(comprimento)
        right(90)
        forward(altura)
        right(90)
    end_fill()
    return
    
    
def desenha_circulo(x, y, raio, cor):
    penup()
    goto(x,y-raio)
    setheading(0)
    pendown()
    fillcolor(cor)
    begin_fill()
    circle(raio)
    end_fill()
    return
    
    
def desenha_poligono(lista_pontos, cor):
    penup()
    fillcolor(cor)
    begin_fill()
    for dado in lista_pontos:
        x = dado["x"]
        y = dado["y"]
        goto(x,y)
        pendown()
    p_inicial = lista_pontos[0]
    goto(p_inicial["x"], p_inicial["y"])
    end_fill()
    return
    
    
# Bandeira 1
desenha_retangulo(-50,   -50, 33.3, 60, 'blue')
desenha_retangulo(-16.7, -50, 33.3, 60, 'white')
desenha_retangulo(16.6,  -50, 33.3, 60, 'red')


# Bandeira 2
desenha_retangulo(-50,  30, 100, 20, 'orange')
desenha_retangulo(-50,  10, 100, 20, 'white')
desenha_retangulo(-50, -10, 100, 20, 'green')
desenha_circulo(0, 0, 10, 'orange')

# Bandeira 3
desenha_retangulo(-50, 110, 100, 60, 'green')
desenha_poligono([{'x':0, 'y':105}, {'x':-45, 'y':80}, {'x':0, 'y':55}, {'x':45, 'y':80}], 'yellow')
desenha_circulo(0, 80, 13, 'blue')


# Mantém a janela do Turtle aberta
mainloop()