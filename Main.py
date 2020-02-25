# -*- coding: utf-8 -*-
import telebot

bot = telebot.TeleBot('1084630642:AAGFHSHxH9fLHaPhzqm6t-y-KYKEYfLe41U')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello, don\'t waste my time')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'hi':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'by':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    else:
        bot.send_message(message.chat.id, 'Repeater: ' + message.text)

bot.polling()