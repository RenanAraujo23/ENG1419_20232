from json import load
from turtle import *


# Copie as funções que você fez na Implementação aqui embaixo
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

# Faça a primeira parte do Aperfeiçoamento aqui

def desenha_bandeira(dicionario_do_pais):
    for dados in dicionario_do_pais["elementos"]:
        if dados["tipo"] == "retângulo":
            desenha_retangulo(dados["x"], dados["y"], dados["comprimento"], dados["altura"], dados["cor"])
        elif dados["tipo"] == "círculo":
            desenha_circulo(dados["x"], dados["y"], dados["raio"], dados["cor"])
        else:
            lista_pontos = dados["pontos"]
            desenha_poligono(lista_pontos, dados["cor"])  
    return


lista_de_paises = load(open('paises.json', encoding="UTF-8"))
desenha_bandeira(lista_de_paises[2])


# Faça a segunda parte do Aperfeiçoamento aqui
def getPais(x,y):
    temp = False
    penup()
    goto(x,y)
    pais = textinput("País", "Digite o nome do país: ")
    for el in lista_de_paises:
        if el["nome"]==pais:
            desenha_bandeira(el)
            temp = True
    if temp == False:
        print("País não encontrado\n")
    
onscreenclick(getPais)

    


# O desafio deve ser feito diretamente no JSON, não aqui!


# Mantém a janela do Turtle aberta
mainloop()