import sublime, sublime_plugin, re

# - Unikum AB -
# Skapat av Pierre Schönbeck

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
		#f = sublime.active_window().new_file()
		for line in reversed(unusedIDL):
			self.view.erase(edit, self.view.full_line(line))
			#counter += f.insert(edit, counter, self.view.substr(self.view.full_line(line)))
		#f.set_syntax_file("Packages/User/BETA.sublime-syntax")
		#sublime.active_window().focus_view(f)

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

class UnusedFunctionsCommand(sublime_plugin.TextCommand):
	# Lägg till support för declare!
	def run(self, edit):
		functions = {}
		unusedFunc = []
		sourceStart = self.view.find(">SOURCE", 0)
		lines = self.view.lines(sublime.Region(sourceStart.b, self.view.size()))
		for line in lines:
			text = self.view.substr(line)
			if text.upper().startswith("FUNCTION"):
				patFunc = re.compile("function", re.IGNORECASE)
				patType = re.compile("(str|bool|int)", re.IGNORECASE)
				text = patFunc.sub("", text)
				text = patType.sub("", text)
				indexEnd = text.index("(")
				text = text[:indexEnd]
				text = text.strip(" \t\n\r")
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



