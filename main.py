from scrape import crawl_page
import sys

def main():
    args = sys.argv
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    if len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)
    BASE_URL = args[-1]
    print(f"starting crawl of: {BASE_URL}")
    crawl_data = crawl_page(base_url=BASE_URL, current_url=BASE_URL)
    number_of_pages = len(crawl_data)
    print("crawled data", crawl_data)
    print(f"number of pages scraped: {number_of_pages}")
    for data in crawl_data:
        print(data)


if __name__ == "__main__":
    main()
