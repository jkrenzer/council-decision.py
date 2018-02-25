import logging
import getpass



def getActionsByDest(argp):
    destDict = {}
    for action in argp._actions:
        destDict.update({action.dest: action})
    return destDict

def askMissingArgs(required, args, argp):
    missing = _getMissingArgs(required, args)
    actions = _getActionsByDest(argp)
    newArgs = []
    for arg in missing:
        if arg in actions.keys():
            action = actions[arg]
            val = input("Enter a value for {arg} ({help}) [{default}]:".format(arg=arg,help=action.help, default=action.default))
            newArgs.append("{} {}".format(action.option_strings[0], val))
    argp.parse_args(newArgs, namespace=args)

def getMissingArgs(requiredArgs, namespace):
    missing = set()
    for arg in set(requiredArgs):
        val = getattr(namespace, arg, None)
        if val is None:
            missing.add(arg)
    return missing
