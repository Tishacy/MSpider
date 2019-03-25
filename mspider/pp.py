# -*- coding: utf-8 -*-

import requests
import numpy as np
import time
from threading import Thread
from bs4 import BeautifulSoup


class ProxyPool(object):
	"""通过爬取西刺免费代理IP来获取代理ip池
	注意：可用的代理IP较少，慎用
	
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
		self.check_all_ip()
		print("[INFO]: http: %d, https: %d" %(len(self.ip_list['http']), len(self.ip_list['https'])))
		print("[INFO]: ProxyPool is ready.")

	def get_ip_list(self):
		res = requests.get(self.website, headers=self.headers)
		html = res.content.decode()
		soup = BeautifulSoup(html, 'html.parser')
		trs = soup.find_all('tr')[1:]
		self.ip_list = {"http":[], "https":[]}
		for tr in trs:
			tds = [td.text for td in tr.find_all('td')]
			ip_addr = tds[1]
			port = tds[2]
			ip_type = tds[5]
			if ip_type == "HTTP": 
				self.ip_list['http'].append("%s://%s:%s" %(ip_type, ip_addr, port))
			elif ip_type == "HTTPS":
				self.ip_list['https'].append("%s://%s:%s" %(ip_type, ip_addr, port))

	# Check IPs and drop unavailable IPs.
	def check_ip(self, ip):
		protocol = ip.split(':')[0].lower()
		if protocol == "http":
			url = "http://www.163.com"
		elif protocol == "https":
			url = "https://www.zhihu.com"
		proxies = {protocol: ip}
		try:
			requests.get(url, proxies=proxies, timeout=6)
		except:
			if ip in self.ip_list[protocol]:
				self.ip_list[protocol].remove(ip)

	def check_all_ip(self):
		print("[INFO]: Check the availability of proxy IPs...")
		check_list = self.ip_list['http'] + self.ip_list['https']
		check_list *= 3
		t1 = time.time()
		thds = []
		for ip in check_list:
			thd = Thread(target=self.check_ip,
						 args=(ip,))
			thd.start()
			thds.append(thd)

		for thd in thds:
			thd.join()
		print("[INFO]: Checking IPs costs %.4f sec." %(time.time() - t1))

	def random_choose_ip(self, protocol='http'):
		"""从代理ip池中随机选择ip
		"""
		return np.random.choice(self.ip_list[protocol])

	def open_url(self, url, timeout=3):
		protocol = url.split(':')[0]
		# If the ip_list is empty
		if len(self.ip_list[protocol]) == 0:
			return requests.get(url, headers=self.headers, timeout=timeout)

		ip = self.random_choose_ip(protocol)
		self.proxies = {protocol: ip}
		try:
			res = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=timeout)
		except:
			# if the proxy IP is not available, drop the proxies, and remove it from IP list.
			res = requests.get(url, headers=self.headers, timeout=timeout)
			self.ip_list[protocol].remove(ip)
			self.proxies = {}
		return res

	def post(self, url, data, timeout=None):
		protocol = url.split(':')[0]
		# If the ip_list is empty
		if len(self.ip_list[protocol]) == 0:
			return requests.post(url, headers=self.headers, data=data, timeout=timeout)

		ip = self.random_choose_ip(protocol)
		self.proxies = {protocol: ip}
		try:
			res = requests.post(url, headers=self.headers, data=data, proxies=self.proxies, timeout=timeout)
		except:
			# if the proxy IP is not available, drop the proxies, and remove it from IP list.
			res = requests.post(url, headers=self.headers, data=data, timeout=timeout)
			self.ip_list[protocol].remove(ip)
			self.proxies = {}
		return res

	def _get_title(self, url):
		res = self.open_url(url)
		html = res.content.decode()
		soup = BeautifulSoup(html, 'html.parser')
		return soup.title.text, res


if __name__ == "__main__":
	proxy_pool = ProxyPool()
	url = "https://www.github.com"
	title, status = proxy_pool._get_title(url)
	print(proxy_pool.proxies)
	print("%s\n%s" %(status, title))
