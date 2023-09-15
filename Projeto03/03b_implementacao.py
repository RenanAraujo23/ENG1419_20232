# importação de bibliotecas
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient
from lirc import init, nextcode
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep


# a linha abaixo apaga todo o banco e reinsere os moradores
redefinir_banco()

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]


# definição de funções
def valida_apt(apt):
    dados = {"apartamento": apt}
    if colecao.find_one(dados):
        return True
    else:
        return False
    
def busca_nome(apt, senha):
    dados = {"apartamento": apt, "senha": senha}
    busca = colecao.find_one(dados)
    if busca == None:
        return None
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

# loop infinito
while True:
    apt = coleta_digito("Digite o apto:")
    if valida_apt(apt):
        senha = coleta_digito("Digite a senha:")
        nome = busca_nome(apt, senha)
        if nome:
            lcd.clear()
            lcd.message("Bem vindo (a)\n"+nome+"!")
            sleep(1)
        else:
            lcd.clear()
            lcd.message("Acesso negado")
            sleep(1)
    else:
        lcd.clear()
        lcd.message("Apartamento\ninvalido!")
        sleep(1)


# Testes
##print( valida_apt("102") )
##print( valida_apt("000") )
##print( busca_nome("102", "102001") )
##print( busca_nome("102", "00") )
##print( coleta_digito("Digite o apto:") )
##print( coleta_digito("Digite a senha:") )

