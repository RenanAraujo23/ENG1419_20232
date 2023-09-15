# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
from py_irsend.irsend import send_once
from lirc import init, nextcode
from flask import Flask
import threading as th

# criação do servidor
app = Flask(__name__)


# definição de funções das páginas
@app.route("/power")
def funcao_power():
    send_once("aquario", ["KEY_POWER"])
    return "Tecla Power enviada"
    
@app.route("/aumentar_volume")
def funcao_aumentar():
    send_once("aquario", ["KEY_VOLUMEUP"])
    return "Tecla Volume Up enviada"

@app.route("/diminuir_volume")
def funcao_diminuir():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    return "Tecla Volume Down enviada"

@app.route("/mudo")
def funcao_mudo():
    send_once("aquario", ["KEY_MUTE"])
    return "Tecla Mute enviada"

@app.route("/canal/<string:botoes>")
def funcao_canal(botoes):
    for c in botoes:
        botao = "KEY_" + c
        send_once("aquario", [botao])
    return "Canal trocado"

@app.route("/desliga/<int:tempo>")
def funcao_desliga(tempo):
    S = th.Timer(tempo, funcao_power)
    S.start()
    return "Timer iniciado"


# rode o servidor
app.run(port=5000, debug=True)