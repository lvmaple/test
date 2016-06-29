import sys,urllib

url = "http://y0pk678.xdctf.com:8081/read?file=newapp.py"
fp = open("getwebpage.txt","w")
i = 0

while 1:
    wp = urllib.urlopen(url)
    content = wp.read()
    print content
    fp.write(str(i) + content )
    i = i + 1
    if i == 100:
        break    

fp.close()