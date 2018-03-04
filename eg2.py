a="b'/home/jessuva/.config/sublime-text-3/Packages/User/eg.cpp:2:9: error: empty filename in #include\n #include<>\n         ^\n/home/jessuva/.config/sublime-text-3/Packages/User/eg.cpp: In function \xe2\x80\x98int main()\xe2\x80\x99:\n/home/jessuva/.config/sublime-text-3/Packages/User/eg.cpp:8:5: error: \xe2\x80\x98i\xe2\x80\x99 was not declared in this scope\n  if(i===1)\n     ^\n/home/jessuva/.config/sublime-text-3/Packages/User/eg.cpp:8:8: error: expected primary-expression before \xe2\x80\x98=\xe2\x80\x99 token\n  if(i===1)\n        ^\n/home/jessuva/.config/sublime-text-3/Packages/User/eg.cpp:10:2: error: \xe2\x80\x98fori\xe2\x80\x99 was not declared in this scope\n  fori=1;i<12;i-!)\n  ^\n/home/jessuva/.config/sublime-text-3/Packages/User/eg.cpp:10:9: error: \xe2\x80\x98i\xe2\x80\x99 was not declared in this scope\n  fori=1;i<12;i-!)\n         ^\n/home/jessuva/.config/sublime-text-3/Packages/User/eg.cpp:10:17: error: expected primary-expression before \xe2\x80\x98)\xe2\x80\x99 token\n  fori=1;i<12;i-!)\n                 ^\n'"

import re

starts = [m.start() for m in re.finditer("error:",a)]

lis_of_err=[]

for error_start in starts:
	str_t = ""
	i = error_start
	while True:
		str_t = str_t + a[i]
		i = i + 1
		if a[i] == '\n':
			break
	#print(str_t[7:].decode())
	lis_of_err.append(str_t[7:])

print(lis_of_err)

