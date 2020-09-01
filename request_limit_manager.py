"""pandadocument.py implements basic Request Limit Managers:
 - AbstractRequestLimitManager
 - NoLimitRequestLimitManager
 - SleepRequestLimitManager
 More about limits can be found here https://developers.pandadoc.com/reference#limits"""

__author__ = "Kostyantyn Ovechko"
__copyright__ = "Copyright 2020, Zxscript"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "kos@zxscript.com"
__status__ = "Production"


from time import sleep
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


class SleepRequestLimitManager(AbstractRequestLimitManager):
    """ 6 seconds should produce less than 10 requests per minutes, which should be ok for sandbox
    When calling from a single thread we can limit number of requests by just adding a delay between them."""
    __limiting_delay_seconds = 6

    def get_request_permission(self):
        print("Waiting for {retry_delay} seconds...".format(retry_delay=self.__class__.__limiting_delay_seconds))
        sleep(self.__class__.__limiting_delay_seconds)
        return True
