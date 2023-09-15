# importação de bibliotecas
from gpiozero import Buzzer, Button, DistanceSensor, LED
from Adafruit_CharLCD import Adafruit_CharLCD
from datetime import datetime, timedelta
from pymongo import MongoClient

# definição de funções
campainha = Buzzer(16)
b1 = Button(11)
b2 = Button(12)
sensor = DistanceSensor(trigger=17, echo=18)
l1 = LED(21)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

cliente = MongoClient("localhost", 27017)
banco = cliente["aula3"]
colecao = banco["dist"]

sensor.threshold_distance = 0.1

def toca_camp():
    campainha.beep(on_time=0.5, off_time=0.5, n=1)
    
def aprox_sensor():
    l1.blink(on_time=0.5, off_time=0.5, n=2)
    
def exibe_dist():
    dist = sensor.distance * 100
    lcd.clear()
    lcd.message("Distancia\n%.1f cm" %(dist))
    
def salva_dist():
    agora = datetime.now()
    dist = sensor.distance
    dado = {"data": agora, "distancia": dist}
    colecao.insert(dado)
    lcd.clear()
    lcd.message("Distancia\n%.1f cm" %(dist * 100))

# criação de componentes
b1.when_pressed = toca_camp
sensor.when_in_range = aprox_sensor
sensor.when_out_of_range = aprox_sensor
#b2.when_pressed = exibe_dist
b2.when_pressed = salva_dist
