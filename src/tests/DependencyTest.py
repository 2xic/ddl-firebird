import unittest
from ..dependency.Dependency import Dependency
from ..FirebirdParser import FirebirdParser
import os
from .TestUtils import get_full_path

class DependencyTest(unittest.TestCase):
    def test_simple_dependency(self):
        content = None
        with open(get_full_path("examples/ProcedureOrder.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        dependency = Dependency(results)

        names = list(map(lambda x: x.name, dependency.get_procedure_dependency(
            "ismultiple"
        )))
        assert names == [
            "LOG",
            "ISMULTIPLE"
        ]

    def test_multiple_dependency(self):
        content = None
        with open(get_full_path("examples/TriggerProcedureOrder.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        dependency = Dependency(results)

        names = list(map(lambda x: x.name, dependency.get_procedure_dependency(
            "ismultiple"
        )))
        assert names == ['USERS', 'GET_COUNT', 'LOGG_OF_CONNECTION_ID', 'LOGS', 'LOG', 'ISMULTIPLE']

    def test_multiple_dependency_with_prune(self):
        content = None
        with open(get_full_path("examples/TriggerProcedureOrder.sql"), "r") as file:
            content = file.read()

        results = FirebirdParser(content).parse()
        dependency = Dependency(results)

        names = list(map(lambda x: x.name, dependency.get_procedure_dependency(
            "ismultiple",
            prune=True
        )))
        assert names == ['LOGS', 'LOG', 'ISMULTIPLE']


if __name__ == '__main__':
    unittest.main()
