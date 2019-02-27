"""
    多线程爬虫 - threading.Thread
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
from threading import Thread
import time
from queue import Queue


# 抓取豆瓣top250的10个网页
def get_title(page_num, queue):
    url = "https://movie.douban.com/top250?start=%d&filter=" %(page_num*25)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    lis = soup.find('ol', {'class':'grid_view'}).find_all('li')
    titles = [li.find('span', {'class':'title'}).text for li in lis]
    queue.put(titles)


# 将上面函数传入，计算10次，返回不使用多线程的运行总时间
def no_thread(func):
    queue = Queue()
    t = time.time()
    for i in range(10):
        func(i, queue)
    duration = time.time() - t
    titles = [queue.get() for _ in range(10)]
    print(titles[0])
    return duration


# 将上面函数传入，计算10次，返回使用多线程的运行总时间
def thread(func):
    queue = Queue()
    t = time.time()
    ths = []
    for i in range(10):
        th = Thread(target = func, args = (i, queue))
        th.start()
        ths.append(th)
    for th in ths:
        th.join()
    duration = time.time() - t
    titles = [queue.get() for _ in range(10)]
    print(titles[0])
    return duration


# 做五次实验，返回每次时间和五次的平均值
def get_duration(func_th, func):
    l = []
    for i in range(1):
        l.append(func_th(func))
    mean_duration = '%.2f' %(np.mean(l))
    all_duration = ['%.2f' %i for i in l]
    return [mean_duration, all_duration]



if __name__=="__main__":
    duration_nth = get_duration(no_thread, get_title)
    duration_th = get_duration(thread, get_title)
    print(duration_nth)
    print(duration_th)


















    
