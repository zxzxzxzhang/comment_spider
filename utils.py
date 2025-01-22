import json
import asyncio
import random
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

def get_content(soup):
    add_c = content2 = content3 = content1 = ''
    if soup.find('div', class_='xeditor_content app_h5_article'):
        content1 = soup.find('div', class_='xeditor_content app_h5_article').text.strip().replace('\n', '').replace(' ','')
    if soup.find('div', class_='newstext '):
        content2 = soup.find('div', class_='newstext ').text.strip().replace('\n', '').replace(' ', '')
    if soup.find('div', class_='xeditor_content editorlungo_content'):
        content3 = soup.find('div', class_='xeditor_content editorlungo_content').text.strip().replace('\n', '').replace(' ', '')

    if soup.find('div', class_='article-body'):
        content1 = soup.find('div', class_='article-body').text.strip().replace('\n', '').replace(' ', '')
    if soup.find_all('script'):
        javascript_blocks = soup.find_all('script')
        post_contents = []
        for block in javascript_blocks:
            # 获取 <script> 标签中的文本内容
            javascript_code = block.text

            # 查找 JavaScript 对象的起始位置和结束位置
            start_index = javascript_code.find("{")
            end_index = javascript_code.rfind("}")

            # 如果找到了对象的起始位置和结束位置
            if start_index != -1 and end_index != -1:
                # 提取 JavaScript 对象部分
                javascript_object = javascript_code[start_index:end_index + 1]
                try:
                    # 尝试将 JavaScript 对象转换为 Python 字典
                    python_dict = json.loads(javascript_object)

                    # 如果字典中包含 'post_add_list' 键
                    if 'post_add_list' in python_dict:
                        # 将其转换为列表形式，以便后续处理
                        python_dict['post_add_lists'] = [python_dict['post_add_list']]

                        # 遍历每个 'post_add_list'
                        for post_list in python_dict.get('post_add_lists', []):
                            # 遍历 post_add_list 中的每个元素
                            if post_list:
                                for post in post_list:
                                    # 提取 HTML 内容
                                    add_soup = BeautifulSoup(post['add_text'], 'html.parser')
                                    # 将每个内容拼接到帖子内容列表中
                                    post_content = add_soup.find('div', class_='xeditor_content').get_text(strip=True)
                                    post_contents.append(post_content)
                                    # 提前结束循环，因为已经找到所需的数据
                                    break
                except json.JSONDecodeError as e:
                    pass

        # 输出所有帖子内容
        for post_content in post_contents:
            add_c = add_c + post_content

    return content1 + content2 + content3 + '\n' + add_c

class GUBAContentPlaywright:
    def __init__(self):
        """
        初始化 CCGPContentPlaywright 实例。
        """

    async def fetch_page(self, browser, url, count):
        """
        使用 Playwright 异步打开单个页面并获取其内容。

        参数:
        - browser: Playwright 的浏览器实例。
        - url: 需要访问的 URL 地址。

        返回:
        - soup: 如果请求成功，返回对应 URL 的 BeautifulSoup 对象，否则返回 None。
        """
        page = await browser.new_page()
        try:
            response = await page.goto(url, timeout=600000)
            if response and response.status == 200:
                html = await page.content()
                soup = BeautifulSoup(html, 'html.parser')
                print(f"第{count}页请求成功, URL: {url}")
                return soup
            else:
                print(f"第{count}页请求失败: {response.status if response else '无响应'}, URL: {url}")
                return None
        except Exception as e:
            print(f"请求错误: {e}, URL: {url}")
            return None
        finally:
            await page.close()

    async def fetch_guba_contents(self, urls_list,wait1,wait2):
        """
        异步遍历每个 URL，使用 Playwright 发送请求并获取响应，最后返回一个包含 BeautifulSoup 对象的列表。

        参数:
        - urls_list: 包含所有需要抓取的 URLs 的列表。

        返回:
        - responses: 一个包含每个 URL 请求返回的 BeautifulSoup 对象的列表。
        """
        responses = []
        count = 0
        async with async_playwright() as p:
            for url in urls_list:
                count += 1
                browser_type = random.choice(['chromium', 'firefox', 'webkit'])  # 随机选择浏览器类型
                browser = None
                try:
                    if browser_type == 'chromium':
                        browser = await p.chromium.launch()
                    elif browser_type == 'firefox':
                        browser = await p.firefox.launch()
                    elif browser_type == 'webkit':
                        browser = await p.webkit.launch()

                    await asyncio.sleep(random.uniform(wait1, wait2))  # 随机等待时间
                    response = await self.fetch_page(browser, url, count)
                    if response:
                        responses.append(response)
                except Exception as e:
                    print(f"启动浏览器错误: {e}")
                finally:
                    if browser:
                        await browser.close()
        return responses


