# coding:utf-8

from bs4 import BeautifulSoup
import re
import sys
import urllib
import time
import random
import time



#################### 配置开始#################

# 版面配置
# 支持爬多个版面，取消下面的注释即可
# 二手房
# board = 'OurHouse'
# 二手市场主版
# board = 'SecondMarket'
# 租房
board = 'HouseRent'

# 关注关键词文件
keywordsFile = '/home/wwwroot/www.reactshare.cn/rent/keywords.txt'

# 爬虫结果文件，简易放入 http 服务目录中
outputFile = '/home/wwwroot/www.reactshare.cn/rent/index.html'

# 结果通知地址, 用于通知爬虫执行完毕，可查看结果
notifyUrl = "http://m.reactshare.cn/rent"

################### 配置结束#################



reload(sys)
sys.setdefaultencoding("utf-8")


keywords = []
matched = []
final = []

for kw in open(keywordsFile).readlines():
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

output = open(outputFile, 'w')
output.write(html)
output.close()

# notify
data = urllib.urlopen(notifyUrl).read()

