from multiprocessing import Process
import time
try:
    from .cfg import parse
    from .rabbit import Rabbit
    from .function_wrapper import FunctionWrapper
except Exception:
    from cfg import parse
    from rabbit import Rabbit
    from function_wrapper import FunctionWrapper


def worker(rabbit_cfg, function):
    f = FunctionWrapper(
        function['module_path'], 
        function['module_name'], 
        function['function_name']
    )
    r = Rabbit(
        function=f,
        exchange=function['exchange'],
        queue=function['queue'], 
        routing_key=function.get('routing_key'),
        host=rabbit_cfg.get('host'),
        port=rabbit_cfg.get('port'),
        userid=rabbit_cfg.get('userid'),
        password=rabbit_cfg.get('password'),
        durable=rabbit_cfg.get('durable', True)
    )
    r.connect()
    r.declare()
    r.consume()


if __name__ == '__main__':

    configuration = parse()
    rabbit_cfg = configuration['rabbitmq']
    functions = configuration['functions']
    processes = {}

    for function in functions:
        p = Process(target=worker, args=(rabbit_cfg, function))
        p.start()
        processes[function['function_name']] = p

    while True:
        for p_name, process in processes.items():
            if not process.is_alive():
                for n, p in processes.items():
                    p.terminate()
                raise ValueError('%s crashed. Stopping the rabbit_binder.' % p_name)
        time.sleep(1)
