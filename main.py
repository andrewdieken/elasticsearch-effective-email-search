import argparse
import json
import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv(dotenv_path='.env')

es_client = Elasticsearch(
    os.getenv("ELASTICSEARCH_HOST"),
    api_key=(os.getenv("ELASTICSEARCH_API_KEY_ID"), os.getenv("ELASTICSEARCH_API_KEY"))
)

index_name = 'account'


def create_index():
    """
    Create the 'account' index.
    """
    settings = json.load(open('index_settings.json'))
    mappings = json.load(open('index_mappings.json'))
    es_client.indices.create(index=index_name, settings=settings, mappings=mappings)


def _delete_index():
    """
    Delete the 'account' index.
    """
    es_client.indices.delete(index=index_name)


def populate_index():
    """
    Populate the 'account' index with data.
    """
    accounts = json.load(open('index_data.json'))
    for account in accounts:
        es_client.index(index=index_name, body=account)


if __name__ == 'main':
    parser = argparse.ArgumentParser(description='Manage Elasticsearch index.')
    parser.add_argument('--create', action='store_true', help='Create the index')
    parser.add_argument('--populate', action='store_true', help='Populate the index with data')
    args = parser.parse_args()

    if args.create:
        create_index()

    if args.populate:
        populate_index()
