import os
import json

from elasticsearch import Elasticsearch
from dotenv import load_dotenv


load_dotenv(dotenv_path='.env')

es_client = Elasticsearch(
    os.getenv("ELASTICSEARCH_HOST"),
    api_key=(os.getenv("ELASTICSEARCH_API_ID"), os.getenv("ELASTICSEARCH_API_KEY"))
)

# Create the 'account' index
account_index_name = 'account'
settings = json.load(open('index_settings.json'))
mappings = json.load(open('index_mappings.json'))
es_client.indices.create(index=account_index_name, settings=settings, mappings=mappings)

# Populate the 'account' index with some data
accounts = json.load(open('index_data.json'))

