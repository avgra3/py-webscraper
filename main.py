from scrape import crawl_page
from async_crawler import AsyncCrawler
import sys
import asyncio

async def crawl_site_async(base_url: str, max_concurrency: int, max_pages: int):
    async with AsyncCrawler(base_url=base_url, page_data={}, max_concurrency=max_concurrency, max_pages=max_pages) as crawler:
        return await crawler.crawl()

async def main():
    args = sys.argv
    if len(args) < 4:
        print("not all arguments given: url max_concurrency max_pages")
        sys.exit(1)
    if len(args) > 4:
        print("too many arguments provided")
        sys.exit(1)
    BASE_URL = args[1]
    MAX_CONCURRENCY = int(args[2])
    MAX_PAGES = int(args[3])
    print(f"starting crawl of: {BASE_URL}")
    crawl_data = await crawl_site_async(base_url=BASE_URL, max_concurrency=MAX_CONCURRENCY, max_pages=MAX_PAGES)
    for url in crawl_data.values():
        print(url)




if __name__ == "__main__":
    asyncio.run(main())
