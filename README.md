# SSU Schedule Parser
# Парсер Расписания СГУ
***
Данный скрипт парсит страницу расписания СГУ (Входящая строка обязана содержать `www.sgu.ru/schedule`) в словарь Python.

Некоторые методы:
 * `def __init__(self, url=None, filename=None)` Инициализирует объект SSUSP с параметрами `url` — адрес страницы расписания, `filename` — html файл с расписанием;
 
 * `def setPageByURL(self, url=None)` Определяет страницу для парсинга. Если `url = None`, то запрашивает адрес в консоли;
 
 * `def setSoup(self, filename=None)` Определяет `self.soup` из контента страницы или из содержимого файла `filename`;
 
 * `def parse(self)` Парсит контент страницы;
 
 * `def getDataAsJSON(self)` Возвращает данные в виде JSON строки;
 
 * `def getDataAsDict(self)` Возвращает данные в виде словаря Python;
 
 * `def writeDataToFile(self, filename="schedule.json")` Записывает данные в виде JSON строки в файл `filename`.
