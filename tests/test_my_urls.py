from fetch_chrome_history import load_chrome_urls
from process_urls import process_urls
from process_urls import separate_stats_from_output
from process_urls import print_call_stats
import random 
import multiprocessing
import requests
number_of_cpus = multiprocessing.cpu_count()

if __name__ == '__main__':
	# urls = get_all_urls(file=urls_file)
	urls = load_chrome_urls()
	urls = random.sample(urls, 20)
	urls = list(set(urls))
	pool = multiprocessing.Pool(processes=number_of_cpus)
	try:
		pool_outputs = pool.map(get_stuff, urls)	
		print(f"pool_outputs={pool_outputs}")
	except requests.exceptions.ConnectionError as error:
		print(error)
	except requests.ConnectionError as error:
		print(error)
	except KeyboardInterrupt as keyboard_exc:
		print(keyboard_exc)
	except:
		print('Unhandled exception')
	pool.close()

	call_stats, responses = separate_stats_from_output(pool_outputs)
	print(responses)
	print_call_stats(call_stats)