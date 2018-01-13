# -*- coding: utf-8 -*-
"""
https://github.com/python-telegram-bot/python-telegram-bot
Created on Fri Jan 12 04:21:29 2018

@author: felipe
"""

import json 
import requests
from API import API # bot API
import time
import urllib #to handle with pecial characters
# from dbhelper import DBHelper # import class and method created to work with sqlite3
from dbZeroEuro import DBHelper

TOKEN = API
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
db = DBHelper()
db.setup()

def get_url(url): # Function to get URL and set encode
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url): # function the get and return json from URL
    content = get_url(url)
    js = json.loads(content)
    return js

def get_last_update_id(updates): #Function to calculate and get the last update id
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)
    
def handle_updates(updates):
    
    for update in updates["result"]:
        try:
            user = update["message"]["chat"]["first_name"]
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            cats = db.get_category()
            #receita = None
            #items = db.get_items(chat)
            if text == "/start": 
                send_message("Welcome to your personal assistent, {}!!".format(user), chat) #confirmar se vai funcionar
                send_message("I'm organizing everything until we can begin!", chat)
                db.insertuser(user, chat)
                send_message("Ok, all done! write /insert to open menu", chat)
            elif text == "/setup": 
                send_message("OK, Setting up the data base!!!")
                db.setup()
            elif text == "/insert":
                # Getting action
                actions = db.get_action()
                action = build_keyboard(actions)
                send_message("select what you intend to do: ", chat, action)
            if text == "receita":
                send_message("OK, tell me the value of your income:", chat)
                receita = True
            
            try:
                receita
            except NameError:
                send_message("Continue!!", chat)
            else:
                if receita:
                    db.insertIncome(user, int(text))
                    send_message("OK!!", chat)
            if text == 'gastos':
                #Getting catgory
                #cats = db.get_category()
                cat = build_keyboard(cats)
                send_message("select the cathegory: ", chat, cat)
            if text in cats:
                db.insertExpenses(user, text, value)
            #elif text.startswith("/"):
            #    continue
            #elif text in items:
            #    db.delete_item(text, chat)
            #    items = db.get_items(chat)
            #    keyboard = build_keyboard(items)
            #    send_message("select an item to delete: ", chat, keyboard)
            #else:                
            #    db.add_item(text, chat)
            #    items = db.get_items(chat)
            #    message = "\n".join(items)
            #    send_message(message, chat)
        except KeyError:
            pass
            
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset) #  (in URLs, the argument list strats with ? but further arguments are separated with &).
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup = None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)
    
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard" : keyboard, "one_time_keyboard" : True}
    return json.dumps(reply_markup)
    
def get_doaction(doaction = None):
    return doaction
    
def main():
    #db.setup()
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"])>0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()