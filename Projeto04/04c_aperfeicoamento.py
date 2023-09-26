# importação de bibliotecas
from os import system
from gpiozero import Button, LED, Buzzer, DistanceSensor
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from requests import post, get
from subprocess import Popen
from urllib.request import urlretrieve
from mplayer import Player
from datetime import datetime, timedelta 


# Mata todos os aplicativos "mplayer" e "arecord"
system("killall mplayer")
system("killall arecord")


# parâmetros iniciais do Telegram
chave = "6578552206:AAF1OKmAKHa9mhyrM59lda1ryE9ycqfvAU8"
id_da_conversa = "6569313137"
endereco_base = "https://api.telegram.org/bot" + chave


# definição de funções

def desliga_buz():
    campainha.off()
    print("enviando msg..")
    endereco = endereco_base + "/sendMessage"
    dados = {"chat_id": id_da_conversa, "text": "Alguem esta na porta"}
    resposta = post(endereco, json=dados)
    print("msg enviada!")
    system("fswebcam --resolution 640x480 --skip 10 foto.jpg")
    print("enviando photo..")
    endereco = endereco_base + "/sendPhoto"
    dados = {"chat_id": id_da_conversa}
    arquivo = {"photo": open("foto.jpg", "rb")}
    resposta = post(endereco, data=dados, files = arquivo)
    print("photo enviada!")
    return        

def b3_pressed():
    global aplicativo
    comando = ["arecord", "--duration", "30", "audio.wav"]
    aplicativo = Popen(comando)
    
def b3_released():
    global aplicativo
    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
    system("opusenc audio.wav audio.ogg")
    print("enviando audio..")
    endereco = endereco_base + "/sendVoice"
    dados = {"chat_id": id_da_conversa}
    arquivo = {"voice": open("audio.ogg", "rb")}
    resposta = post(endereco, data=dados, files = arquivo)
    print("audio enviado!")
    
def baixar_audio(id_do_arquivo):
    endereco = endereco_base + "/getFile"
    dados = {"file_id": id_do_arquivo} 
    resposta = get(endereco, json=dados) 
    dicionario = resposta.json() 
    final_do_link = dicionario["result"]["file_path"] 

    link_do_arquivo = "https://api.telegram.org/file/bot" + chave + "/" + final_do_link

    arquivo_de_destino = "audio_download.ogg" 
    urlretrieve(link_do_arquivo, arquivo_de_destino)
    
def sensor_aprox():
    global tempo_aprox
    tempo_aprox = datetime.now()
    print("Aproximou")
    
def sensor_afast():
    global tempo_afast
    tempo_afast = datetime.now()
    print("Afastou")
    intervalo = tempo_afast - tempo_aprox
    if intervalo.total_seconds() >=10:
        endereco = endereco_base + "/sendMessage"
        dados = {"chat_id": id_da_conversa, "text": "Pessoa saiu"}
        resposta = post(endereco, json=dados)
    

# criação de componentes
aplicativo = None
tempo_aprox = 0
tempo_afast = 0
b1 = Button(11)
b2 = Button(12)
b3 = Button(13)
proximo_id_de_update = 0
l1 = LED(21)
campainha = Buzzer(16)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
player = Player()
sensor = DistanceSensor(trigger=17, echo=18)


b3.when_pressed = b3_pressed
b3.when_released = b3_released
sensor.when_in_range = sensor_aprox
sensor.when_out_of_range = sensor_afast

# loop infinito
while True: 
    endereco = endereco_base + "/getUpdates"
    dados = {"offset": proximo_id_de_update} 
    resposta = get(endereco, json = dados)
    dicionario_da_resposta = resposta.json() 
    for resultado in dicionario_da_resposta["result"]: 
        mensagem = resultado["message"] 
        if "text" in mensagem: 
            text = mensagem["text"]
            if text == "Abrir":
                l1.on()
            elif text == "Soar Alarme":
                campainha.beep(n = 5, on_time = 0.1, off_time = 0.1)
                
        elif "voice" in mensagem: 
            id_do_arquivo = mensagem["voice"]["file_id"]
            baixar_audio(id_do_arquivo)
            
            player.loadfile("audio_download.ogg")
            print("audio ok")
            
        
        elif "photo" in mensagem: 
            foto_mais_resolucao = mensagem["photo"][-1] 
            id_do_arquivo = foto_mais_resolucao["file_id"] 
        # depois baixa o arquivo e faz algo com ele...
        proximo_id_de_update = resultado["update_id"] + 1
    sleep(1)

