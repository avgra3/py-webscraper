import json
from pyscraper.crawl import ExtractedPageData


def write_json_report(
    page_data: dict[str, ExtractedPageData], filename="report.json"
):
    data = sorted(page_data.values(), key=lambda x: x["url"], reverse=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
