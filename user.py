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

	def getSecondDoc(self, id):
		tmpU = self.myMap.get(id)
		if tmpU == None:
			return None
		else:
			return tmpU.second_doc

class User:

	def __init__(self, anId):
		self.id = anId

	state = UserManager.STATE_EMPTY
	mode = UserManager.MOD_MERGE
	first_doc = ""
	second_doc = ""
	id=""

class Sub:
	number=0
	time=""
	text=""
