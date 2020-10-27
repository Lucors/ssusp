# -*- coding: utf-8 -*-
import sys
import json
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree


#SSUSP --> SSU Schedule Parser
class SSUSP:
	def __init__(self, url=None, filename=None):
		if not (url is None):
			self.setPageByURL(url)
		self.setSoup(filename)

	def setPageByURL(self, url=None):
		try:
			if (url is None):
				self.pageURL = self.__urlCheck(input("Введите адрес: "), emitEx = True)
			else:
				self.pageURL = url
			self.page = requests.get(self.pageURL)
		except HTTPError as httpError:
			print("<!> Ошибка получения страницы: " + httpError)
		except Exception as ex:
			print("<!> Ошибка: " + str(ex))

	def __urlCheck(self, string, emitEx = False):
		template = "www.sgu.ru/schedule"
		if (string.find(template) != -1):
			return True
		if (emitEx):
			raise Exception("URL не содержит \""+template+"\"")
		return False

	def setSoup(self, filename=None):
		try:
			data = ""
			if (filename is None):
				data = self.page.text
			else:
				file = open(filename, 'r', encoding="utf-8")
				data = file.read()
				file.close()
				del self.pageURL
			self.soup = BeautifulSoup(data, 'lxml', parse_only = SoupStrainer("table"))
		except OSError as fileEx:
			print("<!> Ошибка открытия файла: " + str(fileEx))
#Связка BeautifulSoup + LXML слишком лояльная и по какой-то
# причине не испускает исключение lxml.etree.XMLSyntaxError
		except etree.XMLSyntaxError as parserError:
			print("<!> Ошибка парсера страницы: " + parserError)

	def parse(self):
		try:
			self.schedule = {}
			if (hasattr(self, "pageURL")):
				self.schedule["pageURL"] = self.pageURL
			self.schedule["schedule"] = []

			self.table = self.soup.select_one("#schedule")
			if (self.table is None):
				raise Exception("не обнаружен элемент \"#schedule\"")
			for day in range(6):
				self.schedule["schedule"].append([])
				for line in range(8):
					self.schedule["schedule"][day].append([])
					self.__parseLesson(line, day)
		except Exception as ex:
			print("<!> Ошибка: " + str(ex))

	def __parseLesson(self, line, day):
		lesson = self.table.find(id=(str(line+1)+"_"+str(day+1)))
		for lessonChild in lesson.children:
			self.schedule["schedule"][day][line].append({
				"parity": lessonChild.select_one(".l-pr-r").text,
				"type": lessonChild.select_one(".l-pr-t").text,
				"other": lessonChild.select_one(".l-pr-g").text,
				"title": lessonChild.select_one(".l-dn").text,
				"author": lessonChild.select_one(".l-tn").text,
				"location": lessonChild.select_one(".l-p").text
			})
			authorAnchor = lessonChild.select_one(".l-tn").find('a')
			if not (authorAnchor is None):
				self.schedule["schedule"][day][line][-1]["aHref"] = "https://www.sgu.ru/" + authorAnchor['href']

#Возвращает расписание в виде JSON строки
	def getDataAsJSON(self):
		try:
			return json.dumps(self.schedule, ensure_ascii=False, indent = 4, separators = (',', ':'))
		except:
			print("<!> Ошибка десериализации JSON")

#Возвращает расписание в виде словаря Python
	def getDataAsDict(self):
		return self.schedule

#Записывает данные JSON в файл filename
	def writeDataToFile(self, filename="schedule.json"):
		try:
			outputFile = open(filename, 'w', encoding="utf-8")
			outputFile.write(self.getDataAsJSON())
			outputFile.close()
		except OSError as fileEx:
			print("<!> Ошибка открытия файла: " + fileEx)



ssusp = SSUSP(url="https://www.sgu.ru/schedule/mm/do/342")
ssusp.parse()
# ssusp.getDataAsJSON()
# ssusp.getDataAsDict()
ssusp.writeDataToFile()
# ssusp.writeDataToFile(filename="test.json")