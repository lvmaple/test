import sys
import socket

# test = "baidu.com"
# counter = 0
# try:
#     result = socket.getaddrinfo(test,None)
#     for i in result:
#         print counter, i[4]
#         counter += 1
# except Exception, e:
#     print e.message

test = "66.249.71.15"
counter = 0
try:
    print 1
    result = socket.gethostbyaddr(test)
    print 2
    
    print counter, result[0], result[1], result[2]
    
except Exception, e:
    print "None"