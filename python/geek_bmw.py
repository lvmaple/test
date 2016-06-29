def getkey():
    source = "!0123456789abcdefghijklmnopqrstuvwxyz{}"
    key = "v}f0frqjudwx4dwl3qv2}3xilqgp71"
    lenth = len(key)
    result = ""

    for i in range(lenth):
        j = source.index(key[i:i+1])
        if j == 2:
            j = 2 + len(source)
        if j == 1:
            j = 1 + len(source)
        if j == 0:
            j = lenth

        result = result + source[j - 3:j - 2]
    print result
    
if __name__=='__main__':
    getkey()
