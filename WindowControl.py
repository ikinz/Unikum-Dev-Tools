# ---------------------------------------------
# Klass som definerar en kontroll i BETA.
# ---------------------------------------------
class WindowControl():
	def __init__(self, view, name, ctrlType, dnr):
		self.view = view
		self.name = name
		self.type = ctrlType
		self.dnr = dnr
		self.events = self.generateEvent()

	def __str__(self):
		string = ""
		for e in self.events:
			string += e + ";"
		return string

	def alreadyExists(self, event):
		eRegion = self.view.find("event", self.view.find(">SOURCE", 0).b)
		return not eRegion == None

	def generateEvent(self):
		ctrlEvents = []
		eventNames = self.getEventFunc(self.type)
		for e in eventNames:
			if not self.alreadyExists("@" + self.name + e):
				ctrlEvents.append(getEventArr(e))
		return ctrlEvents

	def getEventFunc(self, ctrlType):
		return {
			"EF": ["_setupchanged","_show","_select"],
			"D": []
		}.get(ctrlType, "")

	def getEventArr(self, eventName):
		return {
			"_setupchanged": 		"\n\n@?name?_setupchanged\n\tlvEdFindPrepare(?name?,X,X,\"\")",
			"_show": 				"\n\n@?name?_show(int iLu, str sKey)\n\tlvEdfindShow(X,iLu,sKey,\"\")",
			"_select": 				"\n\n@?name?_select\n\t// TODO"
		}.get(eventName, "")	