from typing import Union


class DumpPassword(object):
    __current_password: Union[bytes, None] = None

    def __init__(self, password: bytes):
        self.password = (
            bytes(password, encoding="utf-8")
            if not isinstance(password, bytes)
            else password
        )
        self._active = False

    def __enter__(self):
        if DumpPassword.__current_password is None:
            DumpPassword.__current_password = self.password
            self._active = True
        else:
            raise SyntaxError("There is already another encrypted dump context active!")

    def __exit__(self, type, value, traceback):
        if self._active:
            DumpPassword.__current_password = None
            self._active = False

    @classmethod
    def get(cls) -> bytes:
        if cls.__current_password is not None:
            return cls.__current_password
        else:
            raise SyntaxError("There is no encrypted dump context active!")
