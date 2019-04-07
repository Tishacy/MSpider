# -*- coding: utf-8 -*-

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
            go_on = input("[INPUT]: Recrawl the failed urls, (y/n): ")
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
