import telebot
import requests
import json
from telebot import types

bot = telebot.TeleBot("5995826586:AAHtcGH6qoToJDN29SnMjwBYgpLjoiviON0")
API = "e18fd8f4421d1c1a6638179d7b897f81"


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
        #картиночки

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
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALdKWTqlud3Py_lddg1SSEVPf0_Z-3OAAJWDQACZbCZSlC-DztRCvnTMAQ')



bot.infinity_polling()
# bot.polling(none_stop=True)
