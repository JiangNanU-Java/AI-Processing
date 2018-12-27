# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.mail import MailSender
import scrapy


class XiaoshuoPipeline(object):
    def process_item(self, item, spider):
        with open('nitianxieshen.txt', 'r') as fp:
            line = fp.readline().split('\t')
            if item['chapter'] != line[0]:
                Subject = u'小说《逆天邪神》更新啦！！！'
                Body = u'更新内容:\n%s\n点击地址:\nhttp://m.zongheng.com/h5/book?bookid=408586' % item['chapter']
                mailer = MailSender(smtphost="smtp.163.com", mailfrom="18861857305@163.com", smtpuser="18861857305@163.com",
                                    smtppass="WUDIwsh123", smtpport=25)
                mailer.send(to=['*******@qq.com'], subject=Subject.encode('utf8'), body=Body.encode('utf8'))
                with open('nitianxieshen.txt', 'w') as fp:
                    fp.write(item['chapter'].encode('utf8') + '\t')
                    fp.write(item['updatetime'].encode('utf8') + '\t\n')
        return item
