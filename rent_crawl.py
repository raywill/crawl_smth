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
board = 'HouseRent'

# 关注关键词文件
keywordsFile = '/home/wwwroot/www.reactshare.cn/rent/keywords.txt'

# 黑名单关键词
blacklistFile = '/home/wwwroot/www.reactshare.cn/rent/blacklist.txt'

# 爬虫结果文件，简易放入 http 服务目录中
outputFile = '/home/wwwroot/www.reactshare.cn/rent/index.html'

# 比对文件，如果没有更新则不通知
lastCopy = '/home/wwwroot/www.reactshare.cn/rent/last.html'

# 结果通知地址, 用于通知爬虫执行完毕，可查看结果
notifyUrl = "http://m.reactshare.cn/rent"

# 最多爬的页数
maxCrawlPage = 20

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
    time.sleep(5 + 4 * random.random())

for item in matched:
    if item not in final:
        final.append(item)



# 输出网页
html = "<html><head><meta charset='UTF-8' /><title>租房</title><base href='http://m.newsmth.net/' /></head><body>"
html += "<br/>".join(final)
html += "<p>last update at %s </p><p><a href='http://m.newsmth.net/board/%s'>水木社区</a></p>" % (time.strftime('%Y-%m-%d %X', time.localtime()), board)
html += "</body></html>"

output = open(outputFile, 'w')
output.write(html)
output.close()


# 检查本次爬得得数据是否有更新
if os.path.exists(lastCopy) and "|".join(final).strip() == open(lastCopy).readline().strip() :
    sys.exit(0)

# 保存上次数据
tmp = open(lastCopy, 'w')
tmp.write("|".join(final))
tmp.close()

# notify
data = urllib.urlopen(notifyUrl).read()




