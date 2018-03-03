import sublime
import sublime_plugin
import os
import sys
import re
import subprocess
import json

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'Packages')

sys.path.append(vendor_dir)

import requests

user_api_key = "xQnIkNqv3yeDM22)6iIMPw(("

if not user_api_key: user_api_key = None

import stackexchange
so = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key, impose_throttling=True)



text = ''
tag=''

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit,**args):
		global text 
		text = ""
		file = self.view.file_name()
		file_name = file.split('.')
		ext = file_name[-1]
		if ext == 'py':
			compiler = 'python2'
			args = [compiler,'-u',file]
		elif ext == 'c':
			compiler = 'gcc'
			args = [compiler,file]
		elif ext == 'cpp':
			compiler = 'g++'
			args = [compiler,file]
		child = subprocess.Popen(args=args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		output = str(child.communicate()[0].decode("UTF-8"))
		rc = child.returncode
		#print (output)
		if rc is not 0:
			if compiler == "python2":
				tag = "python2"
				ind = output.index('^')
				errString = output[ind+2:]
				errString = errString.replace('\\n\'',' ')
				print (errString)
				t = self.get_solution_stackoverflow(errString,compiler)
				self.create_phantoms(t)

			elif compiler == "g++":
				tag="c++"
				#print("a")
				#print(type(output))
				#print(output)
				#print(output.find("error:"))
				starts = [m.end()+1 for m in re.finditer("error:",output)]
				lis_of_err=[]
				for error_end in starts:
					str_t = ""
					i = error_end
					while True:
						str_t = str_t + output[i]
						i = i + 1
						if output[i] == '\n':
							break
					str_t = str_t.replace('#','%23')
					lis_of_err.append(str_t)

				print(lis_of_err)

				for errors in lis_of_err:
					print(errors)
					t=self.get_solution_stackoverflow(errors,compiler)
					self.create_phantoms(t)

		else:
			text = str(output)
			print ("rc = ",rc,"text =",text)
			SfCommand.run(self,edit)
			text =''
		


	def get_solution_stackoverflow(self,error_term,compiler):	
		temp_term = error_term
		error_term = error_term.replace(' ','%20')
#		url = "https://api.stackexchange.com/2.2/search?page=1&pagesize=10&order=desc&sort=activity&tagged="+tag+"&intitle="+error_term+"&site=stackoverflow&filter=!Sm*O0f69(tqGyj3*s1"
		
		#check if cache exists and create it if it doesn't exist
		if not os.path.exists("/home/thunderbolt/Desktop/cache.txt"):
				d = dict()
				with open("/home/thunderbolt/Desktop/cache.txt", "w") as f:
						json.dump(d, f)
		with open("/home/thunderbolt/Desktop/cache.txt", "r") as f:
				d = json.load(f)
				if compiler in d:
						if error_term in d:
								print("cache hit!")
								return d[compiler][error_term]
				else:
					d[compiler] = dict()



		url = "http://api.stackexchange.com/2.2/search?page=1&pagesize=10&order=desc&sort=activity&site=stackoverflow&tagged"+tag+"&intitle="+error_term+"&key=Rk74w3DkV08lYi62tlFJag((&filter=!Sm*O0f69(tqGyj3*s1"
	
		print("url going to call is:",url)
		data = requests.get(url)
		lidwin = data.json()
		
		try:

			if "items" not in lidwin.keys():
				raise KeyError("kick liddu")

			if lidwin["items"] == []:
				raise KeyError("kick david");

			elif lidwin["items"] != []:
				items = lidwin["items"]

				for item in items:
					if "answers" in item.keys(): 
						con = item["answers"][0]["body"]
						with open("/home/thunderbolt/Desktop/cache.txt", "w") as f:
							d[compiler][error_term] = con
							json.dump(d, f)
						return con

			#con =  str(lidwin['items'][0]['answers'][0]['body'])

		except KeyError:
			con = temp_term
			with open("/home/thunderbolt/Desktop/cache.txt", "w") as f:
				d[compiler][error_term] = con
				json.dump(d, f)
			return con
		
		#print (con)

		con = con.replace('\n','<br />')
		con = con.replace('<pre>','<div class="preCode"><pre>')
		con = con.replace('</pre>','</pre></div>')
		self.create_phantoms(con)
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


