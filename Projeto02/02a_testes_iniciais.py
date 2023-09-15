# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
from py_irsend.irsend import send_once
from lirc import init, nextcode

# definição de funções
def acenderLEDS():
    leds[0].on()
    leds[1].on()
    leds[2].on()
    leds[3].on()
    leds[4].on()
    
def apagarLEDS():
    leds[0].off()
    leds[1].off()
    leds[2].off()
    leds[3].off()
    leds[4].off()

# criação de componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
button1 = Button(11)
button2 = Button(12)
button3 = Button(13)
button4 = Button(14)
button5 = Button(15)

#inicializacao
init("aula", blocking=False)

button1.when_pressed = acenderLEDS
button2.when_pressed = apagarLEDS
# loop infinito
selecionado = -1
while True:
    lista_com_codigo = nextcode()
    if lista_com_codigo != []:
        codigo = lista_com_codigo[0]
        if   codigo == "KEY_1" :
            lcd.clear()
            lcd.message("LED 1\nSelecionado")
            selecionado = 1
        elif codigo == "KEY_2" :
            lcd.clear()
            lcd.message("LED 2\nSelecionado")
            selecionado = 2
        elif codigo == "KEY_3" :
            lcd.clear()
            lcd.message("LED 3\nSelecionado")
            selecionado = 3
        elif codigo == "KEY_4" :
            lcd.clear()
            lcd.message("LED 4\nSelecionado")
            selecionado = 4
        elif codigo == "KEY_5" :
            lcd.clear()
            lcd.message("LED 5\nSelecionado")
            selecionado = 5
        elif codigo == "KEY_OK" and selecionado != -1:
            leds[selecionado-1].toggle()
        elif codigo =="KEY_UP":
            if selecionado==5:
                selecionado=1
            else:
                selecionado +=1
            mensagem = "LED " + str(selecionado) + "\nSelecionado"
            lcd.clear()
            lcd.message(mensagem)
        elif codigo =="KEY_DOWN":
            if selecionado==1:
                selecionado=5
            else:
                selecionado -=1
            mensagem = "LED " + str(selecionado) + "\nSelecionado"
            lcd.clear()
            lcd.message(mensagem)
                        
    sleep(0.2)
