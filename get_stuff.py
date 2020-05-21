"""
Some weird behavior of multiprocessing.pool
"""
import requests
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
header = {'User-Agent': user_agent}
timeout=1.0 # what is the time unit here ?


def convert_to_ms(duration):
	elapsed_ms = (duration.days * 86400000) + (duration.seconds * 1000) + (duration.microseconds / 1000)
	return elapsed_ms



import multiprocessing
def get_stuff(url):	
	print(f"current_process = {multiprocessing.current_process()}")
	# for url in urls:
	# csv_rows = []
	# for url in urls:
	csv_terms = []
	csv_terms.append(url)
	r = requests.get(url,headers=header, timeout=timeout)
	response_code = r.status_code
	csv_terms.append(str(response_code))
	document_size = len(str(r.content))
	csv_terms.append(str(document_size))
	response_time = r.elapsed
	ms_elapsed  =convert_to_ms(response_time)
	csv_terms.append(str(ms_elapsed)+'ms')
	csv_row = ';'.join(csv_terms)
	# csv_rows.append(csv_row)
	return csv_row
