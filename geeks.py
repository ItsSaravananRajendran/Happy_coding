import sublime
import sublime_plugin
import urllib as r
import os, sys

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'Packages')

sys.path.append(vendor_dir)
from bs4 import BeautifulSoup as b



class GeeksCommand(sublime_plugin.TextCommand):
	
	def run(self, edit):
		link="https://www.geeksforgeeks.org/"
		file = self.view.file_name()
		file_name = file.split('.')
		ext = file_name[-1]
		if ext == 'py':
			file_type = "Python"
		elif ext == 'cpp':
			file_type = "C++"
		for region in self.view.sel():
			if  region.empty():
				lineRegion = self.view.sel()
				lineRegion = self.view.line(lineRegion)
				line = self.view.substr(lineRegion) + "\n"
			else:
				line =self.view.substr(region)
		link += line.replace(' ','-')
		print (line)

		page_html = r.request.urlopen(link)

		soup = b(page_html,"html.parser")

		#print(soup)

		Code_parent_tag = soup.find_all('div',class_='responsive-tabs')

		#print(Code_parent_tag[0])

		Codes=[]

		#self.view.insert(edit, 0, "Hello, World!")
		for i in Code_parent_tag:
			j = i.find_all("div",class_="tabcontent")
			Codes.append(j)

		i=0
		for code in j:
			j[i] = code.text
			i += 1
		#print(len(j))


		k = soup.find_all("h2",class_="tabtitle")

		Langs=[]

		for val in k:
			Langs.append(val.text)

		print(Langs)

		index=0

		for i in Langs:
			if file_type in i:
				break
			index += 1

		print(j[index])
		self.view.insert(edit, region.end(), j[index].replace("\r\n","\n"))
		self.view.erase(edit,region)
		