
# Scraper 

## Setup 

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Running the project
```
python3 auto_scrape.py <config_file>
```

Using the example config:

```
python3 auto_scrape.py dealer-trader-scrape.json
```

## Running the tests

```
python3 -m unittest
```

## Using the Config File


**Base Properties**

| Property           | type     | description                                       | required | default |
|--------------------|----------|---------------------------------------------------|----------|---------|
| num_pages          | int      | Number of pages to scrape                         | false    | 5       |
| start_url          | string   | The url to start scraping at                      | true     |         |
| title_selector     | selector | Selector for the title of a review                | true     |         |
| body_selector      | selector | Selector for the body of a review                 | true     |         |
| next_link_selector | selector | Selector that extracts the next url should be hit | true     |         |


**Selector Object**

| Property  | type                | description                                                                                                                                                                                                                              | required | default    |
|-----------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|------------|
| tag       | string              | The type of tag to select (IE div)                                                                                                                                                                                                       | false    | 5          |
| attrs     | object              | Key value pairs of html attributes. Must match exactly. For example to find tags by class {"class": "className"}. If the value is surrouned by `/`'s it is treated as a regex. `text` will match based on the inner text of the element. | false    |            |
| extractor | string or extractor | If extractor is a string, will return the value of the specified attribute. An object can be used to specify a regex for parital matching or a child object for recursive matching.                                                      | false    | inner text |


**Extractor Object**

| Property | type     | description                                                                                                        | required | default |
|----------|----------|--------------------------------------------------------------------------------------------------------------------|----------|---------|
| attr     | string   | The html attribute to extract (ie href)                                                                            | false    |         |
| regex    | string   | Regex to use to match against the extracted attrbute. Capture groups are not currently supported                   | false    |         |
| child    | selector | A recursive selector. When present, search for the selector this defines in the child html of the parent selector. | false    |         |
