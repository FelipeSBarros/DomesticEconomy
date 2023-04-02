# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 04:21:29 2018

@author: Felipe Sodre Mendes Barros
https://github.com/FelipeSBarros
"""

import json
import os
import time
import urllib  # to handle with special characters
from os.path import dirname, relpath

import requests

# from API import API # bot API.py
from dotenv import load_dotenv

from dbhelper import DBHelper  # import class and method created to work with sqlite3
from messages import WELCOME_MSG
from models import Session

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
NL = "\n"
db = DBHelper(Session)


def get_url(url):  # Function to get URL and set encode
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):  # function the get and return json from URL
    content = get_url(url)
    js = json.loads(content)
    return js


def get_last_update_id(updates):  # Function to calculate and get the last update id
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"  # todo use urllib?
    if offset:
        url += f"&offset={offset}"  # (in URLs, the argument list strats with ? but further arguments are separated with &).
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup=None, parse_mode="markdown"):
    text = urllib.parse.quote_plus(text)
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}&parse_mode={parse_mode}"
    if reply_markup:
        url += f"&reply_markup={reply_markup}"
    get_url(url)


def send_photo(chat_id, photo):
    data = {"chat_id": chat_id}
    url = URL + "sendPhoto"
    files = {"photo": (dirname(photo), open(relpath(photo), "rb"))}
    r = requests.get(url, data=data, files=files)


def send_action(chat_id, action="typing"):
    url = URL + f"sendChatAction?chat_id={chat_id}&action={action}"
    get_url(url)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def handle_updates(updates):
    categories = db.get_categories()
    actions = db.get_actions()
    for update in updates["result"]:
        try:
            if "from" in updates["result"][0]["message"].keys():
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

                for message in WELCOME_MSG:
                    send_message(message, chat)
                keyboard = build_keyboard(actions)
                send_message(
                    "what do you need to register?", chat, reply_markup=keyboard
                )

            elif text == "expenses" and not db.status:
                user = db.filter_user(user)
                db.update_model_user(user.id)
                action = db.filter_action(text)
                db.update_model_action(action.id)
                categories = db.get_categories()
                keyboard = build_keyboard(categories)
                send_message("In which category?", chat, reply_markup=keyboard)
                db.update_status("CATEGORY")

            elif db.status == "CATEGORY" and db.model.action:
                category = db.filter_category(text)
                db.update_model_category(category.id)
                subcategories = db.get_subcategories()
                keyboard = build_keyboard(subcategories)
                send_message("In which subcategory?", chat, reply_markup=keyboard)
                db.update_status("SUBCATEGORY")

            elif db.status == "SUBCATEGORY" and db.model.category:
                subcategory = db.filter_subcategory(text)
                db.update_model_subcategory(subcategory.id)
                # keyboard = build_keyboard(subcategories)
                send_message(
                    "How much?", chat
                )  # todo add buttons # , reply_markup=keyboard  #https://stackoverflow.com/questions/63415226/number-keyboard-for-python-telegram-bot
                db.update_status("VALUE")

            elif db.status == "VALUE" and db.model.subcategory:
                val = float(text)
                db.model.value = val
                db.save_expenses()
                keyboard = build_keyboard(actions)
                send_message(
                    "what do you need to register?", chat, reply_markup=keyboard
                )
                db.clean_model()

            # if text.startswith("income"):  # todo implementar
            #     action, value = text.split(" ")
            #     send_message("Saving income!!", chat)
            #     db.insertIncome(user, value, date.date.today())
            #     send_message(f"Well done!\n {value} inserted as income!", chat)
            #
            # if text == "/category":
            #     cats = db.get_category()
            #     send_message(
            #         "Your options for **category** are:\n\n{}".format("\n".join(cats)),
            #         chat,
            #     )  # todo usar f-string
            #
            # if text.startswith("/subcategory"):
            #     if len(text.split(" ")) == 1:
            #         subcats = db.get_subcategory()
            #         send_message(
            #             "*Subcategory* options:\n\n{}".format("\n".join(subcats)), chat
            #         )  # todo usar f-string
            #     if len(text.split(" ")) == 2:
            #         command, cat = text.split(" ")
            #         subcats = db.get_subcategory(cat)
            #         send_message(
            #             "*Subcategory* options for the category *{}*, are:\n\n{}".format(
            #                 cat, "\n".join(subcats)
            #             ),
            #             chat,
            #         )  # todo usar f-string
            #
            # if text.startswith("/summary"):
            #     if len(text.split(" ")) >= 2:
            #         param = text.split(" ")[1]
            #         if len(text.split(" ")) >= 3:
            #             month = text.split(" ")[2]
            #             month = month.zfill(2)
            #             year = date.date.today().year
            #             if len(text.split(" ")) == 4:
            #                 year = text.split(" ")[3]
            #         else:
            #             month = str(date.date.today().month).zfill(2)
            #             year = date.date.today().year
            #         summary = db.get_summary(param, month, year)
            #         send_message(
            #             f"*Summary by {param} for moth {month} and year {year}*:", chat
            #         )
            #         send_message("{summary}", chat)
            #     else:
            #         send_message(
            #             "*Wrong parameter sent!*\n you ust send:\n /summary [param] [month] [year]\n where [month] and [year] are optional",
            #             chat,
            #         )  # todo export to msg file
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
            #                 send_photo(chat_id=chat, photo=plot)
            #         elif path.startswith("Not"):
            #             send_message(path, chat)
            #         else:
            #             # print(path)
            #             send_photo(chat_id=chat, photo=path)
            #     else:
            #         send_message(
            #             "*Wrong parameter sent!*\n you ust send:\n /plot [param] [month] [year]",
            #             chat,
            #         )  # todo export to msg file
            #
            # if text.startswith("/backup"):
            #     send_message("Building databse backup", chat)
            #     db.sqlite3_backup()
            #     if len(text.split(" ")) == 2:
            #         NO_OF_DAYS = int(text.split(" ")[1])
            #         send_message(
            #             f"Removing backups with {NO_OF_DAYS} days or more", chat
            #         )
            #         db.clean_data(backup_dir="./backup", NO_OF_DAYS=NO_OF_DAYS)
            #     send_message("All done!", chat)
            #
            # if text.startswith("/sql"):
            #     sql = text[5:]
            #     msg = db.sql(sql)
            #     send_message(f"{msg}", chat)
            #
            # if text.startswith("/add"):
            #     if len(text.split(" ")) == 2:
            #         cats = db.get_category()
            #         value = text.split(" ")[1]
            #         if value not in cats:
            #             sql = f"INSERT INTO category(category) VALUES ('{value}')"
            #             msg = db.sql(sql)
            #             send_message("Value *{value}* added on databse", chat)
            #         else:
            #             msg = f"Not processed: Category *{value}* already exists;"
            #             send_message(msg, chat)
            #     if len(text.split(" ")) == 3:
            #         value, svalue = text.split(" ")[1:]
            #         sql = f"INSERT INTO subcategory(catid, subcategory, category) VALUES ((select id from category where category = '{value}'), '{svalue}', '{value}');"
            #         msg = db.sql(sql)  # todo remover
            #         msg = f"Value *{svalue}* added on database!"
            #         send_message(msg, chat)
            #

        except Exception as e:
            send_message(f"ERROR: {e}", chat)


def main():
    last_update_id = None
    while True:
        # print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates.get("result", [])) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
