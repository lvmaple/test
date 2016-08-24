# -*- coding: utf-8 -*-

###############################################################
import urllib
import datetime
import sys
import http.cookiejar
import json
import requests
import config

today = datetime.datetime.today()
todayStr = datetime.datetime.strftime(today, "%Y-%m-%d")
lastDayDate = today - datetime.timedelta(1)
lastDayDateStr = datetime.datetime.strftime(lastDayDate, "%Y-%m-%d")
picname = "vdcode.png"
vdUrl = "https://passport.bilibili.com/captcha"
goLoginUrl = "https://passport.bilibili.com/login"
loginUrl="https://account.bilibili.com/login/dologin"
# accountUrl="http://account.bilibili.cn/crossDomain?Expires=604800&DedeUserID=7385982&DedeUserID__ckMd5=258b1b7cb17d993c&SESSDATA=c4090d71,1450773446,55659e39&gourl=http://www.bilibili.com/"
# mainUrl = "http://www.bilibili.com/"
memberUrl = "http://member.bilibili.com"
#################################################################

def getVdCode():
    # '''获取验证码图片'''
    resp = urllib.request.urlopen(vdUrl)
    f = open(picname, 'wb')
    f.write(resp.read())
    f.close()
    print('VdCodePic Saved!')

def dealCookie():
    # '''处理cookie'''
    config.COOKIE = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(config.COOKIE))
    urllib.request.install_opener(opener)

def toLogin():
    # '''进入登录页面'''
    resp = urllib.request.urlopen(goLoginUrl)
    html = resp.read().decode('utf-8').encode('gbk')

    getVdCode()

def login():
    # '''开始登录'''
    config.COOKIE = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(config.COOKIE))
    username = input("please input your username: ")
    password = input("please input your password: ")
    while True:
        getVdCode()
        vdcode = input("please input your vdcode: ")
        # 登录
        post_dict = {
            'userid': username,
            'pwd': password,
            'vdcode': vdcode
        }
        post_data = urllib.parse.urlencode(post_dict).encode("utf-8")
        req = urllib.request.Request(loginUrl, post_data)
        res = opener.open(req)

        # res = requests.post(loginUrl, post_dict)
        print(res.read().decode("utf-8"))
        # break
        if "验证码错误，请重新输入" in res.read().decode("utf-8"):
            continue
        else:
            break


    # post_data = urllib.parse.urlencode(post_dict)
    #
    # req = urllib.request.Request(loginUrl, post_data)


    # urllib.request.urlopen(req)
    # urllib.request.urlopen(memberUrl)
    # resp = urllib.request.urlopen("http://member.bilibili.com/index.do?act=dynamic&page=1")
    #
    # #开始解析Python数据
    # resp = resp.read().decode('utf-8').encode('gbk')
    # data = json.loads(resp)
    # print( '------------------------------------------------')
    # for i in range(10):
    #     print( data[str(i)]['time_at'])
    #     print( data[str(i)]['uname']+': '+data[str(i)]['title'])
    #     #因为播放数是数字,所以要转成字符串
    #     print( '播放数: '.decode('utf-8')+str(data[str(i)]['play']))
#         print( '------------------------------------------------')
#


def dologin():
    print( "===%s start===%s"%(sys.argv[0], datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")))
    # dealCookie()
    toLogin()
    # getVdCode()
    login()
    print( "===%s end===%s"%(sys.argv[0], datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")))
#
# #################################################################################
# if __name__ == "__main__":
#     main()