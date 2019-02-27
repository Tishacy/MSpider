"""
	用于生成爬虫模板
"""
import sys

def genspider(*args, **kwargs):
	"""生成爬虫模板
	"""
	if len(sys.argv) > 1:
		name = sys.argv[-1]
	else:
		name = kwargs['name']
	spider_template= """from pp import ProxyPool
from mtd import Crawler

class %s(object):
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
	""" %(name)

	with open('./%s.py' %(name), 'w') as f:
		f.write(spider_template)
		f.close()
	print('create a spider named %s.' %(name))


if __name__=="__main__":
	genspider(name="spider")