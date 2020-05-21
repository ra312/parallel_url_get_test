"""test http request status code and latency
Remark: same http get request returns different status code 
Returns:
	[type] -- [description]
"""

# some urls return 403 while I can access the server by hand,
			# therefore I include user-agent in the header
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"


from multiprocessing import Process
import urllib3
from urllib3.util import Timeout
import urllib3.request
import datetime
import requests

def convert_to_ms(duration):
	elapsed_ms = (duration.days * 86400000) + (duration.seconds * 1000) + (duration.microseconds / 1000)
	return elapsed_ms

import requests

def main():
	url = 'https://example.com/'
	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
	header = {'User-Agent': user_agent}
	with open('list_of_urls','rb') as urls:
		
		for url in urls:
			csv_terms = []
			ready_url = url.rstrip().decode('utf-8')
			csv_terms.append(ready_url)
			# print(ready_url)
			try:
				r = requests.get(ready_url,headers=header)
				response_code = r.status_code
				csv_terms.append(str(response_code))
				document_size = len(str(r.content))
				csv_terms.append(str(document_size))
				response_time = r.elapsed
				ms_elapsed  =convert_to_ms(response_time)
				csv_terms.append(str(ms_elapsed)+'ms')
				csv_row = ';'.join(csv_terms)
				print(csv_row)
			except:
				pass

			
			
if __name__ == '__main__':
	main()