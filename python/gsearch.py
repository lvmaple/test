import string
import httplib
import random
import time

fp1 = open("c_zizhan.txt","r")
fp2 = open("c_zizhan_deal.txt","w")
fp3 = open("c_zizhan_pasue.txt","w")

def google(url):
    
    conn = httplib.HTTPConnection("209.116.186.246")
    conn.request("GET",url)
    results = conn.getresponse()
    temp = len(results.read())
    flag = 0
    if temp > 55000 :
       flag = 1
    if temp < 400:
       flag = 3
    # print temp  #测试输出页面长度

    return flag

def url_deal(url):
    start = 0
    start = url.find(":",start)
    url = url[0:start]
    return url

inurl = ""
j = 0
k = 0

while 1 :
    k = k + 1
    url = fp1.readline()
    if not url:
       break
    url = url_deal(url)
    print k
    print url  #输出该次搜索的地址
    for i in range(1,4):
       if i == 1:
         inurl = "php"
         url_google = "/search?q=site:" + url + "+inurl:" + inurl
       if i == 2:
         inurl = "asp"
         url_google = "/search?q=site:" + url + "+inurl:" + inurl
       if i == 3:
         inurl = "jsp"
         url_google = "/search?q=site:" + url + "+inurl:" + inurl
        # print url_google  #测试构造的查询语句

        flag1 = google(url_google)

        if flag1 == 1:
            j = j + 1
            fp2.write(str(j) + "    :   " + url + "    :    " + inurl + "\n")

        if flag1 = 3:
            fp3.write(url + "    :    " + inurl + "\n")
            print "pause"
            time.sleep(3600)

    fp1.close
    fp2.close
    fp3.close