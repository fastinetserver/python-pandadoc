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