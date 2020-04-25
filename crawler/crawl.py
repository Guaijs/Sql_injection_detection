# -*- coding:utf-8 -*-
__author__="www.iplaypython.com"
import os
# import urllib2
import urllib.request,urllib.error

import threading
import queue as Queue
import time
import random

q = Queue.Queue() # FIFO 
threading_num = 5

domain_name = ""
Baidu_spider = "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
exclude_list = ['.jpg', '.gif', '.css', '.png', '.js', '.scss']

proxy_list = [
    {'http': '117.28.254.130:8080'},
    {'http': '118.144.177.254:3128'},
    {'http': '113.118.211.152:9797'},
]

with open("wordpress.txt" , "r") as lines:
    for line in lines:
        line = line.rstrip()
        if os.path.splitext(line)[1] not in exclude_list:
            q.put(line)


def crawler():
    while not q.empty():
        path = q.get()

        url = "%s%s" % (domain_name, path)

        random_proxy = random.choice(proxy_list)
        proxy_support = urllib.request.ProxyHandler(random_proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        headers = {}
        headers['User-Agent'] = Baidu_spider
        request = urllib.request.Request(url, headers=headers)

        try:
            response = urllib.request.urlopen(request)
            content = response.read()

            if len(content):
                print ("Status [%s]  - path: %s" % (response.code, path))

            response.close()
            time.sleep(1)
        except urllib.error.HTTPError as e:
            # print e.code, path
            pass

if __name__ == '__main__':
    # 玩蛇网Python之家 www.iplaypython.com
    for i in range(threading_num):
        t = threading.Thread(target=crawler)
        t.start()
