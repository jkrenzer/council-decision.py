from . import Commands
from .Utility.Ui import tell, ask

class Version(Commands.Command):

    name="version"

    description="Show detailed version information."

    def __init__(self):
        self.parser.add('-f','--format', help='Which format to display version in.',
                        default='short', choices=['short','long'], dest='format')

    def __call__(self):
        if self.arguments.format == 'long':
            tell('One day this will display a LONG version info')
        else:
            tell('One day this will display a short version info')
