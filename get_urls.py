with  open("list_of_urls","rb") as urls_file:
		urls = [url.rstrip().decode("utf-8") for url in urls_file]

print(urls)
