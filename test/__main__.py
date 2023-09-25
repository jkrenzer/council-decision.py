from typer import Typer
from council_decision import logging
from unittest import TestLoader
from pathlib import Path
from . import load_tests
import sys


test_app = Typer()


@test_app.command()
def main(pattern: str = "*", verbose: int = 0, log_level: str = "warn"):
    #    logging.basicConfig(level=logging.DEBUG)

    tests = TestLoader().loadTestsFromModule(sys.modules[__name__], pattern=pattern)

    # Set loglevel
    logging.basicConfig(level=logging.log_levels[log_level.lower()])

    from unittest import TextTestRunner

    testRunner = TextTestRunner(verbosity=verbose)
    testRunner.run(tests)


if __name__ == "__main__":
    test_app()
