# MSpider

A Multi-threaded Spider wrapper that could make your spider multi-threaded easily, helping you crawl website faster. :zap:

*Note that this is for python3 only.*

## Install

```bash
pip install mspider
```

## Quick Start

### Automatically create a `MSpider` 

1. `cd` to the folder you’d like to create a `MSpider` in terminal or cmd, then type `genspider <your spider name>`, such as:

   ```bash
   $ genspider test
   ```

   A file `test.py` that contains a `MSpider` is created successfully if seeing the following information.

   ```bash
   create a spider named test.
   ```

2. Open the spider file `test.py`. Find `self.source = []` in line 14, and replacing it by the sources (usually a list of urls) you’d like to handle by the spider, such as:

   ```python
   self.source = ['http://www.github.com',
                  'http://www.baidu.com']
   ```

   Each element of the `self.source` is called `src_item`, and the index of `src_item` is called `index`.

3. Find the function `basic_func`, where you could define your spider function, such as:

   ```python
   def basic_func(self, index, src_item):
       url = src_item
       res = self.pool.open_url(url)
       html = res.content.decode('utf-8')
       # deal with the html
       # save the extracted information
   ```

4. Run the spider to start crawling.

   ```bash
   $ python3 test.py
   ```

   You just input the number of source items handled by each thread (BATCH SIZE) in the terminal or cmd, then return it, and then the MSpider will crawl your sources in a multi-threaded manner.

   ```bash
   [INFO]: MSpider is ready.
   [INFO]: 2 urls in total.
   [INPUT]: BATCH SIZE: 1
   [INFO]: Open threads: 100%|████████████████| 2/2 [00:00<00:00, 356.36it/s]
   [INFO]: Task done.
   [INFO]: The task costs 1.1157 sec.
   [INFO]: 0 urls failed.
   ```

### Mannually create a `MSpider`

1. Standard import the MSpider.

   ```python
   from mspider.spider import MSpider
   ```

2. Define the function of your single threaded spider.

   Note that this function must has two parameters.

   - `index`: the index of source item
   - `src_item`: the source item you are going to deal with in this function, which is usually an url or anything you need to process, such as a tuple like `(name, url)`.

   ```python
   def spi_func(index, src_item):
       name, url = src_item
       res = mspider.pool.open_url(url)
       html = res.content.decode('utf-8')
       # deal with the html
       # save the extracted information
   ```

   > `mspider.pool` is an instance of `mspider.pp.ProxyPool`, see "**Usages of `pp.ProxyPool`**"  in **Usages** part for more information.

3. Now comes the key part. Create an instance of `MSpider` and pass it your spider function and sources you’d crawl.

   ```python
   sources = [('github', 'http://www.github.com'),
              ('baidu', 'http://www.baidu.com')]
   mspider = MSpider(spi_func, sources)
   ```

4. Start to crawl!

   ```python
   mspider.crawl()
   ```

   Then you will see the following information in your terminal or cmd. You just input the BATCH SIZE, and then the MSpider will crawl your sources in a multi-threaded manner.

   ```bash
   [INFO]: MSpider is ready.
   [INFO]: 2 urls in total.
   [INPUT]: BATCH SIZE: 1
   [INFO]: Open threads: 100%|████████████████| 2/2 [00:00<00:00, 356.36it/s]
   [INFO]: Task done.
   [INFO]: The task costs 1.1157 sec.
   [INFO]: 0 urls failed.
   ```

## Usages

The `mspider` package has three main modules, `pp`, `mtd` and `spider`

- `pp`  has a class of `ProxyPool`, which helps you get the proxy IP pool from xici free IPs.
- `mtd` has two classes, `Crawler` and `Downloader`
  - `Crawler` helps you make your spider multi-threaded.
  - `Downloader` helps you download things multi-threadedly as long as you pass your urls in the form of `list(zip(names, urls)) ` in it.
- `spider` has the class of `MSpider`, which uses the `Crawler` in module `mtd`, and has some basic configurations of `Crawler`, so this is a easier way to turn your spider into a multi-threaded spider.

### Usage of `pp.ProxyPool`

```python
from mspider.pp import ProxyPool

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
from mspider.mtd import Downloader

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

