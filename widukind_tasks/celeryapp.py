# -*- coding: utf-8 -*-

from decouple import config as env_config

from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

CELERY_MODE = env_config('CELERY_MODE', 'dev')

#'mongodb://mongodb/widukind?replicaSet=widukind'
#CELERY_BROKER = env_config('CELERY_BROKER', 'mongodb://localhost/widukind')
CELERY_BROKER = env_config('CELERY_BROKER', 'redis://localhost:6379/0')

#print("__main__ : ", __name__)#widukind_tasks.celeryapp
app = Celery()

#broker=CELERY_BROKER

class Config:
    BROKER_URL = CELERY_BROKER
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'UTC'
    #CELERY_MONGODB_BACKEND_SETTINGS = {
    #    'taskmeta_collection': 'celery_tasks', 
    #}    
    CELERY_IGNORE_RESULT = True
    CELERY_RESULT_PERSISTENT = False
    CELERY_DISABLE_RATE_LIMITS = True
    
class ProdConfig(Config):
    pass    

class DevConfig(Config):
    #CELERYD_CONCURRENCY = 1
    #CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_SEND_TASK_ERROR_EMAILS = False
    CELERYD_TASK_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s'
    #CELERY_REDIRECT_STDOUTS = True
    CELERY_REDIRECT_STDOUTS_LEVEL = 'DEBUG'
    
    #CELERY_REDIS_MAX_CONNECTIONS

if CELERY_MODE == "dev":
    app.config_from_object(DevConfig)
else:
    app.config_from_object(ProdConfig)    

"""
> Collections créés - sans execution de task
messages
messages.broadcast
messages.routing
"""

"""
app.conf.CELERY_MONGODB_BACKEND_SETTINGS = {
    #'database': "widukind", 
    'taskmeta_collection': 'celery_tasks', 
    #'options': {'tz_aware': True}
}

app.conf.CELERY_IGNORE_RESULT = True
#app.conf.CELERY_RESULT_PERSISTENT = False
app.conf.CELERY_DISABLE_RATE_LIMITS = True
app.conf.CELERY_TIMEZONE = 'UTC'
app.conf.CELERY_ENABLE_UTC = True
"""

"""
CELERY_TASK_RESULT_EXPIRES
#CELERYD_TASK_SOFT_TIME_LIMIT
#CELERY_ENABLE_REMOTE_CONTROL

#TODO: gmail ou mailgun
CELERY_SEND_TASK_ERROR_EMAILS = True
ADMINS = []
SERVER_EMAIL
"""

@app.task(#bind=True, 
          name="fetcher.run", ignore_result=True, default_retry_delay=30, max_retries=3)
def fetcher_run_task(fetcher_name=None, dataset_code=None):    
    from widukind_tasks.tasks.fetchers import run_fetcher
    try:
        return run_fetcher(fetcher_name=fetcher_name, dataset_code=dataset_code)
    except Exception as err:
        logger.error(err)
        fetcher_run_task.retry(kwargs=dict(fetcher_name=fetcher_name, dataset_code=dataset_code), exc=err)
        #avec ou sans raise, avec ou sans kwargs, NOK
        #raise self.retry(exc=err)

def main():
    try:
        #app.worker_main(argv=None)
        app.start(argv=None)
    except KeyboardInterrupt:
        pass
    
if __name__ == "__main__":
    """
    set PYTHONPATH=..\dlstats;..\pysdmx
    
    python -m widukind_tasks.celeryapp worker --loglevel=info
    
    > ok
    celery flower -A widukind_tasks.celeryapp --address=127.0.0.1 --port=5555
    
    > flower - onglet broker: 'mongodb' broker is not supported 

    
    python -m widukind_tasks.celeryapp --help
    python -m widukind_tasks.celeryapp worker --help
    python -m widukind_tasks.celeryapp worker --loglevel=info
    
    > log: sans --logfile, les sorties vont vers stderr
    >   -P POOL_CLS, --pool=POOL_CLS - Pool implementation: prefork (default), eventlet, gevent, solo or threads.
    > default: concurrency: 4 (prefork)
    
    > Ne marche plus
    celery -A widukind_tasks.celeryapp worker --loglevel=info
    celery -A widukind_tasks.celeryapp worker --loglevel=info -P gevent --concurrency=10 -n worker1.%h
    
    flower --address=127.0.0.1 --port=5555 --broker=mongodb://localhost/widukind
    flower -A widukind_tasks.celeryapp:app --address=127.0.0.1 --port=5555
    
    """
    main()
    