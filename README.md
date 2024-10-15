# Effective Email Search with Elasticsearch

This repository contains code for easily creating an Elasticsearch cluster configured to interact and experiment with the most effective ways to search by email address. The project is based on the concepts discussed in the article [Elasticsearch Autocomplete Email Analyzer](https://medium.com/@andrewdieken/elasticsearch-autocomplete-email-analyzer-e94693878121).

## Prerequisites

- Python 3.x
- Elasticsearch cluster

## Setup

1. Ensure your Elasticsearch cluster is running.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment: `cp example.env .env` and edit `.env` with your cluster details.

## Usage

### Quick Start

Create index and populate with sample data:

```bash
python main.py --create --populate
```

### Customization

Modify these files to customize the index:
- `index_settings.json`: Index settings (analyzers, filters)
- `index_mappings.json`: Index mappings (fields, data types)
- `index_data.json`: Sample data

To apply changes, recreate the index:

```bash
python main.py --delete --create --populate
```

### Querying Examples

Below are Python code examples for analyzing and searching emails using three different field types:

1. Elasticsearch Text Field (default analysis)
2. Elasticsearch search-as-you-type Field
3. Elasticsearch Text Field with Custom Analyzer

Each section includes:
- An analysis example
- Search examples for various scenarios (full email, partial email, misspellings) highlighting the differences in behavior between the field types.

To run these examples, use the provided Python snippets in your environment.

#### Elasticsearch [Text Field](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) with default analysis

- __Analyze__

    ```python
    from main import *

    resp = es_client.indices.analyze(
        index="account",
        field="built_in_text_field_email",
        text="Mic.Josnson_42@live.com"
    )
    print(resp)
    ```

- __Search__

    ```python
    from main import *

    resp = es_client.search(
        index="account",
        query={
            "multi_match": {
                "query": "Mic.Josnson_42@live.com",
                "fields": [
                    "built_in_text_field_email",
                    "built_in_text_field_email.keyword"
                ]
            }
        }
    )
    print(resp)
    ```

    1. Full email address:
       - Query: `Mic.Johnson_42@live.com`
       - Result: ✅ Works as expected
    2. Full email address with misspelling:
       - Query: `Mic.Josnson_42@live.com`
       - Result: ✅ Works as expected
    3. Partial email address:
       - Query: `Mic.John`
       - Result: ❌ Does __not__ work as expected (analyzer produces no matching tokens)
    4. Partial email address with misspelling:
       - Query: `Mic.Josnson_42`
       - Result: ❌ Does __not__ work as expected (analyzer produces no matching tokens)


#### Elasticsearch [search-as-you-type Field](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-as-you-type.html)

- __Analyze__

    ```python
    from main import *

    resp = es_client.indices.analyze(
        index="account",
        field="search_as_you_type_field_email",
        text="Mic.Johnson-42@live.com"
    )
    print(resp)
    ```

- __Search__

    ```python
    from main import *

    resp = es_client.search(
        index="account",
        query={
            "query": {
                "multi_match": {
                "query": "Mic.Johnson_42@live.com",
                "type": "bool_prefix",
                "fields": [
                    "search_as_you_type_field_email",
                    "search_as_you_type_field_email._2gram",
                    "search_as_you_type_field_email._3gram"
                ]
                }
            }
        }
    )
    print(resp)
    ```

    1. Full email address:
       - Query: `Mic.Johnson_42@live.com`
       - Result: ✅ Works as expected
    2. Full email address with misspelling:
       - Query: `Mic.Josnson_42@live.com`
       - Result: ✅ Works as expected
    3. Partial email address:
       - Query: `Mic.John`
       - Result: ✅ Works as expected
    4. Partial email address with trailing period
        - Query: `Mic.`
        - Result: ❌ Does __not__ work as expected (analyzer produces no matching tokens as the period is stripped from the search query)
    5. Partial email address with misspelling:
       - Query: `Mic.Josnson_42`
       - Result: ❌ Does __not__ work as expected (analyzer produces no matching tokens)

#### Elasticsearch [Text Field](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) with [Custom Analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-overview.html#analysis-customization)

- __Analyze__

    ```python
    from main import *

    resp = es_client.indices.analyze(
        index="account",
        field="built_in_text_field_with_custom_analyzer_email",
        text="Mic.Johnson-42@live.com"
    )
    print(resp)
    ```

- __Search__

    ```python
    from main import *

    resp = es_client.search(
        index="account",
        query={
            "multi_match": {
                "query": "Mic.Johnson-42@live.com",
                "fields": [
                    "built_in_text_field_with_custom_analyzer_email",
                    "built_in_text_field_with_custom_analyzer_email.keyword"
                ]
            }
        }
    )
    print(resp)
    ```

    1. Full email address:
       - Query: `Mic.Johnson_42@live.com`
       - Result: ✅ Works as expected
    2. Full email address with misspelling:
       - Query: `Mic.Josnson_42@live.com`
       - Result: ✅ Works as expected
    3. Partial email address:
       - Query: `Mic.John`
       - Result: ✅ Works as expected
    4. Partial email address with trailing period
        - Query: `Mic.`
        - Result: ✅ Works as expected
    5. Partial email address with misspelling:
       - Query: `Mic.Josnson_42`
       - Result: ✅ Works as expected
