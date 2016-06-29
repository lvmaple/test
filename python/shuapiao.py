import urllib
import httplib 
test_data = {
    'Content-Length':'2',
    'Pragma':'no-cache',
    'Cache-Control': 'no-cache',
    'X-Forwarded-For':'111.193.54.193',
    'Accept': '*/*',
    'Origin': 'http://118.123.249.64:8082',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Referer': 'http://118.123.249.64:8082/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}
test_data_urlencode = urllib.urlencode(test_data)

requrl = "http://118.123.249.64:8082/Home/Praise/23"
headerdata = {"Host":"118.123.249.64:8082"}

conn = httplib.HTTPConnection("118.123.249.64")

conn.request(method="POST",url=requrl,body=test_data_urlencode,headers = headerdata) 

response = conn.getresponse()

res= response.read()

print res