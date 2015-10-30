# -*- coding: utf-8 -*-

import sys
import argparse

from dlstats.fetchers import FETCHERS, FETCHERS_DATASETS

def cmd_fetcher_run(fetcher_name=None, dataset_code=None):
    from widukind_tasks import celeryapp
    result = celeryapp.fetcher_run_task.delay(fetcher_name=fetcher_name, 
                                     dataset_code=dataset_code)
    
    print("run fetcher[%s] - tasks-id[%s]" % (fetcher_name, str(result)))
    return result
    """
    result :  84308e57-eba5-405c-93d7-eff44ff2e59f <class 'celery.result.AsyncResult'>
    > option pour attendre résultat d'execution:
    result.wait(timeout=None, propagate=True, interval=0.5, no_ack=True, follow_parents=True, EXCEPTION_STATES=frozenset(['FAILURE', 'RETRY', 'REVOKED']), PROPAGATE_STATES=frozenset(['FAILURE', 'REVOKED']))  
    """

def options():

    parser = argparse.ArgumentParser(description='dlstats client',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     add_help=True)

    parser.add_argument('-D', '--debug', action="store_true")

    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help',
                                       dest="subcommand")

    #TODO: liste des tâches en cours et leur état ou existe déjà ?

    tools_parser = subparsers.add_parser('tools', 
                                        help="Utils commands") 

    """
    tools_parser.add_argument('--dry', 
                                 action="store_true",
                                 help="Dry mode")
    """
    
    fetchers_parser = subparsers.add_parser('fetchers', 
                                            help="Fetcher commands", 
                                            #aliases=['fetch'],
                                            #dest="fetch_cmd"
                                            )
    
    fetchers_parser.add_argument(choices=FETCHERS.keys(),
                        dest='fetcher',
                        help="Choice fetcher.")

    fetchers_parser.add_argument(choices=['run', 'datasets'],
                        dest='action',
                        help="Action.")

    fetchers_parser.add_argument('--dataset', 
                        dest='dataset',
                        help='Dataset choice')

    """
    fetchers_parser.add_argument('--dry', 
                                 action="store_true",
                                 help="Dry mode")
    """
    
    """
    print(dir(fetcher_choice))
    python -m dlstats.cli fetchers --dry BIS run
    _StoreAction(option_strings=[], dest='fetcher', nargs=None, const=None, default=None, type=None, choices=dict_keys(['BIS']), help='Choice fetcher.', metavar=None)    
    """

    """    
    parser.add_argument('--reset', 
                        dest="reset",
                        action="store_true",
                        help="Reset fixtures")
    
    parser.add_argument('-G', '--greenlets',
                        default=1,
                        dest="greenlets",
                        type=int)
                        
    parser.add_argument('-C', '--config', 
                        dest='config_path',
                        default=os.environ.get('WIDUKIND_SETTINGS', default_config_path), 
                        help='Config filepath. default[%(default)s]')
    
    parser.add_argument('--log-config',
                        dest="log_config", 
                        help='Log config from file')

    """
    return dict(parser.parse_args()._get_kwargs())
        

def main():
    opts = options()
    subcommand = opts.get('subcommand')
    
    debug = opts.get('debug')
    """
    from pprint import pprint
    pprint(opts)
    
    python -m widukind_tasks.client fetchers BIS list
    {'action': 'list',
     'dataset': None,
     'debug': False,
     'fetcher': 'BIS',
     'subcommand': 'fetchers'}
    """

    if subcommand == "tools":
        pass
    
    elif subcommand == "fetchers":
        action = opts.get('action')
        fetcher = opts.get('fetcher')
        dataset = opts.get('dataset')
        #dry_mode = opts.get('dry')
    
        if action == 'run':
            if not dataset:
                sys.stderr.write("--dataset is required\n")
                sys.exit(1)
            cmd_fetcher_run(fetcher, dataset)            
            
        elif action == 'datasets':
            #_command_start(pid_file=pid_file, **config)
            print("----------------------------------------------------")
            print("Datasets for %s fetcher:" % fetcher)
            for dataset_code in FETCHERS_DATASETS[fetcher].keys():                                
                print(dataset_code)
            print("----------------------------------------------------")
        
if __name__ == "__main__":
    main()    
