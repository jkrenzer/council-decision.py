from unittest import TestSuite
from typing import List

from .crypto import tests as crypto_tests
from .data import tests as data_tests

test_cases = crypto_tests + data_tests


def load_tests(loader, tests, pattern: List[str] = ["*"]):
    suite = TestSuite()
    loader.testNamePatterns = pattern
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite
