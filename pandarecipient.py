"""pandarecipient.py implements Recipients as per https://developers.pandadoc.com/reference#new-document"""

__author__ = "Kostyantyn Ovechko"
__copyright__ = "Copyright 2020, Zxscript"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "kos@zxscript.com"
__status__ = "Production"


class Pandarecipient:
    def __init__(self, email: str, first_name: str, last_name: str, role: str):
        self.__email = email
        self.__first_name = first_name
        self.__last_name = last_name
        self.__role = role

    @property
    def as_dict(self):
        return {
            'email': self.__email,
            'first_name': self.__first_name,
            'last_name': self.__last_name,
            'role': self.__role,
        }

    @property
    def email(self):
        return self.__email

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def role(self):
        return self.__role