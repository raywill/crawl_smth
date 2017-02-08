#!/usr/bin/python
# coding:utf-8

from bs4 import BeautifulSoup
import re
import os
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
boards = ['OurEstate', 'PolicyEstate', 'SchoolEstate', 'RealEstate_review', 'ShangHaiEstate', 'RealEstate', 'Picture']

# 关注关键词文件
keywordsFile   = '/home/wwwroot/www.reactshare.cn/rent/keywords.txt'

# 黑名单关键词
blacklistFile  = '/home/wwwroot/www.reactshare.cn/rent/blacklist.txt'

# 爬虫结果文件，简易放入 http 服务目录中
outputFile     = '/home/wwwroot/www.reactshare.cn/rent/index.html'

# 比对文件，如果没有更新则不通知
lastCopy       = '/home/wwwroot/www.reactshare.cn/rent/last.html'

# 结果通知地址, 用于通知爬虫执行完毕，可查看结果
notifyUrl      = "http://m.reactshare.cn/rent"

# 最多爬的页数
maxCrawlPage = 3

# 每爬一个页面最少等待多少秒，防止被黑名单
# 外加一个随机等待因子，总计等待baseSleepSec + [0~X] 秒
baseSleepSec = 1
randWaitSec = 2

# 随机等待
################### 配置结束#################



reload(sys)
sys.setdefaultencoding("utf-8")


keywords = []
blacklist = []
matched = []
final = []

def notInBlackList(item) :
    for kw in blacklist:
        if item.find(kw) >= 0:
            return False
    return True

for kw in open(keywordsFile).readlines():
    keywords.append(kw.strip())

for kw in open(blacklistFile).readlines():
    blacklist.append(kw.strip())

for board in boards:
    for page in range(1, maxCrawlPage):
        url = 'http://m.newsmth.net/board/%s?p=%s' % (board, page)
        data = urllib.urlopen(url).read()
        # print data
        soup = BeautifulSoup(data, "html5lib")
        for a in soup.find_all(href=re.compile("\/article\/" + board)):
            item = a.encode('utf-8')
            for kw in keywords:
                if item.find(kw) >= 0 and notInBlackList(item):
                    matched.append(item)
        time.sleep(baseSleepSec + randWaitSec * random.random())

for item in matched:
    if item not in final:
        final.append(item)



# 为了避免无聊的人反复顶贴，做一次排序
final.sort()

union=final

# 检查本次爬得得数据是否有更新
if os.path.exists(lastCopy):
    last=[]
    for item in open(lastCopy).readlines():
        last.append(item.strip())
    union=list(set(final).union(set(last)))
    diff=list(set(union) ^ set(last))
    if len(diff) == 0 :
        sys.exit(0)

# 保存上次数据
tmp = open(lastCopy, 'w')
tmp.write('\n'.join(union))
tmp.close()

# 输出网页

html = "<html><head><meta charset='UTF-8' /><meta name='viewport' content='width=device-width,user-scalable=yes'><meta name='apple-mobile-web-app-capable' content='yes'><title>水木爬爬</title><base href='http://m.newsmth.net/' /></head><body>"
html += "<style> a:visited {color:gray;} a:active {color:red;} a {color:blue;}</style>"
html += "<br/>".join(union)
html += "<hr />"
for board in boards:
    html += "<p><a href='http://m.newsmth.net/board/%s'>%s</a></p>" % (board, board)
html += "<hr />"
html += "<p>%d items updated at %s </p><p><a href='http://m.newsmth.net/'>水木社区</a></p>" % (len(union), time.strftime('%Y-%m-%d %X', time.localtime()))
html += "</body></html>"

output = open(outputFile, 'w')
output.write(html)
output.close()

# notify
data = urllib.urlopen(notifyUrl).read()


