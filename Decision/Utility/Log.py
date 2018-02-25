import logging

class Level:
    from logging import CRITICAL, ERROR, INFO, DEBUG, NOTSET
    STANDARD = INFO

def getLogLevel(userLevel):
    if isinstance(userLevel, int):
        numericLevel = userLevel
    else:
        numericLevel = getattr(Level, userLevel.upper(), None)
    if numericLevel is None:
        print("Setting STANDARD")
        numericLevel = Level.STANDARD
    return numericLevel

def getLogger(name=__name__):
    logger = logging.getLogger(name)
    return logger
