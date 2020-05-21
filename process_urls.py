"""test http request status code and latency
Remark: same http get request returns different status code 
Returns:
	[type] -- [description]
"""

# some urls return 403 while I can access the server by hand,
			# therefore I include user-agent in the header
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
import sys
# global_id = dict()
global_id = dict()
import requests
# all subexceptions inherit from the base class below


import multiprocessing
number_of_cpus = multiprocessing.cpu_count()
print(f"number_of_cpus={number_of_cpus}")

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
header = {'User-Agent': user_agent}
timeout=10.0 # what is the time unit here ?
pool = multiprocessing.Pool(processes=number_of_cpus)
urls_file = "list_of_urls"

from get_stuff import get_stuff

def get_all_urls(file=urls_file):
	with  open(file,"rb") as urls_file:
		urls = [url.rstrip().decode("utf-8") for url in urls_file]
	return urls



def process_urls(urls):
	try:
		pool_outputs = pool.map(get_stuff, urls)	
	except requests.ConnectionError as error:
		print(error)
	except KeyboardInterrupt as keyboard_exc:
		print(keyboard_exc)
	pool.close()
	return pool_outputs

def separate_stats_from_output(outputs):
	call_stats = dict((id_p,0) for id_p in range(1,number_of_cpus+1,1))
	pool_outputs = []
	for tuple in outputs:
		id_p = tuple[0]
		call_stats[id_p] += 1
		pool_outputs.append(tuple[1])
	return call_stats, '\n'.join(pool_outputs)
def print_call_stats(call_stats):
	for id_p, called_times  in call_stats.items():
		print(f"{id_p}:{called_times}")
if __name__ == '__main__':
	urls = get_all_urls(file=urls_file)
	outputs = process_urls(urls)
	call_stats, pool_outputs = separate_stats_from_output(outputs)
	print(pool_outputs)
	print_call_stats(call_stats)