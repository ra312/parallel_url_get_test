"""test http request status code and latency
Remark: same http get request returns different status code 
Returns:
	[type] -- [description]
"""
import sys
from collections import Counter
import requests
import multiprocessing
number_of_cpus = multiprocessing.cpu_count()

from get_stuff import get_stuff
urls_file = 'list_of_urls'
def get_all_urls(file=urls_file):
	with  open(file,"rb") as urls_file:
		urls = [url.rstrip().decode("utf-8") for url in urls_file]
	return urls



def process_urls(urls):
	pool = multiprocessing.Pool(processes=number_of_cpus)
	try:
		pool_outputs = pool.map(get_stuff, urls)	
	except requests.exceptions.ConnectionError as error:
		print(error)
	except KeyboardInterrupt as keyboard_exc:
		print(keyboard_exc)
	except:
		print('Unhandled exception')
	pool.close()
	return pool_outputs

def print_response_and_stats(outputs):
	id_ps, responses = zip(*outputs)
	print('\n'.join(responses))
	stats = Counter(id_ps)
	for id_p, called_times  in stats.items():
		print(f"{id_p}:{called_times}")

if __name__ == '__main__':
	urls = get_all_urls(file=urls_file)
	pool = multiprocessing.Pool(processes=2*number_of_cpus)
	try:
		pool_outputs = pool.map(get_stuff, urls)	
	# catching keyboard Ctrl-C
	except KeyboardInterrupt as keyboard_exc:
		print(str(keyboard_exc))
		sys.exit(1)
	except requests.exceptions.RequestException as error:
		print(str(error))
	except Exception as error:
		print('Unhandled exception')
		print(str(error))
	pool.close()
	print_response_and_stats(pool_outputs)
	
