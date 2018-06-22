import requests
import re
from bs4 import BeautifulSoup
import time
import pandas as pd
import random
import csv
import codecs
import sqlite3

conn = sqlite3.connect('wake.db')
c = conn.cursor()

c.execute("SELECT link FROM wake")
results = c.fetchall()
idlist = []  # 取出所有的地址
for i in results:
    idlist.append(i[0])

headers = {
    ##这里填写请求头
}


def backscore(url):
    html = requests.get(url=url, headers=headers)
    html.encoding = 'unicode_escape'
    back = {}
    avg = re.findall(r'"avg":"(.*?)"', html.text)
    back['avg'] = ''.join(avg)
    cre = re.findall(r'"credit":"(.*?)"', html.text)
    back['cre'] = ''.join(cre)
    coll = re.findall(r'college_hold":"(.*?)","between90', html.text)
    back['college'] = ''.join(coll)
    bt90 = re.findall(r'"between90":"(.*?)"', html.text)
    back['bt90'] = ''.join(bt90)
    bt80 = re.findall(r'"between80":"(.*?)"', html.text)
    back['bt80'] = ''.join(bt80)
    bt70 = re.findall(r'"between70":"(.*?)"', html.text)
    back['bt70'] = ''.join(bt70)
    bt60 = re.findall(r'"between60":"(.*?)"', html.text)
    back['bt60'] = ''.join(bt60)
    bl60 = re.findall(r'"below60":"(.*?)"', html.text)
    back['bl60'] = ''.join(bl60)
    return back


def getcom(url):
    html = requests.get(url=url, headers=headers)
    html.encoding = 'unicode_escape'
    com = re.findall(r'<h4>(.*?)<\\/h4>', html.text)
    star1 = re.findall(r'"avg_star":"(.*?)"', html.text)
    star = ''.join(star1)
    bac2 = {}
    bac2['com'] = ''.join(com)
    bac2['star'] = star
    return bac2


def backtr(url):
    html = requests.get(url=url, headers=headers)
    back = {}
    av23 = re.findall(r'"year":"12-13\\u5e74","avg_point":"(.*?)"', html.text)
    back['av23'] = ''.join(av23)
    av34 = re.findall(r'"year":"13-14\\u5e74","avg_point":"(.*?)"', html.text)
    back['av34'] = ''.join(av34)
    av45 = re.findall(r'"year":"14-15\\u5e74","avg_point":"(.*?)"', html.text)
    back['av45'] = ''.join(av45)
    av56 = re.findall(r'"year":"15-16\\u5e74","avg_point":"(.*?)"', html.text)
    back['av56'] = ''.join(av56)
    av67 = re.findall(r'"year":"16-17\\u5e74","avg_point":"(.*?)"', html.text)
    back['av67'] = ''.join(av67)
    av78 = re.findall(r'"year":"17-18\\u5e74","avg_point":"(.*?)"', html.text)
    back['av78'] = ''.join(av78)
    return back


url = 'http://bke.huanongbao.com/course/search.html?key=%25'

html = requests.get(url=url, headers=headers)
content = html.content
item = BeautifulSoup(content, 'html.parser')
oneitems = item.find_all('a', class_="weui-cell weui-cell_access")

for i, one in enumerate(oneitems):
    name = one.find('h4').text
    link = one['href']
    reallink = 'http://bke.huanongbao.com' + link
    if reallink in idlist: continue
    else:
        try:
            type = one.find('p').text.strip()
        except AttributeError:
            type = None
        teacher = one.find('div', class_='weui-cell__ft').text
        bac = backscore('http://bke.huanongbao.com/course/score.html?classname=' + str(name))
        avg = bac['avg']
        cre = bac['cre']
        college = bac['college']
        comment = getcom('http://bke.huanongbao.com/course/getcomment.html?classname=' + str(name) + '&teacher=' + str(
            teacher) + '&date=0')
        com = comment['com'].replace("'", "''")
        star = comment['star']
        bt90 = bac['bt90']
        bt80 = bac['bt80']
        bt70 = bac['bt70']
        bt60 = bac['bt60']
        bl60 = bac['bl60']
        tren = backtr('http://bke.huanongbao.com/score/scoretrends.html?classname=' + str(name))
        tr23 = tren['av23']
        tr34 = tren['av34']
        tr45 = tren['av45']
        tr56 = tren['av56']
        tr67 = tren['av67']
        tr78 = tren['av78']
        aitem = [i, name, reallink, type, teacher, avg, cre, college, com, star, bt90, bt80, bt70, bt60, bl60, tr23, tr34,
                 tr45, tr56, tr67, tr78]
        try:
            c.execute(
                "INSERT INTO wake(id,name,type,teacher,avg,credit,college,comments,star,bt90,bt80,bt70,bt60,bl60,av23,av34,av45,av56,av67,av78,link) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    i, name, type, teacher, avg, cre, college, com, star, bt90, bt80, bt70, bt60, bl60, tr23, tr34, tr45,
                    tr56, tr67, tr78,reallink))
            conn.commit()
            print(i, ' get !')
        except UnicodeEncodeError:
            print(i, ' 出现评论乱码')
            print('http://bke.huanongbao.com/course/getcomment.html?classname=' + str(name) + '&teacher=' + str(
                teacher) + '&date=0')
            com = com.encode('unicode_escape').decode('utf-8')
            print(com)
            c.execute(
                "INSERT INTO wake(id,name,type,teacher,avg,credit,college,comments,star,bt90,bt80,bt70,bt60,bl60,av23,av34,av45,av56,av67,av78,link) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    i, name, type, teacher, avg, cre, college, com, star, bt90, bt80, bt70, bt60, bl60, tr23, tr34, tr45,
                    tr56, tr67, tr78,reallink))
            conn.commit()





