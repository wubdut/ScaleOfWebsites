# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

setVisited = set()
zhuji = 'gs.dlut.edu.cn'

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
        # print ("I am here: " + node)
    except Exception as e:
        print ("客户端或服务器错误:" + node)
        return ['no']
    myset = set()
    soup = BeautifulSoup(ret.text)
    for item in soup.find_all('a'):
        myset.add(item.get('href'))
    return list(myset)

def find(pre='', node=''):
    global zhuji, setVisited
    node = detect(pre, node)
    if node.find(zhuji) == -1:
        return
    listURL = parseLink(node)
    if node in setVisited or listURL == ['no']:
        return
    else:
        print 'I am here: ' + node
        setVisited.add(node)
    for item in listURL:
        find(node, str(item))
    return
find('http://gs.dlut.edu.cn','')
print ("T哈同事right")
print len(setVisited)
