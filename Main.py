# -*- coding: utf-8 -*-
import telebot
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from user import UserManager
import os


#bot = telebot.TeleBot('1084630642:AAGFHSHxH9fLHaPhzqm6t-y-KYKEYfLe41U')




userManager = UserManager()
updater = Updater("1084630642:AAGFHSHxH9fLHaPhzqm6t-y-KYKEYfLe41U", use_context=True)

def button(update, context):
    query = update.callback_query

    query.answer()
    userManager.setMode(str(query.from_user.id), query.data)
    query.edit_message_text(text="Selected option: {}".format(query.data + "; user: " + str(query.from_user.id)))
    query.edit_message_text(text="You are - {}. Please upload first file".format(userManager.dumpUser(str(query.from_user.id))))




#@bot.message_handler(commands=['start'])
def start_message(update, context):
    update.message.reply_text('Hello, don\'t waste my time')
    update.message.reply_text("You are " + userManager.dumpUser(str(update.message.from_user.id)))
    reply_markup = buildEmptyStateMarkup()
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

#@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'hi':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'by':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    else:
        bot.send_message(message.chat.id, 'Repeater: ' + message.text)

#@bot.message_handler(content_types=['document'])
def handle_text_doc(update, context):

    tmpState = userManager.getState(str(update.message.from_user.id))
    if userManager.getState(str(update.message.from_user.id)) == userManager.STATE_EMPTY:
        handleFirstDoc(update)
    elif userManager.getState(str(update.message.from_user.id)) == userManager.STATE_FIRST_FILLED:
        handleSecondDoc(update)

def handleFirstDoc(update):
    file_name = downloadFile(update)
    if os.path.exists(file_name):
        userManager.setFirstDoc(update.message.from_user.id, file_name)
        update.message.reply_text('Got it:\n FirstDoc: ' + file_name + '\n Upload netx file')
        userManager.setState(str(update.message.from_user.id), UserManager.STATE_FIRST_FILLED)
    else:
        update.message.reply_text('ERROR: cannot open file: ' + file_name)
    #userManager.setState(str(query.from_user.id), UserManager.STATE_FIRST_FILLED)
    userManager.setState(str(update.message.from_user.id), UserManager.STATE_FIRST_FILLED)

def handleSecondDoc(update):
    file_name = downloadFile(update)
    if os.path.exists(file_name):
        userManager.setSecondDoc(update.message.from_user.id, file_name)
        update.message.reply_text('Got it:\n SecondDoc: ' + file_name)
        userManager.setState(str(update.message.from_user.id), UserManager.STATE_FIRST_FILLED)
        makeFinalMgick(update)
    else:
        update.message.reply_text('ERROR: cannot open file: ' + file_name)

def makeFinalMgick(update):
    if userManager.getState(update.message.from_user.id) == userManager.MOD_MERGE:
        #f1 = open(userManager.getFirstDoc(update.message.from_user.id), "r")
        decompileSubs(update.message.from_user.id)
    elif userManager.getState(update.message.from_user.id) == userManager.MOD_ALIGNE:
        pass
    else:
        update.message.reply_text('ERR: Incorrect mod')

def downloadFile(update):
    file = updater.bot.get_file(update.message.document.file_id)
    file_path = "/home/mikhail_kozyrev_nn/bot/service/download/" + update.message.document.file_id
    #downloaded_file = updater.bot.download_file(file_path)
    file.download(file_path)
    return file_path


#    if message.document.mime_type != 'text/plain':
#        bot.send_message(message.chat.id, message.document.file_name + " is not a text/plain file, please choose another one")
#    if re.search('.srt$', message.document.file_name) == None:
#        bot.send_message(message.chat.id,"WARN: .srt is usual extension for subtitels, something can goes wrong")

#    file = bot.get_file(message.document.file_id)
    
#    bot.send_message(message.chat.id, 'Debug: ' + message.document.file_name + " " + str(message.document.file_size))

#bot.polling()

def decompileSubs(id):
	f = open(userManager.getFirstDoc(id), "r")
	textArr = f.readlines()
	subsArr = []
	for i, line in textArr:
		print("line: " + i + " - " + line)
	f.close()

def buildEmptyStateMarkup():
    keyboard = [[InlineKeyboardButton("Merge subtitelse to one file", callback_data='0')],
                [InlineKeyboardButton("Aligne subtitelse", callback_data='1')]]
    return InlineKeyboardMarkup(keyboard)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary


    updater.dispatcher.add_handler(CommandHandler('start', start_message))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, handle_text_doc))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()