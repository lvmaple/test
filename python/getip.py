import socket
import urllib2
#def getWhois(ip):
    # hearders_data = {
    #     'Pragma':'no-cache',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    #     'Referer': 'http://who.is/',
    #     'Accept-Encoding': 'gzip, deflate, sdch',
    #     'Accept-Language': 'zh-CN,zh;q=0.8'
    #     'Connection':'keep-alive'
    # }
    # req = urllib2.Request(url,headers=headers_data)
    # res = urllib2.urlopen(req)

fp=open("C:\Users\Lvmaple9527\Desktop\sa.txt")
for url in fp.readlines():
    temp = url.split("//")
    temp[1] = temp[1].strip()
    url = temp[1][:-1]
    url = url.strip()
    # print url
    try:
        ip = socket.gethostbyname(url)
        # print url+"--"+ip
        print ip
    except Exception, e:
        print url+"--error"
        print "error"
        pass
fp.close()