# importação de bibliotecas
from gpiozero import LightSensor,MotionSensor,LED,Button,DistanceSensor
from threading import Timer
from requests import post

# definição de funçõ
def recurrent_timer():
    timer = Timer(2.0, recurrent_timer)
    timer.start()
    print("ola")

def motion_handler():
    print('entrou')
    
    led1.on()
    led2.on()
    
    global global_timer
    if global_timer != None:
        global_timer.cancel()
        global_timer = None

def no_motion():
    led1.off()
    
    global global_timer
    global_timer = Timer(8.0, off_led2)
    global_timer.start()

    
def off_led2():
    print('saiu')
    led2.off()

def bt1_handler():
    formated_l = "%.02f"%(100*light_sensor.value)
    formated_d = "%.02f"%(100*dist_sensor.distance)
    dados = {"value1": formated_l, "value2": formated_d}
    #print(dados["Value1"])
    #print(dados["value2"])
    resultado = post(endereco, json=dados)
    print(resultado.text)

# criação de componentes
led1 = LED(21)
led2 = LED(22)

global global_timer
global_timer = None

m_sensor = MotionSensor(27)
m_sensor.when_motion = motion_handler
m_sensor.when_no_motion = no_motion

chave = "IQopku3GSBLxHKiO5iUNf"
evento = "button_pressed"
endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/"+ chave

bt1 = Button(11)
bt1.when_pressed = bt1_handler

light_sensor = LightSensor(8)

dist_sensor = DistanceSensor(trigger=17, echo=18)

# loop infinito
recurrent_timer()
