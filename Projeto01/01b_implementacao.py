# importação de bibliotecas
from os import system
from time import sleep
from gpiozero import LED, Button
from Adafruit_CharLCD import Adafruit_CharLCD
from mplayer import Player


# para de tocar músicas que tenham ficado tocando da vez passada
system("killall mplayer")


# definição de funções
def botao_dois():
    player.pause()
    if player.paused:
        led1.blink(on_time=0.5, off_time=0.5)
    else:
        led1.on()
        
def botao_tres():
    player.pt_step(1)
    
def botao_um():
    inst_tempo = player.time_pos
    if inst_tempo > 2:
        player.time_pos = 0
    else:
        player.pt_step(-1)
        
def exibe_dados():
    metadados = player.metadata
    if metadados != None:
        lcd.clear()
        lcd.message(metadados["Title"])

# criação de componentes
player = Player()
player.loadlist("playlist.txt")
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
led1 = LED(21)
led1.on()
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
botao1.when_pressed = botao_um
botao2.when_pressed = botao_dois
botao3.when_pressed = botao_tres


# loop infinito
while True:
    exibe_dados()

    sleep(0.2)
