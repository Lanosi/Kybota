import telebot
import requests
import json
from telebot import types
import random

bot = telebot.TeleBot("")
API = ""
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
               "CAACAgIAAxkBAAEBFP1lBZu1HCSgLIiyurtSDW9TpLnt2wAC0BcAAvBJ8EpoI6YLGmfpFTAE"]


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
            #bot.send_message(message.chat.id, "Кнопки добавлены", reply_markup=markup)

            data = json.loads(res.text)
            temp = data['main']['temp']
            bot.send_message(message.chat.id, f"Город выбран, температура в нём: {temp}",reply_markup=markup)
        else:
            bot.reply_to(message, "Данных от туда нет...")

            bot.register_next_step_handler(message, define_city)
    except AttributeError:
        bot.reply_to(message, "Сука название города отправь, а не эту хуйню")
        bot.register_next_step_handler(message, define_city)



@bot.message_handler(content_types=["text"])
def choose_city(message):
    if message.text == "Изменить город":
        # тут скорее всего запись города в бд какую-нибудь
        bot.reply_to(message, "Город выбран")
    elif message.text == "Погода":
        bot.reply_to(message, "Ну типа отправяется погода твоего города")
        res = requests.get(A_picture)
        link_image = json.loads(res.text)
        image = link_image["url"]

        bot.send_photo(message.chat.id, image)
        #картиночки
    elif message.text == "Тест":
        res = requests.get(A_picture)
        link_image = json.loads(res.text)
        image = link_image["url"]

        bot.send_photo(message.chat.id,image)

        bot.reply_to(message, "Ура аниме пикча")

    else:
        user_t(message)

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





bot.infinity_polling()
# bot.polling(none_stop=True)
