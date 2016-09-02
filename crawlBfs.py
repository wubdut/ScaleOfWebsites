# coding: UTF-8
import requests
import time
import Queue
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

setVisited = set()
crawlQueue = Queue.Queue()
zhuji = 'bingle.win'
time1=time.time()

def detect(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

def parseLink(node):
    global setVisited
    try:
        ret = requests.get(node)
        if ret.status_code >= 400: #这里不一定只是200,需要了解状态码后确定.以及ip限制的代理问题
            return []
    except Exception as e:
        print ("客户端或服务器错误:" + node)
        return ['no']
    myset = set()
    soup = BeautifulSoup(ret.text)
    for item in soup.find_all('a'):
        myset.add(item.get('href'))
    return list(myset)

def find(netSite=''):
    global zhuji, setVisited, crawlQueue
    crawlQueue.put(netSite)
    while not crawlQueue.empty():
        listURL = []
        node = crawlQueue.get()
        if node.find(zhuji) == -1:
            continue
        if node in setVisited:
            continue
        else:
            listURL = parseLink(node)
            if listURL == 'no':
                continue
            setVisited.add(node)
        # print ("I am here: " + node)
        for item in listURL:
            crawlQueue.put(detect(node, item))
    return

find('http://www.bingle.win:12306')
time2=time.time()
print ("Time: " + str(time2-time1) + ' s')
print ("Number of pages: " + str(len(setVisited)))
