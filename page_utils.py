from playwright.async_api import async_playwright
import pandas as pd
import asyncio
import random

class GUBAScraperPlaywright:
    def __init__(self):
        pass  # Initialization will be handled in an async context

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.page = await self.browser.new_page()

    async def get_html_content(self, url):
        await self.page.goto(url)
        return await self.page.content()
    
    async def get_urls_from_html(self, html_content):
        await self.page.set_content(html_content)  # 确保 await set_content
        urls = []
        
        # 使用 await 获取 query_selector_all 的结果
        title_divs = await self.page.query_selector_all('table.default_list >> div.title')
        for title_div in title_divs:
            a_tag = await title_div.query_selector('a')
            if a_tag:
                href = await a_tag.get_attribute('href')
                if href.startswith('//'):
                    href = 'https:' +href
                if href.startswith('/'):
                    href = 'https://guba.eastmoney.com' + href
                urls.append(href)

        # 以下部分也需要确保使用 await 处理 query_selector_all
        ccgp = await self.page.query_selector('ul.tab_content')
        read_divs = await ccgp.query_selector_all('div.read')
        title_divs = await ccgp.query_selector_all('div.title')
        time_divs = await ccgp.query_selector_all('div.update')
        reply_divs = await ccgp.query_selector_all('div.reply')

        rows = []
        for read, title, time, reply in zip(read_divs, title_divs, time_divs, reply_divs):
            read_text = await read.text_content()
            title_text = await title.text_content()
            time_text = await time.text_content()
            reply_text = await reply.text_content()

            rows.append({'标题': title_text, '评论': reply_text, '发帖时间': time_text, '阅读': read_text})

        df = pd.DataFrame(rows)
        return urls, df


    async def get_urls(self, start_page, end_page, code, wait1, wait2):
        all_urls = []
        df1 = pd.DataFrame({'标题': [], '评论': [], '发帖时间': [], '阅读': []})
        for page in range(start_page, end_page + 1):
            url = f'https://guba.eastmoney.com/list,{code},f_{page}.html'
            html_content = await self.get_html_content(url)
            page_urls, df2 = await self.get_urls_from_html(html_content)
            df1 = pd.concat([df1, df2], ignore_index=True)
            all_urls.extend(page_urls)
            wait_time = random.uniform(wait1, wait2)
            await asyncio.sleep(wait_time)
            print(f"页面 {page} 爬取完成，等待时间: {wait_time} 秒")
        return all_urls, df1

    async def close(self):
        await self.browser.close()
        await self.playwright.stop()

