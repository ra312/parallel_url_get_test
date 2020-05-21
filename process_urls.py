from multiprocessing import Process

with open('list_of_urls','rb') as urls:
	for url in urls:
		print(url)

