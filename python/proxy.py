#!/bin/python
#-*-coding:utf-8-*-

from lxml import html
import requests,time,random
from multiprocessing.dummy import Pool,Queue
from Proxy import  conn,Proxy


PROXY_NUM = '-1'
PROXYDB = "proxy.db"


def proxy_url_list( mon=time.localtime(time.time()).tm_mon):
    """
    获取当月proxy archive
    :param mon: 月份
    :return: url list
    """
    url = "http://socksproxylist24.blogspot.hk/2016_0{mon}_01_archive.html".format(mon = mon)
    pro_url = html.parse(url)
    pro_url = pro_url.xpath("//h3[@class='post-title entry-title']")
    pro_url = [e.find("a").get("href") for e in pro_url]
    return pro_url


def proxy_list(q,url):
    """
    获取Porxy
    :param q: (Queue)缓存列表
    :param url: (str)proxy url
    :return:
    """
    print url
    urls = html.parse(url).xpath("//textarea")[0].text
    q.put(urls)


def proxy_list_day(q,url):
    """
    获取当天proxy
    :param q: (Queue)缓存列表
    :param url: (str)proxy url
    :return:
    """
    day = time.strftime("%d-%m-%y", time.localtime(time.time()))
    if day in url:
        print "in"
        proxy_list(q,url)


def proxy_thr(fun):
    """
    多线程获取代理地址
    :param fun: 处理url函数，用于获取页面内的proxy
    :return:
    """
    q = Queue()
    pool = Pool(40)

    proxys = []
    i = 1
    for u in proxy_url_list():
        pool.apply_async(fun,(q,u))
    pool.close()
    pool.join()

    while 1:
        if q.empty():
            break
        s = q.get().split("\n")
        proxys += s

    proxys = set(proxys)
    return list(proxys)


def add_proxys(list):
    """
    添加proxy 到sqlite数据库
    :param list: 代理列表
    :return:
    """
    session = conn(PROXYDB)
    for p in  list:
        type = "socks5"
        try:
            proxy = Proxy(type=type,ip_port=p,failnum=0)
            session.add(proxy)
            session.commit()
        except Exception,e:
            print e
            pass


def updatedb():
    l = proxy_thr(proxy_list)
    add_proxys(l)

def updatedaydb():
    l = proxy_thr(proxy_list_day)
    add_proxys(l)

def flushNum():

    session = conn(PROXYDB)
    global  PROXY_NUM
    if PROXY_NUM == '-1':
        proxy_num = session.query(Proxy).count()
        PROXY_NUM = proxy_num
    return PROXY_NUM


def autoproxy():

    session = conn(PROXYDB)
    print session.query(Proxy).count()




if __name__ == "__main__":
    pass
