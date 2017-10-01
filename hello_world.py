import sublime
import sublime_plugin
import os
import sys
import subprocess

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'Packages')

sys.path.append(vendor_dir)

import requests

text = 'hello people'

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit,**args):
		global text 
		#self.view.insert(edit, 0, args['parameter']+self.view.file_name())
		text = ""
		self.get_solution_stackoverflow("hello world")



	def get_solution_stackoverflow(self,error_term):	
		term = "vim quit"
		error_term = error_term.replace(' ','%20')
		url = "https://api.stackexchange.com/2.2/search?page=1&pagesize=10&order=desc&sort=activity&tagged=python&intitle="+error_term+"&site=stackoverflow&filter=!Sm*O0f69(tqGyj3*s1"
		data = requests.get(url)
		json = data.json()
		con =  str(json['items'][0]['tags'])
		self.create_phantoms(con)
		#SfCommand.run(self,edit)


	def create_phantoms(self,content):
		#content = 'Hello, <b>World!</b><br /><a href="https://www.sublimetext.com/">Click here to go to the ST3 website in your default browser</a>'
		width = str(int(len(content)*7.8))
		
		html =  '''<body id="my-plugin-feature">
					   <style>
					   		div.error {
			   					background-color: color(var(--background) blend(red 50%));
			   					padding: 5px;
			   					border-radius:2px;
			   					width:'''+width+'''px;
					   		}
					   		div.empty{
					   			background-colot:white;	
					   		}
					   		a{
					   			padding:5px; 
					   		}
					   	</style>
					   	<div class="error">''' + content + '  <a href=hide>'+chr(0x00D7)+'''</a>
					   	</div>
					   	
				   	</body>'''
		
		self.view.add_phantom("test", self.view.sel()[0],html, sublime.LAYOUT_BLOCK, 
			on_navigate=lambda href: self.view.erase_phantoms("test"))
		



class SfprintCommand(sublime_plugin.TextCommand):
	def run(self, edit):
	    self.view.insert(edit, self.view.size(), text)

class SfCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.panel = self.view.window().create_output_panel('sf_st3_output')
		self.view.window().run_command('show_panel', { 'panel': 'output.sf_st3_output' })
		self.panel.run_command('sfprint');


