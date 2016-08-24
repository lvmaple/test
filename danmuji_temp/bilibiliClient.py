import asyncio
import aiohttp
import xml.dom.minidom
import random
from struct import *
import json
import config
import re
import requests
import time
import threading


class BilibiliClient:
    def __init__(self):
        self._CIDInfoUrl = 'http://live.bilibili.com/api/player?id=cid:'
        self._roomId = 0
        self._ChatPort = 788
        self._protocolversion = 1
        self._reader = 0
        self._writer = 0
        self.connected = False
        self._UserCount = 0
        self._ChatHost = 'livecmt-1.bilibili.com'
        self._roomId = input('请输入房间号：')
        if config.TURN_ASKFORFANS == 1:
            self._msg = input('请输入圈粉语：')
        self._roomId = int(self._roomId)
        self.countinroom = 0
        self.threadnum = 0
        self.timeinterval = time.time()

    async def connectserver(self):
        print('正在进入房间。。。。。')
        with aiohttp.ClientSession() as s:
            async with s.get('http://live.bilibili.com/' + str(self._roomId)) as r:
                html = await r.text()
                m = re.findall(r'ROOMID\s=\s(\d+)', html)
                ROOMID = m[0]
            self._roomId = int(ROOMID)
            async with s.get(self._CIDInfoUrl + ROOMID) as r:
                xml_string = '<root>' + await r.text() + '</root>'
                dom = xml.dom.minidom.parseString(xml_string)
                root = dom.documentElement
                server = root.getElementsByTagName('server')
                self._ChatHost = server[0].firstChild.data

        reader, writer = await asyncio.open_connection(self._ChatHost, self._ChatPort)
        self._reader = reader
        self._writer = writer
        print('链接弹幕中。。。。。')
        if await self.sendjoinchannel(self._roomId) is True:
            self.connected = True
            print('进入房间成功。。。。。')
            print('链接弹幕成功。。。。。')
            await self.receivemessageloop()

    async def heartbeatloop(self):
        while self.connected is False:
            await asyncio.sleep(0.5)

        while self.connected is True:
            await self.sendsocketdata(0, 16, self._protocolversion, 2, 1, "")
            await asyncio.sleep(30)

    async def sendjoinchannel(self, channelid):
        self._uid = (int)(100000000000000.0 + 200000000000000.0*random.random())
        body = '{"roomid":%s,"uid":%s}' % (channelid, self._uid)
        await self.sendsocketdata(0, 16, self._protocolversion, 7, 1, body)
        return True

    async def sendsocketdata(self, packetlength, magic, ver, action, param, body):
        bytearr = body.encode('utf-8')
        if packetlength == 0:
            packetlength = len(bytearr) + 16
        sendbytes = pack('!IHHII', packetlength, magic, ver, action, param)
        if len(bytearr) != 0:
            sendbytes = sendbytes + bytearr
        self._writer.write(sendbytes)
        await self._writer.drain()

    async def receivemessageloop(self):
        while self.connected is True:
            tmp = await self._reader.read(4)
            expr, = unpack('!I', tmp)
            tmp = await self._reader.read(2)
            tmp = await self._reader.read(2)
            tmp = await self._reader.read(4)
            num, = unpack('!I', tmp)
            tmp = await self._reader.read(4)
            num2 = expr - 16
            if num2 != 0:
                num -= 1
                if num == 0 or num == 1 or num == 2:
                    tmp = await self._reader.read(4)
                    num3, = unpack('!I', tmp)
                    if self.countinroom != num3:
                        if config.TURN_ASKFORFANS == 1 and self.countinroom < num3:
                            self.askforfans()
                        self.countinroom = num3
                        print(time.strftime('%X', time.localtime(time.time())) + ' 房间人数为 %s' % self.countinroom)

                    self._UserCount = num3
                    continue
                elif num == 3 or num == 4:
                    tmp = await self._reader.read(num2)
                    # strbytes, = unpack('!s', tmp)
                    # 为什么还会出现 utf-8 decode error??????
                    try:
                        messages = tmp.decode('utf-8')
                    except:
                        continue
                    self.parsedanmu(messages)
                    continue
                elif num == 5 or num == 6 or num == 7:
                    tmp = await self._reader.read(num2)
                    continue
                else:
                    if num != 16:
                        tmp = await self._reader.read(num2)
                    else:
                        continue

    def senddata(self, msg=""):

        print(msg)
        msg_t = {'msg': msg,
                 'rnd': '1469360047',
                 'roomid': self._roomId
                 }

        url = "http://live.bilibili.com:80/msg/send"
        # contentlength = len(msg_t)
        origin = "http://static.hdslb.com"
        # cookie = "fts=1469300846; LIVE_BUVID=612e08b4543809a7abcbcfe0d30e9e1d; LIVE_BUVID__ckMd5=00f51bed9a09c589; sid=c1mrqchm; DedeUserID=6610732; DedeUserID__ckMd5=af2c2228dabb32f7; SESSDATA=465ff303%2C1474539517%2C2c93eaab; _cnt_dyn=null; _cnt_pm=0; _cnt_notify=0; uTZ=-480; F_S_T_6610732=1; LIVE_LOGIN_DATA=9c08af6ab763495c9c17728f9ef1f321c5e444bc; LIVE_LOGIN_DATA__ckMd5=dc6504674e3c95aa; rlc_time=1471969292046; _dfcaptcha=c3af09c6d1982c81325d34c12e918b2c; CNZZDATA2724999=cnzz_eid%3D199507959-1446876441-http%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1471970344; summerFanNum=20; user_face=http%3A%2F%2Fi1.hdslb.com%2Fbfs%2Fface%2F2d29b2b0ddbf5af270a75454f4d58212dffcb1b8.jpg; attentionData=%7B%22code%22%3A0%2C%22msg%22%3A%22%22%2C%22data%22%3A%7B%22count%22%3A0%2C%22open%22%3A0%2C%22has_new%22%3A0%7D%7D"
        headers = {'Host': 'live.bilibili.com',
                   'Connection': 'keep-alive',
                   'Origin': origin,
                   'X - Requested - With': 'ShockwaveFlash / 22.0.0.192',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': "*/*",
                   'Referer': 'http://static.hdslb.com/live-static/swf/LivePlayerEx_1.swf?2016072301',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Cookie': config.COOKIE
                   }
        res = requests.post(url, data=msg_t, headers=headers)

        print(res.text)

    def thankthegifts(self, giftname, giftnum, giftuser):

        # msg = "感谢" + giftuser + "送出的 " + str(giftnum) + " 个" + giftname
        msg = "感谢" + giftuser + "送出的 " + giftname
        # print(msg)
        self.senddata(msg)
        # threading.Thread(target=self.senddata, args=msg, name="giftthread_" + self.threadnum).start()

    def askforfans(self):
        if self._msg == "":
            msg = "喜欢太白君的小伙伴点一波关注吧(=^▽^=)"
        else:
            msg = self._msg
        self.senddata(msg)

    def wellcomepeople(self, commentuser):
        msg = "欢迎" + commentuser + "来到太白的小窝"
        self.senddata(msg)

    def parsedanmu(self, messages):
        try:
            dic = json.loads(messages)
        # 有些情况会 jsondecode 失败，未细究，可能平台导致
        except Exception as e:
            return
        cmd = dic['cmd']
        if cmd == 'LIVE':
            print ('直播开始。。。')
            return
        if cmd == 'PREPARING':
            print ('房主准备中。。。')
            return
        if cmd == 'DANMU_MSG':
            commenttext = dic['info'][1]
            commentuser = dic['info'][2][1]
            isadmin = dic['info'][2][2] == '1'
            isvip = dic['info'][2][3] == '1'
            if isadmin:
                commentuser = '管理员 ' + commentuser
            if isvip:
                commentuser = 'VIP ' + commentuser
            try:
                print(time.strftime('%X', time.localtime(time.time())) + commentuser + ' say: ' + commenttext)
            except:
                pass
            return
        if cmd == 'SEND_GIFT' and config.TURN_GIFT == 1:
            giftname = dic['data']['giftName']
            giftuser = dic['data']['uname']
            Giftrcost = dic['data']['rcost']
            giftnum = dic['data']['num']
            self.threadnum += 1

            self.thankthegifts(giftname, giftnum, giftuser)
            try:
                print(time.strftime('%X', time.localtime(time.time())) + giftuser + ' 送出了 ' + str(giftnum) + ' 个 ' + giftname)

            except:
                pass
            return
        if cmd == 'WELCOME' and config.TURN_WELCOME == 1:
            commentuser = dic['data']['uname']
            self.wellcomepeople(commentuser)
            try:
                print('欢迎 ' + commentuser + ' 进入房间。。。。')
            except:
                pass
            return
        return

# 129062
# 喜欢太白君的小伙伴点一波关注吧(=^▽^=)
