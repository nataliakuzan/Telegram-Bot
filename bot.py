from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import requests
import re
from dotenv import load_dotenv
import os
import array
import random


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url


def dog(bot, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def cat(bot, update):
    a = ["cute", "small", "big", "ugly", "gray", "fluffy", "fat", "white", "square", "says/hello", "says/hi"]
    num = random.randint(0, 10)
    n = a[num]
    url = f"https://cataas.com/cat/{n}"
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def get_fact_txt(url):
    contents = requests.get(url).json()
    fact = contents['fact']
    return fact


def dogfact(bot, update):
    fact = get_fact_txt('https://some-random-api.ml/facts/dog')
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=fact)


def catfact(bot, update):
    fact = get_fact_txt('https://some-random-api.ml/facts/cat')
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=fact)


def start(bot, update):
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    bot.send_message(chat_id=chat_id, text=f"Hello {first_name} {last_name}, use /cat or /dog for random pics or find out more with /catfact or /dogfact")


def text(bot, update):
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name
    bot.send_message(chat_id=chat_id, text=f"Please {first_name}, type /start")


load_dotenv()
TOKEN = os.getenv('TOKEN')

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('dog',dog))
dp.add_handler(CommandHandler('cat',cat))
dp.add_handler(CommandHandler('dogfact', dogfact))
dp.add_handler(CommandHandler('catfact', catfact))
dp.add_handler(MessageHandler(Filters.text, text))

updater.start_polling()
updater.idle()