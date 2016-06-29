import httplib
import string

conn = httplib.HTTPConnection("209.116.186.246")
conn.request("GET","/search?q=site:www.test.com+inurl:php")
r = conn.getresponse()
print type(len(r.read())) == type(1)