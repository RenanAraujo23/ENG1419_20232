# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS

# importação de bibliotecas
from gpiozero import LightSensor,MotionSensor,LED,Button,DistanceSensor
from flask import Flask
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from threading import Timer

# criação do servidor
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto5"]
colecao = banco["implementacao"]

app = Flask(__name__)

order = [["data",DESCENDING]]
dado_recente = colecao.find_one(sort=order)

#definição de funções das páginas
def atualiza_led(idx, state):
    if state == True:
        leds[idx-1].on()
    else:
        leds[idx-1].off()
        
    agora = datetime.now()
    estado = []
    for i in leds:        
        estado.append(i.is_lit)
    dados = {"data": agora, "estado": estado}
    colecao.insert(dados)
    #print(dados["estado"])
    
@app.route("/led/<int:x>/<string:s>")    
def pagina_atualiza(x, s):
    if s=="on":
        leds[x-1].on()
    elif s=="off":
        leds[x-1].off()
    else:
        return "Comando incorreto"
    return "LED 0" + str(x) + " " + s
    
def m_handler():    
    atualiza_led(1, True)
    
    global global_timer
    if global_timer != None:
        global_timer.cancel()
        global_timer = None

def no_m_handler():
    global global_timer
    global_timer = Timer(6.0, off_led)
    global_timer.start()
    
def off_led():
    atualiza_led(1, False)
    
def l_handler():
    atualiza_led(2, False)
    
def dark_handler():
    atualiza_led(2, True)
    
@app.route("/verifica/")
def pagina_verifica():
    html = "<p>Pagina de verificacao</p>\n<ul>\n"
    for i in range(5):
        if leds[i].is_lit:
            s = "<li> Luz " + str(i+1) + ": acesa</li>\n"
        else:
            s = "<li> Luz " + str(i+1) + ": apagada</li>\n"
        html = html + s
    html += "</ul>"
    return html

# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]

#restaura estado anterior
for i in range(5):
    if dado_recente["estado"][i]:
        leds[i].on()
    else:
        leds[i].off()    

mov_sensor = MotionSensor(27)
mov_sensor.when_motion = m_handler
mov_sensor.when_no_motion = no_m_handler

l_sensor = LightSensor(8)
l_sensor.threshold = 0.5
l_sensor.when_dark = dark_handler
l_sensor.when_light = l_handler

global global_timer
global_timer = None

# rode o servidor
app.run(port=5000, debug = True)
