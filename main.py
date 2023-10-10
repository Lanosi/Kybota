import telebot
import requests
import json
from telebot import types
import random

bot = telebot.TeleBot("5995826586:AAHtcGH6qoToJDN29SnMjwBYgpLjoiviON0")

API = "e18fd8f4421d1c1a6638179d7b897f81"

A_picture = "https://api.waifu.pics/sfw/waifu"

sticker_ids = ["CAACAgIAAxkBAALdKWTqlud3Py_lddg1SSEVPf0_Z-3OAAJWDQACZbCZSlC-DztRCvnTMAQ",
               "CAACAgIAAxkBAAEBFONlBZkyVNhVLIluElrFHFXcEQw2zwACCBQAAoUTAUviN_lSxPexIjAE",
               "CAACAgIAAxkBAAEBFOVlBZk2_J4I6-ARqhsBE_tb_CNO6wACBhUAAqMfAAFL-hxiQICXrqQwBA",
               "CAACAgIAAxkBAAEBFOdlBZk9EMB61fOUXPBLw74EXXfUDgACDx8AAjEweUvqf9cIWm40rzAE",
               "CAACAgIAAxkBAAEBFOxlBZoYrlYuiFIaVuvjBVUPz5HeqgACwhcAAn35CEpLOXYqcHQJBTAE",
               "CAACAgIAAxkBAAEBFPFlBZqEPyOiahPUPp0TDKEQkcVfxAACZB0AAk6DMUuCuSVVotHEiDAE",
               "CAACAgIAAxkBAAEBFPNlBZqQRB5_URzdendPpsY1F75eLwACKAsAAmabiEupRrF6X15LxjAE",
               "CAACAgIAAxkBAAEBFPVlBZqbgBOY2RT6GqLLtR-BXkdFmAACwg8AAg7WWUqbH6WpjCEvIzAE",
               "CAACAgIAAxkBAAEBFPdlBZqdJeRcB3Gc0cZbUVAhdt9R2AACZwsAAhOBYUpl8WbUGoiU8zAE",
               "CAACAgIAAxkBAAEBFPllBZql2-Sx3qaYGkyXrfxIbO52EwACYgwAAnm2qEo888p9JLFmpjAE",
               "CAACAgIAAxkBAAEBFP1lBZu1HCSgLIiyurtSDW9TpLnt2wAC0BcAAvBJ8EpoI6YLGmfpFTAE",
               "CAACAgIAAxkBAAEBK7JlD0tDalNEyDcWbYBUzbg4mtZKLwACIg0AAqK7iUvYql3GoNextzAE",
               "CAACAgIAAxkBAAEBK7RlD0tRGPxI-24x0gABOss-swWVrb4AAmoVAAK5UUhJQGDOnEsJsxowBA",
               "CAACAgIAAxkBAAEBK7ZlD0tXhirU4WK0T44fwLraIsFVXgACthsAApY7uhcuwCtsy6gmhDAE",
               "CAACAgIAAxkBAAEBK7ZlD0tXhirU4WK0T44fwLraIsFVXgACthsAApY7uhcuwCtsy6gmhDAE",
               "CAACAgIAAxkBAAEBK7plD0trkfm9_cfuAdQWjBqbFfnKLgAC_RUAAmKSWEi-UCy6ZfFEATAE",
               "CAACAgIAAxkBAAEBK75lD0t_ZZMEikwbJ7rbZPN_1R3IhAACWxcAAui0WEgbajEfTFsf2DAE",
               "CAACAgIAAxkBAAEBK8BlD0uGjw2HlcfNbPaDWVBxCPKagQAC_hMAAnKSaUjoc4OjLxpKKDAE",
               "CAACAgIAAxkBAAEBK8JlD0uO76B9K3-F-n5r6E8Cb3LNeQACZRYAAoaISEisVJ66ehkpWDAE"]

user_sity = {}


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Ку, напиши город от куда ты хочешь получать погоду")
    bot.register_next_step_handler(message, define_city)


def define_city(message):
    try:
        city = message.text.strip().lower()
        res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
        if res.status_code == 200:
            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton("Изменить город")
            btn2 = types.KeyboardButton("Погода")
            markup.add(btn1)
            markup.add(btn2)

            data = json.loads(res.text)
            temp = data['main']['temp']
            bot.send_message(message.chat.id, f"Город выбран, температура в нём: {temp}", reply_markup=markup)

            user_sity[message.from_user.id] = city
        else:
            bot.reply_to(message, "Данных от туда нет...")

            bot.register_next_step_handler(message, define_city)
    except AttributeError:
        bot.reply_to(message, "Сука название города отправь, а не эту хуйню")
        bot.register_next_step_handler(message, define_city)



@bot.message_handler(content_types=["text"])
def receiving_text_user(message):
    if message.text == "Погода":
        sending_weather(message)
        #добавить проверку на наличие города в id

    elif message.text == "Изменить город":
        bot.reply_to(message, "изменение в словарь по id")

    else:
        user_t(message)



def sending_weather(message):
    city = user_sity[message.from_user.id]
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    data = json.loads(res.text)
    temp = data['main']['temp']
    bot.send_message(message.chat.id, f"{city} - {temp}")

    res = requests.get(A_picture)
    link_image = json.loads(res.text)
    image = link_image["url"]

    bot.send_photo(message.chat.id, image)

def user_t(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        bot.send_message(message.chat.id, f"Температура: {temp}")
    else:
        bot.send_message(message.chat.id, "Не понял")

@bot.message_handler(content_types=["sticker"])
def reaction_on_sticker(message):
    bot.send_sticker(message.chat.id, random.choice(sticker_ids))


# bot.infinity_polling()
bot.polling(none_stop=True)
