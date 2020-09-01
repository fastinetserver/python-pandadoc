from time import sleep
from .request_limit_manager import AbstractRequestLimitManager


class SleepRequestLimitManager(AbstractRequestLimitManager):
    """ 6 seconds should produce less than 10 requests per minutes, which should be ok for sandbox
    When calling from a single thread we can limit number of requests by just adding a delay between them."""
    __limiting_delay_seconds = 6

    def get_request_permission(self):
        print("Waiting for {retry_delay} seconds...".format(retry_delay=self.__class__.__limiting_delay_seconds))
        sleep(self.__class__.__limiting_delay_seconds)
        return True
