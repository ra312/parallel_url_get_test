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
import random
import requests
# all subexceptions inherit from the base class below

from fetch_chrome_history import load_chrome_urls
import multiprocessing
number_of_cpus = multiprocessing.cpu_count()
print(f"number_of_cpus={number_of_cpus}")

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
header = {'User-Agent': user_agent}
timeout=10.0 # what is the time unit here ?

urls_file = "list_of_urls"

from get_stuff import get_stuff

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
	except requests.ConnectionError as error:
		print(error)
	except KeyboardInterrupt as keyboard_exc:
		print(keyboard_exc)
	except:
		print('Unhandled exception')
	pool.close()
	return pool_outputs

def separate_stats_from_output(outputs):
	call_stats = dict((id_p,0) for id_p in range(1,number_of_cpus+1,1))
	call_stats = dict()
	responses = []
	try:
		for line in outputs:
			id_p = line[0]
			http_string = line[1]
			normal_response = http_string.startswith('http')
			if	normal_response:
				print(f"id_p={id_p}")
				if id_p in call_stats.keys():
					call_stats[id_p] += 1
				else:
					call_stats[id_p]=1
				responses.append(http_string)
	except Exception as e:
		print("67 "+ str(e))
	return call_stats, '\n'.join(responses)

def print_call_stats(call_stats):
	for id_p, called_times  in call_stats.items():
		print(f"{id_p}:{called_times}")

if __name__ == '__main__':
	urls = get_all_urls(file=urls_file)
	# urls = load_chrome_urls()
	for _ in range(100):
		urls_sample = random.sample(urls, 10)
		urls_sample = list(set(urls_sample))
		urls_sample = [url for url in urls_sample if url.startswith('http')]
		print('\n'.join(urls_sample))
		pool = multiprocessing.Pool(processes=number_of_cpus)
		try:
			pool_outputs = pool.map(get_stuff, urls_sample)	
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

	call_stats, responses = separate_stats_from_output(pool_outputs)
	print(responses)
	print_call_stats(call_stats)