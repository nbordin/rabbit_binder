# RabbitMQ binder

This module, provided a .yml file, binds Python functions to RabbitMQ queues.
After the installation and the creation of a `rabbit_binder.yml` file, it can be run from the folder containing the configuration file as:

```shell
python3 -m rabbit_binder
```

Each function defined in the `rabbit_binder.yml` will consume a RabbitMQ queue on a different process. If one of the queue crashes, all the process will be terminated.

# Installation

Requirements:
- `pika==1.0.1`
- `PyYAML==5.1`

```shell
pip3 install setuptools install
```

# rabbit_binder.yml

**Example**:

```yml
rabbitmq:
  host: localhost # default (can be omitted)
  port: 5672 # default (can be omitted)
  userid: guest # default (can be omitted)
  password: guest # default (can be omitted)
functions:
  - module_path: /path/to/module # required
    module_name: module_name # required
    function_name: function_name # required
    exchange: exchange_name # required
    queue: queue_name # required
    routing_key: routing_key # it can be omitted
```

* `rabbitmq`: general configuration of RabbitMQ:
    * `host`: RabbitMQ host address (`localhost` is the default and it can be omitted).
    * `port`: RabbitMQ port (`5672` is the default and it can be omitted).
    * `userid`: RabbitMQ username (`guest` is the default and it can be omitted).
    * `password`: RabbitMQ password (`guest` is the default and it can be omitted).

* `functions`: list of function-queue bindings:
    * `module_path`: path to Python module containing the module.
    * `module_name`: name of Python module containing the function.
    * `function_name`: name of Python function consuming the queue's messages.
    * `exchange`: name of RabbitMQ's exchange.
    * `queue`: name of RabbitMQ's queue.
    * `routing_key`: name of queue's routing_key (if not set `queue = routing_key`).
