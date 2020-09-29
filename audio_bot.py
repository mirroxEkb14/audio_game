import telebot
from telebot import types
import config
import os
import audio_sqlite3
from random import shuffle
import requests
import time

try:
	bot = telebot.TeleBot(config.token)

	user_answers = []
	zero_num = None
	one_num = None

	right_answer = None
	wrong_answer1 = None
	wrong_answer2 = None
	wrong_answer3 = None

	@bot.message_handler(commands = ['start'])
	def greet_func(message):
		bot.send_message(message.chat.id, 'Howdy {0.first_name}!\n You want to play with me? Then enter \'/game\' to start the game'.format(message.from_user))

	@bot.message_handler(commands = ['admin_mode'])
	def hello_admin(message):
		if message.text == '/admin_mode': # ask the user for a password
			bot.send_message(message.chat.id, 'Enter password')
			bot.register_next_step_handler(message, hello_admin)

		elif message.text == 'Q' or message.text == 'q': # quit admin mode
			bot.send_message(message.chat.id, 'Admin mode was cancelled')

		elif message.text == '13673180820': # if the password is correct, get to 'admin_console'
			bot.send_message(message.chat.id, 'Howdy {0.first_name}! Glad to see you, what can I do?\n(enter \'Q\' to exit)\n1.Create database\n2.Add track\n3.Remove track\n4.View all the available tracks'.format(message.from_user))

			bot.register_next_step_handler(message, admin_console)

		else: # if the password is incorrect, we quit admin mode
			bot.send_message(message.chat.id, 'You`re not an admin😠')

	"""after the user enters '/game', we start declare our main game func"""
	@bot.message_handler(commands = ['game'])
	def to_send_track(message):
		send_track(message)

	"""our main game func"""
	@bot.message_handler(content_types = ['text'])
	def send_track(message):
		"""for the first time triggers the condition '/game', """
		if message.text == '/game' or message.text == 'Next guess':

			"""triggers the method 'select_track'"""
			audio_sqlite3.Database().sql_select_track()

			"""create a keyboard so the user can select the answers"""
			markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

			try:
				"""all_answer - the right answer and the wrong answers"""
				all_answer = audio_sqlite3.temp[1] + ', ' + audio_sqlite3.temp[2]
				"""list_items - the list of the right answer and the wrong answers"""
				list_items = []
				for item in all_answer.split(','):
					list_items.append(item)

				"""mix everything up in 'list_items'"""
				shuffle(list_items)

				"""add all the answers from our mixed list to the keyboard"""
				for item in list_items:
					markup.add(item)

				"""temp2 - path to our selected track"""
				for el in os.listdir('C:/Den4ik/music_tgbot/new folder(shorted)/'):
					if audio_sqlite3.temp[1] in el:
						temp2 = el

				"""send selected track to user and get to func 'is_answer'"""
				f = open('C:/Den4ik/music_tgbot/new folder(shorted)/' + temp2, 'rb')
				msg = bot.send_voice(message.chat.id, f, reply_markup = markup)
				bot.register_next_step_handler(message, is_answer)

			except:
				global user_answers, zero_num, one_num
				zero_num = user_answers.count(0) # number of wrong answers
				one_num = user_answers.count(1) # number of right answers

				if one_num >= 6:
					markup = types.ReplyKeyboardRemove()
					bot.send_message(message.chat.id, audio_sqlite3.temp3 + '\n\nCorrect answers - ' + str(one_num) + '\nWrong answers - ' + str(zero_num), reply_markup = markup)
					bot.send_message(message.chat.id, 'I`m impressed, you`re really good at music👏')

				elif one_num >= 4 < 6:
					markup = types.ReplyKeyboardRemove()
					bot.send_message(message.chat.id, audio_sqlite3.temp3 + '\n\nCorrect answers - ' + str(one_num) + '\nWrong answers - ' + str(zero_num), reply_markup = markup)
					bot.send_message(message.chat.id, 'Congratulations, you did really well👏')
				
				elif one_num < 4:
					markup = types.ReplyKeyboardRemove()
					bot.send_message(message.chat.id, audio_sqlite3.temp3 + '\n\nCorrect answers - ' + str(one_num) + '\nWrong answers - ' + str(zero_num), reply_markup = markup)
					bot.send_message(message.chat.id, 'Not bad, you know things✊')

				"""reset the variables"""
				user_answers = []
				zero_num = None
				one_num = None

		elif message.text == 'Next guess' or message.text == 'Quit':
			"""after we get to 'is_answer', user has to select 'Next guess' or 'Quit',
			in any case we get to 'FOR_is_answer' where this answer will be processed"""
			FOR_is_answer(message)

		else:
			bot.send_message(message.chat.id, message.text + '😜')

	def is_answer(message):
		"""create this variable to remember how many right and wrong answers the user gave"""
		global user_answers

		"""after the user selects an answer we add the keyboard"""
		markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
		item1 = types.KeyboardButton('Next guess')
		item2 = types.KeyboardButton('Quit')
		markup.add(item1, item2)

		audio_sqlite3.Database().random_phrases()

		if message.text == audio_sqlite3.temp[1]:
			"""if user answers rightly, we append '1' to the list 'user_answers'"""
			user_answers.append(1)

			"""if the user guessed the right answer, we send random message from 
			'right_phrases' list and get to 'FOR_is_answer'"""
			bot.send_message(message.chat.id, audio_sqlite3.r_phrase, reply_markup = markup)
			bot.register_next_step_handler(message, FOR_is_answer)

		else:
			"""if user answers wrongly, we append '1' to the list 'user_answers'"""
			user_answers.append(0)

			"""if the user guessed the wrong answer, we send random message from 
			'wrong_phrases' list and get to 'FOR_is_answer'"""
			bot.send_message(message.chat.id, audio_sqlite3.w_phrase + audio_sqlite3.temp[1], reply_markup = markup)
			bot.register_next_step_handler(message, FOR_is_answer)


	def FOR_is_answer(message):
		if message.text == 'Next guess':
			"""send the next track"""
			send_track(message)

		elif message.text == 'Quit':
			"""remove the keyboard and send a message"""
			markup = types.ReplyKeyboardRemove()
			bot.send_message(message.chat.id, 'Hope that was funny for you😸', reply_markup = markup)

			"""reset these variables"""
			audio_sqlite3.temp_list = []
			audio_sqlite3.temp_list2 = []
			audio_sqlite3.temp = ''

		else:
			bot.send_message(message.chat.id, 'Sorry, didn`t catch you')


	def admin_console(message):
		if message.text == '1.' or message.text == '1' or message.text == 'Create database' or message.text == 'create database':
			audio_sqlite3.Database().sql_table()

			"""to check whether the database already exists or not"""
			def if_already_exists(message):
				if audio_sqlite3.already == 1:
					bot.send_message(message.chat.id, 'Created')

				else:
					bot.send_message(message.chat.id, 'Already exists')

			if_already_exists(message)

		elif message.text == '2.' or message.text == '2' or message.text == 'Add track' or message.text == 'add track':

			"""to check whether the database exists or not"""
			def if_exists(message):
				"""if exists"""
				if os.path.exists('C:/Users/Daniyar/Desktop/python_scrips/sublime_text python/music_database.db'):
					"""user enters the right answer, get to 'right_answer_func'"""
					bot.send_message(message.chat.id, 'Enter the right answer')
					bot.register_next_step_handler(message, right_answer_func)

				else:
					bot.send_message(message.chat.id, 'The database doesn`t exist')

			def right_answer_func(message):
				global right_answer
				right_answer = message.text

				ifq_or_ifint(message)

			def wrong_answer_func1(message):
				global wrong_answer1
				wrong_answer1 = message.text

				ifq_or_ifint(message)

			def wrong_answer_func2(message):
				global wrong_answer2
				wrong_answer2 = message.text

				ifq_or_ifint(message)

			def wrong_answer_func3(message):
				global wrong_answer3
				wrong_answer3 = message.text

				ifq_or_ifint(message)

			"""our main check function"""
			def ifq_or_ifint(message):
				global right_answer, wrong_answer1, wrong_answer2, wrong_answer3

				if message.text == 'Q' or message.text == 'q':
					bot.send_message(message.chat.id, 'Admin mode was cancelled')

				else:
					"""verification(we need STR, not INT)(maybe a bit difficult but it works)"""
					try:
						if right_answer and wrong_answer1 == None and wrong_answer2 == None and wrong_answer3 == None:
							int(right_answer)

						elif wrong_answer1 and wrong_answer2 == None and wrong_answer3 == None:
							int(wrong_answer1)

						elif wrong_answer2 and wrong_answer3 == None:
							int(wrong_answer2)

						elif wrong_answer3:
							int(wrong_answer3)

						bot.send_message(message.chat.id, 'Admin mode was cancelled\nNote: only letters')

						right_answer = None
						wrong_answer1 = None
						wrong_answer2 = None
						wrong_answer3 = None

					except:
						if wrong_answer1 == None:
							bot.send_message(message.chat.id, 'Wrong answer #1')
							bot.register_next_step_handler(message, wrong_answer_func1)

						elif wrong_answer2 == None:
							bot.send_message(message.chat.id, 'Wrong answer #2')
							bot.register_next_step_handler(message, wrong_answer_func2)

						elif wrong_answer3 == None:
							bot.send_message(message.chat.id, 'Wrong answer #3')
							bot.register_next_step_handler(message, wrong_answer_func3)

						else:
							audio_sqlite3.Database().sql_insert(right_answer, wrong_answer1, wrong_answer2, wrong_answer3)
							bot.send_message(message.chat.id, 'The track has been added to database')

							right_answer = None
							wrong_answer1 = None
							wrong_answer2 = None
							wrong_answer3 = None

			if_exists(message)

		elif message.text == '3.' or message.text == '3' or message.text == 'Remove track' or message.text == 'remove track':

			"""to check whether the database exists or not"""
			def if_exists(message):
				"""if exists"""
				if os.path.exists('C:/Users/Daniyar/Desktop/python_scrips/sublime_text python/music_database.db'):
					"""ask track`s ID and get to 'delete_func'"""
					bot.send_message(message.chat.id, 'Enter track`s ID')
					bot.register_next_step_handler(message, delete_func)

				else:
					bot.send_message(message.chat.id, 'The database doesn`t exist')

			def delete_func(message):
				global id_num
				id_num = message.text

				"""verification(we need numbers, not letters)"""
				try:
					int(id_num)
					audio_sqlite3.Database().sql_remove(id_num)
					right_or_wrong(message)

				except:
					bot.send_message(message.chat.id, 'Admin mode was cancelled\nNote: only numbers')

			def right_or_wrong(message):
				if audio_sqlite3.already2 == 1: # if the track exists
					bot.send_message(message.chat.id, 'The track ' + '\'' + audio_sqlite3.track_name + '\'' + ' has been deleted')

				else: # if not
					bot.send_message(message.chat.id, 'Such an ID doesn`t exist')

			if_exists(message)

		elif message.text == '4.' or message.text == '4' or message.text == 'View all the available tracks' or message.text == 'view all the available tracks':
			audio_sqlite3.Database().sql_select_ALL()
			bot.send_message(message.chat.id, audio_sqlite3.full_message)

		elif message.text == 'Q' or message.text == 'q':
			bot.send_message(message.chat.id, 'Admin mode was cancelled')

		else:
			bot.send_message(message.chat.id, 'Admin mode was cancelled\nNote: I didn`t suggest ' + '\'' + message.text + '\'')


	bot.polling(none_stop = True)

except requests.exceptions.Timeout:
	time.sleep(3)