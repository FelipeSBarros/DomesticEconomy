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
import urllib # to handle with pecial characters
import datetime as date # to manage date and time
from dbZeroEuro import DBHelper # import class and method created to work with sqlite3

TOKEN = API
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
db = DBHelper()

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

def send_message(text, chat_id, parse_mode = 'markdown', reply_markup = None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode={}".format(text, chat_id, parse_mode)
    if reply_markup:
        url += "reply_markup={}".format(reply_markup)
    get_url(url)
    
def send_action(chat_id, action = 'typing'):
    url = URL + "sendChatAction?chat_id={}&action={}".format(chat_id, action)
    get_url(url)
    
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard" : keyboard, "one_time_keyboard" : True}
    return json.dumps(reply_markup)
    
def handle_updates(updates):
    
    for update in updates["result"]:
        try:
            user = update["message"]["chat"]["first_name"]
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            
            if text == "/start": 
                #send_action(chat)
                send_message("Welcome to Dosmestic Economy Bot! Your personal assistent, {}!!".format(user), chat) #confirmar se vai funcionar
                #send_action(chat)
                users = db.get_users()
                if user not in users:
                    db.insertuser(user, chat)
                send_message("Before we can start, a few tips ans tricks: \n *Use:* \n `/insert [value] [category] [subcategory]` \n to insert a expenses, WHERE *value* is a number; \n *Exemple:* \n `/insert Casa Comida 100`", chat)
                send_action(chat)
                send_message("To know the *categorys* you cna use, just type `/category` and I send you the options you have. \n The same for *subcategory* (just write `/subcategory`)", chat)
                
            elif text[0:7] == "/insert":
                action, value, category, subcategory = text.split(" ")
                send_message("Organizing the data {}".format(text), chat)
                #send_message("Date: {}".format(date.date(date)), chat)
                db.insertExpenses(user, category, subcategory, int(value), date.date.today())
                send_message("select Well done! {} inserted as expenses".format(value), chat)

            if text == "/category":
                cats = db.get_category()
                #cats = [[cats] for category in cats]
                send_message("Your options for **category** are:\n\n{}".format('\n'.join(cats)), chat)
            
            if text == "/subcategory":
                subcats = db.get_subcategory()
                #cats = [[cats] for category in cats]
                send_message("Your options for **category** are:\n\n{}".format('\n'.join(subcats)), chat)    

        except KeyError:
            pass
            
def main():
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