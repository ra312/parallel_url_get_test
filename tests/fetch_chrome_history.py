import os
import sqlite3

def load_chrome_urls():
	"""
	loads local user's Google Chrome URL istory
	"""
	#path to user's history database (Chrome)
	data_path = os.path.expanduser('~')+"/Library/Application Support/Google/Chrome/Default"
	files = os.listdir(data_path)
	history_db = os.path.join(data_path, 'history')
	#querying the db
	c = sqlite3.connect(history_db)
	cursor = c.cursor()
	select_statement = "SELECT urls.url FROM urls, visits WHERE urls.id = visits.url;"
	cursor.execute(select_statement)

	results = cursor.fetchall() #tuple
	urls = [result[0] for result in results]
	return urls

