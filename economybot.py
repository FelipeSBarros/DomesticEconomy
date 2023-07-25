import json
import os
import time
import urllib
from os.path import dirname, relpath

import requests

from dotenv import load_dotenv

from dbhelper import DBHelper
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
    categories.append("CANCEL")
    actions = db.get_actions()
    actions.append("CANCEL")
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
