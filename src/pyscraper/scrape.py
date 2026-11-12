import requests
import urllib.parse
from pyscraper.crawl import ExtractedPageData, normalize_url, extract_page_data


def get_html(url: str) -> str:
    data = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    if 400 <= data.status_code:
        data.raise_for_status()
    content_type = data.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise ValueError(f"not `text/html` was: `{content_type}`")
    html = data.text
    return html


def check_two_urls_same_domain(left_url: str, right_url: str) -> bool:
    left = urllib.parse.urlsplit(left_url)
    right = urllib.parse.urlsplit(right_url)
    return left.netloc == right.netloc


def crawl_page(
    base_url: str,
    current_url: str,
    page_data: dict[str, ExtractedPageData] = {},
) -> dict[str, ExtractedPageData]:
    print("current url:", current_url)
    # base_url: root URL of the website we're crawling
    # current_url: current URL we're crawling

    # 01 => Make sure the current_url and base_url are on the same domain. Else return.
    if not check_two_urls_same_domain(left_url=base_url, right_url=current_url):
        return page_data

    # 02 => normalized version of current url
    norm_url: str = normalize_url(url=current_url)

    # 03 => check that norm_url is not already in page_data. If it is, return
    if norm_url in page_data.keys():
        return page_data

    # 04 => get html of current page. With print statement so we can view in real time.
    print(f"Getting html for: `{current_url}`")
    html: str = get_html(url=current_url)

    # 05 => extract page data and add result to page_data
    extracted_data: ExtractedPageData = extract_page_data(
        html=html, page_url=current_url
    )
    page_data[norm_url] = extracted_data

    # 06 => use outgoing links for what to crawl next
    for link in extracted_data["outgoing_links"]:
        crawl_page(base_url=base_url, current_url=link, page_data=page_data)

    return page_data
