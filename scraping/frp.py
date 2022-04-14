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

xpath_block = "//div[@class = 'global']"
driver = create_browser()
url = ['https://www.france-pari.fr/football/france/ligue-1-uber-eats-r',
	'https://www.france-pari.fr/football/france/ligue-2-bkt-r',
	'https://www.france-pari.fr/football/allemagne/bundesliga',
	'https://www.france-pari.fr/football/allemagne/bundesliga-2',
	'https://www.france-pari.fr/football/angleterre/premier-league',
	'https://www.france-pari.fr/football/angleterre/championship',
	'https://www.france-pari.fr/football/espagne/laliga',
	'https://www.france-pari.fr/football/espagne/laliga2',
	'https://www.france-pari.fr/football/italie/serie-a',
	'https://www.france-pari.fr/football/italie/serie-b',
	'https://www.france-pari.fr/football/belgique/jupiler-league',
	'https://www.france-pari.fr/football/ecosse/premiership',
	'https://www.france-pari.fr/competition/169-parier-sur-superleague-ellada',
	'https://www.france-pari.fr/football/pays-bas/eredivisie',
	'https://www.france-pari.fr/football/portugal/primeira-liga',
	'https://www.france-pari.fr/football/turquie/spor-toto-super-lig']
mat_frp = pandas.DataFrame()
k = 0
for urli in url:
	if k in vect_k:
		driver.get(urli)
		time.sleep(5)
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
			c.fill_equipe_dom(xpath = ".//div[@class = 'actors text-ellipsis']//span[1]",attr = '',regex = '')
			if (c.equipe_dom.replace(' ','').replace('\n','').replace('\t','') in list(mat['dom'])) == False and (c.equipe_dom.replace(' ','').replace('\n','').replace('\t','') in list(mat['ext'])) == False:
				c.fill_equipe_ext(xpath = ".//div[@class = 'actors text-ellipsis']//span[2]",attr = '',regex = '')
				c.fill_cote_dom(xpath = ".//a[@title = '1']//span[contains(text(),',')]",attr = '',regex = '')
				c.fill_cote_nul(xpath = ".//a[@title = 'X']//span[contains(text(),',')]",attr = '',regex = '')
				c.fill_cote_ext(xpath = ".//a[@title = '2']//span[contains(text(),',')]",attr = '',regex = '')
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
		mat_frp = mat_frp.append(mat)
	k += 1
driver.quit()
mat_frp.to_csv('C:/Foot_New/Prod/frp.csv',sep = ';',index = False)
