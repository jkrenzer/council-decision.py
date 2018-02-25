
class Identity:
    """ Class describing a generic identity. An identity can have
multiple sub-Ids which use different crypto-systems for verification and
secrecy. """

    type = 'generic'

    def __init__(self, name, email, jid=None):
        self.name = name
        self.email = email
        self.jid = jid

    def getKeys(self):
        pass

    def getSubIDs(self, type=None):
        pass
