#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Name:wgdScan
Author:wanggangdan
Copyright (c) 2019
'''
import sys
from Sql.lib.core.Spider import SpiderMain

def main():
    # root = "https://www.shiyanlou.com/"
    root = "http://fhdemo.s-cms.cn/t1/"
    threadNum = 10
    #spider
    wgd = SpiderMain(root,threadNum)
    wgd.craw()

if __name__ == '__main__':
    main()