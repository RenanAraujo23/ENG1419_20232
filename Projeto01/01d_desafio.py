# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
# DEPOIS FAÇA OS NOVOS RECURSOS

# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS

# importação de bibliotecas
from os import system
from time import sleep
from gpiozero import LED, Button
from Adafruit_CharLCD import Adafruit_CharLCD
from mplayer import Player
from random import shuffle, sample


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
        global inicio, fim
        inicio = 0
        fim = 15
    
def botao_um():
    inst_tempo = player.time_pos
    if inst_tempo > 2:
        player.time_pos = 0
    else:
        player.pt_step(-1)
        global inicio, fim
        inicio = 0
        fim = 15
        
def botao_quatro():
    global flag_tempo,tempo_vol
    vol = player.volume
    player.volume = vol - 5
    flag_tempo = True
    tempo_vol=2
    
def botao_cinco():
    global flag_tempo,tempo_vol
    vol = player.volume
    if vol < 94:
        player.volume = vol + 5
        flag_tempo = True
        tempo_vol=2
    else:
        player.volume=100
        flag_tempo = True
        tempo_vol=2
        
def exibe_dados():
    global inicio, fim, tempo_vol, flag_tempo
    metadados = player.metadata
    inst_tempo = player.time_pos
    total_tempo = player.length
    if metadados != None:
        lcd.clear()
        titulo = metadados["Title"]
        if fim >= len(titulo):
            if inicio == fim:
                inicio = 0
                fim = 15
            else:
                fim = len(titulo)
        lcd.message(titulo[inicio:fim])
    else:
        lcd.clear()
        lcd.message("Erro no titulo")
    
    lcd.message("\n")
    
    if flag_tempo==True and tempo_vol>0:
        vol = player.volume
        tempo_vol = tempo_vol - 0.2
        mensagem = "Volume: %d" % (vol)
        lcd.message(mensagem)
        qtd = int(vol/20)
        if qtd==0:
            led1.off()
            led2.off()
        elif qtd==1:
            led1.on()
        elif qtd==2:
            led1.on()
            led2.on()
        elif qtd==3:
            led1.on()
            led2.on()
            led3.on()
        elif qtd==4:
            led1.on()
            led2.on()
            led3.on()
            led4.on()
        elif qtd==5:
            led1.on()
            led2.on()
            led3.on()
            led4.on()
            led5.on()           
        
    else:
        led1.on()
        led2.off()
        led3.off()
        led4.off()
        led5.off()
        flag_tempo = False
        tempo_vol = 2
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
lista = open("playlist.txt", "r")
pl = lista.readlines()
nova_lista = sample(pl, len(pl))
nova_pl = open("new_playlist.txt", "w")
nova_pl.writelines(nova_lista)
lista.close()
nova_pl.close()


player = Player()
player.loadlist("new_playlist.txt")
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
botao4 = Button(14)
botao5 = Button(15)
led1 = LED(21)
led2 = LED(22)
led3 = LED(23)
led4 = LED(24)
led5 = LED(25)
led1.on()
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
botao1.when_pressed = botao_um
botao2.when_pressed = botao_dois
botao3.when_held = botao_tres_pres
botao3.when_released = botao_tres_solta
botao4.when_pressed = botao_quatro
botao5.when_pressed = botao_cinco

global inicio, fim, tempo_vol, flag_tempo
inicio = 0
fim = 15
tempo_vol = 2
flag_tempo = False


# loop infinito
while True:
    #global inicio, fim
    #led1.on()
    exibe_dados()
    inicio = inicio + 1
    fim = fim + 1

    sleep(0.2)


