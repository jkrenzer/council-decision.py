import getpass
import logging

from .Help import Help
from .Version import Version
from .Utility import Arguments as ArgHelper
from .Commands import Command
from Decision.Utility import Log


class Main(Command):

    name="decision"

    description="Council-Decision is a secure and anonymous voting system written in\
     Python3."

    def __init__(self):
        # Setup the commandline and config-file arguments
        commands = self.parser.add_subparsers(description="Possible commands which can\
                                              be issued by the user.")
        self.addSubcommand(Help,group=commands)
        self.addSubcommand(Version,group=commands)

        self.parser.add('-c', '--config', is_config_file=True, help='Configuration file')

        # Logging options.
        self.parser.add('-q', '--quiet', help='set logging to CRITICAL',
                        action='store_const', dest='logLevel',
                        const=Log.Level.CRITICAL, default=Log.Level.STANDARD)
        self.parser.add('-l', '--logFile', help='set a filepath to log to. Filelogging is deactivated if empty.',
                         dest="logFile", default=None)
        self.parser.add('-d', '--logLevel', help='set the loglevel of the logfile',
                        dest='logLevel', default=Log.Level.STANDARD)
        self.parser.add('-v', '--verbosity', help='set the loglevel of the console',
                        dest='verbosity', default=Log.Level.STANDARD)



    def __call__(self):
        # Setup logging.
        logger = Log.getLogger(None)
        logger.setLevel(-1)

        # Create and add handlers
        logStdErrHandler = logging.StreamHandler()
        if Log.getLogLevel(self.arguments.verbosity) == Log.Level.DEBUG:
            logStdErrHandler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
        else:
            logStdErrHandler.setFormatter(logging.Formatter('%(levelname)s:   %(message)s'))
        logStdErrHandler.setLevel(Log.getLogLevel(self.arguments.verbosity))
        logger.addHandler(logStdErrHandler)

        if self.arguments.logFile is not None:
            logFileHandler = logging.FileHandler(self.arguments.logFile)
            logFileHandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
            logFileHandler.setLevel(Log.getLogLevel(self.arguments.logLevel))
            logger.addHandler(logFileHandler)

        # Start logging
            logger.debug('Logging configured. There are %s handlers configured.' % len(logger.handlers))
        # Log configuration options
        for line in self.parser.format_values().split('\n'):
            logger.debug(line)
