from pyscraper.scrape import crawl_page
from pyscraper.async_crawler import AsyncCrawler
from pyscraper.jasoner import write_json_report
import sys
import asyncio
import argparse
from pathlib import Path


def check_positive_int(value: str) -> int:
    try:
        value_int = int(value)
    except ValueError as e:
        print(e)
        sys.exit(1)
    if value_int <= 0:
        print("value must be positive")
        sys.exit()
    return value_int


def check_parent_dir_exists(value: str) -> Path:
    value_path = Path(value)
    if value_path.parent.exists():
        return value_path
    return Path.cwd() / "report.json"

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pyscraper",
        description="A simple web scraper that uses concurrency to efficiently scrape websites and return a JSON file with the output",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "url", help="The base URL you want to start the crawler."
    )
    parser.add_argument(
        "-p",
        "--max-pages",
        type=check_positive_int,
        default=10,
        help="The maximum number of web pages you want to scrape.",
    )
    parser.add_argument(
        "-c",
        "--max-conccurency",
        type=check_positive_int,
        default=1,
        help="The number of concurrent threads you want to use.",
    )
    parser.add_argument(
        "-f",
        "--filename",
        type=check_parent_dir_exists,
        help="Output file location",
        required=True,
    )
    return parser.parse_args()


async def crawl_site_async(base_url: str, max_concurrency: int, max_pages: int):
    async with AsyncCrawler(
        base_url=base_url,
        page_data={},
        max_concurrency=max_concurrency,
        max_pages=max_pages,
    ) as crawler:
        return await crawler.crawl()


async def _async_main(args: argparse.Namespace) -> None:
    BASE_URL = args.url
    MAX_CONCURRENCY = args.max_concurrency
    MAX_PAGES = args.max_pages
    print(f"starting crawl of: {BASE_URL}")
    crawl_data = await crawl_site_async(
        base_url=BASE_URL, max_concurrency=MAX_CONCURRENCY, max_pages=MAX_PAGES
    )
    write_json_report(page_data=crawl_data, filename=args.filename)

def main() -> None:
    args = parse_arguments()
    try:
        asyncio.run(_async_main(args=args))
    except KeyboardInterrupt:
        sys.exit(130)

if __name__ == "__main__":
    main()
