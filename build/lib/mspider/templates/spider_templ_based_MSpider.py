# -*- coding: utf-8 -*-

from mspider.spider import MSpider

class {0}(MSpider):
    def __init__(self):
        self.name = "{1}"
        self.source = []
        super({0}, self).__init__(self.basic_func, self.source)

    def basic_func(self, index, src_item):
        # parse single source item
        pass

if __name__=="__main__":
    spider = {0}()
    # spider.test()
    spider.crawl()
