str = "12345"
str1 = ""
for i in range(len(str)):

    str1 = str1 + str[len(str)-i -1:len(str)-i]
print str[::-1]