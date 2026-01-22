# news_scraper.py 使用说明

## 1. 功能介绍

`news_scraper.py` 是一个用于从证券时报网（stcn.com）抓取股票相关新闻的爬虫脚本。该脚本能够自动获取指定股票的新闻链接，并抓取新闻的详细内容，包括标题、发布时间、正文内容和原始链接。

## 2. 依赖库

- pandas
- selenium
- BeautifulSoup4
- requests
- json
- random
- os

## 3. 脚本结构

### 3.1 主要函数

#### `get_article_links(ticker, ticker_name)`
- **功能**：获取指定股票代码和名称的新闻链接
- **参数**：
  - `ticker`：股票代码
  - `ticker_name`：股票名称
- **返回值**：无直接返回值，将新闻链接保存到 `../news_link/{ticker}.json` 文件中

#### `fetch_news(ticker)`
- **功能**：根据获取的新闻链接抓取新闻详细内容
- **参数**：
  - `ticker`：股票代码
- **返回值**：无直接返回值，将新闻内容保存到 `../news/{ticker}.json` 或 `../news/{ticker}_failed.json`（如果抓取失败）

#### `main()`
- **功能**：主函数，控制整个新闻抓取流程
- **流程**：
  1. 从 `Corrected_CSV_File_Last_Date_Summary.csv` 文件读取股票列表
  2. 遍历股票列表，检查是否已存在新闻文件
  3. 对未抓取新闻的股票，调用 `get_article_links()` 获取新闻链接
  4. 调用 `fetch_news()` 抓取新闻内容

## 4. 输入输出

### 4.1 输入

- **股票列表文件**：`Corrected_CSV_File_Last_Date_Summary.csv`，包含以下列：
  - `code`：股票代码
  - `code_name`：股票名称

### 4.2 输出

- **新闻链接文件**：`../news_link/{ticker}.json`，存储抓取到的新闻链接
- **新闻内容文件**：
  - 成功：`../news/{ticker}.json`，存储抓取到的新闻内容
  - 失败：`../news/{ticker}_failed.json`，存储失败信息

### 4.3 新闻内容格式

```json
[
    {
        "time": "发布时间",
        "title": "新闻标题",
        "content": "新闻正文",
        "link": "原始新闻链接"
    }
]
```

## 5. 使用方法

### 5.1 准备工作

1. 确保已安装所有依赖库：
   ```bash
   pip install pandas selenium beautifulsoup4 requests
   ```

2. 下载并安装 Chrome 浏览器

3. 确保 ChromeDriver 与 Chrome 浏览器版本匹配，并将其添加到系统 PATH 中

4. 准备股票列表文件 `Corrected_CSV_File_Last_Date_Summary.csv`

### 5.2 运行脚本

在 `dataset_construction` 目录下运行：

```bash
python news_scraper.py
```

### 5.3 配置说明

- **User-Agent 池**：脚本内置了多种 User-Agent，会随机选择以模拟不同设备
- **无头模式**：默认使用无头模式运行 Chrome，不会显示浏览器窗口
- **请求频率控制**：
  - 每 120 个请求暂停 10 秒
  - 滚动加载时每次等待 2 秒
  - 初始页面加载等待 3 秒

## 6. 注意事项

1. **反爬机制**：网站可能有反爬机制，建议不要频繁运行脚本
2. **网络稳定性**：确保网络连接稳定，避免因网络问题导致抓取失败
3. **ChromeDriver 版本**：确保 ChromeDriver 与 Chrome 浏览器版本匹配
4. **文件路径**：脚本中使用了相对路径，确保在正确的目录下运行
5. **错误处理**：脚本会自动处理连续失败情况，连续 10 次失败后会停止抓取

## 7. 运行流程

1. 脚本从 CSV 文件读取股票列表
2. 对于每个股票，检查是否已存在新闻文件
3. 如果不存在，调用 `get_article_links()` 获取新闻链接：
   - 配置 Chrome 浏览器选项
   - 设置随机 User-Agent
   - 访问搜索页面
   - 滚动加载所有新闻链接
   - 解析并保存新闻链接
4. 调用 `fetch_news()` 抓取新闻内容：
   - 遍历新闻链接
   - 使用随机 User-Agent 访问每个新闻页面
   - 解析新闻标题、时间、内容
   - 保存新闻内容到 JSON 文件

## 8. 常见问题

### 8.1 抓取失败

- **原因**：可能是网络问题、网站反爬机制或 ChromeDriver 版本不匹配
- **解决方法**：检查网络连接，更新 ChromeDriver，或降低抓取频率

### 8.2 新闻链接为空

- **原因**：可能是股票名称不正确或该股票没有相关新闻
- **解决方法**：检查 CSV 文件中的股票名称是否正确

### 8.3 ChromeDriver 错误

- **原因**：ChromeDriver 版本与 Chrome 浏览器版本不匹配
- **解决方法**：下载与 Chrome 浏览器版本匹配的 ChromeDriver

## 9. 扩展建议

1. 可以添加更多新闻源支持
2. 可以实现增量抓取，只抓取新发布的新闻
3. 可以添加新闻内容的清洗和预处理功能
4. 可以实现多线程或异步抓取，提高抓取效率

## 10. 示例输出

### 新闻链接文件示例（../news_link/600036.json）

```json
[
    "https://www.stcn.com/article/123456.html",
    "https://www.stcn.com/article/789012.html"
]
```

### 新闻内容文件示例（../news/600036.json）

```json
[
    {
        "time": "2023-06-01 10:00:00",
        "title": "招商银行发布2023年一季度财报",
        "content": "招商银行今日发布2023年一季度财报，营业收入同比增长10%...",
        "link": "https://www.stcn.com/article/123456.html"
    }
]
```