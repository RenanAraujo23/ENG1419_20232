# importação de bibliotecas
from gpiozero import LED, Button
from flask import Flask
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta

# criação do servidor
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto5"]
colecao = banco["implementacao"]

app = Flask(__name__)

# definição de funções das páginas
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
    print(dados["estado"])
    
@app.route("/led/<int:x>/<string:s>")    
def pagina_atualiza(x, s):
    if s=="on":
        atualiza_led(x, True)
    elif s=="off":
        atualiza_led(x, False)
    else:
        return "Comando incorreto"
    return "LED 0" + str(x) + " " + s
    
    

# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]

# rode o servidor
app.run(port=5000, debug = False)