# -*- coding: utf-8 -*-

"""多线程下载器与多线程爬虫容器
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
from tqdm import tqdm


# CLASS Downloader

class Downloader(object):
	"""多线程下载器

	-----------------
	source_dict: (dictionary) 该参数须有两个键"names"和"urls", 示例如下：
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
		"urls": ['https://www.baidu.com/img/baidu_resultlogo@2.png',
				 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png']
	}
	downloader = MultiThreadDownloader(source_dict, 'html')
	downloader.download('test', engine="wget")




# CLASS Crawler

class Crawler(object):
	"""多线程爬虫包装容器
	通过传入爬虫基本函数(basic_func)，来实现单线程爬虫的多线程化

	-----------------------
	basic_func: (function) 具体的单线程爬虫函数
	urls: (list) 需要单线程爬虫处理的url列表
		 该列表中可以存放需要basic_func处理的任何信息，并非只有url
	has_result: (boolean) 单线程爬虫函数是否需要信息输出
	"""
	def __init__(self, basic_func, urls, has_result=False):
		super(Crawler, self).__init__()
		self.basic_func = basic_func
		self.has_result = has_result
		self.urls = urls
		self.num_urls = len(self.urls)
		self.failed_urls = []
		self.check()

	def check(self):
		"""检查参数是否合理
		"""
		pass

	def crawl(self):
		# 初始化参数
		print("[INFO]: 共有 %d 个url" %(self.num_urls))
		batch_size = int(input("[INPUT]: BATCH SIZE: "))
		self.num_thrd = int(np.ceil(self.num_urls / batch_size))
		if self.has_result == True:
			self.queue = Queue()

		thds = []
		# for i in range(self.num_thrd):
		for i in tqdm(range(self.num_thrd), desc="[INFO]: 开启线程"):
			frm = i * batch_size
			# 最后一个线程的batch_size
			if i == self.num_thrd - 1 and self.num_urls % batch_size != 0:
				batch_size = self.num_urls % batch_size
			thd = Thread(target = self.crawl_batch,
						 args=(frm, batch_size))
			thd.start()
			thds.append(thd)
			# print("[INFO]: 已开启第 %d 个线程" %(i+1))
		for thd in thds:
			thd.join()
		print("[INFO]: 已完成爬取")

		if self.has_result == True:
			# 提取数据
			result = []
			for i in tqdm(range(len(thds)), desc="[INFO]: 重载数据"):
				result += self.queue.get()
			# print("[INFO]: 已提取数据")
			return result

	def crawl_batch(self, frm, batch_size):
		thd_num = frm // batch_size
		urls = self.urls[frm: frm + batch_size]
		batch_result = []
		for i, url in enumerate(urls):
		# for i in tqdm(range(len(urls)), desc="线程%d" %(thd_num + 1)):
			# url = urls[i]
			try:
				res = self.basic_func(frm + i, url)
				print("[INFO]: 第 %d 个线程, 第 %d 个url抓取成功" 
					%(thd_num + 1, i+1))
			except:
				res = None
				self.failed_urls.append(url)
				print('[ERROR]: 第 %d 个线程, 第 %d 个url任务失败,已存入failed_urls'
				 	%(thd_num + 1, i+1))
			batch_result.append(res)

		if self.has_result == True:
			self.queue.put(batch_result)


if __name__=="__main__":
	test_downloader()