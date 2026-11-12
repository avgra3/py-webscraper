from pyscraper.crawl import ExtractedPageData, normalize_url, extract_page_data
from pyscraper.scrape import check_two_urls_same_domain
import asyncio
import aiohttp
import urllib.parse


class AsyncCrawler:
    def __init__(
        self,
        base_url: str,
        page_data: dict[str, ExtractedPageData],
        max_concurrency: int,
        max_pages: int,
    ):
        self.base_url = base_url
        self.base_domain = urllib.parse.urlsplit(self.base_url).netloc
        self.page_data = page_data
        self.visited: set[str] = set()
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(max_concurrency)

        self.should_stop: bool = False
        self.all_tasks = set()

        self.max_pages = max_pages

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url: str):
        async with self.lock:
            if self.should_stop:
                return False
            if len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl")
                return False
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True

    async def get_html(self, url: str):
        async with self.session.get(
            url,
            headers={"User-Agent": "BootCrawler/1.0"},
            raise_for_status=True,
        ) as resp:
            content_type = resp.headers.get("Content-Type", "")
            assert "text/html" in content_type
            return await resp.text()

    async def crawl_page(self, current_url: str):
        if self.should_stop:
            return
        print(f"trying -> {current_url}, base_url -> {self.base_url}")
        if not check_two_urls_same_domain(
            left_url=self.base_url, right_url=current_url
        ):
            return
        norm_current_url = normalize_url(current_url)
        new_page = await self.add_page_visit(normalized_url=norm_current_url)
        if not new_page:
            return
        async with self.semaphore:
            html = await self.get_html(url=current_url)
            if html is None:
                return
            extracted_data = extract_page_data(html=html, page_url=current_url)
            async with self.lock:
                self.page_data[norm_current_url] = extracted_data
            background_tasks = set()
            try:
                for link in extracted_data["outgoing_links"]:
                    task = asyncio.create_task(
                        self.crawl_page(current_url=link)
                    )
                    background_tasks.add(task)
                    self.all_tasks.add(task)
            finally:
                for t in background_tasks:
                    self.all_tasks.discard(t)
        await asyncio.gather(*background_tasks)

    async def crawl(self):
        await self.crawl_page(current_url=self.base_url)
        return self.page_data
