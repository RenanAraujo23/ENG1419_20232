# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
# DEPOIS FAÇA OS NOVOS RECURSOS

# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
from py_irsend.irsend import send_once
from lirc import init, nextcode
from flask import Flask, render_template, redirect
import threading as th
import json
# criação do servidor
app = Flask(__name__)

# leitura json
canais = open("canais.json", "r")
canais = json.load(canais)

# definição de funções das páginas
@app.route("/power")
def funcao_power():
    send_once("aquario", ["KEY_POWER"])
    return redirect("/dashboard")
    
@app.route("/aumentar_volume")
def funcao_aumentar():
    send_once("aquario", ["KEY_VOLUMEUP"])
    return redirect("/dashboard")

@app.route("/diminuir_volume")
def funcao_diminuir():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    return redirect("/dashboard")

@app.route("/mudo")
def funcao_mudo():
    send_once("aquario", ["KEY_MUTE"])
    return redirect("/dashboard")

@app.route("/canal/<string:botoes>")
def funcao_canal(botoes):
    for c in botoes:
        botao = "KEY_" + c
        send_once("aquario", [botao])
    return redirect("/dashboard")

@app.route("/desliga/<int:tempo>")
def funcao_desliga(tempo):
    S = th.Timer(tempo, funcao_power)
    S.start()
    return redirect("/dashboard")

@app.route("/dashboard")
def mostrar_pagina():
    return render_template("pagina.html", canais_json = canais)

# rode o servidor
app.run(port=5000, debug=True)

