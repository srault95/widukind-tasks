# -*- coding: utf-8 -*-

from hashlib import md5

from decouple import config as env_config

from celery import Celery
from celery.utils.log import get_task_logger

from widukind_tasks.mongolock import MongoLock, MongoLockLocked
from widukind_tasks import utils

logger = get_task_logger(__name__)

CELERY_MODE = env_config('WIDUKIND_CELERY_MODE', 'prod')

app = Celery()

task_locker = None

class Config:
    BROKER_URL = env_config('WIDUKIND_CELERY_BROKER', 'redis://localhost:6379/0')
    #CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    BROKER_TRANSPORT_OPTIONS = {
        'fanout_prefix': True,
        'fanout_patterns': True,
    }
    #BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # 1 hour.
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'UTC'
    CELERY_IGNORE_RESULT = True
    CELERY_RESULT_PERSISTENT = False
    CELERY_DISABLE_RATE_LIMITS = True
    #TODO: msgpack
    CELERY_ACCEPT_CONTENT = ['pickle', 'json']
    #CELERY_TASK_SERIALIZER = 'json'
    #CELERY_RESULT_SERIALIZER = 'json'
    #CELERYD_HIJACK_ROOT_LOGGER = False
    
class ProdConfig(Config):
    pass    

class DevConfig(Config):
    CELERYD_CONCURRENCY = 1
    #CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_SEND_TASK_ERROR_EMAILS = False
    CELERYD_TASK_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s'
    #CELERY_REDIRECT_STDOUTS = True
    CELERY_REDIRECT_STDOUTS_LEVEL = 'DEBUG'
    #CELERY_REDIS_MAX_CONNECTIONS

class TestConfig(Config):
    pass


if CELERY_MODE == "dev":
    app.config_from_object(DevConfig)
elif CELERY_MODE == "testing":
    app.config_from_object(DevConfig)
else:
    app.config_from_object(ProdConfig)    

"""
TODO: BROKER_FAILOVER_STRATEGY

#CELERYD_TASK_SOFT_TIME_LIMIT
#CELERY_ENABLE_REMOTE_CONTROL

#TODO: gmail ou mailgun
CELERY_SEND_TASK_ERROR_EMAILS = True
ADMINS = []
SERVER_EMAIL
"""

#TODO: lock redis: https://pypi.python.org/pypi/python-redis-lock/2.3.0
#TODO: default_retry_delay and max_retries depends of fetcher settings ?
@app.task(#bind=True, 
          name="fetcher.run", ignore_result=True, default_retry_delay=30, max_retries=3)
def fetcher_run_task(fetcher_name=None, dataset_code=None):    
    from widukind_tasks.tasks.fetchers import run_fetcher

    try:
        #expire 10 minutes - timeout = 5mn
        #TODO: voir effet du timeout
        key = md5(("%s.%s" % (fetcher_name, dataset_code)).encode('utf-8')).hexdigest()
        with task_locker(key, 'fetcher.run', expire=600, timeout=300):
            return run_fetcher(fetcher_name=fetcher_name, dataset_code=dataset_code)
        
    except MongoLockLocked as err:
        logger.warning(str(err))
        #TODO: retry progressive
        fetcher_run_task.retry(kwargs=dict(fetcher_name=fetcher_name, dataset_code=dataset_code), exc=err)
    
    except Exception as err:
        logger.error(err)
        #TODO: retry sur quelles erreurs ?
        fetcher_run_task.retry(kwargs=dict(fetcher_name=fetcher_name, dataset_code=dataset_code), exc=err)

def main():
    global task_locker
    try:
        #app.worker_main(argv=None)
        mongo_client = utils.get_mongo_client()
        db = mongo_client.get_default_database()
        task_locker = MongoLock(client=mongo_client, db=db.name)
        app.start(argv=None)
    except KeyboardInterrupt:
        pass
    
if __name__ == "__main__":
    """
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
    