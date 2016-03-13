# coding: UTF-8
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

setVisited = set()
zhuji = 'gs.dlut.edu.cn'

def detect(pre, node):
    # print 'pre:'+pre
    # print 'node:'+node
    if len(node) > 3:
        if node[0:4] == 'http' or node[0:4] == 'https':
            return node
    # if len(node) > 3 and node[0:4] != 'http':   #此处忽略了直接访问主机ip,但基本可以不考虑
    while pre[-1] == '/' or pre[-1] == '.' or pre[-1] == '#':     #结尾是./#删除
        pre = pre[:-1]
    if len(node) > 1 and node[0:2] == '..': #对于路径操作
        node = pre[:pre.rfind('/')]+'/'+node
    elif len(node) > 1 and node[0:2] =='./':
        node = pre[:pre.rfind('/')]+'/'+node
    elif len(node) > 0 and node[0] == '/': #找第三个斜线
        index = 0
        cnt = 0
        while cnt < 3 and index < len(pre):
            if pre[index] == '/':
                cnt = cnt+1
            index = index+1
        if cnt == 3:
            index = index-1
        pre = pre[0:index]
        node = pre+node
    else:
        node = pre+'/'+node                     #此处代码繁琐,但却说明了考虑的逻辑
    return node

def parseLink(node):
    global setVisited
    try:
        ret = requests.get(node)
        print ("I am here: " + node)
        if ret.status_code != 200: #这里不一定只是200,需要了解状态码后确定.以及ip限制的代理问题
            return []
    except Exception as e:
        print ("ip主机不存在:" + node)
        return ['no']
    myset = set()
    soup = BeautifulSoup(ret.text)
    for item in soup.find_all('a'):
        myset.add(item.get('href'))
    return list(myset)

def find(pre='', node=''):
    global zhuji
    # print 'find_node:'+node
    node = detect(pre, node)
    if node.find(zhuji) == -1:
        return
    iend = node.find('?')                     #删除URL?后参数
    if iend == -1:
        iend = len(node)
    # print node
    listURL = parseLink(node)
    if node[0:iend] in setVisited or listURL == ['no']:
        return
    else:
        setVisited.add(node[0:iend])
    for item in listURL:
        find(node[0:iend], str(item))
    return

#for one in parseLink('http://gs.dlut.edu.cn'):
#    print one

# print find('', 'http://gs.dlut.edu.cn')
# the_node = detect("", "http://gs.dlut.edu.cn")
# the_list = parseLink(the_node)
# for one in the_list:
#     print one
find('', 'http://gs.dlut.edu.cn')
print ("T哈同事right")
# alist = [1,2,3,4,5]
# str1 = 'http://gs.dlut.edu.cn'
# str2 = 'http'
print len(setVisited)

# fileHandle = open('test','w')
# fileHandle.write(r.text.decode('utf8', 'ignore'))
# fileHandle.close()
