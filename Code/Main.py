# -*- coding: utf-8 -*-
import schedule
import time
import TiebaCrawler
import logging

# 爬取帖子的url
Url = "https://tieba.baidu.com/p/xxxxxxxxxx?pn=1"
CommentUrl = "https://tieba.baidu.com/p/totalComment?t=xxxxxxxxxxxxx&tid=xxxxxxxxxx&fid=xxxxxxx&pn=1"

# 贴吧留言总数
TotalNumOfComt = 0

# 每日任务。每天检查是否有更新，有就备份
def DailyJob():
    try:
        crawler = TiebaCrawler.TiebaCrawler(Url, CommentUrl)
        currentNum = crawler.GetTotalNumOfContent()
        # 申明使用全局变量。第一次使用python的坑：全局变量第一次赋值的时候会显示没有申明，必须先给他global来一下
        global TotalNumOfComt
        if (TotalNumOfComt != currentNum):
            logging.info('DailyJob running, ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\r\n')
            TotalNumOfComt = currentNum
            # 开始备份数据
            crawler.StartBackup()        
    except Exception as e:
        logging.error('some error happened in DailyJob, ' + str(e) + ', '+ time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\r\n')

# 每周任务。每周强制备份一次数据
def WeeklyJob():
    try:
        logging.info('WeeklyJob running, ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        crawler = TiebaCrawler.TiebaCrawler(Url, CommentUrl)
        # 开始备份数据
        crawler.StartBackup()
    except Exception as e:
        logging.error('some error happened in WeeklyJob, ' + str(e) + ', '+ time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\r\n')

# 配置日志
logging.basicConfig(filename='logs.log',level=logging.INFO)

schedule.every().day.at("06:00").do(DailyJob)
schedule.every().monday.at("06:00").do(WeeklyJob)

# 运行的时候先给他来一次，给他莽在嘴头！
DailyJob()

while True:
    schedule.run_pending()
    time.sleep(1)