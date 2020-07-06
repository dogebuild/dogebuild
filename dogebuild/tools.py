from typing import Dict
from os import environ


class Environment:
    def __init__(self, variables: Dict[str, str]):
        self.variables = variables
        self.old_variables = {}

    def __enter__(self):
        for var, value in environ.items():
            self.old_variables[var] = value
        for var, value in self.variables.items():
            environ[var] = value

    def __exit__(self, exc_type, exc_val, exc_tb):
        for var in set(environ.keys()).union(self.old_variables.keys()):
            if var in environ and var not in self.old_variables:
                del environ[var]
            else:
                environ[var] = self.old_variables[var]
