# Effective Email Search with Elasticsearch

This repository contains code for easily creating an Elasticsearch cluster configured to interact and experiment with the most effective ways to search by email address. The project is based on the concepts discussed in the article [Elasticsearch Autocomplete Email Analyzer](https://medium.com/@andrewdieken/elasticsearch-autocomplete-email-analyzer-e94693878121).

## Prerequisites

- Python 3.x
- An Elasticsearch cluster

## Setup

1. Ensure you have an Elasticsearch cluster running. You can either run Elasticsearch locally or use a cloud provider.

2. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Copy the `example.env` file to `.env`

    ```bash
    cp example.env .env
    ```

4. Edit the `.env` file with the details for _your_ Elasticsearch cluster.

## Usage

### Quick Start

Get started quickly by running:

```bash
python main.py --create --populate
```

This will create the `account` index and populate it with sample data.

### Customizing the Index

You can customize the index by altering the [settings](#index-settings), [mappings](#index-mappings), or [data](#index-data). After making your changes, recreate the index to apply them by following the steps in the [Recreating the Index](#recreating-the-index) section.

This process allows you to experiment with different configurations and see their effects on search functionality.

#### Index Settings

The index settings are defined in `index_settings.json`.

Alter this file to customize the index settings e.g. analyzers, token filters, etc.

#### Index Mappings

The index mappings are defined in `index_mappings.json`.

Alter this file to customize the index mappings e.g. fields, field data types, etc.

#### Index Data

The index data is defined in `index_data.json`.

Alter this file to customize the index data (the sample data is used to populate the index as part of the `--populate` flag).

### Recreating the Index

If you need to recreate the `account` index (e.g. to update the index settings or mappings), run:

```bash
python main.py --delete --create --populate
```

### Queries

Below you'll find example queries you can run to experiment and see first hand how different configurations affect search functionality.

#### Elasticsearch [Text Field](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) with default analysis

- __Analyze__ - see how the Elasticsearch Text Field with default analysis analyzes different emails by running:

    ```python
    from main import *

    resp = es_client.indices.analyze(
        index="account",
        field="built_in_text_field_email",
        text="Mic.Josnson_42@live.com"
    )
    print(resp)
    ```

- __Search__ - see how searching against the Elasticsearch Text Field with default analysis works by running the following queries.

    1. Full email address ✅ works as expected

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

    2.  Partial email address ❌ does __not__ work as expected due to analyzer producing no matching tokens

        ```python
        from main import *

        resp = es_client.search(
            index="account",
            query={
                "multi_match": {
                    "query": "Mic.John",
                    "fields": [
                        "built_in_text_field_email",
                        "built_in_text_field_email.keyword"
                    ]
                }
            }
        )
        print(resp)
        ```

    3. Full email address with misspelling ✅ works as expected

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

    4. Partial email address with misspelling ❌ does __not__ work as expected due to analyzer producing no matching tokens

        ```python
        from main import *

        resp = es_client.search(
            index="account",
            query={
                "multi_match": {
                    "query": "Mic.Josnson_42",
                    "fields": [
                        "built_in_text_field_email",
                        "built_in_text_field_email.keyword"
                    ]
                }
            }
        )
        print(resp)
        ```


#### Elasticsearch [search-as-you-type Field](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-as-you-type.html)

- __Analyze__ - see how the Elasticsearch search-as-you-type field analyzes different emails by running:

    ```python
    from main import *

    resp = es_client.indices.analyze(
        index="account",
        field="search_as_you_type_field_email",
        text="Mic.Johnson-42@live.com"
    )
    print(resp)
    ```

- __Search__ - see how searching against the Elasticsearch search-as-you-type field works by running the following queries.

    1. Full email address ✅ works as expected

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

    2.  Partial email address ✅ works as expected

        ```python
        from main import *

        resp = es_client.search(
            index="account",
            query={
                "query": {
                    "multi_match": {
                    "query": "Mic.John",
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

    3.  Partial email address (with trailing period) ❌ does __not__ work as expected due to analyzer producing no matching tokens (the `.` is stripped from the search query)

        ```python
        from main import *

        resp = es_client.search(
            index="account",
            query={
                "query": {
                    "multi_match": {
                    "query": "Mic.",
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

    4. Full email address with misspelling ✅ works as expected

        ```python
        from main import *

        resp = es_client.search(
            index="account",
            query={
                "query": {
                    "multi_match": {
                    "query": "Mic.Josnson_42@live.com",
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

    5. Partial email address with misspelling ❌ does __not__ work as expected due to analyzer producing no matching tokens

        ```python
        from main import *

        resp = es_client.search(
            index="account",
            query={
                "query": {
                    "multi_match": {
                    "query": "Mic.Josnson_42",
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

#### Elasticsearch [Text Field](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) with [Custom Analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-overview.html#analysis-customization)

- __Analyze__ - see how the Elasticsearch Text Field with a custom analyzer analyzes different emails by running:

    ```python
    from main import *

    resp = es_client.indices.analyze(
        index="account",
        field="built_in_text_field_with_custom_analyzer_email",
        text="Mic.Johnson-42@live.com"
    )
    print(resp)
    ```

- __Search__ - see how searching against the Elasticsearch Text Field with a custom analyzer works by running the following queries.

    1. Full email address ✅ works as expected

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

    2. Partial email address ✅ works as expected

        ```python
        from main import *

        resp = es_client.search(
            index="account",
            query={
                "multi_match": {
                    "query": "Mic.John",
                    "fields": [
                        "built_in_text_field_with_custom_analyzer_email",
                        "built_in_text_field_with_custom_analyzer_email.keyword"
                    ]
                }
            }
        )
        print(resp)
        ```

    3. Partial email address (with trailing period) ✅ works as expected

        ```python
        from main import *

        resp = es_client.search(
            index="account",
            query={
                "multi_match": {
                    "query": "Mic.",
                    "fields": [
                        "built_in_text_field_with_custom_analyzer_email",
                        "built_in_text_field_with_custom_analyzer_email.keyword"
                    ]
                }
            }
        )
        print(resp)
        ```

    4. Full email address with misspelling ✅ works as expected

        ```python
        from main import *

        resp = es_client.search(
            index="account",
            query={
                "multi_match": {
                    "query": "Mic.Josnson_42@live.com",
                    "fields": [
                        "built_in_text_field_with_custom_analyzer_email",
                        "built_in_text_field_with_custom_analyzer_email.keyword"
                    ]
                }
            }
        )
        print(resp)
        ```

    5. Partial email address with misspelling ✅ works as expected

        ```python
        from main import *

        resp = es_client.search(
            index="account",
            query={
                "multi_match": {
                    "query": "Mic.Josnson_42",
                    "fields": [
                        "built_in_text_field_with_custom_analyzer_email",
                        "built_in_text_field_with_custom_analyzer_email.keyword"
                    ]
                }
            }
        )
        print(resp)
        ```