import urllib2
import string

source = string.lowercase + string.digits
thelast3 = ""
url_s = "http://syc.myclover.org/pentest/findshell/white_god_s_webshell_"

def white_shell():
    for i in range(len(source)):
        for j in range(len(source)):
            for k in range(len(source)):
                thelast3 = source[i : i + 1] + source[j : j + 1] + source[k : k + 1] + ".php"
                url = url_s + thelast3
                print thelast3
                try:
                    response = urllib2.urlopen(url)
                    print response.getcode()
                    if 200 == response.getcode():
                        print url
                        return 0
                except urllib2.HTTPError, e:
                    print e.message

                    
if __name__ == '__main__':
    white_shell()