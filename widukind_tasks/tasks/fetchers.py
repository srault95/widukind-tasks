# -*- coding: utf-8 -*-

#from pymongo import MongoClient
#from elasticsearch import Elasticsearch

from dlstats import configuration
from dlstats.fetchers import FETCHERS, FETCHERS_DATASETS

def run_fetcher(fetcher_name=None, dataset_code=None):
    """Run complete fetcher or one dataset only
    
    TODO: mongolock ici ou dans la tâche appelante ?
    
    """
    #client = MongoClient(**configuration['MongoDB'])
    #db = client.get_default_database()
    
    fetcher = FETCHERS[fetcher_name]()#db=db)
    fetcher.provider.update_database()
    fetcher.upsert_categories()
    
    if dataset_code:
        fetcher.upsert_dataset(dataset_code)
    else:
        for dataset_code in FETCHERS_DATASETS[fetcher_name].keys():
            fetcher.upsert_dataset(dataset_code)
            
