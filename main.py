import pandas as pd
from playwright.async_api import async_playwright
import asyncio
from page_utils import GUBAScraperPlaywright
from utils import GUBAContentPlaywright, get_content
import datetime

async def main(start_page = 1 , end_page = 1, stock_code = 'zssh000001', wait1 = 1, wait2 = 5):

    start_time = datetime.datetime.now()
    guba = pd.DataFrame({}, columns=['正文'])
    a = GUBAScraperPlaywright()
    await a.start()  # Ensure you await any necessary initialization if your class requires it.
    all_urls, df = await a.get_urls(start_page=start_page, end_page=end_page, code=stock_code, wait1=wait1, wait2=wait2)  # 使用 await 等待异步操作完成
    async def run_scraper(urls_list):
        scraper = GUBAContentPlaywright()
        results = await scraper.fetch_guba_contents(urls_list, wait1=wait1, wait2=wait2)
        return results

    guba_content = await run_scraper(all_urls)  # Await the completion of the scraping task

    for i, content in enumerate(guba_content):
        try:
            if content is None:
                print('第', i+1, '页为空，跳过处理。')
                continue
            content_text = get_content(content)
            guba.loc[i] = [content_text]  # Collect the data
            print('第', i+1, '页处理完成')
        except Exception as e:
            print('处理第', i+1, '页时出现异常：', e)

    # Combine with the initial dataframe and save to Excel
    final_result = pd.concat([df, guba], axis=1)
    final_result.to_excel(f'股吧第{start_page}页到{end_page}页.xlsx', index=False)

    # Record and print the processing end time and duration
    end_time = datetime.datetime.now()
    print('处理结束时间：', end_time)
    duration = end_time - start_time
    print('总共用时：', duration)
    await a.close()

if __name__ == "__main__":
    asyncio.run(main())

