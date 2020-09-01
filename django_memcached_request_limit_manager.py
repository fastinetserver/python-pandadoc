import random
from time import sleep

from django.core.cache import cache

from .request_limit_manager import AbstractRequestLimitManager, RequestLimitReachedException

PANDADOC_REQUESTS_PER_MINUTE_QUOTA = 100
PANDADOC_REQUESTS_PER_MINUTE_DOWNLOAD_QUOTA = 20


class DjangoMemcachedRequestLimitManager(AbstractRequestLimitManager):
    def get_request_permission(self):
        # Set low priority for download - ONLY allow download within first 10 tokens
        limit = PANDADOC_REQUESTS_PER_MINUTE_DOWNLOAD_QUOTA if self.for_download else PANDADOC_REQUESTS_PER_MINUTE_QUOTA
        for attempt in range(0, self.max_attempts):
            if attempt > 0:
                print("Could NOT find a free token. Retrying after {retry_delay} seconds delay".format(
                    retry_delay=self.retry_delay))
                sleep(self.retry_delay)
            for idx in random.sample(range(0, limit), limit):
                key = 'pandadoc_token_{idx}'.format(idx=idx)
                # Beware we have some concurrency issue here - another process can acquire
                # the same resource during .get_or_set() method call and if it's lucky enough to generate
                # the same new_value. Hopefully, this won't happen too often. If unsure - consider
                # setting lower PANDADOC_REQUESTS_PER_MINUTE_QUOTA than what you have provided by PandaDoc
                new_value = random.randint(0, 99999999999999)
                old_value = cache.get_or_set(key, new_value, 60)
                if old_value == new_value:
                    print("Found free token at {key} value: {new_value}".format(key=key, new_value=new_value))
                    return True
        raise RequestLimitReachedException('Please try again later.')
