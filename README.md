
---

# Guba Spider

This project is a crawler tool for scraping content from discussion posts about specified stocks on guba website. It uses Playwright for asynchronous web content fetching and BeautifulSoup for parsing the web content.

## Features

- Supports scraping content based on specified stock codes and page range.
- Supports asynchronous operations to improve scraping efficiency.
- Results are saved as an Excel file for easy analysis and processing.
- The saved file format is as follows:

| Title | Comments | Post Time | Views | Body |
|-------|----------|-----------|-------|------|
| xxxxx | xxxxx    | xxxxx     | xxxxx | xxxxx |

## Installation

Before running the code, make sure you have installed the following dependencies:

- python==3.10
- beautifulsoup4==4.12.3
- pandas==2.2.1
- playwright==1.43.0

You can install Python dependencies using the following command:

```bash
pip install beautifulsoup4==4.12.3
pip install playwright==1.43.0
pip install pandas==2.2.1
```

## Usage

1. Set the start and end page numbers, stock code, and random wait time parameters in the `main()` function.
2. Run `asyncio.run(main())` to start the crawler program.
3. Variable settings:
   - `start_page`: Starting page number for scraping.
   - `end_page`: Ending page number for scraping.
   - `stock_code`: Stock code for the target stock.
   - Random wait time: between `wait1` and `wait2` 

## Notes

- Make sure your network environment can access the guba website to avoid network connection issues.
- Pay attention to setting appropriate random wait times to avoid being recognized as malicious requests by the website.

## Example

Here's an example (run.py) that scrapes content from guba posts with the stock code `zssh000001`, from page 1 to page 2, and saves the results as an Excel file:

```python
import asyncio
from main import main

start_page = 1
end_page = 2
stock_code = 'zssh000001'
wait1 = 1
wait2 = 5
asyncio.run(main(start_page=start_page, end_page=end_page, stock_code=stock_code, wait1=wait1, wait2=wait2))
```

---
