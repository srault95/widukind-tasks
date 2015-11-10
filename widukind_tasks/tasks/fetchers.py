# -*- coding: utf-8 -*-

from dlstats.fetchers import FETCHERS, FETCHERS_DATASETS
from widukind_tasks import utils

def run_fetcher(fetcher_name=None, dataset_code=None):
    """Run complete fetcher or one dataset only
    """
    
    db = utils.get_mongo_db()
    es_client = utils.get_es_client()
    fetcher = FETCHERS[fetcher_name](db=db, es_client=es_client)
    fetcher.provider.update_database()
    fetcher.upsert_categories()
    
    if dataset_code:
        fetcher.upsert_dataset(dataset_code)
    else:
        for dataset_code in FETCHERS_DATASETS[fetcher_name].keys():
            fetcher.upsert_dataset(dataset_code)
            
