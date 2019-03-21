# MTSpider

A Multi-threaded Spider wrapper that could make your spider multi-threaded easily, helping you crawl website faster. :zap:

*Note that this is for python3 only.*

## Install

Install it using `pip` is on the way.

## Quick Start

```python
from spider import MSpider

# 1. Define the function of your single threaded spider.
# Note that this function must has two parameters.
# The first param represents the index of source item,
# and the second is the source item you'd handle in the function.
def spi_func(index, src_item):
    url = src_item
    res = mspider.pool.open_url(url)
    html = res.content.decode('utf-8')
    # deal with the html

# 2. Create a multi-threaded spider and pass it your spider function and sources you'd crawl.
source = ['http://github.com', 'http://baidu.com']
mspider = MSpider(spi_func, source)

# 3. Start to Crawl!
mspider.crawl()
"""
[INFO]: MSpider is ready.
[INFO]: 2 urls in total.
[INPUT]: BATCH SIZE: 1
[INFO]: Open threads: 100%|████████████████| 2/2 [00:00<00:00, 356.36it/s]
[INFO]: Task done.
[INFO]: The task costs 1.1157 sec.
[INFO]: 0 urls failed.
"""
```

## Usages

This package has three main module `pp` `mtd` and `spider`

- `pp`  has the class of `ProxyPool`, which helps you get the proxy IP pool from xici free IPs.
- `mtd` has two classes, `Crawler` and `Downloader`
  - `Crawler` helps you make your spider multi-threaded.
  - `Downloader` helps you download things multi-threadedly as long as you pass your urls in the form of `list(zip(names, urls)) ` in it.
- `spider` has the class of `MSpider`, which uses the `Crawler` in module `mtd`, and has some basic configurations of `Crawler`, so this is a easier way to turn your spider into a multi-threaded spider.

### Usage of `pp.ProxyPool`

```python
from pp import ProxyPool

pool = ProxyPool()

# Once an instance of ProxyPool is initialized,
# it will has an attribute named ip_list, which
# has a list of IPs crawled from xici free IPs.
print(pool.ip_list)
"""
['HTTP://58.249.55.222:9797', 'HTTPS://113.54.152.170:8080', 'HTTP://180.140.191.233:36820', 'HTTP://163.125.69.145:8888', 'HTTP://14.115.107.83:808', 'HTTP://182.111.129.37:53281', 'HTTPS://202.112.237.102:3128', 'HTTPS://163.125.252.109:9797', ... , 'HTTPS://120.24.43.177:8080', 'HTTP://113.116.144.124:9000', 'HTTP://114.249.118.17:9000']
"""
# Randomly choose an IP
ip = pool.random_choose_ip()
print(ip)
"""
'HTTP://182.111.129.37:53281'
"""

# Update the IP list
pool.get_ip_list()

# Request an url using proxy by 'GET'
url = "http://www.google.com"
res = pool.open_url(url)
print(res.status_code)
"""
200
"""

# Request an url using post by 'POST'
url = "http://www.google.com"
data = {'key':'value'}
res = pool.post(url, data)
print(res.status_code)
"""
200
"""
```

### Usage of `mtd.Downloader`

```python
from mtd import Downloader

# Prepare source data that need download
names = ['a', 'b', 'c']
urls = ['https://www.baidu.com/img/baidu_resultlogo@2.png',
        'https://www.baidu.com/img/baidu_resultlogo@2.png',
        'https://www.baidu.com/img/baidu_resultlogo@2.png']
source = list(zip(names, urls))

# Download them!
dl = Downloader(source)
dl.download(out_folder='test', engine='wget')
"""
[INFO]: 3 urls in total.
[INPUT]: BATCH SIZE: 1
[INFO]: Open threads: 100%|███████████████| 3/3 [00:00<00:00, 3167.90it/s]
[INFO]: Task done.
[INFO]: The task costs 0.3324 sec.
[INFO]: 0 urls failed.
"""
```

### Usage of `spider.MSpider`

See this in  **Quick Start**.

## License

Copyright (c) 2019 tishacy.

Licensed under the [MIT License](https://github.com/Tishacy/LabTest/blob/master/LICENSE).