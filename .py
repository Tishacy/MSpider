
from pp import ProxyPool
from mtd import Crawler

class (object):
	def __init__(self):
		self.pool = ProxyPool()
		# headers
		self.pool.headers = { }
		# urls need crawl
		self.urls = []
		self.crawler = Crawler(self.basic_func, self.urls, has_result=True)

	def basic_func(self, index, url):
		# parse single url
		pass

	def crawl(self):
		return self.crawler.crawl()
	