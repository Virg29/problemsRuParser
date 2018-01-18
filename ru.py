from bs4 import BeautifulSoup as BeautifulSoup
import requests
import json
from lxml import html
import time
httpproxy = "http://117.135.251.131:80"
proxyDict = {
	"http" : httpproxy
}
text1 = ''
text2 = ''
text3 = ''
strcount = 63
page = 0
listofhrefs = []
questions = []
hints = []
answers = []
pr = 0
fileaddres = open('/home/danila/Site.txt','w')
file = open('/home/danila/Parse.txt','w')

def contains(m_g,c_w):
	print('contains')
	l_m_g = list(m_g)
	l_c_w = list(c_w)
	m_n = 0
	c_n = 0
	y_n = 0
	while True:
		if (m_n == len(m_g)):
			break
		elif (c_n == len(c_w)):
			c_n = 0
		if(l_m_g[m_n] == l_c_w[c_n]):
			m_n = m_n + 1
			c_n = c_n + 1
			if (c_n == len(c_w)):
				y_n = 1
				break
		else:
			m_n = m_n + 1
			c_n = 0
	return y_n
while page < strcount:
	listofhrefs.clear()
	answers.clear()
	hints.clear()
	questions.clear()
	print('gethtmlpreview')
	pagenumber = page * 5
	request = requests.get('http://problems.ru/view_by_subject_new.php?parent=79&start=' + str(pagenumber))
	soupoffirstpage = BeautifulSoup(request.content.decode('KOI8-R'))
	listofatag = soupoffirstpage.findAll('a',attrs={'class' : 'componentboxlink'})
	i = 0
	while i < len(listofatag):
		tagaoni = listofatag[i]
		straoni = str(listofatag[i])
		if (contains(tagaoni['href'],'id') == 1) and (contains(straoni, 'Решение') == 1):
			fileaddres.write(str(tagaoni['href']) + '\n')
			listofhrefs.append(tagaoni['href'])
		else: 
			pass
		i += 1
	print(len(listofhrefs))
	i = 0
	while i < len(listofhrefs):	
		print('listhref')
		time.sleep(1)
		addresoftask = 'http://problems.ru' + listofhrefs[i]
		if (page%2 == 0):
			if (pr == 0):
				pr = 1
			else:
				pr = 0	
		if (pr == 1):
			print('useproxy')
			request = requests.get(addresoftask,proxies = proxyDict)
		else:
			print('notuseproxy')
			request = requests.get(addresoftask)
		print('получение п тегов')
		soupofsecondpage = BeautifulSoup(request.content.decode('KOI8-R'))
		box = soupofsecondpage.find("div", {"class":"componentboxcontents"})
		strofbox = str(box)
		strofbox = strofbox.lower()
		if (contains(strofbox,'<img src="show_document.php?id=')==1):
			print('картинка')
			pass
		else:
			print(box.findAll('p'))
			listofptag = box.findAll('p')
			try:
				print(listofptag[0].nextSibling.strip())
				print(listofptag[1].nextSibling.strip())
				print(listofptag[2].nextSibling.strip())
			except Exception:
				print('Error')
				listofptag.clear()
			else:
				text1 = listofptag[0].nextSibling.strip()
				text2 = listofptag[1].nextSibling.strip()
				text3 = listofptag[2].nextSibling.strip()
				if(contains(text1,'"') == 1):
					j = 0
					while j < len(text1):
						if (text1[j] == '"'):
							text1 = text1[0:j] + '*' + text1[j+1:len(text1)]
						j += 1
				if(contains(text2,'"') == 1):
					j = 0
					while j < len(text2):
						if (text2[j] == '"'):
							text2 = text2[0:j] + '*' + text2[j+1:len(text2)]
						j += 1				
				if(contains(text3,'"') == 1):
					j = 0
					while j < len(text3):
						if (text3[j] == '"'):
							text3 = text3[0:j] + '*' + text3[j+1:len(text3)]
						j += 1
				try:
					print(text1)
					questions.append(text1)	
				except IndexError :
					questions.append('Exception')
	

				try:
					hints.append(text2)
				except IndexError:
					hints.append('Exception')
	

				try:
					answers.append(text3)
				except IndexError:
					answers.append('Exception')
		i += 1
	i = 0
	print('write')
	while i < len(questions):
		file.write('{')
		file.write('"question":"'+str(questions[i]) + ' ", \n')
		file.write('"tip":"'+str(hints[i]) + ' ", \n')
		file.write('"answer":"'+str(answers[i]) + ' " \n')
		file.write('}, \n')
		i += 1		
	page += 1





