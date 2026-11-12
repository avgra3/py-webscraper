from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict


class ExtractedPageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def normalize_url(url: str) -> str:
    o = urlsplit(url)
    return "".join([o.netloc, o.path])


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if h_tag := soup.find("h1"):
        return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""
    if h_tag := soup.find("h2"):
        return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""
    return ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if main_tag := soup.find("main"):
        if p_tag := main_tag.find("p"):  # ty: ignore[missing-attribute]
            return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""
    if p_tag := soup.find("p"):
        return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""
    return ""


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    if body_tag := soup.find("body"):
        a_tags = body_tag.find_all("a")  # ty: ignore[missing-attribute]
        return [
            urljoin(base_url, a.get("href"))
            for a in a_tags
            if isinstance(a, Tag)
        ]
    return []


def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    if body_tag := soup.find("body"):
        img_tags = body_tag.find_all("img")  # ty: ignore[missing-attribute]
        return [
            urljoin(base_url, img.get("src"))
            for img in img_tags
            if isinstance(img, Tag)
        ]
    return []


def extract_page_data(html: str, page_url: str) -> ExtractedPageData:
    extracted_data: ExtractedPageData = {
        "url": page_url,
        "heading": get_heading_from_html(html=html),
        "first_paragraph": get_first_paragraph_from_html(html=html),
        "outgoing_links": get_urls_from_html(html=html, base_url=page_url),
        "image_urls": get_images_from_html(html=html, base_url=page_url),
    }
    return extracted_data
