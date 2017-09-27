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
	def run(self, edit,**args):

		self.view.insert(edit, 0, os.path.basename(__file__))
		user_api_key = None
		so = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key, impose_throttling=True)
		term = "vim quit"
		#qs = so.search(intitle=term)
		i = 0
		#for q in qs:
		#	self.view.insert(edit,0,q.title+"\n")
		#self.view.replace(edit,allcontent,'                               ,|     \n                             //|                              ,|\n                           //,/                             -~ |\n                         // / |                         _-~   /  ,\n                       /\'/ / /                       _-~   _/_-~ |\n                      ( ( / /\'                   _ -~     _-~ ,/\'\n                       \\~\\/\'/|             __--~~__--\\ _-~  _/,\n               ,,)))))));, \\/~-_     __--~~  --~~  __/~  _-~ /\n            __))))))))))))));,>/\\   /        __--~~  \\-~~ _-~\n           -\\(((((\'\'\'\'(((((((( >~\\/     --~~   __--~\' _-~ ~|\n  --==//////((\'\'  .     `)))))), /     ___---~~  ~~\\~~__--~ \n          ))| @    ;-.     (((((/           __--~~~\'~~/\n          ( `|    /  )      )))/      ~~~~~__\\__---~~__--~~--_\n             |   |   |       (/      ---~~~/__-----~~  ,;::\'  \\         ,\n             o_);   ;        /      ----~~/           \\,-~~~\\  |       /|\n                   ;        (      ---~~/         `:::|      |;|      < >\n                  |   _      `----~~~~\'      /      `:|       \\;\\_____// \n            ______/\\/~    |                 /        /         ~------~\n          /~;;.____/;;\'  /          ___----(   `;;;/               \n         / //  _;______;\'------~~~~~    |;;/\\    /          \n        //  | |                        /  |  \\;;,\\              \n       (<_  | ;                      /\',/-----\'  _>\n        \\_| ||_                     //~;~~~~~~~~~ \n            `\\_|                   (,~~ \n                                    \\~\\ \n                                     ~~ \n')
	