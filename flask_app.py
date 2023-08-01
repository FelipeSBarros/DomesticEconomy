# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 04:21:29 2018

@author: Felipe Sodre Mendes Barros
https://github.com/FelipeSBarros
"""

import datetime as date  # to manage date and time
import os
from os.path import relpath

import telepot
import urllib3
from dotenv import load_dotenv
from flask import Flask, request

from dbhelper import DBHelper  # import class and method created to work with sqlite3
from economybot import send_message, build_keyboard
from messages import WELCOME_MSG

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
PYANYWHERE_SECRET = os.getenv("PYANYWHERE_SECRET")
PYANYWHERE_USER = os.getenv("PYANYWHERE_USER")
db = DBHelper()

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    "default": urllib3.ProxyManager(
        proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30
    ),
}
telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager,
    dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30),
)

bot = telepot.Bot(BOT_TOKEN)
bot.setWebhook(
    f"https://{PYANYWHERE_USER}.pythonanywhere.com/{PYANYWHERE_SECRET}",
    max_connections=1,
)

app = Flask(__name__)


@app.route("/{}".format(PYANYWHERE_SECRET), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    categories = db.get_categories()
    categories.append("CANCEL")
    actions = db.get_actions()
    actions.append("CANCEL")
    try:
        if "message" in update:
            if "from" in update.get("message").keys():
                user = update["message"]["from"]["first_name"]
            else:
                user = update["message"]["chat"]["first_name"]
            registered_user = db.filter_user(user)
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]

            if text == "/start":
                send_message(
                    f"Welcome to Dosmestic Economy Bot! Your personal assistent, {user}!!",
                    chat,
                )
                if not registered_user:
                    db.insertuser(user, chat)
                db.clean_model()
                keyboard = build_keyboard(actions)
                send_message(WELCOME_MSG, chat, reply_markup=keyboard)

            elif text == "CANCEL":
                db.clean_model()
                keyboard = build_keyboard(actions)
                send_message(WELCOME_MSG, chat, reply_markup=keyboard)

            elif text == "expenses" and not db.status:
                user = db.filter_user(user)
                db.update_model_user(user.id)
                action = db.filter_action(text)
                db.update_model_action(action.id)
                keyboard = build_keyboard(categories)
                send_message("In which category?", chat, reply_markup=keyboard)
                db.update_status("CATEGORY")

            elif db.status == "CATEGORY" and db.model.action_id:
                category = db.filter_category(text)
                db.update_model_category(category.id)
                subcategories = db.get_subcategories()
                subcategories.append("CANCEL")
                keyboard = build_keyboard(subcategories)
                send_message("In which subcategory?", chat, reply_markup=keyboard)
                db.update_status("SUBCATEGORY")

            elif db.status == "SUBCATEGORY" and db.model.category_id:
                subcategory = db.filter_subcategory(text)
                db.update_model_subcategory(subcategory.id)
                keyboard = build_keyboard(["CANCEL"])
                send_message("How much?", chat, reply_markup=keyboard)
                db.update_status("VALUE")

            elif db.status == "VALUE" and db.model.subcategory_id:
                val = float(text)
                db.model.value = val
                db.save_expenses()
                keyboard = build_keyboard(actions)
                send_message(WELCOME_MSG, chat, reply_markup=keyboard)
                db.clean_model()
    except Exception as e:
        send_message(f"ERROR: {e}", chat)
        #
        #
        # if text.startswith("/plot"):
        #     if len(text.split(" ")) >= 2:
        #         param = text.split(" ")[1]
        #         if len(text.split(" ")) >= 3:
        #             month = text.split(" ")[2].zfill(2)
        #             year = date.date.today().year
        #             if len(text.split(" ")) == 4:
        #                 year = text.split(" ")[3]
        #         else:
        #             month = str(date.date.today().month).zfill(2)
        #             year = date.date.today().year
        #         path = db.get_plots(param, month, year)
        #         if isinstance(path, list):
        #             for plot in path:
        #                 graph = open(relpath(plot), "rb")
        #                 bot.sendPhoto(chat_id, graph)
        #         elif path.startswith("Not"):
        #             bot.sendMenssage(chat_id, path)
        #         else:
        #             graph = open(relpath(path), "rb")
        #             bot.sendPhoto(chat_id, graph)
        #     else:
        #         bot.sendMessage(
        #             chat_id,
        #             "*Wrong parameter sent!*\n you ust send:\n /plot [param] [month] [year]",
        #             parse_mode="markdown",
        #         )
        #
        # if text.startswith("/backup"):
        #     bot.sendMessage(chat_id, "Building databse backup", parse_mode="markdown")
        #     db.sqlite3_backup()
        #     if len(text.split(" ")) == 2:
        #         NO_OF_DAYS = int(text.split(" ")[1])
        #         bot.sendMessage(
        #             chat_id,
        #             "Removing backups with {} days or more".format(NO_OF_DAYS),
        #             parse_mode="markdown",
        #         )
        #         db.clean_data(backup_dir="./backup", NO_OF_DAYS=NO_OF_DAYS)
        #     bot.sendMessage(chat_id, "All done!", parse_mode="markdown")
        #
        # if text.startswith("/sql"):
        #     sql = text[5:]
        #     msg = db.sql(sql)
        #     bot.sendMessage(chat_id, "{}".format(msg), parse_mode="markdown")
        #
        # if text.startswith("/add"):
        #     if len(text.split(" ")) == 2:
        #         cats = db.get_category()
        #         value = text.split(" ")[1]
        #         if value not in cats:
        #             sql = "INSERT INTO category(category) VALUES ('{}')".format(value)
        #             msg = db.sql(sql)
        #             bot.sendMessage(
        #                 chat_id,
        #                 "Value *{}* added on databse".format(value),
        #                 parse_mode="markdown",
        #             )
        #         else:
        #             msg = "Not processed: Category *{}* already exists;".format(value)
        #             bot.sendMessage(chat_id, msg, parse_mode="markdown")
        #     if len(text.split(" ")) == 3:
        #         value, svalue = text.split(" ")[1:]
        #         sql = "INSERT INTO subcategory(catid, subcategory, category) VALUES ((select id from category where category = '{}'), '{}', '{}');".format(
        #             value, svalue, value
        #         )
        #         msg = db.sql(sql)
        #         msg = "Value *{}* added on database!".format(svalue)
        #         bot.sendMessage(chat_id, msg, parse_mode="markdown")

    return "OK"
