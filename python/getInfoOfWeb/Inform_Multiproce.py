__author__ = 'js'
from bs4 import BeautifulSoup
from urlparse import urlparse
import requests,socket,re
from Wappalyzer import Wappalyzer,WebPage
from multiprocessing import Pool,Manager,cpu_count


wappalyzer = Wappalyzer.latest()

def getlist(file):
    """
    Get target list
    :param file:A file contern the target list.
    :return:
    """
    with open(file,"r") as ft:
        tl = ft.readlines()
        tl = [urlparse(url).hostname.strip() for url in tl]
        return tl

def getIP(url):
    """
    Get IP info
    :param tl: the list of target
    :return:
    """

    return socket.gethostbyname(url)


def getWhois(ip):
    """
    Get Whois information
    :param ip: int IP address
    :return:{u'status': u'ASSIGNED NON-PORTABLE', u'fax-no': u'+86 811 2873882', u'descr': u'Chongqing, Sichuan, China', u'phone': u'+86 811 2873972 ext. 22428', u'country': u'CN', u'changed': u'xing@cernet.edu.cn 19950918', u'e-mail': u'helpdesk@apnic.net', u'nic-hdl': u'LZ3-CN', u'source': u'APNIC', u'tech-c': u'SZ2-AP', u'person': u'Lin Zhou', u'role': u'CERNET Helpdesk', u'inetnum': u'202.202.32.0 - 202.202.47.255', u'netname': u'CQUPT-CN', u'remarks': u'Point of Contact for admin-c', u'mnt-by': u'MAINT-NULL', u'admin-c': u'XL1-CN', u'address': u'Chongqing Sichuan PRC', u'notify': u'helpdesk@apnic.net'}
    get inetnum, e-mail, country, person
    """
    s = requests.session()
    url = "http://bgp.he.net/ip/{ip}".format(ip=ip)
    headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate',
               'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
               "Cookie": "__utmt=1; c=BAgiEzExOC4xODQuMjkuMTk2--9be1b2df1e4449dafcf654369087e957928333b0; __utma=83743493.1697038475.1459323317.1465700999.1466651650.7; __utmb=83743493.2.10.1466651650; __utmc=83743493; __utmz=83743493.1459323317.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _bgp_session=BAh7BzoPc2Vzc2lvbl9pZEkiJWIwYmI4OGUxMmYxNGZjN2UyNGEwZWQ5NzQyY2Q5ZTNlBjoGRUY6EF9jc3JmX3Rva2VuSSIxMG9yaDRpdGRxdU1zcWJvN3AxcWlyQWc1TWR5aEZnVUVhQjJYcFQwWEZEZz0GOwZG--2c97d40e1fe296fa8fba62132df434217cbdb392"
               }
    s.headers=headers
    res = s.get(url,headers=headers)
    bs = BeautifulSoup(res.text,"lxml")
    text = bs.find("pre").string
    stext = {}
    for item in text.split('\n'):
        if ":" in item:
            index = item.index(":")
            k,v = item[:index],item[index+1:]
            if k.strip() in stext.keys():
                stext[k] = stext[k]+v
                continue
            stext.update({k.strip():v.strip()})
    return stext

def getCms(url):
    webpage = WebPage.new_from_url(url)
    return "&".join(wappalyzer.analyze(webpage))

class website(object):
    def __init__(self,url):
        self.url = url
        self.ip = None
        self.inetnum = None
        self.desrc = None
        self.cms = None
        self.whois = None
        self.access = True
        self.country = None


    def getInfor(self):
        try:
            self.ip = getIP(self.url)
        except Exception,e:
            self.access = False
            return False

        whois = getWhois(self.ip)
        if "descr" not in whois.keys():
            whois["descr"] = None
        if "inetnum" not in whois.keys():
            if "NetRange" in whois.keys():
                whois["inetnum"] = whois["NetRange"]
            else:
                whois["inetnum"] = None
        self.whois = whois
        self.desrc = whois["descr"]
        self.inetnum = whois["inetnum"]

        if "Country" not in whois.keys():
            if "country" in whois.keys():
                whois["Country"]= whois["country"]
            else:
                whois["Country"] = None
        self.country = whois["Country"]
        try:
            self.cms = getCms("http://"+self.url)
        except Exception,e:
            self.cms = "not found"

def getinfor(web,l):
    try:
        web.getInfor()
    except Exception,e:
        print e
        pass
    #print "process"+web.ip
    l.append(web)
    # print web.ip



def run(file):
    lurl = getlist(file)
    print lurl
    websites = [website(url) for url in lurl]
    mgr = Manager()
    webML = mgr.list()
    cpunum = cpu_count()
    threads = Pool(cpunum)

    for site in websites:
      threads.apply_async(getinfor,args=(site,webML))

    threads.close()
    threads.join()

    #threads.map(website.getInfor,websites)
    #[web.getInfor() for web in websites]
    webs = list(webML)
    for web in webs:
        # if web.access == True:
        print "{url}#{ip}#{cms}#{inetnum}#{derc}#{country}".\
            format(url=web.url,ip=web.ip, cms=web.cms,inetnum=web.inetnum, derc=web.desrc, country=web.country)

if __name__=="__main__":
    run("target")




