# Web Crawler

## Setup on your machine

**Prerequisites:**
- Have one of these 2 routes setup
    - [uv](https://docs.astral.sh/uv/)
    - Python + [venv](https://docs.python.org/3/library/venv.html) + [pip](https://pip.pypa.io/en/stable/installation/)
- Have [git](https://git-scm.com/) installed on your machine.
- Access to this [github page](https://github.com/avgra3/py-webscraper.git)


### UV

```bash
uv venv
source .venv/bin/activate
uv add git+https://github.com/avgra3/py-webscraper.git@main
```

If that all ran without error, you should be good to go!

### Pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/avgra3/py-webscraper.git@main
```

If that all ran without error, you should be good to go!

## Usage

With your enviornment setup, you should be able to run:


```
pyscaper --help

usage: pyscraper [-h] [-p MAX_PAGES] [-c MAX_CONCCURENCY] -f FILENAME url

A simple web scraper that uses concurrency to efficiently scrape websites and return a JSON
file with the output

positional arguments:
  url                   The base URL you want to start the crawler.

options:
  -h, --help            show this help message and exit
  -p, --max-pages MAX_PAGES
                        The maximum number of web pages you want to scrape. (default: 10)
  -c, --max-conccurency MAX_CONCCURENCY
                        The number of concurrent threads you want to use. (default: 1)
  -f, --filename FILENAME
                        Output file location

```


## Acknowledgements

The initial version of this was created during a [boot.dev](boot.dev) project. Making it a more robust CLI was an extension of that project.
