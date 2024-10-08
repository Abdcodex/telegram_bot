import os
import telebot
import requests
import logging
BOT_TOKEN = '7619974501:AAGo9dzaWyLtKdODU84GZgTPup0KhPkI780'
bot = telebot.TeleBot(BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    logging.info('hello')
    bot.reply_to(message, "Howdy, how are you doing ?")

def get_daily_horoscope(sign: str, day: str):
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)

    return response.json()

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    logging.info('horoscope')   
    text = "What's your zodiac sign?\n Choose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode ="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    sign = message.text
    text = "What day do want to know/ \n Choose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope, sign.capitalize()
    )

def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()


