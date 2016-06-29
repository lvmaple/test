#!/usr/bin/python
# vim: set fileencoding=utf-8:
import sys
import urllib2
import re

import ConfigParser
import MySQLdb as mdb

class Db_Connector:
    def __init__(self, config_file_path):
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        db_host = cf.get("mysql_db", "host")
        db_port = cf.getint("mysql_db", "port")
        db_user = cf.get("mysql_db", "username")
        db_pwd = cf.get("mysql_db", "password")
        db_data=cf.get("mysql_db","db_name")
        try:
            self.con=mdb.connect(db_host,db_user,db_pwd,db_data)
            self.cur=self.con.cursor()
        except:
            print "[*] DB Connect Error"
    def find_all(self,sql_script):
        try:
            self.cur.execute(sql_script)
            return self.cur.fetchall()
        except:
            print "[*] DB FindAll Error"
    def find_item(self,sql_script):
        try:
            self.cur.execute(sql_script)
            return self.cur.fetchone()
        except:
            print "[*] DB FindItem Error"
    def insert_item(self,sql_script):
        try:
            self.cur.execute(sql_script)
            self.con.commit()
            return True
        except Exception, e:
            print '[*] DB Insert Into Error'
    def update_item(self,sql_script):
        try:
            self.cur.execute(sql_script)
            self.con.commit()
            return True
        except Exception, e:
            print "[*] DB Update Error"

class SpriderUrl:
    # ��ʼ��
    def __init__(self,url):
        self.url=url
        self.con=Db_Connector('sprider.ini')

#���Ŀ��url�ĵ�һ��url�嵥
    def get_self(self):
        urls=[]
        try:
            body_text=urllib2.urlopen(self.url).read()
        except:
            print "[*] Web Get Error:checking the Url"
            sys.exit(0)
        soup=BeautifulSoup(body_text)
        links=soup.findAll('a')
        for link in links:
            # �����Ŀ���url������Ҫ����
            _url=link.get('href')
             # ���Ŷ�������жϴ���
             # ���ж����Ƿ����������ַ���ͷ�Լ��Ƿ�ΪNoneֵ
             # �ж�URL��׺,�����б�Ĳ�ץȡ
            if re.match('^(javascript|:;|#)',_url) or _url is None or re.match('.(jpg|png|bmp|mp3|wma|wmv|gz|zip|rar|iso|pdf|txt|db)$',_url):
                continue
            # Ȼ���ж����ǲ���http|https��ͷ,������Щ��ͷ�Ķ�Ҫ�ж��Ƿ��Ǳ�վ�㣬 ��������վ�������
            if re.match('^(http|https)',_url):
                if not re.match('^'+self.url,_url):
                    continue
                else:
                    urls.append(_url)
            else:
                urls.append(self.url+_url)
        rst=list(set(urls))
        for rurl in rst:
            if self.con.find_item("select * from url_sprider where url='"+rurl+"' and domain='"+self.url+"'"):
                continue
            else:
                try:
                    self.con.insert_item("insert into url_sprider(url,tag,domain)values('"+rurl+"',0,'"+self.url+"')")
                except:
                    print "[*] insert into is Error!"


    def sprider_self_all(self,domain):
        urls=[]
        try:
            body_text=urllib2.urlopen(domain).read()
        except:
            print "[*] Web Get Error:checking the Url"
            sys.exit(0)
        soup=BeautifulSoup(body_text)
        links=soup.findAll('a')
        for link in links:
            # �����Ŀ���url������Ҫ����
            _url=link.get('href')
             # ���Ŷ�������жϴ���
             # ���ж����Ƿ����������ַ���ͷ�Լ��Ƿ�ΪNoneֵ
             # �ж�URL��׺,�����б�Ĳ�ץȡ
            try:
                if re.match('^(javascript|:;|#)',str(_url)) or str(_url) is None or re.match('.(jpg|png|bmp|mp3|wma|wmv|gz|zip|rar|iso|pdf|txt|db)$',str(_url)):
                    continue
            except TypeError:
                print "[*] Type is Error! :"+str(_url)
                continue
            # Ȼ���ж����ǲ���http|https��ͷ,������Щ��ͷ�Ķ�Ҫ�ж��Ƿ��Ǳ�վ�㣬 ��������վ�������
            if re.match('^(http|https)',_url):
                if not re.match('^'+self.url,_url):
                    continue
                else:
                    urls.append(_url)
            else:
                urls.append(self.url+_url)
        res=list(set(urls))
        for rurl in res:
            if self.con.find_item("select * from url_sprider where url='"+rurl+"' and domain='"+self.url+"'"):
                continue
            else:
                try:
                    self.con.insert_item("insert into url_sprider(url,tag,domain)values('"+rurl+"',0,'"+self.url+"')")
                except:
                    print "[*] insert into is Error!"

    def sprider_self(self):        
        while  True:
            wat_list=self.con.find_all("select url from url_sprider where domain='"+self.url+"' and tag=0")
            if len(wat_list)>0:
                for url in wat_list:
                    try:
                        self.con.update_item("update url_sprider set tag=1 where url='"+url[0]+"'")
                    except:
                        print "[*] DB update Error!"
                        continue
                    try:
                        self.sprider_self_all(url[0])
                    except:
                        print "[*]Sprider Error!"
                        continue
            else:
                print "[*] Sprider is Finish!"
                break

spi="http://www.baidu.com/"
t=SpriderUrl(spi)
# ��һ�β���
t.get_self()
# ��ʼ�������
t.sprider_self()