from selenium import webdriver
import psutil
import pandas
import os
import numpy
import re
import time

class cotes:
	def __init__(self,block):
		self.equipe_dom = ''
		self.equipe_ext = ''
		self.cote_dom = ''
		self.cote_nul = ''
		self.cote_ext = ''
		self.date = ''
		self.ligue = ''
		self.block = block
	def find_element(self,xpath,attr,regex):
		start_time = time.time()
		get_elment = False
		try:
			content = self.block.find_element_by_xpath(xpath)
			get_elment = True
		except:
			pass
		if attr != '':
			content = content.get_attribute(attr)
		else:
			content = content.text
		if regex != '':
			content = re.findall(regex,content)
		else:
			content = [content]
		return content[0]
	def fill_equipe_dom(self,xpath,attr,regex):
		try:
			content = self.find_element(xpath,attr,regex)
			self.equipe_dom = content.lower().replace(' ','')
		except:
			pass
	def fill_equipe_ext(self,xpath,attr,regex):
		try:
			content = self.find_element(xpath,attr,regex)
			self.equipe_ext = content.lower().replace(' ','')
		except:
			pass
	def fill_cote_dom(self,xpath,attr,regex):
		try:
			content = self.find_element(xpath,attr,regex)
			self.cote_dom = content.replace('<!---->','').replace(',','.')
		except:
			pass
	def fill_cote_nul(self,xpath,attr,regex):
		try:
			content = self.find_element(xpath,attr,regex)
			self.cote_nul = content.replace('<!---->','').replace(',','.')
		except:
			pass
	def fill_cote_ext(self,xpath,attr,regex):
		try:
			content = self.find_element(xpath,attr,regex)
			self.cote_ext = content.replace('<!---->','').replace(',','.')
		except:
			pass
	def fill_ligue(self,xpath,attr,regex):
		try:
			content = self.find_element(xpath,attr,regex)
			self.ligue = content.lower()
		except:
			pass
	def fill_date(self,xpath,attr,regex):
		try:
			content = self.find_element(xpath,attr,regex)
			self.date = content.lower()
		except:
			pass

def create_browser():
	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246")
	driver = webdriver.Chrome(executable_path=r'C:/web_driver/chromedriver.exe',chrome_options=options)
	return driver

ligues = ['fr1','fr2','deu1','deu2','uk1','uk2','esp1','esp2','ita1','ita2',
			'bel1','eco1','gre1','hol1','prt1','tur1']
vect_k = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

xpath_block = "//div[@class = 'bet-event-main-row']"
driver = create_browser()
url = ['https://www.joa-online.fr/fr/sport/paris-sportifs/844/54287323',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/54288081',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/54297345',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/1397158588',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/54210798',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/223888023',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/1397387603',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/1415358638',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/54344509',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/54345125',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/227875758',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/913535989',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/223894659',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/54375423',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/1397317764',
		'https://www.joa-online.fr/fr/sport/paris-sportifs/844/223890517']
mat_jao = pandas.DataFrame()
k = 0
for urli in url:
	if k in vect_k:
		driver.get(urli)
		time.sleep(30)
		element = []
		start_time = time.time()
		while len(element) == 0 and time.time() - start_time < 10:
			element = driver.find_elements_by_xpath(xpath_block)
		
		mat = pandas.DataFrame()
		mat['dom'] = numpy.array([''] * len(element))
		mat['ext'] = numpy.array([''] * len(element))
		mat['c_dom'] = numpy.array([''] * len(element))
		mat['c_nul'] = numpy.array([''] * len(element))
		mat['c_ext'] = numpy.array([''] * len(element))
		mat['ligue'] = ligues[k]
		mat['date'] = numpy.array([''] * len(element))
		
		i = 0
		for e in element:
			c = cotes(e)
			c.fill_equipe_dom(xpath = ".//div[@class = 'bet-team-name bet-team1-name']//span",attr = 'innerHTML',regex = '')
			if (c.equipe_dom.replace(' ','').replace('\n','').replace('\t','') in list(mat['dom'])) == False and (c.equipe_dom.replace(' ','').replace('\n','').replace('\t','') in list(mat['ext'])) == False:
				c.fill_equipe_ext(xpath = ".//div[@class = 'bet-team-name bet-team2-name']//span",attr = 'innerHTML',regex = '')
				c.fill_cote_dom(xpath = ".//div[@class = 'bet-outcome-column'][1]//span[@class = 'odd']",attr = 'innerHTML',regex = '')
				c.fill_cote_nul(xpath = ".//div[@class = 'bet-outcome-column'][2]//span[@class = 'odd']",attr = 'innerHTML',regex = '')
				c.fill_cote_ext(xpath = ".//div[@class = 'bet-outcome-column'][3]//span[@class = 'odd']",attr = 'innerHTML',regex = '')
				if c.equipe_dom != '' and c.equipe_ext != '' \
					and c.cote_dom != '' and c.cote_nul != '' \
					and c.cote_ext != '':
					mat['dom'].iloc[i] = c.equipe_dom.replace(' ','').replace('\n','').replace('\t','')
					mat['ext'].iloc[i] = c.equipe_ext.replace(' ','').replace('\n','').replace('\t','')
					mat['c_dom'].iloc[i] = c.cote_dom.replace(',','.').replace(' ','').replace('\n','').replace('\t','')
					mat['c_nul'].iloc[i] = c.cote_nul.replace(',','.').replace(' ','').replace('\n','').replace('\t','')
					mat['c_ext'].iloc[i] = c.cote_ext.replace(',','.').replace(' ','').replace('\n','').replace('\t','')
					
					mat['date'].iloc[i] = c.date
					i += 1
			else:
				pass
		sel = mat['c_ext'] != ''
		mat = mat[sel]
		mat_jao = mat_jao.append(mat)
	k += 1
driver.quit()
sel = mat_jao['dom'] != ''
if sum(sel) > 0:
	mat_jao = mat_jao[sel]
mat_jao.to_csv('C:/Foot_New/Prod/jao.csv',sep = ';',index = False)
