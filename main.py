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
    if es_client.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists. If you'd like to recreate the index, delete the existing index first with the 'delete_index' flag.")
        return

    print(f"Creating index '{index_name}'...")
    settings = json.load(open('index_settings.json'))
    mappings = json.load(open('index_mappings.json'))
    es_client.indices.create(index=index_name, settings=settings, mappings=mappings)
    print(f"Index '{index_name}' created successfully.")


def delete_index():
    """
    Delete the 'account' index.
    """
    if not es_client.indices.exists(index=index_name):
        print(f"Unable to delete, index '{index_name}' does not exist.")
        return

    print(f"Deleting index '{index_name}'...")
    es_client.indices.delete(index=index_name)
    print(f"{index_name}' deleted successfully.")


def populate_index():
    """
    Populate the 'account' index with data.
    """
    print(f"Populating index '{index_name}'...")
    accounts = json.load(open('index_data.json'))
    for account in accounts:
        es_client.index(index=index_name, body=account)
    print(f"Index '{index_name}' populated successfully.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage Elasticsearch index.')
    parser.add_argument('--create', action='store_true', help='Create the index')
    parser.add_argument('--delete', action='store_true', help='Delete the index')
    parser.add_argument('--populate', action='store_true', help='Populate the index with data')
    args = parser.parse_args()

    if args.delete:
        delete_index()

    if args.create:
        create_index()

    if args.populate:
        populate_index()
