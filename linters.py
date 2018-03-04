import sublime
import sublime_plugin
import uuid

class TestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.c()
		self.c()

	def c(self):
		#self.view.insert(edit, 0, "Hello, World!")
		html =  '''<html><body id="my-plugin-feature">
					   <style>
							div.error {
								background-color: color(var(--background) blend(red 70%));
								padding: 5px;
								border-radius:2px;
								width:10px;
								}
							div.preCode{
								background-color:color(var(--background) blend(grey 70%));	
								padding: 5px;
								width:10px;
							}
							a{
								padding:5px; 
							}
						</style>
						<div class="error"> asdfsd sadfsdf <a href=hide>'''+chr(0x00D7)+'''</a>
						</div>
						
					</body></html>'''
		name = str(uuid.uuid4())
		print (vars(self.view.sel()))
		regions = [ sublime.Region(0, self.view.size()) ]
		regions = self.view.split_by_newlines(regions[0])
		reg = regions[0]

		self.view.add_phantom(name, reg,html, sublime.LAYOUT_BLOCK, on_navigate=lambda href: self.view.erase_phantoms(name))
		body = """\n <style>\n body {\n  background-color: #f1f1f1;\n}\n span {\n color: #aaaaaa;\n }\n </style>\n <span>ball </span> """
		#self.view.add_phantom("test", self.view.sel()[0], body, sublime.LAYOUT_INLINE)

