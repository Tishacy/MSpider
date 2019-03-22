# -*- coding: utf-8 -*-
from .pp import ProxyPool
from .mtd import Crawler


class MSpider(object):
	def __init__(self,
				 basic_func,
				 source, 
				 pp_type='wn', 
				 pp_page_num=1, 
				 has_result=False):
		self.source = source
		self.basic_func = basic_func
		self.pool = ProxyPool(pp_type, pp_page_num)
		self.pool.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
		self.crawler = Crawler(self.basic_func, self.source, has_result)
		print("[INFO]: MSpider is ready.")

	def crawl(self):
		self.crawler.crawl()
		print("[INFO]: %d urls failed." %(len(self.crawler.failed_urls), ))
		if len(self.crawler.failed_urls) > 0:
			print("[FAILED]: \n", self.crawler.failed_urls)
			go_on = input("[INPUT]: Recrawl the faield urls, (y/n): ")
			if go_on == 'y':
				self.crawler = Crawler(self.basic_func, self.crawler.failed_urls, has_result=True)
				self.crawl()
			else:
				print('[INFO]: Task done.')
				return

	def test(self):
		src_item = self.source[0]
		self.basic_func(0, src_item)


if __name__=="__main__":
	spider = Spider()
	# spider.test()
	spider.crawl()