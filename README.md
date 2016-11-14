# crawl_smth
水木版面简易爬虫，可用于租房、二手房、二手物品自动提醒

# 原理
读取版面的前若干页的标题，比对标题中的关键词，若匹配则输出到结果文件中。

注意：简单起见，没有分析帖子正文。对于一般租房用途，标题信息已经足够。

# 安装
- 确保已经安装了BeautifulSoup扩展
- git clone https://github.com/raywill/crawl_smth

# 修改
- 修改代码中的路径为自己的实际路径，简易放到 http 服务器路径下，这样可以通过网络直接浏览爬得得结果

# 运行
- python rent_crawl.py

# 扩展
- cron 定时爬
- 消息通知

# 参考
- http://blog.csdn.net/maray/article/details/53163024
