import sublime
import sublime_plugin
import os
import sys
import json
import subprocess

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'Packages')

sys.path.append(vendor_dir)

import requests

text = ''

class ExampleCommand(sublime_plugin.TextCommand):
	compiler = None
	def run(self, edit,**args):
		global text 
		text = ""
		file = self.view.file_name()
		file_name = file.split('.')
		ext = file_name[-1]
		if ext == 'py':
			self.compiler = 'python2'
			args = [self.compiler,'-u',file]
		elif ext == 'c':
			self.compiler = 'gcc'
			args = [self.compiler,file]
		elif ext == 'c++':
			self.compiler = 'g++'
			args = [self.compiler,file]
		child = subprocess.Popen(args=args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		output = str(child.communicate()[0])
		rc = child.returncode  
		print (output)
		if rc is not 0:
			ind = output.index('^\\n')
			print ("Works")
			errString = output[ind+3:]
			errString = errString.replace('\\n\'',' ')
			print (errString)
			con = self.get_solution_stackoverflow(errString,self.compiler)
			self.create_phantoms(con)
		else:
			text = str(output)
			print ("rc = ",rc,"text =",text)
			SfCommand.run(self,edit)
			text =''
		

	def cache(func):
			

		def newfunc(*args, **kwargs):
			if not os.path.isfile("/home/thunderbolt/Desktop/cache.txt"):
				with open("/home/thunderbolt/Desktop/cache.txt",'w') as file:
					d = dict()
					file.write(json.dumps(d))			
			with open("/home/thunderbolt/Desktop/cache.txt","r+") as f:
				data = json.loads(f.read())
				if compiler not in data:
					data[self.compiler] = dict()
				if error_term not in data[self.compiler]:
					data[self.compiler][error_term] = ""
				else:
					if error_term in data[self.compiler]:
						return data[self.compiler][error_term]

				output = func(*args, **kwargs)
				data[self.compiler][error_term] = output
				f.write(json.dumps(data))
				return output



		return newfunc


					
	#@lru_cache(maxsize=128, typed=False)
	@cache
	def get_solution_stackoverflow(self,error_term,ext):	
		error_term = error_term.replace(' ','%20')
		#url = "https://api.stackexchange.com/2.2/search?page=1&pagesize=10&order=desc&sort=activity&intitle="+error_term+"&site=stackoverflow&filter=!Sm*O0f69)((zta.WGi"
		url = "https://api.stackexchange.com/2.2/search?page=1&pagesize=10&order=desc&sort=activity&tagged="+ext+"&intitle="+error_term+"&site=stackoverflow&filter=!Sm*O0f69(tqGyj3*s1"
		data = requests.get(url)
		json = data.json()
		con =  str(json['items'][0]['answers'][0]['body'])
		con = con.replace('\n','<br />')
		con = con.replace('<pre>','<div class="preCode"><pre>')
		con = con.replace('</pre>','</pre></div>')
		return con


	def style(self,content):
		return content


	def create_phantoms(self,content):
		width = (int(len(content)*7.8))
		html =  '''<html><body id="my-plugin-feature">
					   <style>
							div.error {
								background-color: color(var(--background) blend(red 70%));
								padding: 5px;
								border-radius:2px;
								width:'''+str(width)+'''px;
								}
							div.preCode{
								background-color:color(var(--background) blend(grey 70%));	
								padding: 5px;
								width:'''+str(width-15)+'''px;
							}
							a{
								padding:5px; 
							}
						</style>
						<div class="error">''' + content + '  <a href=hide>'+chr(0x00D7)+'''</a>
						</div>
						
					</body></html>'''
		with open("/home/thunderbolt/out.html",'w') as file:
			file.write(html)

		
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


