import sublime, sublime_plugin, re

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
		regions = [x for x in regions if x.b > sourceStart.b and not pattern.match(self.view.substr(self.view.full_line(x)))] #"lng_text" not in self.view.substr(self.view.full_line(x))]
		f = sublime.active_window().new_file()
		counter = 0
		for line in regions:
			counter += f.insert(edit, counter, self.view.substr(self.view.full_line(line)))
		f.set_syntax_file("Packages/User/BETA.sublime-syntax")
		sublime.active_window().focus_view(f)

