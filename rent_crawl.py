# coding:utf-8

from bs4 import BeautifulSoup
import re
import sys
import urllib
import time
import random
import time

reload(sys)
sys.setdefaultencoding("utf-8")

# 支持爬多个版面，取消下面的注释即可

# 二手房
# board = 'OurHouse'

# 二手市场主版
# board = 'SecondMarket'

# 租房
board = 'HouseRent'

keywords = []
matched = []
final = []

for kw in open('/home/wwwroot/www.reactshare.cn/rent/keywords.txt').readlines():
    keywords.append(kw.strip())

# print keywords[0]


#soup = BeautifulSoup(open('pg2.html'), "html5lib")

for page in range(1, 10):
    url = 'http://m.newsmth.net/board/%s?p=%s' % (board, page)
    data = urllib.urlopen(url).read()
    # print data
    soup = BeautifulSoup(data, "html5lib")
    for a in soup.find_all(href=re.compile("\/article\/" + board)):
        item = a.encode('utf-8')
        for kw in keywords:
            if item.find(kw) >= 0:
                matched.append(item)
    time.sleep(5 + 10 * random.random())

for item in matched:
    if item not in final:
        final.append(item)

html = "<html><head><meta charset='UTF-8' /><title>租房</title><base href='http://m.newsmth.net/' /></head><body>"
html += "<br/>".join(final)
html += "<p>last update at %s </p><p><a href='http://m.newsmth.net/board/%s'>水木社区</a></p>" % (time.strftime('%Y-%m-%d %X', time.localtime()), board)
html += "</body></html>"

output = open('/home/wwwroot/www.reactshare.cn/rent/index.html', 'w')
output.write(html)
output.close()

# notify
notifyUrl = "http://m.reactshare.cn/rent"
data = urllib.urlopen(notifyUrl).read()

