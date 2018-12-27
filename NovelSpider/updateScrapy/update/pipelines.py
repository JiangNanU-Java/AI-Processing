# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.mail import MailSender
import scrapy


class NovelPipeline(object):
    """
    数据存储
    """

    # 处理爬取到的item数据
    def process_item(self, item, spider):
        # 读取item存储文件
        with open('nitianxieshen.txt', 'r') as fp:
            line = fp.readline().split('\t')

            # 与上一次保存的章节名进行对比，若不同，则更新
            if item['chapter'] != line[0]:
                print("小说更新了:" + item['chapter'])

                # 邮件信息
                email_subject = u'小说《逆天邪神》更新啦！！！'
                email_body = u'''
                更新内容:
                %s
                点击地址:
                http://m.zongheng.com/h5/book?bookid=408586
                ''' % item['chapter']

                # 通过SMTP发送邮件
                mailer = MailSender(smtphost="smtp.163.com",
                                    mailfrom="18861857305@163.com",
                                    smtpuser="18861857305@163.com",
                                    # 授权码
                                    smtppass="WUDIwsh123",
                                    smtpport=25)
                # 目标邮箱
                mailer.send(to=['18861857305@163.com'],
                            subject=email_subject,
                            body=email_body)

                # 将本次更新内容保存到文件中
                with open('nitianxieshen.txt', 'w') as fp:
                    fp.write(item['chapter'] + '\t')
                    fp.write(item['update_time'] + '\t\n')

        return item
