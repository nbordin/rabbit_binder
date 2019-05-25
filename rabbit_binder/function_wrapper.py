import sys


class FunctionWrapper():

    module_name = None
    function_name = None
    function = None

    def __init__(self, module_path, module_name, function_name):
        self.module_name = module_name
        self.function_name = function_name
        sys.path.append(module_path)
        module = __import__(module_name)
        self.function = getattr(module, function_name)

    def __str__(self):
        return 'Module: ' + self.module_name + '. Function: ' + self.function_name

    def run(self, message):
        self.function(message)
