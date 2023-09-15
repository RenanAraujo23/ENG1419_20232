# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS

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
        
def botao_tres_pres():
    player.speed = 2
    
def botao_tres_solta():
    velocidade = player.speed
    if velocidade == 2:
        player.speed = 1
    else:
        player.pt_step(1)
    
def botao_um():
    inst_tempo = player.time_pos
    if inst_tempo > 2:
        player.time_pos = 0
    else:
        player.pt_step(-1)
        
def exibe_dados():
    metadados = player.metadata
    inst_tempo = player.time_pos
    total_tempo = player.length
    if metadados != None:
        lcd.clear()
        lcd.message(metadados["Title"])
    else:
        lcd.clear()
        lcd.message("Erro no titulo")
    
    lcd.message("\n")
    
    if inst_tempo != None and total_tempo != None:
        minutos_cor = int(inst_tempo/60)
        segundos_cor = int(inst_tempo - minutos_cor*60)
        minutos_total = int(total_tempo/60)
        segundos_total = int(total_tempo - minutos_total*60)
        mensagem = "%.2d:%.2d de %.2d:%.2d" % (minutos_cor,segundos_cor,minutos_total,segundos_total)
        lcd.message(mensagem)
    else:
        lcd.message("Erro no tempo")
    

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
botao3.when_held = botao_tres_pres
botao3.when_released = botao_tres_solta


# loop infinito
while True:
    exibe_dados()

    sleep(0.2)

