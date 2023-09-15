# importação de bibliotecas
from gpiozero import LED, Button
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep

global contador
contador = 0

# definição de funções
def pisca_dois():
    led2.toggle()
    
def pisca_tres():
    global contador
    contador = contador + 1
    led3.blink(n=4, on_time = 1, off_time = 1)
    lcd.clear()
    mensagem = "Contagem: \n" + str(contador)
    lcd.message(mensagem)

# criação de componentes
led1 = LED(21)
led2 = LED(22)
led3 = LED(23)
led4 = LED(24)
led5 = LED(25)

botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)

lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

led1.blink(on_time=1, off_time=2)
botao2.when_pressed = pisca_dois

botao3.when_pressed = pisca_tres



# loop infinito
while True:
    if led1.is_lit and botao1.is_pressed:
        led5.on()
    else:
        led5.off()
            
        

    sleep(0.2)
