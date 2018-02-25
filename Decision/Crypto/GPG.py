import gpg
from . import Generic
from ..Utility import Log

logger = Log.getLogger(__name__)

def context():
    return gpg.Context(armor=True)

class Identity(Generic.Identity):
    """
    Specialized Identity for gpg
    """
    def getKeys(self):
        with context() as c:
            try:
                keylist = list(c.keylist(str(self.email)))
                logger.debug("Found {} keys for identity {}".format(len(keylist),self.email))
                return keylist
            except Exception as e:
                logger.exception("Function keylist for identity {} of context threw an exception: {}".format(self.email,e))
                return None


class Provider:
    """
    Provider for the usage of GnuPG for the needed cryptographic operations
    """

    def __init__(self):
        self.amor = True

    def getKeysWhichCanEncrypt(self,identity):
        if isinstance(identity, Identity):
            keys = identity.getKeys()
            enabledKeys = []
            # See that the keys have a subkey which can actually encrypt
            with context() as c:
                for key in keys:
                    if any(subkey.can_encrypt for subkey in key.subkeys):
                        enabledKeys.append(key)
                if len(enabledKeys) > 0:
                    logger.debug("Found {} encryption enabled keys for identity {}".format(len(enabledKeys),identity.name))
                    return enabledKeys
                else:
                    logger.info("There was no encryption-enabled key found for identity {}".format(identity.name))
                    return None
        else:
            logger.warning("Identity has to be of type GPG.Identity and not {}".format(type(identity)))
            return None

    def encrypt(self, message,recipients):
        if isinstance(recipients, Identity): # We generously accept single arguments also. ;-)
            recipients = [recipients]
        targetKeys = []
        for recipient in recipients:
            keys = self.getKeysWhichCanEncrypt(recipient)
            if keys is not None:
                targetKeys += keys
            else:
                raise Exception("No keys found!")
        if len(targetKeys) > 0:
            ciphertext = str()
            with context() as c:
                try:
                    return c.encrypt(message.encode(), recipients=targetKeys) # String has to be properly encoded or we get in trouble
                except gpg.errors.InvalidRecipients as e:
                    logger.error("Encryption failed for key(s): {}".format(e))
                    return None

    def decrypt(self, message, adressees):
        pass

    def sign(self, message, senders):
        pass

    def verify(self, message, signature, signees):
        pass
