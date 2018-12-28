# AI Toys 基于人工智能算法的相关程序集合

## Baidu

爬取百度搜索结果

-------------------------------------------------

## Gobang

基于α-β剪枝博弈树的五子棋AI

-------------------------------------------------

## NovelSpider

小说更新追踪

### [基于scrapy框架发送小说更新通知到邮箱]()

> 目录 NovelSpider/updateScrapy/update

基于scrapy框架爬取纵横中文网小说更新信息，与上一此爬取内容对比，若发生改变，则发送小说更新通知到用户邮箱

**scrapy资料：**

https://scrapy-chs.readthedocs.io/zh_CN/latest/intro/tutorial.html

**运行：** 
    
    cd NovelSpider/updateScrapy/update
    python -m scrapy crawl novel_spider

**定时调度：**

1. 在目录：../update/ 下， 创建脚本crontab.sh，内容：
    
    cd (服务器绝对路径)/update/
    
    scrapy crawl novel_spider
 
2. 脚本添加文件执行权限 执行命令：

    chmod 774 crontab.sh
 
3. crontab 添加定时任务 执行命令：

    crontab -e
 
    写入：

    30 */6 * * * (服务器绝对路径)/update/crontab.sh

    从6：30开始，每隔6个小时执行一次crontab.sh。

4. 取消脚本执行后发送电脑邮件 

    此邮件非爬虫里的邮件，是cron定时任务发送电脑用户（即yunge）的邮件，执行后会在命令端不断提醒。 重新修改：

    crontab -e
 
    内容：

    30 */6 * * * (服务器绝对路径)/update/crontab.sh &> /dev/null
 
-------------------------------------------------

## TensorFlow

TensorFlow库相关程序

-------------------------------------------------

## Zhiwang

中国知网爬虫
