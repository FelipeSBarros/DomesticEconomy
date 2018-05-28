# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 04:21:29 2018

@author: Felipe Sodre Mendes Barros
https://github.com/FelipeSBarros
"""

from flask import Flask, request
import telepot
import urllib3
import json
from API import API # bot API
import time
import urllib # to handle with pecial characters
import datetime as date # to manage date and time
from dbZeroEuro import DBHelper # import class and method created to work with sqlite3
from os.path import dirname, relpath
import pandas as pd

db = DBHelper()

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "***********"
bot = telepot.Bot(API)
bot.setWebhook("https://****USER****.pythonanywhere.com/{}".format(secret), max_connections=1)

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        user = update["message"]["from"]["first_name"]
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]

        if text == "/start":
            bot.sendMessage(chat_id, "Welcome to Dosmestic Economy Bot! Your personal assistent, {}!!".format(user), parse_mode = 'markdown')
            users = db.get_users()
            bot.sendMessage(chat_id, "{}!!".format(users), parse_mode = 'markdown')
            if user not in users:
                db.insertuser(user, chat_id)

        if text.startswith("/expenses"):
            if len(text.split(" "))<4:
                bot.sendMessage(chat_id, "Sorry, I couldnt save your expenses. Something is missing", parse_mode = 'markdown')
            else:
                action, value, category, subcategory = text.split(" ")
                db.insertExpenses(user, category, subcategory, float(value), date.date.today())
                bot.sendMessage(chat_id, "Ok, I'm done!\n {} inserted as expenses".format(value), parse_mode = 'markdown')

        if text.startswith("/income"):
            action, value = text.split(" ")
            bot.sendMessage(chat_id, "Saving income!!", parse_mode = 'markdown')
            db.insertIncome(user, value, date.date.today())
            bot.sendMessage(chat_id, "Well done!\n {} inserted as income!".format(value), parse_mode = 'markdown')

        if text == "/category":
            cats = db.get_category()
            bot.sendMessage(chat_id, "Your options for **category** are:\n\n{}".format('\n'.join(cats)), parse_mode = 'markdown')

        if text.startswith("/subcategory"):
            if len(text.split(" "))==1:
                subcats = db.get_subcategory()
                bot.sendMessage(chat_id, "*Subcategory* options:\n\n{}".format('\n'.join(subcats)), parse_mode = 'markdown')
            if len(text.split(" "))==2:
                command, cat = text.split(" ")
                subcats = db.get_subcategory(cat)
                bot.sendMessage(chat_id, "*Subcategory* options for the category *{}*, are:\n\n{}".format(cat, '\n'.join(subcats)), parse_mode = 'markdown')

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
                bot.sendMessage(chat_id, "*Summary by {} for moth {} and year {}*:".format(param, month, year), parse_mode = 'markdown')
                bot.sendMessage(chat_id, "{}".format(summary), parse_mode = 'markdown')
            else:
                bot.sendMessage(chat_id, "*Wrong parameter sent!*\n you ust send:\n /summary [param] [month] [year]\n where [month] and [year] are optional", parse_mode = 'markdown')

        if text.startswith("/plot"):
            #bot.sendMessage(chat_id, "/plot [param] [month] [year]")
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
                if path.startswith('Not'):
                    bot.sendMessage(chat_id, path, parse_mode = 'markdown')
                elif len(path) > 1:
                    for plot in path:
                        graph = open(relpath(plot), "rb")
                        sendPhoto(chat_id, graph)
                else:
                    graph = open(relpath(path), "rb")
                    #graph = {'photo': (dirname(photo), open(relpath(photo), "rb"))}
                    bot.sendPhoto(chat_id, graph)
            else:
                bot.sendMessage(chat_id, "*Wrong parameter sent!*\n you ust send:\n /plot [param] [month] [year]", parse_mode = 'markdown')


        if text.startswith("/backup"):
            bot.sendMessage(chat_id, "Building databse backup", parse_mode = 'markdown')
            db.sqlite3_backup()
            if len(text.split(" "))==2:
                NO_OF_DAYS = int(text.split(" ")[1])
                bot.sendMessage(chat_id, "Removing backups with {} days or more".format(NO_OF_DAYS), parse_mode = 'markdown')
                db.clean_data(backup_dir = './backup', NO_OF_DAYS = NO_OF_DAYS)
            bot.sendMessage(chat_id, "All done!", parse_mode = 'markdown')

        if text.startswith("/sql"):
            sql = text[5:]
            msg = db.sql(sql)
            bot.sendMessage(chat_id, "{}".format(msg), parse_mode = 'markdown')

        if text.startswith("/add"):
            if len(text.split(" ")) == 2:
                cats = db.get_category()
                value = text.split(" ")[1]
                if value not in cats:
                    sql = "INSERT INTO category(category) VALUES ('{}')".format(value)
                    msg = db.sql(sql)
                    bot.sendMessage(chat_id, "Value *{}* added on databse".format(value), parse_mode = 'markdown')
                else:
                    msg = 'Not processed: Category *{}* already exists;'.format(value)
                    bot.sendMessage(chat_id, msg, parse_mode = 'markdown')
            if len(text.split(" ")) == 3:
                value, svalue = text.split(" ")[1:]
                sql = "INSERT INTO subcategory(catid, subcategory, category) VALUES ((select id from category where category = '{}'), '{}', '{}');".format(value, svalue, value)
                msg = db.sql(sql)
                msg = "Value *{}* added on database!".format(svalue)
                bot.sendMessage(chat_id, msg, parse_mode = 'markdown')

    return "OK"
