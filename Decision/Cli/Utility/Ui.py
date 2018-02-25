from Decision.Utility import Log
import inspect
import logging
from getpass import getpass

Log.Level.IO = 5
logging.addLevelName(Log.Level.IO,'IO')

SECRET_OMITTED = "###SENSITIVE CONTENT OMITTED###"

def tell(message: str, secret=False):
    frame_records = inspect.stack()[1]
    calling_module = inspect.getmodulename(frame_records[1])
    logger = Log.getLogger(calling_module)
    print(message)
    if secret:
        message = SECRET_OMITTED
    logger.log(Log.Level.IO,"<< " + message)


def ask(prompt: str,*,secret=False,password=False):
    frame_records = inspect.stack()[1]
    calling_module = inspect.getmodulename(frame_records[1])
    logger = Log.getLogger(calling_module)
    if password:
        result = getpass(prompt)
    else:
        result = input(prompt)
    if not secret:
        logger.log(Log.Level.IO,"<< " + prompt)
        if not password:
            logger.log(Log.Level.IO,">> " + result)
        else:
            logger.log(Log.Level.IO,">> " + SECRET_OMITTED)
    else:
        logger.log(Log.Level.IO,"<< " + SECRET_OMITTED + " >> " + SECRET_OMITTED)
    return result

def askPassword(prompt: str):
    return ask(prompt,password=True)

def askSecret(prompt: str):
    return ask(prompt,secret=True)

def tellSecret(message: str):
    tell(message,secret=True)
