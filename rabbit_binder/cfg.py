import os
import yaml

FUNCTION_REQUIRED_KEYS = ['module_path', 'module_name', 'function_name', 'exchange', 'queue']

def parse():

    filepath = os.path.join(os.getcwd(), 'rabbit_binder.yml')
    if not os.path.isfile(filepath):
        raise FileNotFoundError('Cannot find rabbit_binder.yml')
    with open(filepath, 'r') as f:
        configuration = yaml.safe_load(f)

    if not 'rabbitmq' in configuration:
        configuration['rabbitmq'] = {}

    if not configuration.get('functions'):
        raise ValueError('No function to bind rabbit_binder.yml')
    
    for idx, function in enumerate(configuration['functions']):
        if not isinstance(function, dict):
            raise ValueError('Functions must be dictionaries')
        for k in FUNCTION_REQUIRED_KEYS:
            if not function.get(k):
                raise ValueError('%s must be set in function # %s' % (k, idx))

    return configuration
