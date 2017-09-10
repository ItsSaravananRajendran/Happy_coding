from __future__ import print_function    
import sublime
import sublime_plugin
import os
import sys
import subprocess

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'Packages')

sys.path.append(vendor_dir)
import stackexchange

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#self.view.insert(edit, 0, "Happy coding!!!``")
		user_api_key = None
		so = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key, impose_throttling=True)
		term = "vim stack"
		qs = so.search(intitle=term)
		i = 0
		for q in qs:
			self.view.insert(edit,0,q.title+"\n")
			