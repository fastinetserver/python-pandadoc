from abc import ABC, abstractmethod


class RequestLimitManagerException(Exception):
    pass


class LimitManagerIsBusyException(RequestLimitManagerException):
    pass


class RequestLimitReachedException(RequestLimitManagerException):
    pass


class AbstractRequestLimitManager(ABC):
    __in_use = False

    def __init__(self, max_attempts=5, retry_delay=30, for_download=False):
        self.for_download = for_download
        if self.__in_use:
            raise LimitManagerIsBusyException('Release RequestLimit manager before trying again')
        else:
            self.__in_use = True
        self.max_attempts = max_attempts
        self.retry_delay = retry_delay

    @abstractmethod
    def get_request_permission(self):
        pass

    def __enter__(self):
        return self.get_request_permission()

    def __exit__(self, type, value, traceback):
        self.__in_use = False


class NoLimitRequestLimitManager(AbstractRequestLimitManager):
    def get_request_permission(self):
        return True

