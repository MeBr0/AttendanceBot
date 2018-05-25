from constants import TOKEN, START, STUDENT, TEACHER, NO_FAMILY, NO_SLEEP, NO_OTHER, NO_HEALTH, NO_ANSWER, YES, STARTATT, STOPATT, RESULT, ORIGIN
from messages import GREETINGS, ID, SHARE, START_ATT, STOP_ATT, ID_ENTER, _NO_FAMILY, _NO_SLEEP, _NO_OTHER, _NO_HEALTH, _NO_ANSWER, _YES
from tinydb import TinyDB, Query
from telebot import types

import telebot
import json

bot = telebot.TeleBot(TOKEN)

listt = TinyDB('listt.json')
names = TinyDB('names.json')
att = TinyDB('att.json')

# markup for standart keyboard =================================================================

markup = types.ReplyKeyboardMarkup(row_width = 2)
item1 = types.KeyboardButton(STUDENT)
item2 = types.KeyboardButton(TEACHER)
markup.row(item1, item2)

# markup for teacher`s keyboard =================================================================

markupT = types.ReplyKeyboardMarkup(row_width = 3)
item1 = types.KeyboardButton(STARTATT)
item2 = types.KeyboardButton(STOPATT)
item3 = types.KeyboardButton(RESULT)
item4 = types.KeyboardButton(ORIGIN)
markupT.row(item1, item2, item3)
markupT.row(item4)

# markup for student`s keyboard =================================================================

markupS = types.ReplyKeyboardMarkup(row_width = 2)
item1 = types.KeyboardButton(YES)
item2 = types.KeyboardButton(NO_SLEEP)
item3 = types.KeyboardButton(NO_HEALTH)
item4 = types.KeyboardButton(NO_FAMILY)
item5 = types.KeyboardButton(NO_OTHER)
item6 = types.KeyboardButton(ORIGIN)
markupS.row(item1)
markupS.row(item2, item3)
markupS.row(item4, item5)
markupS.row(item6)

# start =================================================================

@bot.message_handler(commands = ['start'])
def welcome(message):
	bot.send_message(message.chat.id, GREETINGS, reply_markup=markup)
	names.insert({"name": message.from_user.first_name + " " + message.from_user.last_name, "id": str(message.chat.id)})

@bot.message_handler(regexp = 'Origin')
def origin(message):
	bot.send_message(message.chat.id, GREETINGS, reply_markup=markup)

# teacher =================================================================

@bot.message_handler(regexp = TEACHER)
def teacher(message):

	if len(listt.search(Query().id == str(message.chat.id))) == 0:
		listt.insert({"id": str(message.chat.id), 'ls': [], 'status': 'false'})

	bot.send_message(message.chat.id, ID + str(message.chat.id) + SHARE, reply_markup = markupT)

@bot.message_handler(regexp = STARTATT)
def start_att(message):
	with open('att.json', 'w') as f:
		f.truncate()

	att.insert({"id": str(message.chat.id), YES:[], NO_SLEEP: [], NO_HEALTH: [], NO_FAMILY: [], NO_OTHER: [], NO_ANSWER: []})


	a = listt.search(Query().id == str(message.chat.id))
	if len(a) == 0:
		return

	for i in a[0]['ls']:
		bot.send_message(i, START_ATT, reply_markup = markupS)

	listt.update({'status': 'true'}, Query().id == str(message.chat.id))

	bot.send_message(message.chat.id, 'Attendance began', reply_markup = markupT)


@bot.message_handler(regexp = STOPATT)
def stop_att(message):
	a = []
	b = []

	if len(listt.search(Query().id == str(message.chat.id))) != 0 and  len(att.search(Query().id == str(message.chat.id))) != 0:
		a = listt.search(Query().id == str(message.chat.id))[0]
		b = att.search(Query().id == str(message.chat.id))[0]
		listt.update({'status': 'false'}, Query().id == str(message.chat.id))

		for i in a['ls']:
			bot.send_message(i, STOP_ATT)



	else: return

	for i in a['ls']:
		if (i not in b[YES]) and (i not in b[NO_SLEEP]) and (i not in b[NO_HEALTH]) and (i not in b[NO_FAMILY]) and (i not in b[NO_OTHER]):
			b[NO_ANSWER].append(i)

			c = b[NO_ANSWER]

			att.update({NO_ANSWER: c}, Query().id == str(message.chat.id))

	bot.send_message(message.chat.id, 'Attendance ended', reply_markup = markupT)



@bot.message_handler(regexp = RESULT)
def result(message):
	res = ''
	a = []
	if len(att.search(Query().id == str(message.chat.id))) != 0:
		a = att.search(Query().id == str(message.chat.id))[0]

	else: return

	if len(a[YES]) != 0:
		res = write(res, YES, a)
	if len(a[NO_SLEEP]) != 0:
		res = write(res, NO_SLEEP, a)
	if len(a[NO_HEALTH]) != 0:
		res = write(res, NO_HEALTH, a)
	if len(a[NO_FAMILY]) != 0:
		res = write(res, NO_FAMILY, a)
	if len(a[NO_OTHER]) != 0:
		res = write(res, NO_OTHER, a)
	if len(a[NO_ANSWER]) != 0:
		res = write(res, NO_ANSWER, a)

	bot.send_message(message.chat.id, res, reply_markup = markup)


# student =================================================================

@bot.message_handler(regexp = STUDENT)
def student(message):
	bot.send_message(message.chat.id, ID_ENTER)


@bot.message_handler(regexp = YES)
def yes(message):
	check(message)
	attend(message, YES)

@bot.message_handler(regexp = NO_SLEEP)
def no_sleep(message):
	check(message)
	attend(message, NO_SLEEP)

@bot.message_handler(regexp = NO_HEALTH)
def no_health(message):
	check(message)
	attend(message, NO_HEALTH)

@bot.message_handler(regexp = NO_FAMILY)
def no_family(message):
	check(message)
	attend(message, NO_FAMILY)

@bot.message_handler(regexp = NO_OTHER)
def no_other(message):
	check(message)
	attend(message, NO_OTHER)

@bot.message_handler(content_types = ['text'])
def id(message):
	a = listt.search(Query().id == str(message.text))
	if len(a) == 0:
		return

	if str(message.chat.id) in a[0]['ls']:
		return

	b = a[0]
	b["ls"].append(str(message.chat.id))
	c = b["ls"]

	listt.update({"ls": c}, Query().id == message.text)


# other functions =================================================================

def write(res, msg, arr):
	if msg == YES:
		res += _YES
	elif msg == NO_FAMILY:
		res += _NO_FAMILY
	elif msg == NO_SLEEP:
		res += _NO_SLEEP
	elif msg == NO_OTHER:
		res += _NO_OTHER
	elif msg == NO_HEALTH:
		res += _NO_HEALTH
	elif msg == NO_ANSWER:
		res += _NO_ANSWER

	for i in arr[msg]:
		if len(names.search*Query().id == i)) != 0:
			b = names.search(Query().id == i)[0]
			res += b['name'] + '\n'

	res += '\n'

	return res

def check(message):
	a = []
	for i in listt.all():
		if str(message.chat.id) in i['ls']:
			a = i['id']
			break

	if len(a) == 0:
		return

	b = listt.search(Query().id == a)[0]
	if b['status'] == 'false': 
		return

	c = att.search(Query().id == a)[0]
	e = ''
	d = []

	if str(message.chat.id) in c[YES]:
		d = remove(message, YES, c)
		e = YES

	elif str(message.chat.id) in c[NO_SLEEP]:
		d = remove(message, NO_SLEEP, c)
		e = NO_SLEEP

	elif str(message.chat.id) in c[NO_HEALTH]:
		d = remove(message, NO_HEALTH, c)
		e = NO_HEALTH

	elif str(message.chat.id) in c[NO_OTHER]:
		d = remove(message, NO_OTHER, c)
		e = NO_OTHER

	elif str(message.chat.id) in c[NO_FAMILY]:
		d = remove(message, NO_FAMILY, c)
		e = NO_FAMILY

	if e != '':
		att.update({e: d}, Query().id == a)


def remove(message, msg, arr):
	arr[msg].remove(str(message.chat.id))

	d = arr[msg]

	return d
	

def attend(message, msg):
	a = []
	for i in listt.all():
		if str(message.chat.id) in i['ls']:
			a = i['id']
			break

	if len(a) == 0:
		return

	b = listt.search(Query().id == a)[0]
	if b['status'] == 'false': 
		return

	c = att.search(Query().id == a)[0]
	c[msg].append(str(message.chat.id))
	d = c[msg]

	att.update({msg: d}, Query().id == a)

# main =================================================================

if __name__ == '__main__':
	print('Started')
	bot.polling()
