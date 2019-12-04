# Python-crawler
python爬虫日常练习

ITjuzi：
采用python3.6 + scrapy 爬取IT橘子网站，突破需要登录的爬虫限制(post请求)。


celery_spider_test: 
celery实现异步任务，tasks里面可修改爬虫任务
具体请参考：https://www.jianshu.com/p/73d109a00e52


头条爬虫实现了数据循环抓取还包括一下几个功能：
（1）图片下载
（2）数据存储到mongodb数据库
（3）随机切换User-Agent
（4）对接IP代理池
（5）爬虫完成后实现邮件发送（请配置自己的授权码以及收发着邮箱地址）
