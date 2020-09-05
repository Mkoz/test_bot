import os

class UserManager:
	STATE_EMPTY = "0"
	STATE_FIRST_FILLED = "1"
	STATE_SECOND_FILLED = "2"

	MOD_MERGE = "0"
	MOD_ALIGNE = "1"

	#{id, User}
	myMap = dict()

	def setState(self, id, state):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			tmpU = User(id)

		tmpU.state = state
		self.myMap.update({id : tmpU})

	def setMode(self, id, mode):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			tmpU = User(id)

		tmpU.mode = mode
		self.myMap.update({id : tmpU})

	def dumpUser(self, id):
		return "state: " + self.getState(id) + " mod: " + self.getMode(id)

	def getState(self, id):
		tmpU = self.myMap.get(id)
		if tmpU != None:
			return tmpU.state
		else:
			return self.STATE_EMPTY

	def getMode(self, id):
		tmpU = self.myMap.get(id)
		if tmpU != None:
			return tmpU.mode
		else:
			return self.MOD_MERGE

	def setFirstDoc(self, id, file):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			tmpU = User(id)
		tmpU.first_doc = file
		self.myMap.update({id : tmpU})

	def setFirstDocName(self, id, name):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			tmpU = User(id)
		tmpU.first_doc_name = name
		self.myMap.update({id : tmpU})

	def setSecondDocName(self, id, name):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			tmpU = User(id)
		tmpU.second_doc_name = name
		self.myMap.update({id : tmpU})

	def setSecondDoc(self, id, file):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			tmpU = User(id)
		tmpU.second_doc = file
		self.myMap.update({id : tmpU})

	def getFirstDoc(self, id):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			return None
		else:
			return tmpU.first_doc

	def getFirstDocName(self, id):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			return None
		else:
			return tmpU.first_doc_name

	def getSecondDoc(self, id):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			return None
		else:
			return tmpU.second_doc

	def getSecondDocName(self, id):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			return None
		else:
			return tmpU.second_doc_name

	def getUser(self, id):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			tmpU = User(id)
		return tmpU

	def setMessId(self, id, aMessId):
		tmpU = self.myMap.get(id)
		if tmpU != None:
			tmpU.messId = aMessId

	def getMessId(self, id, aMessId):
		tmpU = self.myMap.get(id)
		if tmpU != None:
			return tmpU.messId
		else:
			return None

	def clean(self, id):
		user = self.myMap.get(id)
		print("id: " + user.id)

		user.state = self.STATE_EMPTY
		user.mode = ""
		first_doc_name = ""
		second_doc_name = ""
		os.remove(user.first_doc)
		os.remove(user.second_doc)
		user.first_doc = ""
		user.second_doc = ""

class User:

	def __init__(self, anId):
		self.id = anId
		self.state = UserManager.STATE_EMPTY
		self.mode = ""
		self.first_doc = ""
		self.second_doc = ""
		self.messId = 0

	state = UserManager.STATE_EMPTY
	mode = ""
	first_doc = ""
	first_doc_name = ""
	second_doc_name = ""
	second_doc = ""
	id = ""
	messId = 0

class Sub:

	def __init__(self, aNamber, aTime, aText):
		self.number = aNamber
		self.time = aTime
		self.text = aText

	def dump(self):
		print(self.number)
		print(self.time)
		print(self.text)
		print("--------------------------------")

	number="0"
	time=""
	text=""
