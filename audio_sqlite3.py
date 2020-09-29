import sqlite3
from sqlite3 import Error
from random import choice

temp_list = []
temp_list2 = []
temp = ''

class Database():
	"""connect to our database(create an empty database)"""
	def sql_connection(self):
		try:
			con = sqlite3.connect('music_database.db')
			return con

		except Error:
			print(Error)

	"""create database"""
	def sql_table(self):
		con = Database().sql_connection()
		cursorObj = con.cursor()
		"""'already' - for our func 'if_already_exists' in audio_bot
		(1 - created; 0 - already exists)"""
		global already

		try:
			cursorObj.execute("CREATE TABLE music_records(id int, right_answer text, wrong_answers text)")
			con.commit()
			already = 1

		except:
			already = 0
	
	"""add track"""
	def sql_insert(self, right_answer, wrong_answer1, wrong_answer2, wrong_answer3):
		con = Database().sql_connection()
		cursorObj = con.cursor()

		whole_wrong_answer = wrong_answer1 + ', ' + wrong_answer2 + ', ' + wrong_answer3

		"""select id"""
		try: # IDs for our tracks are selected consistant(temp - ID)
			cursorObj.execute("SELECT * FROM music_records")
			rows = cursorObj.fetchall()
			for i in range(1, 100):
				if i not in rows[-1]:
					if i > rows[-1][0]:
						temp = i
						break

		except: # if our database is empty
			temp = 1

		cursorObj.execute("INSERT INTO music_records VALUES(?, ?, ?)", (temp, right_answer, whole_wrong_answer))
		con.commit()

	"""remove track"""
	def sql_remove(self, id_num):
		global already2, track_name
		con = Database().sql_connection()
		cursorObj = con.cursor()
		id_num = int(id_num) # now our entered track`s ID is INT
		cursorObj.execute("SELECT id FROM music_records WHERE id = " + str(id_num))
		"""if such an ID does not exist"""
		if cursorObj.fetchone() is None:
			already2 = 0

		else: # if exists
			cursorObj.execute("SELECT * FROM music_records WHERE id = " + str(id_num))
			rows = cursorObj.fetchall() # here we get a list with a tuple

			for row in rows: # 'row' - element in a tuple
				track_name = row[1]

			cursorObj.execute("DELETE FROM music_records WHERE id == " + str(id_num)).rowcount
			con.commit()
			already2 = 1

	"""select a random track from the database"""
	def sql_select_track(self):
		con = Database().sql_connection()
		global temp, temp_list, temp3, temp_list2
		cursorObj = con.cursor()

		cursorObj.execute("SELECT * FROM music_records").rowcount
		rows = cursorObj.fetchall()

		"""temp_list2 - number of rows in the database"""
		for el in range(1, len(rows) + 1):
			if el in temp_list2:
				break
			else:
				temp_list2.append(el)

		"""if we`re out of tracks, send to user the lower message(temp3)"""
		if len(temp_list) > len(rows):	
			temp3 = 'Sorry, There are no more tracks'

			"""reset these variables"""
			temp_list = []
			temp_list2 = []
			temp = ''

		else:
			while True:
				"""select random number(row) from our list"""
				el = choice(temp_list2)

				"""temp - this random row from database"""
				cursorObj.execute("SELECT * FROM music_records WHERE id == " + str(el))
				temp = cursorObj.fetchone()

				"""if selected ID had alredy been chosen, we pass it and select another
				with the help of 'while True'"""
				if temp[0] in temp_list:
					pass

				else:
					"""temp_list - list of IDs that have been selected to send them to the 
					user(so that the bot does not send them again)"""
					temp_list.append(temp[0])
					"""if we`re out of tracks, we add one more element to our list
					'temp_list' to make len(temp_list) > len(rows)"""
					if len(temp_list) == len(temp_list2):
						temp_list.append('one more')

					break

	def random_phrases(self):
		"""to diversify our bot`s messages"""
		global r_phrase, w_phrase
		right_phrases = ['That`s right! Let`s move on🤩', 'Keep it up!', 'Wow, you heard this song😲', 'That is the right answer🥳', 'Don`t stop, you`re all class!', 'Yeah, keep going🤙']
		wrong_phrases = ['Almost, the right answer is: ', 'Noo, it`s: ', 'You got something wrong😕, the answer is: ', 'Don`t want to upset you😔, but it`s: ', 'Not entirely true, it`s: ']
		r_phrase = choice(right_phrases)
		w_phrase = choice(wrong_phrases)

	def sql_select_ALL(self):
		con = Database().sql_connection()
		cursorObj = con.cursor()
		global full_message 

		cursorObj.execute("SELECT * FROM music_records")
		rows = cursorObj.fetchall()
		full_message = str(rows[0][0]) + '.Right answer: ' + rows[0][1] + '\nWrong answers: ' + rows[0][2] + '\n\n' + str(rows[1][0]) + '.Right answer: ' + rows[1][1] + '\nWrong answers: ' + rows[1][2] + '\n\n' + str(rows[2][0]) + '.Right answer: ' + rows[2][1] + '\nWrong answers: ' + rows[2][2] + '\n\n' + str(rows[3][0]) + '.Right answer: ' + rows[3][1] + '\nWrong answers: ' + rows[3][2] + '\n\n' + str(rows[4][0]) + '.Right answer: ' + rows[4][1] + '\nWrong answers: ' + rows[4][2] + '\n\n' + str(rows[5][0]) + '.Right answer: ' + rows[5][1] + '\nWrong answers: ' + rows[5][2] + '\n\n' + str(rows[6][0]) + '.Right answer: ' + rows[6][1] + '\nWrong answers: ' + rows[6][2] 