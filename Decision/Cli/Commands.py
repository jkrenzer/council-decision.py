import configargparse

import Decision.Utility.Log as Log

class Command:

    name = None

    defaultConfigFiles = [
        '/etc/council/decision.conf',
        '~/.council/decision.conf'
    ]

    description = ""

    epilog = "For more information or if you want to contribute, please visit: \
    https://github.com/jkrenzer/council-decisions.py."

    parser = configargparse.ArgParser(
        default_config_files=defaultConfigFiles,
        prog=name,
        description=description,
        epilog=epilog)

    def __call__(self):
        logger = Log.getLogger(__name__)
        logger.warning("Command '%s' is not implemented yet." % self.name)

    def _defaultChildParser(self,child,group=None):
        if group is None:
            group = self.parser.add_subparsers()
        return group.add_parser(child.name,help=child.description)

    def addSubcommand(self,child,*,parser=None,group=None):
        if parser is None:
            parser = self._defaultChildParser(child,group)
        child.parser = parser
        instance = child()
        instance.parser.set_defaults(func=instance.proxy)

    def proxy(self,arguments):
        self.arguments = arguments
        self.__call__()


    def parse(self):
        self.arguments = self.parser.parse_args()
        self()
        self.arguments.func(self.arguments)
