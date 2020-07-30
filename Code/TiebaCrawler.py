# -*- coding: utf-8 -*-
import json
import requests
import PostgreAccess
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser

class TiebaCrawler:   
    def __init__(self, url, commentUrl):
        self._url = url
        self._commentUrl = commentUrl
        self._getSoup() # 获取新的context，包括content和comment
        self._totalContent = 0 # 总共帖子数
        self._totalPage = 0 # 总共页数
        self._getSummaryInfo()
        self._pidList = [] # pid列表，用来关联帖子和评论
        self._access = PostgreAccess.PostgreAccess() #初始化postgre连接
    
    # 获取帖子总数
    def GetTotalNumOfContent(self):        
        return self._totalContent

    # 开始执行备份任务
    def StartBackup(self):        
        for i in range(self._totalPage):            
            self._backupContent()
            self._backupComment()
            self._turnToNextPage()
            self._getSoup()
        self._access.CommitAndDispose()

    # 整点汤
    def _getSoup(self):
        header = {"cookie": "xxxxxxxx", "acceptLanguage":"zh-CN,zh;q=0.9", "acceptEncoding":"gzip, deflate, br", "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "userAgent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36(KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
        context = requests.get(self._url, headers = header, timeout = 30)        
        self._soup = BeautifulSoup(context.text, 'lxml')
        c_context = requests.get(self._commentUrl, headers = header, timeout = 30)
        self._csoup = BeautifulSoup(c_context.text, 'lxml')

    # 翻页
    def _turnToNextPage(self):
        pageNum = int(self._url[-1])
        self._url = self._url[:-1] + str(pageNum + 1)
        self._commentUrl = self._commentUrl[:-1] + str(pageNum + 1)

    # 获取帖子的概要信息
    def _getSummaryInfo(self):        
        # 获取到页码中的信息，第一个是帖子总数，第二个是页数总数
        summaryInfo = self._soup.find_all("span", "red")
        self._totalContent = int(summaryInfo[0].text)
        self._totalPage = int(summaryInfo[1].text)
    
    # 备份帖子内容
    def _backupContent(self):
        contentList = self._soup.find_all("div", "l_post l_post_bright j_l_post clearfix")
        dateList = self._soup.find_all("div", "post-tail-wrap")
        # 本页楼层计数器（为什么要这么做：因为用“美丽汤”去选子节点太痛苦了！）
        floorCounter = 0
        for m in contentList:                
            data = json.loads(m.attrs["data-field"])
            acctName = data["author"]["user_name"]
            content = data["content"]["content"]
            floor = data["content"]["post_no"]             

            # logging.info(content + '\r\n\r\n')

            # 子节点数目有变化，但最后一个总是日期
            contentLen = len(dateList[floorCounter].contents)
            # 加入pid列表，用来匹配comment楼层
            self._pidList.append(data["content"]["post_id"])
            date = parser.parse(dateList[floorCounter].contents[contentLen-1].text)

            # 数据写入数据库                            
            self._access.InsertContent(floor, content, acctName, date)
            # 楼层计数加一
            floorCounter += 1 

    # 备份帖子评论
    def _backupComment(self):
        commentRawData = json.loads(self._csoup.text)['data']['comment_list']
        if len(commentRawData) == 0:
            return
        commentList = commentRawData.items()
        for m in commentList:
            for n in m[1]["comment_info"]:                
                acctName = n["username"]
                comment = n["content"]
                floor = self._pidList.index(int(n["post_id"])) + 1
                date = datetime.fromtimestamp(n["now_time"])
                # 数据写入数据库                
                self._access.InsertComment(floor, comment, acctName, date)