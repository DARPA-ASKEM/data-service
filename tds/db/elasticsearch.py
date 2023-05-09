"""
The configured ElasticSearch DB engine
"""
from elasticsearch import Elasticsearch

from tds.settings import settings

url = f"http://{settings.ES_HOST}:{settings.ES_PORT}"

es = Elasticsearch([url])
