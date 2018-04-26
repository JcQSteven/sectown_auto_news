#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/21 4:49 PM
# @Author  : Steven
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : main.py.py
# @Software: PyCharm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import sqlite3

class Sqlite_db():
    def __init__(self):
        self.conn=sqlite3.connect('../secrss.sqlite')
        self.cur=self.conn.cursor()
        #mysql列名
        #self.mysql_bar='url,title,time_line,tag,author,head,body'
        self.mysql_col_num=8
        mysql_col = []
        for i in range(0,self.mysql_col_num):
            mysql_col.append('?')
        self.mysql_col=','.join(mysql_col)


    def add(self,table,*data):
        sql = 'insert into %s values(NUll,%s)' % (table,self.mysql_col)
        #print sql
        self.cur.execute(sql, data)
        self.conn.commit()

    def test(self,*data):
        pass
        #print self.conn.


    def get_all(self,table):
        sql='select * from %s'%table
        self.cur.execute(sql)
        value=self.cur.fetchall()
        print value

    def get_last_one(self,table,col_name):
        sql='select %s from %s order by ID DESC limit 1'%(col_name,table)
        self.cur.execute(sql)
        result=self.cur.fetchone()
        return result[0]

    def get_date(self,table,timeline):
        sql='select * from %s where time_line="%s"'%(table,timeline)
        self.cur.execute(sql)
        result=self.cur.fetchall()
        return result
class AutoArt():
    def __init__(self):
        self.login_url='https://www.sectown.cn/login'
        self.create_url = 'https://www.sectown.cn/admin/article/create'
        self.browser=webdriver.Chrome('./chromedriver')

    # 登录界面
    def auto_login(self,username='15700082275',password = 'jcq402'):
        self.browser.get(self.login_url)
        user = self.browser.find_element_by_name('_username')
        pwd = self.browser.find_element_by_name('_password')
        user.send_keys(username)
        pwd.send_keys(password)
        pwd.send_keys(Keys.RETURN)


    def auto_done(self,title_text,head_text,content_text):
        # 跳转资讯发布界面
        self.browser.execute_script('window.open("%s")' % self.create_url)
        # 切换窗口
        handles =self.browser.window_handles
        self.browser.switch_to_window(handles[-1])
        self.browser.implicitly_wait(5)
        # 输入标题
        title = self.browser.find_element_by_id('article-title-field')
        title.send_keys(title_text)

        # 选择标签
        s1 = Select(self.browser.find_element_by_id('categoryId'))
        s1.select_by_value('11')

        # 输入正文
        content = self.browser.find_element_by_tag_name('iframe')
        self.browser.switch_to_frame(content)
        p = self.browser.find_element_by_tag_name('body')
        p.send_keys(head_text + '\n' + content_text)

        # 发布按钮
        self.browser.switch_to_default_content()
        self.browser.find_element_by_id('article-operate-save').click()

        self.browser.close()

if __name__ == '__main__':
    sq=Sqlite_db()
    sql_list=sq.get_date('secrss','2018-04-24')
    news=AutoArt()
    news.auto_login()
    for i in sql_list:
        _,_,_,title_text,_,_,_,head_text,content_text=i
        news.auto_done(title_text,head_text,content_text)
    print 'done'
        # print title_text
        # print head_text
        # print content_text

    #login_url='http://dev3.securitytown.net/login'
    #create_url='http://dev3.securitytown.net/admin/article/create'



