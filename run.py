import asyncio
from main import main

start_page = 1
end_page = 2
stock_code = 'zssh000001'
wait1 = 1
wait2 = 5

asyncio.run(main(start_page = start_page, end_page = end_page, stock_code = stock_code,wait1 = wait1, wait2 = wait2))