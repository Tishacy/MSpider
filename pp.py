# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import numpy as np


class ProxyPool(object):
	"""通过爬取西刺免费代理IP来获取代理ip池
	
	---------------------------------
	kind: (string) 'nt'/'wt'/'nn'/'wn'
			nt: 国内普通代理
			wt: 国内HTTP代理
			nn: 国内高匿代理
			wn: 国内HTTPS代理
	page_num: (int) 页数
	"""
	def __init__(self, kind='nt', page_num=1):
		super(ProxyPool, self).__init__()
		self.kind = kind
		self.page_num = page_num
		self.website = "https://www.xicidaili.com/%s/%d" %(self.kind, self.page_num)
		self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
		self.get_ip_list()

	def get_ip_list(self):
		res = requests.get(self.website, headers=self.headers)
		self.html = res.content.decode()
		# print(html)
		soup = BeautifulSoup(self.html, 'html.parser')
		trs = soup.find_all('tr')[1:]
		self.ip_list = []
		for tr in trs:
			tds = [td.text for td in tr.find_all('td')]
			ip_addr = tds[1]
			port = tds[2]
			ip_type = tds[5]
			self.ip_list.append("%s://%s:%s" %(ip_type, ip_addr, port))

	def random_choose_ip(self):
		"""从代理ip池中随机选择ip
		"""
		ip = np.random.choice(self.ip_list)
		return ip

	def open_url(self, url, timeout=None):
		ip = self.random_choose_ip()
		# print("Using proxies: %s" %(ip))
		self.proxies = {
			ip.split(':')[0]: ip,
		}
		sess = requests.Session()
		return sess.get(url, headers=self.headers, proxies=self.proxies, timeout=timeout)

	def post(self, url, data, timeout=None):
		ip = self.random_choose_ip()
		# print("Using proxies: %s" %(ip))
		self.proxies = {
			ip.split(':')[0]: ip,
		}
		sess = requests.Session()
		return sess.post(url, data=data, headers=self.headers, proxies=self.proxies, timeout=timeout)


	def _get_title(self, url):
		res = self.open_url(url)
		html = res.content.decode()
		soup = BeautifulSoup(html, 'html.parser')
		return soup.title.text, res


if __name__ == "__main__":
	proxy_pool = ProxyPool()
	url = "https://www.baidu.com"
	title, status = proxy_pool._get_title(url)
	print("%s\n%s" %(status, title))
