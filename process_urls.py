"""test http request status code and latency
Remark: same http get request returns different status code 
Returns:
	[type] -- [description]
"""

# some urls return 403 while I can access the server by hand,
			# therefore I include user-agent in the header
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

import multiprocessing
import requests
import sys


import requests
# all subexceptions inherit from the base class below
from requests import ConnectionError

import multiprocessing
number_of_cpus = multiprocessing.cpu_count()
print(f"number_of_cpus={number_of_cpus}")
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
header = {'User-Agent': user_agent}
timeout=1.0 # what is the time unit here ?
pool = multiprocessing.Pool(processes=number_of_cpus)
urls_file = "list_of_urls"

from get_stuff import get_stuff

def get_all_urls(file=urls_file):
	with  open(file,"rb") as urls_file:
		urls = [url.rstrip().decode("utf-8") for url in urls_file]
	return urls



def main():
	urls = get_all_urls(file=urls_file)
	try:
		pool_outputs = pool.map(get_stuff, urls)	
	except ConnectionError as error:
		print(error)
		pass
	except KeyboardInterrupt as keyboard_exc:
		print(keyboard_exc)
		pass
	pool.close()
	print(pool_outputs)
			
if __name__ == '__main__':
	main()