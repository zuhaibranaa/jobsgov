# jobsgov

A Scrapy crawler for **jobs.gov.hk**, the Hong Kong government jobs board. It pages through the
job search results and extracts the posting, including the employing department.

## Stack

- Python, Scrapy
- Item pipelines and middlewares under `jobsgov/`

## Layout

```
scrapy.cfg
jobsgov/
  items.py
  middlewares.py
  pipelines.py
  settings.py
  spiders/
    jobs.py
```

## Running it

```bash
pip install scrapy
scrapy crawl jobs
```

## Note on the department parser

The board renders the employing department as a run of capitalised abbreviations inside the
posting detail. `spiders/jobs.py` extracts that run and filters it against the department name
already present on the listing, which is what keeps the department field clean.

Expect to re-tune the selectors when the board changes its markup.
