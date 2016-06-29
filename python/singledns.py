#Just For fun.  by:lvmple
import urllib2
import string
import sys
import socket
import time
import os

source = string.lowercase + string.digits

def dns(url):
    counter = 0
    
    try:
        result = socket.getaddrinfo(url,None)
        for i in result:
            print counter, i[4], url
            counter += 1
            fp1.write(counter + str(i[4]) + url + "\n")
            
            return 1
    except Exception, e:
        e.message

def url_test(url_s):
    url = "http://" + url_s
    
    try:
        response = urllib2.urlopen(url)
        print response.getcode()
        if 200 == response.getcode() or 302 == response.getcode() or 301 == response.getcode():
            print url + " is usable"
            fp2.write(url)
            
            return 0
    except urllib2.HTTPError, e:
        e.message

def url_deal(url_s):
    for i in range(len(source)):
        for j in range(len(source)):
            for k in range(len(source)):
                url_h =source[i : i + 1] + source[j : j + 1] + source[k : k + 1]
                url = url_h + "." + url_s
                flag = dns(url)
                print url_h
                sys.stdout.write("\r")
                if flag == 1:
                    url_test(url)
            print "pause"
            time.sleep(1.5)

if __name__ == '__main__':
    url = sys.argv[1]
    if os.path.isdir(url) == False:
        os.mkdir(url)
    fp1 = open(os.getcwd() + "\\" + url + "\\" + "dns.txt",'w+')
    fp2 = open(os.getcwd() + "\\" + url + "\\" + "url_deal.txt",'w+')
    url_deal(url)
    fp1.close
    fp2.close