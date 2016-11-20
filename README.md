# crawl_smth
水木版面简易爬虫，可用于租房、二手房、二手物品自动提醒

# 原理
读取版面的前若干页的标题，比对标题中的关键词，若匹配则输出到结果文件中。

注意：
- 简单起见，没有分析帖子正文。对于一般租房用途，标题信息已经足够。
- 为了避免封 IP，每爬一个页面后都随机等待若干秒

# 安装
- 确保已经安装了BeautifulSoup扩展
- git clone https://github.com/raywill/crawl_smth

# 修改
- 修改代码中的路径为自己的实际路径，建议放到 http 服务器路径下，便于通过网络直接浏览爬虫结果

# 运行
- python rent_crawl.py

# 预览效果
![爬虫效果预览](sample.png)

# 扩展
根据您自己的服务器环境，您可以增加如下扩展功能：
- cron 定时爬
- 消息通知

# 参考
- http://blog.csdn.net/maray/article/details/53163024
