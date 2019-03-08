# -*- coding: utf-8 -*-

"""用于生成基于mtd.Crawler的单线程爬虫模板
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

from pp import ProxyPool
from mtd import Crawler


class %s(object):
	def __init__(self):
		self.name = "%s"
		self.pool = ProxyPool()
		# headers
		# self.pool.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
		# urls need crawl
		self.urls = []
		self.crawler = Crawler(self.basic_func, self.urls, has_result=True)
		print("已初始化爬虫")

	def basic_func(self, index, url):
		# parse single url
		pass

	def crawl(self):
		self.crawler.crawl()
		print("共有", len(self.crawler.failed_urls), "个url抓取失败.")
		if len(self.crawler.failed_urls) > 0:
			print("[FAILED]: \n", self.crawler.failed_urls)
			go_on = input("是否继续爬取失败的url, (y/n): ")
			if go_on == 'y':
				self.crawler = Crawler(self.basic_func, self.crawler.failed_urls, has_result=True)
				self.crawl()
			else:
				print('已完成')
				return

	def test(self):
		url = self.urls[0]
		self.basic_func(0, url)


if __name__=="__main__":
	spider = %s()
	# spider.test()
	spider.crawl()
	""" %(class_name, name, class_name)

	with open(spider_path, 'w') as f:
		f.write(spider_template)
		f.close()
	print('create a spider named %s.' %(name))


def format_class_name(spider_name):
	spider_class_name = spider_name.capitalize() + 'Spider'
	return spider_class_name



if __name__=="__main__":
	genspider(name="spider")