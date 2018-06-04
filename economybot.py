# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 04:21:29 2018

@author: Felipe Sodre Mendes Barros
https://github.com/FelipeSBarros
"""

import json 
import requests
from API import API # bot API
import time
import urllib # to handle with pecial characters
import datetime as date # to manage date and time
from dbZeroEuro import DBHelper # import class and method created to work with sqlite3
from os.path import dirname, relpath
import pandas as pd

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

def send_photo(chat_id, photo):
    data = {'chat_id': chat_id}
    url = URL + 'sendPhoto'
    files = {'photo': (dirname(photo), open(relpath(photo), "rb"))}
    r = requests.get(url, data=data, files=files)
    
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
            if "from" in updates['result'][0]['message'].keys():
                user = update["message"]["from"]["first_name"]
            else:
                user = update["message"]["chat"]["first_name"]
            
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            
            if text == "/start": 
                send_message("Welcome to Dosmestic Economy Bot! Your personal assistent, {}!!".format(user), chat) #confirmar se vai funcionar
                users = db.get_users()
                if user not in users:
                    db.insertuser(user, chat)
                send_message("Before we can start, a few tips ans tricks: \n *Use:* \n `/expenses [value] [category] [subcategory]` \n to insert a expenses, WHERE *value* is a number; \n *Exemple:* \n `/expenses 100 alimentacao restaurante`", chat)
                send_action(chat)
                send_message("To know the *category* you can use, just type `/category` and I send you the options you have. \n The same for *subcategory* (just write `/subcategory`)", chat)
                send_action(chat)
                send_message("Also, you can save your incomes! Just type `/income [value]` \n `/income 1000`", chat)
                
            if text.startswith("/expenses"):
                if len(text.split(" "))<4:
                    send_message("Sorry, I couldnt save your expenses. Something is missing", chat)
                else:
                    action, value, category, subcategory = text.split(" ")
                    db.insertExpenses(user, category, subcategory, float(value), date.date.today())
                    send_message("Ok, I'm done!\n {} inserted as expenses".format(value), chat)

            if text.startswith("/income"):
                action, value = text.split(" ")
                send_message("Saving income!!", chat)
                db.insertIncome(user, value, date.date.today())
                send_message("Well done!\n {} inserted as income!".format(value), chat)
                
            if text == "/category":
                cats = db.get_category()
                send_message("Your options for **category** are:\n\n{}".format('\n'.join(cats)), chat)
            
            if text.startswith("/subcategory"):
                if len(text.split(" "))==1:
                    subcats = db.get_subcategory()
                    send_message("*Subcategory* options:\n\n{}".format('\n'.join(subcats)), chat)    
                if len(text.split(" "))==2:
                    command, cat = text.split(" ")
                    subcats = db.get_subcategory(cat)
                    send_message("*Subcategory* options for the category *{}*, are:\n\n{}".format(cat, '\n'.join(subcats)), chat)
            
            if text.startswith("/summary"):
                if len(text.split(" "))>=2:
                    param = text.split(" ")[1]
                    if len(text.split(" "))>=3:
                        month = text.split(" ")[2]
                        month = month.zfill(2)
                        year = date.date.today().year
                        if len(text.split(" "))==4:
                            year = text.split(" ")[3]
                    else:
                        month = str(date.date.today().month).zfill(2)
                        year = date.date.today().year
                    summary = db.get_summary(param, month, year)
                    send_message("*Summary by {} for moth {} and year {}*:".format(param, month, year), chat)
                    send_message("{}".format(summary), chat)
                else:
                    send_message("*Wrong parameter sent!*\n you ust send:\n /summary [param] [month] [year]\n where [month] and [year] are optional", chat)

            if text.startswith("/plot"):
                if len(text.split(" "))>=2:
                    param = text.split(" ")[1]
                    if len(text.split(" "))>=3:
                        month = text.split(" ")[2].zfill(2)
                        year = date.date.today().year
                        if len(text.split(" "))==4:
                            year = text.split(" ")[3]
                    else:
                        month = str(date.date.today().month).zfill(2)
                        year = date.date.today().year
                    path = db.get_plots(param, month, year)
                    if isinstance(path, list):
                        for plot in path:
                            send_photo(chat_id=chat, photo=plot)
                    elif path.startswith('Not'):
                        send_message(path, chat)
                    else:
                        #print(path)
                        send_photo(chat_id = chat, photo = path)
                else:
                    send_message("*Wrong parameter sent!*\n you ust send:\n /plot [param] [month] [year]", chat)    

            if text.startswith("/backup"):
                send_message("Building databse backup", chat)    
                db.sqlite3_backup()
                if len(text.split(" "))==2:
                    NO_OF_DAYS = int(text.split(" ")[1])
                    send_message("Removing backups with {} days or more".format(NO_OF_DAYS), chat)    
                    db.clean_data(backup_dir = './backup', NO_OF_DAYS = NO_OF_DAYS)
                send_message("All done!", chat)    
            
            if text.startswith("/sql"):
                sql = text[5:]
                msg = db.sql(sql)
                send_message("{}".format(msg), chat)
            
            if text.startswith("/add"):
                if len(text.split(" ")) == 2:                
                    cats = db.get_category()
                    value = text.split(" ")[1]
                    if value not in cats:
                        sql = "INSERT INTO category(category) VALUES ('{}')".format(value)
                        msg = db.sql(sql)
                        send_message("Value *{}* added on databse".format(value), chat)
                    else:
                        msg = 'Not processed: Category *{}* already exists;'.format(value)
                        send_message(msg, chat)
                if len(text.split(" ")) == 3:
                    value, svalue = text.split(" ")[1:]
                    sql = "INSERT INTO subcategory(catid, subcategory, category) VALUES ((select id from category where category = '{}'), '{}', '{}');".format(value, svalue, value)
                    msg = db.sql(sql)
                    msg = "Value *{}* added on database!".format(svalue)
                    send_message(msg, chat)
        
        except KeyError:
            pass
        

def main():
    last_update_id = None
    while True:
        #print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"])>0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
