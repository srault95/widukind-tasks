# -*- coding: utf-8 -*-

from urllib.parse import urlparse

from elasticsearch import Elasticsearch
from pymongo import MongoClient
from decouple import config as env_config

def get_mongo_url():
    return env_config("WIDUKIND_MONGODB_URL", "mongodb://localhost/widukind")

def get_es_url():
    return env_config("WIDUKIND_ES_URL", "http://localhost:9200")

def get_mongo_client(url=None):
    # TODO: tz_aware
    url = url or get_mongo_url()
    client = MongoClient(url)
    return client

def get_mongo_db(url=None):
    # TODO: tz_aware
    url = url or get_mongo_url()
    client = get_mongo_client(url)
    return client.get_default_database()

def get_es_client(url=None):
    url = url or get_es_url()
    url = urlparse(url)
    es = Elasticsearch([{"host": url.hostname, "port": url.port}])
    return es

