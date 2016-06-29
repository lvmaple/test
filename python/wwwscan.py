#! /usr/bin/env python
import urllib2
import string
import sys

counter = 0
fp1 = open("cgi.list", "r")
fp2 = open(sys.argv[1] + ".txt", "w+")

def scan(url_s):
    url = "http://" + url_s
    try:
        response = urllib2.open(url)
        if 404 != response.getcode():
            counter += 1
            print response.getcode() + "    " + url
            fp2.write(counter + str(response.getcode()) + "    " + url)
    except Exception, e:
        e.massage

def main(url_h):
    while 1:
        cgi = fp1.readline()
        if not cgi:
            break
        url = url_h + cgi
        print cgi
        sys.stdout.write("\r")
        scan(url)
    
if __name__ == '__main__':
    main(sys.argv[1])
