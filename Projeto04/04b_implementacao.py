# importação de bibliotecas
from os import system
from gpiozero import Button, LED, Buzzer
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from requests import post, get


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
        

# criação de componentes
b1 = Button(11)
b2 = Button(12)
proximo_id_de_update = 0
l1 = LED(21)
campainha = Buzzer(16)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

b1.when_pressed = campainha.on
b1.when_released = desliga_buz
b2.when_pressed = l1.off


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
        
        elif "photo" in mensagem: 
            foto_mais_resolucao = mensagem["photo"][-1] 
            id_do_arquivo = foto_mais_resolucao["file_id"] 
        # depois baixa o arquivo e faz algo com ele...
        proximo_id_de_update = resultado["update_id"] + 1
    sleep(1)
