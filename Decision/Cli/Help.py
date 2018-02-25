

from .Utility import Arguments
from . import Commands

class Help(Commands.Command):

    name="help"

    description="Show detailed help about commands."

    def __init__(self):
        self.parser.add('command', help='Command you want to learn about.')
