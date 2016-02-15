import sublime, sublime_plugin, re

# Uni-Dev-Tools
# - Unikum AB -
# Skapat av Pierre Schönbeck

# ---------------------------------------------
# Rensar alla IDL-texter som inte används.
# ---------------------------------------------
class CleanIdlCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regions = self.view.find_all("(?i)IDL_\d+")	# Hitta alla ställen där IDL-nummer finns
		source = self.view.find(">SOURCE", 0)		# Hitta var källkoden börjar
		beforeCode = [x for x in regions if x.b < source.a]
		afterCode = [self.view.substr(x) for x in regions if x.a > source.b]
		unusedIDL = []
		for idl in beforeCode:
			if self.view.substr(idl) not in afterCode:
				unusedIDL.append(idl)

		# Rensa automatiskt eller visa IDL-texter i annan flik beroende på inställningar
		if self.view.settings().get("auto_idl_removal"):
			for line in reversed(unusedIDL):
				self.view.erase(edit, self.view.full_line(line))
		else:
			counter = 0
			f = sublime.active_window().new_file()
			for line in reversed(unusedIDL):
				counter += f.insert(edit, counter, self.view.substr(self.view.full_line(line)))
			f.set_syntax_file("Packages/User/BETA.sublime-syntax")
			sublime.active_window().focus_view(f)

# ---------------------------------------------
# Ger en lista över alla rader med strängar som
# saknar en lng_text på samma rad.
#
# Notera att denna funktion inte tar hänsyn 
# till om två eller flera strängar finns på 
# samma rad och åtminstånde en av dessa visas
# genom lng_text.
# ---------------------------------------------
class ListAllStringsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regions = self.view.find_all("('|\").+('|\")")
		sourceStart = self.view.find(">SOURCE", 0)
		pattern = re.compile(".+(?i)lng_text.+")
		regions = [x for x in regions if x.b > sourceStart.b and not pattern.match(self.view.substr(self.view.full_line(x)))]
		f = sublime.active_window().new_file()
		counter = 0
		for line in regions:
			counter += f.insert(edit, counter, self.view.substr(self.view.full_line(line)))
		f.set_syntax_file("Packages/User/BETA.sublime-syntax")
		sublime.active_window().focus_view(f)

# ---------------------------------------------
# Listar alla oanvända funktioner. Funktioner
# som ligger i filen men som saknar referenser
# kommer listas i en separat flik.
# ---------------------------------------------
class UnusedFunctionsCommand(sublime_plugin.TextCommand):
	def extractFunc(self, text, startswith):
		patFunc = re.compile(startswith + "\s", re.IGNORECASE)
		patType = re.compile("(str|bool|int)\s", re.IGNORECASE)
		text = patFunc.sub("", text)
		text = patType.sub("", text)
		indexEnd = text.index("(")
		text = text[:indexEnd]
		text = text.strip(" \t\n\r")
		return text

	def run(self, edit):
		functions = {}
		unusedFunc = []
		sourceStart = self.view.find(">SOURCE", 0)
		lines = self.view.lines(sublime.Region(sourceStart.b, self.view.size()))
		for line in lines:
			text = self.view.substr(line)
			if text.upper().startswith("FUNCTION"):
				text = self.extractFunc(text, "function")
				if text not in functions:
					functions[text] = 0
			elif text.upper().startswith("DECLARE"):
				text = self.extractFunc(text, "declare")
				functions[text] = 0
			else:
				for func in functions:
					if func in text:
						functions[func] += 1
		for func in functions:
			if functions[func] == 0:
				unusedFunc.append(func)
		f = sublime.active_window().new_file()
		counter = 0
		for line in unusedFunc:
			counter += f.insert(edit, counter, line + "\n")
		sublime.active_window().focus_view(f)

# ---------------------------------------------
# Aktivera automatisk IDL-borttagning.
# ---------------------------------------------
class EnableAutoIdlRemovalCommand(sublime_plugin.TextCommand):
	def run(self, edit, prop):
		self.view.settings().set(prop, True)

# ---------------------------------------------
# Deaktivera automatisk IDL-borttagning.
# ---------------------------------------------
class DisableAutoIdlRemovalCommand(sublime_plugin.TextCommand):
	def run(self, edit, prop):
		self.view.settings().set(prop, False)

