# dataset_construction 模块 API

本章节详细说明 LightQuant 项目 `dataset_construction` 目录下数据构建相关脚本的 API 接口，包括新闻爬虫和数据收集工具。

## news_scraper.py

新闻数据爬虫模块，用于从证券时报等网站抓取财经新闻。

### get_article_links

获取指定股票的新闻链接列表。

函数签名：
```python
def get_article_links(ticker, ticker_name)
```

参数说明：
- ticker (str)：股票代码
- ticker_name (str)：股票名称

功能说明：
使用 Selenium 模拟浏览器访问证券时报搜索页面，抓取指定股票的相关新闻链接。爬取过程包括模拟滚动加载更多内容，保存链接到 JSON 文件。

实现细节：
- 使用 Chrome 浏览器（headless 模式）
- 随机 User-Agent 模拟不同设备
- 滚动加载最多 200 次
- 每次滚动间隔 2 秒
- 连续 3 次滚动高度不变时停止

输出文件：
- ../news_link/{ticker}.json：包含新闻链接列表

### fetch_news

抓取单条新闻的详细内容。

函数签名：
```python
def fetch_news(ticker)
```

参数说明：
- ticker (str)：股票代码

功能说明：
读取链接文件，依次访问每条新闻链接，抓取新闻的详细信息（发布时间、标题、正文）。使用 BeautifulSoup 解析 HTML，提取结构化内容。

实现细节：
- 使用 Chrome 浏览器（headless 模式）
- 每 120 次请求暂停 10 秒防封禁
- 连续 10 次失败则停止爬取
- 自动清理链接标签保留纯文本

输出文件：
- ../news/{ticker}.json：包含新闻详情列表
- ../news/{ticker}_failed.json：爬取失败时生成

### main

主函数，执行批量爬取。

函数签名：
```python
def main()
```

功能说明：
读取股票代码列表，依次为每只股票执行新闻链接获取和详情抓取。跳过已存在 JSON 文件的股票，避免重复爬取。

输入文件：
- Corrected_CSV_File_Last_Date_Summary.csv：包含股票代码和名称的 CSV 文件

依赖配置：
- Chrome 浏览器驱动
- 网络连接
- 足够的存储空间

## price_data_collection.py

股票价格数据收集模块，提供价格数据的获取和更新功能。

### 预期功能

该模块预期提供以下功能（具体实现可能因版本而异）：从数据源获取历史价格数据；增量更新最新交易日数据；数据格式转换和标准化；质量检查和异常值处理。

### 使用方法

基本使用流程：配置数据源 API 密钥或访问凭证；运行数据收集脚本获取历史数据；执行数据验证确认数据质量；将数据保存到 dataset/price/ 目录。

## 数据构建流程

### 完整流程

构建自定义数据集的完整流程如下：

第一步是准备股票列表。创建包含股票代码和名称的 CSV 文件，格式为：code 列存储股票代码，code_name 列存储股票中文名称。

第二步是运行新闻爬虫。执行 `python dataset_construction/news_scraper.py`，脚本将自动爬取所有股票的财经新闻。

第三步是数据清洗。检查爬取的数据质量，处理重复、缺失或格式错误的数据。

第四步是保存到数据集目录。将处理后的新闻数据保存到 `dataset/{数据集名称}/news/{股票名称}/` 目录，文件以日期命名。

第五步是生成词向量。使用 `python utils/word2vec.py` 生成新闻嵌入文件。

### 注意事项

使用数据构建模块时需要注意以下事项：遵守目标网站的 robots.txt 和服务条款；控制爬取频率避免对服务器造成过大压力；爬取可能需要较长时间，建议分批执行；新闻内容受版权保护，请遵守许可证要求；部分新闻可能已删除或不可访问，导致爬取不完整。

### 依赖配置

运行数据构建脚本需要安装以下依赖：selenium 用于浏览器自动化；beautifulsoup4 用于 HTML 解析；pandas 用于数据处理；Chrome 浏览器或 Chromium 浏览器；ChromeDriver 与浏览器版本匹配。

### 错误处理

爬虫可能遇到的常见错误及处理方法：WebDriver 错误，检查浏览器和驱动版本匹配；网络超时，增加等待时间或重试；元素定位失败，网站结构可能已更新；反爬措施，可能需要使用代理或更复杂的模拟策略。
