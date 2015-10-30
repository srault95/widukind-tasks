==============
Widukind Tasks
==============

Requirements
============

- Redis server
- MongoDB 2.4
- ElasticSearch 1.6.2
- Python 3.4

Installation
============

::

    $ git clone https://github.com/srault95/widukind-tasks.git
    
    $ cd widukind-tasks
    
    $ pip install -r requirements.txt
    
    $ pip install .

    
Run Celery worker
=================

**Servers Redis, MongoDB and Elasticsearch to be launched**

::

    $ widukind-tasks worker --loglevel=info
    # OR
    $ python -m widukind_tasks.celeryapp worker --loglevel=info
    
    # Help with:
    $ widukind-tasks --help
    $ widukind-tasks worker --help
    
    
Add Fetcher tasks
=================

::

    # Fetchers List
    $ widukind-tasks-cli fetchers --help
    
    # OR
    $ python -m widukind_tasks.client fetchers --help

    # Dataset list for one fetcher
    $ widukind-tasks-cli fetchers BIS datasets 
    
    # Run fetcher
    $ widukind-tasks-cli fetchers BIS run
    
    # Run dataset BIS - DSRP (66 series)
    $ widukind-tasks-cli fetchers --dataset DSRP BIS run
