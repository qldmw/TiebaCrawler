# TiebaCrawler
*贴吧爬虫。针对贴吧单独一个帖子的爬虫，定期爬取内容储存到postgre数据库*  

## 创建表
建表语句：SqlScript文件夹下的createTable.sql

## 配置项
### 需要配置的内容
1.帖子的url    
![urlSample](/Image/urlSample.png)  
*就是浏览器输入框中帖子的地址* 
   
2.帖子评论的url  
![commentUrlSample](/Image/commentUrlSample.png)  
*F12,找到请求中名为    `https://tieba.baidu.com/p/totalComment?xxx`的请求*

3.贴吧登录之后的cookie（也可以不配置，但是部分内容较长的帖子会不显示出来，贴吧一个很奇怪的设定。我匿名爬取的时候，字数在2000字符以上的帖子不会显示出来） 
![cookieSample](/Image/cookieSample.png)  
*贴吧账号登录情况下。F12，找到请求的RequestHeader中的Cookie项*  

4.postgre的连接字符串

### 配置位置
第1,2项的配置位置在Main.py中
```python
# 爬取帖子的url
Url = "https://tieba.baidu.com/p/xxxxxxxxxx?pn=1"
CommentUrl = "https://tieba.baidu.com/p/totalComment?t=xxxxxxxxxxxxx&tid=xxxxxxxxxx&fid=xxxxxxx&pn=1"
```
第3项的配置位置在TiebaCrawler.py的_getSoup方法的header变量中
```python
# 整点汤
def _getSoup(self):
    header = {"cookie": "xxxxxxxx", "xxx": "xxxxx"}
```
*如果匿名爬取，就把header中的cookie属性给删掉*  
第4项的配置位置在PostgreAccess.py中
```python
# postgre数据库连接属性
PostgreDic = {"database":"xxxxxxx", "user":"xxxxxxx", "password":"xxxxxxx.", "host":"localhost", "port":5432}
```

## 执行
`python Main.py`