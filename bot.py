import random

import telebot
from telebot import types

import config

from bs4 import BeautifulSoup
import requests


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('stic/hi.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🎲 Кости')
    item2 = types.KeyboardButton('♊♌ Гороскоп')
    item3 = types.KeyboardButton('☺ Как дела?')

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n"
                                      "Я бот {1.first_name}.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def talk(message):
    if message.chat.type == 'private':
        if message.text == '☺ Как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton(text='Хорошо', callback_data='good')
            item2 = types.InlineKeyboardButton(text='Не очень', callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
        elif message.text == '🎲 Кости':
            dice = '⚀⚁⚂⚃⚄⚅'
            bot.send_message(message.chat.id, random.choice(dice))
            bot.send_message(message.chat.id, random.choice(dice))
        elif message.text == '♊♌ Гороскоп':
            url = 'https://ngs.ru/horoscope/daily/'
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "lxml")
            names = soup.find_all(class_="_4K6U+ _9dcVo")
            horoscopes = soup.find_all(class_="BDPZt KUbeq")
            horoscope_list = []
            name_list = []
            for name in names:
                name = name.text
                name_list.append(name)
            for horoscope in horoscopes:
                horoscope = horoscope.text
                horoscope_list.append(horoscope)
            horoscope_dict = dict(zip(name_list, horoscope_list))
            for key, value in horoscope_dict.items():
                bot.send_message(message.chat.id, f'{"{0} : {1}".format(key, value)}')
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить ☹')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и хорошо☺')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает☹')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='☺ Как дела?',
                                  reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
