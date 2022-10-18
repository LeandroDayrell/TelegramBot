from re import X
import telebot
import ast
import time
from telebot import types
from dbhelper import DBHelper
db = DBHelper()


key = None
bot = telebot.TeleBot("") # Adicionar a chave do grupo


startList= {"10": "Informações", "20": "Monitoria"}
listaInfo = {"11": "Instancia", "12": "Processo", "13": "Logins","102": "Voltar",}
listarProcesso = {"14": "Processos Ativos", "15": "Ativar", "16": "Desativar"}
listarLogins = {"17": "Logins ativo", "18": "Logins com defeito","103": "Voltar",}
listMonitoria = {"21": "Processamento de Vendas","40": "BackLog", "101":"Voltar"}
listProcessosDia = {"50": "Migracao", "51": "Portabilidade Talk", "52": "Controle Conta", "53": "Controle Controle", "54": "Conta Conta", "55": "Proposta (CB)", "56": "Private Label (PL)", "57": "Central Image (CI)","100": "Voltar"}

# Verifica no banco de dados se o Telefone pode ter acesso a resposta
def autenticadorTelefone(message):
    #print(message)
    x = db.getAutenticador(message)
    if x:
        return True
    else:
        return False
    
# Remoção de caracteres especificas
def replaceEspecifico(row):
    x = str(row)
    for char in ",()'[]":
        x = x.replace(char, "")
        #print(x)
    return x

def startList1():
    markup = types.InlineKeyboardMarkup()
    for key, value in startList.items():
        markup.add(types.InlineKeyboardButton(text=value,callback_data="['value', '" + value + "', '" + key + "']"))
    return markup


def makeKeyboardInformacoes():
    markup = types.InlineKeyboardMarkup()
    for key, value in listaInfo.items():
        markup.add(types.InlineKeyboardButton(text=value,callback_data="['value', '" + value + "', '" + key + "']"))
    return markup


def makeKeyboardMonitoria():
    markup = types.InlineKeyboardMarkup()
    for key, value in listMonitoria.items():
        markup.add(types.InlineKeyboardButton(text=value,callback_data="['value', '" + value + "', '" + key + "']"))
    return markup

def makeKeyboardProcessoAtivo():
    markup = types.InlineKeyboardMarkup()
    for key, value in listProcessosDia.items():
        markup.add(types.InlineKeyboardButton(text=value,callback_data="['value', '" + value + "', '" + key + "']"))

    return markup

def makeKeyboardProcessoCliente():
    markup = types.InlineKeyboardMarkup()
    for key, value in listarProcesso.items():
        markup.add(types.InlineKeyboardButton(text=value,callback_data="['value', '" + value + "', '" + key + "']"))

    return markup

def makeKeyboardProcessosDia():
    markup = types.InlineKeyboardMarkup()
    for key, value in listProcessosDia.items():
        markup.add(types.InlineKeyboardButton(text=value,callback_data="['value', '" + value + "', '" + key + "']"))

    return markup
def makeKeyboardLogins():
    markup = types.InlineKeyboardMarkup()
    for key, value in listarLogins.items():
        markup.add(types.InlineKeyboardButton(text=value,callback_data="['value', '" + value + "', '" + key + "']"))

    return markup


@bot.message_handler(commands=['rpa'])
def handle_command_adminwindow(message):

    if (autenticadorTelefone(message.from_user.id) == True):
        bot.send_message(chat_id=message.chat.id,text="Seja bem vindo, selecione abaixo",reply_markup=startList1(),parse_mode='HTML')

@bot.message_handler(commands=['start','help'])
def handle_command_help(message):
    bot.send_message(chat_id=message.chat.id,text="Olá! Me chamo Frode, seu atendente virtual e estou aqui para te auxiliar. Como posso te ajudar? \n\nTemos algumas opções para você\n/rpa < Clique para verificar sobre RPA\n/abrirchamado < Clique para abrir um chamado")

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Olá! Me chamo Frode, seu atendente virtual e estou aqui para te auxiliar. Como posso te ajudar? \n\nTemos algumas opções para você\n/rpa < Clique para verificar sobre RPA\n/abrirchamado < Clique para abrir um chamado"""
    bot.reply_to(mensagem, texto)

# keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row('Teste','button2')
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if (call.data.startswith("['value'")):
        #print(call.data.startswith)
        #print(call)
        groupTelegram = call.message.chat.id
        keyFromCallBack = ast.literal_eval(call.data)[2]
        key = keyFromCallBack

        if (key == '10'): # Informacoes
                bot.send_message(chat_id=groupTelegram,text="Essas são as opcões de informações gerais",reply_markup=makeKeyboardInformacoes(),parse_mode='HTML')

        if (key == '20'): # Monitoria
                bot.send_message(chat_id=groupTelegram,text="Essas são as opcões sobre monitoria, selecione o que lhe agrada",reply_markup=makeKeyboardMonitoria(),parse_mode='HTML')
        # Opcoes de voltar
        if (key == '100'): # Monitoria
            bot.send_message(chat_id=groupTelegram,text="Essas são as opcões sobre monitoria, selecione o que lhe agrada",reply_markup=makeKeyboardMonitoria(),parse_mode='HTML')
        if (key == '101'): # Monitoria
            bot.send_message(chat_id=groupTelegram,text="Seja bem vindo, selecione abaixo",reply_markup=startList1(),parse_mode='HTML')
        if (key == '102'): # Monitoria
            bot.send_message(chat_id=groupTelegram,text="Seja bem vindo, selecione abaixo",reply_markup=startList1(),parse_mode='HTML')
        if (key == '103'): # Monitoria
            bot.send_message(chat_id=groupTelegram,text="Essas são as opcões de informações gerais",reply_markup=makeKeyboardInformacoes(),parse_mode='HTML')
        ############################## INFOS ##############################

        if (key == '11'): #Instancia Ativo
            if (autenticadorTelefone(call.from_user.id) == True):
                #print(call.message.from_user.id)
                rows = db.getInstancia()
                bot.send_message(chat_id=groupTelegram,text="********* Instancias ativa: *********")
                for row in rows:
                    x = str(row)
                    mensagem = replaceEspecifico(x)
                    bot.send_message(chat_id=groupTelegram,text=""+mensagem+"")
                bot.send_message(chat_id=groupTelegram,text="****************")

        if (key == '12'): #Processos
            if (autenticadorTelefone(call.from_user.id) == True):
                bot.send_message(chat_id=groupTelegram,text="Aqui estão os processos, selecione para ver detalhes",reply_markup=makeKeyboardProcessoCliente(),parse_mode='HTML')
        
        if (key == '13'): #Logins
            if (autenticadorTelefone(call.from_user.id) == True):
                bot.send_message(chat_id=groupTelegram,text="Selecione para ver detalhes",reply_markup=makeKeyboardLogins(),parse_mode='HTML')

        if (key == '17'): #Logins ativos
            if (autenticadorTelefone(call.from_user.id) == True):
                rows = db.getLogins()
                bot.send_message(chat_id=groupTelegram,text="********* Logins ativo: *********")
                for row in rows:
                    x = str(row)
                    mensagem = replaceEspecifico(x)
                    bot.send_message(chat_id=groupTelegram,text=""+mensagem+"")
                bot.send_message(chat_id=groupTelegram,text="****************")

        if (key == '14'): #Processos ativos
            if (autenticadorTelefone(call.from_user.id) == True):
                rows = db.getProcesso()
                bot.send_message(chat_id=groupTelegram,text="********* Processos ativos: *********")
                for row in rows:
                    x = str(row)
                    mensagem = replaceEspecifico(x)
                    bot.send_message(chat_id=groupTelegram,text=""+mensagem+"")
                bot.send_message(chat_id=groupTelegram,text="****************")
        
        if (key == '18'): #Logins com Defeito
            if (autenticadorTelefone(call.from_user.id) == True):
                #print(call.message.from_user.id)
                rows = db.getLoginsComDefeito()
                bot.send_message(chat_id=groupTelegram,text="********* Logins com defeito: *********")
                for row in rows:
                    x = str(row)
                    mensagem = replaceEspecifico(x)
                    bot.send_message(chat_id=groupTelegram,text=""+mensagem+"")
                bot.send_message(chat_id=groupTelegram,text="****************")
        ############################## MONITORIA ##############################

        if (key == '21'): #Processos
            if (autenticadorTelefone(call.from_user.id) == True):
                bot.send_message(chat_id=groupTelegram,text="Aqui estão os processos, selecione para ver detalhes",reply_markup=makeKeyboardProcessosDia(),parse_mode='HTML')
        

        if (key == '50'): #Migração
            if (autenticadorTelefone(call.from_user.id) == True):
                processo = 3
                nomeProcesso = "Migração"
                getprocesso = db.getRegistroCliente(processo)
                bot.send_message(chat_id=groupTelegram,text="**"+nomeProcesso+"** \n"+getprocesso+" processos")
                bot.send_message(chat_id=groupTelegram,text="Aqui estão os processos, selecione para ver detalhes",reply_markup=makeKeyboardProcessosDia(),parse_mode='HTML')
        if (key == '51'): #Portabilidade Talk
            if (autenticadorTelefone(call.from_user.id) == True):
                processo = 17
                nomeProcesso = "Portabilidade Talk"
                getprocesso = db.getRegistroCliente(processo)
                bot.send_message(chat_id=groupTelegram,text="**"+nomeProcesso+"** \n"+getprocesso+" processos")
                bot.send_message(chat_id=groupTelegram,text="Aqui estão os processos, selecione para ver detalhes",reply_markup=makeKeyboardProcessosDia(),parse_mode='HTML')
        
        if (key == '52'): #Controle Conta
            if (autenticadorTelefone(call.from_user.id) == True):
                processo = 1
                nomeProcesso = "Controle Conta"
                getprocesso = db.getRegistroCliente(processo)
                bot.send_message(chat_id=groupTelegram,text="**"+nomeProcesso+"** \n"+getprocesso+" processos")
                bot.send_message(chat_id=groupTelegram,text="Aqui estão os processos, selecione para ver detalhes",reply_markup=makeKeyboardProcessosDia(),parse_mode='HTML')
        
        if (key == '53'): #Controle Controle
            if (autenticadorTelefone(call.from_user.id) == True):
                processo = 9
                nomeProcesso = "Controle Controle"
                getprocesso = db.getRegistroCliente(processo)
                bot.send_message(chat_id=groupTelegram,text="**"+nomeProcesso+"** \n"+getprocesso+" processos")
                bot.send_message(chat_id=groupTelegram,text="Aqui estão os processos, selecione para ver detalhes",reply_markup=makeKeyboardProcessosDia(),parse_mode='HTML')
        
        if (key == '54'): #Conta Conta
            if (autenticadorTelefone(call.from_user.id) == True):
                processo = 10
                nomeProcesso = "Conta Conta"
                getprocesso = db.getRegistroCliente(processo)
                bot.send_message(chat_id=groupTelegram,text="**"+nomeProcesso+"** \n"+getprocesso+" processos")
                bot.send_message(chat_id=groupTelegram,text="Aqui estão os processos, selecione para ver detalhes",reply_markup=makeKeyboardProcessosDia(),parse_mode='HTML')
       
        if (key == '55'): #Proposta (CB)
            if (autenticadorTelefone(call.from_user.id) == True):
                processo = 18
                nomeProcesso = "Proposta (CB)"
                getprocesso = db.getRegistroCliente(processo)
                bot.send_message(chat_id=groupTelegram,text="**"+nomeProcesso+"** \n"+getprocesso+" processos")
                bot.send_message(chat_id=groupTelegram,text="Aqui estão os processos, selecione para ver detalhes",reply_markup=makeKeyboardProcessosDia(),parse_mode='HTML')

        if (key == '56'): #Private Label (PL)
            if (autenticadorTelefone(call.from_user.id) == True):
                processo = 19
                nomeProcesso = "Private Label (PL)"
                getprocesso = db.getRegistroCliente(processo)
                bot.send_message(chat_id=groupTelegram,text="**"+nomeProcesso+"** \n"+getprocesso+" processos")
                bot.send_message(chat_id=groupTelegram,text="Aqui estão os processos, selecione para ver detalhes",reply_markup=makeKeyboardProcessosDia(),parse_mode='HTML')

        if (key == '57'): #Processos
            if (autenticadorTelefone(call.from_user.id) == True):
                processo = 20
                nomeProcesso = "Central Image (CI)"
                getprocesso = db.getRegistroCliente(processo)
                bot.send_message(chat_id=groupTelegram,text="**"+nomeProcesso+"** \n"+getprocesso+" processos")
                bot.send_message(chat_id=groupTelegram,text="Aqui estão os processos, selecione para ver detalhes",reply_markup=makeKeyboardProcessosDia(),parse_mode='HTML')
        if (key == '40'): #backlog geral
            if (autenticadorTelefone(call.from_user.id) == True):
                bot.send_message(chat_id=groupTelegram,text="Aguarde enquanto estamos retornando os dados")
                rows = db.getBacklog()
                bot.send_message(chat_id=groupTelegram,text="********* BackLog Geral *********")
                for row in rows:
                    x = str(row)
                    mensagem = replaceEspecifico(x)
                    bot.send_message(chat_id=groupTelegram,text=""+mensagem+"")
                bot.send_message(chat_id=groupTelegram,text="****************")
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)