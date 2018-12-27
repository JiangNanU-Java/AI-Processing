#!/usr/bin/env python
# coding:utf-8
from urllib import request, parse
import os
import time
import random
from urllib.error import URLError, HTTPError
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
import smtplib
from lxml import etree


class Spider:
    def __init__(self):
        self.old_title_qidian = list()
        self.old_title_zongheng = list()

    def check_update(self):
        # 从文件中读取上次记录的最新章节
        f = open("qidian.txt", 'r')
        self.old_title_qidian = []
        link_qidian = []
        n = 0
        for line in open('qidian.txt'):
            if (n % 2 == 1):
                line = f.readline()
                line = line.strip()
                self.old_title_qidian.append(line)
            else:
                line = f.readline()
                line = line.strip()
                link_qidian.append(line)
            n = n + 1
        f.close()

        f = open("zongheng.txt", 'r')
        self.old_title_zongheng = []
        link_zongheng = []
        n = 0
        for line in open('zongheng.txt'):
            if (n % 2 == 1):
                line = f.readline()
                line = line.strip()
                self.old_title_zongheng.append(line)
            else:
                line = f.readline()
                line = line.strip()
                link_zongheng.append(line)
            n = n + 1
        f.close()

        print(self.old_title_qidian)
        print(link_qidian)
        print(self.old_title_zongheng)

        # 检测更新
        i = 0
        for k in link_qidian:
            self.update_2(i, k)
            i = i + 1
        i = 0
        for k in link_zongheng:
            self.update_3(i, k)
            i = i + 1

        # 将新章节名保存
        f = open("qidian.txt", "w")
        length = len(link_qidian)
        for i in range(length):
            f.write(link_qidian[i] + '\n')
            f.write(self.old_title_qidian[i] + '\n')
        f.close()

        f = open("zongheng.txt", "w")
        length = len(link_zongheng)
        for i in range(length):
            f.write(link_zongheng[i] + '\n')
            f.write(self.old_title_zongheng[i] + '\n')
        f.close()

    # 获取html
    def open_url(self, link):
        wanted_page = link
        req = request.Request(wanted_page)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                     '(KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393')
        response = request.urlopen(req)
        html = response.read().decode('utf-8')
        return html

    # 检查是否更新  针对起点中文网
    def update_2(self, i, link):
        html = self.open_url(link)
        tree = etree.HTML(html)
        node = tree.xpath(u"/html/body/div[2]/div[6]/div[4]/div[1]/div[1]/div[2]/ul/li[3]/div/p[1]/a/@title")
        print(node[0])
        if (node[0] != self.old_title_qidian[i]):
            self.old_title_qidian[i] = node[0]
            new_email = SendEmail(node[0])
            new_email.send(link)
        else:
            print(0)

    # 检查是否更新 针对纵横中文网
    def update_3(self, i, link):
        html = self.open_url(link)
        tree = etree.HTML(html)
        node = tree.xpath(u"/html/body/div[6]/div[1]/div/div[3]/a/text()")
        node[0] = node[0].strip()  # 起点的标题会多读取一个换行符，要去除
        print(node[0])
        if (node[0] != self.old_title_zongheng[i]):
            self.old_title_zongheng[i] = node[0]
            new_email = SendEmail(node[0])
            new_email.send(link)
        else:
            print(0)


class SendEmail:
    def __init__(self, title):
        self.title = title

    def send(self, link):
        # xxxxxxxxx表示邮箱服务授权码
        data_1 = ['18861857305@163.com', 'WUDIwsh123', '18861857305@163.com', 'smtp.163.com']
        from_addr = data_1[0]
        password = data_1[1]
        to_addr = data_1[2]
        smtp_server = data_1[3]

        msg = MIMEMultipart('alternative')
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = r'同志，小说更新了！！！'
        html = """
        <html> 
          <head></head> 
          <body> 
            <p>同志，最新章节在此：<br> 
               点击链接立即阅读<br> 
               <a href= """ + link + """">""" + self.title + """<a><br>
                <hr style="border:1px dashed #000; height:1px">
               <a href ="http://www.bearcarl.top">点击链接加入我们的社区<a><br>
            </p> 
          </body> 
        </html> 
    """
        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        try:
            server = smtplib.SMTP_SSL(smtp_server, 465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, to_addr, msg.as_string())
            print('success')
        except server.SMTPException as e:
            print("failed")
        finally:
            server.quit()


if __name__ == '__main__':
    update_Spider = Spider()
    while (1):
        # 记录当前时间
        f = open("xs_log.txt", "a")
        now_time = time.strftime('%Y-%m-%d  %H : %M : %S', time.localtime(time.time()))
        f.write(now_time + '\n')
        f.close()
        update_Spider.check_update()
        # 每10分钟检查一次是否更新
        time.sleep(600)
