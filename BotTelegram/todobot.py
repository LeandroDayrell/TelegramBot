
import json # Utilizar para retornar os dados
import requests #Interagir com API do telegram
import time
import urllib
import asyncio

#import config

from dbhelper import DBHelper

db = DBHelper()

TOKEN = "https://api.telegram.org/bot5509513581:AAH_8uhOCOvuQoWKECtDQg7b7muoBFclbY4"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)



## nomes de teste
alianca = "Alianca"
action = "Action"
instancia = "Instancia"
info = "Informações"
monitoria = "Monitoria"
sair = "Sair"


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

async def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)




async def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        #items = db.get_items(chat)
        if text == "/done":
            names = "Leandro1","Paulo1"
            keyboard = await build_keyboard(names)
            keyboard
            send_message("Voce utilizou o /info", chat, keyboard)
            print(text)
            if (keyboard.find("Leandro1")):
                print("Passou Leandro")
            else:
                print("Deu Erro")
        elif text == "/start":
            await send_message("Bem vindo, escolha umas das opcoes /info /start /done", chat)
        elif text == "/info":
            names = "Leandro","Paulo"
            keyboard = await build_keyboard(names)
            await send_message("Voce utilizou o /info", chat, keyboard)
            if (keyboard.find("Leandro")):
                names = "Pedro","Fernando"
                keyboard = await build_keyboard(names)
                await send_message("Voce escolheu 01", chat, keyboard)
                if (keyboard.find("Pedro")):
                    keyboard = await build_keyboard(names)
                    await send_message("Voce escolheu o 02", chat, keyboard)
                    print("Testeeee")
            else:
                print("Deu Erro")
        #else:
            #db.add_item(text, chat)
            #items = db.get_items(chat)
            #message = "\n".join(items)
            #send_message("ULTIMO ELIF", chat)
            #send_message(text, chat)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


# def build_keyboard(name):
#     keyboard = item in name
#     print(keyboard)
#     reply_markup = {"keyboard":keyboard, "one_time_keyboard": True, "resize_keyboard": True}
#     return json.dumps(reply_markup)

async def build_keyboard(names):
    keyboard = [names]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True, "resize_keyboard": True, "row":names}
    return json.dumps(reply_markup)


async def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


async def main():
    #db.setup()
    last_update_id = None
    while True:
        updates = await get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            await handle_updates(updates)
        time.sleep(0.5)


if __name__ ==  '__main__':
    asyncio.run(main())