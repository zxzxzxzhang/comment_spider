
---

# 股吧爬虫

该项目是一个用于爬取股吧网站上指定股票讨论帖内容的爬虫工具，使用了 Playwright 来进行网页内容的异步抓取，同时使用 BeautifulSoup 对网页内容进行解析。

## 功能特点

- 支持指定股票代码和起止页码范围进行内容抓取。
- 支持异步操作，提高爬取效率。
- 结果保存为 Excel 文件，方便后续分析和处理。
- 保存文件格式如下

| 标题 | 评论 | 发帖时间 | 阅读 | 正文 |
|-----|-----|---------|-----|-----|
| xxxxx | xxxxx | xxxxx | xxxxx | xxxxx |

## 安装依赖

在运行代码之前，请确保已安装以下依赖：

- python==3.10
- beautifulsoup4==4.12.3
- pandas==2.2.1
- playwright==1.43.0

你可以使用以下命令安装 Python 依赖：

```bash
pip install beautifulsoup4==4.12.3
pip install playwright==1.43.0
pip install pandas==2.2.1
```

## 使用方法

1. 在 `main()` 函数中设置起止页码、股票代码以及随机等待时间参数。
2. 运行 `asyncio.run(main())` 来启动爬虫程序。
3. 变量设置：
* start_page 开始爬取的页码
* end_page 结束爬取的页码
* stock_code 股票代码
* 随机等待时间：wait1至wait2

## 注意事项

- 请确保你的网络环境能够正常访问股吧网站，以免出现网络连接问题。
- 注意设置合适的随机等待时间，以避免被网站识别为恶意请求。

## 示例

以下是一个示例 (run.py)，爬取股吧网站上股票代码为 `zssh000001` 的帖子内容，从第 1 页到第 2 页，并将结果保存为 Excel 文件：

```python
import asyncio
from main import main

start_page = 1
end_page = 2
stock_code = 'zssh000001'
wait1 = 1
wait2 = 5
asyncio.run(main(start_page = start_page, end_page = end_page, stock_code = stock_code,wait1 = wait1, wait2 = wait2))
```
---
