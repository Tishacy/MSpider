"""
	多线程爬虫与下载器
"""

import os
import requests
import wget
import numpy as np
import pandas as pd
import json
from threading import Thread
from queue import Queue
from bs4 import BeautifulSoup



# CLASS Downloader

class Downloader(object):
	"""多线程下载器
	参数: source_dict
		source_dict = {
			"names":[name1, name2, ..., namen],
		 	"urls":[url1, url2, ..., urln]
	 	}
	"""
	def __init__(self, source_dict, file_extension='normal'):
		self.source_dict = source_dict
		self.file_extension = file_extension
		self.source_dataframe = pd.DataFrame(self.source_dict)
		self.name_list = self.source_dict['names']
		self.url_list = self.source_dict['urls']
		self.file_extension = file_extension
		self.check('initialization')
		
	def check(self, item):
		# 初始化检查
		if item == "initialization":
			if len(self.name_list) == len(self.url_list):
				self.num_files = len(self.url_list)
				print("共获取 %d 个链接" %(self.num_files))
				return True
			else:
				raise ValueError("The name list should have the same length with the url list.")
		# 检查下载文件夹是否存在
		elif item == "out_folder":
			if os.path.isdir(self.out_folder):
				print("%s文件夹已存在，自动下载至该文件夹" % self.out_folder)
				return True
			else:
				os.mkdir(self.out_folder)

	def download(self, out_folder='./', engine='wget'):
		# 初始化参数
		self.out_folder = out_folder
		self.check('out_folder')
		self.engine = engine
		batch_size = int(input("BATCH SIZE: "))
		self.num_thrd = int(np.ceil(self.num_files / batch_size))

		thds = []
		for i in range(self.num_thrd):
			frm = i * batch_size
			# 最后一个线程的batch_size
			if i == self.num_thrd - 1 and self.num_files % batch_size != 0:
				batch_size = self.num_files % batch_size
			thd = Thread(target = self.down_batch,
						 args=(frm, batch_size))
			thd.start()
			thds.append(thd)
			print("已开启第 %d 个线程" %(i+1))
		for thd in thds:
			thd.join()
		print("已完成")
		return True

	def down_batch(self, frm, batch_size):
		url_list = self.url_list[frm: frm + batch_size]
		name_list = self.name_list[frm: frm + batch_size]
		for i, url in enumerate(url_list):			
			if self.file_extension == 'normal':
				filex = url.split('.')[-1]
			else:
				filex = self.file_extension

			out_path = "./%s/%s.%s" %(self.out_folder, name_list[i], filex)

			if os.path.isfile(out_path):
				print("已有该文件，跳过...")
			else:
				try:
					self.down_single_file(url, out_path)
				except:
					print("%s下载失败，链接地址为: %s" %(name_list[i], url_list[i]))
					continue
				
	def down_single_file(self, url, out_path):
		if self.engine == "wget":
			wget.download(url, out=out_path)
		elif self.engine == "wget-cli":
			os.system('wget %s -O %s' %(url, out_path))
		elif self.engine == "you-get":
			os.system('you-get %s -O %s' %(url, out_path))




# A TEST FOR CLASS Downloader

def test_downloader():
	source_dict = {
		"names":['baidu','google'],
		"urls": ["https://www.baidu.com/img/baidu_resultlogo@2.png",'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png']
	}
	downloader = MultiThreadDownloader(source_dict, 'html')
	downloader.download('test', engine="wget")




# CLASS Crawler

class Crawler(object):
	"""多线程爬虫
	"""
	def __init__(self, basic_func, urls, has_result=False):
		super(Crawler, self).__init__()
		self.basic_func = basic_func
		self.has_result = has_result
		self.urls = urls
		self.num_urls = len(self.urls)
		self.check()

	def check(self):
		"""检查参数是否合理
		"""
		pass

	def crawl(self):
		# 初始化参数
		print("共有 %d 个url" %(self.num_urls))
		batch_size = int(input("BATCH SIZE: "))
		self.num_thrd = int(np.ceil(self.num_urls / batch_size))
		if self.has_result == True:
			self.queue = Queue()

		thds = []
		for i in range(self.num_thrd):
			frm = i * batch_size
			# 最后一个线程的batch_size
			if i == self.num_thrd - 1 and self.num_urls % batch_size != 0:
				batch_size = self.num_urls % batch_size
			thd = Thread(target = self.crawl_batch,
						 args=(frm, batch_size))
			thd.start()
			thds.append(thd)
			print("已开启第 %d 个线程" %(i+1))
		for thd in thds:
			thd.join()
		print("\n已完成爬取")

		if self.has_result == True:
			# 提取数据
			result = []
			for thd in thds:
				result += self.queue.get()
			print("已提取数据")
			return result

	def crawl_batch(self, frm, batch_size):
		urls = self.urls[frm: frm + batch_size]
		batch_result = []
		for i, url in enumerate(urls):
			try:
				res = self.basic_func(frm + i, url)
				print("第%d个页面抓取成功" %(frm + i))
			except:
				res = None
				print('第 %d 个url任务失败' %(frm + i))
			batch_result.append(res)

		if self.has_result == True:
			self.queue.put(batch_result)


# A TEST FOR CLASS Crawler

from pp import ProxyPool


def test_crawler():
	test_spider = TestSpider()
	result = test_spider.crawl()
	print(result)


class TestSpider(object):
	def __init__(self):
		self.pool = ProxyPool()
		self.pool.headers = {
			"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
			"Cookie":"nats_at=%7CBkKmEvWI2b%7C1%7C%7C%7C%7C; nats=hope911.2.2.84.0.0.0.0.0; nats_unique=hope911.2.2.84.0.0.0.0.0; nats_sess=e2b90c762f65f237dfdf1e3bef530031; nats_landing=No%2BLanding%2BPage%2BURL; _ym_uid=1534274161862516650; _ym_d=1534274161; feid=570ad9e295469353a21b9676f28ae910; atas_uid=BkKmEvWI2b.1; _ym_isad=2; locale=zh; fesid=5f746caa955e119a1626f36e999abf63; last_visited_set=12679; nats_cookie=http%253A%252F%252Fjavhdasia.com%252Ftour%252F104%253Fnats%253D23178.2.2.84.0.0.0.0.0%2526amp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Bnats_at%255Bsubscription_passthrough1%255D%253DBkKmEvWI2b%2526amp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Bamp%253Ba; form_prices_zh=1; _ym_visorc_47878991=w",
			"X-Requested-With": "XMLHttpRequest"
		}
		self.urls = pd.read_csv("./data/video_links.csv")["0"].values[:1]
		self.crawler = Crawler(self.basic_func, self.urls, has_result=True)

	def basic_func(self, index, url):
		json_data = self.pool.open_url(url).content.decode()
		html = json.loads(json_data)["template"]
		soup = BeautifulSoup(html, 'html.parser')
		imgs_html = soup.find("div", {'class':'photos clearfix'})
		num_imgs = int(imgs_html.text.split('(')[-1].split(')')[0])
		img_url_template = imgs_html.find('a', {"class":"fancybox"}).attrs['href']

		img_urls = []
		for j in range(num_imgs):
			img_urls.append(self._parse_img_url(img_url_template, j+1))

		res = {}
		res['index'] = index
		res['img_urls'] =  img_urls
		return res

	def _parse_img_url(self, template, num):
		head = '/'.join(template.split('/')[:-1])
		last = template.split('/')[-1]
		parsed_last = ''
		for c in last:
			try:
				int(c)
			except:
				parsed_last += c
				continue
		img_url = head + '/%d' %num + parsed_last
		return img_url

	def crawl(self):
		return self.crawler.crawl()



if __name__=="__main__":
	# test_downloader()
	test_crawler()