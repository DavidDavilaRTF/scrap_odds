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

xpath_block = "//ms-event[contains(@class,'grid-event ms-active-highlight')]"
driver = create_browser()
url = ['https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/france-16/ligue-1-102843',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/france-16/ligue-2-102376',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/allemagne-17/bundesliga-102842',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/allemagne-17/2-bundesliga-102845',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/angleterre-14/premier-league-102841',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/angleterre-14/championship-102839',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/espagne-28/laliga-102829',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/espagne-28/laliga-2-102830',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/italie-20/serie-a-102846',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/italie-20/serie-b-102848',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/belgique-35/jupiler-pro-league-102836',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/%C3%A9cosse-26/premiership-102853',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/gr%C3%A8ce-18/super-league-102844',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/pays-bas-36/eredivisie-102847',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/portugal-37/primeira-liga-102851',
	'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/turquie-31/s%C3%BCper-lig-102832']
mat_bwin = pandas.DataFrame()
k = 0
for urli in url:
	if k in vect_k:
		driver.get(urli)
		time.sleep(5)
		try:
			element = driver.find_element_by_xpath("//span[@class = 'ui-icon theme-ex']")
			element.click()
		except:
			pass
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
			c.fill_equipe_dom(xpath = ".//div[@class = 'participant-wrapper'][1]",attr = 'innerHTML',regex = '(?<=>)[^<]+(?=<)')
			if (c.equipe_dom.replace(' ','').replace('\n','').replace('\t','') in list(mat['dom'])) == False and (c.equipe_dom.replace(' ','').replace('\n','').replace('\t','') in list(mat['ext'])) == False:
				c.fill_equipe_ext(xpath = ".//div[@class = 'participant-wrapper'][2]",attr = 'innerHTML',regex = '(?<=>)[^<]+(?=<)')
				c.fill_cote_dom(xpath = ".//ms-option[contains(@class,'grid-option')][1]//ms-font-resizer",attr = 'innerHTML',regex = '')
				c.fill_cote_nul(xpath = ".//ms-option[contains(@class,'grid-option')][2]//ms-font-resizer",attr = 'innerHTML',regex = '')
				c.fill_cote_ext(xpath = ".//ms-option[contains(@class,'grid-option')][3]//ms-font-resizer",attr = 'innerHTML',regex = '')
				c.fill_date(xpath = ".//ms-prematch-timer[contains(@class,'starting-time')]",attr = 'innerHTML',regex = '')
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
		mat_bwin = mat_bwin.append(mat)
	k += 1
driver.quit()
mat_bwin.to_csv('C:/Foot_New/Prod/bwin.csv',sep = ';',index = False)
