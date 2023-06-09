"""
The configured ElasticSearch DB engine
"""
import logging

from elasticsearch import Elasticsearch

from tds.settings import settings

logger = logging.Logger(__name__)


def es_client():
    """
    Factory Function that provides an ElasticSearch connection.
    """
    return Elasticsearch(
        [settings.ES_URL], basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD)
    )
