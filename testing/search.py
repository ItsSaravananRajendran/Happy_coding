#!/usr/bin/env python
from __future__ import print_function

# a hack so you can run it 'python demo/search.py'
import sys
from pprint import pprint
sys.path.append('.')
sys.path.append('../Packages')

try:
    get_input = raw_input
except NameError:
    get_input = input

user_api_key = "xQnIkNqv3yeDM22)6iIMPw(("

if not user_api_key: user_api_key = None

import stackexchange
so = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key, impose_throttling=False)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        term = get_input('Please provide a search term:')
    else:
        term = ' '.join(sys.argv[1:])
    print('Searching for %s...' % term,)
    sys.stdout.flush()

    qs = so.search(intitle=term)

    print('\r--- questions with "%s" in title ---' % (term))
    
    #print(type(qs.json()))
    
#    print(vars(qs))
    	
    
#print(type(qs))

    for i in qs:
	for j in i.transfer[-1]:
		print(type(j[1]))
	
    	
'''
    for q in qs:
        ques = so.question(q.id)
        print('--- %s ---' % ques.title)
        print(type(ques))
        print('%d answers.' % len(ques.answers))

	print(len(ques.answers))
#	for i in ques.answers:
#		print(i)        

	#ans = ques.answers[0].json['answer_id']
        #a = so.answer(ans)
        #print (a)
        
'''


