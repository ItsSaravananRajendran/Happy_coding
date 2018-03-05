import sublime
import sublime_plugin
import os
import sys
import re
import subprocess
import json
import uuid

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
		print (output)
		if rc is not 0:
			if compiler == "python2":
				tag = "python2"
				ind = output.index('^')
				#print ("Output = ",output)
				lineNo = output[output.find("line") + 4:]
				lineNo = int(lineNo.split('\n')[0])
				#print ("Line No = ",lineNo)
				errString = output[ind+2:]
				print ("Error string ",errString)
				errString = errString.replace('\\n\'',' ')
				t = self.get_solution_stackoverflow(errString,compiler)
				self.create_phantoms(t,lineNo-1)

			elif compiler == "g++":
				tag="c++"
				starts = [m.end()+1 for m in re.finditer("error:",output)]
				lineByline = output.split('\n')
				cppStart = [I.find(".cpp")+5 for I in lineByline[1:]]
				lineNo = []
				count = 1
				for I in cppStart:
					if I > -1:
						print ("Before :" ,lineByline[count][I:])
						end = lineByline[count][I:].find(":")
						print (end)
						if end > -1:
							number = lineByline[count][I:I+end]
							print ("Number" ,number)
							lineNo.append(int(number))
					count +=1 



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

				count = 0
				for errors in lis_of_err:
					phantomContent=self.get_solution_stackoverflow(errors,compiler)
					self.create_phantoms(phantomContent,lineNo[count]-1)
					count += 1

		else:
			text = str(output)
			print ("rc = ",rc,"text =",text)
			SfCommand.run(self,edit)
			text =''
		


	def get_solution_stackoverflow(self,error_term,compiler):	
		temp_term = error_term
		error_term = error_term.replace(' ','%20')
		
		if not os.path.exists("/tmp/cache.txt"):
				d = dict()
				with open("/tmp/cache.txt", "w") as f:
						json.dump(d, f)
		with open("/tmp/cache.txt", "r") as f:
				d = json.load(f)
				if compiler in d:
						if error_term in d:
								#print("cache hit!")
								return d[compiler][error_term]
				else:
					d[compiler] = dict()



		url = "http://api.stackexchange.com/2.2/search?page=1&pagesize=10&order=desc&sort=votes&site=stackoverflow&tagged"+tag+"&intitle="+error_term+"&key=Rk74w3DkV08lYi62tlFJag((&filter=!Sm*O0f69(tqGyj3*s1"
	
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
						with open("/tmp/cache.txt", "w") as f:
							d[compiler][error_term] = con
							json.dump(d, f)
						return con

			#con =  str(lidwin['items'][0]['answers'][0]['body'])

		except KeyError:
			con = temp_term
			with open("/tmp/cache.txt", "w") as f:
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


	def create_phantoms(self,content,line):
		width = (int(len(content)*7.8))
		if (width > 400):
			width = 400
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
		
		regions = [ sublime.Region(0, self.view.size()) ]
		regions = self.view.split_by_newlines(regions[0])
		lineRegion = regions[line]		
		name = str(uuid.uuid4())		
		self.view.add_phantom(name, lineRegion,html, sublime.LAYOUT_BLOCK, 
			on_navigate=lambda href: self.view.erase_phantoms(name))








class SfprintCommand(sublime_plugin.TextCommand):
	def run(self, edit):
	    self.view.insert(edit, self.view.size(), text)

class SfCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.panel = self.view.window().create_output_panel('sf_st3_output')
		self.view.window().run_command('show_panel', { 'panel': 'output.sf_st3_output' })
		self.panel.run_command('sfprint');


