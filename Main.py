# -*- coding: utf-8 -*-
import telebot
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from user import UserManager
from user import Sub
import os
import subprocess


#bot = telebot.TeleBot('1084630642:AAGFHSHxH9fLHaPhzqm6t-y-KYKEYfLe41U')




file_folder = "/home/mikhail_kozyrev_nn/bot/service/download/"
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
	reply_markup = buildEmptyStateMarkup()
	update.message.reply_text('Please fill in following form:', reply_markup=reply_markup)

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
	or_name = update.message.document.file_name
	file_name = downloadFile(update)
	if os.path.exists(file_name):
		userManager.setFirstDoc(str(update.message.from_user.id), file_name)
		userManager.setFirstDocName(str(update.message.from_user.id), or_name)
		update.message.reply_text('Got it, Base Doc: ' + or_name + '\n Upload netx file')
		userManager.setState(str(update.message.from_user.id), UserManager.STATE_FIRST_FILLED)
	else:
		update.message.reply_text('ERROR: cannot open file: ' + file_name)
	#userManager.setState(str(query.from_user.id), UserManager.STATE_FIRST_FILLED)
	userManager.setState(str(update.message.from_user.id), UserManager.STATE_FIRST_FILLED)

def handleSecondDoc(update):
	or_name = update.message.document.file_name
	file_name = downloadFile(update)
	if os.path.exists(file_name):
		userManager.setSecondDoc(str(update.message.from_user.id), file_name)
		userManager.setSecondDocName(str(update.message.from_user.id), or_name)
		update.message.reply_text('Got it, Merge Doc: ' + or_name + '\n Upload netx file')
		userManager.setState(str(update.message.from_user.id), UserManager.STATE_SECOND_FILLED)
		makeFinalMagick(update)
	else:
		update.message.reply_text('ERROR: cannot open file: ' + file_name)

def makeFinalMagick(update):
	s1 = decompileSubs(userManager.getFirstDoc(str(update.message.from_user.id)))
	s2 = decompileSubs(userManager.getSecondDoc(str(update.message.from_user.id)))
	res = None
	if userManager.getState(update.message.from_user.id) == userManager.MOD_MERGE:
		res = mergeSubs(s1, s2)
	elif userManager.getState(update.message.from_user.id) == userManager.MOD_ALIGNE:
		res = aligneSubs(s1, s2)
	else:
		update.message.reply_text('ERR: Incorrect mod')
		return
	sendFile(update, res)

def downloadFile(update):
	file = updater.bot.get_file(update.message.document.file_id)
	file_path = "/home/mikhail_kozyrev_nn/bot/service/download/" + update.message.document.file_id
	#downloaded_file = updater.bot.download_file(file_path)
	file.download(file_path)
	return file_path


#	if message.document.mime_type != 'text/plain':
#		bot.send_message(message.chat.id, message.document.file_name + " is not a text/plain file, please choose another one")
#	if re.search('.srt$', message.document.file_name) == None:
#		bot.send_message(message.chat.id,"WARN: .srt is usual extension for subtitels, something can goes wrong")

#	file = bot.get_file(message.document.file_id)

#	bot.send_message(message.chat.id, 'Debug: ' + message.document.file_name + " " + str(message.document.file_size))

#bot.polling()

def decompileSubs(file_name):
	f = open(file_name, "r", encoding=getCharset(file_name))
	textArr = f.readlines()
	subsArr = []
	tmpSub = None
	for i,line in enumerate(textArr):
		if re.match("\d+$", line) != None:
			tmpSub = Sub(line.rstrip('\n'), "?????", "")

			if re.match("\d{2}:\d{2}:\d{2}.* --> \d{2}:\d{2}:\d{2}.*", textArr[i+1]) != None:
				tmpSub.time =  textArr[i+1].rstrip('\n')
#				print("line: " + str(i) + " - " +  textArr[i+1])
				for nLine in textArr[i+2:]:
#					if re.match("\w+ && !(\d+$) && !(\d{2}:\d{2}:\d{2}.* --> \d{2}:\d{2}:\d{2}.*)", nLine) != None:
					if nLine != "\n":
						tmpSub.text += nLine
#						print("line: " + str(i) + " - " + nLine)
					else:
#						print("=================================================")
						break
			subsArr.append(tmpSub)

	#print(textArr)
	f.close()
	return subsArr

def mergeSubs(s1, s2):
	sFinal = []
	for i,s in enumerate(s2):
		s1[i].text += s.text 
	return s1

def aligneSubs(s1, s2):
	sFinal = []
	for i,s in enumerate(s1):
		s2[i].time = s.time
	return s2

def sendFile(update, s):
	id = str(update.message.from_user.id) 
	f = open(file_folder + id, "w", encoding="UTF8")
	for sub in s:
		f.write(sub.number + "\n")
		f.write(sub.time + "\n")
		f.write(sub.text + "\n")
	f.close()
	f = open(file_folder + str(update.message.from_user.id), "rb")
	updater.bot.send_document(update.message.chat.id, f, userManager.getFirstDocName(id).split(".")[0] + userManager.getSecondDocName(id).split(".")[0] + ".srt");
	f.close()
	clean(update)

def buildEmptyStateMarkup():
	keyboard = [[InlineKeyboardButton("Merge mode", callback_data='0'), InlineKeyboardButton("Aligne mode", callback_data='1')]]

	return InlineKeyboardMarkup(keyboard)

def clean(update):
	os.remove(file_folder + str(update.message.from_user.id))
	userManager.clean(str(update.message.from_user.id))

def getCharset(file_name):
	cs = subprocess.check_output('/usr/bin/file -i ' + file_name + '| awk \'{print $3}\' | sed "s|charset=||g"', shell=True).decode("utf-8")
	if re.match("iso-8859.*", cs) != None:
		return "Windows-1251"
	else:
		return cs

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