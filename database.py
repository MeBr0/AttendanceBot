from pymongo import MongoClient

HOST = 'localhost'
PORT = 27017

client = MongoClient(HOST, PORT)

def createTeacher(data, db = 'main', collection = 'l1'):
	_id = client[db][collection].insert(data)
	return _id

def find(data, db = 'main', collection = 'l1'):
	a = {data[0]: data[1]}
	return client[db][collection].find_one(a)

def createStudent(data, db = 'main', collection = 'l1'):
	a = {"chat_id": data[0], "students": data[1]}
	data[1].append(str(data[2]))
	b = {"chat_id": data[0], "students": data[1]}
	print(a)
	print(b)
	return client[db][collection].replace_one(a, b)




# listt: '123': {
# 	'false'
# 	'12312',
# 	'q1'
# }

# att: '123':
# 	'yes' : []
# 	'no_family' : []
# 	'no_health': []
# 	'no_answer': []