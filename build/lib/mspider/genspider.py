# -*- coding: utf-8 -*-

"""用于生成基于mtd.Crawler的爬虫模板
"""

import sys
import os


def genspider(*args, **kwargs):
	"""生成爬虫模板
	"""
	# 获取爬虫名
	if len(sys.argv) > 1:
		name = sys.argv[-1]
	else:
		name = kwargs['name']
	class_name = format_class_name(name)
	spider_path = './%s.py' %(name)

	# 检查是否已有同名文件
	if os.path.isfile(spider_path):
		raise IOError("File %s.py already exists, please change your spider name." %(name))

	spider_template= """# -*- coding: utf-8 -*-

import requests
from mspider.mtd import Crawler


class {0}(object):
	def __init__(self):
		self.name = "{1}"
		self.sess = requests.Session()
		# headers
		self.headers = {{"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}}
		self.sess.headers.update(self.headers)
		# the source list need to crawl
		self.source = []
		self.crawler = Crawler(self.basic_func, self.source)
		print("[INFO]: MSpider is ready.")

	def basic_func(self, index, src_item):
		# parse single source item
		pass

	def crawl(self):
		self.crawler.crawl()
		print("[INFO]: %d urls failed." %(len(self.crawler.failed_urls), ))
		if len(self.crawler.failed_urls) > 0:
			print("[FAILED]: ", self.crawler.failed_urls)
			go_on = input("[INPUT]: Recrawl the faield urls, (y/n): ")
			if go_on == 'y':
				self.crawler = Crawler(self.basic_func, self.crawler.failed_urls)
				self.crawl()
			else:
				print('[INFO]: Task done.')
				return

	def test(self):
		src_item = self.source[0]
		self.basic_func(0, src_item)


if __name__=="__main__":
	spider = {0}()
	# spider.test()
	spider.crawl()
	""".format(class_name, name)

	with open(spider_path, 'w', encoding='utf-8') as f:
		f.write(spider_template)
	print('create a spider named %s.' %(name))


def format_class_name(spider_name):
	spider_class_name = spider_name.capitalize() + 'Spider'
	return spider_class_name



if __name__=="__main__":
	genspider()