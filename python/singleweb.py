# coding:utf-8
import re
import requests
import time

s=time.time()
# 获取网页内容
r = requests.get('http://www.qq.com')
data = r.text

# 利用正则查找所有连接
link_list =re.findall('(https?://.*?|ftp://.*?)[\'\"]',data)
for url in link_list:
    print url
e=time.time()
print e-s
print len(link_list)

