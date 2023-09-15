# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
# DEPOIS FAÇA OS NOVOS RECURSOS

# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS

# importação de bibliotecas
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient, ASCENDING, DESCENDING
from lirc import init, nextcode
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from gpiozero import Buzzer, Button, DistanceSensor, LED
from datetime import datetime, timedelta

# a linha abaixo apaga todo o banco e reinsere os moradores
#redefinir_banco()

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]
entradas = banco["entradas"]
tentativas = banco["tentativas"]

# definição de funções
def valida_apt(apt):
    dados = {"apartamento": apt}
    if colecao.find_one(dados):
        ordenacao = [["data", DESCENDING]]
        busca = tentativas.find_one({"apartamento": apt}, sort = ordenacao)
        if busca == None:
            return True
        else:
            data_tentativa = busca["data"]
            data_agora = datetime.now()
            data_dif = data_agora - data_tentativa
            tempo = 15*(int(busca["tentativas incorretas"])-2)
            if busca["tentativas incorretas"]>2 and data_dif.total_seconds()<tempo:
                return tempo-data_dif.total_seconds()
        return True
    else:
        return False
    
def busca_nome(apt, senha):
    dados = {"apartamento": apt, "senha": senha}
    agora = datetime.now()
    ordenacao = [["data", DESCENDING]]
    busca = colecao.find_one(dados)
    if busca == None:
        ndados = {"apartamento": apt}
        ordenacao = [["data", DESCENDING]]
        nbusca = tentativas.find_one({"apartamento": apt}, sort = ordenacao)
        if nbusca == None:
            dados_erro = {"data": agora, "apartamento": apt, "tentativas incorretas":1}
            tentativas.insert(dados_erro)
        else:
            qtd = int(nbusca["tentativas incorretas"])+1
            dados_erro = {"data": agora, "apartamento": apt, "tentativas incorretas":qtd}
            tentativas.insert(dados_erro)
        return None
    
    dados_erro = {"data": agora, "apartamento": apt, "tentativas incorretas":0}
    tentativas.insert(dados_erro)
    return busca["nome"]

def coleta_digito(mensagem):
    dado = ""
    temp = 0
    lcd.clear()
    lcd.message(mensagem)
    while True:
        lcd.clear()
        lcd.message(mensagem+"\n")
        lista_com_codigo = nextcode()
        if lista_com_codigo != []:
            campainha.beep(on_time=0.2, off_time=0.2, n=1)
            codigo = lista_com_codigo[0]
            if codigo == "KEY_OK":
                temp = 0
                break
            dado = dado + str(codigo[-1])
            temp+=1
        lcd.message("*"*temp)
        sleep(0.1)
    
    return dado

# criação de componentes
init("aula", blocking=False)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
campainha = Buzzer(16)
sensor = DistanceSensor(trigger=17, echo=18)
b1 = Button(11)

# loop infinito
sensor.threshold_distance = 0.1

def rotina_entrada():
    apt = coleta_digito("Digite o apto:")
    if valida_apt(apt) == True:
        senha = coleta_digito("Digite a senha:")
        nome = busca_nome(apt, senha)
        if nome:
            lcd.clear()
            lcd.message("Bem vindo (a)\n"+nome+"!")
            agora = datetime.now()
            dado = {"apartamento": apt, "data": agora, "nome": nome}
            sleep(1)
        else:
            lcd.clear()
            lcd.message("Acesso negado")
            agora = datetime.now()
            dado = {"apartamento": apt, "data": agora}
            campainha.beep(on_time=0.2, off_time=0.2, n=3)
            sleep(1)
        entradas.insert(dado)
    elif valida_apt(apt) == False:
        lcd.clear()
        lcd.message("Apartamento\ninvalido!")
        campainha.beep(on_time=0.2, off_time=0.2, n=3)
        sleep(1)
    else:
        tempo = int(valida_apt(apt))
        lcd.clear()
        lcd.message("Bloqueado por\n"+str(tempo)+" segundos")
        sleep(1)
        
def verifica_entrada():
    apt = coleta_digito("Modo Check:")
    info = {"apartamento": apt}
    ordenacao = [["data", DESCENDING]]
    dados = list(entradas.find(info, sort = ordenacao))
    for dado in dados:
        if "nome" in dado:
            print(dado["data"].strftime("%d/%m (%H:%M):") + dado["nome"])
        else:
            print(dado["data"].strftime("%d/%m (%H:%M):") + "SENHA INCORRETA")
        
sensor.when_in_range = rotina_entrada
b1.when_pressed = verifica_entrada

# Testes
##print( valida_apt("102") )
##print( valida_apt("000") )
##print( busca_nome("102", "102001") )
##print( busca_nome("102", "00") )
##print( coleta_digito("Digite o apto:") )
##print( coleta_digito("Digite a senha:") )
